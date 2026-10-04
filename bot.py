import os
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import asyncio

TOKEN = os.environ.get("BOT_TOKEN", "8874475066:AAG6DOUIbPgNbLxELf9zY4jI1ryVJ60Mf-4") # حط التوكن في Environment تاع Render
REF_CODE = "945179068"
REF_LINK = f"https://www.binance.com/en/copy-trading?ref={REF_CODE}"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")  # مثلا https://dz-binance-bot.onrender.com/webhook

logging.basicConfig(level=logging.INFO)

TOP_TRADERS = [
    {"name": "CryptoKing", "pnl": "+182%", "win": "78%", "followers": "12.5K"},
    {"name": "SOL_Master", "pnl": "+124%", "win": "82%", "followers": "8.2K"},
    {"name": "BNB_Hunter", "pnl": "+98%", "win": "75%", "followers": "5.9K"},
]

# --- دوال البوت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 أفضل المتداولين /rank", callback_data="rank")],
        [InlineKeyboardButton("🔗 رابط التسجيل بكودي", url=REF_LINK)],
    ]
    text = f"أهلا بيك! 🇩🇿\nالبوت يعمل! المرجع: {REF_CODE} - موافق - مباشر\n\n/rank - أفضل المتداولين\n/sub - كيفاش تنسخ"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def rank_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🔥 أفضل متداولي اليوم:\n\n"
    for i, t in enumerate(TOP_TRADERS, 1):
        msg += f"{i}. {t['name']} - {t['pnl']} ✅ {t['win']}\n"
    msg += f"\nسجل هنا: {REF_LINK}\nكود: {REF_CODE}"
    await update.message.reply_text(msg)

async def trader_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"اكتب /rank باش تشوف القائمة\nرابط التسجيل: {REF_LINK}")

async def sub_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"سجل من هنا باش تنسخ:\n{REF_LINK}\nكود الإحالة: {REF_CODE}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "rank":
        await rank_command(update, context)

# إعداد التطبيق
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("rank", rank_command))
application.add_handler(CommandHandler("trader", trader_command))
application.add_handler(CommandHandler("sub", sub_command))
application.add_handler(CallbackQueryHandler(button_handler))

# Flask
app = Flask(__name__)

@app.route("/")
def index():
    return f"البوت يعمل! المرجع: {REF_CODE} - موافق - مباشر"

@app.route("/webhook", methods=["POST"])
def webhook():
    # استقبال رسائل تلغرام
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

@app.route("/setwebhook")
def set_webhook():
    # هادي تزورها مرة وحدة باش تربط تلغرام بـ Render
    if not WEBHOOK_URL:
        return "حط WEBHOOK_URL في Environment أولا"
    async def _set():
        await application.bot.set_webhook(url=WEBHOOK_URL)
    asyncio.run(_set())
    return f"تم ربط الويب هوك: {WEBHOOK_URL}"

if __name__ == "__main__":
    # للتجربة المحلية فقط
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
