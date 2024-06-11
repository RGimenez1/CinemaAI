from pydantic import BaseModel


class ChatRequest(BaseModel):
    context_id: str = None
    message: str
