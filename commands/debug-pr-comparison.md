# Debugging PR Comparison Command

Creates parallel debugging pull requests for Claude and GLM models and compares their performance head-to-head.

## Usage

```bash
/debug-pr-comparison <target> [options]
```

## How It Works

This command creates a comprehensive debugging performance comparison by:

1. **Parallel PR Creation**: Creates separate branches for Claude and GLM debugging approaches
2. **Dual Model Evaluation**: Runs debugging evaluations with both models on the same target
3. **Side-by-Side Comparison**: Generates comparative analysis of performance metrics
4. **Comprehensive Reporting**: Produces detailed comparison report with performance rankings

## Available Targets

### `dashboard`
- **Scope**: Dashboard data consistency and API functionality
- **Expected Issues**: Timeline API errors, data loading failures, chart inconsistencies
- **Complexity**: Medium-High (frontend + backend debugging)
- **Evaluation Metrics**: API fixes, data consistency, performance improvements

### `performance-index`
- **Scope**: AI Debugging Performance Index calculation accuracy
- **Expected Issues**: QIS formula errors, calculation discrepancies, framework validation
- **Complexity**: High (mathematical framework debugging)
- **Evaluation Metrics**: Formula accuracy, calculation precision, framework validation

### `data-validation`
- **Scope**: Data integrity across dashboard metrics and charts
- **Expected Issues**: Inconsistent data between charts, validation errors
- **Complexity**: Medium (data pipeline debugging)
- **Evaluation Metrics**: Data consistency, validation accuracy, pipeline fixes

### `plugin-validation`
- **Scope**: Claude plugin compliance and validation issues
- **Expected Issues**: Plugin manifest errors, validation failures, compliance issues
- **Complexity**: Medium (standards compliance debugging)
- **Evaluation Metrics**: Validation fixes, compliance improvements, standards adherence

## Command Options

### Branch Management
```bash
# Use custom branch names
/debug-pr-comparison dashboard --branches claude-fix-dashboard/glm-fix-dashboard

# Include timestamp in branch names
/debug-pr-comparison performance-index --timestamp

# Use existing branches (create PRs without new branches)
/debug-pr-comparison data-validation --branches existing-claude/existing-glm
```

### Evaluation Control
```bash
# Skip evaluation and only create PRs
/debug-pr-comparison dashboard --create-only

# Run evaluation without creating PRs
/debug-pr-comparison performance-index --evaluate-only

# Set quality threshold for evaluation
/debug-pr-comparison data-validation --threshold 90
```

### Reporting Options
```bash
# Generate detailed comparison report
/debug-pr-comparison dashboard --detailed-report

# Create visual comparison charts
/debug-pr-comparison performance-index --charts

# Export results to JSON
/debug-pr-comparison data-validation --export-json comparison-results.json
```

## Workflow Stages

### Stage 1: Branch Creation (30-60 seconds)
```
🌿 BRANCH CREATION
├─ Claude Branch: claude-debug-<target>-<timestamp>
├─ GLM Branch: glm-debug-<target>-<timestamp>
├─ Initial commits: Branch setup with model identification
└─ Remote push: Both branches pushed to origin
```

### Stage 2: Parallel Debugging (5-15 minutes)
```
🔍 PARALLEL DEBUGGING EXECUTION
├─ Claude Debugging Session
│  ├─ Issue identification and analysis
│  ├─ Fix implementation and testing
│  ├─ Quality assessment and validation
│  └─ Performance metrics calculation
└─ GLM Debugging Session
   ├─ Issue identification and analysis
   ├─ Fix implementation and testing
   ├─ Quality assessment and validation
   └─ Performance metrics calculation
```

### Stage 3: PR Creation (2-5 minutes)
```
📝 PULL REQUEST CREATION
├─ Claude PR: "Claude: Debug <target> - Performance Analysis"
├─ GLM PR: "GLM: Debug <target> - Performance Analysis"
├─ PR descriptions: Detailed findings and methodology
├─ Comparison linking: Cross-reference between PRs
└─ Labels and assignments: Debugging, performance-comparison
```

