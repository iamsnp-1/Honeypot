from enum import Enum

class AgentPhase(Enum):
    HOOK = "hook"
    CLARIFICATION = "clarification"
    PARTIAL_COMPLIANCE = "partial_compliance"
    DELAY = "delay"
    EXIT = "exit"


PHASE_ORDER = [
    AgentPhase.HOOK,
    AgentPhase.CLARIFICATION,
    AgentPhase.PARTIAL_COMPLIANCE,
    AgentPhase.DELAY,
    AgentPhase.EXIT
]
