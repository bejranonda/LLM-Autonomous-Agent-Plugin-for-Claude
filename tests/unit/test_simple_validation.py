"""
Tests for simple_validation.py
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
    from simple_validation import (
        validate_json_file,
        validate_yaml_file,
        validate_python_syntax,
        validate_markdown_file,
        validate_file_structure,
        run_basic_validation
    )
    IMPORTS_AVAILABLE = True
except (ImportError, SyntaxError) as e:
    print(f"Warning: Could not import simple_validation: {e}")
    IMPORTS_AVAILABLE = False


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="simple_validation module not available")
class TestSimpleValidation:
    """Test cases for simple validation functions"""

    def test_validate_json_file_valid(self):
        """Test validating a valid JSON file"""
        valid_json = '{"name": "test", "version": "1.0.0", "type": "plugin"}'

        with patch("builtins.open", mock_open(read_data=valid_json)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_json_file("test.json")

        assert result["valid"] is True
        assert result["errors"] == []

    def test_validate_json_file_invalid(self):
        """Test validating an invalid JSON file"""
        invalid_json = '{"name": "test", "version": 1.0.0, "type": "plugin"'  # Missing closing brace

        with patch("builtins.open", mock_open(read_data=invalid_json)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_json_file("test.json")

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_json_file_empty(self):
        """Test validating an empty JSON file"""
        with patch("builtins.open", mock_open(read_data="")):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_json_file("empty.json")

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_json_file_not_exists(self):
        """Test validating a non-existent JSON file"""
        with patch("pathlib.Path.exists", return_value=False):
            result = validate_json_file("nonexistent.json")

        assert result["valid"] is False
        assert any("not found" in error.lower() for error in result["errors"])

    def test_validate_yaml_file_valid(self):
        """Test validating a valid YAML file"""
        valid_yaml = """
name: test
version: 1.0.0
type: plugin
dependencies:
  - requests
  - pytest
"""

        try:
            import yaml
            yaml_available = True
        except ImportError:
            yaml_available = False

        if yaml_available:
            with patch("builtins.open", mock_open(read_data=valid_yaml)):
                with patch("pathlib.Path.exists", return_value=True):
                    result = validate_yaml_file("test.yaml")

            assert result["valid"] is True
            assert result["errors"] == []
        else:
            # Skip YAML tests if PyYAML not available
            pytest.skip("PyYAML not available")

    def test_validate_python_syntax_valid(self):
        """Test validating Python file with valid syntax"""
        valid_python = '''
def hello_world():
    """Say hello to the world."""
    print("Hello, World!")
    return True

if __name__ == "__main__":
    hello_world()
'''

        with patch("builtins.open", mock_open(read_data=valid_python)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_python_syntax("test.py")

        assert result["valid"] is True
        assert result["errors"] == []

    def test_validate_python_syntax_invalid(self):
        """Test validating Python file with invalid syntax"""
        invalid_python = '''
def hello_world()
    # Missing colon
    print("Hello, World!"
    # Missing closing parenthesis
'''

        with patch("builtins.open", mock_open(read_data=invalid_python)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_python_syntax("test.py")

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_python_syntax_empty(self):
        """Test validating empty Python file"""
        with patch("builtins.open", mock_open(read_data="")):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_python_syntax("empty.py")

        # Empty file is valid Python
        assert result["valid"] is True
        assert result["errors"] == []

    def test_validate_markdown_file_valid(self):
        """Test validating a valid markdown file"""
        valid_markdown = """
# Test Document

This is a test markdown file with valid syntax.

## Section 1

- Item 1
- Item 2
- Item 3

### Subsection

```python
def hello():
    print("Hello")
```

