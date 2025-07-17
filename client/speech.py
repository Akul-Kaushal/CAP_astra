import speech_recognition as sr
import time
from parser import parse_command


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


def listen_and_transcribe(language="en-IN", silence_threshold=4.0, timeout_duration=10, phrase_limit=15):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    wait_for_wake_word(recognizer, mic)

    with mic as source:
        audio_buffer = []
        last_spoken_time = time.time()

        while True:
            try:
                audio = recognizer.listen(source, timeout=timeout_duration, phrase_time_limit=phrase_limit)
                text = recognizer.recognize_google(audio, language=language) #type: ignore
                print("Heard:", text)
                audio_buffer.append(text)
                last_spoken_time = time.time()
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
        print(f"[UPLOAD] File to upload: {parsed['upload_file']}")

    if "ask" in parsed["intents"]:
        print(f"[ASK] Topic: {parsed['ask_topic']}")

    if not parsed["intents"]:
        print("Command not recognized.")
