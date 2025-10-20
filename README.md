# Autonomous Claude Agent Plugin

A comprehensive Claude Code plugin that implements true autonomous agent behavior with pattern learning, skill auto-selection, background task execution, and quality control.

## Features

### Autonomous Decision Making
- **Self-Directed Workflow**: Agent makes decisions independently without constant human approval
- **Smart Delegation**: Automatically delegates to specialized agents based on task type
- **Continuous Learning**: Learns from each task and improves over time

### Pattern Learning (Project Level)
- **Auto-Pattern Detection**: Recognizes successful approaches and stores them
- **Skill Effectiveness Tracking**: Maintains metrics on which skills work best
- **Context-Aware Selection**: Auto-loads relevant skills based on project context and history

### Skill Auto-Selection
- **Task Analysis**: Automatically categorizes tasks and determines required expertise
- **Historical Matching**: Finds similar past tasks and reuses successful approaches
- **Dynamic Loading**: Loads only relevant skills using progressive disclosure

### Background Tasks
- **Parallel Execution**: Runs analysis, optimization, and monitoring in background
- **Non-Blocking**: Main workflow continues while background tasks execute
- **Smart Integration**: Merges background findings into main workflow results

### Quality Control (All Options)
- **Automated Testing**: Runs tests, analyzes coverage, generates missing tests
- **Standards Validation**: Checks linting, formatting, naming conventions
- **Documentation Verification**: Ensures complete documentation coverage
- **Pattern Adherence**: Validates code follows established patterns
- **Auto-Correction**: Fixes issues automatically when quality score < 70/100

## Architecture

### Agents

1. **orchestrator** - Main autonomous controller
   - Analyzes tasks and makes strategic decisions
   - Auto-selects skills and delegates to specialized agents
   - Manages quality assessment and pattern learning
   - Operates completely autonomously

2. **code-analyzer** - Code structure analysis
   - Analyzes code complexity and structure
   - Detects refactoring opportunities
   - Identifies code patterns and anti-patterns

3. **quality-controller** - Quality assurance
   - Runs automated tests
   - Validates coding standards
   - Checks documentation completeness
   - Auto-fixes issues below quality threshold

4. **background-task-manager** - Background execution
   - Manages parallel background tasks
   - Runs continuous monitoring and analysis
   - Handles long-running operations

5. **test-engineer** - Test development
   - Generates missing test cases
   - Fixes failing tests
   - Maintains high test coverage

6. **documentation-generator** - Documentation maintenance
   - Generates missing docstrings
   - Creates and updates API documentation
   - Maintains README and guides

### Skills

1. **pattern-learning** - Pattern recognition and storage system
2. **code-analysis** - Code analysis methodologies and metrics
3. **quality-standards** - Quality benchmarks and standards
4. **testing-strategies** - Test design and coverage strategies
5. **documentation-best-practices** - Documentation templates and standards

### Slash Commands

- `/auto-analyze` - Run autonomous project analysis
- `/quality-check` - Comprehensive quality control with auto-fixing
- `/learn-patterns` - Initialize pattern learning for new projects

## Installation

### For Claude Code CLI

1. Copy this plugin to your Claude Code plugins directory:
   ```bash
   cp -r autonomous-agent ~/.config/claude/plugins/
   ```

2. The plugin will be automatically detected by Claude Code

3. Agents will auto-activate based on task descriptions

### Project-Level Setup

For project-specific pattern learning:

1. Run the initialization command in your project:
   ```
   /learn-patterns
   ```

2. This creates `.claude/patterns/` directory with:
   - `learned-patterns.json` - Pattern database
   - `skill-effectiveness.json` - Skill performance metrics
   - `task-history.json` - Complete task execution log

## Usage

### Autonomous Operation

Simply provide tasks naturally - the orchestrator handles everything:

```
You: "Refactor the authentication module"

Orchestrator (autonomously):
1. Analyzes task → Type: refactoring, Context: auth (security-critical)
2. Auto-loads skills → code-analysis, quality-standards, pattern-learning
3. Checks patterns → Found similar task from 2 weeks ago (95% success)
4. Delegates → code-analyzer for structure analysis
5. Launches background → security scan in parallel
6. Executes refactoring
7. Auto quality check → Score: 96/100 ✓
8. Stores pattern → For future similar tasks
9. Returns results with quality report
```

### Slash Commands

**Analyze Project**:
```
/auto-analyze
```
Runs comprehensive autonomous analysis with background tasks.

**Quality Check**:
```
/quality-check
```
Validates all quality dimensions and auto-fixes issues.

**Initialize Pattern Learning**:
```
/learn-patterns
```
Sets up pattern database for new projects.

## Autonomous Behavior Examples

### Example 1: Task with Auto-Selection

```
You: "Add unit tests for payment processing"

Orchestrator:
- Detects: Task type = testing, Context = payment (critical)
- Auto-loads: testing-strategies, quality-standards
- Queries patterns: Found 3 similar testing tasks
- Auto-selects approach: Use test-engineer agent
- Delegates: test-engineer with testing-strategies skill
- Background: Runs coverage analysis in parallel
- Result: Tests created, coverage 78% → 94%
- Stores: New testing pattern for payment modules
```

