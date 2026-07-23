import time

import music.player as player
from music.youtube import get_audio_url
from music.session import get_session
from music.queue import Song
from music.status import update_status
from music.fairness import check_request, add_request


async def handle_music(event):

    text = event.raw_text.strip()

    if not text.startswith(".play"):
        return

    query = text[5:].strip()

    if not query:
        await event.reply(
            "Usage: .play <song>"
        )
        return

    allowed = check_request(
        event.sender_id
    )

    if not allowed:
        await event.reply(
"""╭─ 🎧 Music Queue
│
│ Your previous song is still having its turn 🎶
│
│ Let someone else pick the songs too 😋
╰─────────────"""
        )
        return

    search_msg = await event.reply(
        f"🔍 Searching for: {query}"
    )

    try:

        info = get_audio_url(query)

        session = get_session(
            event.chat_id
        )

        song = Song(
            title=info["title"],
            url=info["url"],
            duration=info["duration"],
            user_id=event.sender_id,
            username=(
                event.sender.first_name
                if event.sender
                else "Unknown"
            )
        )

        add_request(
            event.sender_id,
            song.title
        )

        session.add(song)

        queue_msg = await event.reply(
f"""🎵 Added to queue

✨ {song.title}
👤 {song.username}"""
        )

        if not session.playing:

            try:
                await search_msg.delete()
            except Exception:
                pass

            try:
                await queue_msg.delete()
            except Exception:
                pass

            await play_next(
                event.chat_id
            )

    except Exception as e:

        try:
            await search_msg.delete()
        except Exception:
            pass

        await event.reply(
            f"❌ {e}"
        )


async def play_next(chat_id):

    session = get_session(chat_id)

    song = session.next()

    if not song:
        session.playing = False
        session.current = None
        return

    session.playing = True
    session.current = song

    song.started_at = time.time()
    song.pause_offset = 0
    song.paused_at = 0

    await update_status(
        player.client,
        session,
        chat_id,
        song
    )

    await player.pytg.play(
        chat_id,
        stream=song.url
    )


player.set_next_callback(play_next)
