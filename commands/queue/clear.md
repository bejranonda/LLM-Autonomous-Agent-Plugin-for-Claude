---
name: queue:clear
description: Clean up completed, failed, and cancelled tasks from the queue
category: workflow
usage_frequency: low
common_for: [maintenance, cleanup, queue-management]
examples:
  - "/queue:clear"
  - "/queue:clear --older-than 48"
  - "/queue:clear --status completed --keep-recent"
tools: Write, Bash
model: inherit
---

# Queue Clear Command

Clean up the autonomous task queue by removing completed, failed, and cancelled tasks. Helps maintain queue performance and storage efficiency.

## Usage

```bash
/queue:clear [--older-than HOURS] [--status STATUS] [--keep-recent] [--dry-run]
```

## Parameters

### Optional Parameters
- `--older-than`: Remove tasks older than specified hours (default: 24)
- `--status`: Specific status to clear (completed, failed, cancelled)
- `--keep-recent`: Keep recent tasks regardless of age (default: 10 tasks)
- `--dry-run`: Show what would be removed without actually deleting

## Clearing Behavior

### Default Behavior
- Removes completed tasks older than 24 hours
- Removes failed tasks older than 24 hours
- Removes cancelled tasks older than 24 hours
- Keeps 10 most recent tasks of each status
- Preserves queued, running, and retrying tasks

### Status-Specific Clearing
```bash
# Clear only completed tasks
/queue:clear --status completed

# Clear only failed tasks
/queue:clear --status failed

# Clear only cancelled tasks
/queue:clear --status cancelled
```

### Age-Based Clearing
```bash
# Clear tasks older than 48 hours
/queue:clear --older-than 48

# Clear tasks older than 7 days
/queue:clear --older-than 168
```

## Examples

### Standard Cleanup
```bash
/queue:clear
```

Output:
```
🧹 Queue Cleanup Summary
├─ Scanning: 45 tasks total
├─ Completed tasks to remove: 23
├─ Failed tasks to remove: 8
├─ Cancelled tasks to remove: 4
├─ Recent tasks preserved: 10
├─ Total tasks removed: 35
└─ Remaining tasks: 10

✅ Queue cleanup completed successfully
```

### Extended Cleanup
```bash
/queue:clear --older-than 72
```

Output:
```
🧹 Extended Queue Cleanup
├─ Age threshold: 72 hours (3 days)
├─ Scanning: 127 tasks total
├─ Tasks older than 72h: 98
├─ Recent tasks preserved: 15
├─ Total tasks removed: 98
└─ Remaining tasks: 29

✅ Extended cleanup completed
```

### Status-Specific Cleanup
```bash
/queue:clear --status failed --older-than 12
```

Output:
```
🧹 Failed Tasks Cleanup
├─ Status: failed only
├─ Age threshold: 12 hours
├─ Failed tasks found: 18
├─ Tasks old enough to remove: 12
├─ Recent failed tasks preserved: 6
├─ Total tasks removed: 12
└─ Remaining failed tasks: 6

✅ Failed tasks cleanup completed
```

### Dry Run (Preview)
```bash
/queue:clear --dry-run --older-than 48
```

Output:
```
🔍 Queue Cleanup Preview (Dry Run)
├─ Mode: Preview only (no changes will be made)
├─ Age threshold: 48 hours
├─ Tasks that would be removed:

Completed Tasks (15):
├─ task_20241226_143022_123 | Quality Analysis | 45h ago
├─ task_20241226_143025_456 | Security Scan | 44h ago
├─ [13 more tasks...]

Failed Tasks (5):
├─ task_20241226_143018_789 | Test Execution | 46h ago
├─ [4 more tasks...]

Cancelled Tasks (2):
├─ task_20241226_143030_012 | Documentation | 43h ago
├─ [1 more task...]

├─ Total tasks that would be removed: 22
├─ Tasks that would be preserved: 18
└─ Recent threshold: keep 10 most recent of each status

💡 Run without --dry-run to perform actual cleanup
```

## Cleanup Rules

### Age-Based Rules
- **Default**: Remove tasks older than 24 hours
- **Extended**: Remove tasks older than specified hours
- **Recent Preservation**: Always keep most recent N tasks

