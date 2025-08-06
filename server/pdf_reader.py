import fitz  # PyMuPDF

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = ""
    for page_num in range(len(doc)):
        page = doc[page_num]
        text += f"\n--- Page {page_num + 1} ---\n"
        text += page.get_text() #type: ignore
    doc.close()
    return text.strip()
