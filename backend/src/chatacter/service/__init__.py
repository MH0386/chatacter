"""Assemble the persona agents, Gemini Live, and tools into a LiveKit agent server."""

from asyncio import Lock
from json import JSONDecodeError, loads

from google.genai.errors import APIError
from livekit.agents import AgentServer, AgentSession, JobContext, TurnHandlingOptions, inference
from livekit.plugins import google

from chatacter.ai.agent import Persona, PersonaAgent
from chatacter.ai.knowledge import DocumentUploads, resolve_file_search_stores, setup_file_search
from chatacter.ai.model import setup_model
from chatacter.ai.tools import setup_mcp_tools
from chatacter.core.logger import get_logger
from chatacter.settings import FileSearchSettings, Settings

logger = get_logger()


def select_persona(metadata: str, default: Persona) -> Persona:
    """Pick the starting persona from dispatch metadata such as `{"persona": "doc_qa"}`.

    Args:
        metadata: Job dispatch metadata, usually JSON.
        default: Persona used when the metadata does not name a valid one.

    Returns:
        The persona that starts the session.

    """
    try:
        requested = loads(metadata).get("persona") if metadata else None
        print(metadata)
        print(requested)
    except JSONDecodeError, AttributeError:
        logger.warning("Ignoring dispatch metadata that is not a JSON object: %r", metadata)
        return default
    if requested in {persona.value for persona in Persona}:
        return Persona(requested)
    return default


def setup_service(settings: Settings) -> AgentServer:
    """Assemble the LiveKit agent server from settings.

    MCP servers are probed, and the Gemini Live connection is opened, for each room the worker joins.

    Args:
        settings: Application settings.

    Returns:
        An agent server to run with `livekit.agents.cli.run_app`.

    """
    mcp_servers_settings = [
        settings.voice_generator_mcp_server,
        settings.video_generator_mcp_server,
        *settings.extra_mcp_servers,
    ]
    server = AgentServer(
        ws_url=settings.livekit.url,
        api_key=settings.livekit.api_key.get_secret_value(),
        api_secret=settings.livekit.api_secret.get_secret_value(),
    )
    file_search_lock = Lock()
    resolved_file_search: FileSearchSettings | None = None

    async def get_file_search(settings: Settings) -> FileSearchSettings:
        """Resolve the File Search store once per worker, retrying on the next session if Gemini fails.

        Args:
            settings: Settings.

        Returns:
            File Search settings, without store names when the store could not be resolved.

        """
        nonlocal resolved_file_search
        async with file_search_lock:
            if resolved_file_search is None:
                try:
                    resolved_file_search = await resolve_file_search_stores(settings.file_search, settings.model)
                except (APIError, ValueError) as error:
                    logger.error("Starting without document search; File Search store unavailable: %s", error)
                    return settings.file_search
            return resolved_file_search

    @server.rtc_session(agent_name=settings.agent.name)
    async def entrypoint(ctx: JobContext) -> None:
        """Join a room and run the persona agent in it.

        Args:
            ctx: The job for the room the agent was dispatched to.

        """
        meta: dict[str, str] = {}
        if ctx.job.metadata:
            try:
                meta = loads(ctx.job.metadata)
            except JSONDecodeError:
                logger.warning("ctx.job.metadata was not valid JSON; using defaults")
        user_id = meta.get("user_id", "default_user_id")
        ctx.log_context_fields = {"user_id": user_id}
        ctx.proc.userdata["user_id"] = user_id
        logger.debug("Starting session in room %s as %s", ctx.room.name, user_id)

        mcp_tools = await setup_mcp_tools(mcp_servers_settings)

        file_search = await get_file_search(settings)
        file_search_tool = setup_file_search(file_search)
        session = AgentSession(
            turn_handling=TurnHandlingOptions(
                turn_detection=inference.TurnDetector(),
            ),
            llm=setup_model(settings.model),
            max_tool_steps=settings.agent.max_tool_steps,
            mcp_servers=mcp_tools,
        )
        persona = select_persona(ctx.job.metadata, Persona(settings.agent.persona))
        logger.info("Starting session in room %s as %s", ctx.room.name, persona.value)
        if file_search.store_names:
            DocumentUploads(settings.model, file_search).register(ctx.room, session)
        await session.start(
            PersonaAgent(
                user_id=user_id,
                persona=persona,
                tools=[google.tools.GoogleSearch(), *([file_search_tool] if file_search_tool else [])],
                greet=settings.agent.greet,
                settings=settings,
            ),
            room=ctx.room,
        )
        await ctx.connect()

    return server
