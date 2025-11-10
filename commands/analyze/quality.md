---
name: analyze:quality
description: Run comprehensive quality control with autonomous auto-fixing
delegates-to: autonomous-agent:orchestrator
---


# Quality Check Command

## 🚨 CRITICAL: RESPONSE SAFETY REQUIREMENTS

**SYSTEM-WIDE FAILURE PREVENTION**: When generating ANY response content for this command, you MUST ensure:

1. **NEVER generate empty text blocks** - All content blocks must have non-empty text
2. **NEVER use Unicode box characters** (=, |, +, +, etc.) - Use safe ASCII alternatives
3. **ALWAYS provide fallback content** for any section that might be empty
4. **VALIDATE all content blocks** before finalizing response
5. **NEVER leave sections empty** - Provide default values for missing data

**SAFE RESPONSE PATTERN**:
- Use ASCII characters instead of Unicode box drawing
- Ensure every score section has actual numeric values
- Provide default content when data is missing
- Never return empty strings or whitespace-only content
- Always include actionable recommendations

**FAILURE TO COMPLY**: Will cause `cache_control cannot be set for empty text blocks` errors and break ALL Claude functionality.

Run comprehensive quality control check with autonomous fixing. This will:

- Run all tests and analyze coverage
- Check code standards compliance
- Verify documentation completeness
- Validate pattern adherence
- Auto-fix issues when possible
- Generate quality report with trends

## How It Works

1. **Test Execution**: Runs all tests and calculates coverage
2. **Standards Check**: Validates code against style and standards
3. **Documentation Review**: Checks for missing or incomplete docs
4. **Pattern Validation**: Verifies adherence to learned patterns
5. **Auto-Fix Loop**: Automatically fixes issues (repeats if needed)
6. **Quality Assessment**: Calculates overall quality score (0-100)
7. **Trend Analysis**: Compares against historical data

**IMPORTANT**: This command delegates to `autonomous-agent:orchestrator` which MUST present a detailed quality report to the user showing scores, test results, auto-fix actions, and specific recommendations. Silent completion is not acceptable.

## Usage

```bash
/analyze:quality
```

## Quality Scoring

- **Test Coverage**: 30 points (aim for >80%)
- **Code Standards**: 25 points (style, conventions)
- **Documentation**: 20 points (completeness)
- **Pattern Adherence**: 15 points (learned patterns)
- **Code Metrics**: 10 points (complexity, maintainability)

**Pass Threshold**: 70/100

If score < 70, auto-fix loop is triggered automatically.

## Example Output

The orchestrator MUST present results in this format:

```
============================================================
  QUALITY CHECK COMPLETED
============================================================

+-------------------------------------------------------+
| OVERALL QUALITY SCORE
+-------------------------------------------------------+
| Current Score: 88/100 [PASS]                         |
| Previous Score: 83/100                                |
| Trend: +5 points (improving)                          |
| Status: Above threshold (70+)                         |
+-------------------------------------------------------+

+-------------------------------------------------------+
| QUALITY BREAKDOWN
+-------------------------------------------------------+
| Tests (30 pts):         26/30 [PASS]                  |
|   45 passed, 2 failed | 88% coverage                 |
|                                                       |
| Standards (25 pts):     18/25 [WARN]                  |
|   18 style violations found                           |
|                                                       |
| Documentation (20 pts): 19/20 [PASS]                  |
|   97% of public APIs documented                       |
|                                                       |
| Patterns (15 pts):      15/15 [PASS]                  |
|   Adheres to 8/8 learned patterns                     |
|                                                       |
| Metrics (10 pts):       10/10 [PASS]                  |
|   Acceptable complexity levels                        |
+-------------------------------------------------------+

+-------------------------------------------------------+
| AUTO-FIX ACTIONS TAKEN
+-------------------------------------------------------+
| * Fixed 12 style violations (auto-formatted)         |
| * Added 3 missing docstrings                          |
| * Updated 1 outdated dependency                       |
| * Quality improved from 83 -> 88 (+5 points)          |
+-------------------------------------------------------+

+-------------------------------------------------------+
| REMAINING ISSUES
+-------------------------------------------------------+
| Tests:                                                |
| * test_user_login() - AssertionError (auth.py:45)     |
| * test_token_refresh() - Timeout (auth.py:89)         |
|                                                       |
| Standards:                                            |
| * 6 violations require manual review                  |
|   (complex refactoring needed)                        |
+-------------------------------------------------------+

+-------------------------------------------------------+
| RECOMMENDATIONS
+-------------------------------------------------------+
| 1. [HIGH] Fix 2 failing tests in auth module          |
|    -> Expected +4 quality points                      |
| 2. [MED] Refactor complex functions flagged           |
|    -> Expected +2 quality points                      |
| 3. [LOW] Review 6 manual style violations             |
|    -> Expected +1 quality point                       |
+-------------------------------------------------------+

Skills Loaded: quality-standards, testing-strategies
Agents Used: quality-controller, test-engineer
Auto-Fix Iterations: 2 (converged)
Patterns Stored: Quality pattern updated in .claude-patterns/
Check Time: 1.8 minutes

============================================================
```

## Auto-Fix Details

When quality < 70, the plugin will:
1. Run failing tests individually
2. Fix style violations
3. Generate missing documentation
4. Suggest pattern improvements
5. Re-check quality
6. Iterate up to 3 times

## See Also

- `/analyze:project` - Autonomous project analysis
- `/learn:init` - Initialize pattern learning database
