import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# =====================
# Logging
# =====================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# =====================
# Environment
# =====================
TOKEN = os.getenv("BOT_TOKEN")

# =====================
# Commands
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 Ali Snipe Bot\n\n"
        "الحالة: 🟢 يعمل\n"
        "الوضع: MANUAL\n\n"
        "البوت شغّال بدون أخطاء."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت Online ويعمل بشكل طبيعي.")

# =====================
# Main
# =====================
def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    logger.info("Bot starting polling...")
    app.run_polling(drop_pending_updates=True)

# =====================
# Entry
# =====================
if __name__ == "__main__":
    main()
