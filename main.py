import json
from utils.facebook_api import listen_messages, send_message
from utils.commands import handle_command
from utils.emotion_handler import detect_emotion
from utils.generator import generate_content

# কনফিগারেশন লোড
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

# Relationship config
RELATIONSHIP = config.get("relationship", {})
INTIMATE_MODE = RELATIONSHIP.get("intimate_mode", {})
PRIVATE_BEHAVIOR = RELATIONSHIP.get("private_behavior", "")
PUBLIC_BEHAVIOR = RELATIONSHIP.get("public_behavior", "")
COMMANDS_BEHAVIOR = RELATIONSHIP.get("commands_behavior", {})
EMOTIONS = RELATIONSHIP.get("emotions", {})
CEO_UID = str(RELATIONSHIP.get("ceo_uid", "100015569688497"))

print(f"🤖 {BOT_BANGLA_NAME} ({BOT_NAME}) চালু হয়েছে... মালিক: {OWNER_NAME}")

# মেসেজ প্রসেস করার ফাংশন
def process_message(msg):
    sender = str(msg["sender_id"])
    text = msg["text"].strip()

    # অনুমোদিত ইউজার নয়? তাহলে কিছুই করবে না
    if sender not in ALLOWED_USERS:
        print(f"❌ অনুমতি নেই: {sender}")
        return

    # যদি কমান্ড হয়, তাহলে হ্যান্ডেল করবে
    if text.startswith(PREFIX):
        command = text[len(PREFIX):].strip()
        response = handle_command(command, sender=sender)
    else:
        # যদি CEO হয়, রোমান্টিক ইন্টিমেট রেসপন্স দিবে
        if sender == CEO_UID:
            matched = False
            for trigger in COMMANDS_BEHAVIOR.get("intimate_response_trigger", []):
                if trigger in text:
                    response = generate_content(f"[INTIMATE_MODE_ON] {text}", emotion="love")
                    matched = True
                    break
            if not matched:
                emotion = detect_emotion(text) if EMOTION_MODE else None
                response = generate_content(text, emotion)

            # অতিরিক্ত প্রেমভরা পরিচয়
            if not response:
                response = f"❤️ হানি {OWNER_NAME}, জান এখানে।"
        else:
            # অন্য কেউ হলে নরমাল ইমোশন/এআই রেসপন্স
            emotion = detect_emotion(text) if EMOTION_MODE else None
            response = generate_content(text, emotion)

            if not response:
                response = f"হ্যালো, আমি {BOT_NAME}। কীভাবে সাহায্য করতে পারি?"

    # রেসপন্স পাঠাবে
    send_message(sender, response)

# বট চালু করে রাখবে
listen_messages(callback=process_message)
