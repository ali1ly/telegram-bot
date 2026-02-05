from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import logging

# تفعيل اللوج
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = (
        "🧠 Ali Snipe Bot\n\n"
        "الحالة: 🟢 يعمل\n"
        "الوضع: Manual\n\n"
        f"مرحبًا {user.first_name} 👋\n"
        "هذا بوت قنص العملات الجديدة.\n"
        "لا توجد إشارات حالياً."
    )
    await update.message.reply_text(msg)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📊 حالة البوت\n\n"
        "🟢 البوت يعمل\n"
        "⚙️ الوضع: Manual\n"
        "🚫 Auto Sniping: غير مفعل\n"
    )
    await update.message.reply_text(msg)

def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    app.run_polling()

if __name__ == "__main__":
    main()

