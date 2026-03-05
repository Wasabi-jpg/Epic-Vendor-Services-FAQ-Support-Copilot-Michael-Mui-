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


def format_faq_for_prompt(faq_data: list[dict]) -> str:
    """
    Format the full FAQ into one prompt-ready string. Each entry gets a 1-based ID [i].
    No filtering; used so the model sees all entries and can cite IDs for sources (Option C).
    """
    parts = []
    for i, e in enumerate(faq_data, 1):
        cat = e.get("category", "")
        q = e.get("question", "")
        ans = e.get("answer", "")
        parts.append(f"[{i}] ({cat}) Q: {q}\nA: {ans}")
    return "\n\n".join(parts) if parts else ""


def parse_answer_and_sources(model_output: str) -> tuple[str, list[int]]:
    """
    Extract answer text and source IDs from model output.
    Expected format: "Answer: <text>\\nSource IDs: 1, 3" or "Source IDs: 1, 3\\nAnswer: <text>".
    Fallback: return (whole response, []).
    """
    if not model_output or not model_output.strip():
        return ("", [])
    text = model_output.strip()
    source_ids: list[int] = []
    # Try "Source IDs: 1, 3" or "Sources: 1, 3" (flexible)
    for pattern in [
        r"[Ss]ource\s*IDs?\s*:\s*([\d\s,]+)",
        r"[Ss]ources?\s*:\s*([\d\s,]+)",
    ]:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            raw = m.group(1)
            for part in raw.replace(",", " ").split():
                if part.isdigit():
                    source_ids.append(int(part))
            source_ids = list(dict.fromkeys(source_ids))  # preserve order, dedupe
            break
    # Remove the Source IDs line from text to get answer only
    answer = text
    for pattern in [
        r"\n?[Ss]ource\s*IDs?\s*:\s*[\d\s,]+\s*",
        r"\n?[Ss]ources?\s*:\s*[\d\s,]+\s*",
    ]:
        answer = re.sub(pattern, "\n", answer, flags=re.IGNORECASE)
    # Extract "Answer: ..." if present
    answer_m = re.search(r"[Aa]nswer\s*:\s*(.+)", answer, re.DOTALL)
    if answer_m:
        answer = answer_m.group(1).strip()
    else:
        answer = re.sub(r"^[Aa]nswer\s*:\s*", "", answer).strip()
    if not answer:
        answer = text.strip()
    return (answer, source_ids)


def build_sources_from_ids(faq_data: list[dict], source_ids: list[int]) -> list[dict]:
    """Map 1-based FAQ entry IDs to list of {category, question, source_url}. Invalid IDs skipped."""
    n = len(faq_data)
    sources = []
    for i in source_ids:
        if 1 <= i <= n:
            e = faq_data[i - 1]
            sources.append({
                "category": e.get("category", ""),
                "question": e.get("question", ""),
                "source_url": e.get("source_url", ""),
            })
    return sources


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


def score_query_with_history(
    current_query: str,
    conversation_history: list[dict] | None,
    threshold: float = 0.2,
) -> bool:
    """
    Decide whether to use conversation history based on topic continuity.
    Considers the past 6 turns, scores current query against prior user messages only.
    Returns True if max overlap with any of the last 3 user messages >= threshold.
    """
    if not conversation_history or not current_query: # Potential problem? Missing query, what happens?
        return False
    recent = conversation_history[-6:]
    user_contents = [t["content"] for t in recent if t.get("role") == "user"]
    prior_user_queries = user_contents[-3:]  # at most 3 prior user messages
    if not prior_user_queries:
        return False
    scores = []
    for prior_text in prior_user_queries:
        # Reuse score_entry: treat prior user message as a minimal "entry"
        entry = {"category": "", "question": prior_text, "answer": ""}
        scores.append(score_entry(current_query, entry))
    topic_score = max(scores) if scores else 0.0
    return topic_score >= threshold


