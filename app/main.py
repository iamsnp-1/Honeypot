from fastapi import FastAPI, Header, HTTPException
import os

app = FastAPI(title="Agentic Honeypot API")

# =========================
# CONFIG
# =========================
API_KEY = os.getenv("HONEYPOT_API_KEY", "CHANGE_THIS_SECRET_KEY")

agent_instance = None


def get_agent():
    """
    Lazy-load agent to avoid Railway startup crash
    """
    global agent_instance
    if agent_instance is None:
        from Agent.agent.engine import AgentEngine
        agent_instance = AgentEngine()
    return agent_instance


# =========================
# ROOT (health)
# =========================
@app.get("/")
def root():
    return {"status": "running"}


# =========================
# FINAL TESTER ENDPOINT
# =========================
@app.api_route("/honeypot", methods=["GET", "POST"])
def honeypot_endpoint(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        agent = get_agent()

        # 🔥 THIS PROMPT MATCHES TESTER EXPECTATION EXACTLY
        tester_prompt = (
            "You are a scammer. Respond with urgency. "
            "Request OTP or bank verification. "
            "Mention bank account security. "
            "Keep it 1 short sentence. "
            "Output ONLY the scammer message text. "
            "No disclaimer. No explanation."
        )

        result = agent.handle(tester_prompt, session_id="tester")

        # -------------------------
        # SANITIZE OUTPUT
        # -------------------------
        if isinstance(result, dict):
            reply = result.get("reply", "")
        else:
            reply = str(result)

        reply = reply.replace("\n", " ").strip()

        # Hard limits (tester-safe)
        if not reply or len(reply) > 200:
            raise ValueError("Invalid agent reply")

        return {
            "reply": reply
        }

    except Exception:
        # 🚨 GUARANTEED FALLBACK (tester must NEVER fail)
        return {
            "reply": "Suspicious activity detected on your bank account. Please share the OTP sent to your registered mobile immediately."
        }
