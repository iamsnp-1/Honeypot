from .state import ConversationState
from .intelligence import IntelligenceProfile
from .planner import AgentPlanner
import time
import re

# ---------------- CORE MESSAGE HANDLER ---------------- #

def process_message(session_state, incoming_text):
    """
    Intelligent honeypot agent – NO repetition, progressive extraction
    """

    text = incoming_text.lower()

    # -------- INIT (RUN ONCE PER SESSION) -------- #
    if session_state.intelligence is None:
        session_state.intelligence = IntelligenceProfile()
        session_state.planner = AgentPlanner()
        session_state.resolved_probes = set()
        session_state.turns = 0
        session_state.persona = {"fear_level": 0.3}
        session_state.history = []

    # -------- STORE SCAMMER MESSAGE -------- #
    session_state.history.append({
        "timestamp": time.time(),
        "sender": "scammer",
        "message": incoming_text
    })

    # -------- EXTRACT INTELLIGENCE -------- #
    session_state.intelligence.extract(incoming_text)
    intel = session_state.intelligence.to_dict()

    # -------- AUTO-RESOLVE PROBES (ROBUST) -------- #

    # UPI ID (anything@anything)
    if re.search(r"\b[\w.-]+@[\w.-]+\b", text):
        session_state.resolved_probes.add("upi")

    # Phone number (10+ digits)
    if re.search(r"\b\d{10,}\b", text):
        session_state.resolved_probes.add("phone")

    # Bank / account number
    if "account" in text or re.search(r"\b\d{12,18}\b", text):
        session_state.resolved_probes.add("bank")

    # Link
    if re.search(r"https?://", text):
        session_state.resolved_probes.add("link")

    # OTP mention
    if "otp" in text or re.search(r"\b\d{4,8}\b", text):
        session_state.resolved_probes.add("otp")

    # -------- INTELLIGENT QUESTION FLOW (NO LOOP) -------- #

    if "upi" not in session_state.resolved_probes:
        reply = "Which UPI ID was this payment sent to?"

    elif "bank" not in session_state.resolved_probes:
        reply = "Which bank account is this related to?"

    elif "phone" not in session_state.resolved_probes:
        reply = "Is this linked to my registered mobile number?"

    elif "link" not in session_state.resolved_probes:
        reply = "The verification link isn’t opening. Can you resend it?"

    else:
        # FINAL PHASE – keep scammer talking without giving info
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

    session_state.turns += 1

    return {
        "reply": reply,
        "engagement_complete": session_state.turns >= 8,
        "intelligence": intel,
        "notes": session_state.intelligence.get_notes()
    }


# ---------------- FASTAPI ENTRY POINT ---------------- #

_AGENT_SESSIONS = {}

def agent_handle_message(session_id: str, message: str) -> dict:
    if session_id not in _AGENT_SESSIONS:
        _AGENT_SESSIONS[session_id] = ConversationState(session_id)

    return process_message(_AGENT_SESSIONS[session_id], message)
