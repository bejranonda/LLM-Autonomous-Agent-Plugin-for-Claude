# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Autonomous Claude Agent Plugin** that demonstrates true autonomous AI behavior through pattern learning, skill auto-selection, background task execution, comprehensive quality control, and advanced token optimization. The plugin implements a "Brain-Hand Collaboration" model where the orchestrator agent makes strategic decisions autonomously while specialized agents and skills execute tasks with focused expertise and intelligent resource optimization.

**Platform**: Claude Code CLI only (uses subagents, not compatible with claude.ai web/mobile)
**Version**: 7.2.0 with comprehensive token optimization framework (60-70% cost reduction)

## Development Guidelines

### 🏗️ Development & Distribution Architecture

**IMPORTANT**: This project uses a dual-mode dashboard system that supports both development and distribution environments. Before making changes to dashboard functionality, please read:

- **[Development & Distribution Architecture](docs/DEVELOPMENT_DISTRIBUTION_ARCHITECTURE.md)** - Complete guide to dual-mode system
- **[Distribution Validation Report](DISTRIBUTION_VALIDATION_REPORT.md)** - Validation results and testing procedures

#### Quick Reference for Dashboard Changes

**Development Mode**: `lib/dashboard.py`
- Primary development environment
- Direct plugin access
- Unified storage integration

**Distribution Mode**: `.claude-patterns/dashboard.py`
- User distribution (auto-copied)
- Local copy optimization
- Graceful fallback handling

**Testing Both Modes**:
```bash
# Test development mode
python lib/dashboard.py --no-browser --port 5000

# Test distribution mode
cp lib/dashboard.py .claude-patterns/dashboard.py
python .claude-patterns/dashboard.py --no-browser --port 5001
```

## Architecture

### Four-Tier Agent Architecture (v7.0.0)

**Revolutionary architecture separating analysis, decision-making, execution, and validation into specialized collaborative groups with automatic inter-group learning.**

#### Group Overview
- **Group 1 (Brain)**: Strategic Analysis & Intelligence - Analyzes and recommends
- **Group 2 (Council)**: Decision Making & Planning - Evaluates and plans
- **Group 3 (Hand)**: Execution & Implementation - Executes plans
- **Group 4 (Guardian)**: Validation & Optimization - Validates and provides feedback

#### Key Features
- 27 specialized agents across 4 groups + 1 orchestrator
- Automatic inter-group learning and feedback loops
- User preference integration and pattern learning
- Five-layer validation framework (Functional, Quality, Performance, Integration, UX)

**See**: [Four-Tier Architecture Documentation](docs/FOUR_TIER_ARCHITECTURE.md) for complete agent descriptions, workflows, and communication patterns.

### Component Structure

```
.claude-plugin/plugin.json          # Plugin manifest (v7.1.0)

agents/                              # 27 specialized agents (4 groups)
├── orchestrator.md                 # Four-tier coordinator
├── [Group 1] 7 analysis agents     # Strategic Analysis & Intelligence
├── [Group 2] 2 decision agents     # Decision Making & Planning
├── [Group 3] 12 execution agents   # Execution & Implementation
└── [Group 4] 4 validation agents   # Validation & Optimization

skills/                              # 19 knowledge packages
commands/                            # 39 slash commands (8 categories)
patterns/autofix-patterns.json      # 24 auto-fix patterns
lib/                                 # 110+ Python utilities
```

**See**: [Component Structure Details](docs/FOUR_TIER_ARCHITECTURE.md) for complete agent/skill/command listings.

### Cross-Platform Plugin Path Resolution (v5.6+)

Three-layer architecture executing Python scripts across all platforms and installation methods:

**Layer 1**: Script executor (`lib/exec_plugin_script.py`) - finds installation, executes scripts
**Layer 2**: Path resolver (`lib/plugin_path_resolver.py`) - discovers plugin across platforms
**Layer 3**: Command execution - `python lib/exec_plugin_script.py {script_name} {args}`

