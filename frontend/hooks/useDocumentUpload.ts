import { useCallback, useState } from "react";
import { useSessionContext } from "@livekit/components-react";

/** Byte stream topic the agent listens on for documents to index. */
export const DOCUMENTS_TOPIC = "documents";

/** Largest document the agent accepts, matching the worker's `FILE_SEARCH__MAX_UPLOAD_MB` default. */
export const MAX_DOCUMENT_BYTES = 100 * 1024 * 1024;

/**
 * Streams documents to the agent, which indexes them for document search.
 *
 * The agent says when a document is ready or why indexing failed. Problems before the agent
 * receives the document are reported through `onError`.
 */
export function useDocumentUpload(onError: (message: string) => void) {
  const { room, isConnected } = useSessionContext();
  const [isUploading, setIsUploading] = useState(false);

  const upload = useCallback(
    async (file: File) => {
      if (!isConnected) {
        onError("Connect to the agent before adding documents.");
        return;
      }
      if (file.size > MAX_DOCUMENT_BYTES) {
        onError(`${file.name} is larger than ${MAX_DOCUMENT_BYTES / (1024 * 1024)} MB.`);
        return;
      }

      setIsUploading(true);
      try {
        await room.localParticipant.sendFile(file, {
          topic: DOCUMENTS_TOPIC,
          mimeType: file.type || undefined,
        });
      } catch (error) {
        console.error(`Could not send document ${file.name}`, error);
        onError(`Could not send ${file.name}.`);
      } finally {
        setIsUploading(false);
      }
    },
    [room, isConnected, onError],
  );

  return { upload, isUploading };
}
