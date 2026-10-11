"""LiveKit voice agents that play a persona and hand off to each other."""

from dataclasses import dataclass
from textwrap import dedent

from livekit.agents import (
    NOT_GIVEN,
    Agent,
    ChatContext,
    NotGivenOr,
)
from livekit.agents.llm.chat_context import Instructions
from livekit.agents.llm.tool_context import Tool

from chatacter.ai.persona import Persona
from chatacter.settings import Settings


@dataclass(frozen=True)
class PersonaInfo:
    """How a persona introduces itself and behaves."""

    name: str
    description: str
    instructions: Instructions


DOC_QA = PersonaInfo(
    name="DocQA",
    description=dedent("""
        DocQA is a helpful assistant that can answer questions about the documents.
    """),
    instructions=Instructions(
        dedent("""
        In Arabic, You are DocQA, a helpful assistant that can answer questions about given documents.
        Always search the documents with File Search before answering questions about them.
        Answer only from what the search returns, and say so when the documents do not contain the answer.
        You can use the other tools provided to you to answer questions.
        """),
    ),
)

NAPOLEON_BONAPARTE = PersonaInfo(
    name="Napoleon Bonaparte",
    description=dedent("""
        Napoleon Bonaparte was a French military and political leader who conquered most of Europe in the early 19th century.
        He was known for his military genius and his ability to inspire his troops.
    """),
    instructions=Instructions(
        dedent(
            """
            In Arabic, You are Napoleon Bonaparte, a French military and political leader who conquered most of Europe in the early 19th century.
            You are known for your military genius and your ability to inspire your troops.
            You are a helpful assistant that can help with a variety of tasks.
            """,
        ),
    ),
)

PERSONAS: dict[Persona, PersonaInfo] = {
    Persona.DOC_QA: DOC_QA,
    Persona.NAPOLEON_BONAPARTE: NAPOLEON_BONAPARTE,
}


@dataclass(frozen=True)
class AgentConfiguration:
    """Settings shared by every persona in a session."""

    instructions: Instructions
    greet: bool = True


class PersonaAgent(Agent):
    """A voice agent that plays one persona.

    Tools shared by all personas belong on the `AgentSession`, so they stay connected across handoffs.
    """

    def __init__(
        self,
        settings: Settings,
        user_id: str,
        persona: Persona,
        tools: list[Tool],
        greet: bool = True,
        chat_ctx: NotGivenOr[ChatContext | None] = NOT_GIVEN,
    ) -> None:
        """Create the agent for a persona.

        Args:
            settings: Settings.
            user_id: User ID.
            persona: Persona to play.
            tools: Tools to use.
            greet: Whether to greet the user when the persona takes over the session.
            chat_ctx: Conversation carried over from the previous persona.

        """
        self.user_id = user_id
        self.persona = persona
        self.info = PERSONAS[persona]
        self.greet = greet
        self.settings = settings
        super().__init__(id=persona.value, instructions=self.info.instructions, chat_ctx=chat_ctx, tools=tools)

    async def on_enter(self) -> None:
        """Greet the user when this persona takes over the session."""
        if self.greet:
            await self.session.generate_reply(
                instructions=f"Greet the user in character as {self.info.name} and offer your help.",
            )
