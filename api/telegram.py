# ✅ File: api/telegram.py
from flask import Request, jsonify

def handler(request: Request):
    return jsonify({"message": "Telegram API OK ✅"}), 200
