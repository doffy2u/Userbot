import random

LOADING_MESSAGES = [
    "⏳ Hold up... turning this into text.",
    "🎧 Lemme listen to this...",
    "🤔 One sec... decoding human noises.",
    "👂 Listening very carefully...",
    "🧠 Processing voice...",
    "🎙️ Cooking the transcript...",
]

INTRO_MESSAGES = [
    "👂 I think they said...",
    "📝 What I heard...",
    "🗣️ Here's what they said...",
    "💬 Human → Text",
    "📜 Decoded message",
]

SONG_MESSAGES = [
    "🎵 That's a banger. I'm not posting the lyrics. 😌",
    "🎶 Music detected. Enjoy the vibes.",
    "🎤 Nice song. No lyric spam from me.",
    "💃 I'm here for speeches, not concerts.",
]

ERROR_MESSAGES = [
    "🤷 Couldn't understand that one.",
    "😵 My ears gave up.",
    "🔇 Too much noise.",
    "🙃 I tried. Promise.",
]

SIGNATURES = [
    "— Your neighborhood stenographer ✍️",
    "— Certified eavesdropper 👂",
    "— Professional listener 🎧",
    "— Definitely not spying 👀",
    "— Powered by caffeine ☕",
]


def pick(messages):
    return random.choice(messages)


def maybe_signature():
    if random.randint(1, 100) <= 30:
        return "\n\n" + random.choice(SIGNATURES)
    return ""
