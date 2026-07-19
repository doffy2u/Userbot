import logging

logging.basicConfig(
    level=logging.WARNING
)
from telethon import TelegramClient, events
from config import API_ID, API_HASH, SESSION_NAME
from handlers.voice import handle_voice
from handlers.commands import handle_commands
from storage.database import init_db
from handlers.messages import handle_message
from telethon import events
from handlers.summary import handle_summary
from storage.database import cleanup_old_messages
from handlers.moderation import handle_moderation
from handlers.scramble import handle_scramble
from services.anagram import load_dictionary
from handlers.afk import handle_afk
from handlers.archive import register_archive
from handlers.search import handle_search

client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH
)
init_db()
cleanup_old_messages()
print("Loading dictionary...")
load_dictionary()
print("Dictionary loaded.")
client.add_event_handler(
    handle_voice,
    events.NewMessage
)

client.add_event_handler(
    handle_commands,
    events.NewMessage
)
client.add_event_handler(
    handle_message,
    events.NewMessage()
)
client.add_event_handler(
    handle_summary,
    events.NewMessage()
)
client.add_event_handler(
    handle_moderation,
    events.Raw()
)
client.add_event_handler(
    handle_scramble,
    events.NewMessage()
)
client.add_event_handler(
    handle_afk,
    events.NewMessage()
)
register_archive(client)
client.add_event_handler(
    handle_search,
    events.NewMessage()
)

print("👂 Yapper is online...")

client.start()

client.run_until_disconnected()
