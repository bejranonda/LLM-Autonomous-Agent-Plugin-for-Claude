#!/usr/bin/env python3
"""
Plugin Path Resolver for Autonomous Agent Plugin.

Resolves paths to plugin files regardless of installation method
(development, marketplace, or manual). Uses the Claude Code plugin
environment variables as the primary mechanism per the official spec:

- ${CLAUDE_PLUGIN_ROOT}: Plugin installation directory (read-only cache)
- ${CLAUDE_PLUGIN_DATA}: Persistent data directory (~/.claude/plugins/data/{id}/)

Usage:
    from plugin_path_resolver import get_plugin_path, get_script_path, get_data_path

    plugin_root = get_plugin_path()
    script = get_script_path("dashboard.py")
    data_dir = get_data_path()
"""

import os
import sys
from pathlib import Path
from typing import Optional


def get_plugin_path() -> Optional[Path]:
    """
    Get the plugin installation directory path.

    Resolution order:
    1. CLAUDE_PLUGIN_ROOT environment variable (set by Claude Code)
    2. Walk up from __file__ looking for .claude-plugin/plugin.json
    3. Walk up from cwd looking for .claude-plugin/plugin.json

    Returns:
        Path to plugin root directory, or None if not found.
    """
    # 1. Official Claude Code environment variable (primary)
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env_root:
        root = Path(env_root)
        if root.exists():
            return root

    # 2. Walk up from this file's location
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        plugin_json = parent / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            return parent

    # 3. Walk up from current working directory
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        plugin_json = parent / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            return parent

    return None


def get_data_path() -> Path:
    """
    Get the persistent data directory for this plugin.

    Per the Claude Code spec, ${CLAUDE_PLUGIN_DATA} points to
    ~/.claude/plugins/data/{id}/ which survives plugin updates.

    Falls back to .claude-patterns/ in the current working directory
    for development mode compatibility.

    Returns:
        Path to data directory (created if it doesn't exist).
    """
    # 1. Official Claude Code data directory
    env_data = os.environ.get("CLAUDE_PLUGIN_DATA")
    if env_data:
        data_dir = Path(env_data)
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    # 2. Fallback: .claude-patterns/ in cwd (development mode)
    data_dir = Path.cwd() / ".claude-patterns"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_script_path(script_name: str) -> Optional[Path]:
    """
    Get the full path to a Python script in the plugin's lib directory.

    Args:
        script_name: Name of the script file (e.g., "dashboard.py")

    Returns:
        Full path to the script, or None if not found.
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
        Path to lib directory, or None if not found.
    """
    plugin_path = get_plugin_path()
    if not plugin_path:
        return None

    lib_path = plugin_path / "lib"
    if lib_path.exists():
        return lib_path

    return None


def get_python_executable() -> str:
    """
    Get the appropriate Python executable for the current platform.

    Returns:
        Path to Python executable.
    """
    return sys.executable


def validate_plugin_installation() -> dict:
    """
    Validate the plugin installation and return status.

    Returns:
        Dictionary with validation results.
    """
    plugin_path = get_plugin_path()

    if not plugin_path:
        return {
            "valid": False,
            "error": "Plugin installation not found",
            "plugin_path": None,
            "lib_path": None,
            "data_path": None,
            "plugin_json": None,
        }

    plugin_json = plugin_path / ".claude-plugin" / "plugin.json"
    lib_path = plugin_path / "lib"
    data_path = get_data_path()

    checks = {
        "plugin_json_exists": plugin_json.exists(),
        "lib_directory_exists": lib_path.exists(),
        "data_directory_exists": data_path.exists(),
    }

    return {
        "valid": all(checks.values()),
        "plugin_path": str(plugin_path),
        "lib_path": str(lib_path) if lib_path.exists() else None,
        "data_path": str(data_path),
        "plugin_json": str(plugin_json) if plugin_json.exists() else None,
        "checks": checks,
        "env": {
            "CLAUDE_PLUGIN_ROOT": os.environ.get("CLAUDE_PLUGIN_ROOT", "not set"),
            "CLAUDE_PLUGIN_DATA": os.environ.get("CLAUDE_PLUGIN_DATA", "not set"),
        },
    }


if __name__ == "__main__":
    print("Plugin Path Resolver")
    print("=" * 50)

    plugin_path = get_plugin_path()
    print(f"Plugin Path: {plugin_path}")

    data_path = get_data_path()
    print(f"Data Path:   {data_path}")

    print(f"Python:      {get_python_executable()}")

    validation = validate_plugin_installation()
    print(f"Valid:       {validation['valid']}")
    print(f"Env CLAUDE_PLUGIN_ROOT: {validation['env']['CLAUDE_PLUGIN_ROOT']}")
    print(f"Env CLAUDE_PLUGIN_DATA: {validation['env']['CLAUDE_PLUGIN_DATA']}")

    if not validation["valid"]:
        print(f"Error: {validation.get('error', 'Unknown')}")