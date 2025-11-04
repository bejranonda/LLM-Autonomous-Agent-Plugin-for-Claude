---
name: analyze:static
description: Run 40+ linters across all languages with intelligent deduplication and unified reporting
delegates-to: orchestrator
---

# Static Analysis Command

Execute comprehensive static analysis across your codebase using 40+ industry-standard linters, with intelligent result deduplication and unified reporting.

## Usage

```bash
/analyze:static [PATH] [OPTIONS]
```

**Examples**:
```bash
/analyze:static                    # Analyze current directory
/analyze:static src/               # Analyze specific directory
/analyze:static src/auth.py        # Analyze specific file
/analyze:static --quick            # Fast analysis (fewer linters)
/analyze:static --security         # Security-focused analysis
```

## Supported Languages and Linters

### Python (10 linters)
- **pylint** - Code quality, bugs, style
- **flake8** - Style guide enforcement
- **mypy** - Static type checking
- **bandit** - Security vulnerability scanning
- **pycodestyle** - PEP 8 style checking
- **pydocstyle** - Docstring conventions
- **vulture** - Dead code detection
- **radon** - Complexity metrics
- **mccabe** - Cyclomatic complexity
- **pyflakes** - Error detection

### JavaScript/TypeScript (5 linters)
- **eslint** - Code quality, bugs, style
- **tslint** - TypeScript-specific linting
- **jshint** - JavaScript error detection
- **prettier** - Code formatting
- **standard** - JavaScript Standard Style

### Multi-Language (3 linters)
- **semgrep** - Security & bug detection (Python, JS, TS, Go, Java)
- **sonarqube** - Comprehensive code quality
- **codeql** - Advanced security scanning

### Go (4 linters)
- **golint** - Style checking
- **govet** - Correctness checking
- **staticcheck** - Advanced static analysis
- **golangci-lint** - Meta-linter (runs 50+ linters)

### Rust (2 linters)
- **clippy** - Comprehensive linting
- **rustfmt** - Code formatting

### Java (3 linters)
- **checkstyle** - Style checking
- **pmd** - Code quality
- **spotbugs** - Bug detection

### C/C++ (3 linters)
- **cppcheck** - Bug and security detection
- **clang-tidy** - Modernization and bug detection
- **cpplint** - Style guide enforcement

### Ruby (2 linters)
- **rubocop** - Style and quality
- **reek** - Code smell detection

### PHP (3 linters)
- **phpcs** - Coding standards
- **phpstan** - Static analysis
- **psalm** - Type system analysis

### Other Languages
- **shellcheck** - Bash/shell script analysis
- **stylelint** - CSS/SCSS/LESS linting
- **sqlfluff** - SQL linting
- **yamllint** - YAML validation
- **markdownlint** - Markdown linting
- **hadolint** - Dockerfile best practices

**Total**: 40+ linters across 15+ languages

## How It Works

### 1. Language Detection

Automatically detects languages in target path:

```python
Detected Languages:
- Python (.py files)
- JavaScript (.js files)
- TypeScript (.ts files)
- CSS (.css files)
```

### 2. Linter Selection

Selects appropriate linters based on detected languages:

```python
Enabled Linters (12):
✅ pylint        (Python quality)
✅ flake8        (Python style)
✅ mypy          (Python typing)
✅ bandit        (Python security)
✅ eslint        (JS/TS quality)
✅ prettier      (JS/TS formatting)
✅ stylelint     (CSS quality)
...
```

### 3. Parallel Execution

Runs linters in parallel for maximum speed:

```python
Running Analysis...
[████████████████████████████████] 12/12 linters (8 parallel workers)

Results:
✅ pylint      (2.3s) - 47 issues
✅ flake8      (1.1s) - 23 issues
✅ mypy        (3.5s) - 12 issues
✅ bandit      (1.8s) - 3 issues
✅ eslint      (4.2s) - 31 issues
...
```

### 4. Result Synthesis

Intelligently deduplicates and synthesizes results:

```python
Synthesis:
- Total Issues Found: 152
- Duplicate Issues: 36
- Unique Issues: 116

Deduplication:
- Same issue from multiple linters
- Different rule IDs for same problem
- Fingerprinting-based matching
```

### 5. Quality Score Calculation

```python
Quality Score (0-100) =
    100 - (
        Critical × 10 +
        Error × 5 +
        Warning × 2 +
        Info × 1 +
        Style × 0.5
    )

Example:
- Critical: 2 → -20 points
- Error: 8 → -40 points
- Warning: 15 → -30 points
- Info: 10 → -10 points
- Style: 20 → -10 points
---


---------------------
Score: 100 - 110 = 0 (capped at 0)
```

**Scoring Bands**:
- 90-100: Excellent
- 70-89: Good
- 50-69: Needs Improvement
- 0-49: Critical Issues

## Output Format

### Terminal Output (Tier 1: Concise Summary)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STATIC ANALYSIS COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Quality Score: 78/100 (GOOD)

🔍 Analysis Summary
   Languages: Python, JavaScript, CSS
   Linters: 12 run, 0 failed
   Total Issues: 116 unique (36 duplicates removed)

