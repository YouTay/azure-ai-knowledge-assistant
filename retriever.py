import os
from pathlib import Path

KB_DIR = Path("kb")

def load_kb() -> list[dict]:
    docs = []
    for p in KB_DIR.glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        docs.append({"id": p.name, "text": text})
    return docs

def simple_retrieve(query: str, k: int = 2) -> list[dict]:
    """
    Super simple retrieval:
    - score by keyword overlap
    - returns top-k docs
    """
    q = query.lower()
    docs = load_kb()

    def score(doc_text: str) -> int:
        tokens = [t for t in q.replace("/", " ").replace("-", " ").split() if len(t) >= 3]
        return sum(1 for t in set(tokens) if t in doc_text.lower())

    ranked = sorted(docs, key=lambda d: score(d["text"]), reverse=True)
    return ranked[:k]