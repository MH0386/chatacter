"use client";

import { useTheme } from "next-themes";
import { ConnectionState } from "livekit-client";
import { AnimatePresence, motion } from "motion/react";
import { useAgent, useSessionContext } from "@livekit/components-react";
import { SessionView } from "@/components/app/session-view";
import { WelcomeView } from "@/components/app/welcome-view";
import type { PersonaId } from "@/lib/persona";

const MotionWelcomeView = motion.create(WelcomeView);
const MotionSessionView = motion.create(SessionView);

const VIEW_MOTION_PROPS = {
  variants: {
    visible: {
      opacity: 1,
    },
    hidden: {
      opacity: 0,
    },
  },
  initial: "hidden",
  animate: "visible",
  exit: "hidden",
  transition: {
    duration: 0.5,
    ease: "linear" as const,
  },
};

interface ViewControllerProps {
  isVideoInputSupported: boolean;
  personaId: PersonaId;
  onPersonaChange: (personaId: PersonaId) => void;
}

export function ViewController({
  isVideoInputSupported,
  personaId,
  onPersonaChange,
}: ViewControllerProps) {
  const { isConnected, connectionState, start } = useSessionContext();
  const isDisconnected = connectionState === ConnectionState.Disconnected;
  const agent = useAgent();
  const { resolvedTheme } = useTheme();

  return (
    <AnimatePresence mode="wait">
      {/* Welcome view */}
      {!isConnected && (
        <MotionWelcomeView
          key="welcome"
          {...VIEW_MOTION_PROPS}
          startButtonText={isDisconnected ? "Start call" : "Connecting"}
          onStartCall={start}
          personaId={personaId}
          onPersonaChange={onPersonaChange}
          isPersonaLocked={!isDisconnected}
        />
      )}
      {/* Session view */}
      {isConnected && (
        <MotionSessionView
          key="session-view"
          {...VIEW_MOTION_PROPS}
          preConnectMessage={
            agent.isConnected ? "Agent is listening, ask it a question" : "Waiting for agent"
          }
          controls={{
            leave: true,
            microphone: true,
            chat: true,
            camera: isVideoInputSupported,
            screenShare: isVideoInputSupported,
          }}
          audioVisualizer={{ type: "bar" }}
          themeMode={resolvedTheme === "dark" ? "dark" : "light"}
          className="fixed inset-0"
        />
      )}
    </AnimatePresence>
  );
}
