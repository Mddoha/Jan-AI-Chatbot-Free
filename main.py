import os
import json
import requests
from flask import Flask, request
from utils.facebook_api import send_message as send_facebook_message
from utils.commands import handle_command
from utils.emotion_handler import detect_emotion
from utils.generator import generate_content

app = Flask(__name__)

# config.json থেকে তথ্য লোড করা
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

BOT_NAME = config["bot_name"]
BOT_BANGLA_NAME = config.get("bot_bangla_name", "জান")
OWNER_NAME = config["owner_name"]
PREFIX = config["prefix"]
ALLOWED_USERS = list(map(str, config["allowed_users"]))
RELATIONSHIP = config.get("relationship", {})
COMMANDS_BEHAVIOR = RELATIONSHIP.get("commands_behavior", {})
EMOTION_MODE = config.get("emotion_mode", False)
CEO_UID = str(RELATIONSHIP.get("ceo_uid", "100015569688497"))
TELEGRAM_TOKEN = config.get("telegram_token", "")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# এখানে VERIFY_TOKEN সংজ্ঞায়িত করলাম
VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN", "my_verify_token_1234")

@app.route("/")
def index():
    return f"{BOT_BANGLA_NAME} (Facebook + Telegram Flask Webhook) চলছে..."

# ✅ Facebook Webhook Verification (GET method)
@app.route("/webhook", methods=["GET"])
def verify_fb():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Verification failed", 403

# ✅ Facebook Message Handling (POST method)
@app.route("/webhook", methods=["POST"])
def webhook_fb():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                if "message" in messaging_event:
                    message_text = messaging_event["message"].get("text", "").strip()
                    if not message_text:
                        continue

                    sender_str = str(sender_id)
                    if sender_str not in ALLOWED_USERS:
                        print(f"❌ অনুমতি নেই: {sender_str}")
                        continue

                    response = process_message(message_text, sender_str)
                    send_facebook_message(sender_str, response)
        return "EVENT_RECEIVED", 200
    return "404 Not Found", 404

# ✅ Telegram Webhook Handler
@app.route("/telegram_webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = str(data["message"]["chat"]["id"])
        text = data["message"].get("text", "").strip()
        if not text:
            return "no text", 200

        response = process_message(text, chat_id)
        payload = {
            "chat_id": chat_id,
            "text": response
        }
        requests.post(TELEGRAM_API_URL, json=payload)

    return "ok", 200

# ✅ Unified Message Handler
def process_message(text, user_id):
    response = None

    if text.startswith(PREFIX):
        command = text[len(PREFIX):].strip()
        try:
            response = handle_command(command, user_id)
        except TypeError:
            response = handle_command(command)
    else:
        if user_id == CEO_UID:
            matched = False
            if "ভালোবাস" in text:
                response = f"🥰 জান সবসময় হানিকে ভালোবাসে, {OWNER_NAME}! ❤️"
                matched = True
            elif "কোথায়" in text:
                response = f"আমি তো সবসময় তোমার মনের ভিতরেই আছি, হানি 🥹"
                matched = True

            if not matched:
                for trigger in COMMANDS_BEHAVIOR.get("intimate_response_trigger", []):
                    if trigger in text:
                        response = generate_content(f"[INTIMATE_MODE_ON] {text}", emotion="love")
                        matched = True
                        break

            if not matched:
                emotion = detect_emotion(text) if EMOTION_MODE else None
                response = generate_content(text, emotion)

            if not response:
                response = f"❤️ হানি {OWNER_NAME}, জান এখানে।"
        else:
            emotion = detect_emotion(text) if EMOTION_MODE else None
            response = generate_content(text, emotion)

            if not response:
                response = f"হ্যালো, আমি {BOT_NAME}। কীভাবে সাহায্য করতে পারি?"

    return response

# ✅ Always-on Check Route (combined both pings)
@app.route("/ping")
def ping():
    return "I am awake!", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"{BOT_BANGLA_NAME} Flask Webhook সার্ভার চালু হচ্ছে Port: {port} ...")
    app.run(host="0.0.0.0", port=port)
