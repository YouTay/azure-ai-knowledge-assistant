from pathlib import Path

KB_DIR = Path("kb")

# These are "always relevant" for architecture answers.
CORE_FILES = {
    "00_playbook.md",
    "10_intake_questions.md",
    "20_patterns_catalog.md",
    "40_tradeoffs_cost.md",
    "50_enterprise_baseline.md",
    "32_network_security.md",
}

def load_kb() -> list[dict]:
    """
    Load all markdown files recursively from kb/.
    Keeps id as relative path for traceability.
    """
    docs = []
    for p in KB_DIR.rglob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        rel = str(p.relative_to(KB_DIR))
        docs.append({"id": rel, "text": text})
    return docs

def _tokenize(text: str) -> list[str]:
    t = text.lower().replace("/", " ").replace("-", " ")
    tokens = [x.strip() for x in t.split() if len(x.strip()) >= 3]
    return tokens

def simple_retrieve(query: str, k: int = 4) -> list[dict]:
    """
    MVP retrieval with guardrails:
    - keyword overlap scoring
    - strong bias towards CORE_FILES
    - returns top-k docs
    """
    q_tokens = set(_tokenize(query))
    docs = load_kb()

    def score(doc: dict) -> int:
        doc_text = doc["text"].lower()

        # keyword overlap
        overlap = sum(1 for t in q_tokens if t in doc_text)

        # core bias: ensure playbook/intake/security/cost/enterprise are frequently included
        base = 0
        doc_name = Path(doc["id"]).name
        if doc_name in CORE_FILES:
            base += 5

        # lightweight topic nudges (helps pick compute/data docs when query suggests it)
        topic_bonus = 0
        if any(t in q_tokens for t in {"aks", "kubernetes", "container", "api", "compute", "app"}):
            if "compute" in doc_name or "container" in doc_text or "compute" in doc_text:
                topic_bonus += 2
        if any(t in q_tokens for t in {"sql", "cosmos", "database", "data", "storage"}):
            if "data" in doc_name or "database" in doc_text or "storage" in doc_text:
                topic_bonus += 2
        if any(t in q_tokens for t in {"network", "vnet", "private", "waf", "front"}):
            if "network" in doc_name or "waf" in doc_text or "vnet" in doc_text:
                topic_bonus += 2
        if any(t in q_tokens for t in {"cost", "budget", "pricing"}):
            if "cost" in doc_name or "cost" in doc_text:
                topic_bonus += 2
        if any(t in q_tokens for t in {"security", "compliance", "gdpr", "pci", "iso", "soc"}):
            if "security" in doc_name or "entra" in doc_text or "key vault" in doc_text:
                topic_bonus += 2

        return base + topic_bonus + overlap

    ranked = sorted(docs, key=score, reverse=True)

    # Guarantee at least the playbook is present
    # (only if it exists; avoids errors if file renamed)
    playbook = [d for d in ranked if Path(d["id"]).name == "00_playbook.md"]
    selected = []
    if playbook:
        selected.append(playbook[0])

    for d in ranked:
        if d in selected:
            continue
        selected.append(d)
        if len(selected) >= k:
            break

    return selected[:k]