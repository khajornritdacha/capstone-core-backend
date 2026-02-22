from .base import AudioStorage, SaveResult
from .local_storage import LocalStorage
from .s3_storage import S3Storage


def get_storage(name: str) -> AudioStorage:
    """Return a configured storage backend by name.

    Supported names: ``"local"``, ``"s3"``.
    Configuration values are read from the application config (config.py).
    """
    import config  # local import to avoid circular dependency at module level

    print(f"get_storage: name={name}")

    if name == "local":
        return LocalStorage(output_dir=config.LOCAL_OUTPUT_DIR)

    if name == "s3":
        return S3Storage(
            bucket=config.S3_BUCKET,
            prefix=config.S3_PREFIX,
            region=config.S3_REGION,
            presign_ttl=config.S3_PRESIGN_TTL,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID or None,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY or None,
        )

    raise ValueError(
        f"Unknown storage backend '{name}'. Available: local, s3"
    )


__all__ = ["AudioStorage", "SaveResult", "LocalStorage", "S3Storage", "get_storage"]
