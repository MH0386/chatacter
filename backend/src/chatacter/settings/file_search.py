from pydantic import BaseModel, Field, PositiveInt


class FileSearchSettings(BaseModel):
    """Gemini File Search stores that the agent searches for document questions."""

    store_names: list[str] = Field(
        default_factory=list,
        description=(
            "File Search store resource names, such as `fileSearchStores/abc123`. When empty, the worker finds or "
            "creates the store named `store_display_name`."
        ),
    )
    store_display_name: str = Field(
        default="chatacter documents",
        description="Display name of the store the worker finds or creates when `store_names` is empty",
    )
    top_k: PositiveInt | None = Field(default=None, description="Maximum number of chunks to retrieve")
    metadata_filter: str | None = Field(default=None, description="Filter on document metadata, in AIP-160 syntax")
    max_upload_mb: PositiveInt = Field(
        default=100,
        description="Largest document, in megabytes, that users can upload from the UI. Gemini allows up to 100 MB.",
    )
