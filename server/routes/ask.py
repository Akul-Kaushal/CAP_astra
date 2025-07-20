from fastapi import APIRouter
from pydantic import BaseModel
from ..gemini_api import query_gemini

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/ask")
async def ask(request: PromptRequest):
    response = query_gemini(request.prompt)
    return {"response": response}
