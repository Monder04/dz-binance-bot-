import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    try:
        with open("token.txt", "r", encoding="utf-8") as f:
            TOKEN = f.read().strip()
    except:
        TOKEN = None

REF_CODE = "945179068"

web_app = Flask(__name__)
@web_app.route('/')
def home():
    return f"Bot running! Ref: {REF_CODE} - OK"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

TRADERS = [
    {"id": "101", "name": "CryptoDZ_Spot", "roi": "+34.2%", "win": "89%", "followers": "1.2K", "risk": "منخفض"},
    {"id": "102", "name": "BNB_Scalper", "roi": "+28.7%", "win": "84%", "followers": "890", "risk": "متوسط"},
    {"id": "103", "name": "Halal_Trader", "roi": "+22.5%", "win": "91%", "followers": "2.1K", "risk": "منخفض جدا"},
    {"id": "104", "name": "Spot_Master", "roi": "+41.1%", "win": "82%", "followers": "650", "risk": "متوسط"},
    {"id": "105", "name": "Algeria_Whale", "roi": "+19.8%", "win": "95%", "followers": "3.4K", "risk": "منخفض"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ref = context.args[0] if context.args else "بدون"
    text = f"""
🚀 مرحبا بيك في بوت نسخ التداول الفوري SPOT 🇩🇿

✅ بدون فيوتشر - بدون رافعة - بدون تصفية
✅ نسخ آمن 100% فوري فقط

كودك: {REF_CODE}
دخل بيه: {ref}

الأوامر:
/rank - أفضل 5 متداولين
/trader 101 - تفاصيل متداول
/sub 101 - اشتراك
/help - مساعدة

رابطك: https://www.binance.com/referral/mine?ref={REF_CODE}
"""
    keyboard = [[InlineKeyboardButton("🚀 ابدأ النسخ الآن", url=f"https://www.binance.com/referral/mine?ref={REF_CODE}")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def rank_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🏆 أفضل متداولين SPOT هذا الأسبوع:\n\n"
    for t in TRADERS:
        msg += f"{t['id']} - {t['name']}\n📈 ROI: {t['roi']} | ✅ {t['win']} | 👥 {t['followers']}\n /trader {t['id']} | /sub {t['id']}\n\n"
    msg += f"\n🔗 رابط النسخ:\nhttps://www.binance.com/referral/mine?ref={REF_CODE}"
    keyboard = [[InlineKeyboardButton("🚀 ابدأ النسخ", url=f"https://www.binance.com/referral/mine?ref={REF_CODE}")]]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

async def trader_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("اكتب: /trader 101")
        return
    tid = context.args[0]
    t = next((x for x in TRADERS if x['id']==tid), None)
    if not t:
        await update.message.reply_text("❌ غير موجود. /rank")
        return
    msg = f"👤 {t['name']}\nROI: {t['roi']}\nنجاح: {t['win']}\nمتابعين: {t['followers']}\nمخاطرة: {t['risk']}\n\nرابط النسخ: https://www.binance.com/referral/mine?ref={REF_CODE}"
    await update.message.reply_text(msg)

async def sub_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✅ اشتركت في {context.args[0] if context.args else ''} - راح نبعثلك التنبيهات!")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"كودك: {REF_CODE} - /rank - /trader 101")

if __name__ == "__main__":
    if not TOKEN:
        print("TOKEN not found! Set env TOKEN")
        exit(1)
    print(f"Bot starting ref {REF_CODE}")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rank", rank_cmd))
    app.add_handler(CommandHandler("trader", trader_cmd))
    app.add_handler(CommandHandler("sub", sub_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.run_polling()
