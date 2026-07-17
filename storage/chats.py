import json
import os

FILE = "enabled_chats.json"

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)


def get_enabled():
    with open(FILE, "r") as f:
        return json.load(f)


def save(enabled):
    with open(FILE, "w") as f:
        json.dump(enabled, f)


def is_enabled(chat_id):
    return chat_id in get_enabled()


def enable(chat_id):
    chats = get_enabled()

    if chat_id not in chats:
        chats.append(chat_id)

    save(chats)


def disable(chat_id):
    chats = get_enabled()

    if chat_id in chats:
        chats.remove(chat_id)

    save(chats)
