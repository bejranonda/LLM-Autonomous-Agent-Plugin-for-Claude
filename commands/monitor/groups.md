---
name: monitor:groups
description: Real-time monitoring of four-tier group performance, communication, and specialization metrics
version: 7.0.0
category: monitoring
---

# Monitor Groups Command

Display comprehensive real-time metrics for all four agent groups including performance, communication effectiveness, specialization, and learning progress.

## What This Command Does

**Analyzes and displays**:
1. **Group Performance Metrics** - Success rates, quality scores, execution times per group
2. **Inter-Group Communication** - Message flow, success rates, feedback effectiveness
3. **Group Specialization** - What each group excels at based on task history
4. **Knowledge Transfer** - Cross-group learning effectiveness
5. **Decision Quality** - Group 2 decision accuracy and user alignment
6. **Validation Effectiveness** - Group 4 validation pass rates

## Execution Steps

Follow these steps to generate comprehensive group monitoring report:

### Step 1: Load All Group Data

```python
from lib.group_collaboration_system import get_group_collaboration_stats
from lib.group_performance_tracker import get_group_performance, compare_groups
from lib.inter_group_knowledge_transfer import get_knowledge_transfer_stats
from lib.group_specialization_learner import get_specialization_profile, get_learning_insights
from lib.agent_performance_tracker import get_agent_performance

# Load all statistics
collab_stats = get_group_collaboration_stats()
knowledge_stats = get_knowledge_transfer_stats()
learning_insights = get_learning_insights()
```

### Step 2: Analyze Each Group

**For Group 1 (Strategic Analysis & Intelligence)**:
```python
group1_perf = get_group_performance(1)
group1_spec = get_specialization_profile(1)

# Key metrics:
# - Total recommendations made
# - Average confidence score
# - Recommendation acceptance rate (by Group 2)
# - Recommendation effectiveness (from Group 4 feedback)
# - Top specializations (refactoring, security, performance)
```

**For Group 2 (Decision Making & Planning)**:
```python
group2_perf = get_group_performance(2)
group2_spec = get_specialization_profile(2)

# Key metrics:
# - Total decisions made
# - Decision accuracy (plans executed successfully)
# - User preference alignment score
# - Average decision confidence
# - Plan adjustment rate (how often plans need revision)
```

**For Group 3 (Execution & Implementation)**:
```python
group3_perf = get_group_performance(3)
group3_spec = get_specialization_profile(3)

# Key metrics:
# - Total executions completed
# - First-time success rate
# - Average quality improvement (before/after)
# - Auto-fix success rate
# - Average iterations needed
```

**For Group 4 (Validation & Optimization)**:
```python
group4_perf = get_group_performance(4)
group4_spec = get_specialization_profile(4)

# Key metrics:
# - Total validations performed
# - GO/NO-GO decision distribution
# - Average quality score (5-layer validation)
# - Feedback effectiveness (improvements from feedback)
# - Issue detection rate
```

### Step 3: Analyze Inter-Group Communication

```python
# Communication flow analysis
comm_flows = {
    "Group 1 → Group 2": collab_stats.get("group_1_to_2", {}),
    "Group 2 → Group 3": collab_stats.get("group_2_to_3", {}),
    "Group 3 → Group 4": collab_stats.get("group_3_to_4", {}),
    "Group 4 → Group 1": collab_stats.get("group_4_to_1", {}),
    "Group 4 → Group 2": collab_stats.get("group_4_to_2", {}),
    "Group 4 → Group 3": collab_stats.get("group_4_to_3", {})
}

# Calculate:
# - Message success rate per flow
# - Average feedback cycle time
# - Communication bottlenecks
```

### Step 4: Analyze Knowledge Transfer

```python
# Knowledge transfer effectiveness
for group_num in [1, 2, 3, 4]:
    knowledge_for_group = query_knowledge(
        for_group=group_num,
        knowledge_type=None  # All types
    )

    # Metrics:
    # - Total knowledge available to group
    # - Knowledge application success rate
    # - Top knowledge sources (which groups share most effectively)
    # - Knowledge confidence trends
```

### Step 5: Identify Top Performers and Areas for Improvement

```python
# Compare groups
comparison = compare_groups(metric='quality_score')

# Identify:
# - Top performing group
# - Groups needing improvement
# - Emerging specializations
# - Communication improvements needed
```

### Step 6: Generate Comprehensive Report

**Report Structure**:

