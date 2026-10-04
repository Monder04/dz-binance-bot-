import os, logging, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = os.getenv("TOKEN")
REF = "945179068"
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return f"Bot running! Ref {REF} - {'OK' if TOKEN else 'NO TOKEN'} - Live"
@web_app.route('/health')
def health():
    return "OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🚀 مرحبا بيك SPOT 🇩🇿\nكودك: {REF}\n/rank - الترتيب\nhttps://www.binance.com/referral/mine?ref={REF}")

async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🏆 أفضل 5 SPOT:\n101 CryptoDZ +34%\n102 BNB_Scalper +28%\n103 Halal +22%\n\nرابطك: https://www.binance.com/referral/mine?ref={REF}")

def run_bot():
    if not TOKEN:
        logger.error("NO TOKEN")
        return
    logger.info(f"Bot starting {REF}")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rank", rank))
    app.run_polling(drop_pending_updates=True)

def start_thread():
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()
    logger.info("Bot thread launched")
    return t

start_thread()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)
else:
    logger.info("Loaded for gunicorn")
