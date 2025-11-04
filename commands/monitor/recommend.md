---
name: monitor:recommend
description: Get smart workflow and optimization recommendations based on learned patterns
delegates-to: orchestrator
---


# Recommend Command

Get intelligent recommendations for optimal workflows, skill combinations, and agent delegations based on learned patterns before starting a task.

## How It Works

1. **Task Analysis**: Analyzes your task description to classify type and complexity
2. **Pattern Matching**: Queries pattern database for similar successful tasks
3. **Probability Calculation**: Calculates success probabilities based on historical data
4. **Ranking**: Ranks approaches by expected quality, time, and confidence
5. **Recommendation Generation**: Provides top 3 approaches with detailed trade-offs
6. **Risk Assessment**: Identifies potential issues and mitigation strategies

**IMPORTANT**: When delegating this command to the orchestrator agent, the agent MUST present comprehensive recommendations with expected outcomes, confidence levels, alternatives, and risk assessments. Silent completion is not acceptable.

## Usage

```bash
# Get recommendations for a specific task
/monitor:recommend "refactor authentication module"

# Or just invoke for general guidance
/monitor:recommend
```

## What You'll Get

### Best Approach Recommendation
- **Expected Quality Score**: Predicted quality (e.g., 94/100)
- **Estimated Time**: How long it will take (e.g., 12-15 minutes)
- **Confidence Level**: How confident the prediction is (e.g., 92%)
- **Recommended Skills**: Which skills to load and why
- **Recommended Agents**: Which agents to delegate to
- **Based On**: Number of similar successful patterns

### Alternative Approaches
- Comparison of different strategies
- Trade-offs between quality, time, and complexity
- When to use each approach

### Skill Synergy Analysis
- Which skill combinations work best together
- Synergy scores showing complementarity
- Expected quality improvement from combinations

### Agent Delegation Strategy
- Optimal agent workflow
- Sequential vs parallel execution
- Time savings from parallelization

### Quality Prediction
- Predicted quality score with confidence interval
- Key factors influencing the prediction
- Comparison to baseline (without patterns)

### Time Estimation
- Estimated duration with confidence range
- Time breakdown by factors
- Historical comparison with similar tasks

### Risk Assessment
- Overall risk level (LOW/MEDIUM/HIGH)
- Specific risk factors identified
- Mitigation strategies for each risk
- Adjusted predictions accounting for risks

## Example Output

The orchestrator MUST present the full recommendation report. The example output in this file demonstrates the EXACT format expected. Do NOT summarize - show the complete recommendations:

```
════════════════════════════════════════════════════════
  SMART RECOMMENDATIONS
════════════════════════════════════════════════════════

Task: "Refactor authentication module"
Analyzed as: feature-implementation, medium-high complexity

┌─ 🎯 RECOMMENDED APPROACH (92% confidence) ─────────────┐
│                                                         │
│ Expected Quality: 94/100 (+19 from baseline)          │
│ Estimated Time:   12-15 minutes                        │
│                                                         │
│ Recommended Skills:                                     │
│ 1. ✓ code-analysis (91% success rate)                 │
│    → Proven effective for refactoring tasks            │
│ 2. ✓ quality-standards (88% success rate)             │
│    → Validation and compliance checking                │
│ 3. ✓ pattern-learning (95% success rate)              │
│    → Captures refactoring patterns for reuse           │
│                                                         │
│ Recommended Agents:                                     │
│ • code-analyzer → Structure analysis and mapping       │
│ • quality-controller → Validation + auto-fix           │
│                                                         │
│ Parallelization:                                        │
│ • background-task-manager → Security scan (parallel)   │
│   Expected time savings: 25%                           │
│                                                         │
│ Based on: 3 similar successful patterns                │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─ 📊 ALTERNATIVE APPROACHES ────────────────────────────┐
│                                                         │
│ 2. Minimal Approach (65% confidence)                   │
│    Quality: 82/100 | Time: 10 min                     │
│    Skills: code-analysis only                          │
│    ⚠ Lower quality but faster                          │
│                                                         │
│ 3. Comprehensive Approach (78% confidence)             │
│    Quality: 91/100 | Time: 20 min                     │
│    Skills: All 5 skills loaded                         │
│    ⚠ Higher quality but slower                         │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─ ⚠️  RISK ASSESSMENT ────────────────────────────────────┐
│                                                         │
│ Overall Risk: MEDIUM (62/100)                          │
│                                                         │
│ 1. [HIGH] Legacy Code Complexity                       │
│    → Mitigation: Use code-analyzer first               │
│    → Add 5 minutes to estimate                         │
│                                                         │
│ 2. [MEDIUM] Security Critical                          │
│    → Mitigation: Add testing-strategies skill          │
│    → Increase quality threshold to 90/100              │
│                                                         │
│ Adjusted Prediction:                                    │
│ Quality: 91/100 | Time: 19 min | Success: 89%         │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─ 💡 KEY INSIGHTS ──────────────────────────────────────┐
│                                                         │
│ ✓ Using code-analysis improves quality by +9 points    │
│ ✓ Delegating to quality-controller saves 30% time      │
│ ✓ Pattern reuse success rate: 87%                      │
│ ✓ 3-skill combinations outperform single skills by 12pts│
│ ⚠ First-time auth task: expect learning curve          │
│                                                         │
└─────────────────────────────────────────────────────────┘

════════════════════════════════════════════════════════
  RECOMMENDATION: Proceed with recommended approach
  Orchestrator will auto-apply if confidence > 80%
════════════════════════════════════════════════════════
```

## Use Cases

1. **Pre-Task Planning**: Get optimal approach before starting work
2. **Quality Optimization**: Find the approach that maximizes quality
3. **Time Optimization**: Find the fastest approach meeting quality threshold
4. **Risk Mitigation**: Identify and address potential issues early
5. **Learning**: Understand which patterns work best for different tasks

## Benefits

- **Higher Quality**: +8-12 points on average when following recommendations
- **Faster Execution**: 15-25% time savings through optimized workflows
- **Better Decisions**: Data-driven rather than guesswork
- **Risk Reduction**: Proactive issue identification and mitigation
- **Continuous Improvement**: Recommendations get smarter with every task

## Confidence Levels

- **90-100%**: Very High - Strong pattern match, auto-apply recommended
- **80-89%**: High - Good pattern match, safe to follow
- **70-79%**: Medium - Some uncertainty, review recommended
- **60-69%**: Low - Limited data, use caution
- **<60%**: Very Low - No similar patterns, baseline approach

## Integration

The smart recommender integrates with:
- **Orchestrator**: Auto-applies high-confidence recommendations
- **Performance Analytics**: Tracks recommendation accuracy
- **Learning Engine**: Improves predictions based on outcomes
- **Quality Controller**: Adjusts thresholds based on risk assessment

## See Also

- `/auto-analyze` - Autonomous project analysis
- `/quality-check` - Comprehensive quality control
- `/performance-report` - Performance analytics dashboard
- `/learn-patterns` - Initialize pattern learning
