from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    me = await client.get_me()
    print(f"Logged in as: {me.first_name} (@{me.username})")

with client:
    client.loop.run_until_complete(main())
