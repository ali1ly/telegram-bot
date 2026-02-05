import os
import asyncio
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
