"""Remote MCP servers that are attached only when they answer."""

from asyncio import CancelledError, gather, wait_for
from collections.abc import Sequence

from livekit.agents.llm.mcp import MCPServer, MCPServerHTTP
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from chatacter.core.logger import get_logger
from chatacter.settings import ExtraMCPServerSettings, VideoGeneratorMCPServerSettings, VoiceGeneratorMCPServerSettings

logger = get_logger()

_INITIALIZE_TIMEOUT_SECONDS = 5.0

type MCPServerSettings = VoiceGeneratorMCPServerSettings | VideoGeneratorMCPServerSettings | ExtraMCPServerSettings


async def _is_server_reachable(server: MCPServerSettings) -> bool:
    """Return whether the MCP server completes the official handshake.

    Args:
        server: Remote MCP server to probe.

    Returns:
        True when the official MCP client can finish the handshake.
    """
    try:
        async with (
            streamable_http_client(str(server.url)) as (read, write, _),
            ClientSession(read, write) as session,
        ):
            await wait_for(session.initialize(), timeout=_INITIALIZE_TIMEOUT_SECONDS)
        return True
    except KeyboardInterrupt, SystemExit:
        raise
    except Exception, CancelledError:  # noqa: BLE001
        return False


async def setup_mcp_tools(mcps: Sequence[MCPServerSettings]) -> list[MCPServer]:
    """Return MCP toolsets for servers that accept a connection.

    Servers are probed when each session starts, so a server that comes up later is attached to the next session
    without restarting the worker.

    Args:
        mcps: Configured remote MCP servers.

    Returns:
        One toolset per reachable server, identified by the server name.
    """
    if not mcps:
        logger.info("No Remote MCP servers found.")
        return []

    probes = await gather(*(_is_server_reachable(mcp) for mcp in mcps))
    reachable = [mcp for mcp, is_reachable in zip(mcps, probes, strict=True) if is_reachable]
    not_reachable = [mcp.name for mcp, is_reachable in zip(mcps, probes, strict=True) if not is_reachable]

    if not_reachable:
        logger.warning("MCP servers %s are unreachable. Skipping.", not_reachable)
    if not reachable:
        logger.info("No reachable Remote MCP servers found.")

    return [MCPServerHTTP(str(mcp.url), transport_type="streamable_http") for mcp in reachable]
