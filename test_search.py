"""Test knowledge base search directly."""

from knowledge import reload_knowledge

items, tfidf = reload_knowledge("knowledge_base.json")
print(f"Loaded {len(items)} sections\n")

test_questions = [
    "Сколько стоят стельки",
    "Какие адреса в Минске",
    "Как делают стельки",
    "Срок изготовления",
    "Как записаться",
    "Плоскостопие",
    "Доставка курьером",
    "Скидка на две пары",
]

for q in test_questions:
    from knowledge import search
    results = search(q, top_k=2, items=items, tfidf=tfidf)
    titles = [r.title for r in results] if results else ["—"]
    print(f"  {q:30s} -> {', '.join(titles)}")
