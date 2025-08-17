from PIL import Image
import pytesseract
import io

def preprocess_image(content: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(content))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"OCR failed: {str(e)}")
