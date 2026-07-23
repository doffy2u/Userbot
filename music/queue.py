from dataclasses import dataclass
import time


@dataclass
class Song:
    title: str
    url: str
    user_id: int
    username: str
    duration: int = 0

    started_at: float = 0
    paused_at: float = 0
    pause_offset: float = 0

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
