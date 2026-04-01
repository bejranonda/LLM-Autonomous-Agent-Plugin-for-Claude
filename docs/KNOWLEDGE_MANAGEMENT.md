# Knowledge Management Paradigm

Starting in version 8.0.0, the Autonomous Agent Plugin enforces strict knowledge decentralization aligned with the Claude Code specifications.

## Global Environment Isolation (`${CLAUDE_PLUGIN_DATA}`)
Previously, data was coupled tightly to the operational paths of the working repository. The system now delegates persistent knowledge integration (such as memory vectors, decision success rates, and token histories) strictly into Claude's native data sandbox: `~/.claude/plugins/data/{plugin-id}`.

### Component Discovery
All logic runs independently and asynchronously.
- **Skills:** Loaded directly via `skills/` metadata.
- **Agents:** System prompts managed via `agents/` and referenced autonomously.
- **Core State:** Consistently retrieved from the singleton `PatternStorage` abstraction mapping the marketplace specifications.

## The `unified_data.json` Mechanism
When consolidating inter-group knowledge across our Four-Tier workflow, the system performs scheduled compactions to `unified_data.json` via file locks, ensuring race-free concurrency across operating systems. This reduces API payload overhead and securely synchronizes Contextual Performance with standard LLM contexts.
