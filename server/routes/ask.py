from fastapi import APIRouter
from pydantic import BaseModel
from ..gemini_api import query_gemini
import json

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/ask/{uid}")
async def ask(request: PromptRequest):
    response = query_gemini(request.prompt)

    try:
        # clean markdown fences if present
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(cleaned)   
        return parsed                  
    except Exception as e:
        return {"raw_response": response, "error": str(e)}
