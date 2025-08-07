import os
import requests
from dotenv import load_dotenv
import time
from .logger import log_interaction
from .semantic_search import find_similar_documents
import base64
from PIL import Image
import mimetypes

# import re

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

"""
# Function to query Gemini API with a prompt and return the response
query_gemini(prompt: str) -> str:
This function sends a prompt to the Gemini API and returns the generated response.
"""
def query_gemini(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}

    results = find_similar_documents(prompt, top_k=3, min_score=0.5)  

    context = ""
    matched_files = []

    if results:
        for score, doc in results:
            filename = doc.get('filename', 'unknown')
            context += f"### Source: {filename} ###\n{doc['text']}\n\n"
            matched_files.append(filename)


    full_prompt = f"""
You are a helpful assistant . If any of the following documents are relevant, use them to answer the user's question. If they are not relevant, answer using general knowledge — but still keep it brief and focused.

Documents:
{context if context.strip() else '[No documents matched]'}

Question:
{prompt}

Provide the most appropriate answer in **Most Precise Way eiter use table bullet point or what ever you fell is right if anything is not present in docs answer on your own**.
""".strip()

    data = {
        "contents": [
            {
                "parts": [{"text": full_prompt}]
            }
        ]
    }

    attempt = 1
    while True:
        response = requests.post(GEMINI_URL, headers=headers, params=params, json=data)
        try:
            response_json = response.json()
        except ValueError:
            return f"Invalid JSON response: {response.text}"

        if response.status_code == 200:
                try:
                    output = response_json['candidates'][0]['content']['parts'][0]['text']
                    log_interaction(prompt, context, output, matched_files)
                    return output.strip()
                except (KeyError, IndexError) as e:
                    return f"Malformed success response: {response_json}"
        elif response.status_code == 503:
                print(f"[Retry {attempt}] Gemini is overloaded. Retrying...")
                time.sleep(2 + attempt)
                attempt += 1
        else:
                return f"Error {response.status_code}: {response.text}"

def ask_gemini_about_image(image_path: str, prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}

    # Detect mime type
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        return "Unsupported image type"

    # Convert image to base64
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    },
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": encoded_image
                        }
                    }
                ]
            }
        ]
    }

    attempt = 1
    while True:
        response = requests.post(GEMINI_URL, headers=headers, params=params, json=data)
        try:
            response_json = response.json()
        except ValueError:
            return f"Invalid JSON response: {response.text}"

        if response.status_code == 200:
            try:
                return response_json['candidates'][0]['content']['parts'][0]['text'].strip()
            except (KeyError, IndexError):
                return f"Malformed success response: {response_json}"
        elif response.status_code == 503:
            print(f"[Retry {attempt}] Gemini is overloaded. Retrying...")
            time.sleep(2 + attempt)
            attempt += 1
        else:
            return f"Error {response.status_code}: {response.text}" 