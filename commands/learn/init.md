---
name: learn:init
description: Initialize pattern learning database
---

EXECUTE THESE BASH COMMANDS DIRECTLY (no agents, no skills):

Step 1 - Check status:
```bash
python lib/exec_plugin_script.py pattern_storage.py check
```

Step 2 - Initialize if needed:
```bash
python lib/exec_plugin_script.py pattern_storage.py init --version 7.6.8
```

Step 3 - Validate:
```bash
python lib/exec_plugin_script.py pattern_storage.py validate
```

Report results with simple text (no markdown formatting, no boxes).