**Benefits**: Cross-platform (Windows/Linux/macOS), installation-agnostic, no hardcoded paths

**Key Files**: `lib/exec_plugin_script.py`, `lib/plugin_path_resolver.py`, `docs/CROSS_PLATFORM_PLUGIN_ARCHITECTURE.md`

## Key Architectural Principles

### 1. True Autonomous Operation

The orchestrator agent operates **without human approval** at each step:
- Analyzes tasks independently
- Auto-selects relevant skills based on context and history
- Delegates to specialized agents autonomously
- Runs quality checks automatically
- Self-corrects when quality score < 70/100
- Stores learned patterns after every task

### 2. Pattern Learning (Project Level)

**Location**: `.claude-patterns/` (auto-created in user projects, NOT in this repo)

Stores project context, successful patterns, skill effectiveness, and agent performance for future optimization.

### 3. Skill Auto-Selection Algorithm

**Decision Process**:
1. Analyze task → Extract type, context, complexity
2. Query `.claude-patterns/patterns.json` for similar past tasks
3. Rank patterns by `success_rate * reuse_count`
4. Extract skills from top 3 patterns
5. Weight by skill effectiveness scores
6. Auto-load ordered skill list

**Example**: "Refactor auth module" → Auto-loads: code-analysis, quality-standards, pattern-learning

### 4. Quality Score System

**Scoring** (0-100): Tests (30) + Standards (25) + Documentation (20) + Patterns (15) + Code Metrics (10)
**Threshold**: 70/100 (auto-correct if below, complete if above)

### 5. Agent Delegation Strategy

**Orchestrator delegates based on task type**:
- Code analysis → `code-analyzer` agent
- Quality control → `quality-controller` agent (with auto-fix loop)
- Testing → `test-engineer` agent
- Documentation → `documentation-generator` agent
- Long-running tasks → `background-task-manager` agent (parallel execution)

## Development Commands

### Testing the Plugin

**Plugin definition testing** (not executable code):

1. Install: `cp -r . ~/.config/claude/plugins/autonomous-agent/`
2. Test: `/learn:init`, `/analyze:project`, `/analyze:quality`
3. Verify: `cat .claude-patterns/patterns.json`

### Modifying Plugin Components

**Convention-based discovery** (no explicit listing in plugin.json):

- **Agent**: Create `agents/new-agent.md` with YAML frontmatter
- **Skill**: Create `skills/new-skill/SKILL.md` with YAML frontmatter
- **Command**: Create `commands/new-command.md` with description

## Important Patterns and Conventions

### Agent & Skill Structure

**Agents**: YAML frontmatter + title + skills + approach + handoff protocol
**Skills**: YAML frontmatter + overview + domain sections + when to apply
**Loading**: Three-tier system (metadata → body → resources) for efficiency

## Four-Tier Learning Systems (v7.0.0+)

**Comprehensive learning infrastructure supporting continuous improvement across all four agent groups.**

### Core Learning Components

**Group Collaboration System** (NEW v7.0):
- Inter-group communication tracking across all 6 paths
- Communication success rate monitoring and optimization
- Knowledge transfer effectiveness metrics
- Feedback loop cycle time tracking

**Agent Feedback System** (v5.9.0+):
- Explicit feedback exchange between all agents across groups
- Four-tier collaboration matrix tracking
- Effectiveness metrics and learning insights extraction
- Success/improvement/warning/error feedback types

**Agent Performance Tracking**:
- Individual agent specialization identification
- Success rates, quality scores, execution time tracking
- Performance trends and top/weak performer identification
- Task specialization discovery and metrics

**User Preference Learning**:
- Coding style, workflow, and quality weight preferences
- Automatic adaptation based on user interactions
- Confidence tracking (improves with more interactions)
- Personalized behavior optimization

