import os
import json
import requests
import random
from flask import Flask, request

# ==============================================================================
# config.json থেকে সমস্ত তথ্য লোড করা (এখানে কোনো পরিবর্তন নেই)
# ==============================================================================
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    print("ত্রুটি: config.json ফাইলটি পাওয়া যায়নি। প্রোগ্রাম বন্ধ হয়ে যাচ্ছে।")
    exit()

# --- কনফিগারেশন থেকে ভেরিয়েবল সেট করা (এখানে কোনো পরিবর্তন নেই) ---
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
# "মস্তিষ্ক" বা Brain ফাংশন (এখানে কোনো পরিবর্তন নেই)
# ==============================================================================
def generate_smart_response(text, user_id, platform="unknown"):
    user_id_str = str(user_id)
    text_lower = text.lower()
    is_ceo = (platform == "telegram" and user_id_str == TELEGRAM_CEO_UID) or \
             (platform == "facebook" and user_id_str == FB_CEO_UID)

    if is_ceo:
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
# ওয়েব সার্ভার এবং Webhook রাউটগুলো (এখানে শুধুমাত্র টেলিগ্রাম হ্যান্ডলারটি উন্নত করা হয়েছে)
# ==============================================================================

@app.route("/")
def index():
    return f"{BOT_BANGLA_NAME} (Facebook + Telegram) Webhook সার্ভার চলছে..."

# --- Facebook Webhook (এখানে কোনো পরিবর্তন নেই) ---
@app.route("/webhook", methods=["GET"])
def verify_fb_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ ফেসবুক ওয়েব-হুক সফলভাবে ভেরিফাই হয়েছে।")
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def handle_fb_webhook():
    data = request.get_json()
    if data.get("object") == "page":
        # ... (আপনার ফেসবুকের বাকি কোড এখানে থাকবে, কোনো পরিবর্তন নেই) ...
        pass
    return "EVENT_RECEIVED", 200

# ==============================================================================
# নতুন এবং উন্নত Telegram Webhook Handler (ডিবাগিং ভার্সন)
# এটি আপনার পুরনো টেলিগ্রাম হ্যান্ডলারকে প্রতিস্থাপন করবে
# ==============================================================================
@app.route(f"/telegram_webhook_{TELEGRAM_TOKEN}", methods=["POST"])
def handle_telegram_webhook_debug():
    print("\n--- [নতুন টেলিগ্রাম মেসেজ] ---")
    try:
        data = request.get_json()
        print("✅ [চেকপয়েন্ট ১] ওয়েব-হুক থেকে ডেটা পাওয়া গেছে।")

        if "message" in data and "chat" in data["message"] and "id" in data["message"]["chat"]:
            chat_id = str(data["message"]["chat"]["id"])
            if "text" in data["message"]:
                text = data["message"]["text"].strip()
                print(f"✅ [চেকপয়েন্ট ২] মেসেজ গ্রহণ করা হয়েছে: User ID='{chat_id}', Text='{text}'")
                
                if ALLOWED_TELEGRAM_USERS and chat_id not in ALLOWED_TELEGRAM_USERS:
                    print(f"❌ [সমস্যা] অনুমতি নেই: User ID '{chat_id}' allowed_telegram_users লিস্টে নেই।")
                    return "ok", 200

                print("✅ [চেকপয়েন্ট ৩] 'generate_smart_response' ফাংশন কল করা হচ্ছে...")
                response = generate_smart_response(text, chat_id, platform="telegram")
                print(f"✅ [চেকপয়েন্ট ৪] 'generate_smart_response' থেকে উত্তর পাওয়া গেছে: '{response}'")
                
                if response:
                    payload = {"chat_id": chat_id, "text": response}
                    print(f"✅ [চেকপয়েন্ট ৫] টেলিগ্রামকে উত্তর পাঠানোর চেষ্টা করা হচ্ছে... Payload: {payload}")
                    api_response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
                    
                    if api_response.status_code == 200:
                        print("✅ [চেকপয়েন্ট ৬] টেলিগ্রামকে উত্তর সফলভাবে পাঠানো হয়েছে।")
                    else:
                        print(f"❌ [সমস্যা] টেলিগ্রাম API থেকে এরর: Status Code={api_response.status_code}, Response={api_response.text}")
                else:
                    print("⚠️ [সতর্কবার্তা] 'generate_smart_response' কোনো উত্তর তৈরি করেনি (None বা খালি স্ট্রিং)।")
        return "ok", 200
    except Exception as e:
        print(f"❌❌❌ [বিপজ্জনক এরর] হ্যান্ডলারের ভেতরে একটি অপ্রত্যাশিত এরর ঘটেছে: {e}")
        return "error", 500

# --- Always-on Check Route (এখানে কোনো পরিবর্তন নেই) ---
@app.route("/ping")
def ping():
    return "I am awake and feeling loved!", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🤖 {BOT_BANGLA_NAME} Flask Webhook সার্ভার Port: {port}-এ চালু হচ্ছে...")
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)
