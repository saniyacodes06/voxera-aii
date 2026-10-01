from utils.audio_processor import process_input
from core.transcriber import transcribe_all


def process_and_transcribe(
    source: str,
    language: str = None
) -> tuple[str, str]:
    """
    Process a YouTube URL or uploaded file,
    then transcribe the resulting audio.
    """

    print("Step 1: Processing audio...")
    audio_path = process_input(source)

    print(f"Audio ready: {audio_path}")

    print("Step 2: Transcribing audio...")

    transcript = transcribe_all(
        [audio_path],
        language=language
    )

    print("Transcription finished.")

    return audio_path, transcript