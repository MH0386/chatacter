import { App } from "@/components/app/app";
import { CHATTR_AGENT_NAME } from "@/lib/persona";

// Token source: the LiveKit Cloud development token server (LIVEKIT_TOKEN_SERVER_ID) if set,
// otherwise the included token endpoint, which defaults to the self-hosted LiveKit server.
const tokenServerId = process.env.LIVEKIT_TOKEN_SERVER_ID;

export default function Page() {
  return (
    <App
      tokenServerId={tokenServerId}
      tokenEndpoint="/api/token"
      agentName={process.env.AGENT_NAME || CHATTR_AGENT_NAME}
      isVideoInputSupported={true}
    />
  );
}
