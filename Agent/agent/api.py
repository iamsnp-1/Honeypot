from .state import ConversationState
from .intelligence import IntelligenceProfile
from .planner import AgentPlanner
import time

# ---------------- CORE MESSAGE HANDLER ---------------- #

def process_message(session_state, incoming_text):
    """
    Main agent brain – single-turn, memory-safe, no repetition
    """

    text = incoming_text.lower()

    # -------- INIT (RUN ONCE) -------- #
    if session_state.intelligence is None:
        session_state.intelligence = IntelligenceProfile()
        session_state.planner = AgentPlanner()
        session_state.resolved_probes = set()
        session_state.last_question_type = None
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

    # Transaction info
    if "₹" in text or "rs" in text or "transfer" in text:
        session_state.resolved_probes.add("transaction")

    # ✅ FIXED: UPI detection (do NOT require word "upi")
    if "@" in text:
        session_state.resolved_probes.add("upi")

    # Phone number
    if sum(c.isdigit() for c in text) >= 10:
        session_state.resolved_probes.add("phone")

    # Phishing link
    if "http" in text or "www" in text:
        session_state.resolved_probes.add("link")

    # Bank / account
    if "account" in text or "bank" in text:
        session_state.resolved_probes.add("bank")

    # -------- SMART BAIT QUESTIONS (ASK ONCE) -------- #
    reply = None

    def ask_once(key, question):
        if key not in session_state.resolved_probes and session_state.last_question_type != key:
            session_state.last_question_type = key
            return question
        return None

    reply = (
        ask_once("transaction", "Which transaction are you referring to?")
        or ask_once("upi", "Which UPI ID was this payment sent to?")
        or ask_once("phone", "Is this linked to my registered mobile number?")
        or ask_once("bank", "Which bank account is this showing from your side?")
        or ask_once("link", "The link isn’t opening for me. Can you resend it?")
    )

    # -------- FALLBACK HUMAN RESPONSE -------- #
    if reply is None:
        reply = session_state.planner.generate_reply(
            session_state.planner.choose_strategy(session_state),
            session_state
        )
        session_state.last_question_type = None

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
        "engagement_complete": session_state.is_complete(),
        "intelligence": intel,
        "notes": session_state.intelligence.get_notes()
    }


# ---------------- FASTAPI ENTRY POINT ---------------- #

_AGENT_SESSIONS = {}

def agent_handle_message(session_id: str, message: str) -> dict:
    if session_id not in _AGENT_SESSIONS:
        _AGENT_SESSIONS[session_id] = ConversationState(session_id)

    return process_message(_AGENT_SESSIONS[session_id], message)
