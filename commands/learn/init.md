---
name: learn:init
description: Initialize pattern learning database and analyze project patterns

delegates-to: autonomous-agent:orchestrator

# Learn Patterns Command

## 🚨 CRITICAL: RESPONSE SAFETY REQUIREMENTS

**SYSTEM-WIDE FAILURE PREVENTION**: When generating ANY response content for this command, you MUST ensure:

1. **NEVER generate empty text blocks** - All content blocks must have non-empty text
2. **NEVER use Unicode box characters** (=, |, +, +, etc.) - Use safe ASCII alternatives
3. **ALWAYS provide fallback content** for any section that might be empty
4. **VALIDATE all content blocks** before finalizing response

**SAFE RESPONSE PATTERN**:
- Use ASCII characters instead of Unicode box drawing
- Ensure every content section has meaningful content
- Provide default values for any missing data
- Never return empty strings or whitespace-only content

**FAILURE TO COMPLY**: Will cause `cache_control cannot be set for empty text blocks` errors and break ALL Claude functionality.

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

**IMPORTANT**: When delegating this command to the orchestrator agent, the agent MUST present initialization results showing what was detected, created, and the next steps. Silent completion is not acceptable.

## Usage

```bash
/learn:init
```

## What Gets Created

The command creates the `.claude-patterns/` directory with:

```
.claude-patterns/
|-- patterns.json              # Learned patterns database
|-- task_queue.json           # Task queue for background work
|-- quality_history.json      # Quality metrics history
+-- config.json              # Configuration and settings
```

## Example Output

The orchestrator MUST present results in this SAFE format:

```
============================================================
  PATTERN LEARNING INITIALIZED
============================================================

PROJECT ANALYSIS:
Type: Python project with FastAPI framework
Languages: Python 3.9+
Frameworks: FastAPI, SQLAlchemy, Pydantic
Total Files: 127
Project Structure: Backend API with modular design

PATTERN DATABASE CREATED:
Location: .claude-patterns/
Files Created:
- patterns.json (pattern storage)
- task_queue.json (task management)
- quality_history.json (quality tracking)
- config.json (configuration)
Status: Ready for pattern capture

INITIAL PATTERNS DETECTED:
- RESTful API endpoint pattern (23 instances)
- Database model pattern (15 models)
- Pydantic schema pattern (18 schemas)
- Error handling pattern (consistent across modules)
- Authentication decorator pattern

BASELINE METRICS:
Skill Effectiveness: Baseline established
Quality Baseline: Will update after first task
Coverage Baseline: Will update after first task
Agent Performance: Will track from first delegation

NEXT STEPS:
1. Run /auto-analyze to analyze project quality
2. Run /quality-check to establish quality baseline
3. Start working on tasks - learning begins!
4. Each task improves the system automatically

Skills Loaded: pattern-learning, code-analysis
```

**CRITICAL**: Use only ASCII characters and ensure all sections have content. Never leave empty sections.
Agents Used: code-analyzer, learning-engine
Pattern Database: .claude-patterns/ (initialized)
Initialization Time: 0.8 minutes

============================================================
  Pattern learning is ready. The system will learn
  and improve automatically with every task you perform.
============================================================
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
---
