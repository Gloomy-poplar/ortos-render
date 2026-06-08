"""Test full pipeline: search + Groq response."""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from knowledge import reload_knowledge, search
from bot import get_grok_response

items, tfidf = reload_knowledge("knowledge_base.json")

test_questions = [
    "Сколько стоят стельки?",
    "Какие адреса в Минске?",
    "Как делают стельки?",
    "Срок изготовления?",
    "Как записаться?",
    "Помогают при плоскостопии?",
    "Доставка курьером?",
    "Есть скидка на две пары?",
    "Как оплатить?",
    "Какие показания для стелек?",
]


async def run_tests():
    for q in test_questions:
        print(f"\n{'='*60}")
        print(f"ВОПРОС: {q}")
        print(f"{'='*60}")
        results = search(q, top_k=2, items=items, tfidf=tfidf)
        if not results:
            print("  → Нет информации в базе")
            continue
        print(f"  Найдено разделов: {[r.title for r in results]}")
        response = await get_grok_response(q, results)
        print(f"  ОТВЕТ: {response.strip()}")


asyncio.run(run_tests())
