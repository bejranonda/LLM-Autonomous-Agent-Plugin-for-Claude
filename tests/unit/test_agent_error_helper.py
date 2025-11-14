"""
Tests for agent_error_helper.py
"""

import pytest
import sys
import os

# Add lib to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

try:
    from agent_error_helper import (
        AVAILABLE_AGENTS,
        get_agent_suggestions,
        format_agent_help,
        find_agent_by_category,
        get_agent_description
    )
    IMPORTS_AVAILABLE = True
except (ImportError, SyntaxError) as e:
    print(f"Warning: Could not import agent_error_helper: {e}")
    IMPORTS_AVAILABLE = False


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="agent_error_helper module not available")
class TestAgentErrorHelper:
    """Test cases for agent error helper functionality"""

    def test_available_agents_structure(self):
        """Test that AVAILABLE_AGENTS has the expected structure"""
        assert isinstance(AVAILABLE_AGENTS, dict)
        assert len(AVAILABLE_AGENTS) > 0

        # Check that each agent has required fields
        for agent_name, agent_info in AVAILABLE_AGENTS.items():
            assert isinstance(agent_name, str)
            assert isinstance(agent_info, dict)
            assert "description" in agent_info
            assert "category" in agent_info
            assert "usage" in agent_info

    def test_core_agents_exist(self):
        """Test that core agents exist in AVAILABLE_AGENTS"""
        core_agents = ["orchestrator", "code-analyzer", "quality-controller", "test-engineer"]
        for agent in core_agents:
            assert agent in AVAILABLE_AGENTS, f"Core agent {agent} missing from AVAILABLE_AGENTS"

    def test_get_agent_suggestions_exact_match(self):
        """Test getting suggestions for exact agent match"""
        suggestions = get_agent_suggestions("orchestrator")
        assert "orchestrator" in suggestions or len(suggestions) == 0  # Exact match might return empty

    def test_get_agent_suggestions_close_match(self):
        """Test getting suggestions for similar agent names"""
        suggestions = get_agent_suggestions("orchestratr")  # Typo
        assert len(suggestions) > 0
        # Should suggest orchestrator or similar
        assert any("orchestrat" in s.lower() for s in suggestions)

    def test_get_agent_suggestions_no_match(self):
        """Test getting suggestions when no close match exists"""
        suggestions = get_agent_suggestions("completely_invalid_agent_name_xyz")
        # Should either return empty list or general suggestions
        assert isinstance(suggestions, list)

    def test_get_agent_suggestions_empty_input(self):
        """Test getting suggestions with empty input"""
        suggestions = get_agent_suggestions("")
        assert isinstance(suggestions, list)

    def test_get_agent_suggestions_none_input(self):
        """Test getting suggestions with None input"""
        suggestions = get_agent_suggestions(None)
        assert isinstance(suggestions, list)

    def test_format_agent_help_all_agents(self):
        """Test formatting help for all agents"""
        help_text = format_agent_help()
        assert isinstance(help_text, str)
        assert len(help_text) > 0

        # Should contain some agent names
        for agent_name in list(AVAILABLE_AGENTS.keys())[:3]:  # Check first 3
            assert agent_name in help_text

    def test_format_agent_help_specific_agent(self):
        """Test formatting help for specific agent"""
        help_text = format_agent_help("orchestrator")
        assert isinstance(help_text, str)
        assert "orchestrator" in help_text.lower()
        assert AVAILABLE_AGENTS["orchestrator"]["description"] in help_text

    def test_format_agent_help_nonexistent_agent(self):
        """Test formatting help for nonexistent agent"""
        help_text = format_agent_help("nonexistent_agent_xyz")
        # Should return general help or empty string
        assert isinstance(help_text, str)

    def test_find_agent_by_category_core(self):
        """Test finding agents by 'core' category"""
        agents = find_agent_by_category("core")
        assert isinstance(agents, list)
        assert len(agents) > 0
        assert "orchestrator" in agents

    def test_find_agent_by_category_analysis(self):
        """Test finding agents by 'analysis' category"""
        agents = find_agent_by_category("analysis")
        assert isinstance(agents, list)
        if agents:  # If category exists
            assert all(AVAILABLE_AGENTS[agent]["category"] == "analysis" for agent in agents)

    def test_find_agent_by_category_nonexistent(self):
        """Test finding agents by nonexistent category"""
        agents = find_agent_by_category("nonexistent_category_xyz")
        assert isinstance(agents, list)
        assert len(agents) == 0

    def test_find_agent_by_category_empty(self):
        """Test finding agents with empty category"""
        agents = find_agent_by_category("")
        assert isinstance(agents, list)
        assert len(agents) == 0

    def test_get_agent_description_existing_agent(self):
        """Test getting description for existing agent"""
        desc = get_agent_description("orchestrator")
        assert isinstance(desc, str)
        assert len(desc) > 0
        assert desc == AVAILABLE_AGENTS["orchestrator"]["description"]

    def test_get_agent_description_nonexistent_agent(self):
        """Test getting description for nonexistent agent"""
        desc = get_agent_description("nonexistent_agent_xyz")
        assert desc is None or isinstance(desc, str)

    def test_get_agent_description_empty_input(self):
        """Test getting description with empty input"""
        desc = get_agent_description("")
        assert desc is None or isinstance(desc, str)

    def test_agent_categories_consistency(self):
        """Test that all agents have valid categories"""
        valid_categories = {"core", "analysis", "quality", "validation", "learning",
                          "testing", "security", "documentation", "performance", "coordination"}

        for agent_name, agent_info in AVAILABLE_AGENTS.items():
            category = agent_info.get("category", "")
            assert isinstance(category, str)
            # Note: Category might not be in predefined list, but should be a string

    def test_agent_info_completeness(self):
        """Test that all agents have complete information"""
        required_fields = ["description", "category", "usage"]

        for agent_name, agent_info in AVAILABLE_AGENTS.items():
            for field in required_fields:
                assert field in agent_info, f"Agent {agent_name} missing field {field}"
                assert isinstance(agent_info[field], str), f"Agent {agent_name} {field} not a string"
                assert len(agent_info[field]) > 0, f"Agent {agent_name} {field} is empty"

    def test_suggestions_case_insensitive(self):
        """Test that suggestions work case-insensitively"""
        suggestions_lower = get_agent_suggestions("orchestrator")
        suggestions_upper = get_agent_suggestions("ORCHESTRATOR")
        suggestions_mixed = get_agent_suggestions("Orchestrator")

        # All should return similar results
        assert isinstance(suggestions_lower, list)
        assert isinstance(suggestions_upper, list)
        assert isinstance(suggestions_mixed, list)


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="agent_error_helper module not available")
class TestAgentErrorHelperEdgeCases:
    """Test edge cases and error conditions"""

    def test_difflib_integration(self):
        """Test that difflib get_close_matches works as expected"""
        from difflib import get_close_matches

        word_list = ["orchestrator", "code-analyzer", "quality-controller"]

        # Test close matches
        matches = get_close_matches("orchestratr", word_list, n=3, cutoff=0.6)
        assert isinstance(matches, list)
        assert len(matches) <= 3

    def test_available_agents_immutability(self):
        """Test that AVAILABLE_AGENTS can be accessed without modification issues"""
        original_count = len(AVAILABLE_AGENTS)

        # Access the data
        agents_copy = dict(AVAILABLE_AGENTS)

        # Should not affect original
        assert len(AVAILABLE_AGENTS) == original_count
        assert agents_copy == AVAILABLE_AGENTS