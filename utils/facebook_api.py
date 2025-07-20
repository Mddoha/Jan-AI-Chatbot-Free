import requests
import time
import json
import os

# Load config from config.json
with open("config.json", "r") as f:
    config = json.load(f)

# Bot Details
RELATIONSHIP = config.get("relationship", {})
BOT_NAME = config.get("bot_name", "Jan")
OWNER_NAME = config.get("owner_name", "Mr Doha")
CEO_ID = RELATIONSHIP.get("ceo_uid", "100015569688497")  # Default fallback

# Access Token Management
token_info = config.get("access", {})
ACCESS_TOKEN = token_info.get("token") or config.get("page_access_token")  # fallback
TOKEN_TYPE = token_info.get("type", "page")

# ----------------------------
# Optional simple fallback message printer (dev/test)
# ----------------------------
def get_channel_type():
    if TOKEN_TYPE == "page":
        return "Facebook Page"
    elif TOKEN_TYPE == "user":
        return "Messenger ID"
    elif TOKEN_TYPE == "group":
        return "Group Messenger"
    else:
        return "Unknown"

# ----------------------------
# Real Messenger API sender
# ----------------------------
def send_facebook_message(recipient_id, message_text):
    if not ACCESS_TOKEN:
        return "❌ Access token missing."

    if TOKEN_TYPE == "page":
        url = f"https://graph.facebook.com/v18.0/me/messages"
    else:
        url = f"https://graph.facebook.com/v18.0/{recipient_id}/messages"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
        "messaging_type": "RESPONSE",
        "access_token": ACCESS_TOKEN
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return f"✅ মেসেজ পাঠানো হয়েছে: {get_channel_type()}"
        else:
            return f"❌ মেসেজ পাঠাতে সমস্যা হয়েছে: {response.text}"
    except Exception as e:
        return f"⚠️ ত্রুটি: {str(e)}"

# ----------------------------
# Simulated listener (for test/dev mode or GitHub Actions)
# ----------------------------
def listen_messages(callback):
    print("📩 Listening to messages (Simulation Mode)...")

    is_ci = os.getenv("CI", "false").lower() == "true"
    simulated_input = os.getenv("SIMULATED_INPUT", "হানি, তুমি কেমন?")
    simulated_uid = os.getenv("SIMULATED_UID", CEO_ID)

    if is_ci:
        # GitHub Actions or CI input mode
        test_msg = {
            "sender_id": simulated_uid,
            "text": simulated_input
        }
        print(f"🤖 Simulated: {simulated_uid} says → {simulated_input}")
        callback(test_msg)
    else:
        # Local test mode
        while True:
            try:
                user_input = input("User says: ")
                if user_input.strip().lower() == "exit":
                    break
                sender_id = input("Sender ID (default=CEO): ") or CEO_ID
                test_msg = {
                    "sender_id": sender_id,
                    "text": user_input
                }
                callback(test_msg)
                time.sleep(0.5)
            except EOFError:
                print("❌ ইনপুট বন্ধ হয়ে গেছে (Non-interactive environment?)")
                break

# ----------------------------
# Smart send wrapper
# ----------------------------
def send_message(receiver_id, message):
    print(f"🧠 Bot reply to {receiver_id}: {message}")
    response = send_facebook_message(receiver_id, message)
    print(response)

# ----------------------------
# Simple test method (prints only)
# ----------------------------
def send_dev_message(uid, message):
    print(f"[📨] Sending message to {uid}: {message}")
    # বাস্তবে এখানে API Call যাবে এই PAGE_ACCESS_TOKEN দিয়ে
