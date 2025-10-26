# Naming Conventions Guide

## Overview

This document outlines the naming conventions used throughout the Autonomous Agent Plugin for Claude Code.

## Agent Naming Standard (v4.2.0+)

### Current Convention: Simple Names Without Prefixes

All agents use simple, descriptive names **without** the `autonomous-agent:` prefix.

#### Format
```
agent-name
```

#### Examples
- `orchestrator` (not `autonomous-agent:orchestrator`)
- `validation-controller` (not `autonomous-agent:validation-controller`)
- `code-analyzer` (not `autonomous-agent:code-analyzer`)
- `frontend-analyzer` (not `autonomous-agent:frontend-analyzer`)

### Agent Directory Structure
```
agents/
├── orchestrator.md                 # Main autonomous controller
├── validation-controller.md        # Tool validation & error prevention
├── code-analyzer.md               # Code structure analysis
├── quality-controller.md          # Quality assurance with auto-fix
├── test-engineer.md               # Test generation & fixing
├── documentation-generator.md     # Documentation maintenance
├── learning-engine.md             # Automatic learning
├── performance-analytics.md       # Performance insights
├── smart-recommender.md           # Intelligent recommendations
├── background-task-manager.md     # Parallel background tasks
├── security-auditor.md           # Security vulnerability scanning
├── pr-reviewer.md                # Pull request review
├── git-repository-manager.md     # Git operations & releases
├── workspace-organizer.md        # Workspace organization
├── report-management-organizer.md # Report organization
├── gui-validator.md              # GUI validation & debugging
├── claude-plugin-validator.md    # Plugin validation
├── dev-orchestrator.md           # Development orchestration
├── api-contract-validator.md     # API contract validation
├── build-validator.md            # Build configuration validation
└── frontend-analyzer.md          # Frontend analysis & auto-fix
```

## Command Delegation

### Command-to-Agent Mapping

Commands delegate to agents using the simple agent names:

#### Command Frontmatter Format
```yaml
---
name: command-name
description: Command description
delegates-to: agent-name
---
```

#### Examples
```yaml
# commands/validate.md
---
name: validate:all
description: Comprehensive validation audit
delegates-to: validation-controller
---

# commands/dashboard.md
---
name: monitor:dashboard
description: Launch monitoring dashboard
delegates-to: orchestrator
---
```

## Skill Naming

### Skill Directory Structure
```
skills/
├── pattern-learning/SKILL.md
├── code-analysis/SKILL.md
├── quality-standards/SKILL.md
├── testing-strategies/SKILL.md
├── documentation-best-practices/SKILL.md
├── validation-standards/SKILL.md
├── fullstack-validation/SKILL.md
├── autonomous-development/SKILL.md
├── git-automation/SKILL.md
├── performance-scaling/SKILL.md
├── security-patterns/SKILL.md
├── model-detection/SKILL.md
├── ast-analyzer/SKILL.md
└── documentation-generator/SKILL.md
```

### Skill Naming Convention
- **Format**: `skill-name` (kebab-case)
- **File**: `skills/skill-name/SKILL.md`
- **Reference**: Agents reference skills by directory name

## Slash Command Naming

### Command Categories

Commands are organized by category with consistent naming:

#### Development Commands (`/dev:*`)
- `/dev:auto` - Autonomous development workflow
- `/dev:release` - Release management workflow
- `/dev:model-switch` - Model switching capability

#### Analysis Commands (`/analyze:*`)
- `/analyze:project` - Project analysis
- `/analyze:quality` - Quality analysis
- `/analyze:static` - Static code analysis
- `/analyze:dependencies` - Dependency scanning

#### Validation Commands (`/validate:*`)
- `/validate:all` - Comprehensive validation
- `/validate:fullstack` - Full-stack validation
- `/validate:patterns` - Pattern validation
- `/validate:plugin` - Plugin validation

#### Debugging Commands (`/debug:*`)
- `/debug:eval` - Evaluation debugging
- `/debug:gui` - GUI debugging

#### Learning Commands (`/learn:*`)
- `/learn:init` - Initialize pattern learning
- `/learn:analytics` - Learning analytics
- `/learn:performance` - Performance analytics
- `/learn:predict` - Predictive analytics

#### Workspace Commands (`/workspace:*`)
- `/workspace:organize` - Workspace organization
- `/workspace:reports` - Report organization
- `/workspace:improve` - Plugin improvement

#### Monitoring Commands (`/monitor:*`)
- `/monitor:dashboard` - Real-time dashboard
- `/monitor:recommend` - Smart recommendations

## Cross-Reference Guidelines

### Agent References in Documentation
When referring to agents in documentation:
- Use the simple name: `validation-controller`
- Not the prefixed name: `autonomous-agent:validation-controller`

### Skill References in Agents
When agents reference skills:
- Use the skill directory name: `pattern-learning`
- Not the file path: `skills/pattern-learning/SKILL.md`

### Command References in Documentation
When referring to commands:
- Use the full slash command: `/validate:all`
- Not just the name: `validate:all`

## System Compatibility

### Backward Compatibility
The system supports both naming conventions:
- ✅ **Simple names**: `validation-controller`
- ✅ **Prefixed names**: `autonomous-agent:validation-controller` (legacy)

### Agent Discovery
Claude Code automatically discovers agents from the `agents/` directory based on:
1. File location (`agents/*.md`)
2. YAML frontmatter structure
3. `name:` field in frontmatter

### Command Discovery
Commands are automatically discovered from the `commands/` directory based on:
1. File location (`commands/*.md`)
2. YAML frontmatter structure
3. `delegates-to:` field for agent mapping

## Migration History

### v4.2.0 (Current) - Simple Names
- **Change**: Removed `autonomous-agent:` prefix from all agent names
- **Reason**: Simplified naming and better user experience
- **Impact**: 22 agents and 24 commands updated
- **Compatibility**: System supports both old and new naming

### v4.1.x and earlier - Prefixed Names
- **Format**: `autonomous-agent:agent-name`
- **Reason**: Plugin identification and namespace separation
- **Status**: Still supported for backward compatibility

## Best Practices

### When Creating New Agents
1. Use descriptive, simple names
2. Follow kebab-case for multi-word names
3. Avoid the `autonomous-agent:` prefix
4. Ensure unique names within the plugin

### When Creating New Commands
1. Use category prefixes (`/category:name`)
2. Delegate to agents using simple names
3. Follow existing naming patterns
4. Keep names descriptive but concise

### When Creating New Skills
1. Use kebab-case naming
2. Create dedicated directory with `SKILL.md`
3. Reference by directory name in agents
4. Keep skill scope focused and specific

## Validation

### Naming Validation Rules
1. **Agent names**: Must be unique, kebab-case preferred
2. **Command names**: Must follow `category:action` format
3. **Skill names**: Must match directory name
4. **Delegation**: Command `delegates-to` must match agent `name`

### Automated Validation
Use `/validate:plugin` to check:
- ✅ All agents have valid names
- ✅ All commands delegate to existing agents
- ✅ All skills are properly structured
- ✅ No naming conflicts exist
- ✅ Cross-references are valid

---

**Version**: 4.2.0
**Last Updated**: 2025-10-26
**Applies to**: All components in the Autonomous Agent Plugin