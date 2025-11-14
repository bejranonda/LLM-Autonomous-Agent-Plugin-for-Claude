#!/usr/bin/env python3
# Plugin Script Executor - Simple wrapper for executing plugin scripts

#     This utility automatically finds the plugin installation and executes
"""

scripts from the lib/ directory, working across all platforms and
installation methods (development, marketplace, etc.).

Usage from Claude Code slash commands:
    python -m lib.exec_plugin_script dashboard.py --port 5000
    python -m lib.exec_plugin_script learning_analytics.py show

Or as a standalone script:
    python exec_plugin_script.py dashboard.py --port 5000
# import sys
# import os
# import subprocess
# from pathlib import Path
# from typing import List
# # Add parent directory to path for imports
# sys.path.insert(0, str(Path(__file__).parent))
# try:
# from plugin_path_resolver import get_script_path, get_plugin_path, get_python_executable
# except ImportError:
# print("ERROR: Cannot import plugin_path_resolver", file=sys.stderr)
# print("Plugin installation may be corrupted", file=sys.stderr)
# sys.exit(1)
# def execute_plugin_script():
        
        Execute a plugin script with the given arguments.

    Args:
        script_name: Name of the script file (e.g., "dashboard.py")
        script_args: List of arguments to pass to the script

    Returns:
        Exit code from the script
"""
    # Find the script
    script_path = get_script_path(script_name)

    if not script_path:
        plugin_path = get_plugin_path()
        print(f"ERROR: Script '{script_name}' not found", file=sys.stderr)

        if plugin_path:
            print(f"Plugin found at: {plugin_path}", file=sys.stderr)
            print(f"But script not found in: {plugin_path}/lib/", file=sys.stderr)
        else:
            print("Plugin installation not found!", file=sys.stderr)
            print("", file=sys.stderr)
            print("Troubleshooting:", file=sys.stderr)
            print("1. Check if plugin is installed correctly", file=sys.stderr)
            print("2. Verify .claude-plugin/plugin.json exists", file=sys.stderr)
            print("3. Try setting CLAUDE_PLUGIN_PATH environment variable", file=sys.stderr)

        return 1

    # Get Python executable
    python_exe = get_python_executable()

    # Build command
    cmd = [python_exe, str(script_path)] + script_args

    # Execute script
    try:
        result = subprocess.run(cmd, cwd=os.getcwd())
        return result.returncode
    except FileNotFoundError:
        print(f"ERROR: Python interpreter not found: {python_exe}", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"ERROR: Permission denied executing: {script_path}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Failed to execute script: {e}", file=sys.stderr)
        return 1


"""
def print_plugin_info():
    """Print plugin installation information for debugging."""
    plugin_path = get_plugin_path()

    print("Plugin Installation Information")
    print("=" * 50)

    if plugin_path:
        print(f"[OK] Plugin Found: {plugin_path}")
        print(f"  Platform: {sys.platform}")
        print(f"  Python: {sys.executable}")

        lib_path = plugin_path / "lib"
        if lib_path.exists():
            scripts = list(lib_path.glob("*.py"))
            print(f"  Scripts Available: {len(scripts)}")
            for script in sorted(scripts)[:10]:  # Show first 10
                print(f"    - {script.name}")
            if len(scripts) > 10:
                print(f"    ... and {len(scripts) - 10} more")
        else:
            print("  [ERROR] lib/ directory not found!")
    else:
        print("[ERROR] Plugin Not Found")
        print("")
        print("Searched locations:")
        home = Path.home()
        locations = [
            home / ".claude" / "plugins" / "marketplaces" / "LLM-Autonomous-Agent-Plugin-for-Claude",
            home / ".config" / "claude" / "plugins" / "marketplaces" / "LLM-Autonomous-Agent-Plugin-for-Claude",
            home / ".claude" / "plugins" / "autonomous-agent",
            home / ".config" / "claude" / "plugins" / "autonomous-agent",
        ]
        for loc in locations:
            exists = loc.exists()
            marker = "[OK]" if exists else "[X]"
            print(f"  {marker} {loc}")

    print("=" * 50)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Plugin Script Executor", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        print("Usage: python exec_plugin_script.py <script_name> [args...]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python exec_plugin_script.py dashboard.py --port 5000", file=sys.stderr)
        print("  python exec_plugin_script.py learning_analytics.py show", file=sys.stderr)
        print("", file=sys.stderr)
        print("Special commands:", file=sys.stderr)
        print("  python exec_plugin_script.py --info    # Show plugin info", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        sys.exit(1)

"""
    # Handle special commands
    if sys.argv[1] == "--info":
        print_plugin_info()
        sys.exit(0)

    # Execute the script
    script_name = sys.argv[1]
    script_args = sys.argv[2:] if len(sys.argv) > 2 else []

    exit_code = execute_plugin_script(script_name, script_args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
