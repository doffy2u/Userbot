import asyncio
import json
import os
import itertools

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import RetryAfter

from animation import render

# ==========================
# CONFIG
# ==========================

BOT_TOKEN = BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

MESSAGE_FILE = "message.json"

UPDATE_DELAY = 2  # seconds

HEART = itertools.cycle([
    "♡",
    "♥",
    "❤️",
    "♥",
    "♡",
    "♡",
    "♡",
    "♡",
])


# ==========================
# STATIC TEXT
# ==========================

HEADER = """
<b>𝗭 𝗜 𝗔</b>

<i>Built with purpose.
Shared by choice.</i>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

FOOTER = """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{heart} CORE        STABLE
● AI          LISTENING
♪ MUSIC       READY
◎ NETWORK     CONNECTED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<i>Initializing...</i>
"""


# ==========================
# MESSAGE STORAGE
# ==========================

def load_message_id():
    if not os.path.exists(MESSAGE_FILE):
        return None

    with open(MESSAGE_FILE, "r") as f:
        return json.load(f)["message_id"]


def save_message_id(mid):
    with open(MESSAGE_FILE, "w") as f:
        json.dump({"message_id": mid}, f)


# ==========================
# CREATE / LOAD MESSAGE
# ==========================

async def get_dashboard(bot: Bot):

    mid = load_message_id()

    if mid:
        return mid

    msg = await bot.send_message(
        chat_id=CHANNEL,
        text="Starting ZIA...",
    )

    save_message_id(msg.message_id)

    print("Dashboard created.")
    print("Message ID:", msg.message_id)

    return msg.message_id


# ==========================
# LOOP
# ==========================

async def animate(bot: Bot, message_id: int):

    while True:
        heart = next(HEART)

        text = (
            HEADER
            + "<pre>\n"
            + render()
            + "\n</pre>"
            + FOOTER.format(
                heart=heart
            )
        )

        try:

            await bot.edit_message_text(
                chat_id=CHANNEL,
                message_id=message_id,
                text=text,
                parse_mode=ParseMode.HTML,
            )

            await asyncio.sleep(UPDATE_DELAY)

        except RetryAfter as e:

            print(f"Flood wait: {e.retry_after}s")

            await asyncio.sleep(e.retry_after)

        except Exception as e:

            print(e)

            await asyncio.sleep(5)


# ==========================
# MAIN
# ==========================

async def main():

    bot = Bot(BOT_TOKEN)

    message_id = await get_dashboard(bot)

    await animate(bot, message_id)


if __name__ == "__main__":

    asyncio.run(main())
