from fastapi import APIRouter
import os
import pickle

from ..notion import fetch_all_notion_pages
from ..gemini_embedding import get_gemini_embedding

router = APIRouter()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "..", "embedding_index.pkl")


@router.post("/embed/notion")
async def embed_notion_pages():
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "rb") as f:
            index = pickle.load(f)
    else:
        index = []

    existing_titles = set(item.get("title") or item.get("filename") for item in index)
    new_embeddings = []

    try:
        pages = await fetch_all_notion_pages()

        for page in pages:
            title = page["title"]
            text = page["text"]

            if title in existing_titles:
                continue

            embedding = get_gemini_embedding(text)
            new_embeddings.append({
                "source": "notion",
                "title": title,
                "text": text,
                "embedding": embedding
            })

        index.extend(new_embeddings)

        with open(INDEX_PATH, "wb") as f:
            pickle.dump(index, f)

        return {
            "message": f"{len(new_embeddings)} new Notion pages embedded.",
            "total_index_size": len(index)
        }

    except Exception as e:
        return {
            "error": str(e)
        }
