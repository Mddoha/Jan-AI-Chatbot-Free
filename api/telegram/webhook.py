# ✅ File: api/telegram/webhook.py
from flask import Request, jsonify

def handler(request: Request):
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("📥 Webhook Hit:", data)

            # এখানে future-এ তুমি AI process, command, UID check ইত্যাদি add করতে পারো
            message = data.get('message', {})
            text = message.get('text', '')
            user = message.get('from', {}).get('first_name', 'User')

            print(f"👉 Message from {user}: {text}")

            return jsonify({'status': 'received'}), 200

        except Exception as e:
            print("❌ Error:", e)
            return jsonify({'error': str(e)}), 400

    return jsonify({'message': 'Invalid Method'}), 405
