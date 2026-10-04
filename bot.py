import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)

REF_LINK = "https://t.me/dz_binance_copy_bot?start=945179068"
REF_CODE = "945179068"

@app.route('/')
def home():
    return f"البوت يعمل! {REF_CODE}"

@app.route('/setwebhook')
def set_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": f"{WEBHOOK_URL}/webhook"}
    r = requests.post(url, json=data)
    return f"Webhook: {r.text}"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            reply = f"مرحبا! 🎉\nرابط الاحالة تاعك:\n{REF_LINK}\n\nالمرجع: {REF_CODE}\n\nالأوامر:\n/rank - ترتيبك\n/trader - المتداولين\n/sub - الاشتراك"
        elif text == "/rank":
            reply = f"🏆 ترتيبك الحالي\n\nالمرجع تاعك: {REF_CODE}\nرابطك: {REF_LINK}\n\nشارك الرابط باش تطلع في الترتيب!"
        elif text == "/trader":
            reply = "📈 قائمة المتداولين\n\nقريبا - سيتم اضافة المتداولين هنا"
        elif text == "/sub":
            reply = f"💎 الاشتراك\n\nاشترك عبر رابط الاحالة:\n{REF_LINK}\n\nالمرجع: {REF_CODE}"
        else:
            reply = f"استقبلت: {text}\n\nجرب /start"

        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                      json={"chat_id": chat_id, "text": reply})
    return "ok"

if __name__ == '__main__':
    app.run()
