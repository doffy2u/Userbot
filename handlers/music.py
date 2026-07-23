import time
from music.preload import preload
from music.session import get_session
from music.queue import Song
from music.status import update_status
from music.search import search_song
from music.youtube import get_audio
import music.player as player


async def handle_music(event):

    text = event.raw_text.strip()

    if not text.startswith(".play"):
        return

    query = text[5:].strip()

    if not query:
        await event.reply("Usage: .play <song>")
        return

    search_msg = await event.reply(
        f"🔍 Searching for: {query}"
    )

    try:
        result = search_song(query)

        if not result:
            await search_msg.edit("❌ Song not found.")
            return

        info = get_audio(
            result["video_id"]
        )

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

        song.search_msg = search_msg

        session.add(song)

        queue_msg = await event.reply(
f"""🎵 Added to queue

✨ {song.title}
👤 {song.username}"""
        )

        song.queue_msg = queue_msg

        if not session.playing:
            await play_next(
                event.chat_id
            )

    except Exception as e:
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

    # Remove temporary search/queue messages
    if song.search_msg:
        try:
            await song.search_msg.delete()
        except Exception:
            pass

    if song.queue_msg:
        try:
            await song.queue_msg.delete()
        except Exception:
            pass

    # Start playing first
    start = time.time()
    
    await player.pytg.play(
        chat_id,
        stream=song.stream or song.url
    )
    
    print(f"play() took {time.time() - start:.2f} seconds")

    # Show now playing after stream starts
    await update_status(
        player.client,
        session,
        chat_id,
        song
    )

    # Prepare next song
    if session.items:
        await preload(session.items[0])
player.set_next_callback(play_next)

