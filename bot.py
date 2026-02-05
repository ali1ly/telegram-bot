import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("ali-snipe-bot")

# -------------------------
# Token (اقرأ أكثر من اسم لتجنب الأخطاء)
# -------------------------
TOKEN = (
    os.getenv("BOT_TOKEN")
    or os.getenv("TELEGRAM_BOT_TOKEN")
    or os.getenv("TELEGRAM_TOKEN")
)

# -------------------------
# Simple in-memory state (لاحقًا نربطه بملف/DB)
# -------------------------
MODE_BY_USER = {}  # user_id -> "MANUAL" / "SEMI" / "AUTO"


def get_mode(user_id: int) -> str:
    return MODE_BY_USER.get(user_id, "MANUAL")


def set_mode(user_id: int, mode: str) -> None:
    MODE_BY_USER[user_id] = mode


# -------------------------
# Commands
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else 0
    mode = get_mode(user_id)
    await update.message.reply_text(
        "✅ البوت شغّال\n"
        f"🎛 الوضع الحالي: {mode}\n\n"
        "اكتب:\n"
        "/status لمعرفة الحالة\n"
        "/mode_manual للوضع اليدوي\n"
        "/mode_semi للوضع نصف تلقائي\n"
        "/mode_auto للوضع التلقائي"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else 0
    mode = get_mode(user_id)
    await update.message.reply_text(
        "📡 الحالة: Online\n"
        f"🎛 الوضع: {mode}\n"
        "🧪 هذا MVP للتأكد أن Railway + Telegram شغالين."
    )


async def mode_manual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else 0
    set_mode(user_id, "MANUAL")
    await update.message.reply_text("✅ تم التغيير: الوضع اليدوي (MANUAL)")


async def mode_semi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else 0
    set_mode(user_id, "SEMI")
    await update.message.reply_text("✅ تم التغيير: الوضع نصف تلقائي (SEMI)")


async def mode_auto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else 0
    set_mode(user_id, "AUTO")
    await update.message.reply_text("✅ تم التغيير: الوضع التلقائي (AUTO)")


def main() -> None:
    if not TOKEN:
        raise RuntimeError(
            "Missing bot token. Set BOT_TOKEN (or TELEGRAM_BOT_TOKEN) in Railway Variables."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("mode_manual", mode_manual))
    app.add_handler(CommandHandler("mode_semi", mode_semi))
    app.add_handler(CommandHandler("mode_auto", mode_auto))

    logger.info("Bot starting polling...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

