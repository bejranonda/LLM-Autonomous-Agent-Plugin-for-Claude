---
name: learn:history
description: Learn from commit history to identify patterns, debugging strategies, and improvement areas
delegates-to: autonomous-agent:orchestrator
---

# Learn-History Command

## Command: `/learn:history`

**Learn from repository evolution** - Analyzes commit history in external GitHub/GitLab repositories to discover successful debugging patterns, development workflows, and improvement strategies that can be applied to the current project.

**📚 Historical Pattern Learning:**
- **Commit Analysis**: Study how issues were resolved over time
- **Debug Pattern Discovery**: Learn effective debugging approaches
- **Development Workflow**: Understand successful development practices
- **Refactoring Patterns**: Identify effective code improvement strategies
- **Test Evolution**: Learn how testing strategies matured
- **Documentation Evolution**: Study documentation improvement patterns

## How It Works

1. **History Access**: Clones repository and analyzes commit history
2. **Pattern Extraction**: Identifies recurring patterns in commits
3. **Debug Strategy Analysis**: Studies how bugs were fixed
4. **Workflow Discovery**: Maps development and release workflows
5. **Quality Improvement Tracking**: Analyzes quality evolution over time
6. **Pattern Application**: Suggests how to apply learnings to current project

## Usage

### Basic Usage
```bash
# Learn from repository history
/learn:history https://github.com/username/repo

# Learn from specific branch
/learn:history https://github.com/username/repo --branch develop

# Learn from date range
/learn:history https://github.com/username/repo --since "2024-01-01" --until "2024-12-31"
```

### Focused Analysis
```bash
# Focus on bug fixes
/learn:history https://github.com/user/repo --focus bug-fixes

# Focus on refactoring patterns
/learn:history https://github.com/user/repo --focus refactoring

# Focus on test improvements
/learn:history https://github.com/user/repo --focus testing

# Focus on performance improvements
/learn:history https://github.com/user/repo --focus performance
```

### Advanced Options
```bash
# Analyze specific contributor's patterns
/learn:history https://github.com/user/repo --author "developer@email.com"

# Deep analysis with AI-powered insights
/learn:history https://github.com/user/repo --deep-analysis

# Compare with current project
/learn:history https://github.com/user/repo --apply-to-current

# Generate actionable roadmap
/learn:history https://github.com/user/repo --generate-improvements
```

## Output Format

### Terminal Output (Concise)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 HISTORY ANALYSIS COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Repository: fastapi/fastapi
Commits Analyzed: 3,892 | Time Range: 3.5 years

Key Discoveries:
* Early focus on type safety prevented 60% of bugs
* Incremental refactoring approach (small PRs)
* Test-first development for all features

Top Patterns to Apply:
1. Implement pre-commit hooks for type checking
2. Use conventional commit messages for automation
3. Add integration tests before refactoring

📄 Full report: .claude/reports/learn-history-fastapi-2025-10-29.md
⏱ Analysis completed in 4.5 minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Detailed Report

