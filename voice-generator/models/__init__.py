from .base import TTSModel, TTSRequest
from .kokoro_model import KokoroModel

_REGISTRY: dict[str, type[TTSModel]] = {
    "kokoro": KokoroModel,
}


def get_model(name: str) -> TTSModel:
    """Return an initialised TTS model by registry name."""
    cls = _REGISTRY.get(name)
    if cls is None:
        raise ValueError(
            f"Unknown TTS model '{name}'. Available: {list(_REGISTRY.keys())}"
        )
    return cls()
