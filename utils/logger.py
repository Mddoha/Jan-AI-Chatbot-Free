import json

with open("config.json", "r") as f:
    config = json.load(f)

CEO_UID = config.get("ceo_uid")

def log_error(module, error_text):
    print(f"[❌ ERROR in {module}] {error_text}")

def notify_admin(message):
    print(f"[🔔 Notify CEO ({CEO_UID})] {message}")
