---
name: learning-analytics
description: Display comprehensive learning analytics dashboard showing pattern learning progress, skill effectiveness, prediction accuracy, and improvement trends
---

# Learning Analytics Dashboard

Display comprehensive analytics about the autonomous agent's learning progress, including:

- **Pattern Learning Progress**: Quality trends, learning velocity, improvement rates
- **Skill Effectiveness**: Top performing skills, success rates, quality contributions
- **Agent Performance**: Reliability scores, efficiency ratings, delegation patterns
- **Skill Synergies**: Best skill combinations and their effectiveness
- **Prediction System**: Accuracy metrics and model performance
- **Cross-Project Learning**: Universal patterns and knowledge transfer
- **Learning Insights**: Actionable recommendations and trend analysis

## Execution

Generate and display the learning analytics report:

```bash
python lib/learning_analytics.py show --dir .claude-patterns
```

## Output Format

The command produces a comprehensive terminal dashboard with:

1. **Overview Section**: Total patterns, quality scores, success rates
2. **Quality Trend Chart**: ASCII visualization of quality progression over time
3. **Learning Velocity**: Improvement rates and trajectory analysis
4. **Top Performing Skills**: Rankings by success rate and quality contribution
5. **Top Performing Agents**: Rankings by reliability and efficiency
6. **Skill Synergies**: Best skill combinations discovered
7. **Prediction System Status**: Accuracy and model training metrics
8. **Cross-Project Learning**: Universal pattern statistics
9. **Learning Patterns**: Fastest and slowest learning areas
10. **Key Insights**: Actionable recommendations based on data

## Example Output

```
╔═══════════════════════════════════════════════════════════════════════════╗
║           LEARNING ANALYTICS DASHBOARD - ENHANCED SYSTEM v3.0           ║
╚═══════════════════════════════════════════════════════════════════════════╝

📊 OVERVIEW
───────────────────────────────────────────────────────────────────────────
  Total Patterns Captured: 156
  Overall Quality Score:   88.5/100
  Success Rate:            92.3%
  Recent Quality:          91.2/100 (+2.7)
  Activity (Last 7 days):  12 patterns
  Activity (Last 30 days): 48 patterns

📈 QUALITY TREND OVER TIME
───────────────────────────────────────────────────────────────────────────
  95.0 │                                            ██████████│
       │                                      ████████████████│
       │                                ████████████████████  │
       │                          ████████████████████        │
  87.5 │                    ████████████████                  │
       │              ████████████                            │
       │        ████████                                      │
       │  ████████                                            │
  80.0 │████                                                  │
       └──────────────────────────────────────────────────────┘
         106                                             → 156

  Trend: IMPROVING

🚀 LEARNING VELOCITY
───────────────────────────────────────────────────────────────────────────
  Weeks Analyzed:          8
  Early Average Quality:   85.3/100
  Recent Average Quality:  91.2/100
  Total Improvement:       +5.9 points
  Improvement Rate:        0.74 points/week
  Trajectory:              ACCELERATING
  Acceleration:            +0.52 (speeding up!)

⭐ TOP PERFORMING SKILLS
───────────────────────────────────────────────────────────────────────────
  1. code-analysis              Success: 94.3%  Quality: 18.5
  2. quality-standards          Success: 92.1%  Quality: 17.8
  3. testing-strategies         Success: 89.5%  Quality: 16.2
  4. security-patterns          Success: 91.0%  Quality: 15.9
  5. pattern-learning           Success: 88.7%  Quality: 15.1

🤖 TOP PERFORMING AGENTS
───────────────────────────────────────────────────────────────────────────
  1. code-analyzer              Reliability: 96.9%  Efficiency: 1.02
  2. quality-controller         Reliability: 95.2%  Efficiency: 0.98
  3. test-engineer              Reliability: 93.5%  Efficiency: 0.89
  4. documentation-generator    Reliability: 91.8%  Efficiency: 0.95
  5. frontend-analyzer          Reliability: 90.5%  Efficiency: 1.05

🔗 SKILL SYNERGIES (Top Combinations)
───────────────────────────────────────────────────────────────────────────
  1. code-analysis + quality-standards    Score: 8.5  Uses: 38
     Quality: 92.3  Success: 97.8%  [HIGHLY_RECOMMENDED]
  2. code-analysis + security-patterns    Score: 7.2  Uses: 28
     Quality: 91.0  Success: 96.4%  [HIGHLY_RECOMMENDED]

🎯 PREDICTION SYSTEM STATUS
───────────────────────────────────────────────────────────────────────────
  Status:                  ACTIVE
  Models Trained:          15 skills
  Prediction Accuracy:     87.5%
  ✓ High accuracy - automated recommendations highly reliable

🌐 CROSS-PROJECT LEARNING
───────────────────────────────────────────────────────────────────────────
  Status:                  ACTIVE
  Universal Patterns:      45
  Avg Transferability:     82.3%
  ✓ Knowledge transfer active - benefiting from other projects

💡 KEY INSIGHTS
───────────────────────────────────────────────────────────────────────────
  ✓ Learning is accelerating! Quality improving at 0.74 points/week and speeding up
  ✓ Recent performance (91.2) significantly better than historical average (88.5)
  ✓ Highly effective skill pair discovered: code-analysis + quality-standards (8.5 synergy score)
  ✓ Prediction system highly accurate (87.5%) - trust automated recommendations
  ✓ Fastest learning in: refactoring, bug-fix

╔═══════════════════════════════════════════════════════════════════════════╗
║  Generated: 2025-10-23T14:30:52.123456                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Export Options

### Export as JSON
```bash
python lib/learning_analytics.py export-json --output reports/analytics.json --dir .claude-patterns
```

### Export as Markdown
```bash
python lib/learning_analytics.py export-md --output reports/analytics.md --dir .claude-patterns
```

## Usage Scenarios

### Daily Standup
Review learning progress and identify areas needing attention:
```bash
/learning-analytics
```

### Weekly Review
Export comprehensive report for documentation:
```bash
python lib/learning_analytics.py export-md --output weekly_analytics.md
```

### Performance Investigation
Analyze why quality might be declining or improving:
```bash
/learning-analytics
# Review Learning Velocity and Learning Patterns sections
```

### Skill Selection Validation
Verify which skills and combinations work best:
```bash
/learning-analytics
# Review Top Performing Skills and Skill Synergies sections
```

## Interpretation Guide

### Quality Scores
- **90-100**: Excellent - Optimal performance
- **80-89**: Good - Meeting standards
- **70-79**: Acceptable - Some improvement needed
- **<70**: Needs attention - Review approach

### Learning Velocity
- **Accelerating**: System is learning faster over time (optimal)
- **Linear**: Steady improvement at constant rate (good)
- **Decelerating**: Improvement slowing down (may need new approaches)

### Prediction Accuracy
- **>85%**: High accuracy - Trust automated recommendations
- **70-85%**: Moderate accuracy - System still learning
- **<70%**: Low accuracy - Need more training data

### Skill Synergies
- **Score >5**: Highly recommended combination
- **Score 2-5**: Recommended combination
- **Score <2**: Use with caution

## Frequency Recommendations

- **After every 10 patterns**: Quick check of trends
- **Weekly**: Full review of all sections
- **Monthly**: Deep analysis with exported reports
- **After major changes**: Verify impact on learning

## Notes

- Analytics require at least 10 patterns for meaningful insights
- Learning velocity requires 3+ weeks of data
- Prediction accuracy improves with more training data
- Cross-project learning activates automatically when enabled
- All metrics update in real-time as new patterns are captured