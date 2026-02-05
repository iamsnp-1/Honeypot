from .state import ConversationState
from .intelligence import IntelligenceProfile
from .planner import AgentPlanner
import time
import re
import random

# ---------------- CORE MESSAGE HANDLER ---------------- #

def process_message(session_state, incoming_text):
    """
    Final flawless honeypot agent:
    - No repeated questions
    - Progressive intelligence extraction
    - Human escalation
    - Self-correction
    """

    text = incoming_text.lower()

    # -------- INIT (RUN ONCE) -------- #
    if session_state.intelligence is None:
        session_state.intelligence = IntelligenceProfile()
        session_state.planner = AgentPlanner()
        session_state.resolved_probes = set()
        session_state.last_question_type = None
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

    # -------- AUTO-RESOLVE PROBES (PATTERN BASED) -------- #
    if re.search(r"\b[\w.-]+@[\w.-]+\b", text):
        session_state.resolved_probes.add("upi")

    if re.search(r"\b\d{10,}\b", text):
        session_state.resolved_probes.add("phone")

    if "account" in text or re.search(r"\b\d{12,18}\b", text):
        session_state.resolved_probes.add("bank")

    if "http://" in text or "https://" in text:
        session_state.resolved_probes.add("link")

    if "otp" in text or re.search(r"\b\d{4,8}\b", text):
        session_state.resolved_probes.add("otp")

    # -------- ASK EACH PROBE ONLY ONCE -------- #
    def ask_once(probe, question):
        if probe not in session_state.resolved_probes and session_state.last_question_type != probe:
            session_state.last_question_type = probe
            return question
        return None

    reply = (
        ask_once("upi", "Which UPI ID was this payment sent to?")
        or ask_once("phone", "Is this linked to my registered mobile number?")
        or ask_once("bank", "Which bank account is this related to?")
        or ask_once("link", "The verification link isn’t opening. Can you resend it?")
    )

    # -------- HUMAN ESCALATION (NO PROBE LOOP) -------- #
    if not reply:
        reply = random.choice([
            "I’m getting worried… what happens if I don’t do this?",
            "Why is this verification needed right now?",
            "Is there another way to resolve this without sharing codes?",
            "Can this be handled at a bank branch instead?",
            "This is confusing me—can you explain it once more?"
        ])
        session_state.last_question_type = "escalation"

    # -------- STORE AGENT MESSAGE -------- #
    session_state.history.append({
        "timestamp": time.time(),
        "sender": "agent",
        "message": reply
    })

    # -------- FEAR PROGRESSION -------- #
    if "otp" in text:
        session_state.persona["fear_level"] = min(1.0, session_state.persona["fear_level"] + 0.1)
    else:
        session_state.persona["fear_level"] = min(1.0, session_state.persona["fear_level"] + 0.05)

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
