from music.session import get_session


async def handle_queue(event):

    text = event.raw_text.strip()

    if text not in [".queue", ".que"]:
        return


    session = get_session(
        event.chat_id
    )


    if not session.current and not session.items:
        await event.reply(
            "🎧 The queue is empty."
        )
        return


    msg = "╭─ 🎧 Music Queue\n│\n"


    if session.current:

        msg += (
            f"│ 🎶 Playing:\n"
            f"│ ✨ {session.current.title}\n"
            f"│ 👤 {session.current.username}\n"
            f"│\n"
        )


    if session.items:

        msg += "│ ⏭ Next:\n"

        for i, song in enumerate(
            session.items,
            start=1
        ):

            msg += (
                f"│ {i}. {song.title}\n"
                f"│    👤 {song.username}\n"
            )

            if i >= 10:
                break


    msg += "╰─────────────"


    await event.reply(msg)
