import os
import pickle
from .gemini_embedding import get_gemini_embedding  
from sentence_transformers.util import cos_sim
import pickle


data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
embedding_index = []

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
            embedding = get_gemini_embedding(text)
            embedding_index.append({
                "filename": filename,
                "text": text,
                "embedding": embedding
            })


pkl_path = os.path.join(os.path.dirname(__file__), "embedding_index.pkl")
with open(pkl_path, "wb") as f:
    pickle.dump(embedding_index, f)

print(f"Index built and saved")