🚨 Issues by Severity
   🔴 Critical: 2
   🟠 Error: 8
   🟡 Warning: 15
   🔵 Info: 10
   ⚪ Style: 81

📂 Top 3 Files
   1. src/auth.py - 23 issues
   2. src/api.js - 18 issues
   3. src/utils.py - 12 issues

🎯 Top 3 Issues
   1. CRITICAL - SQL injection risk (src/auth.py:45)
   2. ERROR - Undefined variable (src/api.js:112)
   3. ERROR - Type mismatch (src/utils.py:78)

✅ Auto-fixable: 45/116 issues

📄 Detailed Report: .reports/static-analysis-2025-01-15.md

⏱️  Analysis completed in 12.4s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### File Report (Tier 2: Comprehensive)

Saved to `.reports/static-analysis-{DATE}.md`:

```markdown
# Static Analysis Report
**Generated**: 2025-01-15 14:23:45
**Path**: /project/src
**Quality Score**: 78/100

---

## Summary

**Languages Detected**: Python, JavaScript, TypeScript, CSS
**Linters Executed**: 12
**Total Issues**: 116 (36 duplicates removed)
**Duration**: 12.4s

---

## Issues by Severity

| Severity | Count | Percentage |
|----------|-------|-----------|
| 🔴 Critical | 2 | 1.7% |
| 🟠 Error | 8 | 6.9% |
| 🟡 Warning | 15 | 12.9% |
| 🔵 Info | 10 | 8.6% |
| ⚪ Style | 81 | 69.8% |

---

## Issues by Category

- **Security**: 5 issues
- **Bug**: 12 issues
- **Code Quality**: 23 issues
- **Style**: 81 issues
- **Typing**: 8 issues
- **Performance**: 3 issues
- **Documentation**: 2 issues

---

## Top 10 Files with Issues

1. `src/auth.py` - 23 issues
2. `src/api.js` - 18 issues
3. `src/utils.py` - 12 issues
4. `src/components/Button.tsx` - 10 issues
5. `src/database.py` - 9 issues
6. `src/helpers.js` - 8 issues
7. `src/styles/main.css` - 7 issues
8. `src/config.py` - 6 issues
9. `src/routes.js` - 5 issues
10. `src/models.py` - 4 issues

---

## Linter Execution Results

### Successful (12)
- ✅ **pylint** (2.3s) - 47 issues
- ✅ **flake8** (1.1s) - 23 issues
- ✅ **mypy** (3.5s) - 12 issues
- ✅ **bandit** (1.8s) - 3 issues
- ✅ **eslint** (4.2s) - 31 issues
- ✅ **prettier** (0.8s) - 15 issues
- ✅ **stylelint** (1.2s) - 7 issues
- ✅ **semgrep** (5.3s) - 8 issues
- ✅ **pycodestyle** (0.9s) - 18 issues
- ✅ **pydocstyle** (1.0s) - 12 issues
- ✅ **radon** (0.7s) - 4 issues
- ✅ **shellcheck** (0.5s) - 2 issues

### Failed (0)
None

---

## Critical and High Priority Issues

### src/auth.py:45
**Severity**: CRITICAL
**Category**: security
**Linter**: bandit
**Rule**: B608 (SQL injection)
**Message**: Possible SQL injection vector through string-based query construction

**Auto-fixable**: ✅ Yes

**Suggested Fix**:
```python
# Before
query = f"SELECT * FROM users WHERE username = '{username}'"

# After
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

---

### src/api.js:112
**Severity**: ERROR
**Category**: bug
**Linter**: eslint
**Rule**: no-undef
**Message**: 'response' is not defined

**Auto-fixable**: ❌ No

**Context**:
```javascript
110: function handleRequest(request) {
111:   processRequest(request);
112:   return response.json();  // ← 'response' not defined
113: }
```

---

### src/utils.py:78
**Severity**: ERROR
**Category**: typing
**Linter**: mypy
**Rule**: assignment
**Message**: Incompatible types in assignment (expression has type "str", variable has type "int")

**Auto-fixable**: ⚠️ Suggest manual fix

**Context**:
```python
76: def calculate_age(birth_year: int) -> int:
77:   current_year = 2025
78:   age = current_year - birth_year
79:   age = str(age)  # ← Type error: int expected, str assigned
80:   return age
```

---

[... continues with all critical/error issues ...]

---

## Fixable Issues Summary

**Total Auto-fixable**: 45/116 (38.8%)

### By Category
- **Style**: 38 auto-fixable
- **Code Quality**: 5 auto-fixable
- **Security**: 2 auto-fixable

Apply all fixes:
```bash
/apply-static-analysis-fixes
```

Apply specific fixes:
```bash
/apply-fix {issue-fingerprint}
```

---

## Quality Score Breakdown

```
Base Score: 100

Penalties:
- Critical (2 × 10): -20
- Error (8 × 5): -40
- Warning (15 × 2): -30
- Info (10 × 1): -10
- Style (81 × 0.5): -40.5

Total Penalty: -140.5 (capped at 100)
Final Score: 0 → Adjusted to actual: 78/100

Note: Score uses weighted algorithm with diminishing returns
```

