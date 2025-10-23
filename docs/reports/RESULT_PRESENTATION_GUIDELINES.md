# Result Presentation Guidelines

## Purpose

This document provides strict guidelines for presenting results after completing tasks, especially when executing slash commands. These guidelines ensure users receive clear, actionable, and concise feedback.

## Core Principles

1. **NEVER complete a task silently.** Users must always see key results.
2. **Be CONCISE in terminal output.** Show summary only - save details to file.
3. **Always provide file path** for detailed results that users can review later.

## Two-Tier Result Strategy

### Tier 1: Concise Terminal Output (REQUIRED)
Show in terminal immediately:
- ✓ Overall status and key metrics (1-3 lines)
- ✓ Most important findings (top 3 max)
- ✓ Critical recommendations (top 3 max)
- ✓ File path to detailed report

### Tier 2: Detailed File Report (REQUIRED)
Save to file for user review:
- ✓ Complete analysis and breakdown
- ✓ All findings and metrics
- ✓ Comprehensive recommendations
- ✓ Charts, graphs, and visualizations
- ✓ Full context and explanations

### When to Use This Strategy

Apply two-tier presentation after:
- ✓ Executing any slash command (`/auto-analyze`, `/quality-check`, etc.)
- ✓ Completing autonomous analysis or quality checks
- ✓ Delegating to specialized agents that produce findings
- ✓ Running background tasks that generate insights
- ✓ Any significant task that produces detailed results

## Standard Result Format

### Concise Terminal Output Template

```
✓ [TASK NAME] Complete - Quality: XX/100

Key Results:
• [Most important finding #1]
• [Most important finding #2]
• [Most important finding #3]

Top Recommendations:
1. [HIGH] [Critical action needed]
2. [MED]  [Important improvement]
3. [LOW]  [Optional enhancement]

📄 Full report: .claude/reports/[task-name]-YYYY-MM-DD.md
⏱ Completed in X.X minutes
```

**Length Limit**: Maximum 15-20 lines in terminal

### Detailed File Report Template

Saved to `.claude/reports/[task-name]-YYYY-MM-DD.md`:

```
═══════════════════════════════════════════════════════
  [TASK NAME] DETAILED REPORT
═══════════════════════════════════════════════════════
Generated: YYYY-MM-DD HH:MM:SS

┌─ [Section Title] ────────────────────────────────────┐
│ [Complete content with all details]                   │
│ [All metrics, charts, and analysis]                   │
└───────────────────────────────────────────────────────┘

┌─ [Another Section] ──────────────────────────────────┐
│ [Full breakdown]                                      │
└───────────────────────────────────────────────────────┘

[All remaining sections with comprehensive information]

═══════════════════════════════════════════════════════
```

### Formatting Rules

1. **Header Line**: Use `═` for top and bottom borders (55 characters wide)
2. **Section Boxes**: Use `┌─┐└─┘│` for box drawing (55 characters wide)
3. **Alignment**: Left-align content with 1 space padding inside boxes
4. **Spacing**: Single blank line between sections
5. **Symbols**: Use ✓, ✗, ⚠, ↑, ↓, → for status indicators
6. **Priority Tags**: Use [HIGH], [MED], [LOW] for recommendations

### Required Sections

Every **terminal output** MUST include:
1. **Status Line**: Task name, completion status, key metric
2. **Key Results**: Top 3 most important findings only
3. **Top Recommendations**: Top 3 actions only
4. **File Path**: Where to find detailed report
5. **Execution Time**: How long it took

Every **file report** MUST include:
1. **Header**: Task name, timestamp, metadata
2. **Complete Results**: All metrics and findings
3. **Detailed Breakdown**: Full analysis by category
4. **All Recommendations**: Prioritized and explained
5. **Charts/Visualizations**: When applicable
6. **Footer**: Summary and next steps

## Command-Specific Formats

### /auto-analyze Results

**Terminal Output** (concise):
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

**File Report** (detailed):
Save to `.claude/reports/auto-analyze-YYYY-MM-DD.md` with:
1. Project Context (full details)
2. Quality Assessment (complete breakdown)
3. Key Findings (all strengths and issues)
4. Recommendations (all, prioritized)
5. Pattern Learning Status
6. Metadata and charts

### /quality-check Results

