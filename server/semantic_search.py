import os
import pickle
import numpy as np
import re
from .gemini_embedding import get_gemini_embedding
from sentence_transformers.util import cos_sim


with open(os.path.join(os.path.dirname(__file__), "embedding_index.pkl"), "rb") as f:
    embedding_index = pickle.load(f)

def simple_tokenize(text):
    return set(re.findall(r'\b\w+\b', text.lower()))

def find_similar_documents(query: str, top_k: int = 3, min_score: float = 0.6) -> list[tuple[float, dict]]:
    query_vec = get_gemini_embedding(query)
    query_vec = np.array(query_vec).reshape(1, -1)

    query_tokens = simple_tokenize(query)
    matches = []

    for doc in embedding_index:
        doc_vec = np.array(doc["embedding"]).reshape(1, -1)
        score = cos_sim(query_vec, doc_vec).item()

        # Textual sanity filter: some token overlap
        doc_tokens = simple_tokenize(doc["text"])
        shared_words = query_tokens.intersection(doc_tokens)

        if score >= min_score and len(shared_words) >= 2:  # Require token overlap
            matches.append((score, doc))

    matches.sort(reverse=True, key=lambda x: x[0])
    return matches[:top_k]
