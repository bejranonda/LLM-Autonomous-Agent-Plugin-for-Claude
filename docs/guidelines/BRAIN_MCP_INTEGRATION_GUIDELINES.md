# Brain MCP Integration Guidelines

## Overview

This plugin can optionally integrate with an **external Brain MCP server** (a separate project-memory service, not part of this plugin) for cross-project knowledge persistence. The Brain stores durable rules, recipes, anti-patterns, and reflexes that survive across sessions and repositories, indexed by project + user.

> **Naming clarity**: The plugin's *internal* "Brain" (Group 1: Strategic Analysis & Intelligence) is **unrelated** to the *external* Brain MCP server. The internal "Brain" is a group of 7 analysis agents inside this plugin. The external Brain is a separate MCP service that this plugin can write to and read from.

## When to Use Brain MCP

| Scenario | Use Brain? | Why |
|---|---|---|
| Capture a durable lesson (e.g. "glob('*') undercounts nested dirs") | **Yes** | Survives across sessions + repos; auto-surfaced on related tasks |
| Store project-specific pattern (e.g. "this repo uses poetry not pipenv") | **Yes** | Scoped to this project, retrieved next time you work here |
| Note a user preference (e.g. "user prefers tabs over spaces") | **Yes** | User-scoped, applies across all projects |
| Cache a transient computation result | **No** | Use local `.claude-patterns/` instead |
| Store a secret or credential | **NO** | Brain is external; never store secrets in it |
| Log every commit message | **No** | Use git log; Brain is for distilled rules, not raw history |

## Connection Protocol

Per the Brain MCP instructions, every coding task should:

1. **Open**: Call `brain_get_user_style` first to verify connectivity and bootstrap your peer card. If it returns "Server not initialized" or any transport error, the MCP connection has dropped — see "Recovery" below.
2. **Start session**: Call `brain_start_session(prompt: <task description>)` — the response carries `relevantKnowledge`, rules the Brain already learned that apply to the task. Apply them and pass their IDs back as `knowledgeUsed` when you close.
3. **Query mid-task**: Use `brain_ask_oracle("what did we decide about X?")` before re-deriving decisions from earlier sessions.
4. **Teach as you learn**: Call `brain_teach_knowledge` for each durable rule you distill. Each item: `{trigger, rule, rationale, type, source}`.
5. **Close**: Call `brain_report_session_outcome` with `learnings: 0-5 durable rules`. This triggers the Knowledge Extraction Agent's feedback loop.

## Retrieval: Oracle vs Scoped — Critical Distinction

The Brain exposes **two retrieval paths** with different ranking behavior:

| Path | Scope | Reliability for new items |
|---|---|---|
| `brain_ask_oracle(query)` | Cross-project, ranking-based | **Misses new project-scoped items** (cold-start penalty + project-scope filter) |
| `brain_retrieve_knowledge(query, projectId)` | Single project, vector-similarity | **Reliable** — surfaces items with similarity 0.50–0.88 even when freshly written |

### Workaround for Oracle Misses (learned v8.4.5)

If `brain_ask_oracle` returns "no knowledge" or tangential results for an item you *just* taught:

1. **Don't assume data loss.** The item is almost certainly stored — verify with scoped retrieval.
2. **Re-query with explicit `projectId`**: `brain_retrieve_knowledge(query, projectId=<id>)` — this path works reliably for new items.
3. **Ranking will improve with use.** Items accrue `usageCount`/`successCount` over time, which boosts oracle ranking. New items start at `usageCount: 0` and may take several related queries to surface.
4. **User-scoped items rank higher than project-scoped** in oracle queries. If a rule applies across all your projects, teach it as user-scoped, not project-scoped.

## Authorization & Guardrails

### Auto-mode classifier behavior

When `permissions.defaultMode: "auto"` is set in `~/.claude/settings.json`, the classifier gates certain Brain operations:

| Operation | Typical outcome |
|---|---|
| Single `brain_teach_knowledge` call | **Allowed** |
| Batch of 15+ `brain_teach_knowledge` calls framed as "user authorized bulk transfer" | **Denied** — classifier flags self-authored authorization framing |
| Same 15 calls retried individually | **Allowed** |
| `brain_get_user_style`, `brain_list_projects`, `brain_ask_oracle` | **Allowed** |
| Editing `~/.claude/settings.json` to add `mcp__brain__*` to `permissions.allow` | **DENIED** — agent cannot self-grant permissions (permission self-modification guardrail) |

### Permission self-grant guardrail (important)

The auto-mode classifier **prevents agents from editing `~/.claude/settings.json` to widen their own permissions**, even when the user said "continue all as suggested." This is a deliberate safety property. To add Brain MCP tools to your allow list, **the user must edit the file manually**:

```jsonc
// ~/.claude/settings.json
{
  "permissions": {
    "defaultMode": "auto",
    "allow": [
      "mcp__brain__brain_teach_knowledge",
      "mcp__brain__brain_retrieve_knowledge",
      "mcp__brain__brain_ask_oracle"
    ]
  }
}
```

## Recovery When Transport Drops

The Brain MCP client SDK does **not** auto-reconnect. Symptoms:

- `brain_*` tool returns "Server not initialized"
- Tool returns "session not found" for an in-flight session
- Tools don't appear in your function list for the session

Recovery procedure (in order):

1. **`/mcp`** in Claude Code → look for the Brain server → reconnect
2. If `/mcp` doesn't restore it: **fully restart Claude Code** (not just `/compact` — exit and reopen)
3. Retry the call. Do not loop on a failing call — the session is gone and retrying won't recover it.

## Knowledge Item Schema

Each `brain_teach_knowledge` call expects:

```json
{
  "trigger": "when this happens / what user might say / what situation arises",
  "rule": "what to do, written as an imperative instruction",
  "rationale": "why this rule exists (context, root cause, evidence)",
  "type": "rule | procedure | pattern | anti-pattern | tip | checklist | security | environment | presentation | debugging | fact",
  "source": "where this rule was learned (project, version, file, URL)",
  "scope": "user | project",
  "projectId": "<required if scope=project>"
}
```

### Writing good triggers

A trigger should match what a future agent would *observe* or what a user would *say*, not internal jargon. Compare:

- **Weak trigger**: "v8.4.5 import bug"
- **Strong trigger**: "metric silently reports wrong number; diagnostic counter never increments"

The Brain's retrieval matches on trigger + rule semantic content, so triggers should be phrased the way the problem would surface in a future session.

## Distillation Best Practices

When extracting `learnings` for `brain_report_session_outcome`:

- Aim for 0–5 items, not 20. Distillation > volume.
- Each learning should be **durable** (applies to future tasks, not just this one).
- Especially valuable: user corrections, rejected approaches, root-cause discoveries.
- A session closed without learnings only gets mined from a thin summary — the explicit `learnings` array is the highest-signal input.

## See Also

- [Knowledge Management Paradigm](../KNOWLEDGE_MANAGEMENT.md) — internal `.claude-patterns/` storage vs external Brain
- [Known Issues](../KNOWN_ISSUES.md) — Brain MCP oracle ranking behavior
- [Approach and Method](../APPROACH_AND_METHOD.md) — methodology bullets on Brain integration
- Brain MCP server instructions (provided at session start when the MCP is connected)
