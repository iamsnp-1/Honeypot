from fastapi import FastAPI, Header, HTTPException
import os

app = FastAPI(title="Agentic Honeypot API")

# API Key (from Railway Variables)
API_KEY = os.getenv("HONEYPOT_API_KEY", "CHANGE_THIS_SECRET_KEY")


@app.get("/")
def root():
    return {"status": "running"}


# 🔐 REQUIRED TEST ENDPOINT (ADD THIS)
@app.get("/honeypot")
def honeypot_test(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return {
        "status": "active",
        "service": "agentic-honeypot",
        "message": "Honeypot API is reachable and secured"
    }
