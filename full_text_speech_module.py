import speech_recognition as sr
import numpy as np
import pyttsx3

# Initialize Recognizer and Text-to-Speech Engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def adjust_noise(source, recognizer):
    """Reduce background noise."""
    print("Calibrating for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Calibration complete.")

def speak_text(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def recognize_speech():
    """Continuously capture and recognize speech until dead silence."""
    with sr.Microphone() as source:
        adjust_noise(source, recognizer)
        print("Listening... Speak clearly.")
        
        while True:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Listen for speech
                text = recognizer.recognize_google(audio, language="en-US")
                print(f"Recognized Speech: {text}")
                
                if text.strip():
                    print(f"{text}")
                    return text
                else:
                    print("No speech detected. Exiting...")
                    break
            
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand the audio.")
            except sr.RequestError:
                print("Error: Could not request results. Check your internet connection.")
            except sr.WaitTimeoutError:
                print("Silence detected. Exiting...")
                break

if __name__ == "__main__":
    recognize_speech()
