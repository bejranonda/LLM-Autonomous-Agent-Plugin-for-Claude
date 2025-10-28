---
name: queue:retry
description: Retry failed tasks in the autonomous task queue
category: workflow
usage_frequency: medium
common_for: [error-recovery, task-management, queue-maintenance]
examples:
  - "/queue:retry --task-id task_20241228_143022_123"
  - "/queue:retry --status failed --priority high"
tools: Write, Bash
model: inherit
---

# Queue Retry Command

Retry failed tasks in the autonomous task queue, either individually or in batches. Useful for recovering from transient failures or after fixing underlying issues.

## Usage

```bash
/queue:retry [--task-id TASK_ID] [--status STATUS] [--priority PRIORITY] [--all]
```

## Parameters

### Optional Parameters
- `--task-id`: Retry specific task by ID
- `--status`: Retry all tasks with specified status (usually 'failed')
- `--priority`: Retry tasks with specified priority
- `--all`: Retry all failed tasks

## Examples

### Retry Specific Task
```bash
/queue:retry --task-id task_20241228_143022_123
```

### Retry All Failed Tasks
```bash
/queue:retry --status failed
```

### Retry High Priority Failed Tasks
```bash
/queue:retry --status failed --priority high
```

### Retry All Failed Tasks
```bash
/queue:retry --all
```

## Retry Behavior

### Single Task Retry
- Checks task retry count limits
- Resets task status to 'retrying'
- Increments retry counter
- Preserves original task configuration
- Moves task to front of queue

### Batch Retry
- Filters tasks by specified criteria
- Validates retry eligibility for each task
- Resets eligible tasks to 'retrying' status
- Maintains priority ordering
- Updates retry statistics

### Retry Limits
- Respects original retry count configuration
- Prevents infinite retry loops
- Tracks retry attempts per task
- Logs retry reasons and outcomes

## Output Format

### Single Task Retry
```
🔄 Task Retry
├─ Task ID: task_20241228_143022_123
├─ Name: Quality Analysis
├─ Previous Status: failed
├─ New Status: retrying
├─ Retry Attempt: 2/3
├─ Original Error: Timeout after 300 seconds
├─ Queue Position: 1 (front of queue)
└─ Estimated Retry Time: Immediately

✅ Task queued for retry
```

### Batch Retry
```
🔄 Batch Retry Operation
├─ Criteria: status=failed, priority=high
├─ Tasks Found: 8
├─ Tasks Eligible: 6
├─ Tasks Retried: 6
├─ Tasks Ineligible: 2

Retried Tasks:
├─ ✅ task_20241228_143022_123 | Quality Analysis | Retry 2/3
├─ ✅ task_20241228_143025_456 | Security Scan | Retry 1/3
├─ ✅ task_20241228_143028_789 | Documentation | Retry 1/3
└─ [3 more tasks...]

Ineligible Tasks:
├─ ❌ task_20241228_143018_333 | Test Execution | Max retries exceeded
└─ ❌ task_20241228_143015_777 | Performance Test | Cancelled by user

📊 Summary: 6 tasks retried | 2 tasks ineligible
```

### All Failed Tasks Retry
```
🔄 Retry All Failed Tasks
├─ Total Failed Tasks: 15
├─ Tasks With Retries Remaining: 12
├─ Tasks Retried: 12
├─ Tasks At Max Retries: 3

Retry Results:
├─ High Priority: 5 retried
├─ Medium Priority: 6 retried
├─ Low Priority: 1 retried

⚠️ 3 tasks have exceeded maximum retry limit
💡 Consider reviewing these tasks manually or increasing retry limits
```

## Retry Eligibility

### Automatic Checks
- **Retry Limit**: Must not have exceeded maximum retry attempts
- **Task Status**: Must be in 'failed' status
- **Dependencies**: Dependencies must be satisfied
- **Cancellation**: Task must not be cancelled

### Manual Override
Future enhancement: Allow retry of tasks at max limit:
```bash
/queue:retry --task-id TASK_ID --force
```

## Retry Strategies

### Immediate Retry
- Tasks are retried immediately
- Placed at front of queue in priority order
- No delay between retry attempts
- Best for transient failures

### Delayed Retry
Future enhancement: Add delay options:
```bash
/queue:retry --delay 300     # 5 minute delay
/queue:retry --exponential   # Exponential backoff
```

### Conditional Retry
Future enhancement: Smart retry conditions:
```bash
/queue:retry --if-timeout     # Only retry timeout failures
/queue:retry --if-network     # Only retry network-related errors
```

## Error Categories for Retry

### Retryable Errors
- **Timeout**: Task exceeded time limit
- **Network**: Network connectivity issues
- **Resource**: Temporary resource unavailability
- **Service**: External service temporarily down

### Non-Retryable Errors
- **Syntax**: Command syntax errors
- **Permission**: File permission issues
- **Configuration**: Configuration errors
- **User Cancelled**: Explicit user cancellation

## Retry Analytics

### Retry Statistics
Track retry effectiveness:
```
📊 Retry Analytics (Last 7 Days)
├─ Total Retries: 45
├─ Successful Retries: 32 (71%)
├─ Failed Retries: 13 (29%)
├─ Average Retry Time: 2.3 minutes
└─ Most Retried Task: Security Scan (4 times)

Retry Success by Category:
├─ Timeout Errors: 85% success rate
├─ Network Errors: 67% success rate
├─ Resource Errors: 50% success rate
└─ Service Errors: 75% success rate
```

### Pattern Learning
- Identifies common failure patterns
- Suggests optimal retry strategies
- Learns from successful retry approaches
- Improves future retry decisions

## Integration with Learning System

### Pattern Recognition
- Detects recurring failure patterns
- Identifies optimal retry timing
- Learns successful retry strategies
- Adapts retry limits based on history

### User Preferences
- Respects your retry preferences
- Adapts to your retry behavior
- Suggests retry actions based on patterns
- Remembers retry decisions for similar tasks

## Best Practices

1. **Review Failures**: Understand why tasks failed before retrying
2. **Fix Root Causes**: Address underlying issues causing failures
3. **Monitor Retries**: Track retry success rates
4. **Adjust Limits**: Consider increasing retry limits for flaky tasks
5. **Batch Operations**: Use batch retry for multiple related failures

## Troubleshooting

### Retry Issues
- **Task Not Found**: Verify task ID is correct
- **Max Retries Exceeded**: Task has reached retry limit
- **Dependencies Unmet**: Check if dependencies are completed
- **Task Cancelled**: Cancelled tasks cannot be retried

### Common Solutions
- Check task status and error messages
- Verify system resources are available
- Review network connectivity
- Fix configuration issues

## Advanced Options

### Conditional Retry
```bash
# Retry only timeout failures
/queue:retry --status failed --error-type timeout

# Retry only specific task types
/queue:retry --status failed --type slash_command

# Retry with modified parameters
/queue:retry --task-id TASK_ID --timeout 600
```

### Batch Management
```bash
# Review before retrying
/queue:list --status failed --limit 10

# Retry with confirmation
/queue:retry --status failed --confirm

# Retry with custom limits
/queue:retry --all --max-retries 5
```

## See Also

- `/queue:list` - Review failed tasks
- `/queue:status` - Check queue state
- `/queue:execute` - Start execution after retry
- `/queue:add` - Add new tasks with updated parameters
- `/queue:clear` - Clean up permanently failed tasks