import requests
import json
from full_text_speech_module import speak_text, recognize_speech

# Check if Ollama server is running
def check_server_status():
    try:
        response = requests.get('http://127.0.0.1:11434/v1/models')  # Check server status
        if response.status_code == 200:
            print("Ollama server is running.")
            return True
        else:
            print(f"Server is not responding with status code {response.status_code}.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        return False

# Query the model with a test message
def query_model():
    
    content_ = recognize_speech()
    print(" ")
    print(content_)
    url = 'http://127.0.0.1:11434/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'  # Ensure server knows we accept JSON responses
    }
    payload = {
        "model": "llama3:latest",  # Specify the model name explicitly
        "messages": [
            {"role": "user", "content": content_}
        ]
    }
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)  # Send the user query
        print("Response Status Code:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                quote = data['choices'][0]['message']['content']
                print("Model response:", quote)
                speak_text(quote)  
            else:
                print("No valid response from model.")
        else:
            print(f"Error querying model, status code: {response.status_code}")
            print("Response Content:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error querying model: {e}")

# Main execution flow
def main():
    if check_server_status():
        query_model()

if __name__ == '__main__':
    main()