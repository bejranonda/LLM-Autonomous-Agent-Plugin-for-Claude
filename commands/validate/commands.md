---
name: validate:commands
description: Command validation and discoverability verification with automatic recovery
usage: /autonomous-agent:validate:commands [options]
category: validate
subcategory: system
---

# Command Validation and Discoverability

## Overview

The command validation system ensures all commands exist, are discoverable, and function correctly. It validates command structure, checks discoverability, and provides automatic recovery for missing commands.

This command specifically addresses issues like the missing `/autonomous-agent:monitor:dashboard` command by validating that all expected commands are present and accessible.

## Usage

```bash
/autonomous-agent:validate:commands                                    # Validate all commands
/autonomous-agent:validate:commands --category monitor                 # Validate specific category
/autonomous-agent:validate:commands --missing-only                     # Show only missing commands
/autonomous-agent:validate:commands --discoverability                  # Check discoverability features
/autonomous-agent:validate:commands --recover                          # Auto-recover missing commands
/autonomous-agent:validate:commands --test /autonomous-agent:monitor:dashboard          # Test specific command
```

## Parameters

### --category
Validate commands in a specific category only.

- **Type**: String
- **Valid values**: dev, analyze, validate, debug, learn, workspace, monitor
- **Example**: `/autonomous-agent:validate:commands --category monitor`

### --missing-only
Show only missing commands, skip validation of existing commands.

- **Type**: Flag
- **Default**: False
- **Example**: `/autonomous-agent:validate:commands --missing-only`

### --discoverability
Focus on discoverability validation (examples, descriptions, accessibility).

- **Type**: Flag
- **Default**: False
- **Example**: `/autonomous-agent:validate:commands --discoverability`

### --recover
Automatically attempt to recover missing commands.

- **Type**: Flag
- **Default**: False
- **Example**: `/autonomous-agent:validate:commands --recover`

### --test
Test a specific command for validation.

- **Type**: String (command format: /autonomous-agent:category:name)
- **Example**: `/autonomous-agent:validate:commands --test /autonomous-agent:monitor:dashboard`

## Examples

### Basic Command Validation
```bash
/autonomous-agent:validate:commands
```
Output:
```
🔍 Command System Validation
✅ Overall Score: 96/100
📋 Commands: 23/23 present
🎯 Discoverable: 22/23 commands
📝 Valid Syntax: 23/23 commands
[WARN]️  Issues: 1 discoverability issue
```

### Category-Specific Validation
```bash
/autonomous-agent:validate:commands --category monitor
```
Output:
```
🔍 Monitor Commands Validation
✅ Category: monitor
📋 Expected Commands: 2
✅ Commands Found: recommend, dashboard
🎯 All Discoverable: True
📝 Syntax Valid: True
```

### Missing Commands Only
```bash
/autonomous-agent:validate:commands --missing-only
```
Output:
```
❌ Missing Commands Detected:
  * /autonomous-agent:monitor:dashboard (CRITICAL)
    Reason: File not found
    Impact: Dashboard functionality unavailable
    Recovery: Auto-recover available

  * /autonomous-agent:workspace:archive (WARNING)
    Reason: File not found
    Impact: Workspace archive functionality missing
    Recovery: Template creation available
```

### Auto-Recovery Mode
```bash
/autonomous-agent:validate:commands --recover
```
Output:
```
🔄 Automatic Command Recovery
📋 Missing Commands Found: 2

🔧 Recovery Progress:
  ✅ /autonomous-agent:monitor:dashboard restored from Git (commit: a4996ed)
  ❌ /autonomous-agent:workspace:archive recovery failed (no template available)

📊 Final Validation:
  * Commands Present: 24/25
  * Overall Score: 98/100 (+2 points)
```

### Discoverability Check
```bash
/autonomous-agent:validate:commands --discoverability
```
Output:
```
🔎 Command Discoverability Analysis
✅ Overall Discoverability: 87%
📊 Categories Analysis:
  * dev: 100% discoverable
  * analyze: 100% discoverable
  * validate: 75% discoverable (2 issues)
  * monitor: 50% discoverable (1 issue)

🎯 Common Issues:
  * Missing usage examples: 3 commands
  * Unclear descriptions: 2 commands
  * No parameter docs: 5 commands
```

