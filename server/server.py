from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
import os
import pickle

from .routes.ask import router as ask_router
from .routes.upload import router as upload_router
from .notion import fetch_all_notion_pages
from .gemini_embedding import get_gemini_embedding

app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(ask_router)
app.include_router(upload_router)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "embedding_index.pkl")

@app.on_event("startup")
async def startup_embed_notion_pages():
    print("Startup: Fetching Notion pages and generating embeddings...")

    # Load existing embeddings
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "rb") as f:
            index = pickle.load(f)
    else:
        index = []

    existing_titles = set(item.get("title") or item.get("filename") for item in index)

    try:
        pages = await fetch_all_notion_pages()
        new_embeddings = []

        for page in pages:
            title = page["title"]
            text = page["text"]

            if title in existing_titles:
                print(f"Skipping already embedded page: {title}")
                continue

            print(f"Embedding: {title}")
            embedding = get_gemini_embedding(text)

            new_embeddings.append({
                "source": "notion",
                "title": title,
                "text": text,
                "embedding": embedding
            })

        index.extend(new_embeddings)

        # Save back to pickle
        with open(INDEX_PATH, "wb") as f:
            pickle.dump(index, f)

        print(f"Updated embedding index with {len(new_embeddings)} new items.")

    except Exception as e:
        print("Failed during startup embedding")
        print(e)


@app.get("/")
def root():
    return {"message": "Project ASTRA backend running"}
