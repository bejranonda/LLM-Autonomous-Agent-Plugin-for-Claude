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
