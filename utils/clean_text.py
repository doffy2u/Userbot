import re


def clean_transcript(text):

    text = text.strip()

    # Remove whisper artifacts
    text = re.sub(
        r"\[.*?\]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()
