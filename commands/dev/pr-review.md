---
name: dev:pr-review
description: CodeRabbit-style PR review with security scanning, test coverage, and one-click fixes
delegates-to: autonomous-agent:pr-reviewer
---

# Pull Request Review Command

Execute a comprehensive CodeRabbit-style review of a pull request with automated analysis, security scanning, and one-click fixes.

## Usage

```bash
/dev:pr-review [PR_NUMBER|BRANCH_NAME]
```

**Examples**:
```bash
/dev:pr-review 123              # Review PR #123
/dev:pr-review feature/auth     # Review branch against main
/dev:pr-review                  # Review current branch changes
```

## Workflow

### 1. Initialize Review
- Detect PR context (number, branch, or current changes)
- Fetch PR metadata (title, author, description)
- Extract git diff and commit history

### 2. Delegate to PR Reviewer Agent

Execute comprehensive review via `pr-reviewer` agent:

```javascript
const review_result = await delegate_to_pr_reviewer({
    pr_number: pr_number,
    pr_data: {
        title: pr_title,
        author: pr_author,
        description: pr_description,
        files: changed_files,
        diff: full_diff,
        commits: commit_history
    }
});
```

### 3. Analysis Pipeline

The PR reviewer agent executes:

**A. Summary Generation** (5-10s):
- Change categorization (features, bug fixes, refactoring, etc.)
- Files changed count and line statistics
- Complexity score calculation

**B. Line-by-Line Analysis** (30-60s):
- Code quality issues (naming, duplication, complexity)
- Best practice violations (SOLID, DRY, error handling)
- Performance concerns (N+1 queries, inefficient algorithms)
- Type annotations and documentation

**C. Security Scan** (20-40s via security-auditor):
- OWASP Top 10 vulnerability detection
- Input validation checks
- Authentication/authorization review
- Secrets exposure detection
- Dependency vulnerability scan

**D. Test Coverage Analysis** (15-30s):
- Calculate coverage for changed lines
- Identify untested functions
- Generate test suggestions
- Coverage delta calculation

**E. Automated Fix Generation** (10-20s):
- Generate one-click fixes for auto-fixable issues
- Provide suggestions with explanations
- Calculate confidence scores

**F. Risk Assessment** (5-10s):
- Calculate weighted risk score
- Identify risk factors (size, complexity, critical files)
- Generate recommendations

**G. Related PR Detection** (5-10s):
- Find PRs touching same files
- Detect similar changes
- Identify dependencies

### 4. Report Generation

Generate comprehensive review report:

```markdown
# Pull Request Review: #{PR_NUMBER}

## 📊 Summary
**Risk Level**: {RISK_LEVEL} ({RISK_SCORE}/100)
Files: {COUNT} | +{ADDITIONS} -{DELETIONS} | Complexity: {SCORE}/100

## 🔒 Security ({VULN_COUNT} issues)
🔴 Critical: {COUNT} | 🟠 High: {COUNT} | 🟡 Medium: {COUNT}

## 📈 Test Coverage
{COVERAGE}% ({DELTA > 0 ? '+' : ''}{DELTA}%) | Untested: {COUNT}

## 💡 Code Review ({ISSUE_COUNT} issues)
{DETAILED_REVIEWS_BY_FILE}

## ⚡ Performance ({ISSUE_COUNT} concerns)
{PERFORMANCE_ISSUES}

## 🎯 Recommendations
### Critical ({COUNT})
### Suggested ({COUNT})
### Nice to Have ({COUNT})

## ✅ Approval Checklist
- [ ] All critical issues resolved
- [ ] Test coverage adequate
- [ ] No new vulnerabilities
- [ ] Performance acceptable
```

### 5. Interactive Fix Application

Provide one-click fix application:

```python
# Auto-fixable issues presented with "Apply Fix" option
# User can select fixes to apply
# System applies fixes and creates commit
```

## Skills Integration

This command leverages:

**ast-analyzer**:
- Deep code structure analysis
- Complexity calculation
- Impact analysis

**security-patterns**:
- Vulnerability detection patterns
- Secure coding guidelines

**contextual-pattern-learning**:
- Find similar successful PRs
- Learn review patterns
- Improve accuracy over time

**code-analysis**:
- Code quality metrics
- Best practice validation

