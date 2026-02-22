import io
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from .base import AudioStorage, SaveResult


class S3Storage(AudioStorage):
    """Save audio files to AWS S3.

    Configuration is pulled from the constructor arguments, which are
    themselves populated from environment variables in config.py.

    A pre-signed URL (valid for *presign_ttl* seconds) is generated and
    returned in SaveResult.url so callers can share or redirect to it
    immediately without additional roundtrips.
    """

    def __init__(
        self,
        bucket: str,
        prefix: str = "voice-output/",
        region: str = "us-east-1",
        presign_ttl: int = 3600,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ) -> None:
        self.bucket = bucket
        self.prefix = prefix.rstrip("/") + "/"
        self.presign_ttl = presign_ttl
        self._s3 = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def save(
        self,
        data: bytes,
        filename: str,
        content_type: str = "audio/wav",
    ) -> SaveResult:
        key = f"{self.prefix}{filename}"
        self._s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=io.BytesIO(data),
            ContentType=content_type,
        )

        try:
            url = self._s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=self.presign_ttl,
            )
        except ClientError:
            url = None

        return SaveResult(
            location=f"s3://{self.bucket}/{key}",
            url=url,
            content_type=content_type,
            backend="s3",
        )
