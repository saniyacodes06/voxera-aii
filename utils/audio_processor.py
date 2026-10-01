import os
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "noplaylist": True,
        "retries": 3,
        "fragment_retries": 3,
        "extractor_retries": 3,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            original_path = ydl.prepare_filename(info)
            wav_path = os.path.splitext(original_path)[0] + ".wav"

            if not os.path.exists(wav_path):
                raise RuntimeError("Audio conversion failed.")

            # Normalize YouTube audio for Whisper:
            # stereo/48kHz -> mono/16kHz
            normalized_path = convert_to_wav(wav_path)

            return normalized_path

    except Exception as e:
        raise RuntimeError(
            f"Could not process this YouTube video. "
            f"Please check that the video is public and available. "
            f"Details: {e}"
        )


def convert_to_wav(input_path: str) -> str:
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(output_path, format="wav")

    return output_path


def process_input(source: str) -> str:
    source = source.strip()

    if source.startswith(("http://", "https://")):
        print("Downloading YouTube audio...")
        return download_youtube_audio(source)

    print("Converting uploaded file...")
    return convert_to_wav(source)