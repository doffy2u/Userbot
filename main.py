from telethon import TelegramClient, events

from config import API_ID, API_HASH, SESSION_NAME
from handlers.voice import handle_voice
from handlers.commands import handle_commands

client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH
)

client.add_event_handler(
    handle_voice,
    events.NewMessage
)

client.add_event_handler(
    handle_commands,
    events.NewMessage
)

print("👂 Yapper is online...")

client.start()

client.run_until_disconnected()