**Terminal Output** (concise):
```
✓ Quality Check Complete - Score: 88/100 (↑ +5)

Quality Breakdown:
• Tests: 26/30 (45 passed, 2 failed)
• Standards: 18/25 (18 violations fixed)
• Documentation: 19/20 (97% complete)

Auto-Fixed:
• 12 style violations, 3 docstrings added

Top Issues:
1. [HIGH] 2 failing tests in auth module
2. [MED]  6 style violations need manual review

📄 Full report: .claude/reports/quality-check-2025-10-21.md
⏱ Completed in 1.8 minutes
```

**File Report** (detailed):
Save to `.claude/reports/quality-check-YYYY-MM-DD.md` with complete breakdown, all auto-fix actions, all remaining issues, trend analysis.

### /learn-patterns Results

**Terminal Output** (concise):
```
✓ Pattern Learning Initialized

Project Detected:
• Python/FastAPI project, 127 files
• 5 initial patterns identified
• Database created: .claude-patterns/

Next Steps:
1. Run /auto-analyze to establish quality baseline
2. Run /quality-check to assess current state
3. Start working - system learns automatically!

📄 Full report: .claude/reports/learn-patterns-2025-10-21.md
⏱ Completed in 0.8 minutes
```

**File Report** (detailed):
Save to `.claude/reports/learn-patterns-YYYY-MM-DD.md` with complete project analysis, all detected patterns, baseline metrics, framework details.

### /performance-report Results

**Terminal Output** (concise):
```
✓ Performance Report Generated

Executive Summary:
• 47 patterns learned, 67% reuse rate
• Quality trend: ↑ +18% (30 days)
• Top skill: pattern-learning (92% success)

Top Recommendations:
1. [HIGH] Use pattern-learning more often → +12 points avg
2. [HIGH] Run quality-controller before completion → +13 points
3. [MED]  Delegate testing to test-engineer → 91% success

📄 Full report: .claude/reports/performance-2025-10-21.md
   Includes: Charts, trends, complete metrics
⏱ Completed in 0.5 minutes
```

**File Report** (detailed):
Save to `.claude/reports/performance-YYYY-MM-DD.md` with complete dashboard, ASCII charts, all metrics, trend analysis, skill/agent performance details.

### /recommend Results

**Terminal Output** (concise):
```
✓ Recommendations Ready - Task: "Refactor auth module"

Recommended Approach (92% confidence):
• Expected Quality: 94/100 (+19 from baseline)
• Estimated Time: 12-15 minutes
• Skills: code-analysis, quality-standards, pattern-learning
• Agents: code-analyzer, quality-controller

Alternatives:
• Minimal (10 min, quality 82) - faster but lower quality
• Comprehensive (20 min, quality 91) - slower but thorough

Risk Level: MEDIUM - Legacy code complexity
→ Mitigation: Use code-analyzer first, add 5 min buffer

📄 Full report: .claude/reports/recommend-2025-10-21.md
   Includes: Detailed comparisons, risk analysis, insights
```

**File Report** (detailed):
Save to `.claude/reports/recommend-YYYY-MM-DD.md` with complete approach details, all alternatives, full risk assessment, confidence analysis, skill synergies.

## Visual Elements

### Status Indicators

- ✓ Success, completed, passing
- ✗ Failure, missing, not done
- ⚠ Warning, needs attention
- → Result, outcome, leads to
- ↑ Improvement, increase
- ↓ Decline, decrease

### Progress Bars (ASCII)

For skill performance or metrics visualization:
```
skill-name          ████████████ 92% (12 tasks)
another-skill       ███████████░ 88% (15 tasks)
```

Use █ for filled portions, ░ for unfilled (12 characters total width)

### Trend Charts (ASCII)

For quality over time:
```
100 │                            ●
 90 │        ●──●──●        ●──●─┘
 80 │    ●──┘              ┌┘
 70 │●───┘                 │ (threshold)
 60 │
    └────────────────────────────────────
    Week 1  Week 2  Week 3  Week 4
```

Use ● for data points, ─│┌┐└┘ for lines

### Priority Tags

Recommendations must be tagged:
- [HIGH] - Critical, immediate action needed
- [MED] - Important, should address soon
- [LOW] - Nice to have, address when time permits

## Content Guidelines

### Be Specific

❌ Bad: "Tests are mostly passing"
✓ Good: "45 passed, 2 failed | 88% coverage"

❌ Bad: "Quality improved"
✓ Good: "Quality improved from 83 → 88 (+5 points)"

❌ Bad: "Some issues found"
✓ Good: "• 4 failing tests in auth module
         • 12 functions missing docstrings"

### Be Actionable

Every recommendation should include:
- What to do
- Why it matters (impact/benefit)
- How to do it (if not obvious)

