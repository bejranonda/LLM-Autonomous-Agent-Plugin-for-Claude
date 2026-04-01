# Release Notes: v8.0.0 (Stabilization Update)

This major release solidifies the foundation of the Autonomous Agent Plugin, bringing it fully into compliance with the official Claude Code plugin marketplace specification.

## Core Refactoring & Stabilization
- **Massive Cleanup (Phase 1):** Removed 62+ dead, experimental, and broken scripts from `lib/` (e.g. `USER_FIX_SCRIPT.py`, `nuclear_fix.py`), eliminating significant technical debt and drastically reducing the plugin's footprint.
- **Manifest Updates (Phases 2 & 3):** Standardized `.claude-plugin/plugin.json` to properly broadcast `agents/`, `skills/`, and `commands/` paths for component discovery. Cleaned up `marketplace.json` documentation strings and repository alignment.
- **Data Persistence Overhaul (Phase 4):** Standardized memory and persistent storage resolution. 
  - `plugin_path_resolver.py` and `pattern_storage.py` rewritten to use Claude Code's native `${CLAUDE_PLUGIN_DATA}` mechanism for safe, update-tolerant data persistence.
  - Eliminated corrupted multiline-string python stubs.
- **Memory Optimization (Phase 5):** Re-architected the `orchestrator.md` file, splitting it from an immense 140KB monolithic prompt down to a streamlined 37KB core instruction set. Deep group implementations have been elegantly factored out into the `orchestrator-implementation` and `orchestrator-subsystems` skills. 
- **Repo Organization (Phase 6):** Relocated all scattered release note files to `docs/releases/`.
- **Infrastructure (Phase 7):** Established rigorous CI via GitHub Actions (`ci.yml`) and instituted a fully defined `requirements.txt`.

This release introduces zero new agents, preferring to dramatically multiply the stability, platform compatibility, and speed of existing implementations.
