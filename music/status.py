async def clear_now_playing(client, session, chat_id):

    if session.now_playing_message:

        try:
            await session.now_playing_message.delete()
        except:
            pass

        session.now_playing_message = None


async def update_status(client, session, chat_id, song):

    await clear_now_playing(
        client,
        session,
        chat_id
    )

    msg = await client.send_file(
        chat_id,
        "music/assets/now_playing.mp4",
        caption=f"""╭─ 🎶 Now Playing
│
│ ✨ {song.title}
│ 👤 Requested by {song.username}
│
│ 🎧 Queue: {len(session.items)}
│
│ 💫 Sit back and enjoy~
╰─────────────"""
    )

    session.now_playing_message = msg
