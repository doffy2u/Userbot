from collections import defaultdict

DICT_FILE = "dictionary/enable2k.txt"
FREQ_FILE = "dictionary/frequency.txt"

ANAGRAMS = defaultdict(list)
FREQUENCY = {}


def signature(word: str) -> str:
    return "".join(sorted(word.lower()))


def load_dictionary():
    with open(DICT_FILE, "r") as f:
        for line in f:
            word = line.strip().lower()

            if not word.isalpha():
                continue

            ANAGRAMS[signature(word)].append(word)


def load_frequency():
    with open(FREQ_FILE, "r") as f:
        for rank, line in enumerate(f):
            parts = line.strip().split()

            if not parts:
                continue

            word = parts[0].lower()

            FREQUENCY[word] = rank


def get_candidates(scrambled: str):
    words = ANAGRAMS.get(signature(scrambled), [])

    return sorted(
        words,
        key=lambda w: FREQUENCY.get(w, 999999)
    )


load_dictionary()
load_frequency()
