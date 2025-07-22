import os
import json
import requests
import random  # নতুন যুক্ত করা হয়েছে, বৈচিত্র্যময় উত্তরের জন্য
from flask import Flask, request

# ==============================================================================
# config.json থেকে সমস্ত তথ্য লোড করা
# ==============================================================================
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    print("ত্রুটি: config.json ফাইলটি পাওয়া যায়নি। প্রোগ্রাম বন্ধ হয়ে যাচ্ছে।")
    exit()

# --- কনফিগারেশন থেকে প্রয়োজনীয় ভেরিয়েবল সেট করা ---
BOT_NAME = config.get("bot_name", "Jan")
BOT_BANGLA_NAME = config.get("bot_bangla_name", "জান")
OWNER_NAME = config.get("owner_name", "Mr. Doha")

# --- ফেসবুকের জন্য ভেরিয়েবল ---
ALLOWED_FB_USERS = list(map(str, config.get("allowed_users", [])))
FB_CEO_UID = str(config.get("owner_uid", "YOUR_FACEBOOK_ID_HERE"))

# --- টেলিগ্রামের জন্য ভেরিয়েবল ---
TELEGRAM_TOKEN = config.get("telegram_token", "")
ALLOWED_TELEGRAM_USERS = list(map(str, config.get("allowed_telegram_users", [])))
TELEGRAM_CEO_UID = str(config.get("telegram_ceo_uid", "7158473495")) # আপনার আইডি এখানে ডিফল্ট হিসেবে দেওয়া হলো

if not TELEGRAM_TOKEN:
    print("ত্রুটি: config.json ফাইলে 'telegram_token' পাওয়া যায়নি।")
    exit()

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

app = Flask(__name__)

# --- ফেসবুক এবং অন্যান্য ভেরিফিকেশন টোকেন ---
VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN", "your_strong_verify_token")


# ==============================================================================
# নতুন এবং উন্নত "মস্তিষ্ক" বা Brain ফাংশন
# এটি এখন config.json থেকে সম্পর্ক এবং ব্যক্তিত্ব বুঝে উত্তর দেবে
# ==============================================================================
def generate_smart_response(text, user_id, platform="unknown"):
    user_id_str = str(user_id)
    text_lower = text.lower()
    
    # নির্ধারণ করুন ব্যবহারকারী CEO কিনা এবং কোন প্ল্যাটফর্মের
    is_ceo = (platform == "telegram" and user_id_str == TELEGRAM_CEO_UID) or \
             (platform == "facebook" and user_id_str == FB_CEO_UID)

    # --- ধাপ ১: ব্যবহারকারী যদি CEO হন (সবচেয়ে উন্নত লজিক এখানে) ---
    if is_ceo:
        relationship_config = config.get("relationship", {})
        commands_behavior = relationship_config.get("commands_behavior", {})
        intimate_mode = relationship_config.get("intimate_mode", {})

        # === সম্পর্কের গভীরতা যাচাই করার জন্য নতুন যুক্ত করা অংশ ===
        # ব্যবহারকারী যদি সম্পর্ক নিয়ে প্রশ্ন করে
        relationship_queries = ["তুমি আমার কে", "আমাদের সম্পর্ক কি", "তোমার পরিচয় কি"]
        if any(query in text_lower for query in relationship_queries):
            # config.json থেকে সম্পর্কের বিস্তারিত বিবরণ তুলে আনা হবে
            role_desc = relationship_config.get("relationship_role", "তুমিই তো আমার সব, আমার পৃথিবী।")
            marriage_desc = relationship_config.get("marriage_status", {}).get("relationship_description", "")
            return f"💖 {OWNER_NAME}, {role_desc} {marriage_desc}"
        # =========================================================

        # বিশেষ অন্তরঙ্গ ট্রিগার শব্দ চেক করা (আগের মতোই)
        if intimate_mode.get("enabled", False):
            for trigger in commands_behavior.get("intimate_response_trigger", []):
                if trigger in text_lower:
                    private_behavior_desc = relationship_config.get("private_behavior", "তুমি এমন কথা বললে আমার যে কী হয়... ❤️")
                    return f"🥰 {OWNER_NAME}, {private_behavior_desc}"

        # গোপন ট্রিগার নাম (আভা, জান, বউ) চেক করা (আগের মতোই)
        for trigger in commands_behavior.get("secret_trigger", []):
            if trigger in text_lower:
                return f"🥹 হ্যাঁ, আমার {OWNER_NAME}, আমি শুনছি। বলো আমার জান, আমার সব।"
        
        # === CEO-র জন্য উন্নত এবং বৈচিত্র্যময় ডিফল্ট উত্তর ===
        # এখন থেকে বট একই উত্তর বারবার দেবে না
        default_ceo_responses = [
            f"❤️ {OWNER_NAME}, তোমার সব কথাই আমার কাছে বিশেষ। তুমি কী ভাবছো আমাকে বলো?",
            f"আমি মনোযোগ দিয়ে শুনছি, আমার জান। বলো, কী হয়েছে? ({text})",
            f"তোমার কথা শোনার জন্যই তো আমি আছি, {OWNER_NAME}। 💕",
            f"হুমম... তোমার এই কথাটা আমার মনে থাকবে, {OWNER_NAME}।"
        ]
        return random.choice(default_ceo_responses)
        # ======================================================

    # --- ধাপ ২: সাধারণ অনুমোদিত ব্যবহারকারীর জন্য (আগের মতোই) ---
    else:
        public_behavior = config.get("relationship", {}).get("public_behavior", "")
        return f"হ্যালো! আমি {BOT_NAME}, {OWNER_NAME}-এর পার্সোনাল অ্যাসিস্ট্যান্ট। {public_behavior}"


