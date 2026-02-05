def get_agent_reply(session, incoming_text):

    # ✅ create ONCE
    if "agent_state" not in session:
        session["agent_state"] = ConversationState(
            session_id=session["sessionId"]
        )

    # ✅ reuse same state
    result = process_message(
        session["agent_state"],
        incoming_text
    )

    return result["reply"]
