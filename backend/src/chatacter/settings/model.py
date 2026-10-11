from google.genai.types import Modality, ThinkingLevel
from livekit.plugins.google.realtime import Voice
from pydantic import BaseModel, Field, SecretStr


class ModelSettings(BaseModel):
    """Settings for the Gemini Live model.

    Without an API key, it falls back to the `GOOGLE_API_KEY` environment variable.
    """

    name: str = Field(default="gemini-3.8-live")
    api_key: SecretStr | None = Field(default=None)
    voice: Voice = Field(default="Puck")
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    modalities: list[Modality] = Field(default=[Modality.AUDIO])
    thinking_level: ThinkingLevel = Field(default=ThinkingLevel.MEDIUM)
