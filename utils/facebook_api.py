import time

# Dummy/mock version (You must replace with actual API handling if using real FB automation)
def listen_messages(callback):
    print("📩 Listening to messages (Simulation Mode)...")
    while True:
        # Simulated message for testing purpose
        test_msg = {
            "sender_id": "1000XXXXXXXXXXX",
            "text": input("User says: ")
        }
        callback(test_msg)
        time.sleep(1)

def send_message(receiver_id, message):
    print(f"\n🧠 Bot reply to {receiver_id}: {message}\n")
