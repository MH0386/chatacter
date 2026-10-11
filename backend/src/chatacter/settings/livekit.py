from pydantic import BaseModel, Field, SecretStr


class LiveKitSettings(BaseModel):
    """Connection to the LiveKit server.

    Defaults match the self-hosted dev server in the compose files (`livekit-server --dev`). Override them with
    `LIVEKIT__URL`, `LIVEKIT__API_KEY`, and `LIVEKIT__API_SECRET` for any other server.
    """

    url: str = Field(default="ws://localhost:7880", description="WebSocket URL of the LiveKit server")
    api_key: SecretStr = Field(default=SecretStr("devkey"))
    api_secret: SecretStr = Field(default=SecretStr("secret"))
