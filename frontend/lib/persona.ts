/** Name the Chattr worker registers with, used to dispatch it into the call. */
export const CHATTR_AGENT_NAME = "chattr";

/** A persona the Chattr agent can play, matching `chattr.ai.persona.Persona` on the worker. */
export interface Persona {
  /** Value the worker reads from the dispatch metadata. */
  id: string;
  /** Name shown in the picker. */
  label: string;
}

export const PERSONAS = [
  { id: "napoleon_bonaparte", label: "Napoleon" },
  { id: "doc_qa", label: "DocQA" },
] as const satisfies readonly Persona[];

export type PersonaId = (typeof PERSONAS)[number]["id"];

export const DEFAULT_PERSONA_ID: PersonaId = "napoleon_bonaparte";

/** Builds the agent dispatch metadata that picks the persona the call starts with. */
export function personaDispatchMetadata(personaId: PersonaId): string {
  return JSON.stringify({ persona: personaId });
}
