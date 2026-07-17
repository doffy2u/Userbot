import os
import tempfile

from utils.messages import (
    pick,
    LOADING_MESSAGES,
    INTRO_MESSAGES,
    ERROR_MESSAGES,
    maybe_signature,
)

from services.transcription import transcribe
from storage.chats import is_enabled


async def handle_voice(event):

    print("📩 Message received")

    if not event.voice:
        return

    print("🎤 Voice detected")

    if not is_enabled(event.chat_id):
        print("🚫 Chat disabled")
        return

    print("✅ Chat enabled")

    reply = await event.reply(
        pick(LOADING_MESSAGES)
    )

    # Download temporarily
    path = await event.download_media(
        file=tempfile.gettempdir()
    )

    print("📥 Downloaded:", path)

    try:
        print("🧠 Starting whisper...")

        text = await transcribe(path)

        print("📝 Result:", text)

        if text:
            message = (
                f"{pick(INTRO_MESSAGES)}\n\n"
                f"{text}"
                f"{maybe_signature()}"
            )

            await reply.edit(message)

        else:
            await reply.edit(
                pick(ERROR_MESSAGES)
            )

    finally:
        # Always delete audio after processing
        if path and os.path.exists(path):
            os.remove(path)
            print("🗑️ Deleted temporary voice file")
