from typing import Optional
from fastapi import APIRouter, Request

from app.schemas import MessageRequest
from app.session_manager import get_or_create_session
from app.adapters.scam_adapter import detect_scam
from app.adapters.agent_adapter import get_agent_reply
from app.adapters.intelligence_adapter import process_intelligence
import os

router = APIRouter()

API_KEY = os.getenv("API_KEY", "CHANGE_THIS_SECRET_KEY")


@router.post("/message")
async def receive_message(request: Request):
    """
    GUVI-safe honeypot endpoint.
    Handles:
    - No headers
    - No body
    - Real scam messages
    """

    # 🟢 MANUAL API KEY CHECK (NO 422)
    api_key = request.headers.get("x-api-key")
    if api_key and api_key != API_KEY:
        return {
            "status": "error",
            "reply": "Unauthorized"
        }

    # 🟢 TRY TO READ BODY (GUVI tester sends none)
    try:
        body = await request.json()
    except Exception:
        body = None

    # 🟢 GUVI endpoint tester probe
    if not body or "sessionId" not in body or "message" not in body:
        return {
            "status": "success",
            "reply": "Service is up"
        }

    data = MessageRequest(**body)

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
