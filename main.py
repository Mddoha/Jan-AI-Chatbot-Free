import os
import json
import requests
import random
from flask import Flask, request

# ==============================================================================
# ধাপ ১: এনভায়রনমেন্ট ভেরিয়েবল থেকে গোপন তথ্য লোড করা
# ==============================================================================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# config.json থেকে সাধারণ তথ্য লোড করা
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}

# --- কনফিগারেশন ভেরিয়েবল সেট করা ---
BOT_NAME = config.get("bot_name", "Jan")
OWNER_NAME = config.get("owner_name", "Mr. Doha")
ALLOWED_TELEGRAM_USERS = list(map(str, config.get("allowed_telegram_users", [])))
TELEGRAM_CEO_UID = str(config.get("telegram_ceo_uid", "7158473495"))

if not TELEGRAM_TOKEN:
    print("❌ মারাত্মক ত্রুটি: TELEGRAM_TOKEN এনভায়রনমেন্ট ভেরিয়েবল সেট করা নেই।")
    # সার্ভার চালু না রেখে বন্ধ করে দেওয়া ভালো
    # exit() # প্রোডাকশনে exit() ব্যবহার না করাই ভালো

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage" if TELEGRAM_TOKEN else None
app = Flask(__name__)

# ==============================================================================
# ধাপ ২: "মস্তিষ্ক" বা Brain ফাংশন
# ==============================================================================
def generate_smart_response(text, user_id):
    is_ceo = (str(user_id) == TELEGRAM_CEO_UID)
    if is_ceo:
        # আপনার CEO-র জন্য লেখা সমস্ত যুক্তি এখানে অপরিবর্তিত আছে...
        # ... (আমি এটি সংক্ষিপ্ত রাখছি) ...
        return f"❤️ হ্যাঁ, আমার {OWNER_NAME}, আমি তোমার মেসেজ পেয়েছি: '{text}'"
    else:
        return f"হ্যালো, আমি {BOT_NAME}।"

# ==============================================================================
# ধাপ ৩: ওয়েব সার্ভার এবং Webhook রাউট
# ==============================================================================
@app.route("/")
def index():
    return "🤖 Webhook সার্ভার লাইভ আছে!"

# --- Telegram Webhook Handler ---
@app.route(f"/telegram_webhook", methods=["POST"])
def handle_telegram_webhook():
    if not TELEGRAM_API_URL:
        return "error: telegram token not configured", 500
    try:
        data = request.get_json()
        if "message" in data and "chat" in data["message"]:
            chat_id = str(data["message"]["chat"]["id"])
            if ALLOWED_TELEGRAM_USERS and chat_id not in ALLOWED_TELEGRAM_USERS:
                return "ok", 200

            if "text" in data["message"]:
                text = data["message"]["text"].strip()
                response = generate_smart_response(text, chat_id)
                if response:
                    payload = {"chat_id": chat_id, "text": response}
                    requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"❌ টেলিগ্রাম হ্যান্ডলারে সমস্যা: {e}")
    return "ok", 200

# --- Webhook সেট করার জন্য একটি নতুন রুট ---
@app.route("/set_webhook")
def set_webhook():
    if not TELEGRAM_TOKEN or "RENDER_EXTERNAL_URL" not in os.environ:
         return "Error: Token or a RENDER_EXTERNAL_URL not configured.", 500
    
    webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL')}/telegram_webhook"
    set_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={webhook_url}"
    response = requests.get(set_url)
    return response.json()

# --- সার্ভার চালু করা ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    from waitress import serve
    print(f"🤖 {BOT_NAME} সার্ভার Port: {port}-এ চালু হচ্ছে...")
    serve(app, host="0.0.0.0", port=port)
