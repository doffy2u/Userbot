from collections import Counter

MY_NAMES = [
    "bogdan",
    "bogie",
    "acbd",
    "abcd",
    "bogiee",
    "bogdon",
    
    
]

IGNORED = {
    "the", "is", "are", "was", "were",
    "a", "an", "and", "or",
    "to", "of", "for", "with",
    "i", "you", "me", "my",
    "your", "our", "we",
    "they", "it", "this",
    "that", "have", "has",
    "had", "will", "would",
    "can", "could", "sum"
}


def analyze(rows):

    users = Counter()
    words = Counter()
    mentions = []

    for sender, message in rows:

        users[sender] += 1

        lower = message.lower()

        for name in MY_NAMES:
            if name in lower:
                mentions.append((sender, message))
                break

        for word in lower.split():

            word = word.strip(".,!?()[]{}:;\"'")

            if len(word) < 3:
                continue

            if word in IGNORED:
                continue

            words[word] += 1

    return {
        "messages": len(rows),
        "people": users.most_common(3),
        "topics": words.most_common(5),
        "mentions": mentions[-5:]
    }
