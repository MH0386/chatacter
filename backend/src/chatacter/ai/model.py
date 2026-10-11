"""Gemini Live model construction for the voice session."""

from livekit.agents import NOT_GIVEN
from livekit.plugins.google.realtime import RealtimeModel

from chatacter.core.logger import get_logger
from chatacter.settings import ModelSettings

logger = get_logger()


def setup_model(model: ModelSettings) -> RealtimeModel:
    """Build a Gemini Live model for a LiveKit agent session.

    Args:
        model: Model name, voice, API key, and sampling options.

    Returns:
        A Gemini Live realtime model. No network call is made here.

    Raises:
        ValueError: When the model name is missing.
    """
    if not model.name:
        message = "Model name is missing. Set it with `MODEL__NAME`"
        raise ValueError(message)
    logger.info("Initializing Gemini Live model %s", model.name)
    return RealtimeModel(
        model=model.name,
        api_key=model.api_key.get_secret_value() if model.api_key else NOT_GIVEN,
        voice=model.voice,
        temperature=model.temperature,
        modalities=model.modalities,
        # thinking_config=ThinkingConfig(thinking_level=model.thinking_level),
    )
