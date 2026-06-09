"""Test search with new KB sections."""

from knowledge import reload_knowledge, search

items, tfidf = reload_knowledge("knowledge_base.json")
print(f"Loaded {len(items)} sections\n")

test_questions = [
    "У вас есть компрессионные чулки?",
    "Какие классы компрессии бывают?",
    "Нужен корсет для поясницы",
    "Есть ортез на голеностоп?",
    "Ортопедические подушки",
    "Как выбрать подушку для сна?",
    "Можно вернуть обувь?",
    "Какая гарантия на стельки?",
    "Как забронировать товар?",
    "Есть карта лояльности?",
    "Ортопедическая обувь в Минске",
]

for q in test_questions:
    results = search(q, top_k=2, items=items, tfidf=tfidf)
    titles = [r.title for r in results] if results else ["—"]
    print(f"  {q:45s} -> {', '.join(titles)}")
