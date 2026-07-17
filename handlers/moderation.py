from telethon import events
from storage.database import save_event


async def handle_moderation(event):

    if not hasattr(event, "action"):
        return

    action = event.action

    # ...rest of your code...

    event_type = None
    target = None

    if hasattr(action, "user_id"):
        target = str(action.user_id)

    name = "Unknown"

    if hasattr(action, "prev_participant"):
        event_type = "kicked"

    elif hasattr(action, "new_participant"):
        event_type = "joined"

    elif action.__class__.__name__ == "ChannelParticipantBanned":
        event_type = "banned"

    if event_type:
        save_event(
            chat_id=event.chat_id,
            event_type=event_type,
            target=target
        )
