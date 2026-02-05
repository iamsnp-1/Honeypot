from agent.api import process_message
from agent.state import ConversationState


def get_agent_reply(session: dict, incoming_text: str) -> str:
    # Create state object once per session
    if "agent_state" not in session:
        session["agent_state"] = ConversationState(
            session_id=session["sessionId"]
        )

    state = session["agent_state"]

    result = process_message(
        session_state=state,
        incoming_text=incoming_text
    )

    # Save extracted intelligence back into session
    session["extractedIntelligence"] = result.get("intelligence", {})

    return result["reply"]