## Output Format

### Terminal Output (Tier 1: Concise Summary)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PR REVIEW COMPLETE: #{PR_NUMBER}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Overview
   Risk Level: {RISK_LEVEL} ({RISK_SCORE}/100)
   Files: {COUNT} | +{ADDITIONS} -{DELETIONS}
   Complexity: {SCORE}/100

🔒 Security Analysis
   🔴 Critical: {COUNT} | 🟠 High: {COUNT} | 🟡 Medium: {COUNT}
   Total New Vulnerabilities: {COUNT}

📈 Test Coverage
   Coverage: {COVERAGE}% ({DELTA > 0 ? '+' : ''}{DELTA}%)
   Untested Functions: {COUNT}

💡 Top 3 Issues
   1. {SEVERITY} - {FILE}:{LINE} - {ISSUE}
   2. {SEVERITY} - {FILE}:{LINE} - {ISSUE}
   3. {SEVERITY} - {FILE}:{LINE} - {ISSUE}

🎯 Top 3 Recommendations
   1. {CRITICAL_RECOMMENDATION}
   2. {SUGGESTED_IMPROVEMENT}
   3. {NICE_TO_HAVE}

✅ Auto-fixable Issues: {COUNT}/{TOTAL}

📄 Detailed Report: .reports/pr-review/pr-{NUMBER}-{DATE}.md

⏱️  Review completed in {DURATION}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Detailed Report (Tier 2: Comprehensive File)

Saved to: `.reports/pr-review/pr-{NUMBER}-{YYYY-MM-DD}.md`

**Full Report Structure**:

