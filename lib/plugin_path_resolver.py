#!/usr/bin/env python3
"""
Plugin Path Resolver for Autonomous Agent

This module provides utilities to resolve paths to Python scripts
within the plugin installation directory, regardless of whether
the plugin is running in development mode or installed from marketplace.

Usage:
    from plugin_path_resolver import get_plugin_path, get_script_path

    script_path = get_script_path("dashboard.py")
    # Returns: /home/user/.config/claude/plugins/autonomous-agent/lib/dashboard.py

    plugin_path = get_plugin_path()
    # Returns: /home/user/.config/claude/plugins/autonomous-agent/
"""

import os
import sys
from pathlib import Path
from typing import Optional


def get_plugin_path() -> Optional[Path]:
    """
    Get the plugin installation directory path.

    Returns:
        Path to plugin root directory or None if not found
    """
    # First, try to find plugin.json in current directory and parents
    current = Path.cwd()

    # Check if we're in development mode (plugin.json in .claude-plugin/)
    for parent in [current] + list(current.parents):
        plugin_json = parent / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            return parent

    # Check if we're running from within the plugin (agents/ or commands/ dir)
    for parent in [current] + list(current.parents):
        if parent.name in ["agents", "commands", "skills", "lib"]:
            plugin_json = parent / ".claude-plugin" / "plugin.json"
            if plugin_json.exists():
                return parent
        # Also check if we're in lib directory itself
        elif parent.name == "lib":
            plugin_dir = parent.parent
            plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
            if plugin_json.exists():
                return plugin_dir

    # Try environment variable
    if "CLAUDE_PLUGIN_PATH" in os.environ:
        plugin_path = Path(os.environ["CLAUDE_PLUGIN_PATH"])
        if (plugin_path / ".claude-plugin" / "plugin.json").exists():
            return plugin_path

    # Try standard plugin locations
    home = Path.home()

    # Marketplace plugin name
    marketplace_plugin_name = "LLM-Autonomous-Agent-Plugin-for-Claude"

    plugin_locations = [
        # Development/local installations
        home / ".config" / "claude" / "plugins" / "autonomous-agent",
        home / ".claude" / "plugins" / "autonomous-agent",

        # Marketplace installations (primary)
        home / ".claude" / "plugins" / "marketplaces" / marketplace_plugin_name,
        home / ".config" / "claude" / "plugins" / "marketplaces" / marketplace_plugin_name,

        # Alternative marketplace paths
        home / ".claude" / "plugins" / "marketplace" / marketplace_plugin_name,
        home / ".config" / "claude" / "plugins" / "marketplace" / marketplace_plugin_name,

        # System-wide installations (Linux/Mac)
        Path("/usr/local/share/claude/plugins/autonomous-agent"),
        Path("/usr/local/share/claude/plugins/marketplaces") / marketplace_plugin_name,
        Path("/opt/claude/plugins/autonomous-agent"),
        Path("/opt/claude/plugins/marketplaces") / marketplace_plugin_name,
    ]

    # Windows-specific paths (using environment variables, not hardcoded)
    if sys.platform == "win32":
        appdata = Path(os.environ.get("APPDATA", ""))
        localappdata = Path(os.environ.get("LOCALAPPDATA", ""))
        programfiles = Path(os.environ.get("PROGRAMFILES", ""))

        if appdata:
            plugin_locations.extend([
                appdata / "Claude" / "plugins" / "autonomous-agent",
                appdata / "Claude" / "plugins" / "marketplaces" / marketplace_plugin_name,
            ])

        if localappdata:
            plugin_locations.extend([
                localappdata / "Claude" / "plugins" / "autonomous-agent",
                localappdata / "Claude" / "plugins" / "marketplaces" / marketplace_plugin_name,
            ])

        if programfiles:
            plugin_locations.extend([
                programfiles / "Claude" / "plugins" / "autonomous-agent",
                programfiles / "Claude" / "plugins" / "marketplaces" / marketplace_plugin_name,
            ])

    for location in plugin_locations:
        if location and (location / ".claude-plugin" / "plugin.json").exists():
            return location

    return None


def get_script_path(script_name: str) -> Optional[Path]:
    """
    Get the full path to a Python script in the plugin's lib directory.

    Args:
        script_name: Name of the script file (e.g., "dashboard.py")

    Returns:
        Full path to the script or None if not found
    """
    plugin_path = get_plugin_path()
    if not plugin_path:
        return None

    script_path = plugin_path / "lib" / script_name
    if script_path.exists():
        return script_path

    return None


def get_lib_path() -> Optional[Path]:
    """
    Get the plugin's lib directory path.

    Returns:
        Path to lib directory or None if not found
    """
    plugin_path = get_plugin_path()
    if not plugin_path:
        return None

    lib_path = plugin_path / "lib"
    if lib_path.exists():
        return lib_path

    return None


def validate_plugin_installation() -> dict:
    """
    Validate the plugin installation and return status.

    Returns:
        Dictionary with validation results
    """
    plugin_path = get_plugin_path()

    if not plugin_path:
        return {
            "valid": False,
            "error": "Plugin installation not found",
            "plugin_path": None,
            "lib_path": None,
            "plugin_json": None
        }

    plugin_json = plugin_path / ".claude-plugin" / "plugin.json"
    lib_path = plugin_path / "lib"

    # Check essential files
    checks = {
        "plugin_json_exists": plugin_json.exists(),
        "lib_directory_exists": lib_path.exists(),
        "dashboard_py_exists": (lib_path / "dashboard.py").exists(),
        "pattern_storage_py_exists": (lib_path / "pattern_storage.py").exists(),
    }

    return {
        "valid": all(checks.values()),
        "plugin_path": str(plugin_path),
        "lib_path": str(lib_path) if lib_path.exists() else None,
        "plugin_json": str(plugin_json) if plugin_json.exists() else None,
        "checks": checks
    }


def get_python_executable() -> str:
    """
    Get the appropriate Python executable for the current platform.

    Returns:
        Path to Python executable
    """
    # Use the same Python that's running this script
    return sys.executable


if __name__ == "__main__":
    # Test the resolver
    print("Plugin Path Resolver Test")
    print("=" * 40)

    # Test plugin path detection
    plugin_path = get_plugin_path()
    print(f"Plugin Path: {plugin_path}")

    # Test script path resolution
    test_scripts = ["dashboard.py", "pattern_storage.py", "learning_analytics.py"]
    for script in test_scripts:
        script_path = get_script_path(script)
        print(f"{script}: {script_path}")

    # Validate installation
    validation = validate_plugin_installation()
    print(f"\nInstallation Valid: {validation['valid']}")
    if not validation['valid']:
        print(f"Error: {validation.get('error', 'Unknown error')}")

    print(f"\nPython Executable: {get_python_executable()}")