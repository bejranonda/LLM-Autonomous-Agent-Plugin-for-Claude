#!/usr/bin/env python3
# Marketplace Plugin Executor - Template-based execution

# This script provides a template-based approach for marketplace installations.
# Claude Code replaces the {PLUGIN_PATH} placeholder during installation
with the actual plugin installation path.

# Usage in slash commands (template):
#     python -c "exec(open(r'{PLUGIN_PATH}/lib/marketplace_executor.py').read())" dashboard.py --port 5000

# After marketplace installation (filled in):
#     python -c "exec(open(r'C:\\Users\\{user}\\.claude\\plugins\\marketplaces\\LLM-Autonomous-Agent-Plugin-for-Claude\\lib\\marketplace_executor.py').read())" dashboard.py --port 5000
import sys
import os
import subprocess
from pathlib import Path


def main():
    """Main execution function - called when script is executed via exec()"""

    if len(sys.argv) < 2:
        print("Usage: marketplace_executor.py <script_name> [args...]", file=sys.stderr)
        print("Example: marketplace_executor.py dashboard.py --port 5000", file=sys.stderr)
        sys.exit(1)

    # Extract script name and arguments
    script_name = sys.argv[1]
    script_args = sys.argv[2:] if len(sys.argv) > 2 else []

    # Get plugin path from the script's own location
    # When executed via exec(open('{PLUGIN_PATH}/lib/marketplace_executor.py').read())
    # __file__ will be the filled path like: C:\Users\user\.claude\plugins\marketplaces\...\lib\marketplace_executor.py
    try:
        plugin_path = Path(__file__).parent.parent
    except NameError:
        # Fallback: Try to extract plugin path from the current execution context
        # When executed via exec(open(r'{PLUGIN_PATH}/lib/marketplace_executor.py').read())
        # We can try to find the plugin installation

        # Search for plugin installation
        home = Path.home()
        plugin_name = "LLM-Autonomous-Agent-Plugin-for-Claude"
        search_paths = [
            home / ".claude/plugins/marketplaces" / plugin_name,
            home / ".config/claude/plugins/marketplaces" / plugin_name,
            home / ".claude/plugins/autonomous-agent",
            home / ".config/claude/plugins/autonomous-agent",
        ]

        plugin_path = None
        for path in search_paths:
            if (path / ".claude-plugin/plugin.json").exists():
                plugin_path = path
                break

        if not plugin_path:
            print(
                "ERROR: Cannot determine plugin path. Install plugin from marketplace or run from development directory.",
                file=sys.stderr,
            )
            sys.exit(1)

    # Construct script path
    script_path = plugin_path / "lib" / script_name

    if not script_path.exists():
        print(f"ERROR: Script '{script_name}' not found at {script_path}", file=sys.stderr)
        sys.exit(1)

    # Execute the script from current working directory
    # This ensures the script can access project-local files like .claude-patterns/
    try:
        cmd = [sys.executable, str(script_path)] + script_args

        # Execute from current directory (preserves access to project data)
        result = subprocess.run(cmd, cwd=os.getcwd())
        sys.exit(result.returncode)

    except Exception as e:
        print(f"ERROR: Failed to execute script: {e}", file=sys.stderr)
        sys.exit(1)


# Make function available for direct execution
if __name__ == "__main__":
    main()
