from telethon import events
from collections import Counter
from services.summary import get_summary
from storage.database import update_last_briefing
from storage.database import get_recent_events

MY_NAMES = [
    "bogdan",
    "bogie",
    "acbd",
    "abcd",
    "bogiee",
    "bogdon",
    "bog",
]

async def handle_summary(event):
    # Only respond to your own command
    if not event.out:
        return

    # Command
    if event.raw_text.strip().lower() != ".sum":
        return

    rows = get_summary(
        event.chat_id,
        event.sender_id
    )

    if not rows:
        await event.reply("📭 Nothing to summarize yet.")
        return

    message_count = len(rows)

    users = Counter()
    words = Counter()
    mentions = []

    ignored = {
        "the", "is", "are", "was", "were",
        "a", "an", "and", "or", "to", "of",
        "i", "you", "me", "my", "your",
        "our", "we", "they", "it", "this",
        "that", "for", "with", "from", "have",
        "has", "had", "will", "would", "can",
        "could", "sum"
    }

    for sender, message in rows:

        users[sender] += 1

        lower = message.lower()

        # Mention detection
        for name in MY_NAMES:
            if name in lower:
                mentions.append((sender, message))
                break

        # Word counting
        for word in lower.split():

            word = word.strip(".,!?()[]{}:;\"'")

            if len(word) < 3:
                continue

            if word in ignored:
                continue

            words[word] += 1

    top_people = users.most_common(3)
    top_words = words.most_common(5)

    report = "Till now since you last checked.\n\n"

    report += f"💬 Messages analyzed: {message_count}\n\n"

    report += "👥 Most active:\n"
    for name, count in top_people:
        report += f"• {name}: {count}\n"
    

    report += "\n\n mentions:\n"

    if mentions:
        for sender, message in mentions[-5:]:
            report += (
                f"\n• {sender}\n"
                f'  💬 "{message}"\n'
            )
    else:
        report += "none :)"
    recent_events = get_recent_events(
        event.chat_id,
        event.sender_id
    )

    if recent_events:
        report += "\n\n⚠️ Events since last check:\n"

        for e in recent_events:
            report += (
                f"• {e['event_type'].title()}: "
                f"{e['user']}\n"
            )

    await event.reply(report)

    update_last_briefing(
        event.chat_id,
        event.sender_id
    )
