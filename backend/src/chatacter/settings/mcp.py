from pydantic import BaseModel, Field


class VoiceGeneratorMCPServerSettings(BaseModel):
    """Voice generator MCP server."""

    name: str = Field("voice_generator", description="Name of the MCP server instance")
    url: str = Field(
        "http://localhost:7861/gradio_api/mcp",
        description="URL of the Voice Generator MCP server instance",
    )


class VideoGeneratorMCPServerSettings(BaseModel):
    """Video generator MCP server."""

    name: str = Field("video_generator", description="Name of the MCP server instance")
    url: str = Field(
        "http://localhost:7862/gradio_api/mcp/?tools=generate_video_mcp",
        description="URL of the Video Generator MCP server instance",
    )


class ExtraMCPServerSettings(BaseModel):
    """An additional remote MCP server."""

    name: str = Field(..., description="Name of the MCP server instance")
    url: str = Field(..., description="URL of the Extra MCP server instance")
