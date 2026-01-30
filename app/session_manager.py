sessions = {}

def get_or_create_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "totalMessages": 0,
            "scamDetected": False,
            "confidence": 0.0,
            "agentActive": False
        }
    return sessions[session_id]
