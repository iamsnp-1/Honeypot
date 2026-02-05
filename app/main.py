from fastapi import FastAPI
from .router import router
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

API_KEY = "CHANGE_THIS_SECRET_KEY"

app = FastAPI(title="Agentic HoneyPot API")
app.include_router(router)

