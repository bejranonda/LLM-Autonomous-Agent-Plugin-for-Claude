---
name: validate:integrity
description: Comprehensive integrity validation and automatic recovery for missing components
usage: /validate:integrity [options]
category: validate
subcategory: system
---

# Comprehensive Integrity Validation

## Overview

The integrity validation command provides comprehensive analysis of plugin integrity with automatic recovery capabilities. It detects missing components, validates system structure, and can automatically restore lost components using multiple recovery strategies.

This command prevents issues like the missing `/monitor:dashboard` command by maintaining continuous integrity monitoring and providing immediate recovery options.

## Usage

```bash
/validate:integrity --auto-recover           # Validate and auto-recover missing components
/validate:integrity --dry-run               # Validate without making changes
/validate:integrity --critical-only          # Check only critical components
/validate:integrity --detailed              # Show detailed validation results
/validate:integrity --backup-check           # Check backup system integrity
```

## Parameters

### --auto-recover
Automatically attempt to recover any missing components found during validation.

- **Type**: Flag
- **Default**: False
- **Example**: `/validate:integrity --auto-recover`

### --dry-run
Perform validation without executing any recovery operations.

- **Type**: Flag
- **Default**: False
- **Example**: `/validate:integrity --dry-run`

### --critical-only
Only validate critical components (core agents, essential commands, key configs).

- **Type**: Flag
- **Default**: False
- **Example**: `/validate:integrity --critical-only`

### --detailed
Show detailed validation results including all issues and recommendations.

- **Type**: Flag
- **Default**: False
- **Example**: `/validate:integrity --detailed`

### --backup-check
Validate the backup system integrity and check for available backups.

- **Type**: Flag
- **Default**: False
- **Example**: `/validate:integrity --backup-check`

## Examples

### Basic Integrity Check
```bash
/validate:integrity
```
Output:
```
🔍 Plugin Integrity Validation
✅ Overall Integrity: 92/100
📊 Components: 56/58 present
[WARN]️  Issues: 2 non-critical
📦 Backups: 3 recent backups available
💡 Recommendations: 2 improvement suggestions
```

### Auto-Recovery Mode
```bash
/validate:integrity --auto-recover
```
Output:
```
🔄 Automatic Recovery Mode
📋 Missing Components Found:
  * /monitor:dashboard (CRITICAL)
  * /commands/workspace/archive (WARNING)

🔧 Recovery Attempting:
  ✅ /monitor:dashboard restored from backup (backup_20250127_143022)
  ❌ /commands/workspace:archive recovery failed (no template available)

📊 Final Integrity: 98/100 (+6 points)
```

### Critical Components Only
```bash
/validate:integrity --critical-only
```
Output:
```
🔍 Critical Components Validation
✅ All critical components present
📋 Critical Inventory:
  * Commands: 22/22 present
  * Agents: 7/7 present
  * Core Skills: 6/6 present
  * Plugin Config: 1/1 present
```

## Output Format

### Summary Section
- **Overall Integrity**: System integrity score (0-100)
- **Components Present**: Found vs. expected component count
- **Issues**: Number and severity of detected issues
- **Backup Status**: Availability and health of backup system

### Detailed Results (when using --detailed)
- **Component Analysis**: Breakdown by category (commands, agents, skills, configs)
- **Missing Components**: List of missing components with severity levels
- **Integrity Issues**: Detailed description of each issue
- **Recovery Options**: Available recovery strategies for each issue

### Recovery Results (when using --auto-recover)
- **Recovery Session**: Session ID and timestamp
- **Components Recovered**: Successfully recovered components
- **Failed Recoveries**: Components that couldn't be recovered
- **Recovery Strategies**: Strategies used and their success rates

## Integrity Scoring

The integrity score is calculated based on:

- **Component Presence** (40 points): All expected components present
- **Discoverability** (25 points): Components are discoverable and accessible
- **System Structure** (20 points): Proper file organization and structure
- **Backup Coverage** (15 points): Adequate backup protection exists

**Score Interpretation:**
- **90-100**: Excellent integrity, no issues
- **80-89**: Good integrity, minor issues
- **70-79**: Acceptable integrity, some issues present
- **60-69**: Poor integrity, significant issues
- **0-59**: Critical integrity problems

