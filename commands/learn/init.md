---
name: learn:init
description: Initialize pattern learning database
---

EXECUTE THESE BASH COMMANDS DIRECTLY (no agents, no skills):

First, find the plugin installation path:
```bash
PLUGIN_PATH=$(find ~/.claude -name "exec_plugin_script.py" 2>/dev/null | head -1 | sed 's|/lib/exec_plugin_script.py||')
echo "Plugin found at: $PLUGIN_PATH"
```

Step 1 - Check status in current project directory:
```bash
python3 "$PLUGIN_PATH/lib/exec_plugin_script.py" pattern_storage.py --dir ./.claude-patterns check
```

Step 2 - Initialize if needed:
```bash
python3 "$PLUGIN_PATH/lib/exec_plugin_script.py" pattern_storage.py --dir ./.claude-patterns init --version 7.6.9
```

Step 3 - Validate:
```bash
python3 "$PLUGIN_PATH/lib/exec_plugin_script.py" pattern_storage.py --dir ./.claude-patterns validate
```

Step 4 - Verify patterns stored in current project:
```bash
ls -la ./.claude-patterns/ 2>/dev/null || echo "Pattern directory not found in current project"
```

Report results with simple text (no markdown formatting, no boxes).
The pattern database will be stored in your current project directory at ./.claude-patterns/
