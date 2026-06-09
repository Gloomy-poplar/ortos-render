"""Analyze dialog CSV — extract ALL client questions."""

import csv
from collections import Counter

with open('all_dialogs.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Всего диалогов: {len(rows)}")

all_questions = []
topics = Counter()

for r in rows:
    client_name = r['client_name']
    text = r['full_text']
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(':', 1)
        if len(parts) != 2:
            continue
        speaker = parts[0].strip()
        msg = parts[1].strip()
        if speaker == client_name and 10 <= len(msg) <= 500:
            all_questions.append(msg)

print(f"Всего сообщений клиентов: {len(all_questions)}")

# Show sample
print("\n--- Примеры первых 20 вопросов ---")
for q in all_questions[:20]:
    print(f"  {q}")

# Find most common words (potential topics)
words = []
for q in all_questions:
    for w in q.lower().split():
        if len(w) > 4:
            words.append(w)
print(f"\n--- Самые частые слова (топ-30) ---")
for word, count in Counter(words).most_common(30):
    print(f"  {word:30s} {count}")
