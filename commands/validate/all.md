---
name: validate:all
description: Run comprehensive validation checks on tool usage, documentation consistency, and execution flow compliance
delegates-to: validation-controller
---



# Comprehensive Validation Check

Performs thorough validation of:
- Tool usage compliance (Edit/Write prerequisites, parameter validation)
- Documentation consistency (version sync, path references, component counts)
- Cross-reference integrity (all links and references valid)
- Best practices adherence (tool selection, error handling)
- Execution flow analysis (dependency tracking, state validation)

## How It Works

This command delegates to the **validation-controller** agent which:

1. **Scans tool usage patterns** in recent session history
2. **Analyzes documentation** for inconsistencies across all .md files and plugin.json
3. **Validates cross-references** to ensure all links and component references exist
4. **Checks best practices** compliance with Claude Code guidelines
5. **Reviews execution flow** for proper tool sequencing and state management
6. **Generates validation report** with severity-prioritized findings and auto-fix suggestions

## Skills Utilized

- **autonomous-agent:validation-standards** - Tool requirements, failure patterns, consistency checks
- **autonomous-agent:quality-standards** - Best practices and quality benchmarks
- **autonomous-agent:pattern-learning** - Historical success/failure patterns

## Usage

```bash
/validate:all
```

## Expected Output (Two-Tier Presentation)

### Terminal Output (Concise)

```
✓ Validation Complete - Score: 85/100

Key Findings:
• [ERROR] Documentation path inconsistency: 6 occurrences in CLAUDE.md
• [WARN] Write operation without prior Read: plugin.json
• [INFO] All cross-references valid

Top Recommendations:
1. [HIGH] Standardize path references in CLAUDE.md → Prevent user confusion
2. [MED]  Add Read before Write to plugin.json → Follow tool requirements
3. [LOW]  Consider adding path validation utility

📄 Full report: .claude/reports/validation-2025-10-21.md
⏱ Completed in 1.2 minutes
```

### File Report (Comprehensive)

Located at: `.claude/reports/validation-YYYY-MM-DD.md`

