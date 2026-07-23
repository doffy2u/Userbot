async def preload(song):
    """
    Prepare a song for instant playback.

    Right now, yt-dlp already gives us a direct stream URL,
    so we simply cache it.

    Later, this is where we'll refresh expired URLs,
    resolve streams in advance, or perform other optimizations.
    """

    if song.stream:
        return

    song.stream = song.url
