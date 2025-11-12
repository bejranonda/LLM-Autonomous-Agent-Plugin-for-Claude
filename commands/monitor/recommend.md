---
name: monitor:recommend
description: Get smart workflow and optimization recommendations based on learned patterns
---

EXECUTE THESE BASH COMMANDS DIRECTLY (no agents, no skills):

First, find the plugin installation path:
```bash
PLUGIN_PATH=$(find ~/.claude -name "exec_plugin_script.py" 2>/dev/null | head -1 | sed 's|/lib/exec_plugin_script.py||')
echo "Plugin found at: $PLUGIN_PATH"
```

Step 1 - Generate recommendations using project patterns:
```bash
python3 "$PLUGIN_PATH/lib/exec_plugin_script.py" recommendation_engine.py --dir ./.claude-patterns --task "your task description here"
```

Step 2 - For general recommendations (no specific task):
```bash
python3 "$PLUGIN_PATH/lib/exec_plugin_script.py" recommendation_engine.py --dir ./.claude-patterns
```

Step 3 - For JSON output (programmatic use):
```bash
python3 "$PLUGIN_PATH/lib/exec_plugin_script.py" recommendation_engine.py --dir ./.claude-patterns --task "your task" --format json
```

Report will show:
- Recommended approach with confidence level
- Quality predictions and time estimates
- Skill suggestions with success rates
- Risk assessment with mitigations
- Alternative approaches with trade-offs

The recommendations will use patterns from your current project directory at ./.claude-patterns/
