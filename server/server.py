from fastapi import FastAPI, Request, UploadFile, File
from pydantic import BaseModel
from .gemini_api import query_gemini
import os
import shutil
from .logger import log_interaction
from .gemini_embedding import get_gemini_embedding
import pickle


app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask(request: PromptRequest):
    response = query_gemini(request.prompt)
    return {"response": response}


@app.post("/upload")
async def upload_manual(file: UploadFile = File(...)):
    if not file or not file.filename or not file.filename.endswith(".txt"):
        return {"error": "Only .txt files are allowed and a file must be provided."}

    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    dest_path = os.path.join(data_dir, file.filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(dest_path, "r", encoding="utf-8") as f:
        text = f.read()
        embedding = get_gemini_embedding(text)

    pkl_path = os.path.join(os.path.dirname(__file__), "embedding_index.pkl")
    if os.path.exists(pkl_path):
        with open(pkl_path, "rb") as f:
            index = pickle.load(f)
    else:
        index = []

    index.append({
        "filename": file.filename,
        "text": text,
        "embedding": embedding
    })

    with open(pkl_path, "wb") as f:
        pickle.dump(index, f)

    return {"message": f"{file.filename} uploaded and embedded successfully."}

