import music.player as player
from music.session import get_session
from music.fairness import release_song
from music.status import clear_now_playing
from utils.permissions import is_admin

async def handle_music_controls(event):

    text = event.raw_text.strip()

    if text not in [
        ".pause",
        ".resume",
        ".skip",
        ".stop"
    ]:
        return


    chat_id = event.chat_id
    session = get_session(chat_id)


    if text == ".pause":

        await player.pytg.pause(
            chat_id
        )

        await event.reply(
            "⏸️ Music paused"
        )


    elif text == ".resume":

        await player.pytg.resume(
            chat_id
        )

        await event.reply(
            "▶️ Music resumed"
        )


    elif text == ".skip":
    
        if not await is_admin(event):
    
            await event.reply(
                "❌ Only admins can skip songs."
            )
    
            return
    
    
        if session.current:
    
            release_song(
                session.current
            )
    
        await clear_now_playing(
            player.client,
            session,
            chat_id
        )
    
        session.playing = False
    
        await event.reply(
            "⏭️ Skipped"
        )
    
        if player.next_callback:
    
            await player.next_callback(
                chat_id
            )
    elif text == ".stop":
    
        if not await is_admin(event):
    
            await event.reply(
                "❌ Only admins can stop the music."
            )
            return
    
    
        # Release the current requester
        if session.current:
            release_song(session.current)
    
    
        # Delete the Now Playing card
        await clear_now_playing(
            player.client,
            session,
            chat_id
        )
    
    
        # Clear everything
        session.items.clear()
        session.current = None
        session.playing = False
    
    
        # Stop playback and leave VC
        try:
            await player.pytg.leave_call(chat_id)
        except Exception:
            pass
    
    
        await event.reply(
            """
    ╭─ ⏹️ Music Stopped
    │
    │ Queue cleared.
    │ Voice chat disconnected.
    │
    │ 🎧 Thanks for listening~
    ╰─────────────
    """
        )
