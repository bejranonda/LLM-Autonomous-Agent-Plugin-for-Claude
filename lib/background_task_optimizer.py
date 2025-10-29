#!/usr/bin/env python3
"""
Background Task Optimization and Scaling System

Intelligent task scheduling, resource optimization, and parallel execution
for maximum autonomous agent system efficiency.
"""

import json
import os
import sys
import time
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Callable
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import queue

@dataclass
class Task:
    """Background task representation"""
    id: str
    name: str
    command: str
    priority: int  # 1-10, 10 is highest
    complexity: str  # simple, medium, complex, expert
    estimated_duration: int
    dependencies: List[str]
    skills_required: List[str]
    agents_involved: List[str]
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Dict] = None
    error: Optional[str] = None
    resource_usage: Optional[Dict] = None

@dataclass
class ResourceMetrics:
    """System resource metrics"""
    cpu_usage: float
    memory_usage: float
    active_tasks: int
    available_workers: int
    system_load: float
    last_updated: datetime

class BackgroundTaskOptimizer:
    """Advanced background task optimization system"""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        self.patterns_dir = patterns_dir
        self.config_file = os.path.join(patterns_dir, "task_optimizer_config.json")
        self.metrics_file = os.path.join(patterns_dir, "task_metrics.json")
        self.performance_file = os.path.join(patterns_dir, "task_performance_history.json")

        # Task management
        self.task_queue = queue.PriorityQueue()
        self.running_tasks = {}
        self.completed_tasks = deque(maxlen=1000)
        self.failed_tasks = deque(maxlen=500)

        # Execution pools
        self.thread_pool = None
        self.process_pool = None
        self.max_workers = self._detect_optimal_workers()

        # Resource monitoring
        self.resource_metrics = ResourceMetrics(0, 0, 0, self.max_workers, 0, datetime.now())
        self.monitoring_active = False

        # Performance learning
        self.performance_history = self._load_performance_history()
        self.task_patterns = defaultdict(list)

        # Configuration
        self.config = self._load_config()

    def _detect_optimal_workers(self) -> int:
        """Detect optimal number of workers based on system"""
        try:
            import psutil
            cpu_count = psutil.cpu_count(logical=False) or 4
            memory_gb = psutil.virtual_memory().total / (1024**3)

            # Conservative estimate: use 70% of CPU cores, adjust for memory
            optimal_workers = min(
                max(cpu_count // 2, 2),
                int(memory_gb // 2),  # 2GB per worker minimum
                8  # Cap at 8 workers to avoid overwhelming system
            )
            return optimal_workers
        except ImportError:
            # Fallback if psutil not available
            return min(4, os.cpu_count() or 2)

    def _load_config(self) -> Dict:
        """Load or create default configuration"""
        default_config = {
            "max_concurrent_tasks": self.max_workers,
            "priority_weights": {
                "urgent": 10,
                "high": 8,
                "medium": 5,
                "low": 2,
                "background": 1
            },
            "complexity_multipliers": {
                "simple": 1.0,
                "medium": 1.5,
                "complex": 2.0,
                "expert": 3.0
            },
            "resource_thresholds": {
                "max_cpu_usage": 80.0,
                "max_memory_usage": 85.0,
                "max_system_load": 2.0
            },
            "auto_scaling": {
                "enabled": True,
                "scale_up_threshold": 90,
                "scale_down_threshold": 30,
                "min_workers": 2,
                "max_workers": 16
            },
            "learning": {
                "enabled": True,
                "pattern_recognition": True,
                "performance_tracking": True,
                "adaptive_scheduling": True
            }
        }

        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in default_config.items():
                    if key not in loaded_config:
                        loaded_config[key] = value
                return loaded_config
        except Exception:
            pass

        return default_config

    def _save_config(self):
        """Save current configuration"""
        os.makedirs(self.patterns_dir, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def _load_performance_history(self) -> Dict:
        """Load historical performance data"""
        try:
            with open(self.performance_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"task_history": [], "performance_patterns": {}, "optimization_results": []}

    def _save_performance_history(self):
        """Save performance history"""
        os.makedirs(self.patterns_dir, exist_ok=True)
        with open(self.performance_file, 'w', encoding='utf-8') as f:
            json.dump(self.performance_history, f, indent=2, ensure_ascii=False)

    def estimate_task_duration(self, task_name: str, complexity: str,
                             command: str) -> int:
        """Estimate task duration based on historical patterns"""
        # Base duration by complexity
        base_durations = {
            "simple": 30,
            "medium": 120,
            "complex": 300,
            "expert": 600
        }

        base_duration = base_durations.get(complexity, 120)

        # Look for similar tasks in performance history
        similar_tasks = []
        for history_task in self.performance_history.get("task_history", []):
            if (history_task.get("complexity") == complexity and
                any(keyword in history_task.get("name", "").lower()
                    for keyword in task_name.lower().split())):
                similar_tasks.append(history_task.get("actual_duration", base_duration))

        if similar_tasks:
            # Use weighted average of similar tasks
            recent_tasks = similar_tasks[-10:]  # Last 10 similar tasks
            if recent_tasks:
                return int(sum(recent_tasks) / len(recent_tasks))

        # Adjust based on command complexity
        command_indicators = {
            "python": 1.0,
            "git": 0.5,
            "npm": 1.5,
            "docker": 2.0,
            "make": 1.2,
            "pytest": 1.8,
            "coverage": 2.5
        }

        for tool, multiplier in command_indicators.items():
            if tool in command.lower():
                base_duration *= multiplier
                break

        return int(base_duration)

    def calculate_task_priority(self, task: Task) -> int:
        """Calculate dynamic task priority based on multiple factors"""
        base_priority = task.priority

        # Time-based priority boost
        wait_time = (datetime.now() - task.created_at).total_seconds()
        if wait_time > 300:  # 5 minutes
            base_priority += 2
        elif wait_time > 900:  # 15 minutes
            base_priority += 4

        # Dependency-based priority
        if task.dependencies:
            # Higher priority if other tasks depend on this one
            dependent_count = len([t for t in self.task_queue.queue
                                 if task.id in getattr(t[1], 'dependencies', [])])
            base_priority += min(dependent_count, 3)

        # Resource availability adjustment
        if self.resource_metrics.cpu_usage > 70:
            # Prefer lighter tasks when CPU is busy
            if task.complexity == "simple":
                base_priority += 1
            elif task.complexity == "expert":
                base_priority -= 1

        # Historical performance adjustment
        task_type = task.name.split()[0]  # Simple classification
        if task_type in self.task_patterns:
            avg_success_rate = sum(1 for t in self.task_patterns[task_type] if t.get("success", False)) / len(self.task_patterns[task_type])
            if avg_success_rate > 0.9:
                base_priority += 1  # Boost historically successful tasks

        return max(1, min(10, base_priority))

    def add_task(self, name: str, command: str, priority: int = 5,
                complexity: str = "medium", dependencies: List[str] = None,
                skills_required: List[str] = None, agents_involved: List[str] = None) -> str:
        """Add a new background task"""
        task_id = f"task_{int(time.time())}_{len(self.task_queue.queue)}"

        # Estimate duration
        estimated_duration = self.estimate_task_duration(name, complexity, command)

        task = Task(
            id=task_id,
            name=name,
            command=command,
            priority=priority,
            complexity=complexity,
            estimated_duration=estimated_duration,
            dependencies=dependencies or [],
            skills_required=skills_required or [],
            agents_involved=agents_involved or [],
            created_at=datetime.now()
        )

        # Add to queue with calculated priority
        calculated_priority = self.calculate_task_priority(task)
        self.task_queue.put((-calculated_priority, task))  # Negative for max-heap behavior

        print(f"Task added: {name} (ID: {task_id}, Priority: {calculated_priority}, Est. Duration: {estimated_duration}s)")
        return task_id

    def start_optimization(self) -> Dict:
        """Start the background task optimization system"""
        print("Starting Background Task Optimization System...")
        print(f"Max Workers: {self.max_workers}")
        print(f"Auto-Scaling: {self.config['auto_scaling']['enabled']}")

        # Initialize execution pools
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=min(4, self.max_workers))

        # Start monitoring
        self.monitoring_active = True
        monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        monitor_thread.start()

        # Start task scheduler
        scheduler_thread = threading.Thread(target=self._task_scheduler, daemon=True)
        scheduler_thread.start()

        return {
            "status": "started",
            "max_workers": self.max_workers,
            "auto_scaling_enabled": self.config["auto_scaling"]["enabled"],
            "monitoring_active": self.monitoring_active
        }

    def _monitor_resources(self):
        """Monitor system resources continuously"""
        while self.monitoring_active:
            try:
                import psutil

                self.resource_metrics.cpu_usage = psutil.cpu_percent(interval=1)
                self.resource_metrics.memory_usage = psutil.virtual_memory().percent
                self.resource_metrics.system_load = os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
                self.resource_metrics.active_tasks = len(self.running_tasks)
                self.resource_metrics.available_workers = self.max_workers - len(self.running_tasks)
                self.resource_metrics.last_updated = datetime.now()

                # Auto-scaling check
                if self.config["auto_scaling"]["enabled"]:
                    self._check_auto_scaling()

                # Save metrics periodically
                if int(time.time()) % 60 == 0:  # Every minute
                    self._save_metrics()

            except Exception as e:
                print(f"Resource monitoring error: {e}")

            time.sleep(5)  # Check every 5 seconds

    def _check_auto_scaling(self):
        """Check if auto-scaling is needed"""
        cpu_usage = self.resource_metrics.cpu_usage
        active_tasks = len(self.running_tasks)

        scale_up_threshold = self.config["auto_scaling"]["scale_up_threshold"]
        scale_down_threshold = self.config["auto_scaling"]["scale_down_threshold"]
        min_workers = self.config["auto_scaling"]["min_workers"]
        max_workers = self.config["auto_scaling"]["max_workers"]

        # Scale up if CPU usage is high and we're at max capacity
        if cpu_usage > scale_up_threshold and active_tasks >= self.max_workers:
            if self.max_workers < max_workers:
                self._scale_up_workers()

        # Scale down if CPU usage is low and we have idle capacity
        elif cpu_usage < scale_down_threshold and active_tasks < self.max_workers // 2:
            if self.max_workers > min_workers:
                self._scale_down_workers()

    def _scale_up_workers(self):
        """Scale up worker count"""
        old_max = self.max_workers
        self.max_workers = min(self.max_workers + 2, self.config["auto_scaling"]["max_workers"])

        print(f"Scaling up workers: {old_max} -> {self.max_workers}")

        # Recreate thread pool with new size
        if self.thread_pool:
            self.thread_pool.shutdown(wait=False)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)

    def _scale_down_workers(self):
        """Scale down worker count"""
        old_max = self.max_workers
        self.max_workers = max(self.max_workers - 1, self.config["auto_scaling"]["min_workers"])

        print(f"Scaling down workers: {old_max} -> {self.max_workers}")

        # Recreate thread pool with new size
        if self.thread_pool:
            self.thread_pool.shutdown(wait=False)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)

    def _task_scheduler(self):
        """Main task scheduler loop"""
        while self.monitoring_active or not self.task_queue.empty():
            try:
                # Check if we can execute more tasks
                if len(self.running_tasks) < self.max_workers:
                    # Check resource availability
                    if self._check_resource_availability():
                        try:
                            # Get next task (timeout to allow checking conditions)
                            priority, task = self.task_queue.get(timeout=1)

                            # Check dependencies
                            if self._check_dependencies(task):
                                # Execute task
                                self._execute_task(task)
                            else:
                                # Put task back if dependencies not met
                                self.task_queue.put((priority, task))

                        except queue.Empty:
                            continue
                    else:
                        # Resources not available, wait
                        time.sleep(2)
                else:
                    # At capacity, wait
                    time.sleep(1)

            except Exception as e:
                print(f"Scheduler error: {e}")
                time.sleep(5)

    def _check_resource_availability(self) -> bool:
        """Check if system resources are available for new tasks"""
        thresholds = self.config["resource_thresholds"]

        return (
            self.resource_metrics.cpu_usage < thresholds["max_cpu_usage"] and
            self.resource_metrics.memory_usage < thresholds["max_memory_usage"] and
            self.resource_metrics.system_load < thresholds["max_system_load"]
        )

    def _check_dependencies(self, task: Task) -> bool:
        """Check if task dependencies are satisfied"""
        for dep_id in task.dependencies:
            if dep_id not in [t.id for t in self.completed_tasks]:
                return False
        return True

    def _execute_task(self, task: Task):
        """Execute a single task"""
        task.status = "running"
        task.started_at = datetime.now()
        self.running_tasks[task.id] = task

        print(f"Executing task: {task.name} (ID: {task.id})")

        # Submit to thread pool
        future = self.thread_pool.submit(self._run_task_command, task)
        future.add_done_callback(lambda f: self._task_completed(task, f))

    def _run_task_command(self, task: Task) -> Dict:
        """Run the actual task command"""
        start_time = time.time()

        try:
            # Execute command
            result = subprocess.run(
                task.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=task.estimated_duration * 2  # Double the estimate
            )

            duration = time.time() - start_time

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "duration": duration,
                "resource_usage": {
                    "peak_memory": 0,  # Would need psutil for accurate tracking
                    "cpu_time": duration
                }
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Task timed out",
                "duration": time.time() - start_time
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "duration": time.time() - start_time
            }

    def _task_completed(self, task: Task, future):
        """Handle task completion"""
        try:
            result = future.result()
            task.result = result
            task.status = "completed" if result["success"] else "failed"
            task.completed_at = datetime.now()

            # Calculate actual duration
            actual_duration = (task.completed_at - task.started_at).total_seconds()

            # Update performance history
            self._update_performance_history(task, result, actual_duration)

            # Update patterns
            task_type = task.name.split()[0]
            self.task_patterns[task_type].append({
                "success": result["success"],
                "duration": actual_duration,
                "estimated_duration": task.estimated_duration,
                "accuracy": abs(actual_duration - task.estimated_duration) / task.estimated_duration
            })

            # Move to appropriate list
            if result["success"]:
                self.completed_tasks.append(task)
                print(f"Task completed: {task.name} (Duration: {actual_duration:.1f}s)")
            else:
                self.failed_tasks.append(task)
                print(f"Task failed: {task.name} (Error: {result.get('error', 'Unknown error')})")

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            task.completed_at = datetime.now()
            self.failed_tasks.append(task)
            print(f"Task failed with exception: {task.name} (Error: {e})")

        finally:
            # Remove from running tasks
            if task.id in self.running_tasks:
                del self.running_tasks[task.id]

    def _update_performance_history(self, task: Task, result: Dict, actual_duration: float):
        """Update performance history with task results"""
        history_entry = {
            "task_id": task.id,
            "name": task.name,
            "complexity": task.complexity,
            "priority": task.priority,
            "estimated_duration": task.estimated_duration,
            "actual_duration": actual_duration,
            "success": result["success"],
            "timestamp": datetime.now().isoformat(),
            "accuracy": abs(actual_duration - task.estimated_duration) / task.estimated_duration,
            "resource_efficiency": 1.0  # Placeholder
        }

        self.performance_history["task_history"].append(history_entry)

        # Keep only recent history (last 1000 tasks)
        if len(self.performance_history["task_history"]) > 1000:
            self.performance_history["task_history"] = self.performance_history["task_history"][-1000:]

        # Update patterns periodically
        if len(self.performance_history["task_history"]) % 50 == 0:
            self._update_performance_patterns()

        # Save periodically
        if len(self.performance_history["task_history"]) % 10 == 0:
            self._save_performance_history()

    def _update_performance_patterns(self):
        """Update performance patterns based on history"""
        history = self.performance_history["task_history"]

        # Analyze by complexity
        complexity_stats = defaultdict(list)
        for entry in history[-100:]:  # Last 100 tasks
            complexity_stats[entry["complexity"]].append(entry)

        patterns = {}
        for complexity, tasks in complexity_stats.items():
            if tasks:
                patterns[complexity] = {
                    "avg_duration": sum(t["actual_duration"] for t in tasks) / len(tasks),
                    "success_rate": sum(1 for t in tasks if t["success"]) / len(tasks),
                    "avg_accuracy": sum(t["accuracy"] for t in tasks) / len(tasks),
                    "sample_size": len(tasks)
                }

        self.performance_history["performance_patterns"] = patterns

    def _save_metrics(self):
        """Save current metrics"""
        metrics_data = {
            "resource_metrics": asdict(self.resource_metrics),
            "queue_size": self.task_queue.qsize(),
            "running_tasks": len(self.running_tasks),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "max_workers": self.max_workers,
            "timestamp": datetime.now().isoformat()
        }

        os.makedirs(self.patterns_dir, exist_ok=True)
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, ensure_ascii=False)

    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        return {
            "resource_metrics": asdict(self.resource_metrics),
            "task_queue": {
                "size": self.task_queue.qsize(),
                "running": len(self.running_tasks),
                "completed": len(self.completed_tasks),
                "failed": len(self.failed_tasks)
            },
            "performance": {
                "total_tasks_processed": len(self.completed_tasks) + len(self.failed_tasks),
                "success_rate": len(self.completed_tasks) / max(len(self.completed_tasks) + len(self.failed_tasks), 1),
                "avg_duration": sum(t.result.get("duration", 0) for t in self.completed_tasks) / max(len(self.completed_tasks), 1),
                "patterns_analyzed": len(self.task_patterns)
            },
            "configuration": self.config,
            "auto_scaling": {
                "enabled": self.config["auto_scaling"]["enabled"],
                "current_workers": self.max_workers,
                "min_workers": self.config["auto_scaling"]["min_workers"],
                "max_workers": self.config["auto_scaling"]["max_workers"]
            }
        }

    def optimize_workload_distribution(self) -> Dict:
        """Intelligently optimize workload distribution"""
        print("Analyzing workload distribution for optimization...")

        # Analyze current patterns
        complexity_distribution = defaultdict(int)
        for task in list(self.task_queue.queue):
            task_obj = task[1]
            complexity_distribution[task_obj.complexity] += 1

        # Analyze resource utilization
        cpu_utilization = self.resource_metrics.cpu_usage
        memory_utilization = self.resource_metrics.memory_usage

        # Generate optimization recommendations
        recommendations = []

        if cpu_utilization > 80:
            recommendations.append({
                "type": "resource",
                "priority": "high",
                "action": "Reduce concurrent tasks or scale up resources",
                "impact": "Improve task completion time by 15-25%"
            })

        if len(self.task_queue.queue) > 50:
            recommendations.append({
                "type": "queue",
                "priority": "medium",
                "action": "Increase worker count or prioritize urgent tasks",
                "impact": "Reduce wait times for high-priority tasks"
            })

        # Analyze task duration accuracy
        if self.performance_history["task_history"]:
            recent_tasks = self.performance_history["task_history"][-20:]
            avg_accuracy = sum(t["accuracy"] for t in recent_tasks) / len(recent_tasks)

            if avg_accuracy > 0.3:  # 30% inaccuracy threshold
                recommendations.append({
                    "type": "estimation",
                    "priority": "medium",
                    "action": "Improve duration estimation using recent patterns",
                    "impact": "Better resource planning and scheduling"
                })

        return {
            "status": "analyzed",
            "complexity_distribution": dict(complexity_distribution),
            "resource_utilization": {
                "cpu": cpu_utilization,
                "memory": memory_utilization
            },
            "recommendations": recommendations,
            "optimization_potential": len(recommendations)
        }

    def stop_optimization(self):
        """Stop the optimization system"""
        print("Stopping Background Task Optimization System...")

        self.monitoring_active = False

        if self.thread_pool:
            self.thread_pool.shutdown(wait=True)
        if self.process_pool:
            self.process_pool.shutdown(wait=True)

        # Save final metrics
        self._save_metrics()
        self._save_performance_history()

        print("Background Task Optimization System stopped.")


