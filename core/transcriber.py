import os
import whisper


WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

_model = None


def load_model():
    global _model

    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL}...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded.")

    return _model


def transcribe_chunk(chunk_path: str, language: str = None) -> str:
    model = load_model()

    options = {
        "task": "transcribe"
    }

    if language:
        options["language"] = language

    result = model.transcribe(
        chunk_path,
        **options
    )

    return result["text"].strip()


def transcribe_all(
    chunks: list,
    language: str = None
) -> str:

    full_transcript = ""

    for i, chunk in enumerate(chunks):

        print(
            f"Transcribing chunk "
            f"{i + 1}/{len(chunks)}..."
        )

        text = transcribe_chunk(
            chunk,
            language=language
        )

        full_transcript += text + " "

    print("Transcription complete.")

    return full_transcript.strip()