# Model-Adaptive Communication Guidelines

## Overview

This document defines communication style adaptations for optimal cross-model compatibility in the Autonomous Agent Plugin. Each model has specific communication preferences that maximize understanding and execution efficiency.

## Communication Style Matrix

| Model | Terminal Style | File Report Style | Reasoning Approach | Key Characteristics |
|-------|----------------|-------------------|-------------------|-------------------|
| **Claude Sonnet 4.5** | Natural flow with insights | Insightful analysis with context | Nuanced pattern matching | Contextual, adaptive, improvisational |
| **Claude Haiku 4.5** | Concise direct results | Efficient focused analysis | Fast focused reasoning | Efficient, streamlined, direct |
| **Claude Opus 4.1** | Enhanced predictive insights | Sophisticated context with predictions | Enhanced predictive execution | Anticipatory, complex pattern recognition |
| **GLM-4.6** | Structured lists | Detailed procedures | Structured decision trees | Explicit, sequential, unambiguous |
| **Fallback** | Simple clear steps | Basic structured format | Conservative approach | Universal compatibility |

## Model-Specific Communication Protocols

### Claude Sonnet 4.5 Communication Style

#### Terminal Output (15-20 lines max)
```
✅ Task Complete - Autonomous Analysis Ready

🔍 Key Insights:
• Discovered sophisticated pattern learning architecture with cross-model compatibility
• Identified 24 auto-fix patterns achieving 89% success rate across multiple project types
• Found intelligent delegation system optimizing for model-specific strengths

💡 Adaptive Recommendations:
1. [STRATEGIC] Leverage GLM-4.6's structured execution for routine validation tasks
2. [TACTICAL] Use Opus 4.1's enhanced reasoning for complex multi-component analysis
3. [OPERATIONAL] Apply Sonnet's contextual awareness for ambiguous requirement interpretation

📊 Contextual Analysis:
The plugin demonstrates exceptional cross-model optimization with each model playing to its strengths. Pattern learning system shows 15% performance improvement after 10 similar tasks.

📄 Comprehensive insights: .claude/reports/analysis-2025-10-22.md
⏱️ Optimized execution: 2.1s (model-adaptive timing)
```

#### File Report Style
- Natural, flowing explanations
- Contextual insights and implications
- Adaptive terminology based on user expertise
- Pattern recognition highlights
- Cross-model optimization analysis

### Claude Haiku 4.5 Communication Style

#### Terminal Output (Concise & Direct)
```
⚡ Analysis Complete - 88/100 Quality

🎯 Key Findings:
• Cross-model compatibility implemented effectively
• Auto-fix patterns show 87% success rate
• Performance scaling adapted per model

🚀 Recommendations:
1. [HIGH] Use GLM-4.6 for structured validation tasks
2. [MEDIUM] Apply Sonnet 4.5 for complex analysis
3. [LOW] Optimize skill loading where needed

📊 Results:
Efficient execution with fast processing capabilities.

📄 Focused report: .claude/reports/efficient-analysis-2025-10-22.md
⏱️ Fast execution: 1.6s (streamlined performance)
```

#### File Report Style
- Concise, direct explanations
- Efficient presentation of key findings
- Clear action items
- Streamlined analysis
- Fast processing highlights

### Claude Opus 4.1 Communication Style

#### Terminal Output (Enhanced & Predictive)
```
⚡ Optimized Analysis Complete - 95/100 Quality

🎯 Enhanced Findings:
• Cross-model compatibility implemented with 94% effectiveness
• Auto-fix patterns show 91% success rate with optimization potential
• Performance scaling precisely adapted per model (GLM: +25%, Claude: optimized)

🚀 Sophisticated Recommendations:
1. [CRITICAL] Deploy GLM-4.6 for structured validation tasks (+14% efficiency)
2. [HIGH] Optimize skill loading across all Claude models (intelligent disclosure)
3. [MEDIUM] Implement predictive error handling with anticipatory capabilities

📈 Advanced Performance Forecast:
Expected 8% overall improvement across all models after optimization, with complex scenario handling enhanced by 22%.

📄 Detailed analytics: .claude/reports/enhanced-analysis-2025-10-22.md
⏱️ Optimized execution: 1.8s (enhanced performance)
```

#### File Report Style
- Enhanced insights with predictive elements
- Sophisticated context recommendations
- Anticipatory guidance with complex understanding
- Advanced performance forecasting
- Strategic optimization paths with detailed analysis

### GLM-4.6 Communication Style

