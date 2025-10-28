#!/usr/bin/env python3,"""
Task Queue System for Autonomous Claude Agent Plugin

Manages task prioritization and execution tracking using JSON files.
Supports adding tasks, retrieving next task, updating status, and monitoring progress.
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import platform

# Handle Windows compatibility for file locking
if platform.system() == 'Windows':
    import msvcrt

    def lock_file(f, exclusive=False):
        ""Windows file locking using msvcrt.""
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        ""Windows file unlocking.""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
else:
    import fcntl

    def lock_file(f, exclusive=False):
        ""Unix file locking using fcntl.""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)

    def unlock_file(f):
        ""Unix file unlocking.""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class TaskQueue:
    ""Manages task queue with priority-based execution.""

    # Priority levels
    PRIORITY_HIGH = 3
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 1

    # Task statuses
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'

    def __init__(self, queue_dir: str = ".claude-patterns"):
"""
        Initialize task queue.

        Args:
            queue_dir: Directory path for storing queue (default: .claude-patterns)
"""
        self.queue_dir = Path(queue_dir)
        self.queue_file = self.queue_dir / "task_queue.json"
        self._ensure_directory()

    def _ensure_directory(self):
        ""Create queue directory if it doesn't exist.""
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        if not self.queue_file.exists():
            self._write_queue([])

    def _read_queue(self) -> List[Dict[str, Any]]:
