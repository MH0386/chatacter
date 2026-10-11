"""Text embeddings through the Gemini embedding model.

Stored memories are embedded with the `RETRIEVAL_DOCUMENT` task type and search queries with `RETRIEVAL_QUERY`, which
Gemini tunes to land close to each other. Vectors are L2-normalized because Gemini only normalizes full-size
embeddings, and cosine search over truncated ones needs unit length.
"""

from typing import TYPE_CHECKING

from google import genai
from google.genai import types

from chatacter.core.logger import get_logger

if TYPE_CHECKING:
    from chatacter.settings import EmbeddingsSettings

logger = get_logger()


async def embed_contents(
    contents: list[types.Content],
    embeddings_settings: EmbeddingsSettings,
) -> list[types.ContentEmbedding] | None:
    """Embed contents, such as a memory before it is stored.

    Args:
        contents: Contents to embed.
        embeddings_settings: Embeddings settings.

    Returns:
        Embeddings for the contents.

    """
    if not contents:
        return []
    client = genai.Client()
    config = types.EmbedContentConfig(output_dimensionality=embeddings_settings.embedding_dims)
    result = await client.aio.models.embed_content(
        model=embeddings_settings.embedding_model,
        contents=contents,
        config=config,
    )
    return result.embeddings
