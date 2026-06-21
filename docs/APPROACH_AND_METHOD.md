# Operational Approach and Methods

This document defines the execution paradigm of the Autonomous Agent Plugin (v8.1.0+).

## The Four-Tier Coordination Method

We compartmentalize tasks into specialized execution groups:

1. **Group 1: Strategic Analysis** - High-level abstraction. Uses analysis skills to map the workspace before making decisions.
2. **Group 2: The Orchestrator** - Takes structural analysis and determines execution sequencing and routing.
3. **Group 3: Execution Engine** - Deterministic rules and localized commands. Isolated step execution.
4. **Group 4: Quality & Validation** - Aggressive cross-verification against the initially proposed approach from Group 1.

## Plugin Specification Compliance (v8.1.0)

With v8.1.0, we prioritize strict compliance with Claude Code's official plugin specification:

1. **Schema-Compliant Frontmatter**: All agents use only officially documented keys (`name`, `description`, `tools`, `model`, `effort`, `maxTurns`, `disallowedTools`, `skills`, `memory`, `background`, `isolation`). Custom metadata moved to markdown body.
2. **Modern Path Resolution**: All script references use `${CLAUDE_PLUGIN_ROOT}/lib/` instead of legacy `find`-based discovery or relative `lib/` paths. This ensures scripts work correctly when installed from any marketplace.
3. **Auto-Discovery Over Explicit Paths**: Plugin relies on Claude Code's convention-based discovery (`agents/`, `skills/`, `commands/` directories) rather than explicit path declarations in `plugin.json`.
4. **Clean System Prompts**: Agent markdown files contain only system prompt instructions. Executable Python/JavaScript code has been removed from markdown files since it was never executed (agents are prompts, not scripts).

## Stabilization Methods

1. **Defunct Code Pruning**: Redundant fix scripts and dead code in agent prompts comprehensively pruned.
2. **Standardized Communication**: `orchestrator.md` delegates via skills and sub-agents. No single prompt exceeds reasonable context length.
3. **Immutable Source Pathing**: All Python libraries reference via `${CLAUDE_PLUGIN_ROOT}`. No arbitrary string injection into terminal evaluations.

## Performance & Cross-Platform Design (v8.2.0)

1. **ASCII-Only Python Output**: All print statements and string literals in lib/*.py use ASCII-only characters. No Unicode symbols, arrows, or emoji. This guarantees compatibility with Windows cp1252 code pages.
2. **Concise Agent System Prompts**: Agent .md files are system prompts, not scripts. They should be focused instructions, not documentation dumps. Oversized agents are periodically audited and trimmed. Target: under 400 lines per agent.
3. **Minimal lib/ Footprint**: Python utility scripts are audited for usage. Unreferenced scripts are removed to keep the plugin install lean.
4. **bin/ Executables**: Key scripts exposed as bare CLI commands via bin/ so agents and users can invoke them without full Python path syntax.

## Dashboard Simplicity (v8.3.0)

1. **Direct JSON Reads**: Dashboard loads `.claude-patterns/*.json` files directly. No intermediate data collector classes, no complex class hierarchies. Each data function is a standalone helper that reads one JSON file and returns a dict.
2. **Flask App Factory**: `create_app(patterns_dir)` produces a configured Flask app. This pattern supports testing, multiple instances, and clean startup. The `dashboard_launcher.py` wrapper provides auto-restart and health monitoring on top.
3. **Zero Local Imports**: The dashboard depends only on Flask and stdlib. Previously it imported deleted modules causing immediate ImportError. This isolation means the dashboard cannot break due to changes elsewhere in lib/.
4. **CDN-Based UI**: Chart.js loaded from jsdelivr CDN. No bundled JS dependencies to maintain. Dark theme with auto-refresh keeps the UI functional without external CSS frameworks.

## Test Integrity & Security (v8.4.0)

1. **Tests Fail Loudly**: Test files import the module under test unconditionally (after putting `lib/` on `sys.path`). The `try/except ImportError -> IMPORTS_AVAILABLE = False -> @pytest.mark.skipif` idiom is banned: it converts a renamed or deleted API into a silently-skipped (green) test, hiding real breakage. A test that cannot import its subject must fail at collection, not skip.
2. **Verify the Whole Surface, Not Just Syntax**: `py_compile` proves a module parses; it does not prove its `from sibling import name` statements resolve. Releases run an import-resolution sweep that actually imports every `lib/*.py` module and classifies failures as real drift vs. merely-missing optional dependencies. Modules must not call `sys.exit()` at import time.
3. **No exec() for Imports**: Dynamic imports use `importlib.import_module()`, never `exec()` of an f-string-built statement. Building executable code from filename- or path-derived strings is a code-injection primitive.
4. **Containment Before Filesystem Access**: Functions that resolve a caller-supplied identifier into a path validate that the resolved path stays inside the intended root (`is_relative_to`) before touching the filesystem.
5. **Documentation Reflects Reality**: Component counts and version strings are verified against the actual repository on each release, not carried forward by assumption. This includes every metadata file a user or marketplace actually reads, not just the primary manifest: `plugin.json`, `marketplace.json`, `CLAUDE.md`, and `README.md` are all checked for version/count drift on release.
6. **The Validator Validates Itself Too (v8.4.1)**: Self-check tooling (`validate-claude-plugin.py`, `quality_control_check.py`) is held to the same scrutiny as the code it checks. A non-recursive `glob("*")` undercounted `commands/` because that directory is organized into category subfolders; a copy-pasted path segment caused reports to be written three directories deeper than intended. Both were caught by actually running the tool and reading its output, not by reading the code in isolation.
7. **Metrics Must Mean What Their Name Says (v8.4.5)**: A metric called `Successful Imports` that silently reports `1` for ~18 months is worse than no metric at all - it looks authoritative while being misleading. The bug: `importlib.import_module("lib.dashboard")` was called from a process whose `sys.path` contained `lib/` (not the project root), so the dotted-path resolution failed for ~99% of files and the `ModuleNotFoundError` was swallowed by an `except`. The fix: load by absolute path with `importlib.util.spec_from_file_location`, which is `sys.path`-independent. Lesson: when a metric depends on environment state (`sys.path`, env vars, CWD), prefer an API that takes the path explicitly over one that does implicit resolution. Additionally, redirect `stdout`/`stderr` during `exec_module` so diagnostic prints from imported modules (dashboard, web_page_validator) do not pollute the report - the tool's output should be the tool's, not its inputs'.
8. **User-Level Hooks Are Not Plugin Bugs (v8.4.5)**: When a session is paralyzed by a `PreToolUse` hook, the temptation is to hunt for the hook in the project's own manifests. This plugin ships no hooks at all; the offending Semgrep Guardian was the user-level `semgrep@claude-plugins-official` plugin in `~/.claude/settings.json`. Before claiming a hook-related bug in any plugin, check (a) `.claude-plugin/plugin.json` for a `hooks` block, (b) user-level `~/.claude/settings.json` for `enabledPlugins`, and (c) whether the error string names a specific vendor ("Semgrep Guardian" != "autonomous-agent"). Document the distinction in `KNOWN_ISSUES.md` so users can self-serve the fix instead of filing it against the wrong project.