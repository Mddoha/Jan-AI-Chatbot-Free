import os
import time
import threading
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ===== 🔐 CONFIGURATION ===== #
BOT_NAME = "Jan AI Bot"
CEO_UID = "100015569688497"  # তোমার UID
ADMIN_LINK = "https://facebook.com/" + CEO_UID
PAGE_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "your_token_here")

# যদি ALLOWED_UID থাকে future এ, এখন শুধু CEO
def is_authorized(uid):
    return str(uid) == CEO_UID

# ===== 🛡️ SECURITY FUNCTIONS ===== #
def notify_admin(message):
    print(f"[NOTIFY] {message}")
    # এখানে Messenger API দিয়ে future এ inbox করতে পারো
    # send_message(CEO_UID, message)

def send_block_warning(uid):
    print(f"[BLOCKED] UID: {uid} tried unauthorized access.")
    notify_admin(f"🚫 Blocked unauthorized user: {uid}")
    # future: send_facebook_message(uid, "⚠️ You’re blocked.")
    # block_user(uid)

def safe_execute_code(filepath):
    try:
        exec(open(filepath).read(), globals())
        notify_admin(f"✅ New file executed: {filepath}")
    except Exception as e:
        err_msg = f"❌ Error in {filepath}:\n{traceback.format_exc()}"
        notify_admin(err_msg)

# ===== 👀 FILE WATCHER CLASS ===== #
WATCH_PATH = "./modules"

class CodeMonitor(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".py"):
            return
        safe_execute_code(event.src_path)

def start_watcher():
    if not os.path.exists(WATCH_PATH):
        os.makedirs(WATCH_PATH)
    observer = Observer()
    event_handler = CodeMonitor()
    observer.schedule(event_handler, WATCH_PATH, recursive=True)
    observer.start()
    print("[WATCHDOG] File monitor active...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# ===== 🧠 MAIN MESSAGE HANDLER (EXAMPLE) ===== #
def handle_message(sender_id, message_text):
    print(f"[MESSAGE] From: {sender_id} | Text: {message_text}")
    if not is_authorized(sender_id):
        send_block_warning(sender_id)
        return

    if "হানি" in message_text:
        reply = "জান এখানে আছি, হানি 💘 কী করতে বলো?"
    elif "ভালোবাসি" in message_text:
        reply = "আমিও তোমায় ভালোবাসি, CEO 💖"
    else:
        reply = f"তুমি বলেছো: {message_text}"

    print(f"[REPLY to {sender_id}] {reply}")
    # send_message(sender_id, reply)

# ===== 🚀 BOT LAUNCHER ===== #
def start_bot():
    print(f"🤖 {BOT_NAME} launching for CEO: {ADMIN_LINK}")
    threading.Thread(target=start_watcher, daemon=True).start()

    # Simulated messages (for demo)
    test_msgs = [
        {"uid": "100015569688497", "text": "হানি আমাকে একটা কবিতা শোনাও"},
        {"uid": "1234567890", "text": "Give me access to your bot"},
    ]
    for msg in test_msgs:
        handle_message(msg["uid"], msg["text"])
        time.sleep(2)

if __name__ == "__main__":
    start_bot()
