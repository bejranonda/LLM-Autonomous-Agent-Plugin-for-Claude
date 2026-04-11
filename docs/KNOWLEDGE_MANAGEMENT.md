# Knowledge Management Paradigm

Starting in v8.1.0, the Autonomous Agent Plugin enforces strict knowledge decentralization aligned with Claude Code specifications.

## Environment Isolation

### Plugin Installation (`${CLAUDE_PLUGIN_ROOT}`)
All plugin code, agents, skills, commands, and Python utilities are installed to the plugin cache directory. Referenced via `${CLAUDE_PLUGIN_ROOT}` which Claude Code substitutes automatically.

### Persistent Data (`${CLAUDE_PLUGIN_DATA}`)
Long-lived data (memory vectors, decision success rates, token histories) is stored in Claude's native plugin data sandbox: `~/.claude/plugins/data/{plugin-id}/`. This directory survives plugin updates.

### Project Data (`.claude-patterns/`)
Per-project learning patterns are stored in `.claude-patterns/` within the user's working directory. This is project-scoped and not part of the plugin installation.

## Component Discovery

All components are auto-discovered by Claude Code's convention-based loader:
- **Skills**: `skills/<name>/SKILL.md` - loaded based on task context matching
- **Agents**: `agents/<name>.md` - available for delegation and user invocation
- **Commands**: `commands/<category>/<name>.md` - exposed as `/autonomous-agent:<name>` slash commands

## Inter-Group Knowledge

When consolidating knowledge across the Four-Tier workflow, the system uses `unified_data.json` with file-locked writes for race-free concurrency across operating systems. This reduces API payload overhead and synchronizes contextual performance data.

## What Changed in v8.2.0

- Purged all non-ASCII characters from 25 Python utility scripts (zero Windows encoding errors)
- Trimmed 3 oversized agent system prompts (84% average line reduction)
- Removed 11 unused Python scripts from lib/
- Added bin/ executables for direct CLI access to key utilities
- Added settings.json to activate orchestrator automatically on plugin enable

## What Changed in v8.1.0

- Removed non-standard frontmatter keys from all components (they were invisible to Claude Code's plugin loader)
- Replaced `<plugin_path>` and `python lib/` references with `${CLAUDE_PLUGIN_ROOT}/lib/` for marketplace compatibility
- Cleaned dead Python import code from agent system prompts
