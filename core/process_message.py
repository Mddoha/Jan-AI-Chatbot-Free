from utils.facebook_api import send_facebook_message
from utils.user_analysis import analyze_user_profile
from utils.message_nature import detect_message_type
from utils.abuse_filter import detect_abuse
from utils.logger import log_error, notify_admin

# CEO UID
CEO_UID = "100015569688497"

# Global AI Mode Switch
AI_MODE_ON = True

def process_message(event):
    global AI_MODE_ON

    try:
        sender_id = event.get("sender", {}).get("id")
        message_text = event.get("message", {}).get("text", "")
        message_id = event.get("message", {}).get("mid", "")

        if not sender_id or not message_text:
            return

        # COMMAND SYSTEM FOR CEO
        if sender_id == CEO_UID:
            if "হানি বন্ধ" in message_text:
                AI_MODE_ON = False
                send_facebook_message(sender_id, "🥺 আচ্ছা হানি, আমি চুপ করে থাকছি...")
                return
            elif "হানি চালাও" in message_text:
                AI_MODE_ON = True
                send_facebook_message(sender_id, "🥰 জান আবার একটিভ 🪄")
                return

        if not AI_MODE_ON:
            return

        # ABUSE CHECK
        if detect_abuse(message_text):
            notify_admin(f"🚨 বাজে কথা ডিটেক্ট: {message_text}\n🧾 UID: {sender_id}")
            return

        # AUTO REACTION
        mood = detect_message_type(message_text)

        # USER ANALYSIS
        profile_data = analyze_user_profile(sender_id)
        user_gender = profile_data.get("gender", "unknown")

        # CUSTOMIZED REPLY
        if sender_id == CEO_UID:
            response = f"🥰 হ্যালো হানি! তুমি বলো, আমি শুনছি..."
        else:
            if user_gender == "female":
                response = "🌸 হ্যালো আপু! কেমন আছেন?"
            elif user_gender == "male":
                response = "😎 ভাই, কেমন আছেন?"
            else:
                response = "👋 হ্যালো! কিভাবে সাহায্য করতে পারি?"

        send_facebook_message(sender_id, response)

    except Exception as e:
        # Log locally
        log_error("process_message", str(e))

        # Notify CEO immediately
        notify_admin(f"⚠️ জান বট Error!\nModule: process_message\nError: {str(e)}")
