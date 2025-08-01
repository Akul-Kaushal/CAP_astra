import speech_recognition as sr
import time
from parser import parse_command
import requests
import os
import shutil
import pyttsx3  
from routes.upload_route import upload_file_to_server as upload_file
from routes.ask_route import ask_question_to_server as ask_gemini

engine = pyttsx3.init()
current_text = ""  

def speak(text):
    global current_text
    if not text or not isinstance(text, str):
        print("[ERROR] Invalid text for TTS:", text)
        return
    try:
        current_text = text
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("[TTS ERROR]", e)

def wait_for_wake_word(recognizer, mic, wake_word="astra", timeout=5):
    print(f"Say '{wake_word}' to activate...")
    while True:
        with mic as source:
            try:
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                text = recognizer.recognize_google(audio).lower()
                print("Heard:", text)
                if wake_word in text:
                    print("Wake word detected. Listening for command...")
                    return
            except sr.WaitTimeoutError:
                print("...Still waiting")
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"Error while listening: {e}")
                continue

def listen_and_transcribe(language="en-IN", silence_threshold=4.0, timeout_duration=10, phrase_limit=15, max_phrases=10):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=3)

    wait_for_wake_word(recognizer, mic)

    print("Listening for command (say 'stop listen' to finish)...")

    audio_buffer = []
    last_spoken_time = time.time()
    phrase_count = 0

    with mic as source:
        while phrase_count < max_phrases:
            try:
                audio = recognizer.listen(source, timeout=timeout_duration, phrase_time_limit=phrase_limit)
                text = recognizer.recognize_google(audio, language=language).lower() #type: ignore
                print("Heard:", text)

                if any(phrase in text for phrase in ["stop listen", "that's all", "done", "end input", "stop now"]):
                    print("Stop command detected. Ending...")
                    break

                audio_buffer.append(text)
                last_spoken_time = time.time()
                phrase_count += 1

            except sr.WaitTimeoutError:
                if time.time() - last_spoken_time > silence_threshold:
                    print("Silence detected. Stopping...")
                    break
                continue
            except sr.UnknownValueError:
                print("Could not understand audio.")
                continue
            except Exception as e:
                print("Error:", e)
                break

    full_text = " ".join(audio_buffer)
    print("\nFinal Transcription:", full_text)
    return full_text

if __name__ == "__main__":
    transcription = listen_and_transcribe()
    parsed = parse_command(transcription)

    print("Parsed:", parsed)

    if "upload" in parsed["intents"]:
        filename = parsed["upload_file"]

        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, "uploads", filename)
        print(f"{parsed['suggested_file']}")
        print(f"Full path to file: {filepath}")
        
        if os.path.exists(filepath):
            upload_response = upload_file(filepath)
            print("Upload Response:", upload_response)
            if upload_response:
                speak(f"{filename} uploaded successfully. Would you like to ask a question from this file?")
                followup = listen_and_transcribe()
                print("Follow-up:", followup)
                
                followup_parsed = parse_command(followup)
                if "ask" in followup_parsed["intents"]:
                    ask_response = ask_gemini(followup_parsed["ask_topic"])
                    print("Gemini Response:", ask_response)
                elif followup.strip():
                    ask_response = ask_gemini(followup)
                    print("Gemini Response:", ask_response)
                else:
                    print("No question asked.")


        elif parsed["suggested_file"]:
            print(f"[ERROR] File '{filename}' not found.")
            print(f"Did you mean '{parsed['suggested_file']}'?")
            confirm = input("Upload suggested file? (y/n): ").strip().lower()
            if confirm == 'y':
                filepath = os.path.join(base_dir, "uploads", parsed["suggested_file"])
                upload_response = upload_file(filepath)
                print("Upload Response:", upload_response)
            else:
                print("Upload cancelled.")
        else:
            print(f"[ERROR] File not found: {filename}")

    if "ask" in parsed["intents"]:
        ask_response = ask_gemini(parsed["ask_topic"])
        print("Gemini Response:", ask_response)
        speak(ask_response)

    if not parsed["intents"]:
        print("Command not recognized.")
