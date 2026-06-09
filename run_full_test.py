"""Full test of all KB sections with questions and Groq responses."""

import asyncio
import json
from knowledge import reload_knowledge, search
from bot import get_grok_response

items, tfidf = reload_knowledge("knowledge_base.json")

test_questions = [
    # Стельки
    "Сколько стоят стельки?",
    "Какая скидка при покупке двух пар стелек?",
    "Как делают стельки?",
    "Срок изготовления стелек?",
    "Какие показания для стелек?",
    "Помогают при плоскостопии?",
    "Кому нужны ортопедические стельки?",
    "Из каких материалов делают стельки?",

    # Компрессионный трикотаж
    "У вас есть компрессионные чулки?",
    "Какие классы компрессии бывают?",
    "Чем отличаются 1 и 2 класс компрессии?",
    "Нужен рукав после мастэктомии",

    # Корсеты, бандажи, ортезы
    "Нужен корсет для поясницы",
    "Есть ортез на голеностоп?",
    "Какие бандажи для колена есть?",
    "Фиксатор для лучезапястного сустава",

    # Подушки
    "Ортопедические подушки",
    "Как выбрать подушку для сна?",

    # Обувь
    "Ортопедическая обувь в Минске",
    "Есть ортопедические сандалии?",

    # Адреса и запись
    "Какие адреса салонов в Минске?",
    "Как записаться на консультацию?",

    # Доставка
    "Доставка курьером?",
    "Сколько стоит доставка?",
    "Можно забрать самовывозом?",

    # Оплата
    "Как можно оплатить?",
    "Можно оплатить картой онлайн?",

    # Программа лояльности
    "Есть карта лояльности?",
    "Какая скидка после 5 покупок?",

    # Возврат и гарантия
    "Можно вернуть товар?",
    "Какая гарантия на стельки?",
    "Что нельзя вернуть?",

    # Бронирование
    "Как забронировать товар?",
    "На сколько дней бронь?",
]


async def run_tests():
    results = []
    for q in test_questions:
        result = search(q, top_k=2, items=items, tfidf=tfidf)
        sections = [r.title for r in result] if result else ["—"]
        if result:
            response = await get_grok_response(q, result)
        else:
            response = await get_grok_response(q, [])
        results.append({
            "question": q,
            "sections_found": sections,
            "answer": response.strip()
        })
        print(f"[{len(results)}/{len(test_questions)}] {q[:50]}")

    # Save results
    with open('test_results.md', 'w', encoding='utf-8') as f:
        f.write("# Результаты тестирования ORTOS бота\n\n")
        for r in results:
            f.write(f"## Вопрос: {r['question']}\n\n")
            f.write(f"**Найдено разделов:** {', '.join(r['sections_found'])}\n\n")
            f.write(f"**Ответ:**\n{r['answer']}\n\n---\n\n")

    # Print summary
    print(f"\n\n=== ИТОГИ ===")
    print(f"Всего вопросов: {len(results)}")
    found = sum(1 for r in results if r['sections_found'] != ["—"])
    print(f"Найден контекст: {found}/{len(results)}")
    print(f"Результаты сохранены в test_results.md")

asyncio.run(run_tests())