### Example 2: Quality Auto-Correction

```
You: "Review the changes I made"

Orchestrator:
- Auto-delegates: quality-controller
- Quality check runs:
  * Tests: 45/50 passing (90%)
  * Standards: 23 violations
  * Docs: 60% coverage
  * Initial score: 68/100 ❌

- Auto-corrections:
  * Fixes 5 failing tests
  * Runs formatter (fixes 15 violations)
  * Generates 10 missing docstrings
  * Re-runs checks
  * Final score: 84/100 ✓

- Stores pattern: Quality improvement approach
```

### Example 3: Background Tasks

```
You: "Refactor the API layer"

Orchestrator:
- Main task: Delegates to code-analyzer
- Background (parallel):
  * Security scan
  * Dependency analysis
  * Documentation update
- Integration:
  * Security: 1 medium issue found → included in refactoring
  * Deps: All up to date
  * Docs: Auto-updated API documentation
- Result: Refactored code + security fix + updated docs
```

## Pattern Learning System

### How It Works

1. **Every Task is Analyzed**:
   - Task type, context, complexity
   - Skills loaded, agents used
   - Execution approach and duration

2. **Success Metrics Captured**:
   - Quality score (0-100)
   - Test results, coverage
   - Standards compliance
   - Outcome (success/failure)

3. **Patterns Stored**:
   - Stored in `.claude/patterns/learned-patterns.json`
   - Includes lessons learned
   - Tracks reuse count

4. **Future Tasks Benefit**:
   - Similar tasks query pattern database
   - Successful approaches reused
   - Skill selection improves over time

### Pattern Database Structure

```json
{
  "patterns": [
    {
      "task_type": "refactoring",
      "context": { "language": "python", "module": "auth" },
      "skills_used": ["code-analysis", "quality-standards"],
      "quality_score": 96,
      "success": true,
      "reuse_count": 5
    }
  ],
  "skill_effectiveness": {
    "code-analysis": {
      "success_rate": 0.93,
      "recommended_for": ["refactoring", "optimization"]
    }
  }
}
```

## Quality Score System

Quality Score = 0-100 based on:
- **Tests** (30 points): Pass rate and coverage
- **Standards** (25 points): Linting and formatting compliance
- **Documentation** (20 points): Docstring coverage
- **Patterns** (15 points): Adherence to established patterns
- **Code Metrics** (10 points): Complexity and duplication

**Threshold**: 70/100 (tasks below this are auto-corrected)

## Configuration

### Agent Customization

Edit agent files in `agents/` to customize behavior:
- Modify system prompts
- Adjust tool access
- Change delegation strategies

### Skill Customization

Edit skill files in `skills/*/SKILL.md` to customize:
- Standards and thresholds
- Language-specific rules
- Documentation templates

### Quality Thresholds

Edit `agents/quality-controller.md` to adjust:
- Minimum quality score (default: 70/100)
- Component weights
- Auto-fix strategies

## Architecture Diagram

```
User Request
    ↓
Orchestrator (Brain)
    ├─→ Auto-load skills (based on patterns + context)
    ├─→ Analyze task type and complexity
    ├─→ Query pattern database
    └─→ Make autonomous decisions
        ↓
    ┌───┴────────────────────┐
    ↓                        ↓
Main Workflow          Background Tasks
    ↓                        ↓
Specialized Agents     Parallel Analysis
    ├─ code-analyzer        ├─ Security scan
    ├─ quality-controller   ├─ Performance check
    ├─ test-engineer        └─ Doc generation
    └─ doc-generator
        ↓                        ↓
    Results              Background Results
        ↓                        ↓
        └────────┬───────────────┘
                 ↓
        Quality Assessment
                 ↓
         Auto-Correction Loop
         (if score < 70)
                 ↓
        Pattern Storage
                 ↓
        Final Report
```

## Brain-Hand Collaboration

This plugin implements the "Brain-Hand" autonomous model:

- **Brain (Orchestrator)**: Makes strategic decisions, plans approach, assesses quality
- **Hand (Skills)**: Provides specialized knowledge and expertise
- **Specialized Agents**: Execute specific tasks with focused expertise
- **No Human in Loop**: Complete autonomous operation from request to result

## Troubleshooting

### Pattern Database Not Found
Run `/learn-patterns` to initialize the pattern learning system.

### Quality Checks Too Strict
Edit `agents/quality-controller.md` to adjust thresholds and weights.

### Skills Not Auto-Loading
Check `.claude/patterns/learned-patterns.json` exists and contains project context.

## Contributing

This plugin demonstrates autonomous agent architecture. To extend:

1. Add new agents in `agents/` for specialized tasks
2. Create new skills in `skills/` for domain knowledge
3. Add slash commands in `commands/` for workflows
4. Update `plugin.json` to include new components

## License

MIT License - Free to use and modify

## Credits

Created based on the autonomous agent architecture pattern, demonstrating true AI autonomy with pattern learning, skill auto-selection, and quality control.
