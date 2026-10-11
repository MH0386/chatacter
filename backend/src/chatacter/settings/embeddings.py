from pydantic import BaseModel, Field, PositiveInt


class EmbeddingsSettings(BaseModel):
    """Settings for embeddings configuration.

    `embedding_dims` must match the size of the `embedding` vector column in the `memories` table.
    """

    embedding_model: str = Field(default="gemini-embedding-2")
    embedding_dims: PositiveInt = Field(default=768)
