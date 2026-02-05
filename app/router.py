from typing import Optional
from fastapi import APIRouter, Depends, Body

from app.schemas import MessageRequest
from app.auth import verify_api_key
from app.session_manager import get_or_create_session
from app.adapters.scam_adapter import detect_scam
from app.adapters.agent_adapter import get_agent_reply
from app.adapters.intelligence_adapter import process_intelligence

router = APIRouter()


@router.post("/message")
def receive_message(
    data: Optional[MessageRequest] = Body(default=None),
    _: str = Depends(verify_api_key)
):
    # 🟢 GUVI endpoint tester (NO BODY)
    if data is None or not data.sessionId or not data.message:
        return {
            "status": "success",
            "reply": "Service is up"
        }

    session = get_or_create_session(data.sessionId)

    session["messages"].append(data.message.dict())
    session["totalMessages"] += 1

    detection = detect_scam(data.message.text, session)

    if detection.get("scamDetected") and not session["agentActive"]:
        session["scamDetected"] = True
        session["agentActive"] = True

    if session["agentActive"]:
        reply = get_agent_reply(session, data.message.text)
    else:
        reply = "Okay."

    process_intelligence(session)

    return {
        "status": "success",
        "reply": reply
    }
