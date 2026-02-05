from typing import Optional
from fastapi import APIRouter, Depends, Body

from app.schemas import MessageRequest, MessageResponse
from app.auth import verify_api_key
from app.session_manager import get_or_create_session
from app.adapters.scam_adapter import detect_scam
from app.adapters.agent_adapter import get_agent_reply
from app.adapters.intelligence_adapter import process_intelligence

router = APIRouter()


@router.post("/message", response_model=MessageResponse)
def receive_message(
    data: Optional[MessageRequest] = Body(default=None),
    _: str = Depends(verify_api_key)
):
    """
    Main GUVI Honeypot entrypoint.
    Must handle:
    - Empty body (GUVI endpoint tester)
    - Real scam messages (mock scammer API)
    """

    # 🟢 GUVI API Endpoint Tester sends NO BODY
    if data is None or not data.sessionId or not data.message:
        return MessageResponse(
            status="success",
            reply="Service is up"
        )

    # 🟢 Create or load session
    session = get_or_create_session(data.sessionId)

    # 🟢 Store message
    session["messages"].append(data.message.dict())
    session["totalMessages"] += 1

    # 🟢 Scam detection
    detection = detect_scam(data.message.text, session)

    if detection.get("scamDetected") and not session["agentActive"]:
        session["scamDetected"] = True
        session["agentActive"] = True

    session["confidence"] = detection.get("confidence", 0.0)

    # 🟢 Agent reply logic
    if session["agentActive"]:
        reply = get_agent_reply(session, data.message.text)
    else:
        reply = "Okay."

    # 🟢 Intelligence extraction + GUVI callback (handled internally)
    process_intelligence(session)

    return MessageResponse(
        status="success",
        reply=reply
    )
