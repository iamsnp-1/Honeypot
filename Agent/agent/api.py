from .state import ConversationState
from .scenarios import SCENARIOS
from .intelligence import IntelligenceProfile
from .planner import AgentPlanner
import time


def process_message(session_state, incoming_text):
    """
    Main API function - processes scammer message and returns structured response
    """

    # ---- INITIALIZE SESSION ONCE ----
    if session_state.intelligence is None:
        session_state.intelligence = IntelligenceProfile()
        session_state.planner = AgentPlanner()
        session_state.persona = {
            "language": "English",
            "tone": "middle-class cautious",
            "tech_skill": "low",
            "fear_level": 0.3,
            "phase": session_state.phase.value
        }

    # ---- EXTRACT INTELLIGENCE FROM CURRENT MESSAGE ----
    session_state.intelligence.extract(incoming_text)

    # ---- APPEND SCAMMER MESSAGE (NO DUPLICATES) ----
    if not session_state.history or session_state.history[-1]["message"] != incoming_text:
        session_state.history.append({
            "timestamp": time.time(),
            "sender": "scammer",
            "message": incoming_text
        })

    # ---- INTENT DETECTION ----
    intent = session_state.planner.detect_intent(incoming_text)
    session_state.add_intent(intent)

    # ---- DELAY SCENARIO LOCKING UNTIL ENOUGH CONTEXT ----
    if session_state.scenario is None and session_state.turns >= 1:
        session_state.scenario = session_state.planner.select_scenario_from_evidence(
            incoming_text,
            intent
        )

    # ---- UPDATE PERSONA PHASE ----
    session_state.persona["phase"] = session_state.phase.value

    # ---- UPDATE PHASE BASED ON PRESSURE ----
    session_state.update_phase(intent)

    # ---- STRATEGY + REPLY GENERATION ----
    strategy = session_state.planner.choose_strategy(session_state)
    reply = session_state.planner.generate_reply(strategy, session_state)

    # ---- STORE AGENT REPLY ----
    session_state.history.append({
        "timestamp": time.time(),
        "sender": "agent",
        "message": reply
    })

    # ---- ENGAGEMENT CHECK ----
    engagement_complete = session_state.is_complete()

    # ---- FEAR PROGRESSION ----
    if "otp" in incoming_text.lower() or "upi" in incoming_text.lower():
        session_state.persona["fear_level"] = min(1.0, session_state.persona["fear_level"] + 0.1)
    else:
        session_state.persona["fear_level"] = min(1.0, session_state.persona["fear_level"] + 0.05)

    # ---- TURN INCREMENT ----
    session_state.turns += 1

    return {
        "reply": reply,
        "engagement_complete": engagement_complete,
        "intelligence": session_state.intelligence.to_dict(),
        "notes": session_state.intelligence.get_notes()
    }


# ---------------- APP ENTRY POINT ---------------- #

_AGENT_SESSIONS = {}

def agent_handle_message(session_id: str, message: str) -> dict:
    """
    Entry point for FastAPI app
    """
    if session_id not in _AGENT_SESSIONS:
        _AGENT_SESSIONS[session_id] = ConversationState(session_id)

    session_state = _AGENT_SESSIONS[session_id]
    return process_message(session_state, message)
