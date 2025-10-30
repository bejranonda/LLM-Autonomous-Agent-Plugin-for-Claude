#!/usr/bin/env python3
"""
Task Queue System for Autonomous Claude Agent Plugin (Minimal Working Version)
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class TaskQueue:
    """Manages task queue with priority-based execution."""

    # Priority levels
    PRIORITY_HIGH = 3
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 1

    # Status constants
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'

    def __init__(self, queue_dir: str = ".claude-patterns"):
        """Initialize task queue."""
        self.queue_dir = Path(queue_dir)
        self.queue_file = self.queue_dir / "task_queue.json"
        self._ensure_directory()

    def _ensure_directory(self):
        """Create queue directory if it doesn't exist."""
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        if not self.queue_file.exists():
            self._write_queue([])

    def _read_queue(self) -> List[Dict[str, Any]]:
        """Read task queue from JSON file."""
        try:
            if self.queue_file.exists():
                with open(self.queue_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception:
            return []

    def _write_queue(self, queue: List[Dict[str, Any]]):
        """Write task queue to JSON file."""
        try:
            with open(self.queue_file, 'w', encoding='utf-8') as f:
                json.dump(queue, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing queue: {e}", file=sys.stderr)

    def add_task(self, name: str, description: str = "", command: str = "",
                 priority: str = "medium", task_type: str = "general") -> str:
        """Add a new task to the queue."""
        # Convert priority string to number
        priority_map = {
            'low': self.PRIORITY_LOW,
            'medium': self.PRIORITY_MEDIUM,
            'high': self.PRIORITY_HIGH
        }
        priority_num = priority_map.get(priority.lower(), self.PRIORITY_MEDIUM)

        task = {
            'id': len(self._read_queue()) + 1,
            'name': name,
            'description': description,
            'command': command,
            'task_type': task_type,
            'priority': priority_num,
            'priority_str': priority,
            'status': self.STATUS_PENDING,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        queue = self._read_queue()
        queue.append(task)
        self._write_queue(queue)
        return str(task['id'])

    def get_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks in the queue."""
        return self._read_queue()

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID."""
        queue = self._read_queue()
        for task in queue:
            if str(task['id']) == task_id:
                return task
        return None

    def update_task_status(self, task_id: str, status: str) -> bool:
        """Update the status of a task."""
        queue = self._read_queue()
        for task in queue:
            if str(task['id']) == task_id:
                task['status'] = status
                task['updated_at'] = datetime.now().isoformat()
                self._write_queue(queue)
                return True
        return False

    def complete_task(self, task_id: str, result: str = "") -> bool:
        """Mark a task as completed."""
        queue = self._read_queue()
        for task in queue:
            if str(task['id']) == task_id:
                task['status'] = self.STATUS_COMPLETED
                task['result'] = result
                task['updated_at'] = datetime.now().isoformat()
                self._write_queue(queue)
                return True
        return False

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Get the next highest priority task."""
        queue = self._read_queue()
        # Filter for pending tasks and sort by priority (high to low)
        pending_tasks = [task for task in queue if task['status'] == self.STATUS_PENDING]
        if not pending_tasks:
            return None

        # Sort by priority (high to low), then by creation time
        pending_tasks.sort(key=lambda x: (-x['priority'], x['created_at']))
        return pending_tasks[0]

def main():
    """CLI interface for task queue."""
    parser = argparse.ArgumentParser(description='Task Queue Management')
    parser.add_argument('action', choices=['status'], help='Action to perform')
    parser.add_argument('--dir', default='.claude-patterns', help='Queue directory')

    args = parser.parse_args()
    queue = TaskQueue(args.dir)

    if args.action == 'status':
        tasks = queue._read_queue()
        print(f"Tasks in queue: {len(tasks)}")
        for task in tasks:
            print(f"  - {task.get('name', 'Unknown')} [{task.get('status', 'Unknown')}]")

if __name__ == '__main__':
    main()
