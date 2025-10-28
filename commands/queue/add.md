---
name: queue:add
description: Add tasks to the autonomous task queue for sequential execution
category: workflow
usage_frequency: medium
common_for: [batch-operations, sequential-workflows, uninterrupted-development]
examples:
  - "/queue:add --name 'Quality Analysis' --command '/analyze:quality' --priority high"
  - "/queue:add --name 'Security Scan' --command '/analyze:dependencies' --priority medium"
  - "/queue:slash --command '/dev:auto \"fix failing tests\"' --priority critical"
tools: Bash
model: inherit
---

# Queue Add Command

Add tasks to the autonomous task queue for sequential execution without user intervention. This allows you to queue multiple commands that will execute one after another automatically.

## Usage

### Add Custom Task
```bash
/queue:add --name "Task Name" --description "Task description" --command "command to execute" --priority high
```

### Add Slash Command to Queue
```bash
/queue:slash --command "/analyze:project" --priority medium
```

## Parameters

### Required Parameters
- `--name`: Task name/identifier
- `--description`: Detailed task description

### Optional Parameters
- `--command`: Command to execute (for autonomous execution)
- `--priority`: Task priority (critical, high, medium, low) - default: medium
- `--type`: Task type (slash_command, autonomous, background, manual) - default: manual
- `--timeout`: Timeout in seconds - default: 300
- `--retry`: Number of retry attempts on failure - default: 3
- `--dependencies`: Comma-separated list of task IDs this task depends on

## Priority Levels

| Priority | Description | Use Case |
|----------|-------------|----------|
| `critical` | Highest priority, executes first | Critical fixes, security issues |
| `high` | High priority, early execution | Important improvements, bug fixes |
| `medium` | Standard priority | Regular tasks, analysis |
| `low` | Low priority, last execution | Cleanup, documentation, optimizations |

## Task Types

| Type | Description | Auto-Execution |
|------|-------------|----------------|
| `slash_command` | Slash command that can be executed automatically | ✅ Yes |
| `autonomous` | Autonomous development task | ✅ Yes |
| `background` | Background analysis task | ✅ Yes |
| `manual` | Manual task requiring user intervention | ❌ No |

## Examples

### Queue Quality Analysis
```bash
/queue:add --name "Quality Analysis" --description "Run comprehensive quality analysis" --command "/analyze:quality" --priority high
```

### Queue Security Scan
```bash
/queue:add --name "Security Scan" --description "Check for security vulnerabilities" --command "/analyze:dependencies" --priority high
```

### Queue Multiple Tasks
```bash
/queue:slash --command "/analyze:project" --priority high
/queue:slash --command "/analyze:quality" --priority medium
/queue:slash --command "/validate:fullstack" --priority medium
```

### Queue with Dependencies
```bash
# First task
/queue:add --name "Setup Environment" --description "Prepare development environment" --priority critical

# Second task (depends on first)
/queue:add --name "Run Tests" --description "Execute test suite" --command "/dev:auto \"run tests\"" --dependencies "task_20241228_143022_123"
```

## Execution

Once tasks are queued, use `/queue:execute` to start sequential execution:
```bash
/queue:execute --stop-on-error    # Stop if any task fails
/queue:execute --background       # Run in background
```

## Integration with User Preferences

The queue system integrates with user preferences to:
- Use your preferred priority levels
- Respect your timeout settings
- Apply your retry preferences
- Learn from your task execution patterns

## Best Practices

1. **Prioritize Critical Tasks**: Use `critical` priority for urgent fixes
2. **Group Related Tasks**: Queue related commands together
3. **Set Appropriate Timeouts**: Longer tasks need higher timeout values
4. **Use Dependencies**: For tasks that must execute in specific order
5. **Monitor Progress**: Use `/queue:status` to track execution

## Output Format

```
✅ Task added with ID: task_20241228_143022_123
📝 Name: Quality Analysis
🎯 Priority: high
⏱ Timeout: 300 seconds
🔄 Retry count: 3
```

## Error Handling

- **Invalid Priority**: Shows valid priority options
- **Missing Parameters**: Indicates required fields
- **Dependency Errors**: Validates task dependencies
- **Storage Errors**: Handles file system issues gracefully

## See Also

- `/queue:status` - View queue status
- `/queue:execute` - Start sequential execution
- `/queue:list` - List queued tasks
- `/queue:clear` - Clear completed tasks