import subprocess
import os
import uuid
import tempfile


WHISPER_PATH = os.path.expanduser(
    "~/whisper.cpp/build/bin/whisper-cli"
)

MODEL_PATH = os.path.expanduser(
    "~/whisper.cpp/models/ggml-base.bin"
)
LANGUAGES = {
    "en": "English",
    "ml": "Malayalam",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ar": "Arabic",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
}

async def transcribe(audio_path):

    wav_file = f"{tempfile.gettempdir()}/{uuid.uuid4()}.wav"

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            audio_path,
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            wav_file
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


    # Normal transcription
    result = subprocess.run(
        [
            WHISPER_PATH,
            "-m",
            MODEL_PATH,
            "-f",
            wav_file,
            "--no-timestamps"
        ],
        capture_output=True,
        text=True
    )


    text = result.stdout.strip()


    # English translation
    translation = subprocess.run(
        [
            WHISPER_PATH,
            "-m",
            MODEL_PATH,
            "-f",
            wav_file,
            "--translate",
            "--no-timestamps"
        ],
        capture_output=True,
        text=True
    )


    english = translation.stdout.strip()


    os.remove(wav_file)


    return {
        "text": text,
        "english": english,
        "language": "unknown"
    }
