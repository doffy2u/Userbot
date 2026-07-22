import uuid
import edge_tts

VOICE = "en-US-AnaNeural"

async def make_voice(text):
    filename = f"/tmp/{uuid.uuid4()}.mp3"

    await edge_tts.Communicate(
        text=text,
        voice=VOICE
    ).save(filename)

    return filename
