from .state import ConversationState
from .intelligence import IntelligenceProfile
from .planner import AgentPlanner
import time
import re
import random

# ---------------- CORE MESSAGE HANDLER ---------------- #

def process_message(session_state, incoming_text):
    """
    FINAL flawless honeypot agent:
    - Each probe asked ONCE
    - Never repeats link / phone / bank questions
    - Human escalation only after probes
    """

    text = incoming_text.lower()

    # -------- INIT (RUN ONCE) -------- #
    if session_state.intelligence is None:
        session_state.intelligence = IntelligenceProfile()
        session_state.planner = AgentPlanner()
        session_state.resolved_probes = set()
        session_state.asked_probes = set()
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

    # -------- ASK EACH PROBE EXACTLY ONCE -------- #
    def ask_once(probe, question):
        if probe not in session_state.asked_probes and probe not in session_state.resolved_probes:
            session_state.asked_probes.add(probe)
            return question
        return None

    reply = (
        ask_once("upi", "Which UPI ID was this payment sent to?")
        or ask_once("phone", "Is this linked to my registered mobile number?")
        or ask_once("bank", "Which bank account is this related to?")
        or ask_once("link", "The verification link isn’t opening. Can you resend it?")
    )

    # -------- HUMAN ESCALATION (NO PROBES EVER AGAIN) -------- #
    if not reply:
        reply = random.choice([
            "I’m getting really worried… what happens if I don’t do this?",
            "Why is this verification required so urgently?",
            "Is there any way to resolve this without sharing an OTP?",
            "Can this be handled safely at a bank branch?",
            "I’m confused—can you explain what will happen if I don’t verify?"
        ])

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
