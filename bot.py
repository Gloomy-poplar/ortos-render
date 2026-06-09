"""ORTOS Telegram Bot — aiogram implementation."""

import os, re
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from openai import OpenAI
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
from knowledge import reload_knowledge, search
kb_items, kb_tfidf = reload_knowledge(['knowledge_base.json', 'knowledge_base_insoles.json'])

OPERATOR_TRIGGERS = [
    re.compile(r'отмен(ит|и|ю|я|иться|ять)', re.I),
    re.compile(r'(удал|отписк|откаж|отзов|отпиш)(ит|и|ю|я|ись)', re.I),
    re.compile(r'(продл|продлит|продление)', re.I),
    re.compile(r'(жалоб|претензи)', re.I),
]

def need_operator(text: str) -> bool:
    text_lower = text.lower()
    for pattern in OPERATOR_TRIGGERS:
        if pattern.search(text_lower):
            return True
    return False


async def get_grok_response(question: str, context_items) -> str:
    system = (
        "Ты — консультант салона ORTOS. Используй ТОЛЬКО переданную информацию. "
        "Не выдумывай цены, характеристики, сроки. "
        "Если в информации нет ответа — напиши: 'Уточните по телефону +375 (29) 145-03-03'. "
        "Никогда не добавляй 'Переход на оператор' в ответ."
    )
    
    context = "\n\n".join(f"[{item.title}]\n{item.content}" for item in context_items)
    
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        http_client=httpx.Client(proxy=None),
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Вопрос клиента: {question}\n\nДоступная информация из базы знаний ORTOS:\n{context}\n\nДай точный ответ на вопрос клиента, используя ТОЛЬКО информацию выше. Если в информации нет нужных данных — скажи что не знаешь."},
        ],
        temperature=0.1,
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
    text = message.text.strip()
    text_lower = text.lower()
    if text_lower in GREETINGS or any(text_lower.startswith(g) for g in GREETINGS if ' ' in g):
        await handle_start(message)
        return
    if need_operator(text):
        await message.answer("Переход на оператор")
        return
    results = search(text, top_k=2, items=kb_items, tfidf=kb_tfidf)
    if not results:
        response = await get_grok_response(text, [])
        await message.answer(response)
        return
    response = await get_grok_response(text, results)
    await message.answer(response)


def start_bot(bot_token: str):
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.message.register(handle_start, Command('start'))
    dp.message.register(handle_message)
    dp.run_polling(bot)
