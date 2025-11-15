---
name: analyze:groups
description: Deep analysis of four-tier group behavior, collaboration patterns, and optimization recommendations
version: 7.0.0
category: analysis
---

# Analyze Groups Command

Perform comprehensive deep analysis of all four agent groups including collaboration patterns, bottlenecks, optimization opportunities, and actionable recommendations for improving group coordination and performance.

## What This Command Does

**Analyzes**:
1. **Group Collaboration Patterns** - How groups work together, communication patterns, handoff quality
2. **Performance Bottlenecks** - Where delays occur, which groups need optimization
3. **Specialization Effectiveness** - Whether groups are specializing appropriately
4. **Knowledge Flow Analysis** - How knowledge transfers between groups
5. **Decision Quality Analysis** - Group 2 decision-making effectiveness
6. **Validation Effectiveness** - Group 4 validation impact on quality

**Delivers**:
- Root cause analysis of performance issues
- Specific optimization recommendations
- Communication improvement strategies
- Specialization guidance
- Actionable next steps

## Execution Steps

### Step 1: Load Comprehensive Data

```python
from lib.group_collaboration_system import get_group_collaboration_stats, analyze_workflow_efficiency
from lib.group_performance_tracker import get_group_performance, compare_groups, analyze_workflow_efficiency as group_workflow
from lib.inter_group_knowledge_transfer import get_knowledge_transfer_stats, get_transfer_effectiveness
from lib.group_specialization_learner import get_specialization_profile, get_recommended_group_for_task, get_learning_insights
from lib.agent_feedback_system import get_feedback_stats
from lib.decision_explainer import get_all_explanations
from lib.proactive_suggester import get_statistics as get_suggestion_stats

# Gather all data for last 100 tasks
collaboration_stats = get_group_collaboration_stats()
workflow_efficiency = analyze_workflow_efficiency()
knowledge_effectiveness = get_transfer_effectiveness()
learning_insights = get_learning_insights()
suggestion_stats = get_suggestion_stats()
```

### Step 2: Analyze Group Collaboration Patterns

```python
def analyze_collaboration_patterns(collab_stats):
    """Identify collaboration patterns and issues"""

    patterns_found = []
    issues_found = []

    # Pattern 1: Sequential Flow (Normal)
    if collab_stats['group_1_to_2']['success_rate'] > 0.9 and \
       collab_stats['group_2_to_3']['success_rate'] > 0.9 and \
       collab_stats['group_3_to_4']['success_rate'] > 0.9:
        patterns_found.append({
            "pattern": "healthy_sequential_flow",
            "description": "Groups collaborate sequentially with high success",
            "status": "excellent"
        })

    # Pattern 2: Feedback Loop Effectiveness
    feedback_loops = [
        collab_stats.get('group_4_to_1', {}),
        collab_stats.get('group_4_to_2', {}),
        collab_stats.get('group_4_to_3', {})
    ]

    avg_feedback_effectiveness = sum(loop.get('effectiveness', 0) for loop in feedback_loops) / 3
    if avg_feedback_effectiveness < 0.7:
        issues_found.append({
            "issue": "weak_feedback_loops",
            "severity": "medium",
            "description": "Group 4 feedback not effectively improving other groups",
            "recommendation": "Review feedback quality and actionability"
        })

    # Pattern 3: Bottleneck Detection
    communication_times = {
        "G1->G2": collab_stats['group_1_to_2'].get('avg_time_seconds', 0),
        "G2->G3": collab_stats['group_2_to_3'].get('avg_time_seconds', 0),
        "G3->G4": collab_stats['group_3_to_4'].get('avg_time_seconds', 0)
    }

    max_time = max(communication_times.values())
    for flow, time in communication_times.items():
        if time > max_time * 0.7:  # More than 70% of max
            issues_found.append({
                "issue": "communication_bottleneck",
                "severity": "high",
                "location": flow,
                "description": f"Communication delay in {flow}: {time}s",
                "recommendation": f"Optimize {flow.split('->')[0]} output preparation"
            })

    return patterns_found, issues_found
```