## Command Categories

### dev (Development Commands)
Critical for plugin development and maintenance.
- **Expected Commands**: auto, release, model-switch, pr-review
- **Critical Level**: Critical
- **Recovery Priority**: Immediate

### analyze (Analysis Commands)
Essential for code analysis and quality assessment.
- **Expected Commands**: project, quality, static, dependencies
- **Critical Level**: Critical
- **Recovery Priority**: Immediate

### validate (Validation Commands)
Core validation functionality for system integrity.
- **Expected Commands**: all, fullstack, plugin, patterns, integrity
- **Critical Level**: Critical
- **Recovery Priority**: Immediate

### debug (Debugging Commands)
Tools for debugging and troubleshooting.
- **Expected Commands**: eval, gui
- **Critical Level**: High
- **Recovery Priority**: High

### learn (Learning Commands)
Learning and analytics functionality.
- **Expected Commands**: init, analytics, performance, predict
- **Critical Level**: Medium
- **Recovery Priority**: Medium

### workspace (Workspace Commands)
Workspace organization and management.
- **Expected Commands**: organize, reports, improve
- **Critical Level**: Medium
- **Recovery Priority**: Medium

### monitor (Monitoring Commands)
System monitoring and recommendations.
- **Expected Commands**: recommend, dashboard
- **Critical Level**: Critical
- **Recovery Priority**: Immediate

## Validation Criteria

### Presence Validation
- **File Existence**: Command file exists in correct location
- **File Accessibility**: File is readable and not corrupted
- **Category Structure**: Commands organized in proper categories

### Syntax Validation
- **YAML Frontmatter**: Valid YAML with required fields
- **Markdown Structure**: Proper markdown formatting
- **Required Sections**: Essential sections present
- **Content Quality**: Adequate content length and structure

### Discoverability Validation
- **Clear Description**: Frontmatter description is clear and descriptive
- **Usage Examples**: Practical examples provided
- **Parameter Documentation**: Parameters documented (when applicable)
- **Accessibility**: Command can be discovered and understood

### Integration Validation
- **File System**: Command discoverable through file system
- **Category Organization**: Proper category placement
- **Naming Conventions**: Consistent naming patterns
- **Cross-references**: References in documentation

## Recovery Process

### Automatic Recovery
When `--recover` is enabled, missing commands are recovered using:

1. **Git History Recovery**
   ```bash
   # Find in Git history
   git log --all --full-history -- commands/monitor/dashboard.md

   # Restore from commit
   git checkout <commit> -- commands/monitor/dashboard.md
   ```

2. **Template Creation**
   - Uses command templates
   - Customizes with category and name
   - Creates basic structure for completion

3. **Pattern-Based Recovery**
   - Uses similar commands as reference
   - Maintains consistency with existing commands
   - Preserves category patterns

### Manual Recovery
For commands that can't be auto-recovered:

1. **Create from Template**
   ```markdown
   ---
   name: monitor:dashboard
   description: Launch system monitoring dashboard
   usage: /autonomous-agent:monitor:dashboard [options]
   category: monitor
   subcategory: system
   ---

   # Monitoring Dashboard

   ## Overview
   Launch the autonomous agent monitoring dashboard...
   ```

2. **Use Similar Command**
   - Copy structure from similar command
   - Modify for specific functionality
   - Ensure consistency with category

## Scoring System

Command validation score calculation:

- **Presence Score** (40 points): All expected commands present
- **Syntax Score** (25 points): Valid YAML and markdown structure
- **Discoverability Score** (25 points): Clear descriptions and examples
- **Integration Score** (10 points): Proper integration and organization

**Score Interpretation:**
- **90-100**: Excellent command system
- **80-89**: Good with minor issues
- **70-79**: Acceptable with some issues
- **60-69**: Needs improvement
- **0-59**: Serious command system issues

