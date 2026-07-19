from ddgs import DDGS
import asyncio

BLOCKED = {
    "porn",
    "xxx",
    "hentai",
    "nsfw",
    "onlyfans",
    "sex"
}


async def handle_search(event):

    if not event.raw_text:
        return

    text = event.raw_text.strip()

    if not text.startswith(".search"):
        return

    query = text[len(".search"):].strip()

    if not query:
        await event.reply("Usage: .search <question>")
        return

    # 18+ filter
    if any(word in query.lower().split() for word in BLOCKED):
        await event.reply("🚫 Explicit searches are blocked.")
        return

    try:
        await event.reply("🔎 Searching...")

        results = await asyncio.to_thread(
            lambda: list(
                DDGS().text(
                    query,
                    max_results=3
                )
            )
        )

        if not results:
            await event.reply("❌ No results found.")
            return

        best = results[0]

        title = best.get("title", "")
        body = best.get("body", "")

        if not body:
            body = "No summary available."

        answer = (
            f"🔎 {title}\n\n"
            f"{body}"
        )

        # Telegram message limit safety
        await event.reply(answer[:1000])

    except Exception as e:
        print("Search error:", e)
        await event.reply("❌ Search failed.")