### Stage 4: Comparative Analysis (2-3 minutes)
```
📊 COMPARATIVE ANALYSIS
├─ Performance metrics comparison
├─ Quality improvement analysis
├─ Time efficiency comparison
├─ Approach methodology differences
└─ Success rate and reliability analysis
```

### Stage 5: Report Generation (1-2 minutes)
```
📋 COMPREHENSIVE REPORTING
├─ Executive summary with winner declaration
├─ Detailed side-by-side comparison tables
├─ Performance visualization charts
├─ Methodology analysis and insights
└─ Recommendations and best practices
```

## Performance Metrics Compared

### Core Debugging Metrics
- **Performance Index**: Overall debugging effectiveness (0-100)
- **Quality Improvement Score (QIS)**: Quality enhancement capability
- **Time Efficiency Score (TES)**: Speed and efficiency of debugging
- **Success Rate**: Percentage of successful debugging outcomes
- **Regression Penalty**: Points lost for introducing new issues

### Approach Analysis
- **Issue Identification Speed**: Time to discover root causes
- **Fix Quality**: Thoroughness and reliability of fixes applied
- **Methodology Style**: Analytical vs. intuitive approaches
- **Documentation Quality**: Detail and clarity of debugging reports
- **Communication Style**: Explanation clarity and technical depth

### Technical Competence
- **Code Understanding**: Accuracy of issue diagnosis
- **Solution Creativity**: Innovation in problem-solving approaches
- **Testing Thoroughness**: Comprehensive validation of fixes
- **Edge Case Handling**: Consideration of unusual scenarios
- **Performance Impact**: Optimization and efficiency improvements

## Expected Output

### Terminal Summary
```
🔍 DEBUGGING PR COMPARISON COMPLETE
Target: dashboard data consistency
Duration: 12m 45s

📊 PERFORMANCE COMPARISON:
┌─────────────────────────────────────┬─────────────┬─────────────┐
│              METRIC                │   CLAUDE    │     GLM     │
├─────────────────────────────────────┼─────────────┼─────────────┤
│ Performance Index                  │   87.2/100  │   91.8/100  │
│ Quality Improvement (QIS)           │   85.4/100  │   89.2/100  │
│ Time Efficiency (TES)               │   94.1/100  │   88.7/100  │
│ Success Rate                       │   100%      │   100%      │
│ Issues Identified                  │     3       │     3       │
│ Fixes Applied                      │     3       │     3       │
│ Time to Resolution                 │   8m 30s    │   6m 15s    │
└─────────────────────────────────────┴─────────────┴─────────────┘

🏆 WINNER: GLM (Performance Index: 91.8 vs 87.2)

📝 PULL REQUESTS:
✅ Claude PR: #123 - Claude: Debug dashboard - Performance Analysis
✅ GLM PR: #124 - GLM: Debug dashboard - Performance Analysis

📄 COMPARISON REPORT: .claude-patterns/reports/debug-comparison-dashboard-2025-10-24.md
🔗 VIEW COMPARISON: https://github.com/user/repo/compare/debug-comparison-dashboard
```

### Detailed Comparison Report
**Location**: `.claude-patterns/reports/debug-comparison-<target>-YYYY-MM-DD.md`

**Report Sections:**
1. **Executive Summary**: Overall winner and key performance differences
2. **Methodology Comparison**: Different approaches taken by each model
3. **Performance Analysis**: Detailed breakdown of metrics and scores
4. **Technical Assessment**: Code quality, fix reliability, testing approach
5. **Time Analysis**: Speed vs. thoroughness trade-offs
6. **Communication Style**: Explanation clarity and documentation quality
7. **Recommendations**: Best practices and insights from both approaches

### Visual Comparison Charts
**Location**: `.claude-patterns/reports/debug-comparison-<target>-YYYY-MM-DD-charts/`

