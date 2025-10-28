---
name: queue:status
description: Show comprehensive status of the autonomous task queue
category: workflow
usage_frequency: high
common_for: [monitoring, progress-tracking, queue-management]
examples:
  - "/queue:status"
  - "/queue:status --verbose"
tools: Read, Bash
model: inherit
---

# Queue Status Command

Display comprehensive status of the autonomous task queue including current execution state, task counts, and performance metrics.

## Usage

```bash
/queue:status [--verbose]
```

## Parameters

### Optional Parameters
- `--verbose`: Show detailed information including individual tasks

## Status Information

### Overview Metrics
- **Total Tasks**: Total number of tasks in queue
- **Queued**: Tasks waiting to be executed
- **Running**: Currently executing task
- **Completed**: Successfully finished tasks
- **Failed**: Tasks that failed execution
- **Cancelled**: Tasks cancelled by user

### Priority Breakdown
- **Critical**: Urgent tasks
- **High**: Important tasks
- **Medium**: Standard tasks
- **Low**: Low priority tasks

### Type Breakdown
- **Slash Commands**: Executable commands
- **Autonomous**: Self-executing tasks
- **Background**: Background processes
- **Manual**: Manual intervention tasks

### Execution State
- **Current Task**: Task currently being executed
- **Execution Active**: Whether background execution is running
- **Queue Health**: Overall queue health score

## Examples

### Basic Status
```bash
/queue:status
```

Output:
```
📊 Queue Status Overview
├─ Total Tasks: 15
├─ Queued: 8
├─ Running: 1
├─ Completed: 5
├─ Failed: 1
├─ Cancelled: 0

🎯 Priority Breakdown
├─ Critical: 2
├─ High: 5
├─ Medium: 6
├─ Low: 2

📋 Type Breakdown
├─ Slash Commands: 8
├─ Autonomous: 4
├─ Background: 2
├─ Manual: 1

⚡ Execution State
├─ Current Task: task_20241228_143022_123 (Quality Analysis)
├─ Execution Active: Yes
├─ Queue Health: Good (87/100)
```

### Verbose Status
```bash
/queue:status --verbose
```

Includes detailed task information:
```
📊 Queue Status Overview
[... overview metrics ...]

📝 Queued Tasks (8)
├─ [1] task_20241228_143030_456 | Security Scan | High | slash_command
├─ [2] task_20241228_143032_789 | Documentation Update | Medium | manual
├─ [3] task_20241228_143034_012 | Performance Test | Low | background
└─ [5 more tasks...]

⚡ Currently Running
├─ Task: task_20241228_143022_123
├─ Name: Quality Analysis
├─ Command: /analyze:quality
├─ Started: 2024-12-28 14:30:25
├─ Duration: 2m 15s
└─ Progress: Analyzing code structure...

✅ Recently Completed (5)
├─ task_20241228_143020_999 | Environment Setup | 45s
├─ task_20241228_143018_777 | Dependency Check | 2m 10s
└─ [3 more tasks...]

❌ Failed Tasks (1)
├─ task_20241228_143015_333 | Test Execution | Timeout after 300s
└─ Retry attempts: 2/3
```

## Health Score Calculation

The queue health score (0-100) is calculated based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Completion Rate | 40% | Ratio of completed to total tasks |
| Failure Rate | 30% | Ratio of failed to total tasks (negative impact) |
| Queue Age | 15% | Age of oldest queued task |
| Execution Consistency | 15% | Regularity of task execution |

### Health Status Levels
- **Excellent** (90-100): Optimal queue performance
- **Good** (75-89): Healthy queue with minor issues
- **Fair** (60-74): Acceptable performance with some concerns
- **Poor** (0-59): Significant issues requiring attention

## Real-time Monitoring

### Active Execution Monitoring
When tasks are running, status includes:
```
⚡ Live Execution Monitor
├─ Current Task: Quality Analysis
├─ Progress: 65% complete
├─ Elapsed Time: 2m 15s
├─ Estimated Remaining: 1m 10s
├─ CPU Usage: 15%
├─ Memory Usage: 250MB
└─ Log Output: Analyzing src/main.py...
```

### Background Execution
For background processes:
```
🔄 Background Execution Active
├─ Process ID: 12345
├─ Started: 2024-12-28 14:30:00
├─ Tasks Completed: 3/8
├─ Current Phase: Security scanning
└─ Estimated Completion: 14:45:00
```

## Performance Metrics

### Execution Statistics
- **Average Execution Time**: Mean time per completed task
- **Success Rate**: Percentage of successful task executions
- **Queue Throughput**: Tasks completed per hour
- **Wait Time**: Average time tasks spend in queue

### Historical Trends
- **Completion Trend**: Increasing/decreasing completion rate
- **Error Rate Trend**: Changes in failure frequency
- **Queue Load Trend**: Queue size over time
- **Performance Trend**: Execution speed changes

## Integration with Other Systems

### User Preferences
Status reflects your preference settings:
- Quality thresholds
- Priority preferences
- Timeout configurations
- Retry limits

### Learning System
Incorporates learned patterns:
- Success probability for similar tasks
- Estimated completion times
- Recommended next actions
- Risk assessments

### Performance Analytics
Displays performance insights:
- Bottleneck identification
- Resource utilization
- Optimization opportunities
- Trend analysis

## Output Format

### Compact Mode (Default)
```
📊 Queue Status
├─ 15 total | 8 queued | 1 running | 5 completed | 1 failed
├─ Priority: 2 critical | 5 high | 6 medium | 2 low
├─ Types: 8 slash | 4 auto | 2 bg | 1 manual
├─ Health: Good (87/100)
└─ Current: Quality Analysis (65% complete)
```

### Verbose Mode
Detailed breakdown with individual tasks, performance metrics, and recommendations.

### JSON Mode (Programmatic)
```json
{
  "total_tasks": 15,
  "status_breakdown": {...},
  "priority_breakdown": {...},
  "type_breakdown": {...},
  "health_score": 87,
  "current_task": {...},
  "performance_metrics": {...}
}
```

## Troubleshooting

### Queue Health Issues
- **High Failure Rate**: Check task commands and dependencies
- **Long Wait Times**: Review task priorities and execution speed
- **Resource Constraints**: Monitor system resources
- **Stuck Tasks**: Check for dependency loops or deadlocks

### Performance Optimization
- **Task Batching**: Group similar tasks together
- **Priority Adjustment**: Reorder tasks for better flow
- **Resource Allocation**: Optimize system resource usage
- **Parallel Execution**: Enable parallel processing where possible

## Best Practices

1. **Regular Monitoring**: Check status during long executions
2. **Health Awareness**: Address queue health issues promptly
3. **Performance Tracking**: Monitor trends over time
4. **Resource Management**: Watch system resource usage
5. **Error Response**: Quickly address failed tasks

## See Also

- `/queue:list` - Detailed task listing
- `/queue:execute` - Start queue execution
- `/queue:stop` - Stop current execution
- `/queue:stats` - Detailed statistics
- `/queue:retry` - Retry failed tasks