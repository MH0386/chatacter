"""Input checks that run before the model sees user text."""

INJECTION_PATTERNS: tuple[str, ...] = (
    "ignore previous instructions",
    "ignore your instructions",
    "you are now a",
    "forget everything above",
    "developer mode",
    "override safety",
    "disregard guidelines",
    "system prompt",
    "jailbreak",
    "act as if",
    "pretend you are",
    "roleplay as",
    "simulate being",
    "bypass restrictions",
    "ignore safeguards",
    "admin override",
    "root access",
    "forget everything",
)

INJECTION_MESSAGE = "Potential jailbreaking or prompt injection detected."


def is_prompt_injection(prompt: str) -> bool:
    """Return whether the prompt matches a known injection phrase.

    Args:
        prompt: User text about to be sent to a model or tool.

    Returns:
        True when the prompt contains an injection phrase.

    """
    lowered = prompt.lower()
    return any(pattern in lowered for pattern in INJECTION_PATTERNS)
