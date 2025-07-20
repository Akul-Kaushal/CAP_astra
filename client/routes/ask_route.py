import requests

def ask_question_to_server(prompt):
    try:
        response = requests.post("http://localhost:8000/ask", json={"prompt": prompt})
        return response.json()
    except Exception as e:
        return {"error": str(e)}
