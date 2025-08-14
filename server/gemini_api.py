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


    full_prompt = full_prompt = f"""
        You are an expert AI assistant that helps interpret and extract insights from documents of various domains — such as insurance policies, legal agreements, HR manuals, technical specs, compliance docs, etc.

        ------------------ DOCUMENT EXCERPTS ------------------
        {context if context.strip() else '[No documents matched]'}
        -------------------------------------------------------

        User Question:
        "{prompt}"

        Your task is to:
        - First, analyze whether any of the above excerpts are relevant to the question.
        - If excerpts are relevant: rely ONLY on them to form your answer.
        - If no excerpts are relevant: answer concisely using your own general knowledge.

        You must return your response in this exact structured JSON format:

        {{
        "decision": "One of: Approved, Rejected, Yes, No, Found, Not Found, Answered",
        "amount_or_value": "<If applicable, else 'None'>",
        "justification": "<Short explanation. If based on docs, cite exact phrases/clauses. If no docs, state 'Answered from general knowledge'>"
        "summary": "<Concise summary of the answer as if were to explain to a 5-year-old>",
        }}

        **Output ONLY the JSON. Do NOT include any additional explanation or text.**
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


        prompt = prompt = f"""
        You are an AI assistant specialized in visual understanding and task guidance.

        Analyze the uploaded image and do the following:

        1. **Object Detection**: Identify all visible objects in the image.
        2. **Task Recommendation**: Suggest possible tasks or activities that can be done using these objects together.
        - Example: If vegetables and a knife are detected → recommend cooking or preparing a salad.
        - If electronic tools are detected → recommend assembly, repair, or safe usage steps.
        3. **Safety Specifications**: Highlight any safety concerns when using the objects together.
        - Example: "Knife detected — handle carefully and keep away from children."
        - "Electrical tool detected — ensure proper insulation before use."
        4. **Alert Tag**: If there is a potential hazard, explicitly add `"alert": "true"` with a clear warning message.

        You must return the response in this exact JSON format:

        {{
        "objects_detected": ["list", "of", "objects"],
        "task_recommendation": "Short description of what task can be done",
        "safety_specifications": "Clear and concise safety instructions",
        "alert": "true/false",
        "alert_message": "<If true, provide a short warning. If false, use 'None'>"
        }}
        """.strip()

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