### Step 3: Analyze Performance Bottlenecks

```python
def identify_bottlenecks():
    """Identify which groups are performance bottlenecks"""

    bottlenecks = []

    for group_num in [1, 2, 3, 4]:
        perf = get_group_performance(group_num)

        # Check success rate
        if perf.get('success_rate', 1.0) < 0.8:
            bottlenecks.append({
                "group": group_num,
                "issue": "low_success_rate",
                "value": perf['success_rate'],
                "severity": "high",
                "recommendation": "Review group training and specialization"
            })

        # Check execution time
        if perf.get('avg_execution_time', 0) > 300:  # 5 minutes
            bottlenecks.append({
                "group": group_num,
                "issue": "slow_execution",
                "value": perf['avg_execution_time'],
                "severity": "medium",
                "recommendation": "Profile and optimize slow operations"
            })

        # Check quality output
        if perf.get('avg_quality_score', 100) < 75:
            bottlenecks.append({
                "group": group_num,
                "issue": "low_quality_output",
                "value": perf['avg_quality_score'],
                "severity": "high",
                "recommendation": "Improve group capabilities or adjust expectations"
            })

    return bottlenecks
```

### Step 4: Analyze Specialization Effectiveness

```python
def analyze_specialization():
    """Check if groups are developing appropriate specializations"""

    specialization_analysis = {}

    for group_num in [1, 2, 3, 4]:
        profile = get_specialization_profile(group_num)

        specializations = profile.get('specializations', [])
        task_count = profile.get('total_tasks', 0)

        # Ideal: 3-5 clear specializations after 100+ tasks
        if task_count < 50:
            status = "insufficient_data"
            recommendation = f"Need {50 - task_count} more tasks to identify specializations"
        elif len(specializations) == 0:
            status = "no_specialization"
            recommendation = "Group not developing specializations - may need more diverse tasks"
        elif len(specializations) < 3:
            status = "emerging"
            recommendation = "Specializations emerging - continue diverse task exposure"
        elif len(specializations) <= 5:
            status = "optimal"
            recommendation = "Good specialization balance - maintain current task distribution"
        else:
            status = "over_specialized"
            recommendation = "Too many specializations - may indicate lack of focus"

        specialization_analysis[f"Group {group_num}"] = {
            "status": status,
            "specializations": specializations,
            "task_count": task_count,
            "recommendation": recommendation
        }

    return specialization_analysis
```

### Step 5: Analyze Knowledge Flow

```python
def analyze_knowledge_flow(knowledge_stats):
    """Analyze how knowledge flows between groups"""

    flow_analysis = {
        "total_knowledge": knowledge_stats.get('total_knowledge', 0),
        "successful_transfers": knowledge_stats.get('successful_transfers', 0),
        "transfer_success_rate": knowledge_stats.get('transfer_success_rate', 0),
        "flow_patterns": []
    }

    # Identify dominant knowledge sources
    sources = {}
    for transfer in knowledge_stats.get('transfers', []):
        source = transfer.get('source_group')
        sources[source] = sources.get(source, 0) + 1

    # Check if knowledge is distributed or concentrated
    if sources:
        max_source = max(sources.values())
        if max_source > sum(sources.values()) * 0.6:
            flow_analysis['flow_patterns'].append({
                "pattern": "concentrated_source",
                "description": f"Group {max(sources, key=sources.get)} is primary knowledge source ({max_source} items)",
                "recommendation": "Encourage knowledge sharing from other groups"
            })
        else:
            flow_analysis['flow_patterns'].append({
                "pattern": "distributed_sources",
                "description": "Knowledge well-distributed across groups",
                "status": "healthy"
            })

    # Check transfer effectiveness
    if flow_analysis['transfer_success_rate'] < 0.7:
        flow_analysis['flow_patterns'].append({
            "pattern": "low_transfer_effectiveness",
            "severity": "medium",
            "description": f"Knowledge transfer success rate: {flow_analysis['transfer_success_rate']:.1%}",
            "recommendation": "Improve knowledge quality, context, and applicability"
        })

    return flow_analysis
```

