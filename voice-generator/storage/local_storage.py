import os
from pathlib import Path

from .base import AudioStorage, SaveResult


class LocalStorage(AudioStorage):
    """Save audio files to the local filesystem.

    The output directory is configurable via the constructor (or through
    the OUTPUT_DIR env var when used via the factory in __init__.py).
    """

    def __init__(self, output_dir: str = "/tmp/voice-output") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        data: bytes,
        filename: str,
        content_type: str = "audio/wav",
    ) -> SaveResult:
        dest = self.output_dir / filename
        dest.write_bytes(data)
        return SaveResult(
            location=str(dest.resolve()),
            url=None,  # No public URL for local files
            content_type=content_type,
            backend="local",
        )
