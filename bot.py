"""ORTOS Telegram Bot — aiogram implementation."""

import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from openai import OpenAI
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
KB_PATH = os.getenv('KB_PATH', 'knowledge_base.json')

from knowledge import reload_knowledge, search
kb_items, kb_tfidf = reload_knowledge(KB_PATH)


async def get_grok_response(question: str, context_items) -> str:
    system = (
        "Ты — помощник салона ортопедических стелек ORTOS. "
        "Отвечай только на русском языке. "
        "Если вопрос не связан с ортопедическими стельками, вежливо скажи, что можешь помочь только с этим."
    )
    
    context = "\n\n".join(f"[{item.title}]\n{item.content}" for item in context_items)
    
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        http_client=httpx.Client(proxy=None),
    )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Вопрос: {question}\n\nИнформация:\n{context}\n\nОтвет:"},
        ],
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content

async def handle_start(message: Message):
    welcome = (
        "Здравствуйте! Я — бот салона ортопедических стелек ORTOS. "
        "Спросите что-нибудь о наших стельках, ценах, доставке, записи на консультацию!"
    )
    await message.answer(welcome)


GREETINGS = {'привет', 'здравствуйте', 'здравствуй', 'добрый день', 'доброе утро', 'добрый вечер', 'хай', 'hi', 'hello', 'приветствую', 'салют'}

async def handle_message(message: Message):
    text = message.text.strip().lower()
    if text in GREETINGS or any(text.startswith(g) for g in GREETINGS if ' ' in g):
        await handle_start(message)
        return
    results = search(message.text, top_k=2, items=kb_items, tfidf=kb_tfidf)
    if not results:
        response = await get_grok_response(message.text, [])
        await message.answer(response)
        return
    response = await get_grok_response(message.text, results)
    await message.answer(response)


def start_bot(bot_token: str):
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.message.register(handle_start, Command('start'))
    dp.message.register(handle_message)
    dp.run_polling(bot)
