from yt_dlp import YoutubeDL


def get_audio_url(query: str):
    opts = {
        "quiet": True,
        "noplaylist": True,
        "format": "bestaudio/best",
    }

    with YoutubeDL(opts) as ydl:
        result = ydl.extract_info(
            f"ytsearch1:{query}",
            download=False
        )

        entry = result["entries"][0]

        return {
            "title": entry["title"],
            "url": entry["url"],
            "duration": entry.get("duration")
        }
