def parse_command(transcription: str) -> dict:
    """
    Parses the voice transcription and returns intent(s) and related info.
    Supports multiple intents like upload + ask in the same sentence.
    """

    transcription = transcription.strip().lower()
    result = {
        "intents": [],
        "upload_file": None,
        "ask_topic": None,
        "raw": transcription
    }

    if not transcription:
        result["intents"].append("none")
        return result

    # Detect upload intent
    if "upload" in transcription:
        result["intents"].append("upload")
        words = transcription.split()
        try:
            idx = words.index("upload")
            file = " ".join(words[idx + 1:]) or "unknown_file"
        except (ValueError, IndexError):
            file = "unknown_file"
        result["upload_file"] = file

    # Detect ask intent
    if any(q in transcription for q in ["how", "what", "why", "when", "where", "who", "can you", "tell me"]):
        result["intents"].append("ask")
        result["ask_topic"] = transcription  # You could refine this further

    if not result["intents"]:
        result["intents"].append("other")

    return result
