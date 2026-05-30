from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    


class UploadResponse(BaseModel):
    message: str
    pages: int
    chunks: int