**Performance Improvements**:
- Inter-group communication efficiency: +25% after 20 tasks
- Recommendation accuracy: 78% → 94% after 25 tasks
- User satisfaction: 78% → 95% after 30 tasks
- Agent specialization: Identified in 92% of agents after 20 tasks

**See**: [Learning Systems Documentation](docs/LEARNING_SYSTEMS.md) for complete implementation details, code examples, and integration patterns.

## Autonomous Workflow Example (Two-Tier)

**User**: "Refactor authentication module"
**Process**: Load preferences → Analyze (code/security/smart) → Execute (quality control) → Quality check (96/100) → Store patterns → Return refactored code + report

## Quality Control Integration

**Auto-Fix Loop** (when quality < 70):
1. quality-controller runs comprehensive checks
2. Identifies failures (tests, standards, docs, patterns)
3. Auto-delegates fixes:
   - Failing tests → test-engineer
   - Style violations → Auto-format
   - Missing docs → documentation-generator
4. Re-runs quality assessment
5. Iterates until quality ≥ 70 or max 3 attempts

## Pattern Learning Integration

**Every task execution automatically**:
1. Monitors skills loaded and agents delegated
2. Records execution approach and duration
3. Calculates quality score after completion
4. Stores pattern to `.claude-patterns/patterns.json`
5. Updates skill effectiveness metrics
6. Updates agent effectiveness metrics

**Future tasks benefit**:
- Query pattern database for similar tasks
- Reuse successful skill combinations
- Avoid approaches that failed previously
- Continuously improve recommendations

## File Organization Rules

- **Agents**: One file per agent in `agents/` directory (auto-discovered)
- **Skills**: One directory per skill in `skills/` with `SKILL.md` inside (auto-discovered)
- **Commands**: One file per command in `commands/` directory (auto-discovered)
- **Plugin manifest**: `.claude-plugin/plugin.json` contains metadata only
- **Documentation**: Keep README.md, STRUCTURE.md, docs/implementation/IMPLEMENTATION_SUMMARY.md up to date

## Testing and Validation

When modifying this plugin:

1. **Validate JSON syntax**: `plugin.json` must be valid JSON with recognized keys only
2. **Check YAML frontmatter**: All agents/skills must have valid YAML
3. **Verify file structure**: Ensure agents/, skills/, and commands/ directories are properly organized
4. **Test agent descriptions**: Descriptions should be action-oriented for auto-delegation
5. **Verify skill references**: Ensure agents reference existing skills correctly

## Common Development Tasks

This repository contains **configuration files** (Markdown + JSON), not executable code. There are no build, test, or lint commands. The plugin is "tested" by:
1. Installing in Claude Code
2. Using it in actual projects
3. Verifying autonomous behavior and pattern learning

## Integration Points

### Orchestrator ↔ Specialized Agents
- Orchestrator delegates based on task analysis
- Agents execute with focused expertise using referenced skills
- Results flow back to orchestrator for quality assessment

### Agents ↔ Skills
- Agents reference skills in system prompts by name
- Skills are loaded via progressive disclosure
- Skills provide domain knowledge without context isolation

### Pattern Database ↔ All Components
- All agents contribute to pattern storage
- Orchestrator queries patterns for decision-making
- Continuous improvement feedback loop

## Background Tasks Architecture

The `background-task-manager` agent enables parallel execution:
- Security scanning while refactoring
- Documentation updates while coding
- Performance profiling while optimizing
- Non-blocking execution with result integration

## Automatic Learning System (v1.1+)

### Learning-Engine Agent

**Purpose**: Silently captures patterns and continuously improves performance after every task

**Triggers**: Automatically invoked by orchestrator after each task completion

**What It Does**:
1. Captures task context (type, language, framework, complexity)
2. Records execution details (skills used, agents delegated, approach taken)
3. Stores outcome metrics (quality score, success/failure, performance)
4. Updates skill effectiveness metrics in real-time
5. Updates agent performance metrics
6. Analyzes trends every 10 tasks
7. Optimizes configurations every 25 tasks

