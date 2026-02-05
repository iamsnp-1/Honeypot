# Adapter for Teammate-2 Agent
from Agent.agent.api import process_message
from Agent.agent.state import ConversationState

AGENT_SESSIONS = {}

def get_agent_reply(session: dict, latest_message: str) -> str:
    session_id = session["sessionId"]

    # create agent state once per session
    if session_id not in AGENT_SESSIONS:
        AGENT_SESSIONS[session_id] = ConversationState(
            session_id=session_id
        )

    agent_state = AGENT_SESSIONS[session_id]

    # 🔥 SYNC FULL CONVERSATION (scammer + agent)
    agent_state.history = [
        {
            "sender": m["sender"],
            "message": m["text"]
        }
        for m in session.get("messages", [])
    ]

    # 🚨 always pass CURRENT scammer message
    result = process_message(
        session_state=agent_state,
        incoming_text=latest_message
    )

    reply = result.get("reply")

    if not reply or not isinstance(reply, str):
        reply = "Can you explain what I need to do now?"
    
    return reply