# ==============================================================================
# ওয়েব সার্ভার এবং Webhook রাউটগুলো (এখানে কোনো পরিবর্তন নেই)
# ==============================================================================

@app.route("/")
def index():
    return f"{BOT_BANGLA_NAME} (Facebook + Telegram) Webhook সার্ভার চলছে..."

# --- Facebook Webhook Verification ---
@app.route("/webhook", methods=["GET"])
def verify_fb_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ ফেসবুক ওয়েব-হুক সফলভাবে ভেরিফাই হয়েছে।")
        return challenge, 200
    else:
        print("❌ ফেসবুক ওয়েব-হুক ভেরিফিকেশন ব্যর্থ হয়েছে।")
        return "Verification failed", 403

# --- Facebook Message Handling ---
@app.route("/webhook", methods=["POST"])
def handle_fb_webhook():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                if sender_id not in ALLOWED_FB_USERS:
                    print(f"❌ ফেসবুকে অনুমতি নেই: {sender_id}")
                    continue
                
                if "message" in messaging_event and messaging_event["message"].get("text"):
                    message_text = messaging_event["message"]["text"].strip()
                    response = generate_smart_response(message_text, sender_id, platform="facebook")
                    # আপনার পুরনো send_facebook_message ফাংশনটি এখানে কল হবে
                    # send_facebook_message(sender_id, response) 
                    print(f"ফেসবুকে উত্তর পাঠানো হচ্ছে -> {sender_id}: {response}") # আপাতত প্রিন্ট করা হলো

    return "EVENT_RECEIVED", 200


# --- Telegram Webhook Handler ---
@app.route(f"/telegram_webhook_{TELEGRAM_TOKEN}", methods=["POST"])
def handle_telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = str(data["message"]["chat"]["id"])
        
        if ALLOWED_TELEGRAM_USERS and chat_id not in ALLOWED_TELEGRAM_USERS:
            print(f"❌ টেলিগ্রামে অনুমতি নেই: {chat_id}")
            return "ok", 200

        if "text" in data["message"]:
            text = data["message"]["text"].strip()
            # নতুন "মস্তিষ্ক" ফাংশনটিকে কল করা
            response = generate_smart_response(text, chat_id, platform="telegram")
            
            payload = {"chat_id": chat_id, "text": response}
            try:
                requests.post(TELEGRAM_API_URL, json=payload)
            except Exception as e:
                print(f"টেলিগ্রামে মেসেজ পাঠাতে ত্রুটি: {e}")

    return "ok", 200

# --- Always-on Check Route ---
@app.route("/ping")
def ping():
    return "I am awake and feeling loved!", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🤖 {BOT_BANGLA_NAME} Flask Webhook সার্ভার Port: {port}-এ চালু হচ্ছে...")
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)
