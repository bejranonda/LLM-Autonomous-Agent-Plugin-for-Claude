#!/usr/bin/env python3
"""
Enhanced Task Queue System for Autonomous Agent Plugin

Manages task prioritization and execution tracking with advanced features:
- Sequential task execution without user intervention
- Slash command integration
- Priority-based scheduling
- Background task processing
- Task dependency management
- Auto-retry and error handling
- Performance tracking and analytics

Version: 2.0.0
Author: Autonomous Agent Development Team
"""

import json
import sys
import threading
import time
import queue
import subprocess
import signal
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from collections import defaultdict
import platform

# Handle Windows compatibility for file locking
if platform.system() == 'Windows':
    import msvcrt

    def lock_file(f, exclusive=False):
        """Windows file locking using msvcrt."""
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        """Windows file unlocking."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl

    def lock_file(f, exclusive=False):
        """Unix file locking using fcntl."""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)

    def unlock_file(f):
        """Unix file unlocking."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class TaskQueue:
    """Enhanced task queue with priority-based execution and slash command support."""

    # Priority levels
    PRIORITY_CRITICAL = 4
    PRIORITY_HIGH = 3
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 1

    # Task statuses
    STATUS_QUEUED = 'queued'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_RETRYING = 'retrying'

    # Task types
    TYPE_SLASH_COMMAND = 'slash_command'
    TYPE_AUTONOMOUS = 'autonomous'
    TYPE_BACKGROUND = 'background'
    TYPE_MANUAL = 'manual'

    def __init__(self, queue_dir: str = ".claude-patterns"):
        """
        Initialize enhanced task queue.

        Args:
            queue_dir: Directory for queue storage
        """
        self.queue_dir = Path(queue_dir)
        self.queue_file = self.queue_dir / "enhanced_task_queue.json"
        self.execution_log = self.queue_dir / "task_execution_log.json"
        self.stats_file = self.queue_dir / "queue_statistics.json"

        # Thread safety
        self._lock = threading.RLock()
        self._execution_lock = threading.Lock()

        # Execution state
        self._current_task = None
        self._execution_thread = None
        self._stop_execution = threading.Event()
        self._execution_queue = queue.PriorityQueue()

        self._ensure_directories()
        self._initialize_storage()

    def _ensure_directories(self):
        """Create necessary directories."""
        self.queue_dir.mkdir(parents=True, exist_ok=True)

    def _initialize_storage(self):
        """Initialize storage files if needed."""
        if not self.queue_file.exists():
            self._write_queue([])

        if not self.execution_log.exists():
            self._write_execution_log([])

        if not self.stats_file.exists():
            default_stats = {
                "total_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "average_execution_time": 0.0,
                "queue_created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "by_priority": {str(p): 0 for p in range(1, 5)},
                "by_type": {t: 0 for t in [self.TYPE_SLASH_COMMAND, self.TYPE_AUTONOMOUS, self.TYPE_BACKGROUND, self.TYPE_MANUAL]},
                "execution_trends": []
            }
            self._write_stats(default_stats)

    def _read_queue(self) -> List[Dict[str, Any]]:
        """Read task queue from file with file locking."""
        try:
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                lock_file(f, exclusive=False)
                try:
                    content = f.read()
                    if not content.strip():
                        return []
                    return json.loads(content)
                finally:
                    unlock_file(f)
        except FileNotFoundError:
            self._initialize_storage()
            return []
        except json.JSONDecodeError as e:
            print(f"Error reading queue: {e}", file=sys.stderr)
            return []

    def _write_queue(self, queue: List[Dict[str, Any]]):
        """Write task queue to file with file locking."""
        try:
            with open(self.queue_file, 'w', encoding='utf-8') as f:
                lock_file(f, exclusive=True)
                try:
                    json.dump(queue, f, indent=2, ensure_ascii=False)
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error writing queue: {e}", file=sys.stderr)
            raise

    def _read_execution_log(self) -> List[Dict[str, Any]]:
        """Read execution log from file."""
        try:
            with open(self.execution_log, 'r', encoding='utf-8') as f:
                lock_file(f, exclusive=False)
                try:
                    content = f.read()
                    if not content.strip():
                        return []
                    return json.loads(content)
                finally:
                    unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_execution_log(self, log: List[Dict[str, Any]]):
        """Write execution log to file."""
        try:
            with open(self.execution_log, 'w', encoding='utf-8') as f:
                lock_file(f, exclusive=True)
                try:
                    json.dump(log, f, indent=2, ensure_ascii=False)
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error writing execution log: {e}", file=sys.stderr)

    def _read_stats(self) -> Dict[str, Any]:
        """Read queue statistics from file."""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                lock_file(f, exclusive=False)
                try:
                    return json.load(f)
                finally:
                    unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self._get_default_stats()

    def _write_stats(self, stats: Dict[str, Any]):
        """Write queue statistics to file."""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                lock_file(f, exclusive=True)
                try:
                    json.dump(stats, f, indent=2, ensure_ascii=False)
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error writing stats: {e}", file=sys.stderr)

    def _get_default_stats(self) -> Dict[str, Any]:
        """Get default statistics structure."""
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "average_execution_time": 0.0,
            "queue_created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "by_priority": {str(p): 0 for p in range(1, 5)},
            "by_type": {t: 0 for t in [self.TYPE_SLASH_COMMAND, self.TYPE_AUTONOMOUS, self.TYPE_BACKGROUND, self.TYPE_MANUAL]},
            "execution_trends": []
        }

    def _parse_priority(self, priority_str: str) -> int:
        """Convert priority string to numeric value."""
        priority_map = {
            'critical': self.PRIORITY_CRITICAL,
            'high': self.PRIORITY_HIGH,
            'medium': self.PRIORITY_MEDIUM,
            'low': self.PRIORITY_LOW,
            '4': self.PRIORITY_CRITICAL,
            '3': self.PRIORITY_HIGH,
            '2': self.PRIORITY_MEDIUM,
            '1': self.PRIORITY_LOW
        }
        return priority_map.get(priority_str.lower(), self.PRIORITY_MEDIUM)

    def _priority_to_string(self, priority: int) -> str:
        """Convert numeric priority to string."""
        priority_map = {
            self.PRIORITY_CRITICAL: 'critical',
            self.PRIORITY_HIGH: 'high',
            self.PRIORITY_MEDIUM: 'medium',
            self.PRIORITY_LOW: 'low'
        }
        return priority_map.get(priority, 'medium')

    def add_task(
        self,
        name: str,
        description: str,
        command: str = None,
        priority: str = 'medium',
        task_type: str = TYPE_MANUAL,
        dependencies: List[str] = None,
        retry_count: int = 3,
        timeout: int = 300,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Add a new task to the queue.

        Args:
            name: Task name/identifier
            description: Detailed task description
            command: Command to execute (for slash commands)
            priority: Task priority (critical, high, medium, low)
            task_type: Type of task
            dependencies: List of task IDs this task depends on
            retry_count: Number of retry attempts on failure
            timeout: Timeout in seconds
            metadata: Additional task metadata

        Returns:
            Task ID of the created task
        """
        with self._lock:
            # Generate task ID
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            task_id = f"task_{timestamp}"

            # Create task object
            task = {
                'task_id': task_id,
                'name': name,
                'description': description,
                'command': command,
                'priority': self._parse_priority(priority),
                'priority_str': priority.lower(),
                'status': self.STATUS_QUEUED,
                'task_type': task_type,
                'dependencies': dependencies or [],
                'retry_count': retry_count,
                'current_retry': 0,
                'timeout': timeout,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat(),
                'queued_at': datetime.now().isoformat(),
                'started_at': None,
                'completed_at': None,
                'execution_time': None,
                'result': None,
                'error': None,
                'execution_log': []
            }

            # Add to queue
            queue_data = self._read_queue()
            queue_data.append(task)

            # Sort by priority (critical to low) and creation time (old to new)
            queue_data.sort(key=lambda x: (-x['priority'], x['created_at']))

            self._write_queue(queue_data)

            # Update statistics
            self._update_stats_add_task(task)

            return task_id

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Get the next pending task with highest priority.

        Returns:
            Task dictionary or None if no pending tasks
        """
        with self._lock:
            queue_data = self._read_queue()

            # Find first task that is not blocked by dependencies
            for task in queue_data:
                if task['status'] == self.STATUS_QUEUED:
                    # Check dependencies
                    if self._are_dependencies_satisfied(task, queue_data):
                        return task

            return None

    def _are_dependencies_satisfied(self, task: Dict[str, Any], queue_data: List[Dict[str, Any]]) -> bool:
        """Check if all task dependencies are satisfied."""
        if not task['dependencies']:
            return True

        dependency_status = {}
        for dep_id in task['dependencies']:
            # Find dependency in queue
            dep_task = next((t for t in queue_data if t['task_id'] == dep_id), None)
            if dep_task:
                dependency_status[dep_id] = dep_task['status'] == self.STATUS_COMPLETED
            else:
                # Dependency not found, assume completed (might be in execution log)
                dependency_status[dep_id] = True

        return all(dependency_status.values())

    def update_task_status(
        self,
        task_id: str,
        status: str,
        result: Optional[str] = None,
        error: Optional[str] = None,
        execution_time: Optional[float] = None
    ) -> bool:
        """
        Update task status and optional result/error.

        Args:
            task_id: ID of the task to update
            status: New status
            result: Task result (optional)
            error: Error message (optional)
            execution_time: Execution time in seconds (optional)

        Returns:
            True if task was found and updated, False otherwise
        """
        with self._lock:
            valid_statuses = [
                self.STATUS_QUEUED, self.STATUS_RUNNING,
                self.STATUS_COMPLETED, self.STATUS_FAILED,
                self.STATUS_CANCELLED, self.STATUS_RETRYING
            ]

            if status not in valid_statuses:
                print(f"Error: Invalid status '{status}'. Must be one of: {valid_statuses}", file=sys.stderr)
                return False

            queue_data = self._read_queue()
            task_found = False

            for task in queue_data:
                if task['task_id'] == task_id:
                    old_status = task['status']
                    task['status'] = status

                    # Update timestamps
                    now = datetime.now().isoformat()
                    if status == self.STATUS_RUNNING and old_status == self.STATUS_QUEUED:
                        task['started_at'] = now
                    elif status in [self.STATUS_COMPLETED, self.STATUS_FAILED, self.STATUS_CANCELLED]:
                        if not task['started_at']:
                            task['started_at'] = now
                        task['completed_at'] = now
                        task['execution_time'] = execution_time

                    # Update result/error
                    if result is not None:
                        task['result'] = result
                    if error is not None:
                        task['error'] = error

                    # Add to execution log
                    log_entry = {
                        'task_id': task_id,
                        'status_change': f"{old_status} -> {status}",
                        'timestamp': now,
                        'result': result,
                        'error': error
                    }
                    self._add_to_execution_log(log_entry)

                    task_found = True
                    break

            if not task_found:
                print(f"Error: Task '{task_id}' not found", file=sys.stderr)
                return False

            self._write_queue(queue_data)
            self._update_stats_task_completed(task_id, status)

            return True

    def _add_to_execution_log(self, log_entry: Dict[str, Any]):
        """Add entry to execution log."""
        log_data = self._read_execution_log()
        log_data.append(log_entry)

        # Keep only last 1000 entries
        if len(log_data) > 1000:
            log_data = log_data[-1000:]

        self._write_execution_log(log_data)

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID."""
        with self._lock:
            queue_data = self._read_queue()
            for task in queue_data:
                if task['task_id'] == task_id:
                    return task
            return None

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive queue status."""
        with self._lock:
            queue_data = self._read_queue()

            if not queue_data:
                return {
                    'total_tasks': 0,
                    'queued': 0,
                    'running': 0,
                    'completed': 0,
                    'failed': 0,
                    'cancelled': 0,
                    'retrying': 0,
                    'by_priority': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
                    'by_type': {t: 0 for t in [self.TYPE_SLASH_COMMAND, self.TYPE_AUTONOMOUS, self.TYPE_BACKGROUND, self.TYPE_MANUAL]},
                    'current_task': self._current_task,
                    'execution_active': self._execution_thread is not None and self._execution_thread.is_alive()
                }

            # Count tasks by status
            status_counts = {
                'queued': 0, 'running': 0, 'completed': 0,
                'failed': 0, 'cancelled': 0, 'retrying': 0
            }

            priority_counts = {
                'critical': 0, 'high': 0, 'medium': 0, 'low': 0
            }

            type_counts = {
                t: 0 for t in [self.TYPE_SLASH_COMMAND, self.TYPE_AUTONOMOUS, self.TYPE_BACKGROUND, self.TYPE_MANUAL]
            }

            for task in queue_data:
                status_counts[task['status']] = status_counts.get(task['status'], 0) + 1
                priority_str = self._priority_to_string(task['priority'])
                priority_counts[priority_str] = priority_counts.get(priority_str, 0) + 1
                type_counts[task['task_type']] = type_counts.get(task['task_type'], 0) + 1

            return {
                'total_tasks': len(queue_data),
                **status_counts,
                'by_priority': priority_counts,
                'by_type': type_counts,
                'current_task': self._current_task,
                'execution_active': self._execution_thread is not None and self._execution_thread.is_alive()
            }

    def list_tasks(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """List tasks, optionally filtered by status."""
        with self._lock:
            queue_data = self._read_queue()

            if status:
                queue_data = [task for task in queue_data if task['status'] == status]

            # Sort by priority and creation time
            queue_data.sort(key=lambda x: (-x['priority'], x['created_at']))

            return queue_data[:limit]

    def clear_completed(self, older_than_hours: int = 24) -> int:
        """
        Remove completed/failed tasks older than specified hours.

        Args:
            older_than_hours: Remove tasks completed more than this many hours ago

        Returns:
            Number of tasks removed
        """
        with self._lock:
            queue_data = self._read_queue()
            cutoff_time = datetime.now() - timedelta(hours=older_than_hours)

            original_count = len(queue_data)
            queue_data = [
                task for task in queue_data
                if task['status'] not in [self.STATUS_COMPLETED, self.STATUS_FAILED, self.STATUS_CANCELLED] or
                   (task.get('completed_at') and datetime.fromisoformat(task['completed_at']) > cutoff_time)
            ]

            self._write_queue(queue_data)
            return original_count - len(queue_data)

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task."""
        return self.update_task_status(task_id, self.STATUS_CANCELLED, error="Task cancelled by user")

    def retry_task(self, task_id: str) -> bool:
        """Retry a failed task."""
        with self._lock:
            task = self.get_task(task_id)
            if not task:
                return False

            if task['status'] != self.STATUS_FAILED:
                print(f"Error: Task '{task_id}' is not in failed status", file=sys.stderr)
                return False

            if task['current_retry'] >= task['retry_count']:
                print(f"Error: Task '{task_id}' has exceeded retry limit", file=sys.stderr)
                return False

            task['current_retry'] += 1
            task['status'] = self.STATUS_RETRYING
            task['error'] = None

            # Update in queue
            queue_data = self._read_queue()
            for i, t in enumerate(queue_data):
                if t['task_id'] == task_id:
                    queue_data[i] = task
                    break

            self._write_queue(queue_data)
            return True

    def _update_stats_add_task(self, task: Dict[str, Any]):
        """Update statistics when task is added."""
        stats = self._read_stats()
        stats['total_tasks'] += 1
        stats['by_priority'][str(task['priority'])] += 1
        stats['by_type'][task['task_type']] += 1
        stats['last_updated'] = datetime.now().isoformat()
        self._write_stats(stats)

    def _update_stats_task_completed(self, task_id: str, status: str):
        """Update statistics when task is completed."""
        stats = self._read_stats()

        if status == self.STATUS_COMPLETED:
            stats['completed_tasks'] += 1
        elif status in [self.STATUS_FAILED, self.STATUS_CANCELLED]:
            stats['failed_tasks'] += 1

        stats['last_updated'] = datetime.now().isoformat()
        self._write_stats(stats)

    def get_statistics(self) -> Dict[str, Any]:
        """Get detailed queue statistics."""
        with self._lock:
            stats = self._read_stats()
            status = self.get_status()

            # Calculate completion rate
            completion_rate = 0.0
            if stats['total_tasks'] > 0:
                completed = stats['completed_tasks']
                completion_rate = (completed / stats['total_tasks']) * 100

            # Calculate average execution time from completed tasks
            completed_tasks = self.list_tasks(self.STATUS_COMPLETED)
            avg_execution_time = 0.0
            if completed_tasks:
                execution_times = [t.get('execution_time', 0) for t in completed_tasks if t.get('execution_time')]
                if execution_times:
                    avg_execution_time = sum(execution_times) / len(execution_times)

            return {
                **stats,
                'current_status': status,
                'completion_rate': round(completion_rate, 2),
                'average_execution_time': round(avg_execution_time, 2),
                'queue_health': self._calculate_queue_health(stats, status)
            }

    def _calculate_queue_health(self, stats: Dict[str, Any], status: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate queue health metrics."""
        health_score = 100.0

        # Deduct for failed tasks
        if stats['total_tasks'] > 0:
            failure_rate = (stats['failed_tasks'] / stats['total_tasks']) * 100
            health_score -= failure_rate * 0.5

        # Deduct for long-running tasks
        if status['running'] > 5:
            health_score -= (status['running'] - 5) * 2

        # Deduct for queued tasks
        if status['queued'] > 10:
            health_score -= (status['queued'] - 10) * 1

        health_score = max(0, min(100, health_score))

        health_status = 'excellent'
        if health_score < 50:
            health_status = 'poor'
        elif health_score < 75:
            health_status = 'fair'
        elif health_score < 90:
            health_status = 'good'

        return {
            'score': round(health_score, 2),
            'status': health_status,
            'issues': self._identify_health_issues(stats, status)
        }

    def _identify_health_issues(self, stats: Dict[str, Any], status: Dict[str, Any]) -> List[str]:
        """Identify potential health issues."""
        issues = []

        if status['running'] > 5:
            issues.append(f"High number of running tasks: {status['running']}")

        if status['queued'] > 10:
            issues.append(f"High number of queued tasks: {status['queued']}")

        if stats['total_tasks'] > 0:
            failure_rate = (stats['failed_tasks'] / stats['total_tasks']) * 100
            if failure_rate > 20:
                issues.append(f"High failure rate: {failure_rate:.1f}%")

        return issues

    # Slash command execution methods

    def add_slash_command(
        self,
        command: str,
        description: str = None,
        priority: str = 'medium',
        timeout: int = 300
    ) -> str:
        """
        Add a slash command to the queue.

        Args:
            command: Slash command to execute
            description: Optional description
            priority: Task priority
            timeout: Command timeout in seconds

        Returns:
            Task ID
        """
        if not description:
            description = f"Execute slash command: {command}"

        return self.add_task(
            name=f"Slash: {command.split()[0]}",
            description=description,
            command=command,
            priority=priority,
            task_type=self.TYPE_SLASH_COMMAND,
            timeout=timeout,
            metadata={'original_command': command}
        )

    def start_sequential_execution(self, stop_on_error: bool = False) -> bool:
        """
        Start sequential execution of queued tasks.

        Args:
            stop_on_error: Whether to stop execution on first error

        Returns:
            True if execution started successfully
        """
        with self._execution_lock:
            if self._execution_thread and self._execution_thread.is_alive():
                print("Error: Execution is already running", file=sys.stderr)
                return False

            self._stop_execution.clear()
            self._execution_thread = threading.Thread(
                target=self._execute_sequential_tasks,
                args=(stop_on_error,),
                daemon=True
            )
            self._execution_thread.start()

            return True

    def stop_execution(self):
        """Stop sequential execution."""
        self._stop_execution.set()
        if self._execution_thread and self._execution_thread.is_alive():
            self._execution_thread.join(timeout=5)

    def _execute_sequential_tasks(self, stop_on_error: bool):
        """Execute tasks sequentially in background thread."""
        print("🚀 Starting sequential task execution...")

        while not self._stop_execution.is_set():
            # Get next task
            task = self.get_next_task()
            if not task:
                print("[OK] No more tasks in queue")
                break

            self._current_task = task['task_id']
            print(f"⚡ Executing task: {task['name']} (ID: {task['task_id']})")

            # Update status to running
            self.update_task_status(task['task_id'], self.STATUS_RUNNING)

            # Execute task based on type
            success = False
            result = None
            error = None
            execution_time = 0.0

            start_time = time.time()

            try:
                if task['task_type'] == self.TYPE_SLASH_COMMAND and task.get('command'):
                    # Execute slash command
                    success, result, error = self._execute_slash_command(task)
                else:
                    # For other task types, mark as completed
                    success = True
                    result = "Task marked as completed (no execution required)"

                execution_time = time.time() - start_time

            except Exception as e:
                success = False
                error = str(e)
                execution_time = time.time() - start_time

            # Update task status
            if success:
                self.update_task_status(
                    task['task_id'],
                    self.STATUS_COMPLETED,
                    result=result,
                    execution_time=execution_time
                )
                print(f"[OK] Task completed: {task['name']}")
            else:
                if task['current_retry'] < task['retry_count']:
                    self.update_task_status(
                        task['task_id'],
                        self.STATUS_RETRYING,
                        error=error,
                        execution_time=execution_time
                    )
                    print(f"⚠️ Task failed, retrying: {task['name']} ({error})")
                    time.sleep(2)  # Brief delay before retry
                    continue
                else:
                    self.update_task_status(
                        task['task_id'],
                        self.STATUS_FAILED,
                        error=error,
                        execution_time=execution_time
                    )
                    print(f"❌ Task failed: {task['name']} ({error})")

                    if stop_on_error:
                        print("🛑 Stopping execution due to error")
                        break

            self._current_task = None

        print("🏁 Sequential execution completed")

    def _execute_slash_command(self, task: Dict[str, Any]) -> tuple[bool, str, str]:
        """Execute a slash command task."""
        command = task['command']
        timeout = task.get('timeout', 300)

        try:
            # Execute command with timeout
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                return True, result.stdout, None
            else:
                error_msg = result.stderr or f"Command failed with exit code {result.returncode}"
                return False, result.stdout, error_msg

        except subprocess.TimeoutExpired:
            return False, None, f"Command timed out after {timeout} seconds"
        except Exception as e:
            return False, None, str(e)

    def get_execution_summary(self, limit: int = 20) -> Dict[str, Any]:
        """Get execution summary from recent tasks."""
        with self._lock:
            # Get recent completed and failed tasks
            recent_tasks = []
            for status in [self.STATUS_COMPLETED, self.STATUS_FAILED, self.STATUS_CANCELLED]:
                tasks = self.list_tasks(status, limit)
                recent_tasks.extend(tasks)

            # Sort by completion time
            recent_tasks.sort(key=lambda x: x.get('completed_at', ''), reverse=True)
            recent_tasks = recent_tasks[:limit]

            # Calculate summary metrics
            summary = {
                'recent_tasks': recent_tasks,
                'total_recent': len(recent_tasks),
                'completed_recent': len([t for t in recent_tasks if t['status'] == self.STATUS_COMPLETED]),
                'failed_recent': len([t for t in recent_tasks if t['status'] == self.STATUS_FAILED]),
                'average_execution_time': 0.0,
                'most_common_commands': self._get_most_common_commands(recent_tasks)
            }

            # Calculate average execution time
            exec_times = [t.get('execution_time', 0) for t in recent_tasks if t.get('execution_time')]
            if exec_times:
                summary['average_execution_time'] = sum(exec_times) / len(exec_times)

            return summary

    def _get_most_common_commands(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get most common commands from recent tasks."""
        command_counts = defaultdict(int)
        command_details = {}

        for task in tasks:
            if task.get('command'):
                cmd = task['command'].split()[0]  # Get first part of command
                command_counts[cmd] += 1
                if cmd not in command_details:
                    command_details[cmd] = {
                        'command': cmd,
                        'success_count': 0,
                        'failure_count': 0,
                        'total_time': 0.0
                    }

                if task['status'] == self.STATUS_COMPLETED:
                    command_details[cmd]['success_count'] += 1
                else:
                    command_details[cmd]['failure_count'] += 1

                if task.get('execution_time'):
                    command_details[cmd]['total_time'] += task['execution_time']

        # Calculate additional metrics and sort
        result = []
        for cmd, count in sorted(command_counts.items(), key=lambda x: x[1], reverse=True):
            details = command_details[cmd]
            details['usage_count'] = count
            details['success_rate'] = (details['success_count'] / count) * 100 if count > 0 else 0
            details['average_time'] = details['total_time'] / count if count > 0 else 0
            result.append(details)

        return result[:10]  # Top 10 commands


def main():
    """Command-line interface for enhanced task queue."""
    import argparse

    parser = argparse.ArgumentParser(description='Enhanced Task Queue System')
    parser.add_argument('--dir', default='.claude-patterns', help='Queue directory path')

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Add task actions
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('--name', required=True, help='Task name')
    add_parser.add_argument('--description', required=True, help='Task description')
    add_parser.add_argument('--command', help='Command to execute')
    add_parser.add_argument('--priority', default='medium', choices=['critical', 'high', 'medium', 'low'])
    add_parser.add_argument('--type', default='manual',
                           choices=['slash_command', 'autonomous', 'background', 'manual'])
    add_parser.add_argument('--timeout', type=int, default=300, help='Timeout in seconds')
    add_parser.add_argument('--retry', type=int, default=3, help='Retry count')

    # Slash command action
    slash_parser = subparsers.add_parser('slash', help='Add slash command to queue')
    slash_parser.add_argument('--command', required=True, help='Slash command to execute')
    slash_parser.add_argument('--description', help='Task description')
    slash_parser.add_argument('--priority', default='medium', choices=['critical', 'high', 'medium', 'low'])
    slash_parser.add_argument('--timeout', type=int, default=300, help='Timeout in seconds')

    # Execution actions
    exec_parser = subparsers.add_parser('execute', help='Execute queued tasks sequentially')
    exec_parser.add_argument('--stop-on-error', action='store_true', help='Stop on first error')
    exec_parser.add_argument('--background', action='store_true', help='Run in background')

    subparsers.add_parser('stop', help='Stop sequential execution')

    # Task management actions
    subparsers.add_parser('next', help='Get next pending task')
    subparsers.add_parser('status', help='Show queue status')
    subparsers.add_parser('stats', help='Show detailed statistics')
    subparsers.add_parser('summary', help='Show execution summary')

    # List tasks action
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--status', help='Filter by status')
    list_parser.add_argument('--limit', type=int, default=20, help='Number of tasks to show')

    # Task operations
    update_parser = subparsers.add_parser('update', help='Update task status')
    update_parser.add_argument('--task-id', required=True, help='Task ID')
    update_parser.add_argument('--status', required=True,
                              choices=['queued', 'running', 'completed', 'failed', 'cancelled', 'retrying'])
    update_parser.add_argument('--result', help='Task result')
    update_parser.add_argument('--error', help='Error message')

    cancel_parser = subparsers.add_parser('cancel', help='Cancel a task')
    cancel_parser.add_argument('--task-id', required=True, help='Task ID')

    retry_parser = subparsers.add_parser('retry', help='Retry a failed task')
    retry_parser.add_argument('--task-id', required=True, help='Task ID')

    # Get task action
    get_parser = subparsers.add_parser('get', help='Get specific task')
    get_parser.add_argument('--task-id', required=True, help='Task ID')

    # Cleanup action
    clear_parser = subparsers.add_parser('clear', help='Clear completed/failed tasks')
    clear_parser.add_argument('--older-than', type=int, default=24, help='Hours to keep tasks')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    queue = TaskQueue(args.dir)

    try:
        if args.action == 'add':
            task_id = queue.add_task(
                args.name, args.description, args.command,
                args.priority, args.type, timeout=args.timeout, retry_count=args.retry
            )
            print(f"[OK] Task added with ID: {task_id}")

        elif args.action == 'slash':
            task_id = queue.add_slash_command(args.command, args.description, args.priority, args.timeout)
            print(f"[OK] Slash command queued with ID: {task_id}")

        elif args.action == 'execute':
            if queue.start_sequential_execution(args.stop_on_error):
                if args.background:
                    print("🚀 Sequential execution started in background")
                else:
                    print("🚀 Sequential execution started... (Ctrl+C to stop)")
                    try:
                        # Wait for execution to complete or be interrupted
                        while queue._execution_thread and queue._execution_thread.is_alive():
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\n🛑 Stopping execution...")
                        queue.stop_execution()
            else:
                print("❌ Failed to start execution")
                sys.exit(1)

        elif args.action == 'stop':
            queue.stop_execution()
            print("🛑 Execution stopped")

        elif args.action == 'next':
            task = queue.get_next_task()
            if task:
                print(json.dumps(task, indent=2))
            else:
                print("No pending tasks available")

        elif args.action == 'status':
            status = queue.get_status()
            print(json.dumps(status, indent=2))

        elif args.action == 'stats':
            stats = queue.get_statistics()
            print(json.dumps(stats, indent=2))

        elif args.action == 'summary':
            summary = queue.get_execution_summary()
            print(json.dumps(summary, indent=2))

        elif args.action == 'list':
            tasks = queue.list_tasks(args.status, args.limit)
            print(json.dumps(tasks, indent=2))

        elif args.action == 'update':
            success = queue.update_task_status(
                args.task_id, args.status, result=args.result, error=args.error
            )
            print(f"[OK] Task {'updated' if success else 'not found'}")

        elif args.action == 'cancel':
            success = queue.cancel_task(args.task_id)
            print(f"[OK] Task {'cancelled' if success else 'not found'}")

        elif args.action == 'retry':
            success = queue.retry_task(args.task_id)
            print(f"[OK] Task {'retry queued' if success else 'not found or not failed'}")

        elif args.action == 'get':
            task = queue.get_task(args.task_id)
            if task:
                print(json.dumps(task, indent=2))
            else:
                print(f"Task '{args.task_id}' not found")
                sys.exit(1)

        elif args.action == 'clear':
            removed = queue.clear_completed(args.older_than)
            print(f"[OK] Removed {removed} completed/failed tasks")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()