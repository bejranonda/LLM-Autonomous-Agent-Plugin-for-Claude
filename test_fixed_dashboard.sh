#!/bin/bash

# Test the fixed dashboard command without Unicode characters
echo "Testing fixed dashboard approach..."

# Step 1: Try local copy (fastest, most reliable)
if [ -f ".claude-patterns/dashboard.py" ]; then
    echo "Starting dashboard from local copy..."
    echo "Would execute: python .claude-patterns/dashboard.py --patterns-dir .claude-patterns"
    echo "SUCCESS: Local copy approach works"
    exit 0
fi

# Step 2: Local copy doesn't exist, try plugin discovery
echo "Local dashboard not found, checking plugin installation..."

# Cross-platform plugin discovery
if command -v find >/dev/null 2>&1; then
    # Unix-like systems (Linux, macOS, Git Bash on Windows)
    PLUGIN_DIR=$(find ~/.claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude ~/.config/claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude 2>/dev/null | head -1)
    echo "Plugin directory found: $PLUGIN_DIR"
elif command -v where >/dev/null 2>&1; then
    # Windows (cmd.exe) - simplified approach
    PLUGIN_DIR=$(find /c/Users/*/.claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude 2>/dev/null | head -1)
    echo "Plugin directory found: $PLUGIN_DIR"
else
    echo "ERROR: Unable to locate files on this system"
    exit 1
fi

# Step 3: If plugin found, copy dashboard locally
if [ -n "$PLUGIN_DIR" ] && [ -f "$PLUGIN_DIR/lib/dashboard.py" ]; then
    echo "Creating local patterns directory..."
    mkdir -p .claude-patterns

    echo "Copying dashboard to local project..."
    cp "$PLUGIN_DIR/lib/dashboard.py" ".claude-patterns/dashboard.py"

    echo "Dashboard copied successfully"
    echo "   From: $PLUGIN_DIR/lib/dashboard.py"
    echo "   To: .claude-patterns/dashboard.py"

    # Step 4: Execute local copy
    echo "Starting dashboard from local copy..."
    echo "Would execute: python .claude-patterns/dashboard.py --patterns-dir .claude-patterns"
    echo "SUCCESS: Plugin discovery and local copy works"
else
    echo "ERROR: Plugin installation not found"
    echo "   Please install the LLM Autonomous Agent Plugin from marketplace"
    echo "   Or ensure you're in a valid project directory"
    exit 1
fi

echo "Fixed dashboard approach test completed successfully!"