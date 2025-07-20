import os
import pickle
import numpy as np
import re
from .gemini_embedding import get_gemini_embedding
from sentence_transformers.util import cos_sim

EMBEDDING_PATH = os.path.join(os.path.dirname(__file__), "embedding_index.pkl")

# Safe loading of the embedding index
def load_embedding_index():
    if not os.path.exists(EMBEDDING_PATH):
        print("[INFO] embedding_index.pkl not found. Returning empty index.")
        return []

    try:
        with open(EMBEDDING_PATH, "rb") as f:
            index = pickle.load(f)
            print(f"[INFO] Loaded {len(index)} embeddings from embedding_index.pkl")
            return index
    except (EOFError, pickle.UnpicklingError) as e:
        print(f"[ERROR] Failed to load embedding_index.pkl: {e}")
        return []

embedding_index = load_embedding_index()

def simple_tokenize(text):
    return set(re.findall(r'\b\w+\b', text.lower()))

def find_similar_documents(query: str, top_k: int = 3, min_score: float = 0.6) -> list[tuple[float, dict]]:
    if not embedding_index:
        print("[WARN] No embeddings available to search.")
        return []

    query_vec = get_gemini_embedding(query)
    query_vec = np.array(query_vec).reshape(1, -1)
    query_tokens = simple_tokenize(query)

    matches = []

    for doc in embedding_index:
        doc_vec = np.array(doc["embedding"]).reshape(1, -1)
        score = cos_sim(query_vec, doc_vec).item()

        # Textual overlap filter
        doc_tokens = simple_tokenize(doc["text"])
        shared_words = query_tokens.intersection(doc_tokens)

        if score >= min_score and len(shared_words) >= 2:
            matches.append((score, doc))

    matches.sort(key=lambda x: x[0], reverse=True)
    return matches[:top_k]
