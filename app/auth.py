from fastapi import Header, HTTPException
import os

API_KEY = os.getenv("API_KEY", "CHANGE_THIS_SECRET_KEY")

def verify_api_key(
    x_api_key: str = Header(..., alias="x-api-key")
):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
