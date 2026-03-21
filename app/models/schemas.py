from pydantic import BaseModel
from typing import Optional, List
from app.models.enums import Model

class Message(BaseModel):
    role: str
    content: str

class ProxyRequest(BaseModel):
    model: Model
    messages: List[Message]
    max_tokens: Optional[int] = 1024
    temperature: Optional[float] = None
    system: Optional[str] = None
    stream: Optional[bool] = False