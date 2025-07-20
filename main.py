import json
from utils.facebook_api import listen_messages, send_message
from utils.commands import handle_command
from utils.emotion_handler import detect_emotion
from utils.generator import generate_content

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

BOT_NAME = config["bot_name"]
OWNER_NAME = config["owner_name"]
PREFIX = config["prefix"]
ALLOWED_USERS = config["allowed_users"]
EMOTION_MODE = config["emotion_mode"]

print(f"🤖 {BOT_NAME} started and listening...")

def process_message(msg):
    sender = msg["sender_id"]
    text = msg["text"]

    if str(sender) not in ALLOWED_USERS:
        return

    if text.startswith(PREFIX):
        command = text[len(PREFIX):].strip()
        response = handle_command(command)
    else:
        emotion = detect_emotion(text) if EMOTION_MODE else None
        response = generate_content(text, emotion)

    send_message(sender, response)

listen_messages(callback=process_message)
