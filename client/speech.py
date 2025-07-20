import speech_recognition as sr
import time
from parser import parse_command
import requests
import os
import shutil

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

def listen_and_transcribe(language="en-IN", silence_threshold=4.0, timeout_duration=10, phrase_limit=15, max_phrases=5):
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
                text = recognizer.recognize_google(audio, language=language).lower()  # type: ignore
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
        # Updated path to point to actual location
        upload_dir = os.path.join("client", "uploads")
        filename = parsed["upload_file"]
        filepath = os.path.join(upload_dir, filename)

        if not os.path.exists(filepath):
            print(f"File not found at {filepath}")
        else:
            with open(filepath, "rb") as f:
                files = {"file": (filename, f, "text/plain")}
                try:
                    response = requests.post("http://localhost:8000/upload", files=files)
                    print("Upload Response:", response.json())

                    # Optional: copy file to /data for use in RAG
                    data_path = os.path.join("data", filename)
                    shutil.copy(filepath, data_path)
                    print(f"Copied uploaded file to: {data_path}")

                except Exception as e:
                    print("Upload failed:", e)

    if "ask" in parsed["intents"]:
        try:
            response = requests.post("http://localhost:8000/ask", json={"prompt": parsed["ask_topic"]})
            print("Gemini Response:", response.json())
        except Exception as e:
            print("Ask failed:", e)

    if not parsed["intents"]:
        print("Command not recognized.")
