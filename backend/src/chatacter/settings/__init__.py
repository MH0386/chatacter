"""Settings for the chatacter app."""

from typing import Literal

from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict

from chatacter.settings.agent import AgentSettings
from chatacter.settings.database import DatabaseSettings
from chatacter.settings.directory import DirectorySettings
from chatacter.settings.embeddings import EmbeddingsSettings
from chatacter.settings.file_search import FileSearchSettings
from chatacter.settings.livekit import LiveKitSettings
from chatacter.settings.logger import LoggerSettings
from chatacter.settings.mcp import (
    ExtraMCPServerSettings,
    VideoGeneratorMCPServerSettings,
    VoiceGeneratorMCPServerSettings,
)
from chatacter.settings.memory import MemorySettings
from chatacter.settings.model import ModelSettings

__all__ = [
    "AgentSettings",
    "DatabaseSettings",
    "DirectorySettings",
    "EmbeddingsSettings",
    "ExtraMCPServerSettings",
    "FileSearchSettings",
    "LiveKitSettings",
    "LoggerSettings",
    "MemorySettings",
    "ModelSettings",
    "VideoGeneratorMCPServerSettings",
    "VoiceGeneratorMCPServerSettings",
]


class Settings(BaseSettings):
    """Configuration for the chatacter app."""

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_parse_none_str="None",
        env_file=".env",
        extra="ignore",
    )

    directory: DirectorySettings = Field(default_factory=DirectorySettings, frozen=True)
    livekit: LiveKitSettings = Field(default_factory=LiveKitSettings)
    model: ModelSettings = Field(default_factory=ModelSettings)
    memory: MemorySettings = Field(default_factory=MemorySettings)
    file_search: FileSearchSettings = Field(default_factory=FileSearchSettings)
    voice_generator_mcp_server: VoiceGeneratorMCPServerSettings = Field(default_factory=VoiceGeneratorMCPServerSettings)
    video_generator_mcp_server: VideoGeneratorMCPServerSettings = Field(default_factory=VideoGeneratorMCPServerSettings)
    extra_mcp_servers: list[ExtraMCPServerSettings] = Field(default_factory=list)
    log: LoggerSettings = Field(default_factory=LoggerSettings)
    debug: bool = Field(default=False)
    host: str = Field(default="0.0.0.0")
    port: PositiveInt = Field(default=7860)
    checkpoint: Literal["runs", "tool-batch", "tools"] | None = Field(default=None)
    tracing: bool = Field(default=True)
    agent: AgentSettings = Field(default_factory=AgentSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    embeddings: EmbeddingsSettings = Field(default_factory=EmbeddingsSettings)


if __name__ == "__main__":
    from rich import print as rprint

    rprint(Settings().model_dump_json(indent=4))
