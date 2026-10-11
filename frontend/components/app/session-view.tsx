"use client";

import React, { useState } from "react";
import { AnimatePresence, type MotionProps, motion } from "motion/react";
import { useAgent, useSessionContext, useSessionMessages } from "@livekit/components-react";
import { AgentChatTranscript } from "@/components/agents-ui/agent-chat-transcript";
import {
  AgentControlBar,
  type AgentControlBarControls,
} from "@/components/agents-ui/agent-control-bar";
import {
  type AudioVisualizerConfig,
  Fade,
} from "@/components/agents-ui/blocks/agent-session-view-01/components/agent-session-block";
import { TileLayout } from "@/components/agents-ui/blocks/agent-session-view-01/components/tile-view";
import { DocumentUploadButton } from "@/components/app/document-upload-button";
import { cn } from "@/lib/shadcn/utils";

const BOTTOM_VIEW_MOTION_PROPS: MotionProps = {
  variants: {
    visible: { opacity: 1, translateY: "0%" },
    hidden: { opacity: 0, translateY: "100%" },
  },
  initial: "hidden",
  animate: "visible",
  exit: "hidden",
  transition: { duration: 0.3, delay: 0.5, ease: "easeOut" },
};

const CHAT_MOTION_PROPS: MotionProps = {
  variants: {
    hidden: { opacity: 0, transition: { ease: "easeOut", duration: 0.3 } },
    visible: { opacity: 1, transition: { delay: 0.2, ease: "easeOut", duration: 0.3 } },
  },
  initial: "hidden",
  animate: "visible",
  exit: "hidden",
};

const SHIMMER_MOTION_PROPS: MotionProps = {
  variants: {
    visible: { opacity: 1, transition: { ease: "easeIn", duration: 0.5, delay: 0.8 } },
    hidden: { opacity: 0, transition: { ease: "easeIn", duration: 0.5, delay: 0 } },
  },
  initial: "hidden",
  animate: "visible",
  exit: "hidden",
};

interface SessionViewProps {
  /** Theme mode forwarded to the aura visualizer so its blend mode follows the theme. */
  themeMode?: "dark" | "light";
  /** Message shown above the controls before the first chat message. */
  preConnectMessage: string;
  /** Controls shown in the control bar. */
  controls: AgentControlBarControls;
  /** Visualizer style rendered in the main tile area. */
  audioVisualizer?: AudioVisualizerConfig;
}

/**
 * Agents UI `AgentSessionView_01` layout with a document upload button beside the control bar.
 *
 * Built from the registry pieces so `pnpm shadcn:install` keeps them up to date.
 */
export function SessionView({
  themeMode,
  preConnectMessage,
  controls,
  audioVisualizer,
  ref,
  className,
  ...props
}: React.ComponentProps<"section"> & SessionViewProps) {
  const session = useSessionContext();
  const { messages } = useSessionMessages(session);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const { state: agentState } = useAgent();

  return (
    <section
      ref={ref}
      className={cn(
        "@container/agent-session-block bg-background relative z-10 h-full w-full overflow-hidden",
        className,
      )}
      {...props}
    >
      <Fade top className="absolute inset-x-4 top-0 z-10 h-40" />
      <AnimatePresence>
        {isChatOpen && (
          <motion.div
            {...CHAT_MOTION_PROPS}
            className="absolute inset-x-0 top-0 bottom-[135px] overflow-hidden @md/agent-session-block:bottom-[170px]"
          >
            <AgentChatTranscript
              agentState={agentState}
              messages={messages}
              className="mx-auto max-w-2xl **:data-[slot=message-scroller-content]:p-4 **:data-[slot=message-scroller-content]:pt-40! @md/agent-session-block:**:data-[slot=message-scroller-content]:p-6"
            />
          </motion.div>
        )}
      </AnimatePresence>

      <TileLayout isChatOpen={isChatOpen} themeMode={themeMode} audioVisualizer={audioVisualizer} />

      <motion.div
        {...BOTTOM_VIEW_MOTION_PROPS}
        className="absolute inset-x-3 bottom-0 z-50 @md/agent-session-block:inset-x-12"
      >
        <AnimatePresence>
          {messages.length === 0 && (
            <motion.p
              key="pre-connect-message"
              {...SHIMMER_MOTION_PROPS}
              className="shimmer shimmer-duration-2000 text-muted-foreground pointer-events-none mx-auto block w-full max-w-2xl pb-4 text-center text-sm"
            >
              {preConnectMessage}
            </motion.p>
          )}
        </AnimatePresence>
        <div className="bg-background relative mx-auto flex max-w-2xl items-end gap-2 pb-3 @md/agent-session-block:pb-12">
          <AgentControlBar
            variant="livekit"
            controls={controls}
            isChatOpen={isChatOpen}
            isConnected={session.isConnected}
            onDisconnect={session.end}
            onIsChatOpenChange={setIsChatOpen}
            className="min-w-0 grow"
          />
          <DocumentUploadButton />
        </div>
      </motion.div>
    </section>
  );
}