### Step 6: Decision Quality Analysis (Group 2)

```python
def analyze_decision_quality():
    """Analyze Group 2 decision-making effectiveness"""

    group2_perf = get_group_performance(2)
    explanations = get_all_explanations()  # Get recent decision explanations

    analysis = {
        "total_decisions": group2_perf.get('total_tasks', 0),
        "decision_accuracy": group2_perf.get('success_rate', 0),
        "avg_confidence": group2_perf.get('avg_confidence', 0),
        "user_alignment": 0,  # From user_preference_learner
        "issues": [],
        "strengths": []
    }

    # Check decision accuracy
    if analysis['decision_accuracy'] < 0.85:
        analysis['issues'].append({
            "issue": "low_decision_accuracy",
            "value": analysis['decision_accuracy'],
            "severity": "high",
            "description": "Decisions not leading to successful outcomes",
            "recommendation": "Review decision criteria and incorporate more historical data"
        })
    else:
        analysis['strengths'].append("High decision accuracy")

    # Check confidence calibration
    if analysis['avg_confidence'] > 0.9 and analysis['decision_accuracy'] < 0.85:
        analysis['issues'].append({
            "issue": "overconfident_decisions",
            "severity": "medium",
            "description": "Confidence higher than actual success rate",
            "recommendation": "Calibrate confidence scoring - add uncertainty factors"
        })

    # Check explanation quality
    if len(explanations) > 0:
        avg_explanation_completeness = sum(
            len(e.get('why_chosen', [])) + len(e.get('why_not_alternatives', []))
            for e in explanations
        ) / len(explanations)

        if avg_explanation_completeness < 5:
            analysis['issues'].append({
                "issue": "sparse_explanations",
                "severity": "low",
                "description": "Decision explanations lack detail",
                "recommendation": "Enhance decision_explainer to provide more comprehensive reasoning"
            })

    return analysis
```

### Step 7: Validation Effectiveness Analysis (Group 4)

```python
def analyze_validation_effectiveness():
    """Analyze Group 4 validation impact"""

    group4_perf = get_group_performance(4)

    analysis = {
        "total_validations": group4_perf.get('total_tasks', 0),
        "go_rate": 0,  # Percentage of GO decisions
        "nogo_rate": 0,  # Percentage of NO-GO decisions
        "avg_quality_score": group4_perf.get('avg_quality_score', 0),
        "feedback_effectiveness": 0,
        "issues": [],
        "impact": []
    }

    # Ideal GO rate: 70-85% (too high = not catching issues, too low = too strict)
    # This data would come from validation results
    # For now, use placeholders

    if analysis['go_rate'] > 0.9:
        analysis['issues'].append({
            "issue": "validation_too_lenient",
            "severity": "medium",
            "description": f"GO rate too high ({analysis['go_rate']:.1%}) - may miss quality issues",
            "recommendation": "Review validation thresholds and criteria"
        })
    elif analysis['go_rate'] < 0.6:
        analysis['issues'].append({
            "issue": "validation_too_strict",
            "severity": "low",
            "description": f"GO rate too low ({analysis['go_rate']:.1%}) - may cause unnecessary iterations",
            "recommendation": "Consider relaxing validation thresholds or improving Group 3 output quality"
        })

    # Check if validation is improving quality
    # Compare quality scores before/after validation feedback
    # This would require analysis of quality trends after Group 4 feedback

    return analysis
```

### Step 8: Generate Comprehensive Analysis Report

**Report Structure**:

