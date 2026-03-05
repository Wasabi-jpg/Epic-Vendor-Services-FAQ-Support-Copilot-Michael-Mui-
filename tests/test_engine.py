"""
Tests for engine: format_faq_for_prompt, parse_answer_and_sources, build_sources_from_ids.
No Ollama required; these are unit tests only.
"""
import sys
from pathlib import Path

# Project root (parent of tests/) so "app" resolves when run from any cwd.
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pytest
from app.engine import (
    format_faq_for_prompt,
    parse_answer_and_sources,
    build_sources_from_ids,
)


# Minimal FAQ for tests (order defines IDs 1, 2, 3).
SAMPLE_FAQ = [
    {"category": "General", "question": "What is X?", "answer": "X is a thing.", "source_url": "https://example.com/1"},
    {"category": "Access", "question": "How do I log in?", "answer": "Use the login page.", "source_url": "https://example.com/2"},
    {"category": "Billing", "question": "What does it cost?", "answer": "Pricing starts at $100.", "source_url": "https://example.com/3"},
]


class TestFormatFaqForPrompt:
    def test_returns_string_with_all_entry_ids(self):
        out = format_faq_for_prompt(SAMPLE_FAQ)
        assert "[1]" in out
        assert "[2]" in out
        assert "[3]" in out
        assert "What is X?" in out
        assert "How do I log in?" in out
        assert "What does it cost?" in out

    def test_empty_list_returns_empty_string(self):
        assert format_faq_for_prompt([]) == ""

    def test_single_entry_has_id_one(self):
        single = [SAMPLE_FAQ[0]]
        out = format_faq_for_prompt(single)
        assert "[1]" in out
        assert "[2]" not in out


class TestParseAnswerAndSources:
    def test_extracts_answer_and_source_ids(self):
        raw = "Answer: You can log in via the login page.\nSource IDs: 2"
        answer, ids = parse_answer_and_sources(raw)
        assert "log in" in answer
        assert ids == [2]

    def test_extracts_multiple_source_ids(self):
        raw = "Answer: See the FAQ.\nSource IDs: 1, 3"
        answer, ids = parse_answer_and_sources(raw)
        assert ids == [1, 3]

    def test_accepts_sources_keyword(self):
        raw = "Answer: Ok.\nSources: 2, 1"
        answer, ids = parse_answer_and_sources(raw)
        assert ids == [2, 1]

    def test_empty_output_returns_empty_answer_and_no_ids(self):
        answer, ids = parse_answer_and_sources("")
        assert answer == ""
        assert ids == []

    def test_fallback_when_no_source_ids_line(self):
        raw = "Just some answer text with no Source IDs line."
        answer, ids = parse_answer_and_sources(raw)
        assert "Just some answer" in answer
        assert ids == []


class TestBuildSourcesFromIds:
    def test_maps_ids_to_sources(self):
        sources = build_sources_from_ids(SAMPLE_FAQ, [1, 3])
        assert len(sources) == 2
        assert sources[0]["category"] == "General"
        assert sources[0]["question"] == "What is X?"
        assert sources[0]["source_url"] == "https://example.com/1"
        assert sources[1]["category"] == "Billing"
        assert sources[1]["question"] == "What does it cost?"
        assert sources[1]["source_url"] == "https://example.com/3"

    def test_skips_invalid_ids(self):
        sources = build_sources_from_ids(SAMPLE_FAQ, [0, 1, 99])
        assert len(sources) == 1
        assert sources[0]["question"] == "What is X?"

    def test_empty_ids_returns_empty_list(self):
        assert build_sources_from_ids(SAMPLE_FAQ, []) == []
