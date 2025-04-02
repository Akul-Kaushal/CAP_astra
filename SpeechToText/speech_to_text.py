import speech_recognition as sr
import numpy as np

# Initialize Recognizer
recognizer = sr.Recognizer()

# Function to reduce background noise
def adjust_noise(source, recognizer):
    print("Calibrating for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce noise
    print("Calibration complete.")

# Function for high-accuracy speech recognition
def recognize_speech():
    with sr.Microphone() as source:
        adjust_noise(source, recognizer)  # Noise calibration
        print("Listening... Speak clearly.")
        audio = recognizer.listen(source, timeout=50)  # Listen for speech

    try:
        # Convert speech to text using Google's API
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"Recognized Speech: {text}")
        return text

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return None

    except sr.RequestError:
        print("Error: Could not request results. Check your internet connection.")
        return None

# Run Speech Recognition
if __name__ == "__main__":
    result = recognize_speech()
    if result:
        print(f"You said: {result}")
