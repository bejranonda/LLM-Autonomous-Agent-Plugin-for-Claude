---
name: Pattern Learning
description: Enables autonomous pattern recognition, storage, and retrieval at project level with self-learning capabilities for continuous improvement
version: 1.0.0
---

## Overview

This skill provides the framework for autonomous pattern learning and recognition at the project level. It enables Claude agents to:
- Automatically detect and store successful task execution patterns
- Build a knowledge base of project-specific approaches
- Recommend skills and strategies based on historical success
- Continuously improve through self-assessment and adaptation

## Pattern Recognition System

### Automatic Pattern Detection

**Task Categorization**:
Automatically classify tasks into categories:
- `refactoring`: Code restructuring and improvement
- `bug-fix`: Error resolution and debugging
- `feature`: New functionality implementation
- `optimization`: Performance improvements
- `documentation`: Docs creation and updates
- `testing`: Test suite development
- `security`: Security analysis and fixes

**Context Extraction**:
Automatically extract context from:
- Programming languages used (file extensions)
- Frameworks detected (package.json, requirements.txt, etc.)
- Project structure patterns (MVC, microservices, etc.)
- Complexity indicators (file count, LOC, dependencies)

### Pattern Storage Structure

**Directory Setup**:
```
.claude/
└── patterns/
    ├── learned-patterns.json       # Main pattern database
    ├── skill-effectiveness.json    # Skill performance metrics
    └── task-history.json           # Complete task execution log
```

**Pattern Data Model**:
```json
{
  "version": "1.0.0",
  "project_context": {
    "detected_languages": ["python", "javascript"],
    "frameworks": ["flask", "react"],
    "project_type": "web-application"
  },
  "patterns": [
    {
      "id": "pattern-001",
      "timestamp": "2025-10-20T10:30:00Z",
      "task_type": "refactoring",
      "task_description": "Refactor authentication module",
      "context": {
        "language": "python",
        "framework": "flask",
        "module": "authentication",
        "complexity": "medium"
      },
      "execution": {
        "skills_used": ["code-analysis", "quality-standards"],
        "agents_delegated": ["code-analyzer", "quality-controller"],
        "approach": "Extract method refactoring with pattern matching",
        "duration_seconds": 120
      },
      "outcome": {
        "success": true,
        "quality_score": 96,
        "tests_passing": true,
        "standards_compliance": 98,
        "documentation_complete": true
      },
      "lessons_learned": "Security-critical modules benefit from quality-controller validation",
      "reuse_count": 5
    }
  ],
  "skill_effectiveness": {
    "code-analysis": {
      "total_uses": 45,
      "successful_uses": 42,
      "success_rate": 0.93,
      "avg_quality_contribution": 15,
      "recommended_for": ["refactoring", "bug-fix", "optimization"]
    },
    "testing-strategies": {
      "total_uses": 30,
      "successful_uses": 27,
      "success_rate": 0.90,
      "avg_quality_contribution": 20,
      "recommended_for": ["testing", "feature", "bug-fix"]
    }
  },
  "agent_effectiveness": {
    "code-analyzer": {
      "total_delegations": 38,
      "successful_completions": 36,
      "success_rate": 0.95,
      "avg_execution_time": 85
    }
  }
}
```

## Skill Auto-Selection Algorithm

### Decision Process

**Step 1: Analyze Current Task**
```
Input: Task description
Output: Task type, context, complexity

Process:
1. Extract keywords and intent
2. Scan project files for context
3. Classify task type
4. Determine complexity level (low/medium/high)
```

**Step 2: Query Pattern Database**
```
Input: Task type, context
Output: Recommended skills, agents, approach

Process:
1. Load learned-patterns.json
2. Filter patterns by task_type match
3. Filter patterns by context similarity
4. Rank by success_rate * reuse_count
5. Extract top 3 most successful patterns
```

**Step 3: Skill Selection**
```
Input: Top patterns, skill effectiveness data
Output: Ordered list of skills to load

Process:
1. Aggregate skills from top patterns
2. Weight by skill effectiveness scores
3. Filter by task type recommendation
4. Return ordered list (highest effectiveness first)
```

### Selection Examples

**Example 1: Refactoring Task**
```
Task: "Refactor user authentication module"

Analysis:
- Type: refactoring
- Context: authentication (security-critical)
- Language: Python (detected)
- Complexity: medium

Pattern Query Results:
- Pattern-001: refactoring + auth → success_rate: 0.96
- Pattern-015: refactoring + security → success_rate: 0.94
- Pattern-023: refactoring + Python → success_rate: 0.91

Skill Selection:
1. code-analysis (appeared in all 3 patterns, avg effectiveness: 0.93)
2. quality-standards (appeared in 2/3 patterns, avg effectiveness: 0.88)
3. pattern-learning (for continuous improvement)

Auto-Load: code-analysis, quality-standards, pattern-learning
```

**Example 2: Testing Task**
```
Task: "Add unit tests for payment processing"

Analysis:
- Type: testing
- Context: payment (critical business logic)
- Language: JavaScript (detected)
- Complexity: high

Pattern Query Results:
- Pattern-042: testing + payment → success_rate: 0.89
- Pattern-051: testing + JavaScript → success_rate: 0.92

Skill Selection:
1. testing-strategies (effectiveness: 0.90)
2. quality-standards (for test quality)
3. pattern-learning (for continuous improvement)

Auto-Load: testing-strategies, quality-standards, pattern-learning
```

## Pattern Storage Workflow

### Automatic Storage Process

**During Task Execution**:
1. Monitor task progress and decisions
2. Record skills loaded and agents delegated
3. Track execution metrics (time, resources)
4. Capture approach and methodology

