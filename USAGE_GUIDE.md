# Autonomous Agent Usage Guide

Complete guide to using the autonomous Claude agent plugin with automatic learning capabilities.

## Table of Contents

1. [First Time Setup](#first-time-setup)
2. [Basic Usage Patterns](#basic-usage-patterns)
3. [Understanding Automatic Learning](#understanding-automatic-learning)
4. [Advanced Workflows](#advanced-workflows)
5. [Monitoring and Optimization](#monitoring-and-optimization)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

---

## First Time Setup

### Installation

**Linux/Mac**:
```bash
# Clone and install
git clone https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude.git
mkdir -p ~/.config/claude/plugins
cp -r LLM-Autonomous-Agent-Plugin-for-Claude ~/.config/claude/plugins/autonomous-agent

# Restart Claude Code
claude
```

**Windows PowerShell**:
```powershell
# Clone and install
git clone https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude.git
$pluginPath = "$env:USERPROFILE\.config\claude\plugins"
New-Item -ItemType Directory -Force -Path $pluginPath
Copy-Item -Recurse -Force "LLM-Autonomous-Agent-Plugin-for-Claude" "$pluginPath\autonomous-agent"

# Restart Claude Code
claude
```

### Initialize Learning for Your Project

**Linux/Mac**:
```bash
cd ~/your-project
claude
```

**Windows**:
```powershell
cd C:\Users\YourName\your-project
claude
```

Then run:
```
/learn-patterns
```

**Expected Output**:
```
✓ Creating .claude/patterns/ directory...
✓ Scanning project structure...
✓ Detected languages: python, javascript
✓ Detected frameworks: flask, react
✓ Initializing pattern database...
✓ Learning system ready!

The agent will now learn from every task you perform.
```

---

## Basic Usage Patterns

### Pattern 1: Let It Learn Naturally

Just use Claude Code normally. Learning happens automatically!

**Example Workflow**:

```
Day 1, Task 1:
You: "Add error handling to the login function"

Agent:
✓ Task type: enhancement
✓ No patterns found (first similar task)
✓ Using default skill selection
✓ Quality: 82/100
✓ [SILENT] Pattern captured

Day 1, Task 2:
You: "Add error handling to the registration function"

Agent:
✓ Task type: enhancement
✓ Found similar pattern (quality: 82)
✓ Auto-applying learned approach
✓ Quality: 87/100 ← Already better!
✓ [SILENT] Pattern updated

Day 2, Task 5:
You: "Add error handling to password reset"

Agent:
✓ Task type: enhancement
✓ Strong pattern found (quality: 89, 4 uses)
✓ Optimal skill combination identified
✓ Quality: 93/100 ← Consistently improving!
```

### Pattern 2: Explicit Quality Checks

Request quality validation at any time:

```
You: "Review the code I just wrote"

# Or use the command
/quality-check
```

**What Happens**:
1. Runs all tests
2. Checks code standards
3. Validates documentation
4. If quality < 70: **Automatically fixes issues**
5. Learns from the quality check for next time

### Pattern 3: Background Analysis

Large codebases benefit from background analysis:

```
You: "Analyze this entire module for refactoring opportunities"

# Or use the command
/auto-analyze
```

**What Happens**:
1. Background tasks run in parallel
2. Code complexity analysis
3. Security scanning
4. Documentation gaps identified
5. **All findings stored as learned patterns**

---

## Understanding Automatic Learning

### What Gets Learned

Every task automatically captures:

**1. Task Context**
```json
{
  "task_type": "refactoring",
  "language": "python",
  "framework": "flask",
  "complexity": "medium"
}
```

**2. Execution Details**
```json
{
  "skills_loaded": ["code-analysis", "quality-standards"],
  "agents_delegated": ["code-analyzer"],
  "approach": "Extract method pattern",
  "duration_seconds": 145
}
```

**3. Outcome Metrics**
```json
{
  "success": true,
  "quality_score": 92,
  "tests_passing": 50,
  "standards_compliance": 98
}
```

**4. Learned Insights**
```json
{
  "what_worked": ["code-analysis identified clear opportunities"],
  "bottlenecks": ["Initial scan took 45s"],
  "lessons": ["Security modules benefit from quality-controller"]
}
```

### How Skills Are Selected

**First Task** (No learning data):
```
User: "Refactor the auth module"
→ Uses default skills based on keywords
→ Loads: code-analysis, quality-standards
→ Quality: 80/100
```

**After 5 Similar Tasks** (Learning active):
```
User: "Refactor the payment module"
→ Queries pattern database
→ Finds: 5 successful refactoring patterns
→ Extracts: Most effective skill combinations
→ Loads: code-analysis, quality-standards, pattern-learning
→ Quality: 91/100 (Better!)
→ Execution: 20% faster
```

### Skill Effectiveness Example

```json
{
  "code-analysis": {
    "total_uses": 87,
    "success_rate": 0.943,
    "recommended_for": ["refactoring", "bug-fix"],
    "not_recommended_for": ["documentation"],
    "avg_quality_contribution": 18.5
  }
}
```

**Auto-Adaptation**:
- If skill has 95%+ success rate for task type → **Always loads**
- If skill has 80-94% success rate → **Loads based on context**
- If skill has 50-79% success rate → **Loads only if pattern suggests**
- If skill has <50% success rate for task type → **Never loads automatically**

---

## Advanced Workflows

### Workflow 1: Progressive Refactoring with Learning

**Scenario**: Refactoring a large codebase module by module

**Day 1**:
```
You: "Refactor user authentication"
✓ Quality: 85/100
✓ Pattern learned: auth refactoring approach
```

**Day 2**:
```
You: "Refactor user authorization"
✓ Found auth pattern (85% quality)
✓ Quality: 90/100
✓ Pattern updated: user security refactoring
```

**Day 3**:
```
You: "Refactor session management"
✓ Strong pattern: user security (87.5% avg, 2 uses)
✓ Quality: 93/100
✓ Also applied: security scanning (learned from patterns)
```

**Result**: Each refactoring is better than the last, and the agent learned to automatically include security scanning for user-related modules.

### Workflow 2: Test-Driven Development with Learning

**Round 1**:
```
You: "Write tests for the payment processor"
✓ No testing patterns yet
✓ Creates 15 tests, 82% coverage
✓ Quality: 79/100
✓ Learns: payment testing structure
```

**Round 2**:
```
You: "Write tests for the order processor"
✓ Found payment test pattern
✓ Creates 20 tests, 89% coverage
✓ Quality: 86/100
✓ Learns: business logic testing patterns
```

**Round 3**:
```
You: "Write tests for the inventory system"
✓ Strong pattern: business logic testing
✓ Creates 25 tests, 94% coverage
✓ Quality: 92/100
✓ Auto-includes: edge case testing (learned improvement)
```

### Workflow 3: Documentation Sprint with Learning

```bash
# Day 1
You: "Document the API endpoints"
Agent: Creates basic documentation
Quality: 75/100
Learning: API documentation structure

# Day 2
You: "Document the database models"
Agent: Applies learned doc structure
Quality: 83/100
Learning: Technical documentation patterns

# Day 3
You: "Document the authentication flow"
Agent: Optimal documentation approach identified
Quality: 91/100
Learning: Documentation now includes examples automatically
```

---

## Monitoring and Optimization

### View Learning Progress

**Check Total Tasks Learned**:

Linux/Mac:
```bash
cat .claude/patterns/learned-patterns.json | jq '.patterns | length'
```

Windows PowerShell:
```powershell
(Get-Content .claude\patterns\learned-patterns.json | ConvertFrom-Json).patterns.Count
```

Windows CMD:
```cmd
type .claude\patterns\learned-patterns.json | find /C "task_id"
```

### Track Quality Improvements

**View Quality Trend**:

Linux/Mac:
```bash
# Get all quality scores
cat .claude/patterns/learned-patterns.json | jq '.patterns[].outcome.quality_score'

# Calculate average
cat .claude/patterns/learned-patterns.json | jq '[.patterns[].outcome.quality_score] | add / length'
```

Windows PowerShell:
```powershell
$patterns = (Get-Content .claude\patterns\learned-patterns.json | ConvertFrom-Json).patterns
$patterns | ForEach-Object { $_.outcome.quality_score }
($patterns | Measure-Object -Average -Property @{E={$_.outcome.quality_score}}).Average
```

### View Top-Performing Skills

Linux/Mac:
```bash
cat .claude/patterns/learned-patterns.json | jq '.skill_effectiveness | to_entries | sort_by(.value.success_rate) | reverse | .[0:5]'
```

Windows PowerShell:
```powershell
$skills = (Get-Content .claude\patterns\learned-patterns.json | ConvertFrom-Json).skill_effectiveness
$skills.PSObject.Properties | Sort-Object {$_.Value.success_rate} -Descending | Select-Object -First 5 | Format-Table
```

### Analyze Patterns by Type

Linux/Mac:
```bash
# Count patterns by type
cat .claude/patterns/learned-patterns.json | jq '.patterns | group_by(.task_type) | map({type: .[0].task_type, count: length})'
```

Windows PowerShell:
```powershell
$patterns = (Get-Content .claude\patterns\learned-patterns.json | ConvertFrom-Json).patterns
$patterns | Group-Object task_type | Select-Object Name, Count
```

### Export Learning Report

**Linux/Mac**:
```bash
cat .claude/patterns/learned-patterns.json | jq '{
  total_tasks: (.patterns | length),
  avg_quality: ([.patterns[].outcome.quality_score] | add / length),
  success_rate: ([.patterns[].outcome.success] | map(if . then 1 else 0 end) | add / length),
  top_skills: (.skill_effectiveness | to_entries | sort_by(.value.success_rate) | reverse | .[0:3] | map(.key))
}' > learning-report.json
```

**Windows PowerShell**:
```powershell
$data = Get-Content .claude\patterns\learned-patterns.json | ConvertFrom-Json
$report = @{
    total_tasks = $data.patterns.Count
    avg_quality = ($data.patterns | Measure-Object -Average -Property {$_.outcome.quality_score}).Average
    top_skills = ($data.skill_effectiveness.PSObject.Properties | Sort-Object {$_.Value.success_rate} -Descending | Select-Object -First 3).Name
}
$report | ConvertTo-Json | Out-File learning-report.json
```

---

## Troubleshooting

### Problem: Learning Not Improving Quality

**Diagnosis**:
```bash
# Check how many tasks have been completed
cat .claude/patterns/learned-patterns.json | jq '.patterns | length'
```

**Solution**:
- Learning requires data (minimum 3-5 similar tasks)
- Do more tasks of the same type
- System will improve from task 3-4 onwards

**Accelerate Learning**:
```
/auto-analyze  # Builds baseline
[Do 5 similar tasks in succession]
[Observe improvement from task 3+]
```

### Problem: Skill Not Being Auto-Selected

**Diagnosis**:
```bash
# Check skill effectiveness
cat .claude/patterns/learned-patterns.json | jq '.skill_effectiveness["skill-name"]'
```

**Solution**:
If success_rate < 0.80, skill is being avoided. Options:

1. **Manual boost** (edit `.claude/patterns/learned-patterns.json`):
```json
{
  "skill_effectiveness": {
    "skill-name": {
      "manual_boost": 1.3,
      "override_recommended_for": ["task-type"]
    }
  }
}
```

2. **Force include** for next few tasks to rebuild confidence

### Problem: Quality Checks Too Strict

**Adjust threshold** in `.claude/patterns/config.json`:
```json
{
  "quality_threshold": 65,  // Lower from default 70
  "auto_fix_enabled": true
}
```

### Problem: Patterns Growing Too Large

**Enable expiration**:
```json
{
  "metadata": {
    "pattern_expiration_days": 60,
    "max_patterns": 500,
    "auto_cleanup": true
  }
}
```

**Manual cleanup** (Linux/Mac):
```bash
# Backup first
cp .claude/patterns/learned-patterns.json .claude/patterns/learned-patterns.backup.json

# Remove old patterns (keep last 100)
cat .claude/patterns/learned-patterns.json | jq '.patterns |= (sort_by(.timestamp) | reverse | .[0:100])' > temp.json
mv temp.json .claude/patterns/learned-patterns.json
```

**Manual cleanup** (Windows PowerShell):
```powershell
# Backup first
Copy-Item .claude\patterns\learned-patterns.json .claude\patterns\learned-patterns.backup.json

# Remove old patterns (keep last 100)
$data = Get-Content .claude\patterns\learned-patterns.json | ConvertFrom-Json
$data.patterns = $data.patterns | Sort-Object timestamp -Descending | Select-Object -First 100
$data | ConvertTo-Json -Depth 10 | Out-File .claude\patterns\learned-patterns.json
```

---

## Best Practices

### 1. Let the System Learn Organically

❌ **Don't**:
- Manually edit patterns frequently
- Force specific skill selections
- Disable learning prematurely

✅ **Do**:
- Let first 5-10 tasks build baseline
- Trust the automatic skill selection from task 5+
- Only intervene if performance clearly degrades

### 2. Commit Patterns to Version Control

**Include** `.claude/patterns/` in your repository:

```bash
# .gitignore
# Don't ignore patterns - they help the team!
# .claude/patterns/

# Optional: Ignore local overrides
.claude/patterns/local-overrides.json
```

**Benefits**:
- Team members benefit from shared learning
- Consistent quality across team
- New team members start with existing knowledge

### 3. Monitor Quality Trends

**Weekly check** (Linux/Mac):
```bash
# Add to cron or run manually
cat .claude/patterns/learned-patterns.json | jq '{
  this_week: ([.patterns[] | select(.timestamp > "2025-10-13")] | length),
  avg_quality_this_week: ([.patterns[] | select(.timestamp > "2025-10-13") | .outcome.quality_score] | add / length)
}'
```

**Weekly check** (Windows - add to Task Scheduler):
```powershell
$data = Get-Content .claude\patterns\learned-patterns.json | ConvertFrom-Json
$weekAgo = (Get-Date).AddDays(-7).ToString("yyyy-MM-dd")
$recent = $data.patterns | Where-Object { $_.timestamp -gt $weekAgo }
@{
    tasks_this_week = $recent.Count
    avg_quality = ($recent | Measure-Object -Average -Property {$_.outcome.quality_score}).Average
}
```

### 4. Specialize Patterns by Project Type

For different project types, initialize separate patterns:

**Backend API Project**:
```
/learn-patterns
# Learns API-specific patterns
```

**Frontend Project**:
```
/learn-patterns
# Learns UI/UX-specific patterns
```

**Mobile Project**:
```
/learn-patterns
# Learns mobile-specific patterns
```

### 5. Use Quality Checks as Gates

**Before Commits**:
```bash
# Add to pre-commit hook
/quality-check
# Only commit if quality >= 70
```

**Before PRs**:
```bash
# Add to CI/CD
claude /quality-check
# Fail build if quality < 70
```

### 6. Share Learning Insights

**Generate team report** (monthly):

Linux/Mac:
```bash
cat .claude/patterns/learned-patterns.json | jq '{
  total_tasks: (.patterns | length),
  quality_trend: {
    month_avg: ([.patterns[] | select(.timestamp > "'$(date -d '30 days ago' -I)'") | .outcome.quality_score] | add / length),
    overall_avg: ([.patterns[].outcome.quality_score] | add / length)
  },
  top_patterns: ([.patterns[] | select(.outcome.quality_score >= 90)] | group_by(.task_type) | map({type: .[0].task_type, count: length}) | sort_by(.count) | reverse | .[0:5]),
  skill_rankings: (.skill_effectiveness | to_entries | sort_by(.value.success_rate) | reverse | .[0:5] | map({skill: .key, success_rate: .value.success_rate}))
}' > team-learning-report.json
```

Windows PowerShell:
```powershell
$data = Get-Content .claude\patterns\learned-patterns.json | ConvertFrom-Json
$monthAgo = (Get-Date).AddDays(-30)
$recent = $data.patterns | Where-Object { [DateTime]$_.timestamp -gt $monthAgo }

$report = @{
    total_tasks = $data.patterns.Count
    monthly_tasks = $recent.Count
    monthly_avg_quality = ($recent | Measure-Object -Average -Property {$_.outcome.quality_score}).Average
    top_skills = ($data.skill_effectiveness.PSObject.Properties | Sort-Object {$_.Value.success_rate} -Descending | Select-Object -First 5).Name
}
$report | ConvertTo-Json | Out-File team-learning-report.json
```

---

## Summary

**Key Takeaways**:

1. ✅ **Just use Claude Code normally** - Learning happens automatically
2. ✅ **First 5 tasks build baseline** - Performance improves from task 5+
3. ✅ **Quality improves over time** - Each similar task gets better
4. ✅ **No configuration needed** - System self-optimizes
5. ✅ **Commit `.claude/patterns/`** - Share learning with team
6. ✅ **Monitor quality trends** - Track continuous improvement
7. ✅ **Trust the automation** - Intervene only when necessary

**Quick Reference**:

```bash
# Initialize (once per project)
/learn-patterns

# Regular usage
[Use Claude Code normally]

# Check quality
/quality-check

# Analyze project
/auto-analyze

# View learning (Linux/Mac)
cat .claude/patterns/learned-patterns.json | jq '.skill_effectiveness'

# View learning (Windows)
type .claude\patterns\learned-patterns.json
```

**Remember**: The agent gets smarter with every task. The more you use it, the better it performs!
