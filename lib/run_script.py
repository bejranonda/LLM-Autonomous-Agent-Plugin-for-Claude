#!/usr/bin/env python3
"""
Script Runner for Autonomous Agent Plugin

This wrapper script ensures that Python scripts are executed from the correct
plugin installation directory, whether running in development mode or
installed from marketplace.

Usage:
    python run_script.py dashboard.py [args]
    python run_script.py learning_analytics.py show --dir .claude-patterns
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path to import plugin_path_resolver
sys.path.insert(0, str(Path(__file__).parent))

try:
    from plugin_path_resolver import get_script_path, get_plugin_path
except ImportError as e:
    print(f"Error: Could not import plugin_path_resolver: {e}", file=sys.stderr)
    print("Please ensure plugin_path_resolver.py is in the same directory.", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_script.py <script_name> [args...]", file=sys.stderr)
        print("Example: python run_script.py dashboard.py --port 8080", file=sys.stderr)
        sys.exit(1)

    script_name = sys.argv[1]
    script_args = sys.argv[2:]

    # Resolve the script path
    script_path = get_script_path(script_name)
    if not script_path:
        plugin_path = get_plugin_path()
        if plugin_path:
            print(f"Error: Script '{script_name}' not found in plugin directory: {plugin_path}/lib/", file=sys.stderr)
        else:
            print("Error: Plugin installation not found. Please ensure the plugin is properly installed.", file=sys.stderr)
        sys.exit(1)

    # Change to the script's directory to ensure relative imports work
    script_dir = script_path.parent
    original_cwd = os.getcwd()

    try:
        os.chdir(script_dir)

        # Execute the script with the same Python interpreter
        # Use subprocess to properly handle script execution
        import subprocess

        # Build the command
        cmd = [sys.executable, str(script_path)] + script_args

        # Execute the script
        result = subprocess.run(cmd, cwd=script_dir)
        sys.exit(result.returncode)

    except FileNotFoundError:
        print(f"Error: Script '{script_path}' not found", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when executing '{script_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error executing script: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Restore original working directory
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()