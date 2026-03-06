"""
Tests for app.memory: add_turn, get_recent_turns, get_all_turns, clear_conversation, memory_used.
No Ollama or FastAPI required; uses autouse fixture to reset conversation before/after each test.
"""
import sys
from pathlib import Path

# Project root (parent of tests/) so "app" resolves when run from any cwd.
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pytest
from app.memory import (
    add_turn,
    get_recent_turns,
    get_all_turns,
    clear_conversation,
    memory_used,
    MAX_TURNS,
)


@pytest.fixture(autouse=True)
def reset_memory():
    from app.memory import clear_conversation
    clear_conversation()
    yield
    clear_conversation()


class TestEmptyState:
    def test_after_reset_memory_used_is_false(self):
        assert memory_used() is False

    def test_after_reset_get_recent_turns_returns_empty(self):
        assert get_recent_turns() == []

    def test_after_reset_get_all_turns_returns_empty(self):
        assert get_all_turns() == []


class TestAddTurn:
    def test_add_one_turn_get_all_returns_single_dict(self):
        add_turn("user", "Hello")
        all_turns = get_all_turns()
        assert len(all_turns) == 1
        assert all_turns[0]["role"] == "user"
        assert all_turns[0]["content"] == "Hello"

    def test_falsy_content_normalized_to_empty_string(self):
        add_turn("user", "")
        all_turns = get_all_turns()
        assert len(all_turns) == 1
        assert all_turns[0]["content"] == ""


class TestGetRecentTurns:
    def test_three_turns_get_recent_10_returns_all_three_in_order(self):
        add_turn("user", "a")
        add_turn("assistant", "b")
        add_turn("user", "c")
        recent = get_recent_turns(10)
        assert len(recent) == 3
        assert recent[0]["content"] == "a"
        assert recent[1]["content"] == "b"
        assert recent[2]["content"] == "c"

    def test_three_turns_get_recent_2_returns_last_two_in_order(self):
        add_turn("user", "a")
        add_turn("assistant", "b")
        add_turn("user", "c")
        recent = get_recent_turns(2)
        assert len(recent) == 2
        assert recent[0]["content"] == "b"
        assert recent[1]["content"] == "c"

    def test_five_turns_get_recent_3_returns_last_three_first_two_not_in_list(self):
        for i in range(5):
            add_turn("user" if i % 2 == 0 else "assistant", f"msg_{i}")
        recent = get_recent_turns(3)
        assert len(recent) == 3
        assert recent[0]["content"] == "msg_2"
        assert recent[1]["content"] == "msg_3"
        assert recent[2]["content"] == "msg_4"
        contents = [t["content"] for t in recent]
        assert "msg_0" not in contents
        assert "msg_1" not in contents


class TestGetAllTurns:
    def test_multiple_add_turn_length_and_order_match(self):
        add_turn("user", "q1")
        add_turn("assistant", "a1")
        add_turn("user", "q2")
        all_turns = get_all_turns()
        assert len(all_turns) == 3
        assert all_turns[0]["role"] == "user" and all_turns[0]["content"] == "q1"
        assert all_turns[1]["role"] == "assistant" and all_turns[1]["content"] == "a1"
        assert all_turns[2]["role"] == "user" and all_turns[2]["content"] == "q2"

    def test_each_element_has_role_and_content(self):
        add_turn("user", "x")
        add_turn("assistant", "y")
        for t in get_all_turns():
            assert "role" in t
            assert "content" in t


class TestMemoryUsed:
    def test_false_when_no_turns(self):
        assert memory_used() is False

    def test_true_after_at_least_one_add_turn(self):
        add_turn("user", "hi")
        assert memory_used() is True


class TestClearConversation:
    def test_after_adding_turns_clear_then_all_empty(self):
        add_turn("user", "a")
        add_turn("assistant", "b")
        clear_conversation()
        assert get_all_turns() == []
        assert memory_used() is False
        assert get_recent_turns() == []


class TestMaxTurnsEviction:
    def test_21_turns_len_is_20_first_evicted_last_is_21st(self):
        for i in range(21):
            add_turn("user" if i % 2 == 0 else "assistant", f"turn_{i}")
        all_turns = get_all_turns()
        assert len(all_turns) == 20
        # First element should NOT be the very first turn (turn_0); oldest was evicted.
        assert all_turns[0]["content"] != "turn_0"
        assert all_turns[0]["content"] == "turn_1"  # first kept is index 1
        # Last element is the 21st turn added (index 20).
        assert all_turns[-1]["content"] == "turn_20"
