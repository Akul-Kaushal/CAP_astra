from fastapi import APIRouter, UploadFile, File
import os
import pickle
import uuid
from ..gemini_embedding import get_gemini_embedding

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file or not file.filename:
        return {"error": "No file uploaded."}

    original_filename = file.filename

    if not original_filename.endswith(".txt"):
        return {"error": "Only .txt files are supported."}

    # Safe path setup
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Generate unique filename
    name, ext = os.path.splitext(original_filename)
    unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
    file_path = os.path.join(data_dir, unique_filename)

    # Save uploaded file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Decode and embed
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return {"error": "Unable to decode file as UTF-8 text."}

    embedding = get_gemini_embedding(text)

    # Load or initialize embedding index
    index_path = os.path.join(base_dir, "embedding_index.pkl")
    try:
        with open(index_path, "rb") as f:
            index = pickle.load(f)
    except Exception:
        index = []

    index.append({
        "original_filename": original_filename,
        "stored_filename": unique_filename,
        "text": text,
        "embedding": embedding
    })

    with open(index_path, "wb") as f:
        pickle.dump(index, f)

    return {"message": f"Uploaded and embedded as {unique_filename}."}