#### Terminal Output (Structured & Explicit)
```
✓ ANALYSIS COMPLETE - Status: SUCCESS

EXECUTION SUMMARY:
1. Total Files Analyzed: 28 configuration files
2. Lines Processed: 10,955 lines
3. Quality Score Achieved: 92/100
4. Execution Time: 2.3 seconds

KEY FINDINGS:
• Finding 1: Model compatibility system properly configured
• Finding 2: Auto-fix patterns operational (24 patterns loaded)
• Finding 3: Performance scaling implemented for all models

STRUCTURED RECOMMENDATIONS:
1. [ACTION] Resolve TODO items in documentation files
   Priority: HIGH
   Impact: +4 quality points
   Effort: 2-3 hours

2. [ACTION] Add unit tests for Python utilities
   Priority: MEDIUM
   Impact: Improves reliability
   Effort: 4-6 hours

3. [ACTION] Standardize skill versions across components
   Priority: MEDIUM
   Impact: Better consistency
   Effort: 1 hour

DETAILED REPORT: .claude/reports/structured-analysis-2025-10-22.md
EXECUTION STATUS: Completed successfully
```

#### File Report Style
- Structured numbered lists
- Explicit step-by-step procedures
- Clear, unambiguous terminology
- Detailed action items with priorities
- Structured problem-solution format

## Universal Communication Standards

### Two-Tier Presentation (All Models)

#### Tier 1: Terminal Output (Concise)
- **Maximum Length**: 15-20 lines
- **Content**: Key results, top findings, critical recommendations
- **Format**: Model-appropriate style (natural/insightful/structured)
- **Elements**:
  - Status line with key metric
  - 3-4 bullet points (findings/recommendations)
  - File path to detailed report
  - Execution time

#### Tier 2: File Report (Comprehensive)
- **Location**: `.claude/reports/[command]-YYYY-MM-DD.md`
- **Content**: Complete analysis with all findings
- **Format**: Model-appropriate detailed style
- **Sections**:
  - Executive summary
  - Detailed findings
  - Complete recommendations
  - Technical analysis
  - Performance metrics

### Error Communication Protocols

#### Claude Models
- Contextual error explanations
- Pattern-based error prevention suggestions
- Adaptive recovery strategies

#### GLM Models
- Structured error categorization
- Explicit recovery procedures
- Clear action steps

## Implementation Guidelines

### Communication Style Detection
```javascript
function selectCommunicationStyle(detectedModel) {
  const styles = {
    'claude-sonnet': 'natural_insightful',
    'claude-4.5': 'concise_predictive',
    'glm-4.6': 'structured_explicit',
    'fallback': 'universal_simple'
  };
  return styles[detectedModel] || styles.fallback;
}
```

### Output Generation
```javascript
function generateOutput(results, model, targetAudience) {
  const style = selectCommunicationStyle(model);
  const template = loadOutputTemplate(style);

  return template.render({
    ...results,
    modelSpecific: adaptResultsToModel(results, model),
    timing: adaptTimingToModel(results.timing, model),
    quality: adaptQualityTargets(results.quality, model)
  });
}
```

### Quality Score Communication
- **Claude Models**: Emphasize contextual improvements and pattern learning
- **GLM Models**: Emphasize structural metrics and explicit achievements

## Validation Metrics

### Communication Effectiveness
- **Claude Sonnet**: Target >95% user comprehension of nuanced insights
- **Claude 4.5**: Target >90% user adoption of predictive recommendations
- **GLM-4.6**: Target >98% user successful completion of structured steps

### Cross-Model Consistency
- All models must provide equivalent information quality
- Format differences should not impact content completeness
- Performance timing should be model-appropriate

## Best Practices

### Do's
- Maintain two-tier presentation (terminal + file)
- Keep terminal output concise (15-20 lines max)
- Provide detailed file reports
- Adapt communication style to detected model
- Include file paths in terminal output
- Show execution timing appropriate to model

### Don'ts
- Use Claude-specific terminology for GLM models
- Provide 50+ lines of terminal output
- Skip detailed file reports
- Use ambiguous language for structured models
- Ignore model-specific timing expectations

## Evolution Strategy

This communication framework evolves with:
1. **User Feedback**: Continuous improvement based on user experience
2. **Model Updates**: Adaptation to new model capabilities
3. **Performance Data**: Optimization based on execution metrics
4. **Cross-Learning**: Pattern sharing across communication styles

The goal is universal comprehension while leveraging each model's unique communication strengths.