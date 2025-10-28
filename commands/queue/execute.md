---
name: queue:execute
description: Execute queued tasks sequentially without user intervention
category: workflow
usage_frequency: medium
common_for: [batch-operations, sequential-workflows, uninterrupted-development]
examples:
  - "/queue:execute --stop-on-error"
  - "/queue:execute --background"
  - "/queue:execute"
tools: Bash
model: inherit
---

# Queue Execute Command

Execute all queued tasks sequentially without requiring user intervention between tasks. Tasks are executed in priority order (critical → high → medium → low) and can run in the background.

## Usage

```bash
/queue:execute [--stop-on-error] [--background]
```

## Parameters

### Optional Parameters
- `--stop-on-error`: Stop execution on first task failure (default: continue)
- `--background`: Run execution in background process

## Execution Behavior

### Priority-Based Execution
Tasks are executed in this order:
1. **Critical** tasks (urgent fixes, security issues)
2. **High** priority tasks (important improvements)
3. **Medium** priority tasks (standard operations)
4. **Low** priority tasks (cleanup, optimization)

### Task Dependencies
Tasks with dependencies wait until all dependencies are completed before execution.

### Error Handling
- **Default Mode**: Continue with next task even if current task fails
- **Stop-on-Error Mode**: Halt execution on first task failure

### Retry Logic
Failed tasks are automatically retried up to their configured retry limit before being marked as failed.

## Examples

### Execute with Error Continuation
```bash
/queue:execute
```
Continues execution even if some tasks fail.

### Execute with Stop on Error
```bash
/queue:execute --stop-on-error
```
Stops execution at first failure.

### Background Execution
```bash
/queue:execute --background
```
Starts execution in background process.

### Combined Options
```bash
/queue:execute --stop-on-error --background
```
Background execution with stop-on-error behavior.

## Execution Process

1. **Task Selection**: Selects highest priority pending task with satisfied dependencies
2. **Status Update**: Updates task status to "running"
3. **Command Execution**: Executes task command (if applicable)
4. **Result Processing**: Updates task status based on execution result
5. **Retry Logic**: Retries failed tasks if retry count allows
6. **Next Task**: Moves to next pending task
7. **Completion**: Stops when no more pending tasks

## Task Types Support

| Task Type | Execution Method | Example Commands |
|-----------|------------------|------------------|
| `slash_command` | Executes slash command via subprocess | `/analyze:quality`, `/dev:auto` |
| `autonomous` | Marks as completed (no direct execution) | Code refactoring tasks |
| `background` | Runs background analysis processes | Performance profiling |
| `manual` | Skips execution (requires manual intervention) | Documentation reviews |

## Progress Monitoring

### Real-time Status
During execution, you'll see:
```
🚀 Starting sequential task execution...
⚡ Executing task: Quality Analysis (ID: task_20241228_143022_123)
✅ Task completed: Quality Analysis
⚡ Executing task: Security Scan (ID: task_20241228_143025_456)
✅ Task completed: Security Scan
🏁 Sequential execution completed
```

### Background Mode
Background execution shows:
```
🚀 Sequential execution started in background
```

Use `/queue:status` to monitor background execution.

## Integration Points

### User Preferences
- Respects your quality threshold settings
- Uses your preferred timeout values
- Applies your retry preferences
- Learns from execution patterns

### Learning System
- Records task execution outcomes
- Updates success patterns
- Improves future suggestions
- Tracks performance metrics

### Error Recovery
- Automatic retry on transient failures
- Dependency resolution for complex workflows
- Rollback capabilities for critical operations
- Error pattern recognition and prevention

## Output Format

### Foreground Execution
```
🚀 Starting sequential task execution...
⚡ Executing task: Quality Analysis (ID: task_20241228_143022_123)
✅ Task completed: Quality Analysis
⚡ Executing task: Security Scan (ID: task_20241228_143025_456)
✅ Task completed: Security Scan
🏁 Sequential execution completed
✅ Executed 2 tasks successfully
```

### Background Execution
```
🚀 Sequential execution started in background
📊 Use /queue:status to monitor progress
```

### Error Output
```
⚡ Executing task: Fix Tests (ID: task_20241228_143028_789)
❌ Task failed: Fix Tests (Tests not found)
🛑 Stopping execution due to error
```

## Error Handling

### Common Errors
- **No Tasks**: Message when queue is empty
- **Execution Conflicts**: Handles multiple execution attempts
- **Timeout Issues**: Respects configured timeouts
- **Permission Errors**: Handles filesystem permission issues

### Recovery Strategies
- **Automatic Retry**: For transient failures
- **Dependency Resolution**: Waits for dependent tasks
- **Resource Management**: Handles system resource constraints
- **Error Logging**: Records failure details for analysis

## Performance Considerations

### System Resources
- Monitors memory usage during execution
- Manages CPU utilization for long-running tasks
- Handles disk space for logging and temp files
- Optimizes I/O operations for file-based tasks

### Execution Efficiency
- Parallel execution for independent tasks (future enhancement)
- Smart scheduling based on task complexity
- Resource pooling for repeated operations
- Caching of expensive computations

## Best Practices

1. **Test Queue**: Verify queue contents before execution
2. **Monitor Progress**: Check status during long executions
3. **Handle Errors**: Review failed tasks and retry if needed
4. **Background Mode**: Use for long-running workflows
5. **Stop on Error**: Use for critical workflows where failures matter

## Troubleshooting

### Execution Stalls
- Check `/queue:status` for current task
- Verify system resources availability
- Review task dependencies
- Check for stuck background processes

### High Failure Rate
- Review task commands and parameters
- Increase timeout values for long tasks
- Check system dependencies
- Verify file permissions

### Performance Issues
- Use background mode for long workflows
- Monitor system resource usage
- Optimize task order and priorities
- Consider task breakdown for complex operations

## See Also

- `/queue:add` - Add tasks to queue
- `/queue:status` - Monitor execution progress
- `/queue:list` - View queued tasks
- `/queue:stop` - Stop current execution
- `/queue:retry` - Retry failed tasks