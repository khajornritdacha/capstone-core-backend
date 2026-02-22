from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class SaveResult:
    """Returned by every storage backend after a successful save."""
    # Human-readable identifier: file path, S3 key, object ID, …
    location: str
    # Publicly (or pre-signed) accessible URL when available, else None
    url: Optional[str]
    # MIME type of the stored file
    content_type: str = "audio/wav"
    # Backend that performed the save
    backend: str = "unknown"


class AudioStorage(ABC):
    """Abstract interface for persisting generated audio.

    To add a new backend:
    1. Subclass AudioStorage and implement `save`.
    2. Register it in storage/__init__.py under a unique key.
    """

    @abstractmethod
    def save(
        self,
        data: bytes,
        filename: str,
        content_type: str = "audio/wav",
    ) -> SaveResult:
        """Persist *data* under *filename* and return a SaveResult."""
        ...