```markdown
# Four-Tier Group Analysis Report
Generated: {timestamp}
Analysis Period: Last {n} tasks

## Executive Summary

**Overall Health**: {score}/100 ({status})

**Key Findings**:
1. {finding_1}
2. {finding_2}
3. {finding_3}

**Critical Issues**: {critical_count}
**Optimization Opportunities**: {opportunity_count}

---

## 1. Collaboration Pattern Analysis

### Identified Patterns

#### Pattern: {pattern_name}
**Status**: {excellent/good/needs_attention}
**Description**: {description}
**Impact**: {impact_description}

### Collaboration Issues

#### Issue: {issue_name}
**Severity**: {high/medium/low}
**Location**: {group_flow}
**Description**: {detailed_description}

**Root Cause Analysis**:
- {cause_1}
- {cause_2}

**Recommendation**:
- {recommendation_1}
- {recommendation_2}

**Expected Improvement**: {improvement_description}

---

## 2. Performance Bottleneck Analysis

### Bottlenecks Identified

#### Bottleneck: {bottleneck_name}
**Group**: Group {group_num} ({group_name})
**Type**: {slow_execution/low_success/poor_quality}
**Severity**: {high/medium/low}

**Metrics**:
- Current Performance: {metric_value}
- Expected Performance: {target_value}
- Gap: {gap_value}

**Impact on System**:
{impact_description}

**Root Cause**:
{root_cause_analysis}

**Optimization Strategy**:
1. **Immediate Actions** (Next 1-5 tasks):
   - {action_1}
   - {action_2}

2. **Short-term Improvements** (Next 10-20 tasks):
   - {improvement_1}
   - {improvement_2}

3. **Long-term Optimization** (Next 50+ tasks):
   - {strategy_1}
   - {strategy_2}

**Expected Results**:
- Performance Improvement: {improvement}%
- Time Savings: {time} per task
- Quality Impact: +{points} points

---

## 3. Specialization Analysis

### Group Specialization Status

#### Group 1 (Strategic Analysis & Intelligence)
**Status**: {optimal/emerging/no_specialization/over_specialized}
**Task Count**: {count}

**Current Specializations**:
1. {specialization_1}: {success_rate}% success, {count} tasks
2. {specialization_2}: {success_rate}% success, {count} tasks
3. {specialization_3}: {success_rate}% success, {count} tasks

**Analysis**:
{analysis_description}

**Recommendation**:
{recommendation}

---

(Repeat for Groups 2, 3, 4)

---

## 4. Knowledge Flow Analysis

### Knowledge Transfer Effectiveness

**Total Knowledge Base**: {count} items
**Successful Transfers**: {success_count} ({success_rate}%)
**Knowledge Sources**:
- Group 1: {count} items
- Group 2: {count} items
- Group 3: {count} items
- Group 4: {count} items

### Flow Patterns

#### Pattern: {pattern_name}
**Description**: {description}
**Impact**: {positive/negative}
**Recommendation**: {recommendation}

### Knowledge Gaps

**Identified Gaps**:
1. {gap_description} - Missing knowledge in {area}
2. {gap_description} - Underutilized knowledge from {source}

**Impact**: {impact_description}

**Actions**:
- {action_1}
- {action_2}

---

## 5. Decision Quality Analysis (Group 2)

### Decision-Making Effectiveness

**Total Decisions**: {count}
**Decision Accuracy**: {accuracy}%
**Average Confidence**: {confidence}
**User Alignment**: {alignment}%

### Strengths
- {strength_1}
- {strength_2}

### Areas for Improvement

#### Issue: {issue_name}
**Severity**: {severity}
**Description**: {description}

**Analysis**:
{detailed_analysis}

**Recommendation**:
{actionable_recommendation}

**Expected Impact**:
- Decision Accuracy: +{improvement}%
- User Satisfaction: +{improvement}%

---

## 6. Validation Effectiveness Analysis (Group 4)

### Validation Impact

**Total Validations**: {count}
**GO Rate**: {rate}%
**NO-GO Rate**: {rate}%
**Average Quality Score**: {score}/100

### Five-Layer Performance
- Functional (30 pts): {avg}/30 ({status})
- Quality (25 pts): {avg}/25 ({status})
- Performance (20 pts): {avg}/20 ({status})
- Integration (15 pts): {avg}/15 ({status})
- UX (10 pts): {avg}/10 ({status})

### Validation Effectiveness

**Feedback Impact**:
- Quality Improvements Driven: +{points} avg
- Issues Prevented: {count}
- Iterations Saved: {count}

### Issues & Recommendations

{issue_analysis}

---

## 7. Optimization Roadmap

### Immediate Actions (Implement Now)

#### Action 1: {action_name}
**Priority**: High
**Group(s) Affected**: {groups}
**Implementation**: {steps}
**Expected Impact**: {impact}
**Effort**: {hours} hours

---

(Additional immediate actions)

---

### Short-Term Improvements (Next 10-20 Tasks)

#### Improvement 1: {improvement_name}
**Objective**: {objective}
**Implementation Strategy**: {strategy}
**Success Metrics**: {metrics}
**Timeline**: {timeline}

---

### Long-Term Strategic Changes (Next 50+ Tasks)

#### Strategy 1: {strategy_name}
**Vision**: {vision_statement}
**Approach**: {approach_description}
**Milestones**: {milestones}
**Expected Transformation**: {transformation_description}

---

## 8. Success Metrics & KPIs

### Target Metrics (30-day goals)

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Overall Quality Score | {current} | {target} | {gap} |
| Average Iterations | {current} | {target} | {gap} |
| Decision Accuracy | {current}% | {target}% | {gap}% |
| Communication Success | {current}% | {target}% | {gap}% |
| GO Rate | {current}% | {target}% | {gap}% |

### Tracking Plan

**Weekly Checkpoints**:
- Run `/autonomous-agent:monitor:groups` weekly
- Track KPI progress
- Adjust strategies as needed

**Monthly Reviews**:
- Run `/autonomous-agent:analyze:groups` monthly
- Comprehensive performance review
- Strategic adjustments

---

## Conclusion

**System Status**: {status}

**Key Takeaways**:
1. {takeaway_1}
2. {takeaway_2}
3. {takeaway_3}

**Next Steps**:
1. {next_step_1}
2. {next_step_2}
3. {next_step_3}

**Confidence in Recommendations**: {confidence}%

---

Report Path: .claude/data/reports/group-analysis-{date}.md
```

