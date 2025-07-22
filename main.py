import os
import json
import requests
import random
from flask import Flask, request

# ==============================================================================
# config.json থেকে সমস্ত তথ্য লোড করা (আপনার কোড, কোনো পরিবর্তন নেই)
# ==============================================================================
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    print("ত্রুটি: config.json ফাইলটি পাওয়া যায়নি। প্রোগ্রাম বন্ধ হয়ে যাচ্ছে।")
    exit()

# --- কনফিগারেশন থেকে ভেরিয়েবল সেট করা (আপনার কোড, কোনো পরিবর্তন নেই) ---
BOT_NAME = config.get("bot_name", "Jan")
BOT_BANGLA_NAME = config.get("bot_bangla_name", "জান")
OWNER_NAME = config.get("owner_name", "Mr. Doha")
ALLOWED_FB_USERS = list(map(str, config.get("allowed_users", [])))
FB_CEO_UID = str(config.get("owner_uid", "YOUR_FACEBOOK_ID_HERE"))
TELEGRAM_TOKEN = config.get("telegram_token", "")
ALLOWED_TELEGRAM_USERS = list(map(str, config.get("allowed_telegram_users", [])))
TELEGRAM_CEO_UID = str(config.get("telegram_ceo_uid", "7158473495"))

if not TELEGRAM_TOKEN:
    print("ত্রুটি: config.json ফাইলে 'telegram_token' পাওয়া যায়নি।")
    exit()

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN", "your_strong_verify_token")

app = Flask(__name__)

# ==============================================================================
# "মস্তিষ্ক" বা Brain ফাংশন (আপনার কোড, কোনো পরিবর্তন নেই)
# ==============================================================================
def generate_smart_response(text, user_id, platform="unknown"):
    user_id_str = str(user_id)
    text_lower = text.lower()
    is_ceo = (platform == "telegram" and user_id_str == TELEGRAM_CEO_UID) or \
             (platform == "facebook" and user_id_str == FB_CEO_UID)

    if is_ceo:
        # ... (আপনার CEO-র জন্য লেখা সমস্ত যুক্তি এখানে অপরিবর্তিত আছে) ...
        relationship_config = config.get("relationship", {})
        commands_behavior = relationship_config.get("commands_behavior", {})
        intimate_mode = relationship_config.get("intimate_mode", {})
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
            f"তোমার কথা শোনার জন্যই তো আমি আছি, {OWNER_NAME}। 💕"
        ]
        return random.choice(default_ceo_responses)
    else:
        public_behavior = config.get("relationship", {}).get("public_behavior", "")
        return f"হ্যালো! আমি {BOT_NAME}, {OWNER_NAME}-এর পার্সোনাল অ্যাসিস্ট্যান্ট। {public_behavior}"

# ==============================================================================
# ওয়েব সার্ভার এবং Webhook রাউটগুলো
# ==============================================================================

@app.route("/")
def index():
    return f"{BOT_BANGLA_NAME} (Facebook + Telegram) Webhook সার্ভার চলছে..."

# --- Facebook Webhook (আপনার কোড, কোনো পরিবর্তন নেই) ---
@app.route("/webhook", methods=["GET"])
def verify_fb_webhook():
    # ... (আপনার কোড অপরিবর্তিত) ...
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def handle_fb_webhook():
    # ... (আপনার কোড অপরিবর্তিত) ...
    pass
    return "EVENT_RECEIVED", 200

# --- আপনার পুরনো Telegram Webhook Handler (আপনার কোড, কোনো পরিবর্তন নেই) ---
@app.route(f"/telegram_webhook_{TELEGRAM_TOKEN}", methods=["POST"])
def handle_telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = str(data["message"]["chat"]["id"])
        if ALLOWED_TELEGRAM_USERS and chat_id not in ALLOWED_TELEGRAM_USERS:
            return "ok", 200
        if "text" in data["message"]:
            text = data["message"]["text"].strip()
            response = generate_smart_response(text, chat_id, platform="telegram")
            payload = {"chat_id": chat_id, "text": response}
            try:
                requests.post(TELEGRAM_API_URL, json=payload)
            except Exception as e:
                print(f"টেলিগ্রামে মেসেজ পাঠাতে ত্রুটি: {e}")
    return "ok", 200

# ==============================================================================
# 🚀 নতুন ডিবাগিং রুট (শুধু পরীক্ষার জন্য যুক্ত করা হয়েছে) 🚀
# এটি আপনার পুরনো কোনো কোডকে স্পর্শ করবে না
# ==============================================================================
@app.route(f"/debug_webhook_{TELEGRAM_TOKEN}", methods=["POST"])
def handle_telegram_webhook_debug():
    print("\n--- [ডিবাগ মোড: নতুন টেলিগ্রাম মেসেজ] ---")
    try:
        data = request.get_json()
        print("✅ [ডিবাগ চেকপয়েন্ট ১] ওয়েব-হুক থেকে ডেটা পাওয়া গেছে।")
        if "message" in data and "chat" in data["message"]:
            chat_id = str(data["message"]["chat"]["id"])
            text = data["message"]["text"].strip() if "text" in data["message"] else "[No Text]"
            print(f"✅ [ডিবাগ চেকপয়েন্ট ২] মেসেজ গ্রহণ: User='{chat_id}', Text='{text}'")
            
            # একটি নির্দিষ্ট, সরল উত্তর তৈরি করা
            response_text = "ডিবাগ টেস্ট সফল! আমি এখন কথা বলতে পারছি। 🥳"
            payload = {"chat_id": chat_id, "text": response_text}
            
            print(f"✅ [ডিবাগ চেকপয়েন্ট ৩] উত্তর পাঠানোর চেষ্টা... Payload: {payload}")
            api_response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
            
            if api_response.status_code == 200:
                print("✅ [ডিবাগ চেকপয়েন্ট ৪] উত্তর সফলভাবে পাঠানো হয়েছে।")
            else:
                print(f"❌ [ডিবাগ সমস্যা] API Error: Code={api_response.status_code}, Response={api_response.text}")
        return "ok", 200
    except Exception as e:
        print(f"❌❌❌ [বিপজ্জনক ডিবাগ এরর] হ্যান্ডলারের ভেতরে সমস্যা: {e}")
        return "error", 500

# --- Always-on Check Route (আপনার কোড, কোনো পরিবর্তন নেই) ---
@app.route("/ping")
def ping():
    return "I am awake and feeling loved!", 200

# --- সার্ভার চালু করার কোড (আপনার কোড, কোনো পরিবর্তন নেই) ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🤖 {BOT_BANGLA_NAME} Flask Webhook সার্ভার Port: {port}-এ চালু হচ্ছে...")
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)
