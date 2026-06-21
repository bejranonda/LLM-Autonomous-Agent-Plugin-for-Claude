# Known Issues & Stabilization Roadmap (v8.3.0+)

The v8.3.0 release focused on dashboard reliability and dead code removal. Below are currently identified operational constraints:

## Resolved in v8.4.3

- **[FIXED] Marketplace version drift (again)**: the 8.4.2 version bump updated `plugin.json`/`CLAUDE.md`/`README.md` but missed `marketplace.json`, immediately reintroducing the v8.4.2 fix. `validate-claude-plugin.py` now checks `marketplace.json` against `plugin.json` and warns on drift, so this is caught automatically going forward.

## Resolved in v8.4.2

- **[FIXED] Stale marketplace listing**: `.claude-plugin/marketplace.json` (the listing shown when browsing/installing from the marketplace) was stuck at `version: 8.0.0` with stale component counts — nine releases behind `plugin.json`. Synced to the current release with accurate counts.

## Resolved in v8.4.1

- **[FIXED] Malformed report path**: `quality_control_check.py` wrote its detailed report to a literal triple-nested path `.claude/data/data/data/reports/...` instead of the documented `.claude/reports/...` convention.
- **[FIXED] Undercounted commands**: `validate-claude-plugin.py` used a non-recursive `glob("*")` on `commands/`, which is organized into 10 category subfolders, so it reported 11 "files" instead of the actual 41 command definitions. Counting is now recursive per component type.

## Resolved in v8.4.0

- **[FIXED] Test-suite false confidence**: The unit suite reported `77 passed / 96 skipped`, but every skip was a `try/except ImportError -> @pytest.mark.skipif` guard that silently turned a real failure into a green skip. `test_detect_current_model` and `test_agent_error_helper` imported renamed/removed symbols; `test_plugin_validator`, `test_dashboard_validator`, and `test_simple_validation` tested deleted modules. The two live-module tests were rewritten against the real API (no skip guard); the three orphaned files were removed. Suite now: `113 passed, 0 skipped, 0 warnings`.
- **[FIXED] exec() code-injection primitive**: `quality_control_check.py` built import statements from filename-derived strings and ran them via `exec()`. Replaced with `importlib.import_module()`.
- **[FIXED] Backup path traversal (latent)**: `BackupManager.restore_backup()` now rejects a `backup_id` that escapes the backup directory before any filesystem access (legitimate missing IDs still raise `FileNotFoundError`).
- **[FIXED] Unimportable dead modules**: `lib/web_dashboard.py` (called `sys.exit(1)` at import) and `lib/debug_timeline.py` (imported the removed `DashboardDataCollector`) deleted; both referenced deleted code with no live callers.
- **[FIXED] pytest collection warning**: utility class `TestSuiteValidator` renamed to `SuiteValidator` so pytest stops trying to collect it.
- **[FIXED] Documentation drift**: corrected component counts (36 agents, 27 skills, 41 commands) and the plugin-manifest version reference in CLAUDE.md.

## Resolved in v8.3.0

- **[FIXED] Dashboard Syntax Error**: `lib/dashboard.py` had an unterminated triple-quoted string (197 quotes, odd count) causing SyntaxError at line 6835. Complete rewrite reduced it to 534 working lines.
- **[FIXED] Dashboard Import Failures**: Dashboard imported deleted modules (`parameter_compatibility`, `unified_parameter_storage`, `detect_current_model` at import time). Rewrite uses zero local module dependencies - reads JSON directly.
- **[FIXED] Flask App Not Starting**: `app = Flask(__name__)` was commented out. New version uses Flask app factory pattern (`create_app()`).
- **[FIXED] Dashboard HTML Bloat**: 3655 lines of inline HTML replaced with 190-line dark-theme template using Chart.js from CDN.
- **[FIXED] Broken API Endpoints**: 30+ endpoints (many returning 404 or errors) consolidated to 11 working endpoints.

## Resolved in v8.2.0

- **[FIXED] Windows UnicodeEncodeError**: All 103 non-ASCII characters removed from 25 Python scripts. Zero non-ASCII characters remain in lib/*.py.
- **[FIXED] Oversized Agent Prompts**: learning-engine (1642→208 lines), dev-orchestrator (759→135 lines), security-auditor (755→152 lines) trimmed by 80-87%.
- **[FIXED] Unused Scripts**: 11 unreferenced Python scripts removed from lib/ to reduce install size.
- **[FIXED] Duplicate Skill File**: Removed redundant TRANSCENDENT_AI_SYSTEMS.md (SKILL.md already existed).

## Resolved in v8.1.0

- **[FIXED] Installation Failure**: "agents: Invalid input" error caused by non-standard frontmatter keys in agent files (group, category, tier, etc.). All 36 agents now use only spec-compliant frontmatter.
- **[FIXED] Path Discovery**: Legacy `find`-based path resolution replaced with `${CLAUDE_PLUGIN_ROOT}` across 81 files. Scripts now work correctly when installed from marketplace.
- **[FIXED] Orchestrator Bloat**: Removed ~230 lines of non-functional Python import code embedded in the orchestrator markdown system prompt.
- **[FIXED] Missing SKILL.md**: `transcendent-ai-systems` skill was missing its SKILL.md file (had TRANSCENDENT_AI_SYSTEMS.md instead).
- **[FIXED] YAML Parse Errors**: Fixed broken frontmatter in `analyze:project`, `workspace:organize`, and `evolve:transcendent` commands.
- **[FIXED] Invalid model values**: Removed `model: inherit` from 25 agent files (not a valid value; omitting the field achieves the same default behavior).

## Remaining Known Issues

### Data Storage
- **Local Fallback Persistence**: If the plugin operates outside an initialized Claude Code environment (where `${CLAUDE_PLUGIN_DATA}` is undefined), data saves to `.claude-patterns/` in the CWD. Switching directories can fragment patterns.
- **Concurrency Locks on Windows**: High-volume sequential tasks on Windows use `msvcrt` locks in `pattern_storage.py`. There may be 1-5ms delays during heavy multi-agent logging.

### Sub-Agent Execution
- **Long-Running Process Limits**: Certain Python validation scripts (like headless browser testing) may timeout under Claude Code's default step execution timer if they exceed ~180 seconds.
- **Terminal Parsing Variations**: PowerShell/CMD output parsing differs per system. Workarounds are included but rely on standard stderr.

### Plugin Size
- **Large lib/ Directory**: 124 active scripts (78K lines, 6MB) are bundled. Not all are actively used by agents/commands. Future versions may prune unused utilities.

### Data & Tooling Integrity
- **Auto-fix pattern count mismatch**: `patterns/autofix-patterns.json` declares `statistics.total_patterns: 24`, but only 19 patterns are actually defined across the category arrays (typescript 5, python 5, javascript 3, build_config 3, api_contract 3). Either 5 patterns are unwritten or the statistics block is stale.
- **Stale manual test script**: `scripts/testing/test_metrics_kpi_system.py` still has one deferred reference to the deleted `token_monitoring_dashboard` and a `sys.path` that assumes repo root. It is a standalone manual script (not part of the `pytest` suite), kept pending a decision on the token-monitoring feature.
- **Editor hook may block edits**: A Semgrep Guardian `PreToolUse` hook can fail closed when unauthenticated, blocking file edits/deletes in some environments. Authenticate or disable it if operations are unexpectedly rejected.

## Reporting Issues
If you encounter issues, ensure you are running v8.1.0+ installed via `/plugin install`. Run validation with `/validate:plugin`.
