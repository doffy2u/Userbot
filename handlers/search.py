import requests


async def handle_search(event):

    if not event.raw_text:
        return

    text = event.raw_text.strip()

    if not (
        text.startswith(".search")
        or text.startswith(".fact")
    ):
        return

    mode = "fact" if text.startswith(".fact") else "search"

    # -------- Get query --------

    if event.is_reply:

        reply = await event.get_reply_message()
        query = (reply.raw_text or "").strip()

        if not query:
            await event.reply("❌ Replied message is empty.")
            return

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
                "pretty": 1,
                "no_html": 1,
                "no_redirect": 1,
                "skip_disambig": 0
            },
            timeout=10
        )

        data = r.json()

        fields = [
            data.get("AbstractText", ""),
            data.get("Answer", ""),
            data.get("Definition", ""),
            data.get("Entity", "")
        ]

        answer = ""

        for field in fields:
            if field and field.strip():
                answer = field.strip()
                break

        if not answer:

            related = data.get("RelatedTopics", [])

            for item in related:

                if isinstance(item, dict):

                    if item.get("Text"):
                        answer = item["Text"]
                        break

                    for sub in item.get("Topics", []):

                        if sub.get("Text"):
                            answer = sub["Text"]
                            break

                if answer:
                    break

        if answer:

            if mode == "fact":
                await event.reply(f"📌 {answer[:1000]}")
            else:
                await event.reply(f"🔎 {answer[:1000]}")

        else:
            await event.reply("❌ No answer found.")

    except Exception as e:
        print(e)
        await event.reply("❌ Search failed.")
