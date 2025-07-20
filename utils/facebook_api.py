import requests import time from config import config

RELATIONSHIP = config.get("relationship", {}) BOT_NAME = config.get("bot_name", "Jan") OWNER_NAME = config.get("owner_name", "Mr Doha") CEO_ID = RELATIONSHIP.get("ceo_uid", "100015569688497")  # Default fallback

token_info = config.get("access", {}) ACCESS_TOKEN = token_info.get("token") TOKEN_TYPE = token_info.get("type", "page")

def get_channel_type(): if TOKEN_TYPE == "page": return "Facebook Page" elif TOKEN_TYPE == "user": return "Messenger ID" elif TOKEN_TYPE == "group": return "Group Messenger" else: return "Unknown"

def send_facebook_message(recipient_id, message_text): if not ACCESS_TOKEN: return "❌ Access token missing."

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

----------------------------

Simulated listener (for test/dev mode)

----------------------------

def listen_messages(callback): print("📩 Listening to messages (Simulation Mode)...") while True: user_input = input("User says: ") if user_input.strip().lower() == "exit": break

test_msg = {
        "sender_id": input("Sender ID (default=CEO): ") or CEO_ID,
        "text": user_input
    }
    callback(test_msg)
    time.sleep(0.5)

----------------------------

Smart send wrapper

----------------------------

def send_message(receiver_id, message): print(f"🧠 Bot reply to {receiver_id}: {message}") response = send_facebook_message(receiver_id, message) print(response)

