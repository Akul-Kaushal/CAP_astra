import os
import requests
from google import genai
import asyncio
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key= api_key)

def get_gemini_embedding(text: str) -> list[float]:
    """Generate embeddings for a given text using Gemini."""
    try:
        response = client.models.embed_content(
            model="models/embedding-001",
            contents=text[:3500]
        )
        return response.embedding.values
    except Exception as e:
        print(f"Gemini Embedding Error: {e}")
        return []
