import os
import requests
from dotenv import load_dotenv
import time
from .logger import log_interaction
from .semantic_search import find_similar_documents

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

    results = find_similar_documents(prompt, top_k=3, min_score=0.5)  # loosen threshold

    context = ""
    matched_files = []

    if results:
        for score, doc in results:
            filename = doc.get('filename', 'unknown')
            context += f"### Source: {filename} ###\n{doc['text']}\n\n"
            matched_files.append(filename)


    full_prompt = f"""
You are a helpful assistant trained on task-specific manuals. If any of the following documents are relevant, use them to answer the user's question. If they are not relevant, answer using general knowledge — but still keep it brief and focused.

Documents:
{context if context.strip() else '[No documents matched]'}

Question:
{prompt}

Provide the most appropriate answer in **Detail A tabular form wolud be much better**.
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

    


"""
Test function to query gemini paired with load_relevant_documents(prompt) to get context
def test_query_gemini():
"""
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



"""
Test function to check for matching documents
def load_relevant_document():
"""
# def simple_word_tokenize(text):
#     return re.findall(r'\b\w+\b', text.lower())

# def load_relevant_documents(prompt: str) -> tuple[str, bool, list[str]]:
#     context = ""
#     data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

#     STOPWORDS = {
#         "what", "is", "the", "how", "to", "a", "an", "of", "for", "in", "on", "and", "or", "with", "about", "do", "i", "you",
#         "are", "some", "this", "that", "it", "from", "was", "were"
#     }

#     # Tokenize the prompt properly
#     meaningful_words = [word for word in simple_word_tokenize(prompt) if word not in STOPWORDS]

#     matched_files = []

#     for filename in os.listdir(data_dir):
#         if filename.endswith(".txt"):
#             filepath = os.path.join(data_dir, filename)
#             with open(filepath, 'r', encoding='utf-8') as file:
#                 content = file.read().lower()
#                 content_words = set(simple_word_tokenize(content))  # tokenize file content once

#                 # Check how many words from prompt are in the content (as full words)
#                 match_count = sum(word in content_words for word in meaningful_words)

#                 if match_count >= 1:  # you can reduce to 1 match for more flexibility
#                     matched_files.append((filename, content))

#     print(f"[DEBUG] Matching words: {meaningful_words}")
#     print(f"[DEBUG] Matched files: {[f[0] for f in matched_files]}")

#     if not matched_files:
#         return "", False, []

#     for filename, content in matched_files:
#         context += f"### {filename.replace('.txt', '').capitalize()} Manual ###\n"
#         context += content.strip() + "\n\n"

#     matched_filenames = [f[0] for f in matched_files]
#     return context, True, matched_filenames