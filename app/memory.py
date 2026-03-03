"""
In-memory conversation store for the current app run.
Uses a deque (queue): FIFO, and optional maxlen for a rolling window of turns.
One conversation per process; when the app stops, it's gone. No cross-run persistence.
"""
from collections import deque
from typing import Any

# Set to an int to keep only the last N turns (oldest drop off); None = unbounded.
MAX_TURNS: int = 20

# Single conversation: deque of {"role": "user" | "assistant", "content": str}
_turns: deque[dict[str, Any]] = deque(maxlen=MAX_TURNS)


def add_turn(role: str, content: str) -> None:
    """Append one message. role should be 'user' or 'assistant'."""
    _turns.append({"role": role, "content": content or ""})


def get_recent_turns(n: int = 10) -> list[dict[str, Any]]:
    """Return the last n turns (each is {"role", "content"})."""
    if len(_turns) <= n:
        return list(_turns)
    return list(_turns)[-n:]


def get_all_turns() -> list[dict[str, Any]]:
    """Return all turns in this run's conversation."""
    return list(_turns)


def clear_conversation() -> None:
    """Clear all turns. Same effect as starting fresh (still in same process)."""
    _turns.clear()


def memory_used() -> bool:
    """True if there is at least one prior turn (memory is in use)."""
    return len(_turns) > 0


if __name__ == "__main__":
    # Quick sanity check: add turns, retrieve, clear
    assert not memory_used()

    add_turn("user", "How do I log in?")
    add_turn("assistant", "Use the Vendor Services login menu...")
    add_turn("user", "What if I forgot my password?")

    assert memory_used()
    recent = get_recent_turns(n=4)
    assert len(recent) == 3
    assert recent[0]["role"] == "user" and recent[0]["content"] == "How do I log in?"
    assert recent[-1]["content"] == "What if I forgot my password?"

    clear_conversation()
    assert not memory_used()
    assert get_recent_turns() == []

    # Maxlen test: simulated 20-turn conversation, then one more pair; no LLM calls.
    # Use a local deque with maxlen=20 to verify FIFO eviction.
    q: deque[dict[str, Any]] = deque(maxlen=20)
    for i in range(10):
        q.append({"role": "user", "content": f"simulated_user_{i + 1}"})
        q.append({"role": "assistant", "content": f"simulated_asst_{i + 1}"})
    assert len(q) == 20, "after 20 entries we should have 20"
    first_before = (q[0]["role"], q[0]["content"])
    last_before = (q[-1]["role"], q[-1]["content"])

    q.append({"role": "user", "content": "simulated_user_11"})
    q.append({"role": "assistant", "content": "simulated_asst_11"})
    assert len(q) == 20, "maxlen=20: after inserting 22 entries we must have 20"
    assert (q[0]["role"], q[0]["content"]) != first_before, "oldest entry should be evicted"
    assert q[0] == {"role": "user", "content": "simulated_user_2"}, "first kept is 2nd user (user_1 and asst_1 evicted)"
    assert q[-1] == {"role": "assistant", "content": "simulated_asst_11"}, "last is the new assistant reply"

    print("memory.py: all checks passed.")
