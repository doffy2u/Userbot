from music.queue import MusicQueue

class Session(MusicQueue):

    def __init__(self):
        super().__init__()
        self.current = None
        self.now_playing_message = None
        self.current = None
        self.now_playing_message = None
        self.progress_task = None


sessions = {}


def get_session(chat_id):

    if chat_id not in sessions:
        sessions[chat_id] = Session()

    return sessions[chat_id]
