import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)

@app.route('/')
def home():
    return "البوت يعمل! المرجع: 945179068 - موافق - مباشر"

@app.route('/setwebhook')
def set_webhook():
    if not TOKEN or not WEBHOOK_URL:
        return "حط TOKEN و WEBHOOK_URL في Environment أولا"
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": f"{WEBHOOK_URL}/webhook"}
    r = requests.post(url, json=data)
    return f"Webhook set: {r.text}"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            reply = "مرحبا! 🎉\nرابط الإحالة تاعك:\nhttps://t.me/dz_binance_copy_bot?start=945179068\n\nالمرجع: 945179068"
        else:
            reply = f"استقبلت: {text}"
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": chat_id, "text": reply})
    return "ok"

if __name__ == '__main__':
    app.run()
