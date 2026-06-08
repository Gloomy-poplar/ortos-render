"""Knowledge base module for ORTOS Telegram Bot.

Loads knowledge_base.json, indexes sections, and searches by keyword.
"""

import json
import re
from collections import Counter
from pydantic import BaseModel
from nltk.stem.snowball import SnowballStemmer


stemmer = SnowballStemmer('russian')


class KnowledgeItem(BaseModel):
    id: str
    title: str
    content: str


def _extract_words(text: str) -> list[str]:
    words = re.findall(r'[а-яё]{3,}', text.lower())
    return [stemmer.stem(w) for w in words if len(w) >= 3]


STOPWORDS = {
    'это', 'который', 'которая', 'которое', 'которые', 'которого',
    'которой', 'которому', 'которым', 'которых', 'который',
    'в', 'на', 'с', 'по', 'к', 'из', 'для', 'у', 'о',
    'не', 'но', 'и', 'или', 'также', 'только', 'еще',
    'при', 'как', 'чем', 'что', 'такой', 'такая', 'такое',
    'где', 'зачем', 'когда', 'почему', 'кто', 'что',
    'от', 'до', 'за', 'без', 'между', 'через',
}


def _load_keywords(path: str) -> dict[str, dict[str, float]]:
    """Load and compute TF-IDF for all sections."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_docs = []
    for name, sec in data['sections'].items():
        words = _extract_words(sec['title'] + '\n\n' + sec['content'])
        all_docs.append(words)
    
    tfidf = {}
    
    for name, sec in data['sections'].items():
        words = _extract_words(sec['title'] + '\n\n' + sec['content'])
        # Filter out stopwords
        words = [w for w in words if w not in STOPWORDS]
        
        # TF
        word_counts = Counter(words)
        total_words = len(words)
        
        # IDF
        tfidf[name] = {
            'title': sec['title'],
            'content': sec['content'],
            'tfidf': {w: count / total_words * (1 + sum(1 for doc in all_docs if w in doc))
                      for w, count in word_counts.items()},
        }
    
    return tfidf


def load_knowledge_base(path: str) -> list[KnowledgeItem]:
    """Load sections from knowledge_base.json."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [
        KnowledgeItem(id=name, title=sec['title'], content=sec['content'])
        for name, sec in data['sections'].items()
    ]


def search(query: str, top_k: int = 2, items: list[KnowledgeItem] = [], 
           tfidf: dict[str, dict[str, float]] = {}) -> list[KnowledgeItem]:
    """Search by TF-IDF. Returns top-k items with score > 0."""
    query_words = set(_extract_words(query))
    query_words -= STOPWORDS
    
    if not tfidf:
        # Fallback to simple keyword overlap
        all_items = load_knowledge_base(items[0].id if items else 'knowledge_base.json')
        scores = [(item, len(query_words & set(_extract_words(item.content)))) 
                  for item in all_items]
        scores = [(item, score) for item, score in scores if score > 0]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [item for item, _ in scores[:top_k]]
    
    results = []
    for name, data in tfidf.items():
        score = sum(data['tfidf'].get(w, 0) for w in query_words)
        title_stems = set(_extract_words(data['title']))
        title_bonus = sum(2.0 for w in query_words if w in title_stems)
        score += title_bonus
        if score > 0:
            results.append((data['content'], score))
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Match back to items
    matched_items = []
    for content, _ in results[:top_k]:
        for item in items:
            if item.content == content:
                matched_items.append(item)
                break
    
    return matched_items


def reload_knowledge(path: str) -> tuple[list[KnowledgeItem], dict[str, dict[str, float]]]:
    """Reload and recompute keywords."""
    items = load_knowledge_base(path)
    tfidf = _load_keywords(path)
    return items, tfidf
