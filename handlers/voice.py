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

    if not event.voice:
        return

    if not is_enabled(event.chat_id):
        return

    reply = await event.reply(
        pick(LOADING_MESSAGES)
    )

    path = await event.download_media(
        file=tempfile.gettempdir()
    )

    try:
        result = await transcribe(path)

        text = result["text"]
        english = result["english"]

        if text:

            if text.lower() == english.lower():

                message = (
                    f"📝 {text}"
                    f"{maybe_signature()}"
                )

            else:

                message = (
                    f"🌐 Language detected\n\n"
                    f"🗣️ They said:\n"
                    f"{text}\n\n"
                    f"🇬🇧 English:\n"
                    f"{english}"
                    f"{maybe_signature()}"
                )

            await reply.edit(message)

        else:
            await reply.edit(
                pick(ERROR_MESSAGES)
            )

    finally:
        if path and os.path.exists(path):
            os.remove(path)
