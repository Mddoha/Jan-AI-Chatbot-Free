import json
import os
from utils.facebook_api import listen_messages, send_message
from utils.commands import handle_command
from utils.emotion_handler import detect_emotion
from utils.generator import generate_content

# 🔧 কনফিগারেশন লোড
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

BOT_NAME = config["bot_name"]
BOT_BANGLA_NAME = config.get("bot_bangla_name", "জান")
OWNER_NAME = config["owner_name"]
PREFIX = config["prefix"]
ALLOWED_USERS = list(map(str, config["allowed_users"]))
OWNER_UIDS = list(map(str, config.get("OWNER", [])))
OPERATOR_UIDS = list(map(str, config.get("OPERATOR", [])))
ADMIN_UIDS = list(map(str, config.get("ADMINBOT", [])))
CONTACT_INFO = config.get("contact", {})
EMOTION_MODE = config.get("emotion_mode", False)
LANG = config.get("language", "bn")

# ❤️ Relationship config
RELATIONSHIP = config.get("relationship", {})
INTIMATE_MODE = RELATIONSHIP.get("intimate_mode", {})
PRIVATE_BEHAVIOR = RELATIONSHIP.get("private_behavior", "")
PUBLIC_BEHAVIOR = RELATIONSHIP.get("public_behavior", "")
COMMANDS_BEHAVIOR = RELATIONSHIP.get("commands_behavior", {})
EMOTIONS = RELATIONSHIP.get("emotions", {})
CEO_UID = str(RELATIONSHIP.get("ceo_uid", "100015569688497"))

print(f"🤖 {BOT_BANGLA_NAME} ({BOT_NAME}) চালু হয়েছে... মালিক: {OWNER_NAME}")

# 📩 মেসেজ প্রসেস করার ফাংশন
def process_message(msg):
    sender = str(msg["sender_id"])
    text = msg["text"].strip()

    if sender not in ALLOWED_USERS:
        print(f"❌ অনুমতি নেই: {sender}")
        return

    if text.startswith(PREFIX):
        command = text[len(PREFIX):].strip()
        try:
            response = handle_command(command, sender)
        except TypeError:
            response = handle_command(command)
    else:
        if sender == CEO_UID:
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

    send_message(sender, response)

# ✅ বট চালু রাখবে বা সিমুলেটেড চালাবে
if __name__ == "__main__":
    simulated_input = os.getenv("SIMULATED_INPUT")
    simulated_uid = os.getenv("SIMULATED_UID")

    if simulated_input and simulated_uid:
        print("🧪 সিমুলেটেড ইনপুট চালু হয়েছে...")
        process_message({
            "sender_id": simulated_uid,
            "text": simulated_input
        })
    else:
        listen_messages(callback=process_message)