```markdown
# Pull Request Review: #{PR_NUMBER}
**Generated**: {TIMESTAMP}
**Review Time**: {DURATION}
**Reviewer**: Autonomous PR Review Agent v1.0
---


## Table of Contents
1. [Summary](#summary)
2. [Security Analysis](#security-analysis)
3. [Test Coverage](#test-coverage)
4. [Code Review](#code-review)
5. [Performance Analysis](#performance-analysis)
6. [Recommendations](#recommendations)
7. [Related PRs](#related-prs)
8. [Approval Checklist](#approval-checklist)

---

## Summary

**Title**: {PR_TITLE}
**Author**: {AUTHOR}
**Status**: {STATUS}
**Risk Level**: {RISK_LEVEL} ({RISK_SCORE}/100)

### Changes Overview
- **Files Changed**: {COUNT}
- **Lines Added**: +{ADDITIONS}
- **Lines Removed**: -{DELETIONS}
- **Complexity Score**: {SCORE}/100

### Change Categories
- ✨ **Features**: {COUNT} files
  - {FILE_LIST}
- 🐛 **Bug Fixes**: {COUNT} files
  - {FILE_LIST}
- ♻️  **Refactoring**: {COUNT} files
  - {FILE_LIST}
- 📝 **Documentation**: {COUNT} files
  - {FILE_LIST}
- ✅ **Tests**: {COUNT} files
  - {FILE_LIST}

### Risk Factors
| Factor | Score | Weight | Impact |
|--------|-------|--------|--------|
| Size | {SCORE}/100 | 20% | {IMPACT} |
| Complexity | {SCORE}/100 | 25% | {IMPACT} |
| Test Coverage | {SCORE}/100 | 25% | {IMPACT} |
| Critical Files | {SCORE}/100 | 20% | {IMPACT} |
| Security | {SCORE}/100 | 10% | {IMPACT} |

---

## Security Analysis

**New Vulnerabilities Detected**: {COUNT}

### Critical Issues (🔴)

#### {VULN_TITLE_1}
- **File**: `{FILE_PATH}`
- **Line**: {LINE_NUMBER}
- **Severity**: CRITICAL
- **CWE**: CWE-{NUMBER} - {CWE_NAME}
- **OWASP**: {OWASP_CATEGORY}

**Vulnerable Code**:
```{LANGUAGE}
{VULNERABLE_CODE}
```

**Description**: {DETAILED_DESCRIPTION}

**Remediation**:
```{LANGUAGE}
{FIXED_CODE}
```

**Explanation**: {EXPLANATION}

**Auto-fixable**: {YES/NO}

[Apply Fix] (One-click button)

---

### High Issues (🟠)
{SIMILAR_STRUCTURE}

### Medium Issues (🟡)
{SIMILAR_STRUCTURE}

### Low Issues (⚪)
{SIMILAR_STRUCTURE}

---

## Test Coverage

**Overall Coverage**: {COVERAGE}% ({DELTA > 0 ? '+' : ''}{DELTA}%)
- **Changed Lines Coverage**: {CHANGED_LINES_COV}%
- **Untested Functions**: {COUNT}

### Coverage by File

| File | Before | After | Delta | Untested Functions |
|------|--------|-------|-------|-------------------|
| {FILE} | {BEFORE}% | {AFTER}% | {DELTA}% | {COUNT} |

### Untested Functions

#### {FILE_PATH}
- `{FUNCTION_NAME}` (line {LINE})
- `{FUNCTION_NAME}` (line {LINE})

**Suggested Test**:
```{LANGUAGE}
{SUGGESTED_TEST_CODE}
```

---

## Code Review

### {FILE_PATH_1}

#### Line {LINE}: {ISSUE_TITLE}
**Severity**: {CRITICAL/HIGH/MEDIUM/LOW}
**Category**: {CODE_QUALITY/BEST_PRACTICE/PERFORMANCE}

**Original Code**:
```{LANGUAGE}
{ORIGINAL_CODE}
```

**Issue**: {DETAILED_ISSUE_DESCRIPTION}

**Suggested Fix**:
```{LANGUAGE}
{SUGGESTED_CODE}
```

**Explanation**: {WHY_THIS_IS_BETTER}

**Auto-fixable**: {YES/NO}
**Confidence**: {CONFIDENCE}%

[Apply Fix] (One-click button)

---

### {FILE_PATH_2}
{SIMILAR_STRUCTURE}

---

## Performance Analysis

**Potential Performance Impact**: {LOW/MEDIUM/HIGH}

### N+1 Query Issues ({COUNT})

#### {FILE}:{LINE} - {FUNCTION_NAME}
**Detected Pattern**: Loop with database query inside

**Current Code**:
```{LANGUAGE}
{CURRENT_CODE}
```

**Optimized Code**:
```{LANGUAGE}
{OPTIMIZED_CODE}
```

**Performance Improvement**: {ESTIMATED_IMPROVEMENT}

---

### Inefficient Algorithms ({COUNT})
{SIMILAR_STRUCTURE}

### Missing Indexes ({COUNT})
{SIMILAR_STRUCTURE}

### Large Data Operations ({COUNT})
{SIMILAR_STRUCTURE}

---

## Recommendations

### 🔴 Critical Actions Required ({COUNT})

1. **{CRITICAL_ISSUE_1}**
   - **File**: {FILE}
   - **Action**: {SPECIFIC_ACTION}
   - **Impact**: {IMPACT_DESCRIPTION}

2. **{CRITICAL_ISSUE_2}**
   {SIMILAR_STRUCTURE}

---

### 🟡 Suggested Improvements ({COUNT})

1. **{IMPROVEMENT_1}**
   - **File**: {FILE}
   - **Benefit**: {BENEFIT_DESCRIPTION}
   - **Effort**: {LOW/MEDIUM/HIGH}

2. **{IMPROVEMENT_2}**
   {SIMILAR_STRUCTURE}

---

### ⚪ Nice to Have ({COUNT})

1. **{NICE_TO_HAVE_1}**
   - **File**: {FILE}
   - **Benefit**: {MINOR_BENEFIT}

---

## Related PRs

### PRs Touching Same Files

- **#{PR_NUMBER}**: {TITLE}
  - **Author**: {AUTHOR}
  - **Status**: {STATUS}
  - **Overlap**: {FILE_COUNT} files
  - **Potential Conflict**: {YES/NO}

### Similar PRs

- **#{PR_NUMBER}**: {TITLE}
  - **Similarity**: {PERCENTAGE}%
  - **Lessons Learned**: {INSIGHTS}

### Dependent PRs

- **#{PR_NUMBER}**: {TITLE}
  - **Dependency Type**: {BLOCKS/BLOCKED_BY}

---

## Approval Checklist

### Mandatory Requirements
- [ ] All critical security issues resolved
- [ ] Test coverage ≥ 70% for changed lines
- [ ] No new critical vulnerabilities introduced
- [ ] All tests passing
- [ ] Documentation updated

### Code Quality
- [ ] No code quality issues with severity > MEDIUM
- [ ] Best practices followed
- [ ] Performance impact acceptable
- [ ] No technical debt introduced

### Review Sign-off
- [ ] Security review complete
- [ ] Performance review complete
- [ ] Test coverage adequate
- [ ] Code review complete

---

## Review Metadata

**Review Generated**: {TIMESTAMP}
**Review Time**: {DURATION}
**Auto-fixable Issues**: {COUNT}/{TOTAL}
**Confidence Score**: {AVERAGE_CONFIDENCE}%

**Reviewer Agent**: pr-reviewer v1.0
**Security Scanner**: security-auditor v1.0
**AST Analyzer**: ast-analyzer v1.0
**Pattern Learner**: contextual-pattern-learning v3.0

---

## One-Click Fixes Available

{COUNT} issues can be fixed automatically. Apply all fixes with:

```bash
/apply-pr-fixes {PR_NUMBER}
```

Or apply individual fixes:

```bash
/apply-fix {ISSUE_ID}
```

---

**End of Report**
```

