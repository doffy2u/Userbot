from pytgcalls import PyTgCalls
from pytgcalls.types import StreamEnded

pytg = None
client = None
next_callback = None


def set_next_callback(callback):
    global next_callback
    next_callback = callback
    print("✅ Next callback registered")


async def on_stream_end(client, update):

    print("🔥 Event:", type(update))

    if isinstance(update, StreamEnded):
        print("🎵 Stream ended")

        if next_callback:
            await next_callback(update.chat_id)


async def init_music(app):

    global pytg, client

    client = app
    pytg = PyTgCalls(client)

    pytg.add_handler(on_stream_end)

    await pytg.start()

    print("🎵 Music engine started")
