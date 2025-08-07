from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
import uuid
import imghdr

from ..gemini_api import ask_gemini_about_image

router = APIRouter()

ALLOWED_EXTENSIONS = {"png", "jpeg", "jpg"}
UPLOAD_FOLDER = "server/image"

@router.post("/ask_image")
async def ask_image(prompt: str = Form(...), file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    extension = os.path.splitext(file.filename)[1].lower().lstrip(".")
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file extension")

    unique_filename = f"{uuid.uuid4()}.{extension}"
    image_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Save file
    with open(image_path, "wb") as f:
        content = await file.read()
        f.write(content)


    detected_type = imghdr.what(image_path)
    if detected_type not in ALLOWED_EXTENSIONS:
        os.remove(image_path)  
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")

    answer = ask_gemini_about_image(image_path, prompt)
    try:
        os.remove(image_path)
    except Exception as e:
        print(f"Warning: Could not delete image: {e}")

    return {"answer": answer}
