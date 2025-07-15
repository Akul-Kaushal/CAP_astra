import os
import requests
from dotenv import load_dotenv
import time
import re
from .logger import log_interaction

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


# def query_gemini(prompt: str) -> str:
#     headers = {"Content-Type": "application/json"}
#     params = {"key": API_KEY}

#     context, matched = load_relevant_documents(prompt)

#     if matched:
#         full_prompt = f"""Use the following task manuals to help answer the query:

# {context}

# User Query: {prompt}
# """
#     else:
#         full_prompt = prompt  

#     data = {
#         "contents": [
#             {
#                 "parts": [{"text": full_prompt}]
#             }
#         ]
#     }
    

#     attempt = 1

#     while True:
#         response = requests.post(GEMINI_URL, headers=headers, params=params, json=data)
#         if response.status_code == 200:
#             return response.json()['candidates'][0]['content']['parts'][0]['text']
#         elif response.status_code == 503:
#             print(f"Attempt {attempt}: Model is overloaded (503). Retrying in {2 + attempt}s...")
#             time.sleep(2 + attempt)
#             attempt += 1
#         else:
#             return f"Error: {response.status_code} - {response.text}"

def query_gemini(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}
    
    context, matched, matched_files = load_relevant_documents(prompt)

    if matched:
        full_prompt = f"""Use the following task manuals to help answer the query:

{context}

User Query: {prompt}
"""
    else:
    # Fallback: Just use raw prompt, no misleading instruction
        full_prompt = prompt

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
        if response.status_code == 200:
            output = response.json()['candidates'][0]['content']['parts'][0]['text']
            log_interaction(prompt, context, output, matched_files if matched else [])
            return output
        elif response.status_code == 503:
            print(f"Attempt {attempt}: Model is overloaded (503). Retrying in {2 + attempt}s...")
            time.sleep(2 + attempt)
            attempt += 1
        else:
            return f"Error: {response.status_code} - {response.text}"


def simple_word_tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def load_relevant_documents(prompt: str) -> tuple[str, bool, list[str]]:
    context = ""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

    STOPWORDS = {
        "what", "is", "the", "how", "to", "a", "an", "of", "for", "in", "on", "and", "or", "with", "about", "do", "i", "you",
        "are", "some", "this", "that", "it", "from", "was", "were"
    }

    # Tokenize the prompt properly
    meaningful_words = [word for word in simple_word_tokenize(prompt) if word not in STOPWORDS]

    matched_files = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read().lower()
                content_words = set(simple_word_tokenize(content))  # tokenize file content once

                # Check how many words from prompt are in the content (as full words)
                match_count = sum(word in content_words for word in meaningful_words)

                if match_count >= 1:  # you can reduce to 1 match for more flexibility
                    matched_files.append((filename, content))

    print(f"[DEBUG] Matching words: {meaningful_words}")
    print(f"[DEBUG] Matched files: {[f[0] for f in matched_files]}")

    if not matched_files:
        return "", False, []

    for filename, content in matched_files:
        context += f"### {filename.replace('.txt', '').capitalize()} Manual ###\n"
        context += content.strip() + "\n\n"

    matched_filenames = [f[0] for f in matched_files]
    return context, True, matched_filenames