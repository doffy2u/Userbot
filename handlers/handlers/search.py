import requests

async def handle_search(event):
    if not event.raw_text:
        return

    text = event.raw_text.strip()

    if not (text.startswith(".search") or text.startswith(".fact")):
        return

    mode = "fact" if text.startswith(".fact") else "search"

    if event.is_reply:
        reply = await event.get_reply_message()
        query = (reply.raw_text or "").strip()
    else:
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            await event.reply(f"Usage:\n.{mode} question")
            return
        query = parts[1].strip()

    try:
        r = requests.get(
            "https://api.duckduckgo.com/",
            params={
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1,
            },
            timeout=10,
        )

        data = r.json()

        answer = (
            data.get("Answer")
            or data.get("AbstractText")
            or data.get("Definition")
            or ""
        ).strip()

        if answer:
            if mode == "fact":
                await event.reply(f"📌 {answer[:1000]}")
            else:
                title = data.get("Heading", "").strip()
                if title:
                    await event.reply(f"🔎 {title}\n\n{answer[:1000]}")
                else:
                    await event.reply(f"🔎 {answer[:1000]}")
        else:
            await event.reply("❌ No answer found.")

    except Exception as e:
        print(e)
        await event.reply("❌ Search failed.")
