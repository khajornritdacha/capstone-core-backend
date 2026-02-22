from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class TTSRequest:
    """Canonical request passed to every TTS model."""
    text: str
    voice: str = "default"
    speed: float = 1.0
    language: str = "a"
    # Future extensibility: add format, sample_rate, etc.
    extra: dict = field(default_factory=dict)


class TTSModel(ABC):
    """Abstract base class for all TTS backends.

    To add a new backend:
    1. Subclass TTSModel and implement `generate`.
    2. Register it in models/__init__.py under a unique key.
    """

    @abstractmethod
    def generate(self, request: TTSRequest) -> bytes:
        """Generate audio from *request* and return raw PCM/WAV bytes.

        The returned bytes must be a valid WAV file so callers can pipe them
        directly into a response or hand them to a storage backend.
        """
        ...

    def supported_voices(self) -> list[str]:
        """Optional: return a list of voice identifiers this model supports."""
        return []

    def supported_languages(self) -> list[str]:
        """Optional: return BCP-47 or model-specific language codes."""
        return []
