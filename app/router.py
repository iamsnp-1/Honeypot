from fastapi import APIRouter, Depends
from .schemas import MessageRequest, MessageResponse
from .auth import verify_api_key
from .session_manager import get_or_create_session
from .detectors.scam_detector import detect_scam
from .agent.responder import generate_reply

router = APIRouter()
@router.post("/message", response_model=MessageResponse)
def receive_message(
    data: MessageRequest,
    _: str = Depends(verify_api_key)
):
    session = get_or_create_session(data.sessionId)

    session["messages"].append(data.message.dict())
    session["totalMessages"] += 1

    detection = detect_scam(data.message.text, session)

    # Activate agent ONLY ONCE
    if detection["scamDetected"] and not session["agentActive"]:
        session["scamDetected"] = True
        session["agentActive"] = True

    session["confidence"] = detection["confidence"]
    print(session)
    # 🔑 TWO-PHASE REPLY LOGIC
    if not session["agentActive"]:
        reply = "Okay, noted."
    else:
        reply = generate_reply(
            session=session,
            latest_message=data.message.text
        )

    return MessageResponse(
        status="success",
        reply=reply
    )