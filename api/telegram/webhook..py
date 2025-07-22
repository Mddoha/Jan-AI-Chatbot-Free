# path: api/telegram/webhook.py
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        print("Webhook Hit:", post_data.decode())

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
