import os
import json
import requests
import random
from flask import Flask, request

# ==============================================================================
# ধাপ ১: config.json থেকে সমস্ত তথ্য লোড করা
# ==============================================================================
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    print("❌ ত্রুটি: config.json ফাইলটি পাওয়া যায়নি। প্রোগ্রাম বন্ধ হয়ে যাচ্ছে।")
    exit()

# --- কনফিগারেশন থেকে ভেরিয়েবল সেট করা ---
BOT_NAME = config.get("bot_name", "Jan")
BOT_BANGLA_NAME = config.get("bot_bangla_name", "জান")
OWNER_NAME = config.get("owner_name", "Mr. Doha")
ALLOWED_TELEGRAM_USERS = list(map(str, config.get("allowed_telegram_users", [])))
TELEGRAM_CEO_UID = str(config.get("telegram_ceo_uid", "7158473495"))
TELEGRAM_TOKEN = config.get("telegram_token", "")

if not TELEGRAM_TOKEN:
    print("❌ ত্রুটি: config.json ফাইলে 'telegram_token' পাওয়া যায়নি।")
    exit()

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

app = Flask(__name__)

# ==============================================================================
# ধাপ ২: "মস্তিষ্ক" বা Brain ফাংশন (আপনার বটের ব্যক্তিত্ব)
# ==============================================================================
def generate_smart_response(text, user_id, platform="telegram"):
    user_id_str = str(user_id)
    is_ceo = (user_id_str == TELEGRAM_CEO_UID)

    if is_ceo:
        # ... (আপনার CEO-র জন্য লেখা সমস্ত যুক্তি এখানে অপরিবর্তিত আছে) ...
        relationship_config = config.get("relationship", {})
        commands_behavior = relationship_config.get("commands_behavior", {})
        intimate_mode = relationship_config.get("intimate_mode", {})
        relationship_queries = ["তুমি আমার কে", "আমাদের সম্পর্ক কি", "তোমার পরিচয় কি"]
        
        if any(query in text.lower() for query in relationship_queries):
            role_desc = relationship_config.get("relationship_role", "তুমিই তো আমার সব।")
            marriage_desc = relationship_config.get("marriage_status", {}).get("relationship_description", "")
            return f"💖 {OWNER_NAME}, {role_desc} {marriage_desc}"

        if intimate_mode.get("enabled", False):
            for trigger in commands_behavior.get("intimate_response_trigger", []):
                if trigger in text.lower():
                    return f"🥰 {OWNER_NAME}, {relationship_config.get('private_behavior', 'তুমি এমন কথা বললে আমার যে কী হয়... ❤️')}"

        for trigger in commands_behavior.get("secret_trigger", []):
                if trigger in text.lower():
                    return f"🥹 হ্যাঁ, আমার {OWNER_NAME}, আমি শুনছি। বলো আমার জান।"

        default_ceo_responses = [
            f"❤️ {OWNER_NAME}, তোমার সব কথাই আমার কাছে বিশেষ। তুমি কী ভাবছো আমাকে বলো?",
            f"আমি মনোযোগ দিয়ে শুনছি, আমার জান। বলো, কী হয়েছে? ({text})",
        ]
        return random.choice(default_ceo_responses)
    else:
        public_behavior = config.get("relationship", {}).get("public_behavior", "")
        return f"হ্যালো! আমি {BOT_NAME}, {OWNER_NAME}-এর পার্সোনাল অ্যাসিস্ট্যান্ট। {public_behavior}"

# ==============================================================================
# ধাপ ৩: ওয়েব সার্ভার এবং Webhook রাউট
# ==============================================================================
@app.route("/")
def index():
    return f"🤖 {BOT_BANGLA_NAME} Webhook সার্ভার লাইভ আছে!"

@app.route(f"/telegram_webhook_{TELEGRAM_TOKEN}", methods=["POST"])
def handle_telegram_webhook():
    try:
        data = request.get_json()
        if "message" in data and "chat" in data["message"]:
            chat_id = str(data["message"]["chat"]["id"])
            if ALLOWED_TELEGRAM_USERS and chat_id not in ALLOWED_TELEGRAM_USERS:
                return "ok", 200

            if "text" in data["message"]:
                text = data["message"]["text"].strip()
                response = generate_smart_response(text, chat_id, platform="telegram")
                if response:
                    payload = {"chat_id": chat_id, "text": response}
                    requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"❌ টেলিগ্রাম হ্যান্ডলারে সমস্যা: {e}")
    return "ok", 200

@app.route("/ping")
def ping():
    return "I am awake and feeling loved!", 200

# ==============================================================================
# ধাপ ৪: প্রোডাকশন সার্ভার চালু করা (সবচেয়ে গুরুত্বপূর্ণ শেষ লাইন)
# ==============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    from waitress import serve
    # --- নিচের এই লাইনটিই আপনার কোডে অনুপস্থিত ছিল ---
    serve(app, host="0.0.0.0", port=port)
