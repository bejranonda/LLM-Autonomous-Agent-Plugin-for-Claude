# Session Start Checklist

A pre-flight checklist for new Claude Code sessions working on this plugin. Run through these checks at the start of any session that expects to (a) use the optional Brain MCP server, (b) validate plugin changes, or (c) release a new version. Catches the most common "wasted half a session before noticing" failures.

## Triage (30 seconds)

Answer these three questions before doing anything else in the session:

1. **What's the plugin version?** — `grep '"version"' .claude-plugin/plugin.json` — confirms you're working on the version you think you are.
2. **Is the working tree clean?** — `git status --short` — surfaces leftover changes from prior sessions that should be committed or stashed before new work.
3. **Are there unpushed commits?** — `git log origin/main..main --oneline` — surfaces work that landed locally but didn't ship.

If any of these surface surprises, address them before starting new work.

## Brain MCP Connectivity Probe (10 seconds, if Brain is expected)

The Brain MCP client does **not** auto-reconnect on transport drop. A session that started after a server restart, 30-min orphan sweep, or network blip will silently have no `mcp__brain__*` tools available. Verify connectivity *before* relying on it:

```
1. Call mcp__brain__brain_get_user_style
   - Success: peer card + reflexes returned. Brain is healthy. Proceed.
   - "Server not initialized": transport dropped. See recovery below.
   - Tool not in function list: MCP not connected this session.
```

### Recovery (if probe fails)

| Symptom | Fix |
|---|---|
| "Server not initialized" | `/mcp` → Brain server → reconnect |
| Tool missing from function list | Fully restart Claude Code (not just `/compact`) |
| Worked yesterday, broken today | Same as above — Brain drops don't auto-heal |

Do **not** retry a failing `brain_*` call in a loop. The session is gone; the call will not recover on its own.

## Plugin Validator Sweep (5 seconds, before any release)

```
py lib/validate-claude-plugin.py
```

Expected: `Score: 100/100, Status: PERFECT`. If lower, fix before release. The validator checks:

- `plugin.json` and `marketplace.json` versions match (the v8.4.2 drift bug)
- Component counts (currently 36 agents / 27 skills / 41 commands / 61 lib)
- Markdown validity across all 490+ files
- Required directory structure

## Test Suite (3 seconds, before any release)

```
py -m pytest tests/ -q
```

Expected: `113 passed, 0 skipped, 0 warnings`. Any `skipped` result is a regression of the v8.4.0 test-integrity fix — the `try/except ImportError -> @pytest.mark.skipif` anti-pattern has crept back in. Any warnings should be investigated.

## Lint Sweep (1 second, before any release)

```
py -m ruff check .
```

Expected: `All checks passed!`. Ruff config is in `ruff.toml`.

## Release Readiness (when preparing a new version)

Before bumping the version, confirm:

- [ ] Validator: 100/100
- [ ] pytest: 113 passed / 0 skipped / 0 warnings
- [ ] ruff: clean
- [ ] Working tree has only intended changes (`git status` is clean except for staged work)
- [ ] No `TODO`/`FIXME` introduced in production code (only in approved placeholders)

After bumping the version, update **all five** places in lockstep (the v8.4.2 drift bug):

1. `.claude-plugin/plugin.json` → `"version": "X.Y.Z"`
2. `.claude-plugin/marketplace.json` → `"version": "X.Y.Z"`
3. `CLAUDE.md` → `**Version**: X.Y.Z` and the manifest comment
4. `README.md` → title, badge URL, new release-notes section
5. `CHANGELOG.md` → new `## [X.Y.Z] - YYYY-MM-DD` entry

The validator's marketplace-sync check will catch (1)↔(2) drift automatically, but not the other three. Be disciplined.

## Plugin Reload into Workspace (when testing a new release as user)

If you need to validate a new release without waiting for `/plugin update`, update three layers:

1. **Marketplace clone** at `~/.claude/plugins/marketplaces/<marketplace>/`:
   ```bash
   git fetch --tags origin
   git merge --ff-only origin/main
   ```
2. **Cache dir** at `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`:
   ```bash
   mkdir -p cache/<version>
   cp -r marketplace_clone/. cache/<version>/
   rm -rf cache/<version>/.git   # match clean-install shape
   ```
3. **Registry** at `~/.claude/plugins/installed_plugins.json`:
   - Update `installPath` to point at the new version dir
   - Update `version`
   - Update `gitCommitSha` (`git rev-parse <tag>`)
   - Update `lastUpdated`

**Claude Code only re-reads these at session start.** An in-session cache edit does not take effect until restart.

## Testing Commands Without Restart (pre-restart validation)

Slash commands aren't live until Claude Code restart. To validate a command's behavior before restart:

1. Read `commands/<category>/<name>.md` to find `delegates-to:` and any backing script
2. Invoke the backing `lib/*.py` directly with `CLAUDE_PLUGIN_ROOT` resolved to the new cache dir
3. Batch-validate YAML frontmatter (`name:` + `description:` keys) across all `agents/*.md`, `commands/**/*.md`, `skills/**/SKILL.md`

This catches regressions in the actual surface area (scripts + metadata) before users hit them.

## Pre-Commit Hook Awareness

If the session has `semgrep@claude-plugins-official` enabled in `~/.claude/settings.json` and you see:

> `Not logged into Semgrep Guardian. Ask the guardian mcp to login.`

…on every `Bash`/`Edit`/`Write` call, the Semgrep Guardian `PreToolUse` hook is failing closed. Recovery options:

- **Disable**: edit `~/.claude/settings.json`, set `"semgrep@claude-plugins-official": false`, fully restart Claude Code.
- **Authenticate**: `/mcp` → Semgrep Guardian → Login.

This is **not** a bug in this plugin (which ships no `PreToolUse` hooks). See `docs/KNOWN_ISSUES.md` "Editor hook may block edits" for details.

## Brain MCP Permission Self-Grant Guardrail

If you (the agent) attempt to edit `~/.claude/settings.json` to add `mcp__brain__*` to `permissions.allow` and the auto-mode classifier denies it with "Self-Modification that widens the agent's own permissions":

- **Do not** attempt to work around this. It is a deliberate safety property.
- **Do** surface the exact JSON to add to the user and let them apply it manually.

The same applies to editing `enabledPlugins` to re-enable a security hook the user disabled.

## See Also

- [`BRAIN_MCP_INTEGRATION_GUIDELINES.md`](BRAIN_MCP_INTEGRATION_GUIDELINES.md) — full Brain MCP integration protocol
- [`../KNOWN_ISSUES.md`](../KNOWN_ISSUES.md) — current known issues
- [`../APPROACH_AND_METHOD.md`](../APPROACH_AND_METHOD.md) — methodology and design principles
- [`../../CLAUDE.md`](../../CLAUDE.md) — project overview (read at every session start by Claude Code)