## Troubleshooting

### Missing Commands
**Symptoms**: Command validation shows missing commands
**Solutions**:
1. Run auto-recovery: `/autonomous-agent:validate:commands --recover`
2. Check Git history for deleted files
3. Create from template manually
4. Verify file system permissions

### Discoverability Issues
**Symptoms**: Commands exist but not easily discoverable
**Solutions**:
1. Add clear descriptions to frontmatter
2. Include practical usage examples
3. Document parameters clearly
4. Improve command categorization

### Syntax Errors
**Symptoms**: Invalid YAML frontmatter or markdown structure
**Solutions**:
1. Validate YAML syntax with linter
2. Check markdown formatting
3. Ensure required sections present
4. Review content quality guidelines

### File Organization Issues
**Symptoms**: Commands in wrong locations or disorganized
**Solutions**:
1. Use proper category structure
2. Follow naming conventions
3. Organize with consistent patterns
4. Run workspace organization: `/autonomous-agent:workspace:organize`

## Best Practices

### Command Development
1. **Use Templates**: Start from command templates
2. **Follow Structure**: Maintain consistent structure
3. **Include Examples**: Provide practical usage examples
4. **Document Parameters**: Clear parameter documentation
5. **Test Discoverability**: Verify command can be found and understood

### Maintenance
1. **Regular Validation**: Run command validation weekly
2. **Monitor Changes**: Validate after command modifications
3. **Backup Protection**: Ensure commands are backed up
4. **Documentation Sync**: Keep docs aligned with commands

### Organization
1. **Category Consistency**: Commands in appropriate categories
2. **Naming Patterns**: Consistent naming conventions
3. **File Structure**: Proper file organization
4. **Cross-references**: Maintain documentation links

## Integration Points

### Pre-Operation Validation
Automatically validates before:
- Command restructuring or organization
- Plugin updates affecting commands
- Release preparation
- File system operations

### Post-Operation Validation
Automatically validates after:
- Command creation or modification
- Category reorganization
- File system changes
- Version updates

### Continuous Monitoring
- Event-driven validation on file changes
- Periodic integrity checks
- Real-time missing command detection
- Automated recovery triggers

## Advanced Features

### Custom Validation Rules
```bash
# Validate with custom rules
/autonomous-agent:validate:commands --rules custom_rules.json

# Validate specific patterns
/autonomous-agent:validate:commands --pattern "*/monitor/*.md"

# Exclude specific commands
/autonomous-agent:validate:commands --exclude "*/test/*.md"
```

### Batch Operations
```bash
# Validate and fix issues
/autonomous-agent:validate:commands --fix-discoverability --add-examples

# Validate and generate report
/autonomous-agent:validate:commands --generate-report --output validation_report.md
```

## Monitoring and Analytics

Track command system health with:
- **Validation History**: Historical validation results
- **Issue Trends**: Recurring command issues
- **Recovery Success**: Auto-recovery effectiveness
- **Usage Patterns**: Command usage and discoverability

Use `/autonomous-agent:learn:performance` for analytics and `/autonomous-agent:learn:analytics` for comprehensive reporting.

## Related Commands

- `/autonomous-agent:validate:integrity` - Complete system integrity validation
- `/autonomous-agent:validate:all` - Full system validation
- `/autonomous-agent:workspace:organize` - Fix file organization issues
- `/autonomous-agent:learn:analytics` - Command system analytics
- `/autonomous-agent:monitor:recommend` - Get system improvement recommendations

## Configuration

### Validation Settings
```json
{
  "command_validation": {
    "auto_recover": true,
    "critical_threshold": 80,
    "validate_discoverability": true,
    "exclude_patterns": ["*/test/*"],
    "notification_level": "warning"
  }
}
```

### Recovery Preferences
```json
{
  "command_recovery": {
    "strategies": ["git_history", "template_creation", "pattern_based"],
    "create_backup_before_recovery": true,
    "verify_after_recovery": true,
    "notification_on_recovery": true
  }
}
```