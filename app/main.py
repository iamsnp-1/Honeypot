from fastapi import FastAPI, Header, HTTPException, Request
import os

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
