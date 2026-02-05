from .state import ConversationState
from .intelligence import IntelligenceProfile
from .planner import AgentPlanner
import time

# ---------------- CORE MESSAGE HANDLER ---------------- #

def process_message(session_state, incoming_text):
    """
    Main agent brain – single-turn, no loops, no repetition
    """

    text = incoming_text.lower()

    # -------- INIT (RUN ONCE) -------- #
    if session_state.intelligence is None:
        session_state.intelligence = IntelligenceProfile()
        session_state.planner = AgentPlanner()
        session_state.resolved_probes = set()
        session_state.turns = 0
        session_state.persona = {
            "fear_level": 0.3,
            "phase": session_state.phase.value
        }

    # -------- STORE SCAMMER MESSAGE -------- #
    session_state.history.append({
        "timestamp": time.time(),
        "sender": "scammer",
        "message": incoming_text
    })

    # -------- EXTRACT INTELLIGENCE -------- #
    session_state.intelligence.extract(incoming_text)

    intel = session_state.intelligence.to_dict()

    # -------- MARK WHAT SCAMMER ALREADY GAVE -------- #
    if "₹" in text or "rs" in text or "transfer" in text:
        session_state.resolved_probes.add("transaction")

    if "@" in text and "upi" in text:
        session_state.resolved_probes.add("upi")

    if any(c.isdigit() for c in text) and len(text) >= 10:
        session_state.resolved_probes.add("phone")

    if "http" in text or "www" in text:
        session_state.resolved_probes.add("link")

    if "account" in text or "bank" in text:
        session_state.resolved_probes.add("bank")

    # -------- BAIT QUESTIONS (STRICT ORDER, ASK ONCE) -------- #
    if "transaction" not in session_state.resolved_probes:
        reply = "Which transaction are you referring to?"

    elif "upi" not in session_state.resolved_probes:
        reply = "Which UPI ID was this payment sent to?"

    elif "phone" not in session_state.resolved_probes:
        reply = "Is this linked to my registered mobile number?"

    elif "bank" not in session_state.resolved_probes:
        reply = "Which bank account is this showing from your side?"

    elif "link" not in session_state.resolved_probes:
        reply = "The link isn’t opening for me. Can you resend it?"

    else:
        # -------- FALLBACK HUMAN RESPONSE -------- #
        reply = session_state.planner.generate_reply(
            session_state.planner.choose_strategy(session_state),
            session_state
        )

    # -------- STORE AGENT MESSAGE -------- #
    session_state.history.append({
        "timestamp": time.time(),
        "sender": "agent",
        "message": reply
    })

    # -------- FEAR PROGRESSION -------- #
    if "otp" in text or "upi" in text:
        session_state.persona["fear_level"] = min(1.0, session_state.persona["fear_level"] + 0.1)
    else:
        session_state.persona["fear_level"] = min(1.0, session_state.persona["fear_level"] + 0.05)

    session_state.turns += 1

    return {
        "reply": reply,
        "engagement_complete": session_state.turns >= 6,
        "intelligence": intel,
        "notes": session_state.intelligence.get_notes()
    }


# ---------------- FASTAPI ENTRY POINT ---------------- #

_AGENT_SESSIONS = {}

def agent_handle_message(session_id: str, message: str) -> dict:
    if session_id not in _AGENT_SESSIONS:
        _AGENT_SESSIONS[session_id] = ConversationState(session_id)

    return process_message(_AGENT_SESSIONS[session_id], message)
