# Task Queue System

## Overview

The Enhanced Task Queue System is a powerful component of the Autonomous Agent Plugin that enables sequential task execution without user intervention. It provides priority-based scheduling, dependency management, and intelligent retry logic for reliable batch operations.

## Key Features

### 1. Priority-Based Execution
- **Critical Tasks**: Highest priority for urgent fixes and security issues
- **High Priority**: Important improvements and bug fixes
- **Medium Priority**: Standard development tasks
- **Low Priority**: Cleanup, documentation, and optimization tasks

### 2. Sequential Execution
- **Uninterrupted Workflow**: Execute multiple tasks without stopping
- **Background Processing**: Run tasks in background for long workflows
- **Error Handling**: Configurable error handling (continue or stop on error)
- **Progress Monitoring**: Real-time progress tracking and status updates

### 3. Dependency Management
- **Task Dependencies**: Define prerequisite tasks that must complete first
- **Dependency Resolution**: Automatic dependency checking and validation
- **Complex Workflows**: Support for multi-step processes with dependencies
- **Circular Dependency Detection**: Prevent infinite dependency loops

### 4. Intelligent Retry Logic
- **Configurable Retry Limits**: Set retry count per task
- **Exponential Backoff**: Smart retry timing for transient failures
- **Error Categorization**: Different retry strategies for different error types
- **Retry Analytics**: Track retry success rates and patterns

### 5. Task Types
- **Slash Commands**: Execute plugin slash commands automatically
- **Autonomous Tasks**: Self-executing development tasks
- **Background Processes**: Long-running analysis and optimization
- **Manual Tasks**: Tasks requiring user intervention

## Architecture

### Core Components

#### TaskQueue Class
```python
class TaskQueue:
    """Enhanced task queue with priority-based execution."""

    def add_task(self, name: str, description: str, command: str = None,
                  priority: str = 'medium', task_type: str = 'manual',
                  dependencies: List[str] = None, retry_count: int = 3,
                  timeout: int = 300, metadata: Dict[str, Any] = None) -> str

    def add_slash_command(self, command: str, description: str = None,
                         priority: str = 'medium', timeout: int = 300) -> str

    def start_sequential_execution(self, stop_on_error: bool = False) -> bool

    def get_status(self) -> Dict[str, Any]

    def list_tasks(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]

    def update_task_status(self, task_id: str, status: str,
                          result: Optional[str] = None, error: Optional[str] = None) -> bool
```

#### Task Structure
```python
{
    "task_id": "task_20241228_143022_123",
    "name": "Quality Analysis",
    "description": "Run comprehensive quality analysis",
    "command": "/analyze:quality",
    "priority": 3,  # 1=low, 2=medium, 3=high, 4=critical
    "priority_str": "high",
    "status": "running",  # queued, running, completed, failed, cancelled, retrying
    "task_type": "slash_command",
    "dependencies": [],
    "retry_count": 3,
    "current_retry": 0,
    "timeout": 300,
    "metadata": {},
    "created_at": "2024-12-28T14:30:22.123Z",
    "queued_at": "2024-12-28T14:30:22.123Z",
    "started_at": "2024-12-28T14:30:25.456Z",
    "completed_at": null,
    "execution_time": null,
    "result": null,
    "error": null,
    "execution_log": []
}
```

## Storage Structure

### Directory Layout
```
.claude-patterns/
├── enhanced_task_queue.json    # Main queue storage
├── task_execution_log.json     # Execution history
├── queue_statistics.json       # Performance metrics
└── backups/                    # Automatic backups
    ├── enhanced_task_queue_20241228_143022.json
    └── task_execution_log_20241228_143022.json
```

