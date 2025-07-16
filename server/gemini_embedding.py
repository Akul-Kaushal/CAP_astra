import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")  # Debugging line to check if API_KEY is loaded
EMBEDDING_URL = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"

def get_gemini_embedding(text: str) -> list[float]:
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": API_KEY
    }

    # Payload per official Gemini Embedding docs
    payload = {
        "model": "models/embedding-001",
        "content": {
            "parts": [
                {"text": text[:3500]}  # Safe truncation
            ]
        }
    }

    response = requests.post(EMBEDDING_URL, headers=headers, params=params, json=payload)

    # Show full Gemini error if 400
    if not response.ok:
        print("❌ Gemini Error:")
        print(response.text)
        response.raise_for_status()

    return response.json()["embedding"]["values"]