```markdown
=======================================================
  REPOSITORY HISTORY ANALYSIS
=======================================================
Repository: https://github.com/fastapi/fastapi
Time Range: 2018-12-05 to 2025-01-15 (3.5 years)
Commits Analyzed: 3,892
Contributors: 487

+- Development Evolution ------------------------------+
| Phase 1: Initial Development (6 months)              |
| * Focus: Core functionality and type safety          |
| * Commits: 234                                       |
| * Key Pattern: Type-first development                |
| * Result: Strong foundation, fewer bugs later        |
|                                                       |
| Phase 2: Feature Expansion (12 months)               |
| * Focus: Adding features while maintaining quality   |
| * Commits: 892                                       |
| * Key Pattern: Test-before-feature approach          |
| * Result: Features added without quality degradation |
|                                                       |
| Phase 3: Maturity & Optimization (24 months)         |
| * Focus: Performance and developer experience        |
| * Commits: 2,766                                     |
| * Key Pattern: Continuous small improvements         |
| * Result: Best-in-class performance and DX           |
+-------------------------------------------------------+

+- Bug Fix Patterns Discovered ------------------------+
| 1. Type Error Prevention (423 commits)               |
|    Pattern: Added type hints before features         |
|    Effectiveness: Prevented 60% of potential bugs    |
|    Application to Current Project:                    |
|    -> Add comprehensive type hints to all agents      |
|    -> Use mypy in pre-commit hooks                    |
|    -> Validate agent schemas with Pydantic            |
|                                                       |
| 2. Test-Driven Bug Fixes (892 commits)               |
|    Pattern: Write failing test -> Fix -> Verify        |
|    Effectiveness: 95% of bugs didn't recur           |
|    Application to Current Project:                    |
|    -> Add test case for every bug fix                 |
|    -> Use regression test suite                       |
|    -> Integrate with quality-controller agent         |
|                                                       |
| 3. Incremental Refactoring (234 commits)             |
|    Pattern: Small, focused refactoring PRs           |
|    Effectiveness: Zero breaking changes               |
|    Application to Current Project:                    |
|    -> Refactor one agent/skill at a time              |
|    -> Maintain backward compatibility                 |
|    -> Use deprecation warnings before removal         |
|                                                       |
| 4. Dependency Updates (156 commits)                  |
|    Pattern: Regular, automated dependency updates    |
|    Effectiveness: Zero security incidents            |
|    Application to Current Project:                    |
|    -> Use Dependabot or similar automation            |
|    -> Test after each dependency update               |
|    -> Pin versions with compatibility ranges          |
+-------------------------------------------------------+

+- Development Workflow Patterns ----------------------+
| Commit Message Pattern Analysis:                     |
| * 78% use conventional commits (feat:, fix:, etc.)   |
| * Average commit size: 127 lines changed             |
| * 92% of commits reference issues                    |
|                                                       |
| PR Review Process:                                    |
| * Average review time: 18 hours                      |
| * Requires 2+ approvals for core changes             |
| * Automated CI checks (tests, linting, types)        |
| * Documentation updated in same PR                    |
|                                                       |
| Release Workflow:                                     |
| * Semantic versioning strictly followed              |
| * Changelog auto-generated from commits              |
| * Release notes include upgrade guide                |
| * Beta releases before major versions                |
|                                                       |
| Application to Current Project:                       |
| 1. Adopt conventional commit format                  |
| 2. Link commits to slash command implementations     |
| 3. Auto-generate CHANGELOG.md from commits           |
| 4. Add pre-commit hooks for validation               |
| 5. Implement automated release workflow              |
+-------------------------------------------------------+

+- Testing Strategy Evolution -------------------------+
| Timeline of Testing Improvements:                     |
|                                                       |
| Year 1 (2019):                                       |
| * Coverage: 45% -> 75%                                |
| * Pattern: Added tests retrospectively               |
| * Result: Many bugs caught late                      |
|                                                       |
| Year 2 (2020):                                       |
| * Coverage: 75% -> 92%                                |
| * Pattern: Test-first for new features              |
| * Result: Fewer bugs in new code                     |
|                                                       |
| Year 3 (2021):                                       |
| * Coverage: 92% -> 96%                                |
| * Pattern: Property-based testing added              |
| * Result: Edge cases discovered automatically        |
|                                                       |
| Key Learnings:                                        |
| * Early investment in testing pays off               |
| * Property-based testing finds unexpected bugs       |
| * Fast tests encourage frequent execution            |
| * Integration tests complement unit tests            |
|                                                       |
| Application to Current Project:                       |
| 1. Set coverage goal: 90%+ for agents/skills         |
| 2. Add property-based tests for core logic           |
| 3. Use test-engineer agent for all features          |
| 4. Optimize test execution time (<60s total)         |
| 5. Add integration tests for agent workflows         |
+-------------------------------------------------------+

+- Documentation Improvement Patterns -----------------+
| Documentation Evolution:                              |
|                                                       |
| Early Stage:                                          |
| * Basic README with installation steps               |
| * Inline code comments only                          |
| * Result: High support burden                        |
|                                                       |
| Growth Stage:                                         |
| * Added tutorials and examples                       |
| * API documentation from docstrings                  |
| * Result: 40% reduction in support requests          |
|                                                       |
| Mature Stage:                                         |
| * Multi-language documentation                       |
| * Interactive examples                               |
| * Video tutorials                                    |
| * Result: Best-in-class documentation                |
|                                                       |
| Key Patterns:                                         |
| * Documentation updated with code (same PR)          |
| * Examples tested as part of CI                      |
| * User feedback drives improvements                  |
| * Visual aids (diagrams, flowcharts)                 |
|                                                       |
| Application to Current Project:                       |
| 1. Keep command documentation with implementation    |
| 2. Add usage examples to all slash commands          |
| 3. Create visual architecture diagrams               |
| 4. Test documentation examples automatically         |
| 5. Add troubleshooting section to each command       |
+-------------------------------------------------------+

+- Performance Optimization Journey -------------------+
| Performance Commits: 167                              |
|                                                       |
| Major Optimizations:                                  |
| 1. Async/Await Migration (Commit #1234)              |
|    * 3x throughput improvement                       |
|    * Pattern: Gradual migration, one module at time  |
|    * Lesson: Plan async from start or budget time    |
|                                                       |
| 2. Dependency Injection Caching (Commit #2456)       |
|    * 40% latency reduction                           |
|    * Pattern: Cache resolved dependencies            |
|    * Lesson: Profile before optimizing               |
|                                                       |
| 3. Response Model Optimization (Commit #3012)        |
|    * 25% faster serialization                        |
|    * Pattern: Lazy loading and selective fields      |
|    * Lesson: Measure real-world impact               |
|                                                       |
| Application to Current Project:                       |
| 1. Add async support to background-task-manager      |
| 2. Cache pattern database queries                    |
| 3. Profile agent execution times                     |
| 4. Optimize skill loading (lazy load when possible)  |
| 5. Implement parallel agent execution                |
+-------------------------------------------------------+

+- Refactoring Strategy Analysis ----------------------+
| Refactoring Commits: 234 (6% of total)               |
|                                                       |
| Successful Refactoring Patterns:                      |
|                                                       |
| Pattern A: Extract & Test                            |
| * Extract component -> Write tests -> Refactor -> Verify|
| * Success Rate: 98%                                  |
| * Average PR size: 89 lines changed                  |
|                                                       |
| Pattern B: Deprecate -> Migrate -> Remove              |
| * Mark old API deprecated                            |
| * Add new API alongside                              |
| * Migrate internally                                 |
| * Remove after 2+ versions                           |
| * Success Rate: 100% (no breaking changes)           |
|                                                       |
| Pattern C: Incremental Type Addition                 |
| * Add types to new code                              |
| * Gradually add to existing code                     |
| * Use Any temporarily if needed                      |
| * Success Rate: 94%                                  |
|                                                       |
| Failed Refactoring Attempts:                          |
| * Big-bang rewrites (2 attempts, both failed)        |
| * Premature optimization (4 reverted commits)        |
| * Refactoring without tests (3 bugs introduced)      |
|                                                       |
| Application to Current Project:                       |
| 1. Refactor agents one at a time                     |
| 2. Always add tests before refactoring               |
| 3. Use deprecation warnings for breaking changes     |
| 4. Keep refactoring PRs small (<200 lines)           |
| 5. Profile before performance refactoring            |
+-------------------------------------------------------+

+- Actionable Improvements for Current Project --------+
| IMMEDIATE ACTIONS (This Week):                       |
|                                                       |
| 1. Add Conventional Commit Format                    |
|    Command: Configure Git hooks                      |
|    Impact: Better changelog generation               |
|    Effort: 30 minutes                                |
|    Implementation: /dev:auto "add conventional commit hooks"
|                                                       |
| 2. Implement Pre-Commit Type Checking                |
|    Command: Add mypy to pre-commit                   |
|    Impact: Catch type errors before commit           |
|    Effort: 1 hour                                    |
|    Implementation: /dev:auto "add mypy pre-commit hook"
|                                                       |
| 3. Add Test Coverage Reporting                       |
|    Command: Integrate coverage.py                    |
|    Impact: Visibility into test gaps                 |
|    Effort: 45 minutes                                |
|    Implementation: /dev:auto "add test coverage reporting"
|                                                       |
| SHORT-TERM ACTIONS (This Month):                     |
|                                                       |
| 4. Implement Automated Dependency Updates            |
|    Tool: Dependabot or Renovate                      |
|    Impact: Stay current, avoid security issues       |
|    Effort: 2 hours                                   |
|                                                       |
| 5. Add Property-Based Testing                        |
|    Library: Hypothesis for Python                    |
|    Impact: Discover edge case bugs                   |
|    Effort: 4 hours                                   |
|                                                       |
| 6. Create Visual Architecture Diagrams               |
|    Tool: Mermaid in markdown                         |
|    Impact: Better understanding for contributors     |
|    Effort: 3 hours                                   |
|                                                       |
| LONG-TERM ACTIONS (This Quarter):                    |
|                                                       |
| 7. Migrate to Async-First Architecture               |
|    Scope: Background-task-manager and orchestrator   |
|    Impact: Faster execution, better scalability      |
|    Effort: 2-3 weeks                                 |
|                                                       |
| 8. Implement Comprehensive Integration Tests         |
|    Scope: All agent workflows end-to-end             |
|    Impact: Catch integration bugs early              |
|    Effort: 2 weeks                                   |
|                                                       |
| 9. Add Performance Profiling & Monitoring            |
|    Tool: Built-in profiler + custom metrics          |
|    Impact: Identify and fix bottlenecks              |
|    Effort: 1 week                                    |
+-------------------------------------------------------+

=======================================================
  NEXT STEPS
=======================================================

Ready to Apply Learnings?
* Start with immediate actions (easiest wins)
* Use /dev:auto for implementation
* Track progress with /learn:analytics

Want More Historical Analysis?
* Analyze another repository for comparison
* Deep-dive into specific time periods
* Focus on particular contributors' patterns

=======================================================

Analysis Time: 4.5 minutes
Commits Analyzed: 3,892
Patterns Extracted: 12 major patterns
Actionable Improvements: 9 recommendations

Historical patterns stored in learning database.
```

## Integration with Learning System

Stores historical patterns for future reference:

```json
{
  "history_learning_patterns": {
    "source_repo": "fastapi/fastapi",
    "patterns_extracted": {
      "bug_fix_strategies": 4,
      "refactoring_approaches": 3,
      "testing_evolution": 3,
      "documentation_improvements": 4
    },
    "applied_to_current_project": true,
    "effectiveness_tracking": true,
    "reuse_count": 1
  }
}
```

## Agent Delegation

- **orchestrator**: Coordinates analysis
- **code-analyzer**: Analyzes code changes over time
- **pattern-learning**: Extracts and stores patterns
- **quality-controller**: Evaluates quality improvements

## Use Cases

### Learning Debug Patterns
```bash
/learn:history https://github.com/user/repo --focus bug-fixes
```

### Understanding Quality Evolution
```bash
/learn:history https://github.com/user/repo --focus quality-improvements
```

### Studying Refactoring Success
```bash
/learn:history https://github.com/user/repo --focus refactoring
```

---

**Version**: 1.0.0
**Integration**: Full pattern learning integration
**Platform**: Cross-platform
**Scope**: Learn from repository evolution to improve current project
