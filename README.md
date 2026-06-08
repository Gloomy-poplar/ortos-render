# ORTOS Telegram Bot v2

AI assistant for answering customer questions about ORTOS orthopedic insoles.

Uses vector search over knowledge base + Grok 3 API.

## Setup

1. Copy `.env` and fill in `TELEGRAM_TOKEN`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python server.py`

## Knowledge Base

Edit `knowledge_base.json` to update bot knowledge.

## Deploy to fly.io

See `fly.toml` and `Dockerfile`.
