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

## What Changed in v8.4.2

- Synced `.claude-plugin/marketplace.json` version and component-count description to the current release; it had drifted nine releases behind `plugin.json`.

## What Changed in v8.4.1

- Fixed the plugin'"'"'s own quality-check report path (was writing to a malformed triple-nested directory).
- Fixed the plugin'"'"'s own structure validator undercounting `commands/` due to a non-recursive glob.

## What Changed in v8.4.0

- Restored unit-test integrity: a `try/except ImportError -> @pytest.mark.skipif` pattern across five files was silently skipping 96 tests (every "covered" test was a no-op). Tests of live modules were rewritten against the real API with unconditional imports; tests of deleted modules were removed. The suite now fails loudly on a missing symbol instead of skipping.
- Hardened security: removed an `exec()` import primitive (`quality_control_check.py`), added path-traversal validation to `BackupManager.restore_backup()`, and HTML-escaped dashboard output.
- Pruned unimportable dead modules (`web_dashboard.py`, `debug_timeline.py`) that referenced deleted code.
- Reconciled documented component counts (36 agents, 27 skills, 41 commands) with actual repository contents.

## What Changed in v8.2.0

- Purged all non-ASCII characters from 25 Python utility scripts (zero Windows encoding errors)
- Trimmed 3 oversized agent system prompts (84% average line reduction)
- Removed 11 unused Python scripts from lib/
- Added bin/ executables for direct CLI access to key utilities
- Added settings.json to activate orchestrator automatically on plugin enable

## What Changed in v8.3.0

- Rewrote `lib/dashboard.py` from 6835 broken lines to 534 working lines (92% reduction)
- Dashboard now reads JSON data directly from `.claude-patterns/` with no intermediate data classes
- Removed all imports of deleted modules (`parameter_compatibility`, `unified_parameter_storage`, etc.)
- Flask app factory pattern (`create_app()`) replaces global app instance
- 11 working API endpoints replace 30+ broken ones
- 4-tab dark-theme dashboard with Chart.js visualizations and auto-refresh

## What Changed in v8.1.0

- Removed non-standard frontmatter keys from all components (they were invisible to Claude Code's plugin loader)
- Replaced `<plugin_path>` and `python lib/` references with `${CLAUDE_PLUGIN_ROOT}/lib/` for marketplace compatibility
- Cleaned dead Python import code from agent system prompts
