---
name: auto-analyze
description: Autonomously analyze the project with automatic skill selection and pattern learning
---

# Auto-Analyze Command

Analyze the current project autonomously using the orchestrator agent. This will:

- Auto-detect project type and technologies
- Load relevant skills based on project context
- Run code analysis in background
- Generate comprehensive quality report
- Store learned patterns for future use

The orchestrator will make all decisions autonomously without requiring confirmation at each step.

## How It Works

1. **Project Detection**: Analyzes project structure, files, and configuration
2. **Context Analysis**: Determines project type, languages, and frameworks
3. **Skill Loading**: Auto-selects relevant skills based on context
4. **Analysis Execution**: Runs comprehensive code analysis
5. **Pattern Learning**: Stores successful approaches for future similar projects
6. **Report Generation**: Creates detailed analysis report

## Usage

```bash
/auto-analyze
```

## Example Output

```
Autonomous Project Analysis Started
├── Detected: Python project with FastAPI framework
├── Loading skills: code-analysis, quality-standards, pattern-learning
├── Running analysis...
├── Tests found: 45 tests, 92% passing
├── Code quality: 88/100
├── Pattern learned and stored
└── Analysis complete in 2.3 minutes
```

## See Also

- `/quality-check` - Comprehensive quality control with auto-fix
- `/learn-patterns` - Initialize pattern learning database
