import os
import json
import requests
import random
from flask import Flask, request

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}

BOT_NAME = config.get("bot_name", "Jan")
OWNER_NAME = config.get("owner_name", "Mr. Doha")
ALLOWED_TELEGRAM_USERS = list(map(str, config.get("allowed_telegram_users", [])))
TELEGRAM_CEO_UID = str(config.get("telegram_ceo_uid", "7158473495"))

if not TELEGRAM_TOKEN:
    print("❌ মারাত্মক ত্রুটি: TELEGRAM_TOKEN এনভায়রনমেন্ট ভেরিয়েবল সেট করা নেই।")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage" if TELEGRAM_TOKEN else None
app = Flask(__name__)

def generate_smart_response(text, user_id):
    user_id_str = str(user_id)
    text_lower = text.lower()
    is_ceo = (user_id_str == TELEGRAM_CEO_UID)

    if is_ceo:
        relationship_config = config.get("relationship", {})
        commands_behavior = relationship_config.get("commands_behavior", {})
        intimate_mode = relationship_config.get("intimate_mode", {})

        greetings = ["hello", "hi", "salam", "assalamualaikum", "/start"]
        if any(greet in text_lower for greet in greetings):
            return f"💖 হ্যাঁ, আমার {OWNER_NAME}! আমি তোমার জন্যই অপেক্ষা করছিলাম। বলো, আমার জান।"

        relationship_queries = ["তুমি আমার কে", "আমাদের সম্পর্ক কি", "তোমার পরিচয় কি"]
        if any(query in text_lower for query in relationship_queries):
            role_desc = relationship_config.get("relationship_role", "তুমিই তো আমার সব।")
            marriage_desc = relationship_config.get("marriage_status", {}).get("relationship_description", "")
            return f"💖 {OWNER_NAME}, {role_desc} {marriage_desc}"
        
        if intimate_mode.get("enabled", False):
            for trigger in commands_behavior.get("intimate_response_trigger", []):
                if trigger in text_lower:
                    return f"🥰 {OWNER_NAME}, {relationship_config.get('private_behavior', 'তুমি এমন কথা বললে আমার যে কী হয়... ❤️')}"

        for trigger in commands_behavior.get("secret_trigger", []):
            if trigger in text_lower:
                return f"🥹 হ্যাঁ, আমার {OWNER_NAME}, আমি শুনছি। বলো আমার জান।"

        default_ceo_responses = [
            f"❤️ {OWNER_NAME}, তোমার সব কথাই আমার কাছে বিশেষ। তুমি কী ভাবছো আমাকে বলো?",
            f"আমি মনোযোগ দিয়ে শুনছি, আমার জান। বলো, কী হয়েছে? ({text})",
        ]
        return random.choice(default_ceo_responses)
        
    else:
        public_behavior = config.get("relationship", {}).get("public_behavior", "")
        return f"হ্যালো! আমি {BOT_NAME}, {OWNER_NAME}-এর পার্সোনাল অ্যাসিস্ট্যান্ট। {public_behavior}"

@app.route("/")
def index():
    return "🤖 Webhook সার্ভার লাইভ আছে!"

@app.route("/api/telegram", methods=["POST"])
def handle_telegram():
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

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    from waitress import serve
    print(f"🤖 {BOT_NAME} সার্ভার Port: {port}-এ চালু হচ্ছে...")
    serve(app, host="0.0.0.0", port=port)
