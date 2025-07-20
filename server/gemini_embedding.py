import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_URL = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"

def get_gemini_embedding(text: str) -> list[float]:
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": API_KEY
    }

    payload = {
        "content": {
            "parts": [
                {"text": text[:3500]}  # Safe length for context
            ]
        }
    }

    response = requests.post(EMBEDDING_URL, headers=headers, params=params, json=payload)

    if not response.ok:
        print("Gemini Embedding Error:")
        print(response.text)
        response.raise_for_status()

    print(response.json())

    return response.json()["embedding"]["values"]
