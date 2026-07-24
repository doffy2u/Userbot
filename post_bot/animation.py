from pathlib import Path
import random

FACE_DIR = Path("faces")

frames = list(FACE_DIR.glob("*.txt"))

if not frames:
    raise RuntimeError("No .txt files found in faces/")

last = None


def render():
    global last

    choices = [f for f in frames if f != last]

    frame = random.choice(choices)

    last = frame

    return frame.read_text(encoding="utf-8")
