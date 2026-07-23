requests = {}


def check_request(user_id):

    return user_id not in requests


def add_request(user_id, song):

    requests[user_id] = song


def remove_request(user_id):

    if user_id in requests:
        del requests[user_id]


def release_song(song):

    if song and hasattr(song, "user_id"):

        remove_request(
            song.user_id
        )
