import subprocess
import os


WHISPER_PATH = os.path.expanduser(
    "~/whisper.cpp/build/bin/whisper-cli"
)

MODEL_PATH = os.path.expanduser(
    "~/whisper.cpp/models/ggml-base.bin"
)


def run_whisper(audio_file, translate=False):

    command = [
        WHISPER_PATH,
        "-m",
        MODEL_PATH,
        "-f",
        audio_file,
        "--no-timestamps"
    ]

    if translate:
        command.append("--translate")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()
