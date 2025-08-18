from fastapi import APIRouter
from pydantic import BaseModel
from ..gemini_api import query_gemini
import json


router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/ask/{uid}")
async def ask(uid: str, request: PromptRequest)-> dict:
    response = query_gemini(request.prompt)

    try:
        cleaned = response.strip()
        parsed = {}
        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
        else:
            parsed = {"reply": cleaned}
        reply_text = parsed.get("summary", "") + "\n" + parsed.get("justification", "")
        return {"reply": reply_text.strip(), **parsed}
    except Exception as e:
        return {"raw_response": response, "error": str(e)}
