#!/usr/bin/env python3
"""
Universal Dashboard Launcher

This script provides a cross-platform way to launch the dashboard
that works regardless of where the user runs the command from.

Usage (in slash commands):
    python lib/universal_dashboard_launcher.py [args...]

This script automatically:
1. Finds the plugin installation
2. Locates the dashboard.py script
3. Executes it with the provided arguments
4. Uses current directory for pattern data
"""

import sys
import os
import subprocess
from pathlib import Path
import platform

def find_plugin_installation():
    """
    Find plugin installation across all platforms and methods.
    """
    home = Path.home()
    plugin_name = "LLM-Autonomous-Agent-Plugin-for-Claude"

    # Build comprehensive search paths
    search_paths = [
        # Marketplace installations (primary)
        home / ".claude" / "plugins" / "marketplaces" / plugin_name,
        home / ".config" / "claude" / "plugins" / "marketplaces" / plugin_name,

        # Alternative marketplace paths
        home / ".claude" / "plugins" / "marketplace" / plugin_name,
        home / ".config" / "claude" / "plugins" / "marketplace" / plugin_name,

        # Development/local installations
        home / ".claude" / "plugins" / "autonomous-agent",
        home / ".config" / "claude" / "plugins" / "autonomous-agent",
    ]

    # Platform-specific paths
    if platform.system() == "Windows":
        appdata = Path(os.environ.get("APPDATA", ""))
        localappdata = Path(os.environ.get("LOCALAPPDATA", ""))
        programfiles = Path(os.environ.get("PROGRAMFILES", ""))

        if appdata:
            search_paths.extend([
                appdata / "Claude" / "plugins" / "marketplaces" / plugin_name,
                appdata / "Claude" / "plugins" / "autonomous-agent",
            ])

        if localappdata:
            search_paths.extend([
                localappdata / "Claude" / "plugins" / "marketplaces" / plugin_name,
                localappdata / "Claude" / "plugins" / "autonomous-agent",
            ])

        if programfiles:
            search_paths.extend([
                programfiles / "Claude" / "plugins" / "marketplaces" / plugin_name,
                programfiles / "Claude" / "plugins" / "autonomous-agent",
            ])

    else:  # Linux/macOS
        search_paths.extend([
            Path("/usr/local/share/claude/plugins/marketplaces") / plugin_name,
            Path("/usr/local/share/claude/plugins/autonomous-agent"),
            Path("/opt/claude/plugins/marketplaces") / plugin_name,
            Path("/opt/claude/plugins/autonomous-agent"),
        ])

    # Search for plugin installation
    for search_path in search_paths:
        if search_path and (search_path / ".claude-plugin" / "plugin.json").exists():
            return search_path

    # Fallback: try to find via current working directory (development mode)
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".claude-plugin" / "plugin.json").exists():
            return parent

    return None

def main():
    """Main execution function."""
    # Get arguments (excluding script name)
    script_args = sys.argv[1:] if len(sys.argv) > 1 else []

    try:
        # Find plugin installation
        plugin_path = find_plugin_installation()

        if not plugin_path:
            print("ERROR: Plugin installation not found", file=sys.stderr)
            print("Please install the LLM Autonomous Agent Plugin from marketplace", file=sys.stderr)
            print("Or run this command from the plugin development directory", file=sys.stderr)
            sys.exit(1)

        # Construct script path
        script_path = plugin_path / "lib" / "dashboard.py"

        if not script_path.exists():
            print(f"ERROR: Dashboard script not found at {script_path}", file=sys.stderr)
            print(f"Plugin installation: {plugin_path}", file=sys.stderr)
            sys.exit(1)

        # Default patterns directory
        patterns_dir = ".claude-patterns"

        # Add default arguments if none provided
        if not script_args:
            script_args = ["--patterns-dir", patterns_dir]
        else:
            # Ensure patterns-dir is included
            if "--patterns-dir" not in script_args:
                script_args.extend(["--patterns-dir", patterns_dir])

        # Execute script from current working directory
        # This preserves access to project-specific data
        cmd = [sys.executable, str(script_path)] + script_args

        print(f"Starting dashboard from: {plugin_path}", file=sys.stderr)
        print(f"Using patterns from: {Path.cwd() / patterns_dir}", file=sys.stderr)

        result = subprocess.run(cmd, cwd=Path.cwd())
        sys.exit(result.returncode)

    except Exception as e:
        print(f"ERROR: Failed to start dashboard: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()