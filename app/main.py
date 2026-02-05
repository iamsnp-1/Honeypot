from fastapi import FastAPI, Header, HTTPException, Body
import os

# 🔁 CHANGE THIS IMPORT ONLY if path differs
from Agent.agent.engine import AgentEngine  

app = FastAPI(title="Agentic Honeypot API")

# 🔐 API KEY (set in Railway Variables)
API_KEY = os.getenv("HONEYPOT_API_KEY", "CHANGE_THIS_SECRET_KEY")

# 🧠 Initialize Agent ONCE
agent = AgentEngine()


# --------------------------------------------------
# ROOT (health check)
# --------------------------------------------------
@app.get("/")
def root():
    return {"status": "running"}


# --------------------------------------------------
# TESTER ENDPOINT (DO NOT CHANGE THIS)
# --------------------------------------------------
@app.api_route("/honeypot", methods=["GET", "POST"])
def honeypot_test(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return {
        "status": "active",
        "service": "agentic-honeypot",
        "message": "Honeypot API is reachable and secured"
    }


# --------------------------------------------------
# LIVE AGENTIC HONEYPOT (REAL LOGIC)
# --------------------------------------------------
@app.post("/honeypot/live")
def honeypot_live(
    payload: dict = Body(...),
    x_api_key: str = Header(...)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    message = payload.get("message", "")
    session_id = payload.get("session_id", "default")

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    # 🧠 Call your agent
    result = agent.handle(message, session_id=session_id)

    # 🔁 Handle both dict / string agent outputs safely
    if isinstance(result, dict):
        return {
            "reply": result.get("reply"),
            "phase": result.get("phase"),
            "intent": result.get("intent"),
            "extracted_intel": result.get("intel")
        }

    return {
        "reply": result
    }
