"""
Tests for plugin_validator.py
"""

import pytest
import os
import sys
import json
from unittest.mock import patch, mock_open
from pathlib import Path

# Add lib to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

try:
    from plugin_validator import (
        validate_plugin_manifest,
        validate_agent_file,
        validate_skill_file,
        validate_command_file,
        validate_plugin_structure,
        PluginValidationError
    )
    IMPORTS_AVAILABLE = True
except (ImportError, SyntaxError) as e:
    print(f"Warning: Could not import plugin_validator: {e}")
    IMPORTS_AVAILABLE = False


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="plugin_validator module not available")
class TestPluginValidator:
    """Test cases for plugin validation functionality"""

    def test_validate_plugin_manifest_valid(self):
        """Test validating a valid plugin manifest"""
        valid_manifest = {
            "name": "autonomous-agent",
            "version": "7.7.0",
            "description": "Autonomous Claude Agent Plugin",
            "author": "Test Author",
            "license": "MIT",
            "claude_code_version": ">=1.0.0"
        }

        with patch("builtins.open", mock_open(read_data=json.dumps(valid_manifest))):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_plugin_manifest("plugin.json")

        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 0

    def test_validate_plugin_manifest_missing_required_fields(self):
        """Test validating manifest with missing required fields"""
        incomplete_manifest = {
            "name": "autonomous-agent",
            # Missing version, description, etc.
        }

        with patch("builtins.open", mock_open(read_data=json.dumps(incomplete_manifest))):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_plugin_manifest("plugin.json")

        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert any("version" in error.lower() for error in result["errors"])

    def test_validate_plugin_manifest_invalid_version_format(self):
        """Test validating manifest with invalid version format"""
        invalid_manifest = {
            "name": "autonomous-agent",
            "version": "not.a.version",
            "description": "Test plugin",
            "author": "Test Author",
            "license": "MIT"
        }

        with patch("builtins.open", mock_open(read_data=json.dumps(invalid_manifest))):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_plugin_manifest("plugin.json")

        assert result["valid"] is False
        assert any("version" in error.lower() for error in result["errors"])

    def test_validate_agent_file_valid_structure(self):
        """Test validating agent file with valid structure"""
        valid_agent_content = """---
name: "test-agent"
description: "Test agent for validation"
category: "testing"
skills:
  - code-analysis
  - quality-standards
---

# Test Agent

This is a test agent with valid structure.
"""

        with patch("builtins.open", mock_open(read_data=valid_agent_content)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_agent_file("agents/test-agent.md")

        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_agent_file_missing_yaml_frontmatter(self):
        """Test validating agent file without YAML frontmatter"""
        invalid_agent_content = """# Test Agent

This agent has no YAML frontmatter.
"""

        with patch("builtins.open", mock_open(read_data=invalid_agent_content)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_agent_file("agents/test-agent.md")

        assert result["valid"] is False
        assert any("frontmatter" in error.lower() for error in result["errors"])

    def test_validate_agent_file_missing_required_fields(self):
        """Test validating agent file with missing required YAML fields"""
        incomplete_agent_content = """---
name: "test-agent"
# Missing description and category
---

# Test Agent
"""

        with patch("builtins.open", mock_open(read_data=incomplete_agent_content)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_agent_file("agents/test-agent.md")

        assert result["valid"] is False
        assert len(result["errors"]) >= 2  # description and category missing

    def test_validate_skill_file_valid_structure(self):
        """Test validating skill file with valid structure"""
        valid_skill_content = """---
name: "code-analysis"
description: "Code analysis and pattern detection"
category: "analysis"
difficulty: "intermediate"
---

# Code Analysis Skill

This skill provides code analysis capabilities.

## Domain Analysis
Analyzes code structure and patterns.

## When to Apply
Use when you need to understand code architecture.
"""

        with patch("builtins.open", mock_open(read_data=valid_skill_content)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_skill_file("skills/code-analysis/SKILL.md")

        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_skill_file_not_in_skill_directory(self):
        """Test validating skill file not in skills/ directory"""
        with patch("builtins.open", mock_open(read_data="# Test")):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_skill_file("not/in/skills/test.md")

        assert result["valid"] is False
        assert any("skills" in error.lower() for error in result["errors"])

    def test_validate_command_file_valid_structure(self):
        """Test validating command file with valid structure"""
        valid_command_content = """
# /test-command

Test command description for validation.

## Usage
/test-command [options]

## Examples
/test-command --help

## Parameters
- options: Command options
"""

        with patch("builtins.open", mock_open(read_data=valid_command_content)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_command_file("commands/test-command.md")

        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_command_file_missing_description(self):
        """Test validating command file with missing description"""
        incomplete_command_content = """
# /test-command

## Usage
/test-command
"""

        with patch("builtins.open", mock_open(read_data=incomplete_command_content)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_command_file("commands/test-command.md")

        assert result["valid"] is False
        # Should warn about missing description

    def test_validate_plugin_structure_complete(self):
        """Test validating complete plugin structure"""
        required_files = [
            ".claude-plugin/plugin.json",
            "agents/",
            "skills/",
            "commands/"
        ]

        existing_files = {
            ".claude-plugin/plugin.json": True,
            "agents/": True,
            "skills/": True,
            "commands/": True,
            "README.md": True
        }

        with patch("pathlib.Path.exists", side_effect=lambda x: existing_files.get(str(x), False)):
            with patch("pathlib.Path.is_dir", side_effect=lambda x: str(x).endswith("/")):
                result = validate_plugin_structure("/test/plugin")

        assert result["valid"] is True
        assert len(result["missing_files"]) == 0

    def test_validate_plugin_structure_missing_components(self):
        """Test validating plugin structure with missing components"""
        existing_files = {
            ".claude-plugin/plugin.json": True,
            "agents/": False,  # Missing
            "skills/": True,
            "commands/": False  # Missing
        }

        with patch("pathlib.Path.exists", side_effect=lambda x: existing_files.get(str(x), False)):
            with patch("pathlib.Path.is_dir", side_effect=lambda x: str(x).endswith("/")):
                result = validate_plugin_structure("/test/plugin")

        assert result["valid"] is False
        assert "agents/" in result["missing_files"]
        assert "commands/" in result["missing_files"]

    def test_plugin_validation_error_custom(self):
        """Test custom PluginValidationError exception"""
        error = PluginValidationError("Test validation error", file="test.py", line=10)

        assert str(error) == "Test validation error"
        assert error.file == "test.py"
        assert error.line == 10


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="plugin_validator module not available")
class TestPluginValidatorEdgeCases:
    """Test edge cases and error conditions"""

    def test_validate_nonexistent_manifest(self):
        """Test validating non-existent plugin manifest"""
        with patch("pathlib.Path.exists", return_value=False):
            result = validate_plugin_manifest("nonexistent.json")

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_invalid_json_manifest(self):
        """Test validating manifest with invalid JSON"""
        invalid_json = '{"name": "test", "version": 1.0.0'  # Missing closing brace

        with patch("builtins.open", mock_open(read_data=invalid_json)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_plugin_manifest("invalid.json")

        assert result["valid"] is False
        assert any("json" in error.lower() for error in result["errors"])

    def test_validate_agent_file_read_error(self):
        """Test agent file validation with read error"""
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_agent_file("restricted.md")

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_empty_files(self):
        """Test validating empty files"""
        with patch("builtins.open", mock_open(read_data="")):
            with patch("pathlib.Path.exists", return_value=True):
                agent_result = validate_agent_file("empty.md")
                command_result = validate_command_file("empty.md")

        assert agent_result["valid"] is False
        assert command_result["valid"] is False

    def test_validate_plugin_structure_empty_path(self):
        """Test validating plugin structure with empty path"""
        result = validate_plugin_structure("")

        # Should handle empty path gracefully
        assert isinstance(result, dict)
        assert "valid" in result