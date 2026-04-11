---
name: learn:init
description: Initialize pattern learning database
---

EXECUTE THESE BASH COMMANDS DIRECTLY (no agents, no skills):

Step 1 - Check status in current project directory:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/lib/pattern_storage.py" --dir ./.claude-patterns check
```

Step 2 - Initialize if needed:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/lib/pattern_storage.py" --dir ./.claude-patterns init --version 8.0.1
```

Step 3 - Validate:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/lib/pattern_storage.py" --dir ./.claude-patterns validate
```

Step 4 - Verify patterns stored in current project:
```bash
ls -la ./.claude-patterns/ 2>/dev/null || echo "Pattern directory not found in current project"
```

Report results with simple text (no markdown formatting, no boxes).
The pattern database will be stored in your current project directory at ./.claude-patterns/
