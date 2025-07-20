import os
import re
import difflib

def clean_filename(raw: str) -> str:
    corrections = {
        "dot text": ".txt",
        "dot txt": ".txt",
        "text": ".txt",
        "tx": ".txt",
        "file": "",
        "document": "",
        "a": "",
        "the": "",
        "random": "random",  # keep common filenames
    }

    raw = raw.lower()
    for k in sorted(corrections, key=len, reverse=True):
        raw = re.sub(rf"\b{k}\b", corrections[k], raw)

    # Remove unwanted characters but preserve dot and underscore
    raw = re.sub(r"[^\w\._]+", "_", raw).strip("_")

    # Ensure .txt if no extension
    if not re.search(r'\.\w+$', raw):
        raw += ".txt"

    return raw if raw else "unknown_file.txt"

def find_best_matching_file(filename: str, directory: str = "uploads") -> str | None:
    """
    Finds the most similar filename in the uploads directory.
    """
    try:
        files = os.listdir(directory)
        matches = difflib.get_close_matches(filename, files, n=1, cutoff=0.5)
        return matches[0] if matches else None
    except FileNotFoundError:
        return None

def parse_command(transcription: str, uploads_dir: str = "uploads") -> dict:
    """
    Parses transcription and identifies intent: 'upload', 'ask', or 'other'.
    Suggests matching file if original file is not found.
    """
    transcription = transcription.strip().lower()
    result = {
        "intents": [],
        "upload_file": None,
        "suggested_file": None,
        "ask_topic": None,
        "raw": transcription
    }

    if not transcription:
        result["intents"].append("none")
        return result

    words = transcription.split()

    # Upload intent
    if "upload" in words:
        result["intents"].append("upload")
        try:
            idx = words.index("upload")
            file_raw = " ".join(words[idx + 1:])
            cleaned = clean_filename(file_raw)
            result["upload_file"] = cleaned

            # Suggest close file if exact not found
            full_path = os.path.join(uploads_dir, cleaned)
            if not os.path.exists(full_path):
                suggestion = find_best_matching_file(cleaned, uploads_dir)
                if suggestion:
                    result["suggested_file"] = suggestion
        except IndexError:
            result["upload_file"] = "unknown_file.txt"

    # Ask intent
    if any(q in transcription for q in ["how", "what", "why", "when", "where", "who", "can you", "tell me"]):
        result["intents"].append("ask")
        result["ask_topic"] = transcription

    if not result["intents"]:
        result["intents"].append("other")

    return result

def handle_voice_command(transcription: str):
    parsed = parse_command(transcription)
    print(f"\nFinal Transcription: {parsed['raw']}")
    print(f"Parsed: {parsed}")

    if "upload" in parsed["intents"]:
        filename = parsed["upload_file"]
        filepath = os.path.join("uploads", filename)

        if os.path.exists(filepath):
            print(f"Uploading file: {filename}")
        elif parsed["suggested_file"]:
            print(f"File '{filename}' not found.")
            print(f"Did you mean '{parsed['suggested_file']}'?")
            confirm = input("Upload suggested file? (y/n): ").strip().lower()
            if confirm == 'y':
                print(f"Uploading file: {parsed['suggested_file']}")
            else:
                print("Upload cancelled.")
        else:
            print(f"No matching file found for '{filename}'. Upload aborted.")

    if "ask" in parsed["intents"]:
        print(f"Asking question: {parsed['ask_topic']}")