### Queue Data Schema
```json
{
  "tasks": [
    {
      "task_id": "task_20241228_143022_123",
      "name": "Quality Analysis",
      "description": "Run comprehensive quality analysis",
      "command": "/analyze:quality",
      "priority": 3,
      "priority_str": "high",
      "status": "completed",
      "task_type": "slash_command",
      "dependencies": [],
      "retry_count": 3,
      "current_retry": 0,
      "timeout": 300,
      "metadata": {"original_command": "/analyze:quality"},
      "created_at": "2024-12-28T14:30:22.123Z",
      "queued_at": "2024-12-28T14:30:22.123Z",
      "started_at": "2024-12-28T14:30:25.456Z",
      "completed_at": "2024-12-28T14:32:15.789Z",
      "execution_time": 110.333,
      "result": "Quality analysis completed successfully",
      "error": null,
      "execution_log": [
        {
          "status_change": "queued -> running",
          "timestamp": "2024-12-28T14:30:25.456Z"
        },
        {
          "status_change": "running -> completed",
          "timestamp": "2024-12-28T14:32:15.789Z",
          "result": "Quality analysis completed successfully"
        }
      ]
    }
  ]
}
```

## Slash Commands

### Task Management

#### /queue:add
Add custom tasks to the queue.

```bash
/queue:add --name "Task Name" --description "Description" --command "command" --priority high
```

**Parameters:**
- `--name`: Task name (required)
- `--description`: Task description (required)
- `--command`: Command to execute (optional)
- `--priority`: Priority level (critical, high, medium, low) - default: medium
- `--type`: Task type (slash_command, autonomous, background, manual) - default: manual
- `--timeout`: Timeout in seconds - default: 300
- `--retry`: Number of retry attempts - default: 3
- `--dependencies`: Comma-separated task IDs this task depends on

**Example:**
```bash
/queue:add --name "Security Scan" --description "Check for security vulnerabilities" \
           --command "/analyze:dependencies" --priority high --retry 5
```

#### /queue:slash
Add slash commands directly to the queue.

```bash
/queue:slash --command "/analyze:quality" --priority high
```

**Parameters:**
- `--command`: Slash command to execute (required)
- `--description`: Optional description
- `--priority`: Priority level - default: medium
- `--timeout`: Timeout in seconds - default: 300

**Example:**
```bash
/queue:slash --command "/dev:auto \"fix failing tests\"" --priority critical
```

### Execution Control

#### /queue:execute
Start sequential execution of queued tasks.

```bash
/queue:execute [--stop-on-error] [--background]
```

**Parameters:**
- `--stop-on-error`: Stop execution on first task failure
- `--background`: Run execution in background process

**Execution Flow:**
1. Select highest priority pending task with satisfied dependencies
2. Update task status to "running"
3. Execute task command (if applicable)
4. Update task status based on result
5. Retry failed tasks if retry count allows
6. Continue with next pending task
7. Stop when no more pending tasks

**Example:**
```bash
# Execute with error continuation
/queue:execute

# Execute with stop on error
/queue:execute --stop-on-error

# Execute in background
/queue:execute --background
```

#### /queue:stop
Stop current sequential execution.

```bash
/queue:stop
```

### Status and Monitoring

#### /queue:status
Show comprehensive queue status.

```bash
/queue:status [--verbose]
```

**Output Example:**
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

#### /queue:list
List tasks with filtering options.

```bash
/queue:list [--status STATUS] [--priority PRIORITY] [--limit N] [--format FORMAT]
```

**Parameters:**
- `--status`: Filter by status (queued, running, completed, failed, cancelled, retrying)
- `--priority`: Filter by priority (critical, high, medium, low)
- `--limit`: Maximum number of tasks to show - default: 20
- `--format`: Output format (table, json, detailed) - default: table

**Example:**
```bash
# List queued tasks
/queue:list --status queued

# List high priority tasks
/queue:list --priority high

# Detailed format with limit
/queue:list --format detailed --limit 5
```

### Task Management

#### /queue:retry
Retry failed tasks.

```bash
/queue:retry [--task-id TASK_ID] [--status STATUS] [--priority PRIORITY] [--all]
```

**Parameters:**
- `--task-id`: Retry specific task by ID
- `--status`: Retry all tasks with specified status (usually 'failed')
- `--priority`: Retry tasks with specified priority
- `--all`: Retry all failed tasks

