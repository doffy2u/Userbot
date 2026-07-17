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


async def transcribe(audio_path):

    wav_file = f"{tempfile.gettempdir()}/{uuid.uuid4()}.wav"

    print("🔄 Converting audio...")

    convert = subprocess.run(
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
        capture_output=True,
        text=True
    )

    if convert.returncode != 0:
        print("FFMPEG ERROR:")
        print(convert.stderr)
        return None


    print("🧠 Running Whisper...")

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


    os.remove(wav_file)


    print("WHISPER:")
    print(result.stdout)


    # Remove whisper info lines
    lines = result.stdout.splitlines()

    text_lines = [
        line for line in lines
        if not line.startswith("[")
    ]

    text = " ".join(text_lines).strip()

    return text if text else None