### Status Rules
- **Safe to Remove**: completed, failed, cancelled
- **Never Removed**: queued, running, retrying
- **Selective**: Can specify specific status to clear

### Preservation Rules
- **Recent Tasks**: Keep N most recent tasks (configurable)
- **Important Tasks**: Preserve high-priority completed tasks
- **Dependencies**: Don't remove tasks with dependents
- **Learning Data**: Preserve tasks needed for pattern learning

## Safety Features

### Backup Creation
Before cleanup, the system:
- Creates backup of queue data
- Stores backup in `.claude-patterns/backups/`
- Uses timestamp for backup identification
- Retains backups for 7 days

### Validation Checks
- Verifies no running tasks are affected
- Checks task dependencies before removal
- Validates storage integrity after cleanup
- Confirms learning data preservation

### Rollback Capability
If cleanup causes issues:
- Restore from recent backup
- Manual recovery options available
- Data integrity verification
- Minimal disruption to operations

## Performance Impact

### Storage Optimization
- Reduces queue file size
- Improves loading performance
- Frees up disk space
- Optimizes memory usage

### Execution Efficiency
- Faster queue status queries
- Improved task selection speed
- Reduced memory overhead
- Better cache utilization

## Integration with Other Systems

### User Preferences
Respects your cleanup preferences:
- Default age threshold
- Preservation count
- Status preferences
- Backup settings

### Learning System
Protects learning data:
- Preserves task patterns
- Maintains success metrics
- Keeps failure analysis data
- Retains user behavior patterns

### Performance Analytics
Maintains performance data:
- Execution time history
- Success rate trends
- Resource utilization data
- Bottleneck analysis

## Advanced Options

### Custom Preservation Rules
```bash
# Keep high-priority completed tasks longer
/queue:clear --older-than 24 --keep-high-priority

# Preserve tasks with specific tags
/queue:clear --preserve-tags "important,production"

# Custom preservation by task name pattern
/queue:clear --preserve-pattern "security.*"
```

### Selective Cleanup
```bash
# Clear specific task types only
/queue:clear --type slash_command --older-than 12

# Clear tasks by name pattern
/queue:clear --pattern "test.*" --status failed

# Clear tasks with specific metadata
/queue:clear --metadata "environment:dev" --status completed
```

## Monitoring and Analytics

### Cleanup Statistics
Track cleanup effectiveness:
```
📊 Cleanup Analytics (Last 30 Days)
├─ Total cleanups: 12
├─ Average tasks removed: 45
├─ Storage saved: 2.3 MB
├─ Performance improvement: 15%
└─ Last cleanup: 2024-12-28 10:30:00
```

### Impact Assessment
- Queue size reduction percentage
- Loading time improvement
- Memory usage optimization
- Storage space savings

## Error Handling

### Common Errors
- **Permission Denied**: Check file permissions
- **Storage Full**: Free up disk space
- **Backup Failed**: Verify backup directory permissions
- **Integrity Check Failed**: Data corruption detected

### Recovery Procedures
- Restore from last backup
- Manual data reconstruction
- Partial recovery options
- Data validation and repair

## Best Practices

1. **Regular Cleanup**: Run cleanup daily for optimal performance
2. **Dry Run First**: Preview changes with --dry-run
3. **Conservative Settings**: Start with longer age thresholds
4. **Monitor Impact**: Check performance after cleanup
5. **Backup Verification**: Ensure backups are created successfully

## Troubleshooting

### Cleanup Issues
- **Tasks Not Removed**: Check age threshold and status filters
- **Performance Problems**: Verify backup and restore operations
- **Data Loss**: Restore from backup and adjust settings
- **Storage Issues**: Check disk space and permissions

### Optimization Tips
- Adjust age thresholds based on usage patterns
- Monitor queue size growth trends
- Balance cleanup frequency vs. performance
- Consider automation for regular maintenance

## See Also

- `/queue:status` - Check queue before cleanup
- `/queue:list` - Review tasks before cleanup
- `/queue:backup` - Manual backup creation
- `/queue:restore` - Restore from backup
- `/queue:stats` - Analyze queue performance