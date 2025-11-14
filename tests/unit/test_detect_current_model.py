"""
Tests for detect_current_model.py
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add lib to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

try:
    from detect_current_model import (
        detect_model_from_env,
        detect_model_from_process,
        get_current_model,
        detect_model_fallback
    )
    IMPORTS_AVAILABLE = True
except (ImportError, SyntaxError) as e:
    print(f"Warning: Could not import detect_current_model: {e}")
    IMPORTS_AVAILABLE = False


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="detect_current_model module not available")
class TestDetectCurrentModel:
    """Test cases for model detection functionality"""

    def test_detect_model_from_env_anthropic_model(self):
        """Test detection from ANTHROPIC_MODEL environment variable"""
        with patch.dict(os.environ, {"ANTHROPIC_MODEL": "claude-3-sonnet-20240229"}, clear=True):
            model, method = detect_model_from_env()
            assert model == "claude-3-sonnet-20240229"
            assert method == "env_anthropic_model"

    def test_detect_model_from_env_claude_model(self):
        """Test detection from CLAUDE_MODEL environment variable"""
        with patch.dict(os.environ, {"CLAUDE_MODEL": "claude-3-opus-20240229"}, clear=True):
            model, method = detect_model_from_env()
            assert model == "claude-3-opus-20240229"
            assert method == "env_claude_model"

    def test_detect_model_from_env_model_name(self):
        """Test detection from MODEL_NAME environment variable"""
        with patch.dict(os.environ, {"MODEL_NAME": "claude-3-haiku-20240307"}, clear=True):
            model, method = detect_model_from_env()
            assert model == "claude-3-haiku-20240307"
            assert method == "env_model_name"

    def test_detect_model_from_env_ai_model(self):
        """Test detection from AI_MODEL environment variable"""
        with patch.dict(os.environ, {"AI_MODEL": "claude-sonnet-4-5-20250929"}, clear=True):
            model, method = detect_model_from_env()
            assert model == "claude-sonnet-4-5-20250929"
            assert method == "env_ai_model"

    def test_detect_model_from_env_priority(self):
        """Test environment variable priority order"""
        # Set multiple env vars - should return the first one in priority order
        with patch.dict(os.environ, {
            "ANTHROPIC_MODEL": "claude-3-sonnet",
            "CLAUDE_MODEL": "claude-3-opus",
            "MODEL_NAME": "claude-3-haiku"
        }, clear=True):
            model, method = detect_model_from_env()
            assert model == "claude-3-sonnet"
            assert method == "env_anthropic_model"

    def test_detect_model_from_env_no_vars(self):
        """Test detection when no environment variables are set"""
        with patch.dict(os.environ, {}, clear=True):
            model, method = detect_model_from_env()
            assert model is None
            assert method is None

    def test_detect_model_from_env_empty_values(self):
        """Test detection when environment variables are empty strings"""
        with patch.dict(os.environ, {"ANTHROPIC_MODEL": "", "CLAUDE_MODEL": "valid_model"}, clear=True):
            model, method = detect_model_from_env()
            assert model == "valid_model"
            assert method == "env_claude_model"

    @patch('detect_current_model.psutil')
    def test_detect_model_from_process_with_psutil(self, mock_psutil):
        """Test detection from process information using psutil"""
        # Mock psutil process
        mock_process = MagicMock()
        mock_process.parent.return_value = MagicMock()
        mock_process.parent.return_value.cmdline.return_value = [
            "python", "-m", "claude", "--model", "claude-3-sonnet-20240229"
        ]
        mock_psutil.Process.return_value = mock_process

        model, method = detect_model_from_process()

        assert model is not None
        assert "process" in method.lower()

    @patch('detect_current_model.psutil')
    def test_detect_model_from_process_no_parent(self, mock_psutil):
        """Test detection when process has no parent"""
        mock_process = MagicMock()
        mock_process.parent.return_value = None
        mock_psutil.Process.return_value = mock_process

        model, method = detect_model_from_process()

        assert model is None or method is None

    @patch('detect_current_model.psutil')
    def test_detect_model_from_process_exception(self, mock_psutil):
        """Test detection when psutil raises exception"""
        mock_psutil.Process.side_effect = Exception("Process error")

        model, method = detect_model_from_process()

        assert model is None
        assert method is None

    @patch('detect_current_model.psutil')
    def test_detect_model_from_process_import_error(self, mock_psutil):
        """Test detection when psutil is not available"""
        with patch.dict('sys.modules', {'psutil': None}):
            # Force ImportError by removing psutil from modules
            import sys
            if 'psutil' in sys.modules:
                del sys.modules['psutil']

            model, method = detect_model_from_process()

            assert model is None
            assert method is None

    def test_get_current_model_integration(self):
        """Test get_current_model function with mocked dependencies"""
        with patch('detect_current_model.detect_model_from_env') as mock_env:
            with patch('detect_current_model.detect_model_from_process') as mock_process:
                with patch('detect_current_model.detect_model_fallback') as mock_fallback:

                    # Test environment detection works
                    mock_env.return_value = ("claude-3-sonnet", "env_anthropic_model")
                    mock_process.return_value = (None, None)
                    mock_fallback.return_value = (None, None)

                    result = get_current_model()
                    assert result == ("claude-3-sonnet", "env_anthropic_model")

                    # Test process detection as fallback
                    mock_env.return_value = (None, None)
                    mock_process.return_value = ("claude-3-opus", "process_cmdline")
                    mock_fallback.return_value = (None, None)

                    result = get_current_model()
                    assert result == ("claude-3-opus", "process_cmdline")

                    # Test fallback detection
                    mock_env.return_value = (None, None)
                    mock_process.return_value = (None, None)
                    mock_fallback.return_value = ("claude-3-haiku", "fallback_file")

                    result = get_current_model()
                    assert result == ("claude-3-haiku", "fallback_file")

                    # Test no detection
                    mock_env.return_value = (None, None)
                    mock_process.return_value = (None, None)
                    mock_fallback.return_value = (None, None)

                    result = get_current_model()
                    assert result == ("unknown", "none")

    @patch('builtins.open')
    @patch('os.path.exists')
    def test_detect_model_fallback_file_exists(self, mock_exists, mock_open):
        """Test fallback detection when marker file exists"""
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = "claude-sonnet-4-5-20250929"
        mock_open.return_value.__enter__.return_value = mock_file

        model, method = detect_model_fallback()

        assert model == "claude-sonnet-4-5-20250929"
        assert method == "fallback_file"

    @patch('os.path.exists')
    def test_detect_model_fallback_no_file(self, mock_exists):
        """Test fallback detection when marker file doesn't exist"""
        mock_exists.return_value = False

        model, method = detect_model_fallback()

        assert model is None
        assert method is None

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_detect_model_fallback_file_error(self, mock_open, mock_exists):
        """Test fallback detection when reading file fails"""
        mock_exists.return_value = True
        mock_open.side_effect = IOError("File read error")

        model, method = detect_model_fallback()

        assert model is None
        assert method is None


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="detect_current_model module not available")
class TestDetectCurrentModelEdgeCases:
    """Test edge cases and error conditions"""

    def test_environment_variable_values_with_spaces(self):
        """Test environment variables with spaces and special characters"""
        with patch.dict(os.environ, {"ANTHROPIC_MODEL": "claude-3-sonnet-20240229 (latest)"}, clear=True):
            model, method = detect_model_from_env()
            assert "claude-3-sonnet-20240229" in model

    def test_environment_variable_case_sensitivity(self):
        """Test that environment variable detection is case sensitive"""
        with patch.dict(os.environ, {"anthropic_model": "should-not-work"}, clear=True):
            model, method = detect_model_from_env()
            assert model is None

    def test_model_name_patterns(self):
        """Test various model name patterns"""
        test_models = [
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229",
            "claude-3-haiku-20240307",
            "claude-sonnet-4-5-20250929"
        ]

        for model in test_models:
            with patch.dict(os.environ, {"ANTHROPIC_MODEL": model}, clear=True):
                detected_model, method = detect_model_from_env()
                assert detected_model == model
                assert method == "env_anthropic_model"

    def test_empty_string_detection_methods(self):
        """Test detection methods return appropriate values for empty inputs"""
        # Test with empty environment
        with patch.dict(os.environ, {}, clear=True):
            model, method = detect_model_from_env()
            assert model is None
            assert method is None