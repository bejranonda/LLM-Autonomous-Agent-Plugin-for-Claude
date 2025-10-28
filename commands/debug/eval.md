---
name: debug:eval
description: Command for eval debug
delegates-to: orchestrator
---


# Debugging Performance Evaluation

Measures AI debugging performance by analyzing and fixing real issues in the codebase.

## Usage

```bash
/debug:eval <target> [options]
```

### Options

```bash
--help                Show this help message
--verbose             Show detailed agent selection process
--dry-run            Preview actions without executing
--report-only        Generate report without fixing issues
--performance         Include detailed performance metrics
```

### Help Examples

```bash
# Show help
/debug:eval --help

# Debug with verbose output (shows agent selection)
/debug:eval dashboard --verbose

# Preview what would be fixed
/debug:eval data-validation --dry-run

# Generate report without fixing
/debug:eval performance-index --report-only
```

## How It Works

This command delegates to the **orchestrator** agent which:

1. **Analyzes the debugging request** and determines optimal approach
2. **Selects appropriate specialized agents** based on task type and complexity
3. **May delegate to validation-controller** for debugging-specific tasks:
   - Issue identification and root cause analysis
   - Systematic debugging methodology
   - Fix implementation with quality controls
4. **Measures debugging performance** using the comprehensive framework:
   - Quality Improvement Score (QIS)
   - Time Efficiency Score (TES)
   - Success Rate tracking
   - Regression detection
   - Overall Performance Index calculation

5. **Generates detailed performance report** with metrics and improvements

### Agent Delegation Process

When using `--verbose` flag, you'll see:
```
🔍 ORCHESTRATOR: Analyzing debugging request...
📋 ORCHESTRATOR: Task type identified: "dashboard debugging"
🎯 ORCHESTRATOR: Selecting agents: validation-controller, code-analyzer
🚀 VALIDATION-CONTROLLER: Beginning systematic analysis...
📊 CODE-ANALYZER: Analyzing code structure and patterns...
```

### Why Orchestrator Instead of Direct Validation-Controller?

- **Better Task Analysis**: Orchestrator considers context, complexity, and interdependencies
- **Multi-Agent Coordination**: Complex issues often require multiple specialized agents
- **Quality Assurance**: Orchestrator ensures final results meet quality standards (≥70/100)
- **Pattern Learning**: Successful approaches are stored for future optimization

4. **Measures debugging performance** using the comprehensive framework:
   - Quality Improvement Score (QIS)
   - Time Efficiency Score (TES)
   - Success Rate tracking
   - Regression detection
   - Overall Performance Index calculation

5. **Generates detailed performance report** with metrics and improvements

## Available Targets

### `dashboard`
- **Issue**: Quality Score Timeline chart data inconsistency
- **Symptom**: Chart values change when switching time periods and returning
- **Root Cause**: `random.uniform()` without deterministic seeding in `dashboard.py:710-712`
- **Expected Fix**: Replace random generation with deterministic seeded calculation
- **Complexity**: Medium (requires code modification and testing)

### `performance-index`
- **Issue**: AI Debugging Performance Index calculation accuracy
- **Symptom**: Potential discrepancies in performance measurements
- **Root Cause**: QIS formula implementation and regression penalty system
- **Expected Fix**: Validate and correct calculation methodology
- **Complexity**: High (requires framework validation)

### `data-validation`
- **Issue**: Data integrity across dashboard metrics
- **Symptom**: Inconsistent data between different charts
- **Root Cause**: Data processing and caching inconsistencies
- **Expected Fix**: Standardize data loading and processing
- **Complexity**: Medium (requires data pipeline analysis)

## Debugging Performance Framework

The evaluation uses the comprehensive debugging performance framework:

### Quality Improvement Score (QIS)
```
QIS = 0.6 × FinalQuality + 0.4 × (GapClosedPct × 100/100)
```

### Time Efficiency Score (TES)
- Measures speed of problem identification and resolution
- Accounts for task complexity and analysis depth
- Ideal debugging time: ~30 minutes per task

### Performance Index with Regression Penalty
```
PI = (0.40 × QIS) + (0.35 × TES) + (0.25 × SR) − Penalty
```

Where Penalty = RegressionRate × 20

## Skills Utilized

- **autonomous-agent:validation-standards** - Tool requirements and consistency checks
- **autonomous-agent:quality-standards** - Best practices and quality benchmarks
- **autonomous-agent:pattern-learning** - Historical debugging patterns and approaches
- **autonomous-agent:security-patterns** - Security-focused debugging methodology

## Expected Output

### Terminal Summary
```
🔍 DEBUGGING PERFORMANCE EVALUATION
Target: dashboard data inconsistency

📊 PERFORMANCE METRICS:
• Initial Quality: 85/100
• Final Quality: 96/100 (+11 points)
• QIS (Quality Improvement): 78.5/100
• Time Efficiency: 92/100
• Success Rate: 100%
• Regression Penalty: 0
• Performance Index: 87.2/100

⚡ DEBUGGING RESULTS:
✓ Root cause identified: random.uniform() without seeding
✓ Fix implemented: deterministic seeded calculation
✓ Quality improvement: +11 points
✓ Time to resolution: 4.2 minutes

📄 Full report: .claude/reports/debug-eval-dashboard-2025-10-24.md
⏱ Completed in 4.2 minutes
```

### Detailed Report
Located at: `.claude/reports/debug-eval-<target>-YYYY-MM-DD.md`

Comprehensive analysis including:
- Issue identification and root cause analysis
- Step-by-step debugging methodology
- Code changes and quality improvements
- Performance metrics breakdown
- Validation and testing results
- Recommendations for future improvements

## Integration with AI Debugging Performance Index

Each `/eval-debug` execution automatically:
1. Records debugging task in quality history
2. Calculates QIS based on quality improvements made
3. Measures time efficiency for problem resolution
4. Updates model performance metrics
5. Stores debugging patterns for future learning
6. Updates AI Debugging Performance Index chart

## Examples

### Analyze Dashboard Data Inconsistency
```bash
/eval-debug dashboard
```

### Validate Performance Index Calculations
```bash
/eval-debug performance-index
```

### Comprehensive Data Validation
```bash
/eval-debug data-validation
```

## Benefits

**For Debugging Performance Measurement**:
- Real-world debugging scenarios with measurable outcomes
- Comprehensive performance metrics using established framework
- Quality improvement tracking over time
- Time efficiency analysis for different problem types

**For Code Quality**:
- Identifies and fixes actual issues in codebase
- Improves system reliability and data integrity
- Validates fixes with quality controls
- Documents debugging approaches for future reference

**For Learning System**:
- Builds database of debugging patterns and solutions
- Improves debugging efficiency over time
- Identifies most effective debugging approaches
- Tracks performance improvements across different problem types