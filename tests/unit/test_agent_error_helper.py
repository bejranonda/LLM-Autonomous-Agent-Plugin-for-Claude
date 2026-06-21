"""Unit tests for lib/agent_error_helper.py.

Exercises the REAL public API:
    AVAILABLE_AGENTS, COMMON_MISTAKES, find_closest_agents,
    generate_helpful_error, suggest_agents_for_task, list_all_agents

The import is unconditional on purpose: a missing or renamed symbol must fail
the suite loudly rather than be silently skipped.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))

from agent_error_helper import (
    AVAILABLE_AGENTS,
    COMMON_MISTAKES,
    find_closest_agents,
    generate_helpful_error,
    list_all_agents,
    suggest_agents_for_task,
)


# --- data tables ------------------------------------------------------------


def test_available_agents_is_populated():
    assert isinstance(AVAILABLE_AGENTS, dict)
    assert len(AVAILABLE_AGENTS) > 0
    assert "orchestrator" in AVAILABLE_AGENTS


def test_available_agents_entries_have_required_fields():
    for name, info in AVAILABLE_AGENTS.items():
        assert "description" in info, f"{name} missing description"
        assert "category" in info, f"{name} missing category"
        assert "usage" in info, f"{name} missing usage"


def test_common_mistakes_map_to_real_agents():
    for wrong, correct in COMMON_MISTAKES.items():
        assert correct in AVAILABLE_AGENTS, f"{wrong} -> {correct} is not a real agent"


# --- find_closest_agents ----------------------------------------------------


def test_find_closest_agents_exact_match():
    assert find_closest_agents("orchestrator") == ["orchestrator"]


def test_find_closest_agents_resolves_common_mistake():
    # "security" is a known alias for "security-auditor".
    assert find_closest_agents("security") == ["security-auditor"]


def test_find_closest_agents_fuzzy_matches_typo():
    assert "orchestrator" in find_closest_agents("orchestratr")


def test_find_closest_agents_empty_for_nonsense():
    assert find_closest_agents("zzzqqqxyz") == []


def test_find_closest_agents_respects_limit():
    assert len(find_closest_agents("validator", limit=2)) <= 2


# --- generate_helpful_error -------------------------------------------------


def test_generate_helpful_error_returns_actionable_message():
    msg = generate_helpful_error("orchestratr")
    assert isinstance(msg, str)
    assert "orchestratr" in msg          # echoes the bad input
    assert "[ERROR]" in msg
    assert "orchestrator" in msg         # offers the close match


def test_generate_helpful_error_handles_no_match():
    msg = generate_helpful_error("zzzqqqxyz")
    assert isinstance(msg, str)
    assert "zzzqqqxyz" in msg
    # Falls back to listing popular agents.
    assert "orchestrator" in msg


# --- suggest_agents_for_task ------------------------------------------------


def test_suggest_agents_for_task_returns_pairs():
    result = suggest_agents_for_task("review code quality and standards")
    assert isinstance(result, list)
    assert result  # non-empty
    assert all(len(item) == 2 for item in result)
    assert all(item[0] in AVAILABLE_AGENTS for item in result)


def test_suggest_agents_for_task_matches_security():
    names = [agent for agent, _ in
             suggest_agents_for_task("security vulnerability scanning and assessment")]
    assert "security-auditor" in names


def test_suggest_agents_for_task_caps_at_three():
    result = suggest_agents_for_task("test quality security documentation performance build api")
    assert len(result) <= 3


def test_suggest_agents_for_task_defaults_to_orchestrator():
    result = suggest_agents_for_task("zzzqqqxyz")
    assert result[0][0] == "orchestrator"


# --- list_all_agents --------------------------------------------------------


def test_list_all_agents_reports_every_agent():
    out = list_all_agents()
    assert isinstance(out, str)
    assert f"{len(AVAILABLE_AGENTS)} total" in out
    assert "orchestrator" in out
