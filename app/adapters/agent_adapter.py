from agent.api import process_message
from agent.state import ConversationState

# Store session-level agent states
AGENT_SESSIONS = {}

def get_agent_reply(session: dict, incoming_text: str) -> str:
    session_id = session["sessionId"]

    # Create agent state once per session
    if session_id not in AGENT_SESSIONS:
        AGENT_SESSIONS[session_id] = ConversationState(session_id=session_id)

    agent_state = AGENT_SESSIONS[session_id]

    result = process_message(agent_state, incoming_text)

    return result["reply"]
