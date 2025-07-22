import os
import requests
from flask import Flask, request

# --- শুধুমাত্র টোকেন সরাসরি এনভায়রনমেন্ট থেকে লোড করা হচ্ছে ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage" if TELEGRAM_TOKEN else None

app = Flask(__name__)

# --- একটিমাত্র ওয়েব-হুক রাউট ---
@app.route(f"/telegram_webhook", methods=["POST"])
def handle_telegram_webhook_final_test():
    if not TELEGRAM_API_URL:
        print("❌ মারাত্মক ত্রুটি: TELEGRAM_TOKEN পাওয়া যায়নি।")
        return "error: token not configured", 500
        
    try:
        data = request.get_json()
        print("✅ [চূড়ান্ত টেস্ট] ওয়েব-হুক থেকে ডেটা পাওয়া গেছে।")

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            print(f"✅ [চূড়ান্ত টেস্ট] চ্যাট আইডি পাওয়া গেছে: {chat_id}")

            response_text = "FINAL TEST SUCCESSFUL! আমি এখন উত্তর দিতে পারছি। ✅"
            payload = {"chat_id": chat_id, "text": response_text}
            
            print(f"✅ [চূড়ান্ত টেস্ট] উত্তর পাঠানোর চেষ্টা করা হচ্ছে: {payload}")
            requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
            print("✅ [চূড়ান্ত টেস্ট] উত্তর সফলভাবে পাঠানো হয়েছে।")

        return "ok", 200
        
    except Exception as e:
        print(f"❌❌❌ [চূড়ান্ত টেস্ট এরর] হ্যান্ডলারের ভেতরে অপ্রত্যাশিত সমস্যা: {e}")
        return "error", 500

# --- Webhook সেট করার রুট ---
@app.route("/set_webhook")
def set_webhook():
    if not TELEGRAM_TOKEN or "RENDER_EXTERNAL_URL" not in os.environ:
         return "Error: Token or a RENDER_EXTERNAL_URL not configured.", 500
    
    webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL')}/telegram_webhook"
    set_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={webhook_url}"
    response = requests.get(set_url)
    return response.json()

# --- সার্ভার চালু করার কোড ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    from waitress import serve
    print(f"🤖 [চূড়ান্ত টেস্ট মোড] সার্ভার Port: {port}-এ চালু হচ্ছে...")
    serve(app, host="0.0.0.0", port=port)
