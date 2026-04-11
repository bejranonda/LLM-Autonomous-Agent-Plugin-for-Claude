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
