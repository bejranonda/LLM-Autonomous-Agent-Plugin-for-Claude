"""
Unit tests for Plugin Path Resolver

Tests the plugin discovery and path resolution functionality including:
- Cross-platform plugin path detection
- Development vs marketplace installation handling
- Environment variable support
- Path validation and script resolution
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add lib directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from plugin_path_resolver import (
    get_plugin_path, get_script_path, get_lib_path,
    validate_plugin_installation, get_python_executable
)


class TestPluginPathResolver:
    """Test suite for Plugin Path Resolver functions"""

    @pytest.fixture
    def mock_plugin_structure(self, temp_directory):
        """Create a mock plugin directory structure"""
        plugin_dir = Path(temp_directory) / "test_plugin"
        plugin_dir.mkdir()

        # Create .claude-plugin directory
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()

        # Create plugin.json
        plugin_json = claude_plugin_dir / "plugin.json"
        plugin_json.write_text('{"name": "Test Plugin", "version": "1.0.0"}')

        # Create lib directory with test scripts
        lib_dir = plugin_dir / "lib"
        lib_dir.mkdir()

        test_script = lib_dir / "test_script.py"
        test_script.write_text("# Test script")

        return plugin_dir

    @pytest.fixture
    def mock_marketplace_structure(self, temp_directory):
        """Create a mock marketplace plugin structure"""
        home = Path(temp_directory) / "home"
        home.mkdir()

        marketplace_name = "LLM-Autonomous-Agent-Plugin-for-Claude"
        marketplace_dir = home / ".claude" / "plugins" / "marketplaces" / marketplace_name
        marketplace_dir.mkdir(parents=True)

        # Create plugin.json
        claude_plugin_dir = marketplace_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()

        plugin_json = claude_plugin_dir / "plugin.json"
        plugin_json.write_text('{"name": "Marketplace Plugin", "version": "1.0.0"}')

        # Create lib directory
        lib_dir = marketplace_dir / "lib"
        lib_dir.mkdir()

        test_script = lib_dir / "dashboard.py"
        test_script.write_text("# Dashboard script")

        return marketplace_dir, home

    @pytest.mark.unit
    @pytest.mark.cross_platform
    def test_get_plugin_path_development_mode(self, mock_plugin_structure):
        """Test plugin path detection in development mode"""
        with patch('pathlib.Path.cwd', return_value=mock_plugin_structure):
            plugin_path = get_plugin_path()

        assert plugin_path is not None
        assert plugin_path == mock_plugin_structure

    @pytest.mark.unit
    def test_get_plugin_path_from_subdirectory(self, mock_plugin_structure):
        """Test plugin path detection from within subdirectory"""
        # Change to lib subdirectory
        lib_dir = mock_plugin_structure / "lib"
        with patch('pathlib.Path.cwd', return_value=lib_dir):
            plugin_path = get_plugin_path()

        assert plugin_path is not None
        assert plugin_path == mock_plugin_structure

    @pytest.mark.unit
    def test_get_plugin_path_environment_variable(self, mock_plugin_structure):
        """Test plugin path detection via environment variable"""
        env_path = str(mock_plugin_structure)
        with patch.dict(os.environ, {'CLAUDE_PLUGIN_PATH': env_path}):
            with patch('pathlib.Path.cwd', return_value=Path('/tmp')):
                plugin_path = get_plugin_path()

        assert plugin_path is not None
        assert str(plugin_path) == env_path

    @pytest.mark.unit
    @pytest.mark.parametrize("platform", ["win32", "linux", "darwin"])
    def test_get_plugin_path_standard_locations(self, platform, mock_marketplace_structure):
        """Test plugin path detection in standard locations"""
        marketplace_dir, home = mock_marketplace_structure

        with patch('sys.platform', platform), \
             patch('pathlib.Path.home', return_value=home), \
             patch('pathlib.Path.cwd', return_value=Path('/tmp')):
            plugin_path = get_plugin_path()

        assert plugin_path is not None
        assert plugin_path == marketplace_dir

    @pytest.mark.unit
    def test_get_plugin_path_windows_specific_paths(self, mock_plugin_structure):
        """Test Windows-specific plugin paths"""
        with patch('sys.platform', 'win32'), \
             patch.dict(os.environ, {
                 'APPDATA': str(mock_plugin_structure / 'appdata'),
                 'LOCALAPPDATA': str(mock_plugin_structure / 'localappdata'),
                 'PROGRAMFILES': str(mock_plugin_structure / 'programfiles')
             }):
            # Create plugin.json in each location
            for env_var in ['APPDATA', 'LOCALAPPDATA', 'PROGRAMFILES']:
                base_path = Path(os.environ[env_var.lower()])
                plugin_path = base_path / "Claude" / "plugins" / "autonomous-agent"
                plugin_path.mkdir(parents=True)

                claude_plugin_dir = plugin_path / ".claude-plugin"
                claude_plugin_dir.mkdir()
                (claude_plugin_dir / "plugin.json").write_text('{"name": "Windows Plugin"}')

            with patch('pathlib.Path.cwd', return_value=Path('/tmp')):
                found_path = get_plugin_path()
                assert found_path is not None

    @pytest.mark.unit
    def test_get_plugin_path_not_found(self):
        """Test when plugin path is not found"""
        with patch('pathlib.Path.cwd', return_value=Path('/nonexistent')):
            with patch('pathlib.Path.home', return_value=Path('/tmp')):
                plugin_path = get_plugin_path()

        assert plugin_path is None

    @pytest.mark.unit
    def test_get_script_path_success(self, mock_plugin_structure):
        """Test successful script path resolution"""
        with patch('plugin_path_resolver.get_plugin_path', return_value=mock_plugin_structure):
            script_path = get_script_path("test_script.py")

        assert script_path is not None
        assert script_path.name == "test_script.py"
        assert script_path.parent.name == "lib"

    @pytest.mark.unit
    def test_get_script_path_not_found(self, mock_plugin_structure):
        """Test script path resolution when script doesn't exist"""
        with patch('plugin_path_resolver.get_plugin_path', return_value=mock_plugin_structure):
            script_path = get_script_path("nonexistent_script.py")

        assert script_path is None

    @pytest.mark.unit
    def test_get_script_path_no_plugin(self):
        """Test script path resolution when plugin not found"""
        with patch('plugin_path_resolver.get_plugin_path', return_value=None):
            script_path = get_script_path("test_script.py")

        assert script_path is None

    @pytest.mark.unit
    def test_get_lib_path_success(self, mock_plugin_structure):
        """Test successful lib directory path resolution"""
        with patch('plugin_path_resolver.get_plugin_path', return_value=mock_plugin_structure):
            lib_path = get_lib_path()

        assert lib_path is not None
        assert lib_path.name == "lib"
        assert lib_path.exists()

    @pytest.mark.unit
    def test_get_lib_path_not_found(self):
        """Test lib directory resolution when it doesn't exist"""
        # Create plugin without lib directory
        plugin_dir = Path(tempfile.mkdtemp())
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()
        (claude_plugin_dir / "plugin.json").write_text('{"name": "Test Plugin"}')

        try:
            with patch('plugin_path_resolver.get_plugin_path', return_value=plugin_dir):
                lib_path = get_lib_path()

            assert lib_path is None
        finally:
            shutil.rmtree(plugin_dir)

    @pytest.mark.unit
    def test_validate_plugin_installation_success(self, mock_plugin_structure):
        """Test successful plugin installation validation"""
        # Create additional required files
        lib_dir = mock_plugin_structure / "lib"
        (lib_dir / "dashboard.py").write_text("# Dashboard")
        (lib_dir / "pattern_storage.py").write_text("# Pattern storage")

        validation = validate_plugin_installation()

        assert validation["valid"] is True
        assert validation["plugin_path"] is not None
        assert validation["lib_path"] is not None
        assert validation["plugin_json"] is not None

        # Check all essential files exist
        checks = validation["checks"]
        assert checks["plugin_json_exists"] is True
        assert checks["lib_directory_exists"] is True
        assert checks["dashboard_py_exists"] is True
        assert checks["pattern_storage_py_exists"] is True

    @pytest.mark.unit
    def test_validate_plugin_installation_missing_files(self, temp_directory):
        """Test validation with missing essential files"""
        # Create incomplete plugin structure
        plugin_dir = Path(temp_directory) / "incomplete_plugin"
        plugin_dir.mkdir()

        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()

        # Only create plugin.json, missing lib directory
        (claude_plugin_dir / "plugin.json").write_text('{"name": "Incomplete Plugin"}')

        with patch('plugin_path_resolver.get_plugin_path', return_value=plugin_dir):
            validation = validate_plugin_installation()

        assert validation["valid"] is False
        assert validation["lib_path"] is None
        assert "lib_directory_exists" not in validation["checks"] or not validation["checks"]["lib_directory_exists"]

    @pytest.mark.unit
    def test_validate_plugin_installation_not_found(self):
        """Test validation when plugin installation not found"""
        with patch('plugin_path_resolver.get_plugin_path', return_value=None):
            validation = validate_plugin_installation()

        assert validation["valid"] is False
        assert validation["error"] == "Plugin installation not found"
        assert validation["plugin_path"] is None
        assert validation["lib_path"] is None
        assert validation["plugin_json"] is None

    @pytest.mark.unit
    def test_get_python_executable(self):
        """Test Python executable detection"""
        python_exe = get_python_executable()

        assert python_exe is not None
        assert Path(python_exe).exists()

        # Should match current Python interpreter
        assert python_exe == sys.executable

    @pytest.mark.unit
    def test_path_search_priority(self, mock_plugin_structure):
        """Test that path search follows correct priority order"""
        # Test 1: Current directory takes priority
        with patch('pathlib.Path.cwd', return_value=mock_plugin_structure), \
             patch.dict(os.environ, {'CLAUDE_PLUGIN_PATH': '/tmp/fake'}):
            plugin_path = get_plugin_path()
            assert plugin_path == mock_plugin_structure

        # Test 2: Environment variable used if current dir doesn't have plugin
        with patch('pathlib.Path.cwd', return_value=Path('/tmp')), \
             patch.dict(os.environ, {'CLAUDE_PLUGIN_PATH': str(mock_plugin_structure)}):
            plugin_path = get_plugin_path()
            assert plugin_path == mock_plugin_structure

    @pytest.mark.unit
    def test_multiple_plugins_found(self, temp_directory):
        """Test handling when multiple plugin installations are found"""
        # Create two plugin installations
        plugin1 = Path(temp_directory) / "plugin1"
        plugin2 = Path(temp_directory) / "plugin2"

        for plugin_dir in [plugin1, plugin2]:
            plugin_dir.mkdir()
            claude_plugin_dir = plugin_dir / ".claude-plugin"
            claude_plugin_dir.mkdir()
            (claude_plugin_dir / "plugin.json").write_text('{"name": "Test Plugin"}')

        # Should return the first one found based on search order
        with patch('pathlib.Path.cwd', return_value=plugin1):
            found_path = get_plugin_path()
            assert found_path == plugin1

        with patch('pathlib.Path.cwd', return_value=plugin2):
            found_path = get_plugin_path()
            assert found_path == plugin2

    @pytest.mark.unit
    @pytest.mark.parametrize("script_name", [
        "dashboard.py",
        "pattern_storage.py",
        "learning_analytics.py",
        "quality_tracker.py",
        "test_script.py"
    ])
    def test_get_script_path_various_scripts(self, mock_plugin_structure, script_name):
        """Test script path resolution for various script names"""
        # Create the script file
        script_file = mock_plugin_structure / "lib" / script_name
        script_file.write_text(f"# {script_name}")

        with patch('plugin_path_resolver.get_plugin_path', return_value=mock_plugin_structure):
            found_path = get_script_path(script_name)

        assert found_path is not None
        assert found_path.name == script_name

    @pytest.mark.unit
    def test_edge_case_empty_script_name(self, mock_plugin_structure):
        """Test edge case with empty script name"""
        with patch('plugin_path_resolver.get_plugin_path', return_value=mock_plugin_structure):
            script_path = get_script_path("")

        assert script_path is None

    @pytest.mark.unit
    def test_edge_case_script_name_with_path(self, mock_plugin_structure):
        """Test script name with path separators"""
        with patch('plugin_path_resolver.get_plugin_path', return_value=mock_plugin_structure):
            # Should handle path separators gracefully
            script_path = get_script_path("subdir/script.py")

        assert script_path is None  # Script doesn't exist

    @pytest.mark.unit
    def test_file_permission_handling(self, temp_directory):
        """Test handling of files with permission issues"""
        plugin_dir = Path(temp_directory) / "restricted_plugin"
        plugin_dir.mkdir()

        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()

        plugin_json = claude_plugin_dir / "plugin.json"
        plugin_json.write_text('{"name": "Restricted Plugin"}')

        # Mock permission error when checking file existence
        with patch('pathlib.Path.exists', side_effect=PermissionError("Permission denied")):
            with patch('plugin_path_resolver.get_plugin_path', return_value=plugin_dir):
                script_path = get_script_path("test.py")

        assert script_path is None

    @pytest.mark.unit
    def test_symbolic_link_handling(self, temp_directory):
        """Test handling of symbolic links (where supported)"""
        plugin_dir = Path(temp_directory) / "real_plugin"
        plugin_dir.mkdir()

        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()
        (claude_plugin_dir / "plugin.json").write_text('{"name": "Real Plugin"}')

        lib_dir = plugin_dir / "lib"
        lib_dir.mkdir()

        test_script = lib_dir / "test.py"
        test_script.write_text("# Test script")

        # Create symbolic link if supported
        try:
            link_dir = Path(temp_directory) / "linked_plugin"
            if hasattr(os, 'symlink'):
                os.symlink(plugin_dir, link_dir)

                with patch('plugin_path_resolver.get_plugin_path', return_value=link_dir):
                    script_path = get_script_path("test.py")

                assert script_path is not None
                assert script_path.exists()
            else:
                # Skip symbolic link test on Windows without admin rights
                pytest.skip("Symbolic links not supported")
        except (OSError, NotImplementedError):
            pytest.skip("Cannot create symbolic link")

    @pytest.mark.unit
    def test_case_sensitivity(self, mock_plugin_structure, mock_platform):
        """Test case sensitivity handling across platforms"""
        # Create script with mixed case
        script_path = mock_plugin_structure / "lib" / "Test_Script.py"
        script_path.write_text("# Test script")

        with patch('plugin_path_resolver.get_plugin_path', return_value=mock_plugin_structure):
            # Test exact match
            found_path = get_script_path("Test_Script.py")
            if mock_platform in ["Linux", "Darwin"]:  # Case sensitive
                assert found_path is not None
                assert found_path.name == "Test_Script.py"

            # Test case insensitive search
            found_path_lower = get_script_path("test_script.py")
            if mock_platform == "Windows":  # Case insensitive
                assert found_path_lower is not None

    @pytest.mark.unit
    def test_path_with_spaces(self, temp_directory):
        """Test handling of paths with spaces"""
        plugin_dir = Path(temp_directory) / "plugin with spaces"
        plugin_dir.mkdir()

        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()
        (claude_plugin_dir / "plugin.json").write_text('{"name": "Plugin with spaces"}')

        lib_dir = plugin_dir / "lib"
        lib_dir.mkdir()

        test_script = lib_dir / "test script.py"
        test_script.write_text("# Test script with spaces")

        with patch('plugin_path_resolver.get_plugin_path', return_value=plugin_dir):
            found_path = get_script_path("test script.py")

        assert found_path is not None
        assert " " in str(found_path)

    @pytest.mark.unit
    def test_unicode_paths(self, temp_directory):
        """Test handling of Unicode characters in paths"""
        plugin_name = "têst_plûgîn_ñoñ_ãscii"
        plugin_dir = Path(temp_directory) / plugin_name
        plugin_dir.mkdir()

        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()
        (claude_plugin_dir / "plugin.json").write_text('{"name": "Unicode Plugin"}')

        with patch('plugin_path_resolver.get_plugin_path', return_value=plugin_dir):
            validation = validate_plugin_installation()

        assert validation["valid"] is True
        assert plugin_name in str(validation["plugin_path"])