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
#from handlers.search import handle_search
from handlers.replay import handle_ai_reply
from handlers.music import handle_music
from music.player import init_music
from music.youtube import get_audio
from handlers.queue import handle_queue
from handlers.music_controls import handle_music_controls
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
    handle_ai_reply,
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
client.add_event_handler(
    handle_music,
    events.NewMessage()
)
client.add_event_handler(
    handle_queue,
    events.NewMessage()
)
client.add_event_handler(
    handle_music_controls,
    events.NewMessage()
)
#register_archive(client)
#client.add_event_handler(
    #handle_search,
    #events.NewMessage()
#)

print("👂 Yapper is online...")

client.start()
client.loop.run_until_complete(
    init_music(client)
)
client.run_until_disconnected()