## Recovery Strategies

The validation system uses multiple recovery strategies in order of preference:

1. **Backup Restore** (95% success rate)
   - Restores from recent automated backups
   - Preserves original content and metadata
   - Fastest recovery option

2. **Git Recovery** (85% success rate)
   - Recovers from Git history
   - Useful for recently deleted components
   - Preserves version history

3. **Template Creation** (70% success rate)
   - Creates components from templates
   - Provides basic structure for new components
   - Requires manual customization

4. **Pattern-Based** (60% success rate)
   - Uses similar components as reference
   - Maintains consistency with existing components
   - May need manual adjustments

5. **Manual Guidance** (100% guidance rate)
   - Provides step-by-step manual recovery instructions
   - References similar existing components
   - Includes best practices and examples

## Integration Points

### Pre-Operation Validation
Automatically triggered before:
- `/workspace:improve` - Plugin modifications
- `/dev:release` - Release preparation
- Major command restructuring
- Agent or skill modifications

### Post-Operation Validation
Automatically triggered after:
- File system operations
- Command modifications
- Plugin updates
- Version releases

### Continuous Monitoring
- Periodic integrity checks (configurable interval)
- Event-driven validation after file changes
- Real-time missing component detection

## Best Practices

### Prevention
1. **Run regularly**: Perform weekly integrity checks
2. **Auto-recover**: Enable auto-recovery for critical issues
3. **Backup verification**: Regularly verify backup system health
4. **Monitor trends**: Track integrity score over time

### Response Protocol
1. **Critical issues**: Immediate response with auto-recovery
2. **High issues**: Review and address within 24 hours
3. **Medium issues**: Plan fixes in next maintenance window
4. **Low issues**: Include in regular improvement cycle

### System Health
1. **Maintain 90+ score**: Target excellent integrity
2. **Zero missing critical**: Never accept missing critical components
3. **Regular backups**: Ensure recent backups available
4. **Documentation sync**: Keep documentation aligned with actual structure

## Troubleshooting

### Recovery Failures
When auto-recovery fails:
1. Check backup availability: `/validate:integrity --backup-check`
2. Verify Git repository status: `git status`
3. Review manual guidance provided
4. Consider manual creation using templates

### Validation Errors
Common validation issues:
1. **File permission errors**: Check file system permissions
2. **Locked files**: Close other programs using plugin files
3. **Git conflicts**: Resolve Git conflicts before validation
4. **Corrupted backups**: Verify backup system integrity

### Performance Issues
If validation is slow:
1. Use `--critical-only` for faster checks
2. Reduce scope with specific category validation
3. Check system resources and disk space
4. Verify plugin directory isn't excessively large

## Related Commands

- `/validate:commands` - Command-specific validation
- `/validate:all` - Full system validation
- `/workspace:organize` - File organization fixes
- `/dev:auto "validate integrity"` - Automated integrity management

## Configuration

### Validation Settings
```json
{
  "validation": {
    "auto_recover": true,
    "critical_threshold": 70,
    "backup_check_interval": "daily",
    "notification_level": "warning"
  }
}
```

### Recovery Preferences
```json
{
  "recovery": {
    "preferred_strategies": ["backup_restore", "git_recovery"],
    "max_recovery_attempts": 3,
    "require_confirmation": false,
    "create_backup_before_recovery": true
  }
}
```

## Advanced Usage

### Custom Validation Profiles
```bash
# Create custom validation profile
/validate:integrity --profile production --critical-only

# Validate specific categories
/validate:integrity --categories commands,agents --detailed

# Validate with custom thresholds
/validate:integrity --threshold 85 --strict-mode
```

### Batch Operations
```bash
# Validate and create recovery plan
/validate:integrity --dry-run --save-plan

# Execute recovery from saved plan
/validate:integrity --execute-plan recovery_plan_20250127.json
```

## Monitoring and Analytics

The integrity validation maintains comprehensive analytics:
- **Historical Trends**: Track integrity score over time
- **Issue Patterns**: Identify recurring component loss
- **Recovery Success**: Monitor recovery strategy effectiveness
- **System Health**: Overall plugin health assessment

Use `/learn:performance` to view detailed analytics and `/learn:analytics` for comprehensive reporting.