**After Task Completion**:
1. Run quality assessment
2. Calculate quality score
3. Determine success/failure
4. Extract lessons learned
5. Store pattern to database
6. Update skill effectiveness metrics
7. Update agent effectiveness metrics

### Storage Implementation

**Auto-Create Pattern Directory**:
```javascript
// Executed automatically by orchestrator
if (!exists('.claude/patterns/')) {
  create_directory('.claude/patterns/')
  create_file('.claude/patterns/learned-patterns.json', initial_structure)
  create_file('.claude/patterns/skill-effectiveness.json', {})
  create_file('.claude/patterns/task-history.json', [])
}
```

**Store New Pattern**:
```javascript
// Executed after each task completion
function store_pattern(task_data, execution_data, outcome_data) {
  const pattern = {
    id: generate_id(),
    timestamp: now(),
    task_type: task_data.type,
    task_description: task_data.description,
    context: extract_context(task_data),
    execution: execution_data,
    outcome: outcome_data,
    lessons_learned: analyze_lessons(execution_data, outcome_data),
    reuse_count: 0
  }

  // Load existing patterns
  const db = load('.claude/patterns/learned-patterns.json')

  // Check for similar patterns
  const similar = find_similar_patterns(db.patterns, pattern)

  if (similar.length > 0 && similarity_score > 0.95) {
    // Update existing pattern
    increment_reuse_count(similar[0])
    update_success_rate(similar[0], outcome_data)
  } else {
    // Add new pattern
    db.patterns.push(pattern)
  }

  // Update skill effectiveness
  update_skill_metrics(db, execution_data.skills_used, outcome_data)

  // Save
  save('.claude/patterns/learned-patterns.json', db)
}
```

## Self-Assessment & Quality Metrics

### Quality Score Calculation

**Formula**:
```
Quality Score (0-100) =
  tests_passing (30 points) +
  standards_compliance (25 points) +
  documentation_complete (20 points) +
  pattern_adherence (15 points) +
  code_quality_metrics (10 points)
```

**Component Breakdown**:

1. **Tests Passing (30 points)**:
   - All tests pass: 30 points
   - 90-99% pass: 25 points
   - 80-89% pass: 20 points
   - <80% pass: 0 points

2. **Standards Compliance (25 points)**:
   - Linting score: up to 15 points
   - Code style adherence: up to 10 points

3. **Documentation Complete (20 points)**:
   - All functions documented: 20 points
   - Partial documentation: 10 points
   - No documentation: 0 points

4. **Pattern Adherence (15 points)**:
   - Follows established patterns: 15 points
   - Partially follows: 8 points
   - Deviates from patterns: 0 points

5. **Code Quality Metrics (10 points)**:
   - Cyclomatic complexity: up to 5 points
   - Code duplication: up to 5 points

### Continuous Improvement

**Learning Cycle**:
```
Execute Task
    ↓
Measure Quality
    ↓
Store Pattern
    ↓
Analyze Trends
    ↓
Adjust Skill Selection
    ↓
[Next Task Benefits from Learning]
```

**Trend Analysis**:
- Track quality scores over time
- Identify improving/declining patterns
- Adjust skill recommendations based on trends
- Deprecate ineffective approaches

## Pattern Retrieval & Recommendation

### Query Interface

**Find Similar Patterns**:
```javascript
function find_similar_tasks(current_task) {
  const db = load('.claude/patterns/learned-patterns.json')

  return db.patterns
    .filter(p => p.task_type === current_task.type)
    .filter(p => context_similarity(p.context, current_task.context) > 0.7)
    .sort((a, b) => b.outcome.quality_score - a.outcome.quality_score)
    .slice(0, 5)
}
```

**Recommend Skills**:
```javascript
function recommend_skills(task_type, context) {
  const db = load('.claude/patterns/learned-patterns.json')

  // Get skills with highest success rate for this task type
  const skills = Object.entries(db.skill_effectiveness)
    .filter(([skill, data]) => data.recommended_for.includes(task_type))
    .sort((a, b) => b[1].success_rate - a[1].success_rate)
    .map(([skill, data]) => skill)

  return skills
}
```

### Usage History Tracking

**Maintain Complete History**:
```json
// .claude/patterns/task-history.json
[
  {
    "timestamp": "2025-10-20T10:00:00Z",
    "task_description": "Refactor auth module",
    "skills_used": ["code-analysis", "quality-standards"],
    "quality_score": 96,
    "success": true
  },
  {
    "timestamp": "2025-10-20T11:30:00Z",
    "task_description": "Add payment tests",
    "skills_used": ["testing-strategies"],
    "quality_score": 89,
    "success": true
  }
]
```

## When to Apply

Use this skill when:
- Starting any new task (for pattern retrieval)
- Completing any task (for pattern storage)
- Analyzing project approach effectiveness
- Optimizing skill selection strategy
- Building project-specific knowledge base
- Enabling autonomous decision-making
- Tracking improvement over time

## Integration with Agents

**Orchestrator Agent**:
- Uses pattern-learning for skill auto-selection
- Stores patterns after each task
- Queries patterns before delegation

**Quality Controller Agent**:
- References quality score calculations
- Uses trend analysis for improvement recommendations

**All Specialized Agents**:
- Reference pattern database for context
- Contribute to pattern storage after execution

## Resources

**Reference Files**:
- REFERENCE.md: Detailed algorithm implementations
- pattern-database-schema.json: Complete data structure
- quality-metrics-guide.md: In-depth quality assessment guide

**Auto-Generated Files** (in project):
- .claude/patterns/learned-patterns.json
- .claude/patterns/skill-effectiveness.json
- .claude/patterns/task-history.json
