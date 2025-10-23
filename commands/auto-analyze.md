---
name: auto-analyze
description: Autonomously analyze the project with automatic skill selection and pattern learning
---

# Auto-Analyze Command

Analyze the current project autonomously using the orchestrator agent. This will:

- Auto-detect project type and technologies
- Load relevant skills based on project context
- Run code analysis in background
- Generate comprehensive quality report
- Store learned patterns for future use

The orchestrator will make all decisions autonomously without requiring confirmation at each step.

## How It Works

1. **Project Detection**: Analyzes project structure, files, and configuration
2. **Context Analysis**: Determines project type, languages, and frameworks
3. **Skill Loading**: Auto-selects relevant skills based on context
4. **Analysis Execution**: Runs comprehensive code analysis
5. **Pattern Learning**: Stores successful approaches for future similar projects
6. **Report Generation**: Creates detailed analysis report

**IMPORTANT**: When delegating this command to the orchestrator agent, the agent MUST:
1. Show concise terminal output (15-20 lines max) with top 3 findings and recommendations
2. Save detailed report to `.claude/reports/auto-analyze-YYYY-MM-DD.md` with ALL findings
3. Include file path in terminal output
4. Never complete silently, never show 50+ lines in terminal

## Usage

```bash
/auto-analyze
```

## Example Output

The orchestrator MUST use two-tier presentation:

### Terminal Output (Concise)

```
✓ Auto-Analyze Complete - Quality: 88/100

Key Findings:
• Python/FastAPI project, 127 files analyzed
• 4 failing tests in auth module
• 12 functions missing docstrings

Top Recommendations:
1. [HIGH] Fix failing auth tests → +4 quality points
2. [MED]  Add docstrings to public APIs
3. [MED]  Refactor high-complexity functions

📄 Full report: .claude/reports/auto-analyze-2025-10-21.md
⏱ Completed in 2.3 minutes
```

### File Report (Detailed)

Saved to `.claude/reports/auto-analyze-2025-10-21.md`:

```
═══════════════════════════════════════════════════════
  AUTO-ANALYZE DETAILED REPORT
═══════════════════════════════════════════════════════
Generated: 2025-10-21 14:30:00

┌─ Project Context ────────────────────────────────────┐
│ Type: Python project with FastAPI framework          │
│ Languages: Python 3.9+                                │
│ Frameworks: FastAPI, SQLAlchemy, Pydantic            │
│ Total Files: 127                                      │
│ Lines of Code: 12,450                                 │
└───────────────────────────────────────────────────────┘

┌─ Quality Assessment ─────────────────────────────────┐
│ Overall Score: 88/100 ✓                              │
│ Tests: 45 tests, 92% passing (41/45)                 │
│ Coverage: 82%                                         │
│ Standards: 89% compliant                              │
│ Documentation: 85% complete                           │
│ Pattern Adherence: 95%                                │
└───────────────────────────────────────────────────────┘

┌─ Strengths ──────────────────────────────────────────┐
│ • Well-structured API endpoints                       │
│ • Good test coverage on core modules                  │
│ • Consistent coding style                             │
│ • Clear separation of concerns                        │
│ • Effective use of Pydantic for validation           │
└───────────────────────────────────────────────────────┘

┌─ Issues Found ───────────────────────────────────────┐
│ Tests:                                                │
│ • test_user_login() - AssertionError (auth.py:45)   │
│ • test_token_refresh() - Timeout (auth.py:89)       │
│ • test_logout() - Connection error (auth.py:112)    │
│ • test_password_reset() - Invalid state (auth.py:145)│
│                                                       │
│ Documentation:                                        │
│ • 12 functions missing docstrings                     │
│ • API endpoint documentation incomplete              │
│                                                       │
│ Complexity:                                           │
│ • get_user_permissions() - Cyclomatic: 18 (auth.py) │
│ • validate_token() - Cyclomatic: 16 (auth.py)       │
│ • process_payment() - Cyclomatic: 15 (payment.py)   │
└───────────────────────────────────────────────────────┘

┌─ All Recommendations ────────────────────────────────┐
│ 1. [HIGH] Fix 4 failing tests in auth module         │
│    → Expected quality impact: +4 points               │
│    → Run /quality-check for auto-fix                  │
│                                                       │
│ 2. [MED] Add docstrings to 12 public functions       │
│    → Improves maintainability and API documentation  │
│    → Expected quality impact: +2 points               │
│                                                       │
│ 3. [MED] Refactor 3 high-complexity functions        │
│    → Target: get_user_permissions(), validate_token()│
│    → Expected quality impact: +2 points               │
│                                                       │
│ 4. [LOW] Complete API endpoint documentation         │
│    → Add OpenAPI descriptions                         │
│    → Expected quality impact: +1 point                │
└───────────────────────────────────────────────────────┘

Skills Loaded: code-analysis, quality-standards, pattern-learning
Agents Used: code-analyzer, background-task-manager
Patterns Stored: 1 new pattern in .claude-patterns/
Analysis Time: 2.3 minutes

═══════════════════════════════════════════════════════
```

## See Also

- `/quality-check` - Comprehensive quality control with auto-fix
- `/learn-patterns` - Initialize pattern learning database
