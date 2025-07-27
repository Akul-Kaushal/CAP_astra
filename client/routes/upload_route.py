import os
import requests

def upload_file_to_server(file_path: str, server_url="http://localhost:8000/upload"):

    if not os.path.exists(file_path):
        print(f"[ERROR _upload] File not found: {file_path}")
        return None


    if not file_path.endswith(".txt"):
        print("[ERROR] Only .txt files are supported.")
        return None

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        try:
            response = requests.post(server_url, files=files)
            if response.status_code == 200:
                print("[SUCCESS]", response.json())
                return response.json()
            else:
                print(f"[FAILURE] Status Code: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"[ERROR] Could not connect to server: {e}")