```markdown
# Four-Tier Group Monitoring Report
Generated: {timestamp}

## Executive Summary
- Overall System Health: {score}/100
- Total Tasks Completed: {total}
- Average Quality Score: {avg_quality}/100
- Communication Success Rate: {comm_success}%
- Knowledge Transfer Effectiveness: {knowledge_eff}%

## Group Performance Overview

### Group 1: Strategic Analysis & Intelligence (The "Brain")
**Performance**: {rating} | **Tasks**: {count} | **Success Rate**: {success}%

**Key Metrics**:
- Recommendations Made: {rec_count}
- Average Confidence: {avg_conf}
- Acceptance Rate: {acceptance}%
- Effectiveness Score: {effectiveness}/100

**Top Specializations**:
1. {spec_1} - {quality}% success rate
2. {spec_2} - {quality}% success rate
3. {spec_3} - {quality}% success rate

**Top Agents**:
- {agent_1}: {performance} ({task_type})
- {agent_2}: {performance} ({task_type})

---

### Group 2: Decision Making & Planning (The "Council")
**Performance**: {rating} | **Decisions**: {count} | **Accuracy**: {accuracy}%

**Key Metrics**:
- Decisions Made: {decision_count}
- Decision Confidence: {avg_conf}
- User Alignment: {alignment}%
- Plan Success Rate: {plan_success}%

**Decision Quality**:
- Excellent (90-100): {excellent_count}
- Good (70-89): {good_count}
- Needs Improvement (<70): {poor_count}

**Top Agents**:
- strategic-planner: {performance}
- preference-coordinator: {performance}

---

### Group 3: Execution & Implementation (The "Hand")
**Performance**: {rating} | **Executions**: {count} | **Success**: {success}%

**Key Metrics**:
- Executions Completed: {exec_count}
- First-Time Success: {first_time}%
- Quality Improvement: +{improvement} points avg
- Auto-Fix Success: {autofix}%

**Top Specializations**:
1. {spec_1} - {quality}% success rate
2. {spec_2} - {quality}% success rate
3. {spec_3} - {quality}% success rate

**Top Agents**:
- {agent_1}: {performance} ({task_type})
- {agent_2}: {performance} ({task_type})
- {agent_3}: {performance} ({task_type})

---

### Group 4: Validation & Optimization (The "Guardian")
**Performance**: {rating} | **Validations**: {count} | **Pass Rate**: {pass_rate}%

**Key Metrics**:
- Validations Performed: {val_count}
- GO Decisions: {go_count} ({go_pct}%)
- NO-GO Decisions: {nogo_count} ({nogo_pct}%)
- Average Quality Score: {avg_quality}/100
- Feedback Effectiveness: {feedback_eff}%

**Five-Layer Validation Breakdown**:
- Functional (30 pts): {func_avg}/30
- Quality (25 pts): {qual_avg}/25
- Performance (20 pts): {perf_avg}/20
- Integration (15 pts): {integ_avg}/15
- UX (10 pts): {ux_avg}/10

**Top Agents**:
- post-execution-validator: {performance}
- performance-optimizer: {performance}
- continuous-improvement: {performance}

---

## Inter-Group Communication

### Communication Flow Analysis

**Group 1 → Group 2 (Analysis → Decision)**:
- Messages Sent: {count}
- Success Rate: {success}%
- Average Response Time: {time}s
- Recommendation Acceptance: {acceptance}%

**Group 2 → Group 3 (Decision → Execution)**:
- Plans Sent: {count}
- Execution Success: {success}%
- Plan Completeness: {completeness}%
- Average Execution Time: {time}s

**Group 3 → Group 4 (Execution → Validation)**:
- Results Sent: {count}
- Validation Pass Rate: {pass_rate}%
- Average Quality Improvement: +{improvement} pts
- Iterations Needed: {iterations} avg

**Group 4 → All Groups (Feedback Loops)**:
- Feedback Messages: {count}
- Feedback Effectiveness: {effectiveness}%
- Average Cycle Time: {time}s
- Learning Applied: {learning_count} instances

### Communication Health
- ✅ Excellent (>95%): {excellent_flows}
- ⚠️  Needs Attention (70-95%): {warning_flows}
- ❌ Critical (<70%): {critical_flows}

---

## Knowledge Transfer

### Cross-Group Learning

**Total Knowledge Base**: {total_knowledge} items
**Average Confidence**: {avg_confidence}
**Application Success Rate**: {application_success}%

**Knowledge by Type**:
- Patterns: {pattern_count} (avg confidence: {pattern_conf})
- Best Practices: {bp_count} (avg confidence: {bp_conf})
- Optimizations: {opt_count} (avg confidence: {opt_conf})
- Anti-Patterns: {ap_count} (avg confidence: {ap_conf})

**Top Knowledge Sources** (Groups sharing most effectively):
1. Group {group_num}: {knowledge_count} items, {success}% success rate
2. Group {group_num}: {knowledge_count} items, {success}% success rate
3. Group {group_num}: {knowledge_count} items, {success}% success rate

**Knowledge Transfer Matrix**:
```
           To G1  To G2  To G3  To G4
