"""Debug why 'показания' doesn't find the indications section."""

from knowledge import reload_knowledge, _extract_words, STOPWORDS

items, tfidf = reload_knowledge("knowledge_base.json")

query = "Какие показания для стелек?"
query_words = set(_extract_words(query))
query_words -= STOPWORDS
print(f"Query words (stemmed, without stopwords): {query_words}")

for name, data in tfidf.items():
    score = sum(data['tfidf'].get(w, 0) for w in query_words)
    # Check if "показан" is in the tfidf index
    has_pokazan = "показан" in data['tfidf']
    if score > 0 or has_pokazan:
        print(f"  {data['title']:40s} score={score:.4f}  has_показан={has_pokazan}")
