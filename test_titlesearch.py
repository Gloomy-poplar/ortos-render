"""Check if title boost fixes the показания search."""

from knowledge import reload_knowledge, search

items, tfidf = reload_knowledge("knowledge_base.json")
results = search("Какие показания для стелек?", top_k=3, items=items, tfidf=tfidf)
print(f"Found {len(results)} sections:")
for r in results:
    print(f"  - {r.title}")
