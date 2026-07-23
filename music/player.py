from pytgcalls import PyTgCalls
from pytgcalls.types import StreamEnded
from music.session import get_session
from music.status import clear_now_playing
from music.fairness import remove_request
from music.fairness import release_song
pytg = None
next_callback = None
client = None


def set_next_callback(callback):

    global next_callback

    next_callback = callback

    print("✅ Next callback registered")



async def on_stream_end(client, update):

    print(
        "🔥 PyTgCalls event:",
        type(update),
        update
    )


    if isinstance(update, StreamEnded):
    
        chat_id = update.chat_id
    
        session = get_session(chat_id)
    
    
        # Release previous owner
        release_song(
            session.current
        )
    
    
        await clear_now_playing(
            client,
            session,
            chat_id
        )
    
    
        session.current = None
    
    
        await next_callback(chat_id)
async def init_music(app):

    global pytg, client

    client = app


    pytg = PyTgCalls(client)


    pytg.add_handler(
        on_stream_end
    )


    await pytg.start()


    print(
        "🎵 Music engine started"
    )