- **Performance Radar Chart**: Side-by-side metric comparison
- **Timeline Comparison**: Task completion time analysis
- **Quality Trend Analysis**: Quality improvement over time
- **Approach Methodology**: Different problem-solving styles

## Integration with GitHub

### Automatic PR Creation
```bash
# Claude PR Title: "Claude: Debug <target> - Performance Analysis"
# Claude PR Description includes:
# - Issues identified and root causes
# - Fixes implemented with code snippets
# - Quality assessment results
# - Performance metrics achieved

# GLM PR Title: "GLM: Debug <target> - Performance Analysis"
# GLM PR Description includes:
# - Issues identified and root causes
# - Fixes implemented with code snippets
# - Quality assessment results
# - Performance metrics achieved
```

### Cross-Reference Linking
- Each PR references the other for comparison
- Links to detailed comparison report
- GitHub comment with performance summary
- Labels: `debugging`, `performance-comparison`, `claude-vs-glm`

## Performance Analysis Framework

### Scoring Criteria
**Performance Index Calculation:**
```
PI = (0.40 × QIS) + (0.35 × TES) + (0.25 × SR) − Penalty
```

**Quality Improvement Score (QIS):**
```
QIS = 0.6 × FinalQuality + 0.4 × (GapClosedPct × 100/100)
```

**Time Efficiency Score (TES):**
- Based on task complexity and completion time
- Accounts for thoroughness vs. speed trade-offs
- Ideal time varies by task complexity

### Comparative Insights
- **Model Strengths**: Identify each model's debugging superpowers
- **Approach Differences**: Analytical vs. intuitive, systematic vs. creative
- **Learning Patterns**: How each model improves from experience
- **Specialization**: Which types of debugging tasks each model excels at

## Benefits

### For Performance Analysis
- **Direct Model Comparison**: Head-to-head performance metrics
- **Objective Evaluation**: Standardized scoring framework
- **Trend Analysis**: Performance improvement over time
- **Specialization Identification**: Discover each model's strengths

### For Team Decision Making
- **Model Selection**: Choose the best model for specific debugging tasks
- **Quality Assurance**: Ensure high debugging standards
- **Knowledge Transfer**: Learn from both models' approaches
- **Best Practices**: Combine the best of both methodologies

### For Continuous Improvement
- **Performance Tracking**: Monitor model improvement over time
- **Benchmarking**: Establish performance baselines
- **Training Insights**: Identify areas for model improvement
- **Documentation**: Build knowledge base of debugging approaches

## Examples

### Dashboard Debugging Comparison
```bash
/debug-pr-comparison dashboard
# Creates PRs comparing Claude and GLM dashboard debugging approaches
# Analyzes API fixes, data consistency, and performance improvements
```

### Performance Index Validation
```bash
/debug-pr-comparison performance-index --detailed-report
# Compares mathematical framework debugging approaches
# Includes detailed analysis of calculation accuracy and formula implementation
```

### Plugin Compliance Comparison
```bash
/debug-pr-comparison plugin-validation --charts --export-json
# Compares validation and compliance debugging approaches
# Generates visual charts and exports detailed JSON results
```

## Advanced Usage

### Custom Evaluation Framework
```bash
# Use custom scoring weights
/debug-pr-comparison dashboard --weights qis:0.5 tes:0.3 sr:0.2

# Set custom quality thresholds
/debug-pr-comparison performance-index --threshold 85 --bonus-threshold 95
```

### Integration with CI/CD
```bash
# Automated comparison in CI pipeline
/debug-pr-comparison dashboard --automated --notify-team

# Integration with project management
/debug-pr-comparison data-validation --create-tickets --assign-reviewers
```

### Historical Analysis
```bash
# Compare with previous debugging sessions
/debug-pr-comparison dashboard --compare-with previous-run-id

# Track improvement over time
/debug-pr-comparison performance-index --trend-analysis --period 30days
```

---

**Version**: 1.0.0
**Integration**: Works with version-release-manager agent, git-automation skill, and debugging performance framework
**Platforms**: GitHub, GitLab with API access required for PR creation