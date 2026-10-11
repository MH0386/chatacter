"""Personas the agent can play."""

from enum import StrEnum, auto


class Persona(StrEnum):
    """A persona the agent can adopt."""

    DOC_QA = auto()
    NAPOLEON_BONAPARTE = auto()
