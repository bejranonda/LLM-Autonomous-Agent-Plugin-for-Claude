---
name: quality-check
description: Run comprehensive quality control with autonomous auto-fixing
---

# Quality Check Command

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

## Usage

```bash
/quality-check
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

```
Quality Control Check Started
├── Tests: 45 passed, 2 failed → 88% coverage (26/30 points)
├── Standards: 18 violations found → 18/25 points
├── Documentation: Complete (19/20 points)
├── Patterns: Adheres to 8/8 patterns (15/15 points)
├── Metrics: Acceptable complexity (10/10 points)
├── Current Score: 88/100 ✓ PASS
├── Quality Trend: ↑ +5 from last check
└── Check complete in 1.8 minutes
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

- `/auto-analyze` - Autonomous project analysis
- `/learn-patterns` - Initialize pattern learning database
