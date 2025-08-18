from fastapi import APIRouter, UploadFile, File
import os
import pickle
import uuid


from ..gemini_embedding import get_gemini_embedding
from ..pdf_reader import extract_text_from_pdf

router = APIRouter()

@router.post("/upload/{uid}")
async def upload_file(uid: str, file: UploadFile = File(...)):
    if not file or not file.filename:
        return {"error": "No file uploaded."}

    original_filename = file.filename
    ext = os.path.splitext(original_filename)[-1].lower()

    if ext not in [".txt", ".pdf"]:
        return {"error": "Only .txt, .pdf files are supported."}

    # Safe storage directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data",f"{uid}")
    os.makedirs(data_dir, exist_ok=True)

    # Unique file name
    unique_filename = f"{os.path.splitext(original_filename)[0]}_{uuid.uuid4().hex[:8]}{ext}"
    file_path = os.path.join(data_dir, unique_filename)

    # Save file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Extract text
    try:
        if ext == ".txt":
            text = content.decode("utf-8")
        elif ext == ".pdf":
            text = extract_text_from_pdf(file_path)
        else:
            return {"error": "Unsupported file type."}
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}

    # Generate embedding
    embedding = get_gemini_embedding(text)

    # Load existing index
    index_path = os.path.join(base_dir, "embedding_index.pkl")
    try:
        with open(index_path, "rb") as f:
            index = pickle.load(f)
    except Exception:
        index = []

    # Append new embedding
    index.append({
        "source": "upload",
        "original_filename": original_filename,
        "stored_filename": unique_filename,
        "text": text,
        "embedding": embedding
    })


    with open(index_path, "wb") as f:
        pickle.dump(index, f)

    return {"message": f"Uploaded and embedded {unique_filename} successfully."}
