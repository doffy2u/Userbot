from dataclasses import dataclass


@dataclass
class Song:
    title: str
    url: str
    duration: int
    user_id: int
    username: str

    # Cached stream (prepared while another song is playing)
    stream: str | None = None

    # Playback timing
    started_at: float = 0
    paused_at: float = 0
    pause_offset: float = 0
    search_msg = None
    queue_msg = None


class MusicQueue:

    def __init__(self):
        self.items = []
        self.playing = False

    def add(self, song):
        self.items.append(song)

    def next(self):
        if not self.items:
            return None

        return self.items.pop(0)

    def clear(self):
        self.items.clear()
