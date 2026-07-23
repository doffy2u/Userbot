async def is_admin(event):

    if not event.is_group:
        return True

    permissions = await event.client.get_permissions(
        event.chat_id,
        event.sender_id
    )

    return (
        permissions.is_admin
        or permissions.is_creator
    )
