import datetime

from storage.database import get_deleted


async def handle_deleted(event):

    if not event.raw_text:
        return

    text = event.raw_text.lower().strip()

    if text == ".del":

        await event.reply(
            "🗑 Deleted History\n\n"
            ".del1\n"
            ".del2\n"
            ".del3\n"
            ".del4\n"
            ".del5"
        )

        return

    if text not in (
        ".del1",
        ".del2",
        ".del3",
        ".del4",
        ".del5"
    ):
        return

    number = int(text[-1])

    row = get_deleted(
        event.chat_id,
        number
    )

    if not row:

        await event.reply(
            "Nothing found."
        )

        return

    sent = datetime.datetime.fromtimestamp(
        row["sent_time"]
    ).strftime("%d %b %Y %H:%M")

    deleted = datetime.datetime.fromtimestamp(
        row["deleted_time"]
    ).strftime("%d %b %Y %H:%M")

    if row["message_type"] == "text":

        await event.reply(

            f"🗑 Deleted Message #{number}\n\n"

            f"👤 {row['sender_name']}\n"

            f"@{row['username']}\n"

            f"🆔 {row['sender_id']}\n\n"

            f"💬 {row['text']}\n\n"

            f"📤 Sent: {sent}\n"

            f"🗑 Deleted: {deleted}"

        )

    else:

        await event.reply(

            f"🗑 Deleted Message #{number}\n\n"

            f"👤 {row['sender_name']}\n"

            f"@{row['username']}\n"

            f"🆔 {row['sender_id']}\n\n"

            f"📦 {row['message_type'].title()}\n\n"

            f"📤 Sent: {sent}\n"

            f"🗑 Deleted: {deleted}\n\n"

            f"⚠️ Media hidden for safety."

        )
