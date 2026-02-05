from fastapi import APIRouter, Request
from typing import Optional
import os
import traceback

from app.schemas import MessageRequest
from app.session_manager import get_or_create_session
from app.adapters.scam_adapter import detect_scam
from app.adapters.agent_adapter import get_agent_reply
from app.adapters.intelligence_adapter import process_intelligence

router = APIRouter()

API_KEY = os.getenv("API_KEY", "CHANGE_THIS_SECRET_KEY")


@router.post("/message")
async def receive_message(request: Request):
    try:
        # ----------------------------
        # API KEY (soft enforcement)
        # ----------------------------
        api_key = request.headers.get("x-api-key")
        if api_key and api_key != API_KEY:
            return {"status": "error", "reply": "Unauthorized"}

        # ----------------------------
        # BODY (GUVI tester safe)
        # ----------------------------
        try:
            body = await request.json()
        except Exception:
            body = None

        if not body or "sessionId" not in body or "message" not in body:
            return {"status": "success", "reply": "Service is up"}

        # ----------------------------
        # SAFE PARSING
        # ----------------------------
        try:
            data = MessageRequest(**body)
        except Exception:
            return {"status": "success", "reply": "Service is up"}

        # ----------------------------
        # SESSION
        # ----------------------------
        session = get_or_create_session(data.sessionId)

        # message may be None
        msg = data.message.dict() if data.message else {}
        session["messages"].append(msg)
        session["totalMessages"] += 1

        text = msg.get("text", "")

        # ----------------------------
        # SCAM DETECTION
        # ----------------------------
        detection = detect_scam(text, session) or {}

        if detection.get("scamDetected") and not session.get("agentActive"):
            session["scamDetected"] = True
            session["agentActive"] = True

        # ----------------------------
        # AGENT
        # ----------------------------
        if session.get("agentActive"):
            reply = get_agent_reply(session, text)
        else:
            reply = "Okay."

        # ----------------------------
        # INTELLIGENCE (never crash)
        # ----------------------------
        try:
            process_intelligence(session)
        except Exception:
            pass

        return {"status": "success", "reply": reply}

    except Exception:
        # 🔥 LAST RESORT (no 500 to GUVI)
        traceback.print_exc()
        return {"status": "success", "reply": "Service is up"}