```markdown
# Comprehensive Validation Report
Generated: 2025-10-21 12:30:45

## Executive Summary
Validation Score: 85/100 (Good)
- Tool Usage: 27/30 ✓
- Documentation Consistency: 18/25 ✗
- Best Practices: 20/20 ✓
- Error-Free Execution: 12/15 ✓
- Pattern Compliance: 8/10 ✓

## Detailed Findings

### 🔴 Critical Issues (2)

#### 1. Documentation Path Inconsistency
**Severity**: ERROR
**Category**: Documentation Consistency
**Impact**: High - User confusion, incorrect instructions

**Details**:
- File: CLAUDE.md
- Inconsistent path references detected:
  - `.claude-patterns/patterns.json` (standardized)
    - Line 17: Pattern learning location
    - Line 63: Pattern database location
    - Line 99: Skill auto-selection query
    - Line 161: Verification command
    - Line 269: Pattern storage
    - Line 438: Notes for future instances
  - Actual implementation: `.claude-patterns/patterns.json`

**Root Cause**: Documentation written before Python utilities (v1.4) implementation

**Recommendation**: Standardize all references to `.claude-patterns/patterns.json`

**Auto-Fix Available**: Yes
```bash
# Automated fix command
sed -i 's|\.claude/patterns/|\.claude-patterns/|g' **/*.md
```

#### 2. Write Without Prior Read
**Severity**: WARNING
**Category**: Tool Usage
**Impact**: Medium - Violates tool requirements

**Details**:
- Tool: Write
- File: .claude-plugin/plugin.json
- Error: "File has not been read yet"

**Root Cause**: Edit tool called without prerequisite Read operation

**Recommendation**: Always call Read before Edit on existing files

**Auto-Fix Available**: Yes
```python
# Correct sequence
Read(".claude-plugin/plugin.json")
Edit(".claude-plugin/plugin.json", old_string, new_string)
```

### ✅ Passed Validations (12)

- ✓ Version consistency across all files (v1.6.1)
- ✓ Component counts accurate (10 agents, 6 skills, 6 commands)
- ✓ All cross-references valid
- ✓ Tool selection follows best practices
- ✓ Bash usage avoids anti-patterns
- ✓ No broken links in documentation
- ✓ All referenced files exist
- ✓ Agent YAML frontmatter valid
- ✓ Skill metadata complete
- ✓ Command descriptions accurate
- ✓ Pattern database schema valid
- ✓ No duplicate component names

### 📊 Validation Breakdown

**Tool Usage Compliance**: 27/30 points
- ✓ 15/16 Edit operations had prerequisite Read
- ✗ 1/16 Edit failed due to missing Read
- ✓ 8/8 Write operations on new files proper
- ✗ 1/2 Write on existing file without Read
- ✓ All Bash commands properly chained
- ✓ Specialized tools preferred over Bash

**Documentation Consistency**: 18/25 points
- ✗ Path references inconsistent (6 violations)
- ✓ Version numbers synchronized
- ✓ Component counts accurate
- ✓ No orphaned references
- ✓ Examples match implementation

**Best Practices Adherence**: 20/20 points
- ✓ Tool selection optimal
- ✓ Error handling comprehensive
- ✓ File operations use correct tools
- ✓ Documentation complete
- ✓ Code structure clean

**Error-Free Execution**: 12/15 points
- ✓ 95% of operations successful
- ✗ 1 tool prerequisite violation
- ✓ Quick error recovery
- ✓ No critical failures

**Pattern Compliance**: 8/10 points
- ✓ Follows successful patterns
- ✗ Minor deviation in tool sequence
- ✓ Quality scores consistent
- ✓ Learning patterns applied

## Recommendations (Prioritized)

### High Priority (Implement Immediately)

1. **Fix Documentation Path Inconsistency**
   - Impact: Prevents user confusion and incorrect instructions
   - Effort: Low (10 minutes)
   - Auto-fix: Available
   - Files: CLAUDE.md (6 replacements)

2. **Add Pre-flight Validation for Edit/Write**
   - Impact: Prevents 87% of tool usage errors
   - Effort: Medium (integrated in orchestrator)
   - Auto-fix: Built into validation-controller agent

### Medium Priority (Address Soon)

3. **Create Path Validation Utility**
   - Impact: Prevents path inconsistencies in future
   - Effort: Medium (create new utility script)
   - Location: lib/path_validator.py

4. **Enhance Session State Tracking**
   - Impact: Better dependency tracking
   - Effort: Medium (extend orchestrator)
   - Benefit: 95% error prevention rate

### Low Priority (Nice to Have)

5. **Add Validation Metrics Dashboard**
   - Impact: Visibility into validation effectiveness
   - Effort: High (new component)
   - Benefit: Data-driven improvement

## Failure Patterns Detected

### Pattern: Edit Before Read
- **Frequency**: 1 occurrence
- **Auto-fixed**: Yes
- **Prevention rule**: Enabled
- **Success rate**: 100%

### Pattern: Path Inconsistency
- **Frequency**: 6 occurrences
- **Type**: Documentation drift
- **Root cause**: Implementation changes without doc updates
- **Prevention**: Add doc consistency checks to CI/CD

## Validation Metrics

### Session Statistics
- Total operations: 48
- Successful: 46 (95.8%)
- Failed: 2 (4.2%)
- Auto-recovered: 2 (100% of failures)

### Tool Usage
- Read: 24 calls (100% success)
- Edit: 16 calls (93.8% success, 1 prerequisite violation)
- Write: 6 calls (83.3% success)
- Bash: 2 calls (100% success)

### Prevention Effectiveness
- Failures prevented: 0 (validation not yet active during session)
- Failures detected and fixed: 2
- False positives: 0
- Detection rate: 100%

## Next Steps

1. Apply high-priority fixes immediately
2. Enable pre-flight validation in orchestrator
3. Schedule medium-priority improvements
4. Monitor validation metrics for 10 tasks
5. Run /validate again to verify improvements

## Validation History

This validation compared to baseline (first validation):
- Score: 85/100 (baseline - first run)
- Issues found: 8 total (2 critical, 3 medium, 3 low)
- Auto-fix success: 100% (2/2 fixable issues)
- Time to complete: 1.2 minutes

---

**Next Validation Recommended**: After applying high-priority fixes
**Expected Score After Fixes**: 95/100
```

## When to Use

Run `/validate:all` when:
- Before releases or major changes
- After significant refactoring
- When documentation is updated
- After adding new components
- Periodically (every 10-25 tasks)
- When unusual errors occur
- To audit project health

## Integration with Autonomous Workflow

The orchestrator automatically triggers validation:
- **Pre-flight**: Before Edit/Write operations (checks prerequisites)
- **Post-error**: After tool failures (analyzes and auto-fixes)
- **Post-documentation**: After doc updates (checks consistency)
- **Periodic**: Every 25 tasks (comprehensive audit)

Users can also manually trigger full validation with `/validate:all`.

## Success Criteria

Validation passes when:
- Score ≥ 70/100
- No critical (ERROR) issues
- Tool usage compliance ≥ 90%
- Documentation consistency ≥ 80%
- All cross-references valid
- Best practices followed

## Validation Benefits

**For Users**:
- Catch issues before they cause problems
- Clear, actionable recommendations
- Auto-fix for common errors
- Improved project quality

**For Development**:
- Enforces best practices
- Prevents documentation drift
- Maintains consistency
- Reduces debugging time

**For Learning**:
- Builds failure pattern database
- Improves prevention over time
- Tracks validation effectiveness
- Continuous improvement loop
