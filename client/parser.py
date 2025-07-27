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
    Finds the most similar .txt filename in the uploads directory.
    Handles common voice recognition mistakes and plural/singular mismatches.
    """
    try:
        files = os.listdir(directory)
        txt_files = [f for f in files if f.endswith(".txt")]

        def try_match(name: str, candidates: list[str]) -> str | None:
            matches = difflib.get_close_matches(name, candidates, n=1, cutoff=0.4)
            return matches[0] if matches else None

        # 1. Try exact match
        match = try_match(filename, txt_files)
        if match:
            return match

        # 2. Try appending .txt
        if not filename.endswith(".txt"):
            match = try_match(filename + ".txt", txt_files)
            if match:
                return match

        # 3. Try removing .txt
        if filename.endswith(".txt"):
            base = filename.removesuffix(".txt")
            stripped_files = [f.removesuffix(".txt") for f in txt_files]
            match = try_match(base, stripped_files)
            if match:
                return match + ".txt"

        # 4. Try plural/singular conversions
        if filename.endswith("s.txt"):
            singular = filename.replace("s.txt", ".txt")
            if singular in txt_files:
                return singular
            match = try_match(singular, txt_files)
            if match:
                return match
        elif filename.endswith(".txt"):
            plural = filename.replace(".txt", "s.txt")
            if plural in txt_files:
                return plural
            match = try_match(plural, txt_files)
            if match:
                return match

        return None

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
    if "upload" in words:
        result["intents"].append("upload")
        try:
            idx = words.index("upload")
            file_raw = " ".join(words[idx + 1:])  
            cleaned = clean_filename(file_raw)


            result["upload_file"] = cleaned

            upload_dir_path = os.path.abspath(uploads_dir)
            full_path = os.path.join(upload_dir_path, cleaned)
            print(f"Full path to file: {full_path}")


            if not os.path.exists(full_path):
                suggestion = find_best_matching_file(file_raw, upload_dir_path)
                if suggestion:
                    print(f"[INFO] Suggested file based on fuzzy match: {suggestion}")
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

