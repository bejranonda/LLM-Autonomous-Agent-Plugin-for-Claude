---
name: queue:list
description: List tasks in the autonomous task queue with filtering and sorting options
category: workflow
usage_frequency: high
common_for: [task-management, queue-monitoring, progress-tracking]
examples:
  - "/queue:list"
  - "/queue:list --status queued"
  - "/queue:list --priority high --limit 10"
tools: Read
model: inherit
---

# Queue List Command

Display detailed list of tasks in the autonomous task queue with filtering, sorting, and pagination options.

## Usage

```bash
/queue:list [--status STATUS] [--priority PRIORITY] [--type TYPE] [--limit N] [--format FORMAT]
```

## Parameters

### Optional Parameters
- `--status`: Filter by task status (queued, running, completed, failed, cancelled, retrying)
- `--priority`: Filter by priority (critical, high, medium, low)
- `--type`: Filter by task type (slash_command, autonomous, background, manual)
- `--limit`: Maximum number of tasks to show (default: 20)
- `--format`: Output format (table, json, detailed) - default: table

## Filter Options

### Status Filters
- `queued`: Tasks waiting to be executed
- `running`: Currently executing tasks
- `completed`: Successfully finished tasks
- `failed`: Tasks that failed execution
- `cancelled`: Tasks cancelled by user
- `retrying`: Tasks being retried after failure

### Priority Filters
- `critical`: Urgent tasks (priority level 4)
- `high`: Important tasks (priority level 3)
- `medium`: Standard tasks (priority level 2)
- `low`: Low priority tasks (priority level 1)

### Type Filters
- `slash_command`: Executable slash commands
- `autonomous`: Self-executing development tasks
- `background`: Background analysis processes
- `manual`: Tasks requiring manual intervention

## Examples

### List All Tasks
```bash
/queue:list
```

### List Queued Tasks Only
```bash
/queue:list --status queued
```

### List High Priority Tasks
```bash
/queue:list --priority high
```

### List Failed Tasks
```bash
/queue:list --status failed
```

### List Slash Commands
```bash
/queue:list --type slash_command
```

### Combined Filters
```bash
/queue:list --status queued --priority high --type slash_command --limit 10
```

### JSON Output
```bash
/queue:list --format json
```

### Detailed Format
```bash
/queue:list --format detailed --limit 5
```

## Output Formats

### Table Format (Default)
```
📋 Task Queue List (showing 15 of 23 tasks)

+-----+-----------------------------+------------------+----------+---------+--------------+
| #   | Task ID                    | Name             | Priority | Status  | Type         |
+-----+-----------------------------+------------------+----------+---------+--------------+
| 1   | task_20241228_143022_123   | Quality Analysis | High     | Running | slash_command|
| 2   | task_20241228_143025_456   | Security Scan    | High     | Queued  | slash_command|
| 3   | task_20241228_143028_789   | Documentation    | Medium   | Queued  | manual       |
| 4   | task_20241228_143030_012   | Performance Test | Low      | Queued  | background   |
| 5   | task_20241228_143018_333   | Test Execution   | High     | Failed  | slash_command|
+-----+-----------------------------+------------------+----------+---------+--------------+

📊 Summary: 15 tasks shown | 8 queued | 1 running | 5 completed | 1 failed
```

### JSON Format
```json
{
  "tasks": [
    {
      "task_id": "task_20241228_143022_123",
      "name": "Quality Analysis",
      "description": "Run comprehensive quality analysis",
      "priority": "high",
      "priority_level": 3,
      "status": "running",
      "task_type": "slash_command",
      "command": "/analyze:quality",
      "created_at": "2024-12-28T14:30:22.123Z",
      "started_at": "2024-12-28T14:30:25.456Z",
      "execution_time": 125.5,
      "retry_count": 3,
      "current_retry": 0,
      "timeout": 300
    }
  ],
  "total_count": 15,
  "shown_count": 15,
  "filters": {
    "status": null,
    "priority": null,
    "type": null
  },
  "summary": {
    "queued": 8,
    "running": 1,
    "completed": 5,
    "failed": 1,
    "cancelled": 0,
    "retrying": 0
  }
}
```

### Detailed Format
```
📋 Detailed Task Information (Page 1 of 2)

[1] task_20241228_143022_123 | Quality Analysis
+- Status: Running (65% complete)
+- Priority: High (Level 3)
+- Type: Slash Command
+- Command: /analyze:quality
+- Created: 2024-12-28 14:30:22
+- Started: 2024-12-28 14:30:25
+- Duration: 2m 5s
+- Timeout: 300s
+- Retries: 0/3
+- Dependencies: None
+- Description: Run comprehensive quality analysis

[2] task_20241228_143025_456 | Security Scan
+- Status: Queued
+- Priority: High (Level 3)
+- Type: Slash Command
+- Command: /analyze:dependencies
+- Created: 2024-12-28 14:30:25
+- Queued: 2024-12-28 14:30:25
+- Timeout: 300s
+- Retries: 3/3
+- Dependencies: task_20241228_143022_123
+- Description: Check for security vulnerabilities
```

