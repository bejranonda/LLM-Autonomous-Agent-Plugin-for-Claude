---
name: learn:performance
description: Display performance analytics dashboard with metrics, trends, and optimization recommendations
delegates-to: autonomous-agent:orchestrator
---

# Performance Report Command

Generate comprehensive performance analytics report showing learning effectiveness, skill/agent performance trends, quality improvements, and optimization recommendations.

## How It Works

1. **Data Collection**: Reads pattern database, quality history, and task queue
2. **Metrics Calculation**: Computes learning effectiveness, trend analysis, success rates
3. **Insight Generation**: Identifies patterns, correlations, and improvement opportunities
4. **Visualization**: Creates ASCII charts showing performance over time
5. **Recommendations**: Provides actionable optimization suggestions
6. **Report Generation**: Outputs comprehensive analytics report

**IMPORTANT**: When delegating this command to the orchestrator agent, the agent MUST present the complete performance report with charts, metrics, and prioritized recommendations. This command is specifically designed to show comprehensive results to the user. Silent completion is not acceptable.

## Usage

```bash
/autonomous-agent:learn:performance
```

## What You'll Get

### Learning Effectiveness Analysis
- Pattern database growth rate and diversity
- Knowledge coverage across task types
- Pattern reuse rates and success correlation
- Time to competency for different task types
- Overall learning velocity metrics

### Skill Performance Dashboard
- Success rate per skill over time
- Quality score correlation with skill usage
- Top skill combinations and their effectiveness
- Skill loading efficiency metrics
- Recommendation accuracy analysis

### Agent Performance Summary
- Delegation success rates per agent
- Average quality scores achieved
- Task completion time analysis
- Agent specialization effectiveness
- Background task performance

### Quality Trend Visualization
- Quality score trends over time (ASCII charts)
- Improvement rate calculations
- Baseline vs. current comparison
- Threshold compliance tracking
- Consistency analysis (variance)

### Optimization Recommendations
- Top 5 actionable recommendations prioritized by impact
- Pattern-based insights (which patterns work best)
- Quality-based insights (when to run quality checks)
- Agent-based insights (optimal delegation strategies)
- Efficiency improvements (parallelization opportunities)

## Example Output

The orchestrator MUST present the full performance report. The example output in this file demonstrates the EXACT format expected. Do NOT summarize - show the complete report:

```
=======================================================
  PERFORMANCE ANALYTICS REPORT
=======================================================
Generated: 2025-10-21 11:30:00

+- Executive Summary ----------------------------------+
| Learning Status: [PASS] Active and highly effective      |
| Total Patterns:  47 patterns across 8 task types    |
| Quality Trend:   ^ +18% improvement (30 days)       |
| Pattern Reuse:   67% reuse rate (excellent)         |
+------------------------------------------------------+

+- Learning Effectiveness -----------------------------+
| Knowledge Growth:    3.2 patterns/week               |
| Coverage:           8/10 common task types           |
| Improvement Rate:   +1.2 quality points/week        |
| Time to Competency: ~5 similar tasks                |
+------------------------------------------------------+

+- Skill Performance ----------------------------------+
| pattern-learning          ████████████ 92% (12)     |
| quality-standards         ███████████░ 88% (15)     |
| code-analysis            ██████████░░ 85% (8)      |
| documentation-practices   ████████░░░░ 78% (6)      |
| testing-strategies       ███████░░░░░ 72% (5)      |
|                                                      |
| Top Combination: pattern-learning + quality -> 94/100|
+------------------------------------------------------+

+- Quality Trends (30 Days) ---------------------------+
| 100 |                            [X]                   |
|  90 |        [X]--[X]--[X]        [X]--[X]-+                   |
|  80 |    [X]--+              ++                        |
|  70 |[X]---+                 | (threshold)             |
|  60 |                                                |
|     +------------------------------------           |
|     Week 1  Week 2  Week 3  Week 4                  |
|                                                      |
| [PASS] Quality improved 23% from baseline (65 -> 92)     |
| [PASS] Consistently above threshold for 3 weeks         |
| [PASS] 15% improvement after learning 10+ patterns      |
+------------------------------------------------------+

+- Top Recommendations --------------------------------+
| 1. [HIGH] Use pattern-learning skill more often     |
|    -> +12 points avg quality improvement             |
|    -> 95% success rate (highest)                     |
|                                                      |
| 2. [HIGH] Run quality-controller before completion  |
|    -> +13 points with quality check vs without       |
|    -> 88% auto-fix success rate                      |
|                                                      |
| 3. [MED] Delegate testing to test-engineer          |
|    -> 91% success vs 76% manual                      |
|    -> 35% time savings                               |
|                                                      |
| 4. [MED] Combine pattern-learning + quality skills  |
|    -> Best combination: 94/100 avg quality           |
|                                                      |
| 5. [LOW] Archive patterns with reuse_count = 0     |
|    -> Free up 15% storage, improve query speed       |
+------------------------------------------------------+

=======================================================
  CONCLUSION: Learning system performing excellently
  Continue current approach, implement recommendations
=======================================================
```

## Use Cases

1. **Monitor Learning Progress**: Track how the system improves over time
2. **Identify Optimization Opportunities**: Find which skills/agents to use more/less
3. **Validate Learning Effectiveness**: Prove the autonomous system is working
4. **Troubleshoot Issues**: Understand why quality might be declining
5. **Demonstrate ROI**: Show concrete improvements from the learning system

## Report Frequency

- **Weekly**: Review learning progress and trends
- **Monthly**: Comprehensive analysis and strategy adjustment
- **On-Demand**: When investigating specific performance questions
- **Automated**: After every 10 tasks (orchestrator integration)

## See Also

- `/auto-analyze` - Autonomous project analysis
- `/quality-check` - Comprehensive quality control
- `/learn-patterns` - Initialize pattern learning
