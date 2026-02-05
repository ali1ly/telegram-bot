import os
import logging
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ---------- Logging ----------
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("ali-snipe-bot")

# ---------- Config ----------
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Railway variable
DEFAULT_MODE = "MANUAL"  # MANUAL / SEMI / AUTO

# In-memory per-user state (simple MVP)
USER_MODE: dict[int, str] = {}


def get_mode(user_id: int) -> str:
    return USER_MODE.get(user_id, DEFAULT_MODE)


def set_mode(user_id: int, mode: str) -> None:
    USER_MODE[user_id] = mode


# ---------- Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    uid = user.id if user else 0
    mode = get_mode(uid)

    msg = (
        "✅ **Ali Snipe Bot شغّال**\n"
        f"🧭 الوضع الحالي: **{mode}**\n\n"
        "الأوامر:\n"
        "• /status — حالة البوت\n"
        "• /mode — تغيير الوضع\n"
        "• /setmode MANUAL|SEMI|AUTO — ضبط الوضع مباشرة\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    uid = user.id if user else 0
    mode = get_mode(uid)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    msg = (
        "📊 **Status**\n"
        f"🟢 البوت: **ONLINE**\n"
        f"🧭 وضعك: **{mode}**\n"
        f"⏱ الوقت: `{now}`\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    uid = user.id if user else 0
    current = get_mode(uid)

    msg = (
        "🧭 **الأوضاع**\n\n"
        f"الوضع الحالي: **{current}**\n\n"
        "غيّر وضعك هكذا:\n"
        "• `/setmode MANUAL`\n"
        "• `/setmode SEMI`\n"
        "• `/setmode AUTO`\n\n"
        "شرح سريع:\n"
        "MANUAL = إشعارات فقط\n"
        "SEMI   = إشعار + تأكيد منك\n"
        "AUTO   = تنفيذ تلقائي (لاحقًا)\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def setmode_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    uid = user.id if user else 0

    if not context.args:
        await update.message.reply_text("اكتب: /setmode MANUAL أو /setmode SEMI أو /setmode AUTO")
        return

    mode_value = context.args[0].strip().upper()
    if mode_value not in {"MANUAL", "SEMI", "AUTO"}:
        await update.message.reply_text("❌ وضع غير صحيح. اختر: MANUAL / SEMI / AUTO")
        return

    set_mode(uid, mode_value)
    await update.message.reply_text(f"✅ تم ضبط وضعك إلى: {mode_value}")


# ---------- Main ----------
def main() -> None:
    if not TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN env var")

    # Important: use Application.builder() (PTB v20+)
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("mode", mode))
    app.add_handler(CommandHandler("setmode", setmode_cmd))

    logger.info("Bot starting polling...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()



