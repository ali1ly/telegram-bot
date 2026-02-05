from datetime import datetime

STARTED_AT = datetime.now()
CHECKS_TODAY = 0
ALERTS_TODAY = 0

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uptime = datetime.now() - STARTED_AT
    msg = (
        "📊 الحالة\n\n"
        f"🟢 البوت يعمل\n"
        f"⏱️ Uptime: {str(uptime).split('.')[0]}\n"
        f"🔎 فحوصات اليوم: {CHECKS_TODAY}\n"
        f"🔔 إشارات اليوم: {ALERTS_TODAY}\n"
        f"🧭 الوضع: Manual\n"
    )
    await update.message.reply_text(msg)