**Example:**
```bash
# Retry specific task
/queue:retry --task-id task_20241228_143022_123

# Retry all failed tasks
/queue:retry --status failed

# Retry high priority failed tasks
/queue:retry --status failed --priority high
```

#### /queue:clear
Clean up completed, failed, and cancelled tasks.

```bash
/queue:clear [--older-than HOURS] [--status STATUS] [--keep-recent] [--dry-run]
```

**Parameters:**
- `--older-than`: Remove tasks older than specified hours - default: 24
- `--status`: Specific status to clear (completed, failed, cancelled)
- `--keep-recent`: Keep recent tasks regardless of age
- `--dry-run`: Show what would be removed without actually deleting

**Example:**
```bash
# Standard cleanup
/queue:clear

# Extended cleanup
/queue:clear --older-than 72

# Dry run to preview
/queue:clear --dry-run --older-than 48
```

## Usage Examples

### Basic Workflow

```bash
# Add tasks to queue
/queue:slash --command "/analyze:project" --priority high
/queue:slash --command "/analyze:quality" --priority medium
/queue:slash --command "/validate:fullstack" --priority medium

# Check queue status
/queue:status

# Execute all tasks
/queue:execute

# Monitor progress
/queue:status --verbose
```

### Complex Workflow with Dependencies

```bash
# First task - no dependencies
/queue:add --name "Environment Setup" \
           --description "Prepare development environment" \
           --command "/dev:auto \"setup environment\"" \
           --priority critical

# Second task - depends on first
/queue:add --name "Run Tests" \
           --description "Execute test suite" \
           --command "/dev:auto \"run tests\"" \
           --priority high \
           --dependencies "task_20241228_143022_123"

# Third task - depends on test completion
/queue:add --name "Generate Documentation" \
           --description "Create project documentation" \
           --command "/dev:auto \"generate docs\"" \
           --priority medium \
           --dependencies "task_20241228_143025_456"

# Execute with stop on error for critical workflow
/queue:execute --stop-on-error
```

### Batch Operations

```bash
# Queue multiple related tasks
/queue:slash --command "/analyze:project" --priority high
/queue:slash --command "/analyze:quality" --priority high
/queue:slash --command "/analyze:dependencies" --priority high
/queue:slash --command "/validate:fullstack" --priority medium

# Execute in background
/queue:execute --background

# Monitor progress
/queue:status
```

### Error Recovery

```bash
# Check what failed
/queue:list --status failed

# Retry failed tasks
/queue:retry --status failed

# If retries fail, check details
/queue:list --status failed --format detailed

# Manually fix issues and retry specific tasks
/queue:retry --task-id task_20241228_143022_123
```

## Task Types and Execution

### Slash Command Tasks
```bash
# Add slash command
/queue:slash --command "/analyze:quality" --priority high

# Execution: Runs the slash command via subprocess
# Success: Command exits with code 0
# Failure: Command exits with non-zero code or times out
```

### Autonomous Tasks
```bash
# Add autonomous task
/queue:add --name "Code Refactoring" \
           --description "Refactor authentication module" \
           --priority medium \
           --type autonomous

# Execution: No direct command execution
# Success: Manually marked as completed
# Use Case: Complex development work requiring human oversight
```

### Background Tasks
```bash
# Add background task
/queue:add --name "Performance Analysis" \
           --description "Analyze code performance" \
           --priority low \
           --type background \
           --timeout 600

# Execution: Long-running analysis processes
# Success: Analysis completes successfully
# Use Case: Performance profiling, security scanning
```

### Manual Tasks
```bash
# Add manual task
/queue:add --name "Code Review" \
           --description "Review pull request #123" \
           --priority medium \
           --type manual

# Execution: Skipped in automatic execution
# Success: Manually marked as completed by user
# Use Case: Tasks requiring human intervention
```

## Priority and Scheduling

