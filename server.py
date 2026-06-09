"""Entry point for ORTOS Telegram Bot on Render."""

import os, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
PORT = int(os.getenv('PORT', '8080'))

if not TELEGRAM_TOKEN:
    print("ERROR: TELEGRAM_TOKEN not set in .env")
    exit(1)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args):
        pass


def run_bot():
    from bot import start_bot
    start_bot(TELEGRAM_TOKEN)


if __name__ == '__main__':
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()

    server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
    print(f"Health server listening on port {PORT}")
    server.serve_forever()
