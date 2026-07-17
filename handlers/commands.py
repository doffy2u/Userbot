from telethon import events

from storage.chats import enable, disable, is_enabled


async def handle_commands(event):
    # Only respond to your own messages
    if not event.out:
        return

    text = event.raw_text.strip().lower()

    chat_id = event.chat_id

    if text == ".enable":
        enable(chat_id)
        await event.reply("✅ Yapper is awake in this chat.")

    elif text == ".disable":
        disable(chat_id)
        await event.reply("😴 Yapper is going back to sleep.")

    elif text == ".status":
        if is_enabled(chat_id):
            await event.reply("🟢 Yapper is enabled here.")
        else:
            await event.reply("🔴 Yapper is disabled here.")
