from fastapi import FastAPI, Header, HTTPException, Request
import os
from fastapi import Body

# import your agent (adjust import if needed)
from Agent.agent.engine import AgentEngine

agent = AgentEngine()


@app.post("/honeypot/live")
def honeypot_live(
    payload: dict = Body(...),
    x_api_key: str = Header(...)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    message = payload.get("message", "")
    session_id = payload.get("session_id", "default")

    result = agent.handle(message, session_id=session_id)

    return {
        "reply": result.get("reply"),
        "phase": result.get("phase"),
        "intent": result.get("intent"),
        "extracted_intel": result.get("intel")
    }

app = FastAPI(title="Agentic Honeypot API")

API_KEY = os.getenv("HONEYPOT_API_KEY", "CHANGE_THIS_SECRET_KEY")


@app.api_route("/honeypot", methods=["GET", "POST"])
def honeypot_test(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return {
        "status": "active",
        "service": "agentic-honeypot",
        "message": "Honeypot API is reachable and secured"
    }

