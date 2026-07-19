from telethon.sync import TelegramClient
from config import API_ID, API_HASH

CHANNEL_ID = -1004362776514

with TelegramClient("yapper", API_ID, API_HASH) as client:
    client.send_message(CHANNEL_ID, "✅ Userbot connected successfully!")
