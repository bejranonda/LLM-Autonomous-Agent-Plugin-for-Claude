# Known Issues & Stabilization Roadmap (v8.3.0+)

The v8.3.0 release focused on dashboard reliability and dead code removal. Below are currently identified operational constraints:

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

## Reporting Issues
If you encounter issues, ensure you are running v8.1.0+ installed via `/plugin install`. Run validation with `/validate:plugin`.
