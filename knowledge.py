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


def _load_keywords(paths: list[str] | str) -> dict[str, dict[str, float]]:
    """Load and compute TF-IDF for all sections across multiple files."""
    if isinstance(paths, str):
        paths = [paths]
    all_docs = []
    sections_data = []
    
    for path in paths:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for name, sec in data['sections'].items():
            key = f"{path}:{name}"
            words = _extract_words(sec['title'] + '\n\n' + sec['content'])
            all_docs.append(words)
            sections_data.append((key, sec))
    
    tfidf = {}
    
    for key, sec in sections_data:
        words = _extract_words(sec['title'] + '\n\n' + sec['content'])
        words = [w for w in words if w not in STOPWORDS]
        
        word_counts = Counter(words)
        total_words = len(words) or 1
        
        tfidf[key] = {
            'title': sec['title'],
            'content': sec['content'],
            'tfidf': {w: count / total_words * (1 + sum(1 for doc in all_docs if w in doc))
                      for w, count in word_counts.items()},
        }
    
    return tfidf


def load_knowledge_base(paths: list[str] | str) -> list[KnowledgeItem]:
    """Load sections from multiple knowledge base files."""
    if isinstance(paths, str):
        paths = [paths]
    items = []
    for path in paths:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for name, sec in data['sections'].items():
            items.append(KnowledgeItem(id=f"{path}:{name}", title=sec['title'], content=sec['content']))
    return items


def search(query: str, top_k: int = 2, items: list[KnowledgeItem] = [], 
           tfidf: dict[str, dict[str, float]] = {}) -> list[KnowledgeItem]:
    """Search by TF-IDF. Returns top-k items with score > 0."""
    query_words = set(_extract_words(query))
    query_words -= STOPWORDS
    
    if not tfidf:
        return []
    
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


def reload_knowledge(paths: list[str] | str) -> tuple[list[KnowledgeItem], dict[str, dict[str, float]]]:
    """Reload and recompute keywords from one or multiple files."""
    if isinstance(paths, str):
        paths = [paths]
    items = load_knowledge_base(paths)
    tfidf = _load_keywords(paths)
    return items, tfidf
