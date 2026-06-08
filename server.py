"""Entry point for ORTOS Telegram Bot."""

import os
from dotenv import load_dotenv
from bot import start_bot

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    print("ERROR: TELEGRAM_TOKEN not set in .env")
    exit(1)

if __name__ == '__main__':
    start_bot(TELEGRAM_TOKEN)