### Priority Levels
| Priority | Level | Description | Use Case |
|----------|-------|-------------|---------|
| Critical | 4 | Highest priority, executes first | Security fixes, production issues |
| High | 3 | High priority, early execution | Important improvements, bug fixes |
| Medium | 2 | Standard priority | Regular development tasks |
| Low | 1 | Low priority, last execution | Cleanup, documentation, optimization |

### Scheduling Algorithm
1. **Priority Sort**: Tasks sorted by priority (descending)
2. **Creation Time**: Same priority sorted by creation time (ascending)
3. **Dependency Check**: Only tasks with satisfied dependencies are executable
4. **Status Filter**: Only queued tasks are considered for execution

### Execution Order Example
```
Priority 4 (Critical):   [task_4] -> [task_1] -> [task_7]
Priority 3 (High):       [task_2] -> [task_5] -> [task_9]
Priority 2 (Medium):     [task_3] -> [task_6] -> [task_8]
Priority 1 (Low):        [task_10] -> [task_11]

Execution Order: task_4, task_1, task_7, task_2, task_5, task_9, ...
```

## Error Handling and Recovery

### Error Categories
- **Timeout Errors**: Task execution exceeds timeout limit
- **Command Errors**: Command returns non-zero exit code
- **System Errors**: File system, permission, or resource issues
- **Dependency Errors**: Required dependencies not satisfied
- **User Errors**: Invalid task configuration or parameters

### Retry Logic
```python
def should_retry(task, error):
    """Determine if task should be retried."""
    # Check retry limit
    if task['current_retry'] >= task['retry_count']:
        return False, "Max retries exceeded"

    # Check error type
    if is_timeout_error(error):
        return True, "Timeout error, retrying"
    elif is_transient_error(error):
        return True, "Transient error, retrying"
    elif is_permanent_error(error):
        return False, "Permanent error, not retrying"

    # Default retry for unknown errors
    return True, "Unknown error, retrying"
```

### Recovery Strategies
1. **Automatic Retry**: For transient failures
2. **Manual Intervention**: For configuration or logic errors
3. **Dependency Resolution**: For dependency-related failures
4. **Resource Allocation**: For resource constraint issues

## Performance and Optimization

### Execution Metrics
- **Throughput**: Tasks completed per hour
- **Success Rate**: Percentage of successful task executions
- **Average Execution Time**: Mean time per task
- **Queue Velocity**: Rate at which queue is processed

### Optimization Techniques
1. **Batch Processing**: Group similar tasks for efficiency
2. **Parallel Execution**: Future enhancement for independent tasks
3. **Resource Pooling**: Reuse resources across tasks
4. **Caching**: Cache expensive computations

### Performance Monitoring
```bash
# Check queue statistics
/queue:status --verbose

# Monitor execution trends
python lib/enhanced_task_queue.py --dir .claude-patterns stats
```

## Integration Points

### User Preferences
```python
# Queue respects user preferences
preferences = {
    "workflow": {
        "default_priority": "medium",
        "auto_retry": True,
        "max_retry_count": 3,
        "stop_on_error": False
    }
}
```

### Learning System
```python
# Learn from execution patterns
learning_data = {
    "task_patterns": {
        "analyze:quality": {
            "success_rate": 0.95,
            "average_time": 120,
            "optimal_priority": "high"
        }
    }
}
```

### System Environment
```python
# Adapt to system capabilities
system_caps = {
    "parallel_execution": psutil.cpu_count() >= 4,
    "memory_adequate": psutil.virtual_memory().total >= 8 * (1024**3),
    "disk_space_adequate": psutil.disk_usage('/').free >= 10 * (1024**3)
}
```

## API Reference

### TaskQueue Class Methods

#### add_task()
```python
def add_task(self, name: str, description: str, command: str = None,
              priority: str = 'medium', task_type: str = 'manual',
              dependencies: List[str] = None, retry_count: int = 3,
              timeout: int = 300, metadata: Dict[str, Any] = None) -> str
```
Add a new task to the queue.

