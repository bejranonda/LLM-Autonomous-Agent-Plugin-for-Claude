---
name: learn-patterns
description: Initialize pattern learning database and analyze project patterns
---

# Learn Patterns Command

Analyze project patterns and build the pattern learning database. This will:

- Scan entire project structure
- Identify successful code patterns
- Detect frameworks and architectural approaches
- Create `.claude-patterns/` directory
- Initialize pattern database with project context
- Store initial skill effectiveness baseline

Use this command when starting with a new project to build the autonomous learning foundation.

## How It Works

1. **Project Scanning**: Analyzes entire project structure
2. **Pattern Detection**: Identifies recurring code patterns
3. **Framework Detection**: Detects frameworks, libraries, and tools
4. **Database Initialization**: Creates pattern storage structure
5. **Context Recording**: Stores project metadata
6. **Baseline Setup**: Establishes initial skill metrics

## Usage

```bash
/learn-patterns
```

## What Gets Created

The command creates the `.claude-patterns/` directory with:

```
.claude-patterns/
├── patterns.json              # Learned patterns database
├── task_queue.json           # Task queue for background work
├── quality_history.json      # Quality metrics history
└── config.json              # Configuration and settings
```

## Example Output

```
Pattern Learning Initialization Started
├── Project Analysis
│   ├── Detected: Python project with FastAPI
│   ├── Languages: Python 3.9+
│   ├── Frameworks: FastAPI, SQLAlchemy, Pydantic
│   └── Files analyzed: 127 files
├── Pattern Database
│   ├── Created .claude-patterns/ directory
│   ├── Initialized patterns.json (empty)
│   ├── Initialized task_queue.json (empty)
│   ├── Initialized quality_history.json (empty)
│   └── Initialized config.json
├── Baseline Metrics
│   ├── Skill effectiveness baseline established
│   ├── Quality baseline: TBD (will update after first task)
│   └── Coverage baseline: TBD
└── Pattern learning ready for autonomous operation
```

## Pattern Database Structure

Each pattern stored includes:

- **task_type**: Type of task (feature, bug fix, refactoring, etc.)
- **context**: Description of task context
- **skills_used**: Which skills were successful
- **approach**: What worked well
- **quality_score**: Final quality achieved
- **completion_time**: How long it took
- **success_rate**: Effectiveness of this pattern

## Next Steps

After initializing pattern learning:

1. Run `/auto-analyze` to analyze the project
2. Run `/quality-check` to assess current state
3. Start working on tasks - each one builds the pattern database
4. The plugin learns and improves with every task

## See Also

- `/auto-analyze` - Autonomous project analysis
- `/quality-check` - Comprehensive quality control
