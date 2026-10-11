# Agent Guidelines for chatacter

## Build/Lint/Test Commands

### Installation

```bash
uv sync  # Install dependencies
```

### Building

```bash
uv build  # Build source and wheel distributions
```

### Execution

```bash
uv run chatacter dev  # Run the LiveKit agent worker in development mode (also: start, console)
```

### Linting & Formatting

```bash
uvx prek run --all-files  # Run all linters and formatting checks
```

### Testing

```bash
uv run pytest  # Run all tests
uv run pytest tests/test_app.py::test_app  # Run single test
```

## Code Style Guidelines

### General

- **Line length**: 120 characters
- **Indentation**: 4 spaces
- **Quote style**: Double quotes (`"`)
- **File encoding**: UTF-8
- **Architecture**: Follow a ports and adaptors pattern

### Imports

- Use `from __future__ import annotations` when needed
- Group imports: standard library, third-party, local
- Use `TYPE_CHECKING` for conditional imports
- Combine multiple imports from the same module (e.g., `from typing import Any, Sequence`)

### Type Hints

- Use type hints for all function parameters and return values
- Use `Self` for methods returning the same class instance
- Use `Sequence`, `list`, `dict` instead of bare generics
- Use `Path` from `pathlib` for file paths
- Use `Pydantic` models for data validation and configuration

### Naming Conventions

- **Functions/Methods**: `snake_case`
- **Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Private attributes**: `_leading_underscore`

### Error Handling

- Use specific exception types (e.g., `OSError`, `ValueError`, `ValidationError`)
- Log errors with appropriate levels (`logger.error`, `logger.warning`)
- Use try/except blocks with meaningful error messages

### Async/Await

- Use `async def` for coroutines
- Use `await` for async operations
- Return `AsyncGenerator` from `collections.abc` for streaming responses

### Frameworks & Tools

- Use `livekit-agents` for the voice session, persona agents, handoffs, tools, and MCP toolsets
- Do not add Pydantic AI, LangChain, or a self-hosted vector database; document search uses Gemini File Search through
  `livekit.plugins.google.tools.FileSearch`
- Use `pydantic` and `pydantic-settings` for configuration management

### Documentation

- Use docstrings for all public functions, classes, and modules
- Follow a Google-style docstring format
- Document parameters, return values, and exceptions

### Logging

- Import logger from module settings
- Use appropriate log levels: `debug`, `info`, `warning`, `error`
- Include relevant context in log messages

### Testing Guidelines

- Use `pytest` framework
- Test functions named `test_*`
- Use descriptive assertions
- Mock external dependencies when needed

## Learned User Preferences

- Prefer the official MCP Python SDK (`streamable_http_client` + `ClientSession.send_ping`) for MCP reachability checks
  over raw TCP/socket probes.
- Prefer built-in framework helpers (for example LiveKit `MCPToolset`) or the official MCP SDK over ad-hoc utilities;
  review changes for existing library solutions before writing custom code.
- Remote MCP servers should be optional at startup: skip unreachable servers and continue booting rather than failing
  the app lifespan.
- Prefer framework-agnostic package names for process assembly (for example `service` over `agentos` or FastAPI-oriented
  names).

## Learned Workspace Facts

- chatacter is a LiveKit Agents voice worker using the Gemini Live realtime model; use one `MCPToolset` per remote server.
- Package layout: `ai/` builds the model, MCP toolsets, File Search tool, and persona agents; `core/`
  holds the logger and shared utilities; `service/` assembles everything into a LiveKit `AgentServer` via
  `setup_service`.
- Personas are `PersonaInfo` values in `chatacter.ai.agent` played by `PersonaAgent`; the `switch_persona` tool hands off
  between them, and dispatch metadata such as `{"persona": "doc_qa"}` picks the starting persona.
- Shared tools (MCP toolsets, Gemini `FileSearch`) live on the `AgentSession` so they survive persona handoffs.
- Documents are indexed into a Gemini File Search store with `scripts/upload_documents.py`; set the store in
  `FILE_SEARCH__STORE_NAMES` as a JSON list. Document search is optional: without it the worker starts without
  `FileSearch`.
- Two clients mirror each other: a Next.js web client in `ui/` (pnpm, LiveKit agents-ui starter) and a Flutter app in
  `flutter/`. Both default to the self-hosted LiveKit server (`ws://localhost:7880`), dispatch the `chatacter` agent with
  the picked persona as metadata, and have a paperclip button that sends documents as byte streams on the `documents`
  topic; `DocumentUploads` in `chatacter.ai.knowledge` indexes them into the first configured store and the agent
  announces when each one is ready.
- Running the worker needs a LiveKit server. Both compose files run a self-hosted one in dev mode (`devkey` /
  `secret`, media advertised on `127.0.0.1`); in `docker-compose.yaml` the `chatacter` container shares the `livekit`
  network namespace so `127.0.0.1` reaches it. `LiveKitSettings` defaults to that server; use `LIVEKIT__URL`,
  `LIVEKIT__API_KEY`, `LIVEKIT__API_SECRET` for any other (the worker ignores unprefixed `LIVEKIT_*` variables).
- Default remote MCP endpoints are voice on `http://localhost:7861/gradio_api/mcp` and video on
  `http://localhost:7862/gradio_api/mcp/?tools=generate_video_mcp`; additional servers come from `extra_mcp_servers`.
- `Settings` uses pydantic-settings with `env_nested_delimiter="__"`; nested fields use `__` (for example
  `AGENT__DEBUG_MODE`), and list fields like `extra_mcp_servers` are JSON env values.
- `setup_mcp_tools` probes MCP servers when each session starts and only attaches the reachable ones, so a server that
  comes up later is used by the next session without restarting the worker.
- `docker-compose-dev.yaml` can run the LiveKit server and the voice and video generator MCP services used in local
  development.
- `chatacter/__main__.py` builds a module-level `server` (`AgentServer`) so `lk agent dev .\src\chatacter\__main__.py` can
  discover it; `uv run chatacter dev` reuses it. The `lk` CLI needs its own credentials (a saved `lk project` or
  single-underscore `LIVEKIT_URL` / `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET`).
- `PYTHONUTF8=1` is set in `mise.toml` and `.envrc` so LiveKit logs don't fail on non-ASCII transcripts on Windows.
