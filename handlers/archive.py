from telethon import events
from config import ARCHIVE_CHANNEL
from storage.chats import is_enabled


def register_archive(client):

    @client.on(events.NewMessage())
    async def archive_messages(event):

        if not is_enabled(event.chat_id):
            return

        if event.raw_text in [".enable", ".disable"]:
            return

        try:
            await client.forward_messages(
                ARCHIVE_CHANNEL,
                event.message
            )

        except Exception as e:
            print("Archive error:", e)
