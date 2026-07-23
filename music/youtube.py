from yt_dlp import YoutubeDL


def get_audio(video_id):

    url = f"https://www.youtube.com/watch?v={video_id}"

    opts = {
        "quiet": True,
        "noplaylist": True,
        "format": "bestaudio/best",
    }

    with YoutubeDL(opts) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

        return {
            "title": info["title"],
            "url": info["url"],
            "duration": info.get("duration")
        }
