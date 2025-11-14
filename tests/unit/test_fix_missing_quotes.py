"""
Tests for fix_missing_quotes.py utility
"""

import pytest
from unittest.mock import patch, mock_open
import tempfile
import os
from pathlib import Path
import sys

# Add lib to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from fix_missing_quotes import fix_missing_quotes


class TestFixMissingQuotes:
    """Test cases for fix_missing_quotes function"""

    def test_fix_version_with_quotes(self):
        """Test fixing version number without quotes"""
        content = "{\n    version: 2.0.0,\n    name: test\n}"
        expected = '{\n    "version": 2.0.0,\n    name: test\n}'

        with patch("builtins.open", mock_open(read_data=content)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = fix_missing_quotes("test.py")

        # Check file was written
        mock_file.assert_called()
        handle = mock_file.return_value.__enter__.return_value
        written_data = ''.join(call[0][0] for call in handle.write.call_args_list)
        assert '"version": 2.0.0' in written_data

    def test_fix_project_type_with_quotes(self):
        """Test fixing project_type without quotes"""
        content = "{\n    project_type: ai-plugin,\n    team_size: small\n}"

        with patch("builtins.open", mock_open(read_data=content)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = fix_missing_quotes("test.py")

        handle = mock_file.return_value.__enter__.return_value
        written_data = ''.join(call[0][0] for call in handle.write.call_args_list)
        assert '"project_type": "ai-plugin"' in written_data

    def test_fix_team_size_with_quotes(self):
        """Test fixing team_size without quotes"""
        content = "{\n    team_size: medium,\n    framework: fastapi\n}"

        with patch("builtins.open", mock_open(read_data=content)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = fix_missing_quotes("test.py")

        handle = mock_file.return_value.__enter__.return_value
        written_data = ''.join(call[0][0] for call in handle.write.call_args_list)
        assert '"team_size": "medium"' in written_data

    def test_fix_ferror_statements(self):
        """Test fixing fERROR statements"""
        content = 'print(fERROR storing data: {e})'
        expected = 'print(f"ERROR storing data: {e}")'

        with patch("builtins.open", mock_open(read_data=content)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = fix_missing_quotes("test.py")

        handle = mock_file.return_value.__enter__.return_value
        written_data = ''.join(call[0][0] for call in handle.write.call_args_list)
        assert 'f"ERROR storing data:' in written_data

    def test_fix_missing_brackets(self):
        """Test fixing missing closing brackets"""
        content = 'self.current_task = {\n'

        with patch("builtins.open", mock_open(read_data=content)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = fix_missing_quotes("test.py")

        handle = mock_file.return_value.__enter__.return_value
        written_data = ''.join(call[0][0] for call in handle.write.call_args_list)
        assert 'self.current_task = {}' in written_data

    def test_no_changes_needed(self):
        """Test when no changes are needed"""
        content = '{"version": "2.0.0", "project_type": "ai-plugin"}'

        with patch("builtins.open", mock_open(read_data=content)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = fix_missing_quotes("test.py")

        # Should not write if no changes
        handle = mock_file.return_value.__enter__.return_value
        assert not handle.write.called
        assert result is False

    def test_file_error_handling(self):
        """Test error handling when file doesn't exist or can't be read"""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            result = fix_missing_quotes("nonexistent.py")
            assert result is False

    def test_file_permission_error(self):
        """Test error handling when file has permission issues"""
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            result = fix_missing_quotes("restricted.py")
            assert result is False

    @patch('lib.fix_missing_quotes.Path')
    def test_main_function_critical_files(self, mock_path):
        """Test main function processes critical files"""
        # Mock Path and directory structure
        mock_lib_dir = mock_path.return_value
        mock_lib_dir.__truediv__.return_value.exists.return_value = True

        # Mock file contents
        file_contents = {
            "auto_learning_trigger.py": "{version: 1.0.0}",
            "assessment_storage.py": "{project_type: ai-plugin}",
            "task_queue.py": "{team_size: small}",
            "backup_manager.py": "{framework: fastapi}",
        }

        def mock_open_side_effect(filename, mode='r', encoding='utf-8'):
            if 'r' in mode:
                filename_str = str(filename)
                for key, content in file_contents.items():
                    if key in filename_str:
                        return mock_open(read_data=content)()
            return mock_open()()

        with patch("builtins.open", side_effect=mock_open_side_effect):
            with patch('builtins.print') as mock_print:
                # Import and run main
                from fix_missing_quotes import main
                main()

        # Check that print was called for each file
        assert mock_print.call_count >= 5  # At least 4 files + summary

    def test_multiple_patterns_in_one_file(self):
        """Test multiple patterns in the same file"""
        content = """
{
    version: 2.0.0,
    project_type: ai-plugin,
    team_size: medium,
    development_stage: production
}
"""

        with patch("builtins.open", mock_open(read_data=content)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = fix_missing_quotes("test.py")

        handle = mock_file.return_value.__enter__.return_value
        written_data = ''.join(call[0][0] for call in handle.write.call_args_list)

        # Check all patterns were fixed
        assert '"version": 2.0.0' in written_data
        assert '"project_type": "ai-plugin"' in written_data
        assert '"team_size": "medium"' in written_data
        assert '"development_stage": "production"' in written_data