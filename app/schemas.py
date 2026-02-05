from typing import Optional, List, Dict
from pydantic import BaseModel


class Message(BaseModel):
    sender: Optional[str] = None
    text: Optional[str] = None
    timestamp: Optional[str] = None


class MessageRequest(BaseModel):
    sessionId: Optional[str] = None
    message: Optional[Message] = None
    conversationHistory: Optional[List[Dict]] = []
    metadata: Optional[Dict] = {}


class MessageResponse(BaseModel):
    status: str
    reply: str
