import os
import asyncio
import requests
from bot.config import BOT_TOKEN
UPLOAD_FOLDER = "downloads"

upload_running = False

def upload_to_bot(file_path):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    with open(file_path, "rb") as f:

        r = requests.post(
            url,
            data={
                "chat_id": 8379433717
            },
            files={
                "document": f
            }
        )

    return r.ok
async def handle_upload(event):
    global upload_running

    # Only your own messages
    if not event.out:
        return

    if not event.raw_text:
        return

    if event.raw_text.strip().lower() != ".upload":
        return

    if upload_running:
        await event.reply("⚠️ Upload already running.")
        return

    if not os.path.exists(UPLOAD_FOLDER):
        await event.reply("📂 downloads folder not found.")
        return

    files = []

    for root, _, filenames in os.walk(UPLOAD_FOLDER):
        for name in filenames:
            files.append(os.path.join(root, name))

    if not files:
        await event.reply("📂 Nothing to upload.")
        return

    upload_running = True

    uploaded = 0
    skipped = 0
    failed = 0

    status = await event.reply(
        f"📤 Starting upload...\n"
        f"Total files: {len(files)}"
    )

    try:

        for index, file_path in enumerate(files, start=1):

            # Skip & delete voice notes
            if file_path.lower().endswith(".ogg"):

                try:
                    os.remove(file_path)
                    skipped += 1
                except Exception as e:
                    print(e)

                await status.edit(
                    f"📤 Progress: {index}/{len(files)}\n"
                    f"✅ Uploaded: {uploaded}\n"
                    f"🗑 Voices deleted: {skipped}\n"
                    f"❌ Failed: {failed}"
                )

                continue

            try:

                if upload_to_bot(file_path):
                
                    os.remove(file_path)
                    uploaded += 1
                
                else:
                
                    failed += 1

            except Exception as e:

                failed += 1
                print(e)

            await status.edit(
                f"📤 Progress: {index}/{len(files)}\n"
                f"✅ Uploaded: {uploaded}\n"
                f"🗑 Voices deleted: {skipped}\n"
                f"❌ Failed: {failed}"
            )

            await asyncio.sleep(1)

    finally:

        upload_running = False

    await status.edit(
        "✅ Upload Finished!\n\n"
        f"📤 Uploaded: {uploaded}\n"
        f"🗑 Voices deleted: {skipped}\n"
        f"❌ Failed: {failed}"
    )
