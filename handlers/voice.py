import os
from storage.chats import is_enabled

from utils.messages import (
    pick,
    LOADING_MESSAGES,
    INTRO_MESSAGES,
    ERROR_MESSAGES,
    maybe_signature,
)
from services.transcription import transcribe

DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


async def handle_voice(event):
    # Ignore non-voice messages
    if not event.voice:
        return
    if not is_enabled(event.chat_id):
        return
   
    # Random loading message
    reply = await event.reply(
        pick(LOADING_MESSAGES)
    )

    # Download the voice note
    path = await event.download_media(file=DOWNLOAD_FOLDER)

    # Transcribe (placeholder for now)
    text = await transcribe(path)

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
