import time

from storage.database import (
    set_afk,
    remove_afk,
    get_afk
)


async def handle_afk(event):

    sender = await event.get_sender()

    if getattr(sender, "bot", False):
        return

    # -------------------
    # Remove AFK on ANY message
    # -------------------
    afk = get_afk(
        event.chat_id,
        sender.id
    )

    is_afk_command = (
        event.raw_text
        and event.raw_text.strip().lower().startswith(".afk")
    )

    if afk and not is_afk_command:

        seconds = int(time.time()) - afk["start_time"]

        mins = seconds // 60
        hours = mins // 60
        days = hours // 24

        remove_afk(
            event.chat_id,
            sender.id
        )

        if days:
            duration = f"{days}d {hours % 24}h"
        elif hours:
            duration = f"{hours}h {mins % 60}m"
        else:
            duration = f"{mins}m"

        await event.reply(
            f"👋 Welcome back, {afk['name']}!\n\n"
            f"You were away for {duration}."
        )

        return

    # Ignore non-text messages after checking AFK
    if not event.raw_text:
        return

    text = event.raw_text.strip()

    # -------------------
    # .afk command
    # -------------------
    if text.lower().startswith(".afk"):

        reason = text[4:].strip()

        if not reason:
            reason = "AFK"

        # Prevent duplicate AFK
        if get_afk(event.chat_id, sender.id):
            await event.reply(
                f"🤖 {sender.first_name or sender.username or 'Unknown'} is already AFK."
            )
            return

        set_afk(
            event.chat_id,
            sender.id,
            sender.first_name or sender.username or "Unknown",
            reason
        )

        await event.reply(
            f" {sender.first_name or sender.username or 'Unknown'} is now AFK.\n\n"
            f"📝 {reason}"
        )