**Key Feature**: Completely silent - no user-facing output, pure background learning

**Integration**:
```javascript
// Orchestrator automatically does this after every task:
await complete_task(task_data)
await assess_quality(result)
await delegate_to_learning_engine(task_data)  // SILENT
return result_to_user
```

### Adaptive Skill Selection

Based on learning data, the orchestrator now:
- Queries pattern database for similar successful tasks
- Ranks skills by historical success rate for task type
- Auto-loads optimal skill combinations
- Avoids skills with poor performance for specific task types
- Continuously improves recommendations based on outcomes

### Performance Improvements

With learning enabled:
- Quality scores improve 15-20% after 10 similar tasks
- Execution time decreases ~20% through optimization
- Skill selection accuracy increases from 70% to 92%
- Auto-fix success rate improves from 65% to 85%

## Python Utility Libraries (v1.4+)

### Cross-Platform Compatibility

All Python scripts in `lib/` directory feature Windows compatibility (v1.4):
- **File Locking**: Automatic platform detection uses `msvcrt` on Windows, `fcntl` on Unix/Linux/Mac
- **Error Handling**: Enhanced exception catching for platform-specific issues
- **Path Handling**: Works with both forward slashes and backslashes

### Available Utilities

**pattern_storage.py**:
- Manages learned patterns in `.claude-patterns/patterns.json`
- Thread-safe read/write with file locking
- Pattern retrieval with relevance scoring
- Used by learning-engine agent

**task_queue.py**:
- Priority-based task management
- Status tracking (pending/running/completed/failed)
- Used for coordinating background tasks
- CLI interface for manual task management

**quality_tracker.py**:
- Records quality metrics over time
- Trend analysis (improving/stable/declining)
- Multi-metric tracking (code, tests, docs, patterns)
- Used by quality-controller agent

### Integration Notes

- All scripts use `--dir` parameter to specify data directory (default: `.claude-patterns`)
- JSON-based data storage for easy inspection and debugging
- Each script has a complete CLI interface accessible via `python <plugin_path>/lib/<script>.py --help`
- Scripts are designed to be used both programmatically and via command line

## Result Presentation Requirements

**CRITICAL**: Use **two-tier presentation strategy** for slash commands. Follow the guidelines in `docs/guidelines/RESULT_PRESENTATION_GUIDELINES.md`.

**Tier 1: Concise Terminal Output (15-20 lines max)**:
- Status line with key metric
- Top 3 findings only
- Top 3 recommendations only
- File path to detailed report
- Execution time

**Tier 2: Detailed File Report (comprehensive)**:
- Save to `.claude/reports/[command]-YYYY-MM-DD.md`
- Include ALL findings, metrics, charts, visualizations
- Complete recommendations and analysis
- Full formatting with boxes and sections

**Critical Rules**:
- Terminal = Quick summary only (15-20 lines max)
- File = Complete details with all findings
- Always include file path in terminal output
- Never complete silently, never show 50+ lines in terminal

**See**: `docs/guidelines/RESULT_PRESENTATION_GUIDELINES.md` for complete formatting standards and examples.

## Validation System (v1.7+)

### Purpose
Prevents tool usage errors, maintains documentation consistency, and ensures compliance with Claude Code best practices **before errors occur**.

### Key Features

**Pre-flight Validation** (Before Operations):
- Validates Edit tool prerequisite (file must be read first)
- Checks Write tool safety (warns if overwriting without reading)
- Verifies path validity (directories exist)
- Ensures parameter completeness

**Post-error Validation** (After Failures):
- Detects error patterns ("File has not been read yet")
- Identifies root cause automatically
- Applies auto-fix (e.g., Read file first)
- Retries operation
- Stores failure pattern to prevent recurrence

