import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from bot.config import BOT_TOKEN, PASSWORD
from storage.database import (
    init_db,
    authorize_user,
    is_authorized
)
waiting_for_password = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if is_authorized(user_id):
        await update.message.reply_text(
            "✅ You're already authenticated."
        )
        return

    waiting_for_password.add(user_id)

    await update.message.reply_text(
        "🔒 Enter your password:"
    )


async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in waiting_for_password:
        return

    if update.message.text == PASSWORD:

        waiting_for_password.remove(user_id)
        authorize_user(user_id)

        await update.message.reply_text(
            "✅ Login successful."
        )

    else:

        await update.message.reply_text(
            "❌ Wrong password."
        )

init_db()
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        password
    )
)

print("Private bot running...")

app.run_polling()
