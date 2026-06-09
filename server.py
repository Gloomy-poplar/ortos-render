"""Entry point for ORTOS Telegram Bot on Render."""

import os, time, threading
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


def run_health_server():
    server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
    print(f"Health server listening on port {PORT}")
    server.serve_forever()


if __name__ == '__main__':
    t = threading.Thread(target=run_health_server, daemon=False)
    t.start()
    time.sleep(1)

    from bot import start_bot
    print("Starting Telegram bot...")
    start_bot(TELEGRAM_TOKEN)
