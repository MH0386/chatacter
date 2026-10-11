"""Document search through Gemini File Search, which runs on Google's servers."""

from asyncio import Task, create_task, sleep
from io import BytesIO, IOBase
from mimetypes import guess_type
from os import PathLike
from pathlib import PurePath

from google import genai
from google.genai import types
from google.genai.errors import APIError
from livekit import rtc
from livekit.agents import AgentSession
from livekit.plugins.google.tools import FileSearch

from chatacter.core.error import DocumentIndexingError
from chatacter.core.logger import get_logger
from chatacter.settings import FileSearchSettings, ModelSettings

logger = get_logger()

DOCUMENTS_TOPIC = "documents"
"""Byte stream topic the UI sends documents on."""

_POLL_SECONDS = 2.0
_GENERIC_MIME_TYPES = {"", "application/octet-stream"}


def setup_file_search(file_search: FileSearchSettings) -> FileSearch | None:
    """Build the Gemini File Search provider tool.

    Document search is optional: without configured stores, the agent runs without it.

    Args:
        file_search: Store names and retrieval options.

    Returns:
        A provider tool for the Gemini Live session, or None when no store is configured.
    """
    if not file_search.store_names:
        logger.warning("No File Search stores configured. Set `FILE_SEARCH__STORE_NAMES` to enable document search.")
        return None
    return FileSearch(
        file_search_store_names=file_search.store_names,
        top_k=file_search.top_k,
        metadata_filter=file_search.metadata_filter,
    )


async def resolve_file_search_stores(
    file_search_settings: FileSearchSettings, model_settings: ModelSettings
) -> FileSearchSettings:
    """Fill in the store names, finding or creating the store named `store_display_name` when none are configured.

    Args:
        model_settings: Model settings.
        file_search_settings: File Search settings, possibly without store names.

    Returns:
        The settings with at least one store name.

    Raises:
        APIError: When Gemini cannot list or create stores.
        ValueError: When Gemini returns a store without a name.
    """
    client = genai.Client(api_key=model_settings.api_key.get_secret_value() if model_settings.api_key else None)
    if file_search_settings.store_names:
        return file_search_settings
    display_name = file_search_settings.store_display_name
    async for store in await client.aio.file_search_stores.list():
        if store.display_name == display_name and store.name:
            logger.info("Using File Search store %s (%s)", store.name, display_name)
            return file_search_settings.model_copy(update={"store_names": [store.name]})
    store = await client.aio.file_search_stores.create(
        config=types.CreateFileSearchStoreConfig(display_name=display_name)
    )
    if not store.name:
        message = f"Gemini created the File Search store {display_name!r} without a name"
        raise ValueError(message)
    logger.info("Created File Search store %s (%s)", store.name, display_name)
    return file_search_settings.model_copy(update={"store_names": [store.name]})


def resolve_mime_type(name: str, mime_type: str) -> str | None:
    """Pick the MIME type to send to Gemini, guessing from the file name when the sender gave none.

    Args:
        name: File name, used to guess the type.
        mime_type: MIME type reported by the sender, possibly empty or generic.

    Returns:
        A specific MIME type, or None when it cannot be determined.
    """
    if mime_type not in _GENERIC_MIME_TYPES:
        return mime_type
    return guess_type(name)[0]


async def index_document(
    client: genai.Client,
    store_name: str,
    file: str | PathLike[str] | IOBase,
    *,
    display_name: str,
    mime_type: str | None = None,
) -> None:
    """Upload a document to a File Search store and wait until it is searchable.

    Args:
        client: Gemini API client.
        store_name: Store resource name, such as `fileSearchStores/abc123`.
        file: Path to the document, or its contents as a binary stream.
        display_name: Name shown for the document in the store and in citations.
        mime_type: MIME type of the document. Required for streams; inferred from the extension for paths.

    Raises:
        DocumentIndexingError: When Gemini fails to index the document.
    """
    operation = await client.aio.file_search_stores.upload_to_file_search_store(
        file_search_store_name=store_name,
        file=file,
        config=types.UploadToFileSearchStoreConfig(display_name=display_name, mime_type=mime_type),
    )
    while not operation.done:
        await sleep(_POLL_SECONDS)
        operation = await client.aio.operations.get(operation)
    if operation.error:
        message = f"Failed to index {display_name}: {operation.error}"
        raise DocumentIndexingError(message)


class DocumentUploads:
    """Index documents that users send over the room into the first configured File Search store.

    The UI sends each document as a byte stream on the `documents` topic. Once indexed, the agent tells the user the
    document is ready, and the session's `FileSearch` tool can find it right away.
    """

    def __init__(self, model_settings: ModelSettings, file_search: FileSearchSettings) -> None:
        """Create the upload handler.

        Args:
            model_settings: Model settings.
            file_search: Store names and upload limits. The first store receives uploads.

        Raises:
            ValueError: When no File Search store is configured.
        """
        self._client = genai.Client(
            api_key=model_settings.api_key.get_secret_value() if model_settings.api_key else None
        )
        if not file_search.store_names:
            message = "Document uploads need a File Search store. Set `FILE_SEARCH__STORE_NAMES`."
            raise ValueError(message)
        self._store_name = file_search.store_names[0]
        self._max_bytes = file_search.max_upload_mb * 1024 * 1024
        self._tasks: set[Task[None]] = set()

    def register(self, room: rtc.Room, session: AgentSession) -> None:
        """Start accepting documents sent to the room.

        Args:
            room: Room the agent joined.
            session: Session that announces the result to the user.
        """

        def on_stream(reader: rtc.ByteStreamReader, participant_identity: str) -> None:
            task = create_task(self._receive(reader, participant_identity, session))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

        room.register_byte_stream_handler(DOCUMENTS_TOPIC, on_stream)

    async def _receive(self, reader: rtc.ByteStreamReader, participant_identity: str, session: AgentSession) -> None:
        """Read one document from the room, index it, and tell the user how it went."""
        name = PurePath(reader.info.name).name or "document"
        logger.info("Receiving document %s from %s", name, participant_identity)
        try:
            data = await self._read(reader, name)
            await index_document(
                self._client,
                self._store_name,
                data,
                display_name=name,
                mime_type=resolve_mime_type(name, reader.info.mime_type),
            )
        except (rtc.StreamError, DocumentIndexingError, APIError) as error:
            logger.error("Could not add document %s: %s", name, error)
            session.generate_reply(
                instructions=f"Tell the user that the document {name!r} could not be added, and briefly why: {error}",
            )
            return
        logger.info("Indexed document %s into %s", name, self._store_name)
        session.generate_reply(
            instructions=f"Tell the user that the document {name!r} is ready and they can ask questions about it.",
        )

    async def _read(self, reader: rtc.ByteStreamReader, name: str) -> BytesIO:
        """Collect a byte stream into memory, enforcing the upload size limit.

        Raises:
            DocumentIndexingError: When the document is larger than the limit.
        """
        too_large = DocumentIndexingError(f"{name} is larger than {self._max_bytes // (1024 * 1024)} MB")
        if reader.info.size and reader.info.size > self._max_bytes:
            raise too_large
        buffer = BytesIO()
        async for chunk in reader:
            if buffer.tell() + len(chunk) > self._max_bytes:
                raise too_large
            buffer.write(chunk)
        buffer.seek(0)
        return buffer
