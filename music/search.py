from ytmusicapi import YTMusic

ytmusic = YTMusic()


def search_song(query):

    results = ytmusic.search(
        query,
        filter="songs",
        limit=1
    )

    if not results:
        return None

    song = results[0]

    return {
        "title": song["title"],
        "video_id": song["videoId"],
        "artist": song["artists"][0]["name"]
    }
