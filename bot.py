import os
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

STARTED_AT = datetime.now()
CHECKS_TODAY = 0
ALERTS_TODAY = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        "🧠 Ali Snipe Bot\n\n"
        "الحالة: 🟢 يعمل\n"
        "الوضع: Manual\n\n"
        f"مرحبًا {user.first_name} 👋\n"
        "هذا بوت قنص العملات الجديدة\n"
        "لا إشارات الآن."
    )
    await update.message.reply_text(text)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uptime = datetime.now() - STARTED_AT
    msg = (
        "📊 الحالة\n\n"
        "🟢 البوت يعمل\n"
        f"⏱️ Uptime: {str(uptime).split('.')[0]}\n"
        f"🔎 فحوصات اليوم: {CHECKS_TODAY}\n"
        f"🔔 إشارات اليوم: {ALERTS_TODAY}\n"
        "🧭 الوضع: Manual\n"
    )
    await update.message.reply_text(msg)


async def heartbeat(context: ContextTypes.DEFAULT_TYPE):
    global CHECKS_TODAY
    CHECKS_TODAY += 1


def main():
    if not TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN env var")

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    # Heartbeat every 30 seconds
    app.job_queue.run_repeating(heartbeat, interval=30, first=5)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