**Parameters:**
- `name`: Task name/identifier
- `description`: Detailed task description
- `command`: Command to execute (optional)
- `priority`: Task priority level
- `task_type`: Type of task
- `dependencies`: List of task IDs this task depends on
- `retry_count`: Number of retry attempts
- `timeout`: Timeout in seconds
- `metadata`: Additional task metadata

**Returns:** Task ID string

#### add_slash_command()
```python
def add_slash_command(self, command: str, description: str = None,
                     priority: str = 'medium', timeout: int = 300) -> str
```
Add a slash command to the queue.

**Parameters:**
- `command`: Slash command to execute
- `description`: Optional description
- `priority`: Task priority level
- `timeout`: Command timeout in seconds

**Returns:** Task ID string

#### start_sequential_execution()
```python
def start_sequential_execution(self, stop_on_error: bool = False) -> bool
```
Start sequential execution of queued tasks.

**Parameters:**
- `stop_on_error`: Stop execution on first task failure

**Returns:** True if execution started successfully

#### get_status()
```python
def get_status(self) -> Dict[str, Any]
```
Get comprehensive queue status.

**Returns:** Dictionary with queue statistics and current state

#### list_tasks()
```python
def list_tasks(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]
```
List tasks with optional filtering.

**Parameters:**
- `status`: Filter by task status
- `limit`: Maximum number of tasks to return

**Returns:** List of task dictionaries

## Configuration

### Environment Variables
```bash
export CLAUDE_QUEUE_DIR="/path/to/queue"
export CLAUDE_QUEUE_TIMEOUT="300"
export CLAUDE_QUEUE_MAX_RETRIES="3"
export CLAUDE_QUEUE_AUTO_EXECUTE="false"
```

### Default Configuration
```json
{
  "queue": {
    "default_priority": "medium",
    "default_timeout": 300,
    "default_retry_count": 3,
    "max_concurrent_tasks": 1,
    "stop_on_error": false,
    "auto_cleanup": true,
    "cleanup_interval": 24,
    "backup_enabled": true,
    "backup_retention": 7
  }
}
```

## Troubleshooting

### Common Issues

#### Task Not Executing
```bash
# Check queue status
/queue:status --verbose

# Check task dependencies
/queue:list --status queued --format detailed

# Check for stuck execution
python lib/enhanced_task_queue.py --dir .claude-patterns status
```

#### High Failure Rate
```bash
# Check failed tasks
/queue:list --status failed

# Review error messages
/queue:list --status failed --format detailed

# Retry with different parameters
/queue:retry --status failed
```

#### Performance Issues
```bash
# Check queue statistics
/queue:status --verbose

# Monitor system resources
python lib/enhanced_task_queue.py --dir .claude-patterns stats

# Clean up old tasks
/queue:clear --older-than 48
```

### Debug Mode
```bash
# Enable debug logging
export CLAUDE_DEBUG=true

# Check queue integrity
python lib/enhanced_task_queue.py --dir .claude-patterns --validate

# Manual task execution
python lib/enhanced_task_queue.py --dir .claude-patterns execute --task-id TASK_ID
```

## Best Practices

1. **Task Organization**: Group related tasks together
2. **Priority Management**: Use appropriate priority levels
3. **Dependency Planning**: Design clear dependency chains
4. **Error Handling**: Configure appropriate retry limits
5. **Monitoring**: Regularly check queue status and performance
6. **Cleanup**: Periodically clean up completed tasks
7. **Backup**: Enable automatic backups for important queues

## Future Enhancements

### Planned Features
- **Parallel Execution**: Execute independent tasks simultaneously
- **Task Templates**: Reusable task configurations
- **Web Interface**: Web-based queue management
- **API Integration**: REST API for external integration
- **Advanced Scheduling**: Cron-like scheduling capabilities

### Extension Points
- **Custom Task Types**: Add domain-specific task types
- **Plugin Integration**: Third-party task execution plugins
- **Custom Retry Strategies**: Implement specialized retry logic
- **External Triggers**: Webhook and event-based task creation

---

*This documentation is part of the Autonomous Agent Plugin v5.3.4*