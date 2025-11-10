---
name: validate:patterns
description: Validate pattern learning database integrity and generate health reports
delegates-to: autonomous-agent:orchestrator
---

# Command: `/validate:patterns`

Validates the pattern learning system across all commands and agents. Ensures patterns are being stored correctly, consistently formatted, and effectively used for improving performance over time.

## Purpose

- Validate pattern learning is working across all commands
- Check pattern format consistency and completeness
- Analyze learning effectiveness and trends
- Identify commands that aren't storing patterns
- Generate comprehensive learning analytics

## What It Does

### 1. **Command Coverage Validation** (10-20 seconds)
- Scan all commands in `commands/` directory
- Check which commands store patterns vs. utility commands
- Validate pattern storage code presence
- Identify missing pattern integration

### 2. **Agent Learning Validation** (10-15 seconds)
- Verify all agents contribute to pattern learning
- Check learning-engine integration points
- Validate agent effectiveness tracking
- Ensure proper handoff protocols

### 3. **Pattern Storage Analysis** (15-30 seconds)
- Validate `.claude-patterns/patterns.json` format
- Check for required fields and data types
- Analyze pattern quality and completeness
- Detect duplicate or corrupted patterns

### 4. **Learning Effectiveness Metrics** (10-20 seconds)
- Calculate pattern reuse rates
- Analyze success rates by task type
- Track skill effectiveness over time
- Identify improvement trends

### 5. **Cross-Reference Validation** (10-15 seconds)
- Validate skill references in patterns
- Check agent consistency with stored patterns
- Verify tool usage compliance
- Ensure documentation alignment

### 6. **Learning Analytics Report** (20-40 seconds)
- Generate comprehensive learning dashboard
- Create visualizations and charts
- Provide improvement recommendations
- Export data for external analysis

## Usage

```bash
# Basic pattern validation
/validate:patterns

# Include detailed analytics (slower but comprehensive)
/validate:patterns --analytics

# Quick validation skip analytics
/validate:patterns --quick

# Validate specific command or agent
/validate:patterns --filter orchestrator
/validate:patterns --filter release-dev
```

## Output

### Terminal Summary (concise)
```
Pattern Learning Validation Complete ✅
+- Commands Validated: 18/18 (100%)
+- Pattern Storage: Healthy ✅
+- Learning Effectiveness: 94% ✅
+- Issues Found: 0 critical, 2 minor
+- Duration: 1m 45s

📊 Full analytics: .claude/reports/validate-patterns-2025-01-15.md
```

### Detailed Report (file)
- Command-by-command validation results
- Pattern storage format validation
- Learning effectiveness metrics with charts
- Agent performance tracking
- Specific issues and fixes needed
- Trend analysis over time

## Validation Categories

### 1. Commands Pattern Storage

**Analysis Commands** (should store patterns):
- `/analyze:project` ✅
- `/analyze:quality` ✅
- `/validate:fullstack` ✅
- `/dev:pr-review` ✅
- And 12 more...

**Utility Commands** (don't store patterns - expected):
- `/monitor:dashboard` - Display only
- `/workspace:reports` - File management only

### 2. Pattern Format Validation

Required fields checked:
```json
{
  "task_type": "string",
  "context": "object",
  "execution": {
    "skills_used": "array",
    "agents_delegated": "array",
    "approach_taken": "string"
  },
  "outcome": {
    "success": "boolean",
    "quality_score": "number",
    "duration_ms": "number"
  },
  "reuse_count": "number",
  "last_used": "string"
}
```

### 3. Learning Effectiveness Metrics

- **Pattern Reuse Rate**: How often patterns are reused
- **Success Rate by Task Type**: Performance across different tasks
- **Skill Effectiveness**: Which skills perform best
- **Agent Performance**: Agent reliability and speed
- **Improvement Trend**: Learning progress over time

## Integration

The `/validate-patterns` command integrates with:

- **learning-engine agent**: Validates pattern capture and storage
- **pattern-learning skill**: Validates pattern format and structure
- **performance-analytics skill**: Generates learning metrics
- **orchestrator**: Uses validation to improve pattern selection

## Expected Validation Results

### Successful Validation (what you should see)
- 18/18 commands validated
- All analysis commands storing patterns
- Pattern format consistent
- Learning effectiveness > 80%
- No critical issues

### Common Issues and Fixes

1. **Missing Pattern Storage**
   - Issue: Command not storing patterns when it should
   - Fix: Add pattern learning integration

2. **Format Inconsistencies**
   - Issue: Missing required fields in patterns
   - Fix: Update pattern generation code

3. **Low Reuse Rate**
   - Issue: Patterns not being reused effectively
   - Fix: Improve pattern matching algorithm

4. **Storage Location Issues**
   - Issue: Patterns not in `.claude-patterns/`
   - Fix: Update storage path configuration

## Analytics Dashboard

When using `--analytics` flag, generates:

### Learning Metrics
- Total patterns stored: 247
- Average reuse count: 3.2
- Success rate: 89%
- Most reused pattern: "refactor-auth-module" (12 times)

### Skill Performance
```
Top Performing Skills:
1. code-analysis (94% success, 45 uses)
2. quality-standards (91% success, 38 uses)
3. pattern-learning (89% success, 52 uses)
```

### Agent Performance
```
Agent Reliability:
1. orchestrator: 96% success
2. code-analyzer: 94% success
3. quality-controller: 92% success
```

## Usage Examples

### Example 1: Basic Validation
```bash
User: /validate:patterns

System: ✅ Pattern learning system healthy
        Commands storing patterns: 16/16
        Pattern format: Valid
        Learning effectiveness: 91%
```

### Example 2: With Analytics
```bash
User: /validate:patterns --analytics

System: 📊 Generated comprehensive analytics
        Learning trends: Improving (+12% over 30 days)
        Top skill: code-analysis (95% success)
        Recommendation: Increase pattern reuse threshold
```

### Example 3: Filter Validation
```bash
User: /validate:patterns --filter orchestrator

System: ✅ Orchestrator pattern integration validated
        Patterns contributed: 89
        Effectiveness score: 96%
        Integration quality: Excellent
```

## When to Use

Run `/validate:patterns` when:
- After implementing new commands or agents
- Suspecting pattern learning issues
- Regular system health checks
- Before major releases
- Analyzing learning effectiveness

## Automation

The orchestrator can automatically run `/validate:patterns`:
- Every 50 tasks to ensure system health
- When learning effectiveness drops below 75%
- After adding new commands or agents
- During system diagnostics

## Troubleshooting

### Common Validation Failures

1. **Pattern Database Missing**
   ```
   Error: .claude-patterns/patterns.json not found
   Fix: Run /learn:init to initialize
   ```

2. **Permission Issues**
   ```
   Error: Cannot read pattern database
   Fix: Check file permissions in .claude-patterns/
   ```

3. **Corrupted Patterns**
   ```
   Error: Invalid JSON in patterns
   Fix: Manual repair or reset patterns
   ```

## Related Commands

- `/learn:init` - Initialize pattern learning system
- `/analyze:project` - Analyze project and learn patterns
- `/analyze:quality` - Check overall system quality

## See Also

- [Learning-Engine Agent](../agents/learning-engine.md)
- [Pattern-Learning Skill](../skills/pattern-learning/SKILL.md)
- [Analytics Dashboard Guide](../docs/guidelines/ANALYTICS_GUIDE.md)
---