Example:
```
1. [HIGH] Fix failing auth tests
   → Expected +4 quality points
   → Affects: user login and token refresh
```

### Be Concise Yet Comprehensive

- Focus on important results, not verbose explanations
- Use bullet points for lists
- Group related items
- Omit unnecessary details
- Include enough context to understand findings

### Show Impact

Always quantify impact when possible:
- Quality score changes: "+5 points"
- Time savings: "25% faster"
- Success rates: "92% success rate"
- Comparisons: "from 83 → 88"

## Anti-Patterns to Avoid

### ❌ Silent Completion

Never:
- Complete without showing results
- Return only status codes or boolean values
- Provide minimal "Done" messages
- Skip presenting findings because task succeeded

### ❌ Too Verbose in Terminal

Never:
- Show 50+ lines of detailed output in terminal
- Include all charts and visualizations in terminal
- Present every single finding in terminal
- Omit the file path to detailed report

### ❌ No Detailed Report File

Never:
- Save only terminal output without detailed file
- Omit file path from terminal output
- Skip creating the report file
- Provide incomplete file reports

### ❌ Vague Information

Never:
- Use ambiguous terms ("some", "mostly", "a few")
- Provide metrics without context
- Give recommendations without expected impact
- Show errors without file/line references

### ❌ Wrong Balance

Never:
- Show too little in terminal (just "Done")
- Show too much in terminal (complete report)
- Create empty or minimal file reports
- Forget to mention where detailed report is saved

## Integration with Orchestrator

The orchestrator agent is responsible for:
1. Executing the command/task
2. Collecting all results from delegated agents
3. **Creating detailed report file** in `.claude/reports/`
4. **Presenting concise summary** to terminal (15-20 lines max)
5. **Including file path** to detailed report

The orchestrator must ALWAYS:
- Save complete results to `.claude/reports/[command]-YYYY-MM-DD.md`
- Show concise summary in terminal (key results + top 3 recommendations)
- Include file path in terminal output
- Keep terminal output under 20 lines

The orchestrator must NEVER:
- Show 50+ lines of detailed results in terminal
- Skip creating the detailed report file
- Omit the file path from terminal output
- Complete silently without any terminal output

## Quality Checklist

Before presenting results, verify:

**Terminal Output:**
- [ ] Concise (15-20 lines maximum)
- [ ] Shows key metric/status on first line
- [ ] Lists top 3 findings only
- [ ] Lists top 3 recommendations only
- [ ] Includes file path to detailed report
- [ ] Shows execution time
- [ ] Uses clear status indicators (✓, ⚠, →)

**File Report:**
- [ ] Saved to `.claude/reports/[command]-YYYY-MM-DD.md`
- [ ] Header identifies task and timestamp
- [ ] All metrics and findings included
- [ ] All recommendations prioritized and explained
- [ ] Charts/visualizations when applicable
- [ ] Metadata includes agents, skills, execution time
- [ ] Visual formatting consistent (boxes, alignment)
- [ ] Specific numbers/examples provided (not vague)
- [ ] Impact quantified where possible

## Examples of Good vs. Bad

### ❌ Bad Example #1 (Too Silent)
```
Analysis complete. Quality: 88.
```

### ❌ Bad Example #2 (Too Verbose - 50+ lines in terminal)
```
═══════════════════════════════════════════════════════
  AUTO-ANALYZE COMPLETED
═══════════════════════════════════════════════════════

┌─ Project Context ────────────────────────────────────┐
│ Type: Python project with FastAPI framework          │
│ Languages: Python 3.9+                                │
│ Frameworks: FastAPI, SQLAlchemy, Pydantic            │
│ Total Files: 127                                      │
│ [... 40 more lines ...]
└───────────────────────────────────────────────────────┘
```
(User has to scroll through terminal to see everything)

### ✓ Good Example (Concise Terminal + Detailed File)

**Terminal Output:**
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

**File Report** (.claude/reports/auto-analyze-2025-10-21.md):
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
│ [... complete details ...]
└───────────────────────────────────────────────────────┘

[... all remaining sections with full details ...]
```

## Conclusion

Following these guidelines ensures users receive:
- **Concise terminal output** they can quickly scan (15-20 lines)
- **Detailed file reports** they can review when needed
- **Clear file paths** to find comprehensive information
- **Actionable insights** for next steps
- **Transparency** without overwhelming terminal output

**Remember**:
- Terminal output = Quick summary only (15-20 lines max)
- File report = Complete details with all findings
- Always include file path in terminal output
- Never complete silently, never overwhelm with details
