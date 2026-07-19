from storage.database import (
    save_message,
    get_all_afk
)

from storage.chats import is_enabled

import time


async def handle_message(event):

    if not is_enabled(event.chat_id):
        return

    if event.out:
        return

    text = event.raw_text or ""

    sender = await event.get_sender()

    if getattr(sender, "bot", False):
        return

    if sender.username:
        name = sender.username
    else:
        name = sender.first_name or "Unknown"

    message_type = "text"
    text = event.raw_text or ""
    file_path = ""
    
    if event.photo:
        message_type = "photo"
        file_path = await event.download_media(
            file=f"downloads/{event.id}"
        )
    
    elif event.sticker:
        message_type = "sticker"
        file_path = await event.download_media(
            file=f"downloads/{event.id}"
        )
    
    elif event.gif:
        message_type = "gif"
        file_path = await event.download_media(
            file=f"downloads/{event.id}"
        )
    
    elif event.video:
        message_type = "video"
        file_path = await event.download_media(
            file=f"downloads/{event.id}"
        )
    
    elif event.voice:
        message_type = "voice"
        file_path = await event.download_media(
            file=f"downloads/{event.id}"
        )
    
    elif event.document:
        message_type = "document"
        file_path = await event.download_media(
            file=f"downloads/{event.id}"
        )
    
    save_message(
        event.id,
        event.chat_id,
        sender.id,
        sender.first_name or "Unknown",
        sender.username or "",
        message_type,
        text,
        file_path or ""
    )

    text = text.lower()

    afk_users = get_all_afk(event.chat_id)

    for afk in afk_users:

        found = False

        # Username or display name mentioned
        if afk["name"].lower() in text:
            found = True

        # Reply to AFK user
        if event.is_reply:

            reply = await event.get_reply_message()

            if reply and reply.sender_id == afk["user_id"]:
                found = True

        if not found:
            continue

        seconds = int(time.time()) - afk["start_time"]

        mins = seconds // 60
        hours = mins // 60
        days = hours // 24

        if days:
            duration = f"{days}d {hours % 24}h"

        elif hours:
            duration = f"{hours}h {mins % 60}m"

        else:
            duration = f"{mins}m"

        await event.reply(
            f"🤖 {afk['name']} is currently AFK.\n\n"
            f"📝 {afk['reason']}\n"
            f"⏱ Away for: {duration}"
        )

        break
