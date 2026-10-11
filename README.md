# **chatacter**: App part of the Chatacter Backend

[![Build](https://github.com/MH0386/chatacter/actions/workflows/build.yaml/badge.svg)](https://github.com/MH0386/chatacter/actions/workflows/build.yaml)
[![CI Tools](https://github.com/MH0386/chatacter/actions/workflows/ci_tools.yaml/badge.svg)](https://github.com/MH0386/chatacter/actions/workflows/ci_tools.yaml)
[![CodeQL](https://github.com/MH0386/chatacter/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/MH0386/chatacter/actions/workflows/github-code-scanning/codeql)
[![Dependabot Updates](https://github.com/MH0386/chatacter/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/MH0386/chatacter/actions/workflows/dependabot/dependabot-updates)
[![Release](https://github.com/MH0386/chatacter/actions/workflows/release.yaml/badge.svg)](https://github.com/MH0386/chatacter/actions/workflows/release.yaml)
[![Test](https://github.com/MH0386/chatacter/actions/workflows/test.yaml/badge.svg)](https://github.com/MH0386/chatacter/actions/workflows/test.yaml)

## Environment Variables

The configuration of the server is done using environment variables:

| Name                       | Description                      | Required | Default Value                              |
|:---------------------------|:---------------------------------|:--------:|:-------------------------------------------|
| `LIVEKIT__URL`             | LiveKit server WebSocket URL     |    ✘     | `ws://localhost:7880`                      |
| `LIVEKIT__API_KEY`         | LiveKit API key                  |    ✘     | `devkey`                                   |
| `LIVEKIT__API_SECRET`      | LiveKit API secret               |    ✘     | `secret`                                   |
| `MODEL__NAME`              | Gemini Live model for voice      |    ✘     | `gemini-3.8-live`                          |
| `MODEL__API_KEY`           | Gemini API key                   |    ✘     | `GOOGLE_API_KEY` env var                   |
| `MODEL__VOICE`             | Gemini Live voice                |    ✘     | `Puck`                                     |
| `MODEL__TEMPERATURE`       | Model temperature (0.0-1.0)      |    ✘     | `0.0`                                      |
| `AGENT__NAME`              | Agent name for room dispatch     |    ✘     | `chattr`                                   |
| `AGENT__PERSONA`           | Default starting persona         |    ✘     | `napoleon_bonaparte`                       |
| `SHORT_TERM_MEMORY__URL`   | Redis URL for memory store       |    ✘     | `redis://localhost:6379`                   |
| `FILE_SEARCH__STORE_NAMES` | Gemini File Search stores (JSON) |    ✘     | `[]` (document search disabled)            |
| `FILE_SEARCH__TOP_K`       | Chunks retrieved per search      |    ✘     | Gemini default                             |
| `FILE_SEARCH__MAX_UPLOAD_MB` | Largest document the UI can upload |  ✘     | `100`                                      |
| `VOICE_GENERATOR_MCP__URL` | MCP service for audio generation |    ✘     | `http://localhost:8001/gradio_api/mcp/sse` |
| `VIDEO_GENERATOR_MCP__URL` | MCP service for video generation |    ✘     | `http://localhost:8002/gradio_api/mcp/sse` |
| `DIRECTORY__ASSETS`        | Base assets directory            |    ✘     | `./assets`                                 |
| `DIRECTORY__LOG`           | Log files directory              |    ✘     | `./logs`                                   |
| `DIRECTORY__IMAGE`         | Image assets directory           |    ✘     | `./assets/image`                           |
| `DIRECTORY__AUDIO`         | Audio assets directory           |    ✘     | `./assets/audio`                           |
| `DIRECTORY__VIDEO`         | Video assets directory           |    ✘     | `./assets/video`                           |
