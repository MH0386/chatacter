"use client";

import { useCallback, useRef } from "react";
import { Loader, PaperclipIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toastAlert } from "@/hooks/useAgentErrors";
import { useDocumentUpload } from "@/hooks/useDocumentUpload";
import { cn } from "@/lib/shadcn/utils";

/** Round button that picks a document and streams it to the agent for document search. */
export function DocumentUploadButton({ className }: { className?: string }) {
  const inputRef = useRef<HTMLInputElement>(null);
  const showError = useCallback(
    (message: string) => toastAlert({ title: "Document not sent", description: message }),
    [],
  );
  const { upload, isUploading } = useDocumentUpload(showError);

  return (
    <div
      className={cn(
        "bg-background border-input/50 dark:border-muted rounded-[31px] border p-3 drop-shadow-md/3",
        className,
      )}
    >
      <input
        ref={inputRef}
        type="file"
        hidden
        onChange={(e) => {
          const file = e.target.files?.[0];
          e.target.value = "";
          if (file) upload(file);
        }}
      />
      <Button
        variant="outline"
        size="icon"
        disabled={isUploading}
        aria-label="Add document"
        title={isUploading ? "Sending document..." : "Add document"}
        onClick={() => inputRef.current?.click()}
        className="bg-accent hover:bg-foreground/10 rounded-full"
      >
        {isUploading ? <Loader className="animate-spin" /> : <PaperclipIcon />}
      </Button>
    </div>
  );
}
