from fastapi import FastAPI, Request, UploadFile, File
from pydantic import BaseModel
from .gemini_api import query_gemini
import os
import shutil
from .logger import log_interaction
from .gemini_embedding import get_gemini_embedding
import pickle

from pydantic import BaseModel


app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask(request: PromptRequest):
    response = query_gemini(request.prompt)
    return {"response": response}



"""

"""
class UploadRequest(BaseModel):
    filename: str

from pydantic import BaseModel

class SpeechUploadRequest(BaseModel):
    filename: str

@app.post("/upload")
def upload_from_filename(data: SpeechUploadRequest):
    filename = data.filename.strip()

    if not filename.endswith(".txt"):
        filename += ".txt"

    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    filepath = os.path.join(data_dir, filename)

    if not os.path.exists(filepath):
        return {"error": f"File '{filename}' not found in /data"}

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
        embedding = get_gemini_embedding(text)

    pkl_path = os.path.join(os.path.dirname(__file__), "embedding_index.pkl")
    if os.path.exists(pkl_path):
        with open(pkl_path, "rb") as f:
            index = pickle.load(f)
    else:
        index = []

    index.append({
        "filename": filename,
        "text": text,
        "embedding": embedding
    })

    with open(pkl_path, "wb") as f:
        pickle.dump(index, f)

    return {"message": f"{filename} uploaded and embedded successfully via speech."}


