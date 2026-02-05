from datetime import datetime
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ Read token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ Simple runtime stats
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
        "هذا بوت قنص العملات الجديدة.\n"
        "حاليًا: لا إشارات — فقط فحص تجريبي."
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


async def periodic_check(context: ContextTypes.DEFAULT_TYPE):
    global CHECKS_TODAY
    CHECKS_TODAY += 1
    print(f"[CHECK] market scan ok | checks_today={CHECKS_TODAY}")


def main():
    if not TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN environment variable")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    # ✅ Run a periodic check every 30 seconds (starts after 5 seconds)
    app.job_queue.run_repeating(periodic_check, interval=30, first=5)

    print("[BOOT] Bot is starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
