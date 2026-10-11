from pydantic import BaseModel, Field, PositiveInt

from chatacter.ai.persona import Persona


class AgentSettings(BaseModel):
    """Settings for the LiveKit agent session."""

    name: str = Field(default="chatacter", description="Agent name used for explicit dispatch to rooms")
    persona: Persona = Field(
        default=Persona.NAPOLEON_BONAPARTE,
        description="Persona used when the dispatch metadata does not choose one",
    )
    greet: bool = Field(default=True, description="Whether a persona greets the user when it takes over")
    max_tool_steps: PositiveInt = Field(default=3, description="Maximum consecutive tool calls per turn")