From G1     --    {n}    {n}    {n}
From G2    {n}     --    {n}    {n}
From G3    {n}    {n}     --    {n}
From G4    {n}    {n}    {n}     --
```

---

## Specialization Insights

### Group Specialization Maturity

**Group 1 (Brain)**: {maturity_level}
- Expertise Areas: {areas}
- Emerging Specializations: {emerging}
- Recommendation: {recommendation}

**Group 2 (Council)**: {maturity_level}
- Expertise Areas: {areas}
- Decision Patterns: {patterns}
- Recommendation: {recommendation}

**Group 3 (Hand)**: {maturity_level}
- Expertise Areas: {areas}
- Execution Strengths: {strengths}
- Recommendation: {recommendation}

**Group 4 (Guardian)**: {maturity_level}
- Expertise Areas: {areas}
- Validation Focus: {focus}
- Recommendation: {recommendation}

---

## Trends & Insights

### Performance Trends (Last 50 Tasks)

**Quality Score Trend**: {trend} ({direction})
- Current Average: {current_avg}/100
- 10-Task Moving Average: {moving_avg}/100
- Trend Direction: {improving/stable/declining}

**Iteration Efficiency**: {trend}
- Current Average: {current_iterations}
- Target: 1.2 or less
- Status: {on_track/needs_attention}

**Decision Accuracy**: {trend}
- Current: {current_accuracy}%
- Target: 90%+
- Status: {excellent/good/needs_improvement}

### Learning Insights

{insight_1}

{insight_2}

{insight_3}

---

## Recommendations

### High Priority
1. {recommendation_1}
2. {recommendation_2}

### Medium Priority
1. {recommendation_1}
2. {recommendation_2}

### Optimization Opportunities
1. {opportunity_1}
2. {opportunity_2}

---

## System Health Score: {score}/100

**Breakdown**:
- Group Performance (40 pts): {group_perf}/40
- Communication Quality (25 pts): {comm_quality}/25
- Knowledge Transfer (20 pts): {knowledge}/20
- Specialization Maturity (15 pts): {specialization}/15

**Status**: {Excellent/Good/Needs Attention/Critical}

---

Report Path: .claude/reports/group-monitoring-{date}.md
```

## Result Presentation

**Terminal Output (15-20 lines max)**:
```
╔══════════════════════════════════════════════════════════════╗
║     FOUR-TIER GROUP MONITORING REPORT                        ║
╚══════════════════════════════════════════════════════════════╝

System Health: {score}/100 ({status})
Total Tasks: {count} | Avg Quality: {quality}/100 | Success Rate: {success}%

GROUP PERFORMANCE:
  Group 1 (Brain):     {rating} │ {tasks} tasks │ {success}% success
  Group 2 (Council):   {rating} │ {decisions} decisions │ {accuracy}% accurate
  Group 3 (Hand):      {rating} │ {executions} executions │ {success}% success
  Group 4 (Guardian):  {rating} │ {validations} validations │ {pass}% pass rate

COMMUNICATION: {comm_success}% success rate │ {feedback_count} feedback loops

TOP PERFORMERS:
  1. {agent_name} ({group}): {performance}
  2. {agent_name} ({group}): {performance}
  3. {agent_name} ({group}): {performance}

TRENDS: Quality {trend_icon} {direction} │ Iterations {trend_icon} {direction}

📄 Detailed Report: .claude/reports/group-monitoring-{date}.md
⏱️  Execution Time: {time}s
```

**File Report**: Save complete detailed report to `.claude/reports/group-monitoring-YYYY-MM-DD.md`

## Notes

- Automatically refreshes data from all learning systems
- Identifies bottlenecks and improvement opportunities
- Tracks specialization emergence over time
- Monitors communication effectiveness
- **Run regularly** (e.g., after every 10-20 tasks) to track trends
- Use insights to optimize group coordination

## Integration

This command integrates with:
- `lib/group_collaboration_system.py` - Communication tracking
- `lib/group_performance_tracker.py` - Performance metrics
- `lib/inter_group_knowledge_transfer.py` - Knowledge stats
- `lib/group_specialization_learner.py` - Specialization insights
- `lib/agent_performance_tracker.py` - Individual agent data
- `lib/agent_feedback_system.py` - Feedback effectiveness