[Link](https://example.com)
"""

        with patch("builtins.open", mock_open(read_data=valid_markdown)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_markdown_file("test.md")

        assert result["valid"] is True
        assert result["errors"] == []

    def test_validate_markdown_file_invalid_links(self):
        """Test validating markdown file with broken links"""
        markdown_with_broken_links = """
# Test Document

[Broken Link](nonexistent-file.md)
[Another Broken](missing-reference.md)
"""

        with patch("builtins.open", mock_open(read_data=markdown_with_broken_links)):
            with patch("pathlib.Path.exists", return_value=True):
                with patch("pathlib.Path.is_file", return_value=False):
                    result = validate_markdown_file("test.md")

        # Should have warnings about broken links
        assert len(result["warnings"]) > 0

    def test_validate_file_structure_complete(self):
        """Test validating complete file structure"""
        files = {
            "plugin.json": True,
            "README.md": True,
            ".claude-plugin/": True,
            "agents/": True,
            "skills/": True,
            "commands/": True
        }

        with patch("pathlib.Path.exists", side_effect=lambda x: files.get(str(x), False)):
            with patch("pathlib.Path.is_dir", side_effect=lambda x: str(x).endswith("/")):
                result = validate_file_structure("/test/plugin")

        assert result["valid"] is True
        assert result["missing_files"] == []

    def test_validate_file_structure_missing_files(self):
        """Test validating file structure with missing files"""
        files = {
            "plugin.json": True,
            "README.md": False,  # Missing
            ".claude-plugin/": True,
            "agents/": False,     # Missing
            "skills/": True,
            "commands/": True
        }

        with patch("pathlib.Path.exists", side_effect=lambda x: files.get(str(x), False)):
            with patch("pathlib.Path.is_dir", side_effect=lambda x: str(x).endswith("/")):
                result = validate_file_structure("/test/plugin")

        assert result["valid"] is False
        assert "README.md" in result["missing_files"]
        assert "agents/" in result["missing_files"]

    @patch('simple_validation.validate_json_file')
    @patch('simple_validation.validate_python_syntax')
    @patch('simple_validation.validate_file_structure')
    def test_run_basic_validation_all_valid(self, mock_structure, mock_python, mock_json):
        """Test running basic validation with all files valid"""
        mock_json.return_value = {"valid": True, "errors": []}
        mock_python.return_value = {"valid": True, "errors": []}
        mock_structure.return_value = {"valid": True, "missing_files": []}

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.is_dir", return_value=True):
                result = run_basic_validation("/test/plugin")

        assert result["overall_valid"] is True
        assert result["total_errors"] == 0

    @patch('simple_validation.validate_json_file')
    @patch('simple_validation.validate_python_syntax')
    @patch('simple_validation.validate_file_structure')
    def test_run_basic_validation_with_errors(self, mock_structure, mock_python, mock_json):
        """Test running basic validation with errors"""
        mock_json.return_value = {"valid": False, "errors": ["JSON syntax error"]}
        mock_python.return_value = {"valid": False, "errors": ["Python syntax error"]}
        mock_structure.return_value = {"valid": False, "missing_files": ["README.md"]}

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.is_dir", return_value=True):
                result = run_basic_validation("/test/plugin")

        assert result["overall_valid"] is False
        assert result["total_errors"] == 3  # 2 syntax errors + 1 missing file

    def test_run_basic_validation_nonexistent_path(self):
        """Test running basic validation on nonexistent path"""
        with patch("pathlib.Path.exists", return_value=False):
            result = run_basic_validation("/nonexistent/path")

        assert result["overall_valid"] is False
        assert result["total_errors"] > 0


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="simple_validation module not available")
class TestSimpleValidationEdgeCases:
    """Test edge cases and error conditions"""

    def test_validate_json_file_with_read_error(self):
        """Test JSON validation with file read error"""
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_json_file("restricted.json")

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_python_syntax_with_encoding_error(self):
        """Test Python syntax validation with encoding issues"""
        with patch("builtins.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid byte")):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_python_syntax("encoding.py")

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_markdown_file_empty(self):
        """Test validating empty markdown file"""
        with patch("builtins.open", mock_open(read_data="")):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_markdown_file("empty.md")

        # Empty markdown is valid
        assert result["valid"] is True

    def test_validate_file_structure_empty_directory(self):
        """Test validating file structure on empty directory"""
        with patch("pathlib.Path.exists", return_value=False):
            with patch("pathlib.Path.is_dir", return_value=False):
                result = validate_file_structure("/empty/dir")

        assert result["valid"] is False
        assert len(result["missing_files"]) > 0