import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "sessions/userbot"
archive_channel = os.getenv("ARCHIVE_CHANNEL")
ARCHIVE_CHANNEL = int(archive_channel) if archive_channel else None
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
