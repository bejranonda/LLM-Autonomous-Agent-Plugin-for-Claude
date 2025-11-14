"""
Tests for dashboard_validator.py
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
    from dashboard_validator import (
        validate_dashboard_compatibility,
        validate_dashboard_imports,
        validate_dashboard_dependencies,
        check_dashboard_health,
        validate_dashboard_routes,
        DashboardValidationError
    )
    IMPORTS_AVAILABLE = True
except (ImportError, SyntaxError) as e:
    print(f"Warning: Could not import dashboard_validator: {e}")
    IMPORTS_AVAILABLE = False


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="dashboard_validator module not available")
class TestDashboardValidator:
    """Test cases for dashboard validation functionality"""

    def test_validate_dashboard_compatible_version(self):
        """Test validating compatible dashboard version"""
        dashboard_code = '''
# Dashboard v7.7.0 - Compatible with current plugin
import json
from pathlib import Path

def main():
    """Main dashboard function"""
    pass
'''

        with patch("builtins.open", mock_open(read_data=dashboard_code)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_dashboard_compatibility("dashboard.py")

        assert result["compatible"] is True
        assert len(result["issues"]) == 0

    def test_validate_dashboard_outdated_version(self):
        """Test validating outdated dashboard version"""
        dashboard_code = '''
# Dashboard v5.0.0 - Outdated version
import json

def main():
    """Old dashboard function"""
    pass
'''

        with patch("builtins.open", mock_open(read_data=dashboard_code)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_dashboard_compatibility("dashboard.py")

        assert result["compatible"] is False
        assert len(result["issues"]) > 0
        assert any("version" in issue.lower() for issue in result["issues"])

    def test_validate_dashboard_imports_valid(self):
        """Test validating dashboard with valid imports"""
        dashboard_code = '''
import json
import os
from pathlib import Path
from datetime import datetime
import streamlit as st

def validate_imports():
    """Function with valid imports"""
    return True
'''

        with patch("builtins.open", mock_open(read_data=dashboard_code)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_dashboard_imports("dashboard.py")

        assert result["valid"] is True
        assert len(result["missing_imports"]) == 0

    def test_validate_dashboard_imports_missing(self):
        """Test validating dashboard with missing imports"""
        dashboard_code = '''
import json
from pathlib import Path

def missing_imports_function():
    # These imports are used but not imported
    return os.path.exists("/tmp") and datetime.now()
'''

        with patch("builtins.open", mock_open(read_data=dashboard_code)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_dashboard_imports("dashboard.py")

        assert result["valid"] is False
        assert "os" in result["missing_imports"]
        assert "datetime" in result["missing_imports"]

    def test_validate_dashboard_dependencies_available(self):
        """Test validating dashboard when all dependencies are available"""
        with patch("importlib.util.find_spec") as mock_find_spec:
            # Mock that all required modules are available
            mock_find_spec.return_value = True

            dependencies = ["streamlit", "pandas", "plotly", "pathlib"]
            result = validate_dashboard_dependencies(dependencies)

        assert result["all_available"] is True
        assert len(result["missing"]) == 0

    def test_validate_dashboard_dependencies_missing(self):
        """Test validating dashboard when some dependencies are missing"""
        with patch("importlib.util.find_spec") as mock_find_spec:
            # Mock that some modules are missing
            def side_effect(module):
                return module in ["pandas", "pathlib"]  # Only these are available

            mock_find_spec.side_effect = side_effect

            dependencies = ["streamlit", "pandas", "plotly", "pathlib"]
            result = validate_dashboard_dependencies(dependencies)

        assert result["all_available"] is False
        assert "streamlit" in result["missing"]
        assert "plotly" in result["missing"]
        assert "pandas" not in result["missing"]
        assert "pathlib" not in result["missing"]

    def test_check_dashboard_health_healthy(self):
        """Test dashboard health check for healthy dashboard"""
        health_checks = {
            "file_exists": True,
            "imports_valid": True,
            "dependencies_available": True,
            "syntax_valid": True,
            "version_compatible": True
        }

        with patch("dashboard_validator.validate_dashboard_imports", return_value={"valid": True}):
            with patch("dashboard_validator.validate_dashboard_dependencies", return_value={"all_available": True}):
                with patch("dashboard_validator.validate_dashboard_compatibility", return_value={"compatible": True}):
                    with patch("pathlib.Path.exists", return_value=True):
                        result = check_dashboard_health("dashboard.py")

        assert result["healthy"] is True
        assert result["overall_score"] >= 80

    def test_check_dashboard_health_unhealthy(self):
        """Test dashboard health check for unhealthy dashboard"""
        with patch("dashboard_validator.validate_dashboard_imports", return_value={"valid": False}):
            with patch("dashboard_validator.validate_dashboard_dependencies", return_value={"all_available": False}):
                with patch("dashboard_validator.validate_dashboard_compatibility", return_value={"compatible": False}):
                    with patch("pathlib.Path.exists", return_value=False):
                        result = check_dashboard_health("dashboard.py")

        assert result["healthy"] is False
        assert result["overall_score"] < 50

    def test_validate_dashboard_routes_valid(self):
        """Test validating dashboard with valid routes"""
        dashboard_code = '''
@st.route("/dashboard")
def dashboard_page():
    """Main dashboard page"""
    return "Dashboard"

@st.route("/metrics")
def metrics_page():
    """Metrics page"""
    return "Metrics"

@st.route("/analytics")
def analytics_page():
    """Analytics page"""
    return "Analytics"
'''

        with patch("builtins.open", mock_open(read_data=dashboard_code)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_dashboard_routes("dashboard.py")

        assert result["valid"] is True
        assert len(result["routes"]) >= 3
        assert "/dashboard" in [r["path"] for r in result["routes"]]

    def test_validate_dashboard_routes_duplicate_paths(self):
        """Test validating dashboard with duplicate route paths"""
        dashboard_code = '''
@st.route("/dashboard")
def dashboard_page():
    return "Dashboard 1"

@st.route("/dashboard")
def dashboard_page_duplicate():
    return "Dashboard 2"
'''

        with patch("builtins.open", mock_open(read_data=dashboard_code)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_dashboard_routes("dashboard.py")

        assert result["valid"] is False
        assert any("duplicate" in issue.lower() for issue in result["issues"])

    def test_validate_dashboard_routes_missing_handlers(self):
        """Test validating dashboard with routes missing handlers"""
        dashboard_code = '''
# Route decorator without function
@st.route("/incomplete")

@st.route("/another")
# Missing function definition here
'''

        with patch("builtins.open", mock_open(read_data=dashboard_code)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_dashboard_routes("dashboard.py")

        assert result["valid"] is False
        assert any("handler" in issue.lower() for issue in result["issues"])

    def test_dashboard_validation_error_custom(self):
        """Test custom DashboardValidationError exception"""
        error = DashboardValidationError(
            "Dashboard validation failed",
            component="routes",
            severity="error"
        )

        assert str(error) == "Dashboard validation failed"
        assert error.component == "routes"
        assert error.severity == "error"


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="dashboard_validator module not available")
class TestDashboardValidatorEdgeCases:
    """Test edge cases and error conditions"""

    def test_validate_nonexistent_dashboard(self):
        """Test validating non-existent dashboard file"""
        with patch("pathlib.Path.exists", return_value=False):
            result = validate_dashboard_compatibility("nonexistent.py")

        assert result["compatible"] is False
        assert len(result["issues"]) > 0

    def test_validate_dashboard_read_error(self):
        """Test dashboard validation with file read error"""
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_dashboard_imports("restricted.py")

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_empty_dashboard(self):
        """Test validating empty dashboard file"""
        with patch("builtins.open", mock_open(read_data="")):
            with patch("pathlib.Path.exists", return_value=True):
                compatibility = validate_dashboard_compatibility("empty.py")
                imports = validate_dashboard_imports("empty.py")
                routes = validate_dashboard_routes("empty.py")

        assert compatibility["compatible"] is False
        assert imports["valid"] is False
        assert routes["valid"] is False

    def test_validate_dashboard_with_syntax_errors(self):
        """Test validating dashboard with syntax errors"""
        dashboard_with_syntax_error = '''
import streamlit as st

def broken_function(
    # Missing closing parenthesis and colon
    print("This has syntax errors")
'''

        with patch("builtins.open", mock_open(read_data=dashboard_with_syntax_error)):
            with patch("pathlib.Path.exists", return_value=True):
                result = validate_dashboard_imports("broken.py")

        assert result["valid"] is False
        assert any("syntax" in error.lower() for error in result["errors"])

    def test_check_dashboard_health_missing_file(self):
        """Test health check when dashboard file doesn't exist"""
        with patch("pathlib.Path.exists", return_value=False):
            result = check_dashboard_health("nonexistent.py")

        assert result["healthy"] is False
        assert result["overall_score"] == 0

    def test_validate_dashboard_dependencies_empty_list(self):
        """Test dependencies validation with empty list"""
        result = validate_dashboard_dependencies([])

        assert result["all_available"] is True
        assert len(result["missing"]) == 0
        assert len(result["available"]) == 0