def main():
    """CLI interface for background task optimizer"""
    import argparse

    parser = argparse.ArgumentParser(description="Background Task Optimization System")
    parser.add_argument("--dir", default=".claude-patterns", help="Patterns directory")
    parser.add_argument("--start", action="store_true", help="Start optimization system")
    parser.add_argument("--stop", action="store_true", help="Stop optimization system")
    parser.add_argument("--status", action="store_true", help="Get system status")
    parser.add_argument("--add-task", nargs=3, metavar=("NAME", "COMMAND", "PRIORITY"),
                       help="Add a task (name command priority)")
    parser.add_argument("--optimize", action="store_true", help="Run workload optimization")

    args = parser.parse_args()

    optimizer = BackgroundTaskOptimizer(args.dir)

    if args.start:
        result = optimizer.start_optimization()
        print(f"Optimization system started: {result['status']}")

        # Keep running
        try:
            while True:
                time.sleep(10)
                status = optimizer.get_system_status()
                print(f"Active tasks: {status['task_queue']['running']}, Queue: {status['task_queue']['size']}")
        except KeyboardInterrupt:
            optimizer.stop_optimization()

    elif args.stop:
        optimizer.stop_optimization()

    elif args.status:
        status = optimizer.get_system_status()
        print(f"\nSystem Status:")
        print(f"  CPU Usage: {status['resource_metrics']['cpu_usage']:.1f}%")
        print(f"  Memory Usage: {status['resource_metrics']['memory_usage']:.1f}%")
        print(f"  Active Tasks: {status['task_queue']['running']}")
        print(f"  Queue Size: {status['task_queue']['size']}")
        print(f"  Success Rate: {status['performance']['success_rate']*100:.1f}%")
        print(f"  Workers: {status['auto_scaling']['current_workers']}")

    elif args.add_task:
        name, command, priority = args.add_task
        task_id = optimizer.add_task(name, command, int(priority))
        print(f"Task added with ID: {task_id}")

    elif args.optimize:
        result = optimizer.optimize_workload_distribution()
        print(f"\nOptimization Analysis:")
        print(f"  Recommendations: {len(result['recommendations'])}")
        for rec in result['recommendations']:
            print(f"  - {rec['action']} ({rec['priority']} priority)")

    else:
        print("Background Task Optimization System")
        print("Use --help to see available commands")


if __name__ == "__main__":
    main()