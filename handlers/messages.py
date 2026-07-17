from storage.database import save_message
from storage.chats import is_enabled


async def handle_message(event):

    # Only enabled chats
    if not is_enabled(event.chat_id):
        return

    # Ignore your own messages
    if event.out:
        return

    # Ignore non-text messages for now
    if not event.raw_text:
        return

    # Ignore commands
    if event.raw_text.startswith("/"):
        return

    sender = await event.get_sender()
    if getattr(sender, "bot", False):
        return

    if sender.username:
        name = sender.username
    else:
        name = sender.first_name or "Unknown"

    save_message(
        event.chat_id,
        name,
        event.raw_text
    )
