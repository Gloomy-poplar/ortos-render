"""Categorize client questions by product type."""

import csv
from collections import Counter

with open('all_dialogs.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

categories = {
    'стельки': ['стельк', 'стелек', 'ортопедические стельк'],
    'компрессионный трикотаж': ['чулк', 'компрессионн', 'гольф', 'рукав', 'колготк'],
    'корсеты/бандажи/ортезы': ['корсет', 'бандаж', 'ортез', 'фиксатор', 'реклинатор', 'корректор'],
    'подушки': ['подушк', 'подушечк'],
    'обувь': ['обув', 'туфл', 'ботинк', 'сапог', 'кроссовк', 'тапочк'],
    'массажеры/тренажеры': ['массажер', 'тренажер', 'коврик', 'мяч'],
    'доставка': ['доставк', 'курьер', 'почт'],
    'размеры/подбор': ['размер', 'подобрать', 'какой размер'],
}

category_counts = Counter()
uncategorized = []

for r in rows:
    client_name = r['client_name']
    text = r['full_text']
    lines = text.split('\n')
    
    # Get all client messages for this dialog
    client_msgs = []
    for line in lines:
        line = line.strip()
        parts = line.split(':', 1)
        if len(parts) == 2 and parts[0].strip() == client_name:
            client_msgs.append(parts[1].strip().lower())
    
    joined = ' '.join(client_msgs)
    
    found = False
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw in joined:
                category_counts[cat] += 1
                found = True
                break
        if found:
            break
    
    if not found and client_msgs:
        uncategorized.append(client_msgs[0][:100])

print("=== Категории вопросов из диалогов ===")
print(f"{'Категория':40s} {'Диалогов':>10s}")
print("-" * 52)
for cat, count in category_counts.most_common():
    print(f"{cat:40s} {count:>10d}")

print(f"\nВсего распределено: {sum(category_counts.values())} из {len(rows)}")
print(f"\n--- Примеры некатегоризированных (первые 20) ---")
for q in uncategorized[:20]:
    print(f"  {q}")
