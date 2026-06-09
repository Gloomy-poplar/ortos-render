"""Deep analysis of each product category."""

import csv
from collections import Counter

with open('all_dialogs.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

categories = {
    'компрессионный трикотаж': ['чулк', 'компрессионн', 'гольф', 'рукав', 'колготк'],
    'корсеты/бандажи/ортезы': ['корсет', 'бандаж', 'ортез', 'фиксатор', 'реклинатор', 'корректор'],
    'подушки': ['подушк'],
    'обувь': ['обув', 'туфл', 'ботинк', 'сапог', 'кроссовк', 'тапочк'],
    'размеры': ['размер', 'какой размер', 'подобрать размер'],
}

cat_questions = {cat: [] for cat in categories}

for r in rows:
    client_name = r['client_name']
    text = r['full_text']
    lines = text.split('\n')
    
    client_msgs = []
    for line in lines:
        line = line.strip()
        parts = line.split(':', 1)
        if len(parts) == 2 and parts[0].strip() == client_name:
            client_msgs.append(parts[1].strip())
    
    joined = ' '.join(m.lower() for m in client_msgs)
    
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw in joined:
                cat_questions[cat].extend(client_msgs)
                break

for cat, questions in cat_questions.items():
    print(f"\n{'='*60}")
    print(f"=== {cat.upper()} ({len(questions)} сообщений) ===")
    print(f"{'='*60}")
    # Show first 10 unique meaningful questions
    seen = set()
    count = 0
    for q in questions:
        if len(q) > 15 and q not in seen:
            print(f"  {q[:120]}")
            seen.add(q)
            count += 1
            if count >= 12:
                break