## Result Presentation

**Terminal Output (15-20 lines max)**:
```
+==============================================================+
|      FOUR-TIER GROUP ANALYSIS REPORT                         |
+==============================================================+

Overall Health: {score}/100 ({status})
Analysis Period: Last {n} tasks

KEY FINDINGS:
  [PASS] {finding_1}
  [WARN]️  {finding_2}
  [FAIL] {finding_3}

CRITICAL ISSUES: {count}
  * {issue_1}
  * {issue_2}

OPTIMIZATION OPPORTUNITIES: {count}
  * {opportunity_1}
  * {opportunity_2}

TOP RECOMMENDATIONS:
  1. [{priority}] {recommendation_1}
  2. [{priority}] {recommendation_2}

📄 Detailed Analysis: .claude/data/reports/group-analysis-{date}.md
⏱️  Execution Time: {time}s
```

**File Report**: Save complete analysis to `.claude/data/reports/group-analysis-YYYY-MM-DD.md`

## Notes

- **Deep Analysis**: Goes beyond monitoring to identify root causes
- **Actionable**: Every issue comes with specific recommendations
- **Prioritized**: Clear immediate, short-term, and long-term actions
- **Data-Driven**: Based on comprehensive metrics across all systems
- **Run Monthly**: Or when performance issues are observed
- **Complements**: `/autonomous-agent:monitor:groups` (real-time) vs `/autonomous-agent:analyze:groups` (deep dive)

## Integration

Uses all four-tier learning systems:
- `lib/group_collaboration_system.py`
- `lib/group_performance_tracker.py`
- `lib/inter_group_knowledge_transfer.py`
- `lib/group_specialization_learner.py`
- `lib/agent_performance_tracker.py`
- `lib/agent_feedback_system.py`
- `lib/decision_explainer.py`
- `lib/proactive_suggester.py`