# def retrieve(
#     query: str,
#     faq_data: list[dict] | None = None,
#     top_k: int = 3,
#     min_score: float = 0.0,
# ) -> list[dict]:
#     """
#     Return top_k FAQ entries most relevant to the query.
#     Each returned dict includes the original entry; optionally add a "score" key for debugging.
#     """
#     if faq_data is None:
#         faq_data = load_faq()
#     if not query or not faq_data:
#         return []
#     scored = [(e, score_entry(query, e)) for e in faq_data]
#     scored = [(e, s) for e, s in scored if s >= min_score]
#     scored.sort(key=lambda x: -x[1])
#     return [e for e, _ in scored[:top_k]]


# Default model: larger model for reasoning over full FAQ (Option C source grounding).
_DEFAULT_MODEL = "llama3.2:3b"# larger model: "llama3.1:8b"


def answer_with_sources(
    query: str,
    faq_data: list[dict],
    conversation_history: list[dict] | None = None,
    model: str = _DEFAULT_MODEL,
) -> dict:
    """
    Call Ollama with full FAQ context (formatted). Model must output Answer and Source IDs.
    faq_data: full list of FAQ entries (all sent; no retrieval filter).
    conversation_history: list of {"role": "user"|"assistant", "content": "..."}
    Returns: {"answer": str, "sources": [{"category", "question", "source_url"}]}
    Source grounding (Option C): sources come from model-cited entry IDs.
    """
    faq_context = format_faq_for_prompt(faq_data)
    if not faq_context:
        return {"answer": "No FAQ data available.", "sources": []}

    system = """You are an Epic Vendor Services support agent.
Answer only using the provided FAQ context. Be concise.
If the context does not contain enough information, say so and suggest the user rephrase or contact support.
For login or password issues, direct users to use "Forgot username or password" or contact their admin / UserWeb Support / vendorservices@epic.com—do not invent reset steps.

You must reply in this exact format:
Answer: <your answer here>
Source IDs: <comma-separated list of FAQ entry numbers you used, e.g. 1, 3>"""

    user_block = ""
    if conversation_history:
        for turn in conversation_history[-6:]:
            role = turn.get("role", "")
            content = turn.get("content", "")
            user_block += f"({role}): {content}\n"
        user_block += f"(user): {query}\n"
    else:
        user_block = query

    prompt = f"""FAQ (each entry has an ID in brackets; cite these IDs in Source IDs):\n{faq_context}\n\nConversation so far:\n{user_block}"""

    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    response = ollama.chat(model=model, messages=messages)
    raw = (response.get("message") or {}).get("content", "").strip()

    answer, source_ids = parse_answer_and_sources(raw)
    sources = build_sources_from_ids(faq_data, source_ids)

    return {
        "answer": answer,
        "sources": sources,
    }


def run_query(
    query: str,
    conversation_history: list[dict] | None = None,
    faq_data: list[dict] | None = None,
    model: str = _DEFAULT_MODEL,
) -> dict:
    """
    One-shot: load FAQ (if needed), format full FAQ, then answer with sources.
    No retrieval for context selection; full FAQ is sent. Sources from model-cited IDs (Option C).
    """
    if faq_data is None:
        faq_data = load_faq()
    use_history = score_query_with_history(query, conversation_history)
    history = conversation_history if use_history else None
    return answer_with_sources(
        query,
        faq_data,
        conversation_history=history,
        model=model,
    )


if __name__ == "__main__":
    # Run from project root: python app/engine.py   or   python -m app.engine
    print("Loading FAQ...")
    faq = load_faq()
    print(f"Loaded {len(faq)} entries.\n")

    test_query = "How do I log in to Vendor Services?"
    print(f"Calling run_query (full FAQ, model-cited sources) for: {test_query!r}")
    result = run_query(test_query, conversation_history=None, faq_data=faq)
    print("Answer:", result["answer"][:300] + ("..." if len(result["answer"]) > 300 else ""))
    print("Sources:", result["sources"])


    