## Task Information

### Core Fields
- **Task ID**: Unique identifier for the task
- **Name**: Human-readable task name
- **Description**: Detailed task description
- **Status**: Current execution status
- **Priority**: Task priority level
- **Type**: Task execution type

### Execution Fields
- **Command**: Command to execute (for slash commands)
- **Created At**: When task was added to queue
- **Started At**: When task execution began
- **Completed At**: When task finished
- **Execution Time**: Total execution duration
- **Timeout**: Maximum allowed execution time

### Retry Fields
- **Retry Count**: Maximum retry attempts
- **Current Retry**: Current retry attempt
- **Retry Reason**: Reason for last retry

### Dependency Fields
- **Dependencies**: List of task IDs this task depends on
- **Dependents**: Tasks waiting for this task to complete

## Sorting and Ordering

### Default Sort Order
Tasks are sorted by:
1. **Priority** (critical -> high -> medium -> low)
2. **Status** (running -> queued -> retrying -> completed -> failed -> cancelled)
3. **Creation Time** (oldest first)

### Custom Sorting
Future enhancement: Add `--sort` parameter for custom sorting options:
- `--sort priority` - Sort by priority
- `--sort created` - Sort by creation time
- `--sort name` - Sort alphabetically by name
- `--sort status` - Sort by status

## Filtering Examples

### Complex Filtering
```bash
# Show high priority failed tasks
/queue:list --priority high --status failed

# Show queued slash commands
/queue:list --status queued --type slash_command

# Show recent completed tasks
/queue:list --status completed --limit 10

# Show critical and high priority tasks
/queue:list --priority critical --priority high
```

### Common Use Cases
```bash
# What's queued to run next?
/queue:list --status queued --priority critical

# What failed recently?
/queue:list --status failed --limit 5

# What manual tasks need attention?
/queue:list --type manual --status queued

# What background processes are running?
/queue:list --type background --status running
```

## Integration with Other Systems

### User Preferences
Filtering respects your preferences:
- Default limit based on your display preferences
- Priority colors match your color scheme
- Status icons follow your accessibility settings

### Learning System
Learns from your filtering patterns:
- Remembers frequently used filter combinations
- Suggests relevant filters based on context
- Adapts display format to your preferences

### Performance Analytics
Provides insights:
- Execution time trends for similar tasks
- Success rates by task type and priority
- Bottleneck identification
- Resource utilization patterns

## Batch Operations

### Multi-Task Operations
Future enhancement: Support for batch operations:
```bash
# Cancel multiple tasks
/queue:cancel --task-ids task_1,task_2,task_3

# Retry multiple failed tasks
/queue:retry --status failed --priority high

# Change priority of multiple tasks
/queue:update --priority critical --task-ids task_1,task_2
```

### Export Functionality
```bash
# Export to CSV
/queue:list --format csv --export queue_export.csv

# Export to JSON
/queue:list --format json --export queue_data.json
```

## Performance Considerations

### Large Queues
- Pagination for queues with 100+ tasks
- Efficient filtering with indexed searches
- Lazy loading of task details
- Caching of frequently accessed data

### Real-time Updates
- Live updates for running tasks
- Progress indicators for long-running tasks
- Status change notifications
- Auto-refresh for active monitoring

## Troubleshooting

### Common Issues
- **No Tasks Found**: Check filters and queue state
- **Slow Loading**: Use more specific filters or reduce limit
- **Incorrect Status**: Task status may be updating
- **Missing Tasks**: Verify queue storage integrity

### Performance Tips
- Use specific status filters for faster loading
- Limit results for large queues
- Use JSON format for programmatic access
- Cache frequently accessed task lists

## Best Practices

1. **Specific Filters**: Use specific filters to reduce noise
2. **Regular Monitoring**: Check queue status regularly
3. **Failed Task Review**: Review failed tasks promptly
4. **Priority Management**: Keep priorities up to date
5. **Dependency Planning**: Plan task dependencies carefully

## See Also

- `/queue:status` - Queue overview and health
- `/queue:add` - Add new tasks
- `/queue:execute` - Start task execution
- `/queue:retry` - Retry failed tasks
- `/queue:clear` - Clean up completed tasks