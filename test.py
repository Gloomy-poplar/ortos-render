import requests
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY")
if not key:
    print("ERROR: GROQ_API_KEY not set in .env")
    exit(1)

print(f"Testing with key: {key[:10]}...{key[-4:]}")

r = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",  # Правильный endpoint для Groq
    json={
        "model": "llama-3.1-8b-instant",  # Эта модель есть в Groq
        "messages": [{"role": "user", "content": "Привет, кто ты?"}],
        "max_tokens": 100,
    },
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    },
)

print(f"\nStatus: {r.status_code}")
print(f"Response: {r.text[:500]}")