---

## Implementation Details

### Git Integration

```python
def fetch_pr_data(pr_identifier):
    """Fetch PR data from git or GitHub CLI."""
    if pr_identifier.isdigit():
        # Use gh CLI for PR number
        pr_data = subprocess.run(
            ["gh", "pr", "view", pr_identifier, "--json",
             "title,author,body,files,additions,deletions"],
            capture_output=True
        )
    else:
        # Use git for branch comparison
        diff = subprocess.run(
            ["git", "diff", f"origin/main...{pr_identifier}"],
            capture_output=True
        )
        commits = subprocess.run(
            ["git", "log", f"origin/main..{pr_identifier}",
             "--oneline"],
            capture_output=True
        )

    return parse_pr_data(pr_data)
```

### Fix Application

```python
def apply_fix(issue_id):
    """Apply automated fix for specific issue."""
    issue = load_issue(issue_id)

    if not issue.auto_fixable:
        print("Issue not auto-fixable")
        return False

    # Apply Edit tool
    Edit(
        file_path=issue.file,
        old_string=issue.original_code,
        new_string=issue.suggested_code
    )

    # Run tests to verify
    test_result = run_tests()

    if test_result.success:
        # Create commit
        git_commit(f"Fix: {issue.title}\n\nAuto-applied fix from PR review")
        return True
    else:
        # Rollback
        git_checkout(issue.file)
        return False
```

## Learning Integration

After each PR review, the learning engine captures:

1. **Review Patterns**:
   - Which issues were found in which file types
   - Success rate of automated fixes
   - False positive rates

2. **Project Patterns**:
   - Common issue patterns in this codebase
   - Team coding style preferences
   - Review thoroughness preferences

3. **Performance Metrics**:
   - Review time by PR size
   - Issue detection accuracy
   - Fix application success rate

4. **Continuous Improvement**:
   - Reduce false positives over time
   - Improve fix suggestion quality
   - Personalize review style to team

## Error Handling

```python
try:
    review_result = comprehensive_pr_review(pr_number)
except GitError as e:
    print(f"Git error: {e.message}")
    print("Ensure you're in a git repository and PR exists")
except SecurityScanError as e:
    print(f"Security scan failed: {e.message}")
    print("Review will continue with partial results")
except Exception as e:
    print(f"Review failed: {e}")
    print("Saving partial results...")
    save_partial_review(partial_data)
```

## Performance Expectations

| PR Size | Files | Lines | Review Time |
|---------|-------|-------|-------------|
| Small | 1-5 | <200 | 30-60s |
| Medium | 6-15 | 200-500 | 1-2min |
| Large | 16-30 | 500-1000 | 2-4min |
| XLarge | 31+ | 1000+ | 4-8min |

## Follow-up Commands

After review:

```bash
/apply-pr-fixes {PR_NUMBER}     # Apply all auto-fixable issues
/apply-fix {ISSUE_ID}           # Apply specific fix
/dev:pr-review-history          # Show review history
/learn:analytics                # Review performance analytics
```

---

This command provides comprehensive, CodeRabbit-level PR review capabilities with deep integration into the autonomous learning system.
