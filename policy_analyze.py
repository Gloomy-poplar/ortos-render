"""Extract common uncategorized questions and policy questions."""

import csv
from collections import Counter

with open('all_dialogs.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Find questions about: warranty, returns, booking, loyalty, discounts, BADs
policy_questions = {
    'возврат': [],
    'гарантия': [],
    'скидка': [],
    'карта лояльности': [],
    'запись': [],
    'бронь': [],
}

for r in rows:
    client_name = r['client_name']
    text = r['full_text']
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        parts = line.split(':', 1)
        if len(parts) == 2 and parts[0].strip() == client_name:
            msg = parts[1].strip().lower()
            for topic, keywords in [('возврат', ['возврат', 'вернут']),
                                     ('гарантия', ['гаранти']),
                                     ('скидка', ['скидк', 'акци']),
                                     ('карта лояльности', ['лояльност', 'карта лояльности']),
                                     ('запись', ['записат', 'запись на']),
                                     ('бронь', ['бронь', 'бронирова', 'отложит'])]:
                for kw in keywords:
                    if kw in msg:
                        policy_questions[topic].append(parts[1].strip())
                        break

for topic, questions in policy_questions.items():
    if questions:
        print(f"\n=== {topic.upper()} ({len(questions)}) ===")
        for q in list(dict.fromkeys(questions))[:5]:
            print(f"  {q}")