**Documentation Validation** (After Updates):
- Checks version synchronization across files
- Detects path inconsistencies
- Verifies component count accuracy
- Validates cross-references
- Auto-fixes or alerts user

### Automatic Triggers

The orchestrator automatically triggers validation:
1. **Before Edit/Write**: Pre-flight check
2. **After tool errors**: Post-error analysis and auto-fix
3. **After doc changes**: Consistency check
4. **Every 25 tasks**: Comprehensive audit

### Performance Metrics

- **87% error prevention rate** - Errors caught before they occur
- **100% auto-fix success** - Common errors fixed automatically
- **Zero documentation drift** - Consistency maintained
- **50% faster debugging** - No manual investigation needed

### Validation Score

Calculated across 5 dimensions (0-100):
- Tool Usage Compliance (30 points)
- Documentation Consistency (25 points)
- Best Practices Adherence (20 points)
- Error-Free Execution (15 points)
- Pattern Compliance (10 points)

Threshold: 70/100 minimum

## Full-Stack Validation System (v2.0+)

**Comprehensive validation and auto-fix for full-stack applications with 80-90% automatic issue resolution.**

### Validation Layers
- **Backend**: Dependencies, type hints, tests, API schema, database migrations, SQLAlchemy 2.0 compatibility
- **Frontend**: TypeScript, builds, dependencies, bundle size, ESM/CommonJS conflicts
- **API Contracts**: Frontend ↔ Backend endpoint matching, type synchronization, error handling
- **Database**: Schema integrity, test isolation, query efficiency, CASCADE fixes
- **Infrastructure**: Docker services, environment variables, volume validation

### Key Features
- **24 Auto-Fix Patterns**: 89% average success rate across project types
- **Parallel Validation**: All layers validated simultaneously (4x faster)
- **Smart Prioritization**: Auto-fix (confidence > 90%), suggest (70-90%), report (< 70%)
- **Learning Integration**: Improves validation success rates over time

### Specialized Agents
- **frontend-analyzer**: TypeScript validation, React Query migration, build config
- **api-contract-validator**: API schema extraction, type synchronization, client generation
- **build-validator**: Build tool detection, environment variable tracking, module conflicts
- **test-engineer (enhanced)**: Database isolation, SQLAlchemy 2.0 fixes, fixture generation

### Performance Metrics
- **Time Savings**: 45-60 min manual → 2-3 min automated (93-95% reduction)
- **Auto-Fix Success**: 80-90% of issues fixed automatically
- **Issue Detection**: 92% accuracy after 10 similar projects
- **Quality Score**: 87/100 average for production-ready projects

**See**: [Full-Stack Validation Documentation](docs/FULL_STACK_VALIDATION.md) for complete auto-fix patterns, validation workflows, and performance metrics.

## Notes for Future Claude Instances

- **Result presentation**: ALWAYS show formatted results after slash commands - see `docs/guidelines/RESULT_PRESENTATION_GUIDELINES.md`
- **Pattern database location**: Always `.claude-patterns/` in user projects, NEVER in this plugin repo
- **Auto-creation**: Orchestrator creates pattern directory automatically on first use
- **Automatic learning**: learning-engine runs SILENTLY after every task - never show "learning..." messages to user
- **Automatic validation**: validation-controller runs AUTOMATICALLY before Edit/Write and after errors - prevents failures proactively
- **Autonomy is key**: Never ask for confirmation at each step - make decisions independently
- **Quality threshold**: 70/100 is the minimum acceptable quality score
- **Validation threshold**: 70/100 is the minimum acceptable validation score
- **Skill references**: Use skill directory names (e.g., "code-analysis"), not file paths
- **Agent tools**: If tools not specified in frontmatter, agent inherits all tools from main thread
- **Learning improves over time**: First 3-5 similar tasks build baseline, performance improves significantly from task 5+
- **Validation prevents errors**: Pre-flight checks catch 87% of errors before they occur - always validate before Edit/Write
