"""
FAQ retrieval and Ollama-backed answering. Source-grounded responses with citations.
"""
import json
import os
import re
from pathlib import Path
import ollama

# Resolve project root so this works when run as script or as module
_APP_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _APP_DIR.parent
_FAQ_PATH = _PROJECT_ROOT / "SEED_DATA" / "epic_vendor_faq.json"


def load_faq(path: Path | None = _FAQ_PATH) -> list[dict]:
    """Load FAQ entries from JSON. Uses SEED_DATA/epic_vendor_faq.json by default."""
    p = path or _FAQ_PATH
    if not p.exists():
        raise FileNotFoundError(f"FAQ file not found: {p}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _normalize(text: str) -> str:
    """Lowercase and collapse whitespace for scoring."""
    return " ".join(re.sub(r"[^a-z0-9\s]", "", text.lower()).split())


def score_entry(query: str, entry: dict) -> float:
    """
    Score one FAQ entry against the query. Higher = better match.
    Uses word overlap between query and (question + answer + category).
    """
    q = _normalize(query)
    if not q:
        return 0.0
    combined = _normalize(
        f"{entry.get('category', '')} {entry.get('question', '')} {entry.get('answer', '')}"
    )
    query_words = set(q.split())
    text_words = set(combined.split())
    overlap = len(query_words & text_words)
    # Prefer entries where more of the query words appear
    return overlap / len(query_words) if query_words else 0.0


def retrieve(
    query: str,
    faq_data: list[dict] | None = None,
    top_k: int = 3,
    min_score: float = 0.0,
) -> list[dict]:
    """
    Return top_k FAQ entries most relevant to the query.
    Each returned dict includes the original entry; optionally add a "score" key for debugging.
    """
    if faq_data is None:
        faq_data = load_faq()
    if not query or not faq_data:
        return []
    scored = [(e, score_entry(query, e)) for e in faq_data]
    scored = [(e, s) for e, s in scored if s >= min_score]
    scored.sort(key=lambda x: -x[1])
    return [e for e, _ in scored[:top_k]]


def answer_with_sources(
    query: str,
    retrieved_entries: list[dict],
    conversation_history: list[dict] | None = None,
    model: str = "llama3.2:1b",
) -> dict:
    """
    Call Ollama with FAQ context (and optional prior turns) and return answer + sources.
    retrieved_entries: list of most relevant faq entries (hits) used to send to the model.
    conversation_history: list of {"role": "user"|"assistant", "content": "..."}
    Returns: {"answer": str, "sources": [{"category", "question", "source_url"}]}
    """
    # import ollama

    # Build context from retrieved FAQ entries
    context_parts = []
    for i, e in enumerate(retrieved_entries, 1):
        cat = e.get("category", "")
        q = e.get("question", "")
        ans = e.get("answer", "")
        context_parts.append(f"[{i}] ({cat}) Q: {q}\nA: {ans}")
    faq_context = "\n\n".join(context_parts) if context_parts else "No relevant FAQ entries found."

    system = """You are an Epic Vendor Services support agent. 
    Answer only using the provided FAQ context. Be concise. 
    If the context does not contain enough information, say so and suggest the user rephrase or contact support. 
    For login or password issues, direct users to use "Forgot username or password" or contact their admin / UserWeb Support / vendorservices@epic.com—do not invent reset steps."""

    user_block = ""
    if conversation_history:
        for turn in conversation_history[-6:]:  # last 3 exchanges 
            role = turn.get("role", "")
            content = turn.get("content", "")
            user_block += f"({role}): {content}\n"
        user_block += f"(user): {query}\n"
    else:
        user_block = query

    prompt = f"""FAQ context:\n{faq_context}\n\nConversation so far:\n{user_block}\n\n System Constraints:\n{system}"""

    messages = [{"role": "user", "content": prompt}]
    response = ollama.chat(model=model, messages=messages)
    answer = (response.get("message") or {}).get("content", "").strip()

    sources = [
        {
            "category": e.get("category", ""),
            "question": e.get("question", ""),
            "source_url": e.get("source_url", ""),
        }
        for e in retrieved_entries
    ]

    return {
        "answer": answer,
        "sources": sources
    }


def run_query(
    query: str,
    conversation_history: list[dict] | None = None,
    faq_data: list[dict] | None = None,
    model: str = "llama3.2:1b",
    top_k: int = 3,
    min_score: float = 0.0,
) -> dict:
    """
    One-shot: load FAQ (if needed), retrieve, then answer with sources.
    For use by API or terminal testing.
    """
    if faq_data is None:
        faq_data = load_faq()
    retrieved = retrieve(query, faq_data=faq_data, top_k=top_k, min_score=min_score)
    return answer_with_sources(
        query,
        retrieved,
        conversation_history=conversation_history,
        model=model,
    )


if __name__ == "__main__":
    # Run from project root: python app/engine.py   or   python -m app.engine
    print("Loading FAQ...")
    faq = load_faq()
    print(f"Loaded {len(faq)} entries.\n")

    test_query = "How do I log in to Vendor Services?"
    print(f"Retrieving for: {test_query!r}")
    hits = retrieve(test_query, faq_data=faq, top_k=3)
    for i, e in enumerate(hits, 1):
        print(f"  {i}. [{e.get('category')}] {e.get('question')}")

    print("\nCalling Ollama for answer with sources...")
    result = answer_with_sources(test_query, hits, conversation_history=None)
    print("Answer:", result["answer"][:300] + ("..." if len(result["answer"]) > 300 else ""))
    print("Sources:", result["sources"])

    print("\nTesting run_query()")
    rq_result = run_query("What is Vendor Services")
    print(f"Answer: {rq_result["answer"]}\n")
    print(f"Sources: {result["sources"]}")


    