**Score Interpretation**:
- ✅ **70-100**: Production ready
- ⚠️ **50-69**: Needs improvement
- ❌ **0-49**: Critical issues require attention

**Current Status**: ✅ GOOD (78/100)

---

## Recommendations

### Critical Actions (2)
1. **Fix SQL injection vulnerability** (src/auth.py:45)
   - Use parameterized queries
   - Auto-fixable: Yes

2. **Fix critical type error** (src/database.py:123)
   - Review type annotations
   - Auto-fixable: No (requires manual review)

### Suggested Improvements (8)
1. **Add type hints** to 12 functions
2. **Fix undefined variables** in 3 locations
3. **Improve error handling** in 5 functions
4. **Add missing docstrings** to 15 functions
5. **Reduce complexity** in 4 functions
6. **Remove unused imports** in 8 files
7. **Fix naming conventions** in 6 variables
8. **Update deprecated syntax** in 3 files

### Style Improvements (81)
- Run auto-formatter on all files
- Apply `black` for Python
- Apply `prettier` for JavaScript/TypeScript
- Apply `stylelint --fix` for CSS

---

## Next Steps

1. **Address Critical Issues**: Fix 2 critical security vulnerabilities
2. **Apply Auto-fixes**: Run `/apply-static-analysis-fixes` for 45 fixable issues
3. **Manual Review**: Review 8 error-level issues requiring manual fixes
4. **Continuous Monitoring**: Integrate into CI/CD pipeline
5. **Re-run Analysis**: Verify quality score improvement

**Target Score**: 85+/100 (Excellent)

---

**End of Report**
```

## Advanced Options

### Quick Analysis (Fast Mode)

```bash
/analyze:static --quick
```

**Features**:
- Runs only essential linters (10-15)
- Skips style-only linters
- Focuses on bugs and security
- 3-5x faster execution

**Use Case**: Rapid feedback during development

### Security-Focused Analysis

```bash
/analyze:static --security
```

**Features**:
- Runs only security linters
- Deep vulnerability scanning
- OWASP Top 10 focused
- SARIF output for CI/CD

**Linters**:
- bandit (Python)
- semgrep (multi-language)
- codeql (multi-language)
- eslint security plugins
- shellcheck
- hadolint

### Category-Specific Analysis

```bash
/analyze:static --category=typing     # Only type checking
/analyze:static --category=style      # Only style checking
/analyze:static --category=complexity # Only complexity analysis
```

### Output Formats

```bash
/analyze:static --format=json         # JSON output
/analyze:static --format=sarif        # SARIF for CI/CD
/analyze:static --format=html         # HTML report
```

## Integration with Learning System

The static analysis system integrates with pattern learning:

```python
# After each analysis
learning_engine.store_pattern({
    "task_type": "static_analysis",
    "context": {
        "languages": detected_languages,
        "linters_used": linters_run,
        "issues_found": total_issues
    },
    "execution": {
        "duration": total_duration,
        "parallel_workers": 8
    },
    "outcome": {
        "quality_score": 78,
        "fix_success_rate": 0.92
    }
})

# Future analyses benefit from:
- Learned false positive patterns
- Optimal linter combinations
- Expected issue distributions
- Quality score trends
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Static Analysis
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Static Analysis
        run: |
          /analyze:static --format=sarif --output=results.sarif
      - name: Upload Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
```

### GitLab CI Example

```yaml
static-analysis:
  stage: test
  script:
    - /analyze:static --format=json --output=results.json
  artifacts:
    reports:
      codequality: results.json
```

## Performance Expectations

| Project Size | Files | Linters | Duration | Workers |
|-------------|-------|---------|----------|---------|
| Small | <50 | 8 | 5-15s | 4 |
| Medium | 50-200 | 12 | 15-60s | 8 |
| Large | 200-1000 | 15 | 1-5min | 12 |
| XLarge | 1000+ | 20+ | 5-15min | 16 |

**Optimization**:
- Parallel execution (default: 8 workers)
- Incremental analysis (only changed files)
- Caching of linter installations
- Smart linter selection

## Troubleshooting

### Issue: Linter Not Found

```
❌ pylint not installed
```

**Solution**:
```bash
pip install pylint flake8 mypy bandit
npm install -g eslint prettier
```

### Issue: Timeout

```
⚠️ semgrep timeout after 60s
```

**Solution**:
```bash
/analyze:static --timeout=120  # Increase timeout
```

### Issue: Too Many Style Issues

```
⚪ Style: 500 issues
```

**Solution**:
```bash
# Run auto-formatter first
black .
prettier --write .

# Then analyze
/analyze:static
```

## Best Practices

1. **Run Before Commit**: Integrate into pre-commit hooks
2. **Target Score 85+**: Aim for "Excellent" quality
3. **Fix Critical First**: Address security and errors before style
4. **Use Auto-Fix**: Apply 38% of fixes automatically
5. **Regular Analysis**: Run daily or per commit
6. **Track Trends**: Monitor quality score over time
7. **Team Standards**: Configure linters for team preferences

---

This command provides comprehensive static analysis with minimal configuration, intelligent result synthesis, and actionable recommendations.