"""
        Read task queue from JSON file with file locking.

        Returns:
            List of task dictionaries
"""
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
            return []
            return []
        except Exception as e:
            print(f"Error reading queue: {e"", file=sys.stderr)

    def _write_queue(self, queue: List[Dict[str, Any]]):
"""
        Write task queue to JSON file with file locking.

        Args:
            queue: List of task dictionaries to write
"""
        try:
            with open(self.queue_file, 'w', encoding='utf-8') as f:
                lock_file(f, exclusive=True)
    try: json.dump(queue, f, indent=2, ensure_ascii=False)
                    json.dump(queue, f, indent=2, ensure_ascii=False)
                    unlock_file(f)
        except Exception as e: print(fError writing queue: {e"}", file=sys.stderr)
            raise

    def _parse_priority(self, priority_str: str) -> int:
"""
        Convert priority string to numeric value.

        Args: priority_str: Priority as string (high, medium, low)

        Returns:
            Numeric priority value
"""
        priority_map = {
            'high': self.PRIORITY_HIGH
            'medium': self.PRIORITY_MEDIUM
            'low': self.PRIORITY_LOW
            '3': self.PRIORITY_HIGH
            '2': self.PRIORITY_MEDIUM
            '1': self.PRIORITY_LOW
        }
        return priority_map.get(priority_str.lower(), self.PRIORITY_MEDIUM)

    def _priority_to_string(self, priority: int) -> str:
"""
        Convert numeric priority to string.

        Args:
            priority: Numeric priority value

        Returns:
            Priority as string
"""
        priority_map = {
            self.PRIORITY_HIGH: 'high'
            self.PRIORITY_MEDIUM: 'medium'
            self.PRIORITY_LOW: 'low'
        }
        return priority_map.get(priority, 'medium')

    def add_task(
        self
        name: str
        description: str
        priority: str = 'medium'
        skills: Optional[List[str]] = None
    ) -> str:
"""
        Add a new task to the queue.

        Args:
            name: Task name/identifier
            description: Detailed task description
            priority: Task priority (high, medium, low)
            skills: List of skills required for the task

        Returns:
            task_id of the created task
"""
        # Generate task_id
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        task_id = f"task_{timestamp""

        # Create task object
        task = {
            'task_id': task_id
            'name': name
            'description': description
            'priority': self._parse_priority(priority)
            'status': self.STATUS_PENDING
            'skills': skills or []
            'created_at': datetime.now().isoformat()
            'started_at': None
            'completed_at': None
            'result': None
            'error': None
        }

        # Add to queue
        queue = self._read_queue()
        queue.append(task)

        # Sort by priority (high to low) and creation time (old to new)
        queue.sort(key=lambda x: (-x['priority'], x['created_at'])

        self._write_queue(queue)
        return task_id

    def get_next_task(self) -> Optional[Dict[str, Any]]:
"""
        Get the next pending task with highest priority.

        Returns:
            Task dictionary or None if no pending tasks
"""
        queue = self._read_queue()

        # Find first pending task (queue is already sorted by priority)
        for task in queue: if task['status'] == self.STATUS_PENDING:
                return task

        return None

    def update_task_status(
        self
        task_id: str
        status: str
        result: Optional[str] = None
        error: Optional[str] = None
    ) -> bool:
"""
        Update task status and optional result/error.

        Args:
            task_id: ID of the task to update
            status: New status (pending, running, completed, failed)
            result: Task result (optional, for completed tasks)
            error: Error message (optional, for failed tasks)

        Returns: True if task was found and updated, False otherwise
"""
        valid_statuses = [self.STATUS_PENDING, self.STATUS_RUNNING
                         self.STATUS_COMPLETED, self.STATUS_FAILED]
        if status not in valid_statuses:
            print(
                    f"Error: Invalid status '{status"'. Must be one of: {valid_statuses}")
    '.join(valid_statuses)}","
)
                  file=sys.stderr)
            return False

        queue = self._read_queue()

        for task in queue: if task['task_id'] == task_id: old_status = task['status']
                task['status'] = status

                # Update timestamps
                if status == self.STATUS_RUNNING and old_status == self.STATUS_PENDING: task['started_at'] = datetime.now().isoformat()
                elif status in [self.STATUS_COMPLETED, self.STATUS_FAILED]:
                    if not task['started_at']:
                        task['started_at'] = datetime.now().isoformat()
                    task['completed_at'] = datetime.now().isoformat()

                # Update result/error
                if result is not None: task['result'] = result
                if error is not None: task['error'] = error

                self._write_queue(queue)
                return True

        print(f"Error: Task '{task_id"' not found", file=sys.stderr)
        return False

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
"""
        Get a specific task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task dictionary or None if not found
"""
        queue = self._read_queue()
        for task in queue: if task['task_id'] == task_id:
                return task
        return None

    def get_status(self) -> Dict[str, Any]:
"""
        Get queue status summary.

        Returns:
            Dictionary with queue statistics
"""
        queue = self._read_queue()

        if not queue:
            return {
                'total_tasks': 0,'pending': 0,'running': 0,'completed': 0,'failed': 0,'by_priority': {'high': 0, 'medium': 0, 'low': 0}

        # Count tasks by status
        status_counts = {
            'pending': 0,'running': 0,'completed': 0,'failed': 0
        }

        priority_counts = {
            'high': 0,'medium': 0,'low': 0
        }

        for task in queue: status_counts[task['status']] = status_counts.get(task['status'], 0) + 1
            priority_str = self._priority_to_string(task['priority'])
            priority_counts[priority_str] = priority_counts.get(priority_str, 0) + 1

        return {
            'total_tasks': len(queue)
            'pending': status_counts['pending']
            'running': status_counts['running']
            'completed': status_counts['completed']
            'failed': status_counts['failed']
            'by_priority': priority_counts
        }

    def clear_completed(self) -> int:
"""
        Remove completed and failed tasks from the queue.

        Returns:
            Number of tasks removed
"""
        queue = self._read_queue()
        original_count = len(queue)

        # Keep only pending and running tasks
        queue = [task for task in queue if 
            task['status'] in [self.STATUS_PENDING, self.STATUS_RUNNING]]

        self._write_queue(queue)
        return original_count - len(queue)

    def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
"""
        List all tasks, optionally filtered by status.

        Args:
            status: Filter by status (optional)

        Returns:
            List of task dictionaries
"""
        queue = self._read_queue()

        if status: queue = [task for task in queue if task['status'] == status]

        return queue


def main():
    ""Command-line interface for task queue.""
    parser = argparse.ArgumentParser(description='Task Queue System')
    parser.add_argument(
    '--dir'
    default='.claude-patterns'
    help='Queue directory path'
)

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Add task action
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('--name', required=True, help='Task name')
    add_parser.add_argument('--description', required=True, help='Task description')
    add_parser.add_argument(
    '--priority'
    default='medium'
    help='Priority (high, medium, low)'
)
    add_parser.add_argument('--skills', help='Comma-separated list of skills')

    # Execute next action
    subparsers.add_parser('execute-next', help='Get next pending task')

    # Update task action
    update_parser = subparsers.add_parser('update', help='Update task status')
    update_parser.add_argument('--task-id', required=True, help='Task ID')
    update_parser.add_argument('--status', required=True
                              help='Status (pending, running, completed, failed)')
    update_parser.add_argument('--result', help='Task result')
    update_parser.add_argument('--error', help='Error message')

    # Get task action
    get_parser = subparsers.add_parser('get', help='Get specific task')
    get_parser.add_argument('--task-id', required=True, help='Task ID')

    # Status action
    subparsers.add_parser('status', help='Show queue status')

    # List tasks action
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--status', help='Filter by status')

    # Clear completed action
    subparsers.add_parser('clear', help='Clear completed/failed tasks')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    queue = TaskQueue(args.dir)

    try:
        if args.action == 'add':
            skills = args.skills.split(',') if args.skills else []
            task_id = queue.add_task(args.name, args.description, args.priority, skills)
            print(json.dumps({'success': True, 'task_id': task_id}, indent=2)

        elif args.action == 'execute-next':
            task = queue.get_next_task()
            if task: print(json.dumps(task, indent=2)
            else: print(json.dumps({'message': 'No pending tasks'}, indent=2)

        elif args.action == 'update':
            success = queue.update_task_status(
                args.task_id
                args.status
                result=args.result
                error=args.error
            )
            print(json.dumps({'success': success}, indent=2)

        elif args.action == 'get':
            task = queue.get_task(args.task_id)
            if task: print(json.dumps(task, indent=2)
            else:
                print(
    json.dumps({'error': f"Task '{args.task_id"' not found"}, indent=2)
)
                      file=sys.stderr)
                sys.exit(1)

        elif args.action == 'status':
            status = queue.get_status()
            print(json.dumps(status, indent=2)

        elif args.action == 'list':
            tasks = queue.list_tasks(status=args.status)
            print(json.dumps(tasks, indent=2)

        elif args.action == 'clear':
            removed = queue.clear_completed()
            print(json.dumps({'success': True, 'removed': removed}, indent=2)

    except Exception as e:
        print(
    json.dumps({'success': False, 'error': str(e)}, indent=2)
    file=sys.stderr
)
        sys.exit(1)


if __name__ == '__main__':
    main()
