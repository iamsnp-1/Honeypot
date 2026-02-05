from fastapi import FastAPI, Header, HTTPException, Body
import os

app = FastAPI(title="Agentic Honeypot API")

# 🔐 API KEY
API_KEY = os.getenv("HONEYPOT_API_KEY", "CHANGE_THIS_SECRET_KEY")

# 🧠 Lazy agent holder
agent_instance = None


def get_agent():
    global agent_instance
    if agent_instance is None:
        try:
            # ⬇️ IMPORT INSIDE FUNCTION (CRITICAL)
            from Agent.agent.engine import AgentEngine
            agent_instance = AgentEngine()
        except Exception as e:
            raise RuntimeError(f"Agent initialization failed: {e}")
    return agent_instance


# --------------------------------------------------
# ROOT
# --------------------------------------------------
@app.get("/")
def root():
    return {"status": "running"}


# --------------------------------------------------
# TESTER ENDPOINT (DO NOT TOUCH)
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
# LIVE AGENTIC HONEYPOT
# --------------------------------------------------
@app.post("/honeypot/live")
def honeypot_live(
    payload: dict = Body(...),
    x_api_key: str = Header(...)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    message = payload.get("message")
    session_id = payload.get("session_id", "default")

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    try:
        agent = get_agent()
        result = agent.handle(message, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if isinstance(result, dict):
        return result

    return {"reply": result}
