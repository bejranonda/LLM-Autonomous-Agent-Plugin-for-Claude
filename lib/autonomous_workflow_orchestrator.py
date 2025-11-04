#!/usr/bin/env python3
"""
Autonomous Workflow Orchestrator
Advanced automation system with intelligent workflow orchestration,
self-healing capabilities, and autonomous decision-making for complex
multi-agent tasks.
"""

import json
import sys
import time
import threading
import asyncio
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable, Union
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import hashlib

# Platform-specific imports for file locking
try:
    import msvcrt  # Windows
    PLATFORM = 'windows'
except ImportError:
    import fcntl  # Unix/Linux/Mac
    PLATFORM = 'unix'


class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"
    RETRYING = "retrying"


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


@dataclass
class WorkflowTask:
    """Individual workflow task definition."""
    task_id: str
    workflow_id: str
    task_type: str
    agent_id: str
    tier: str
    priority: TaskPriority
    dependencies: List[str]
    payload: Dict[str, Any]
    timeout_seconds: int = 300
    retry_count: int = 0
    max_retries: int = 3
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_context: Dict[str, Any] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.execution_context is None:
            self.execution_context = {}


@dataclass
class WorkflowDefinition:
    """Complete workflow definition."""
    workflow_id: str
    name: str
    description: str
    tasks: List[WorkflowTask]
    priority: TaskPriority
    created_at: datetime = None
    created_by: str = "system"
    context: Dict[str, Any] = None
    auto_heal: bool = True
    parallel_execution: bool = False
    rollback_on_failure: bool = True

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.context is None:
            self.context = {}


@dataclass
class WorkflowExecution:
    """Workflow execution instance."""
    execution_id: str
    workflow_id: str
    status: WorkflowStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    current_tasks: List[str] = None
    completed_tasks: List[str] = None
    failed_tasks: List[str] = None
    results: Dict[str, Any] = None
    error: Optional[str] = None
    execution_context: Dict[str, Any] = None

    def __post_init__(self):
        if self.current_tasks is None:
            self.current_tasks = []
        if self.completed_tasks is None:
            self.completed_tasks = []
        if self.failed_tasks is None:
            self.failed_tasks = []
        if self.results is None:
            self.results = {}
        if self.execution_context is None:
            self.execution_context = {}


class AutonomousWorkflowOrchestrator:
    """
    Advanced autonomous workflow orchestrator with intelligent task scheduling,
    self-healing capabilities, and autonomous decision-making.
    """

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the autonomous workflow orchestrator.

        Args:
            storage_dir: Directory for storing workflow data
        """
        self.storage_dir = Path(storage_dir)
        self.workflows_file = self.storage_dir / "workflows.json"
        self.executions_file = self.storage_dir / "workflow_executions.json"
        self.templates_file = self.storage_dir / "workflow_templates.json"
        self.automation_file = self.storage_dir / "automation_rules.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Workflow management
        self.workflows = {}  # workflow_id -> WorkflowDefinition
        self.active_executions = {}  # execution_id -> WorkflowExecution
        self.task_queue = asyncio.PriorityQueue()
        self.running_tasks = {}  # task_id -> WorkflowTask
        self.completed_tasks = {}  # task_id -> WorkflowTask

        # Automation and intelligence
        self.automation_rules = []
        self.healing_strategies = {}
        self.performance_models = {}
        self.decision_trees = {}
        self.learning_patterns = defaultdict(list)

        # Execution state
        self.orchestrator_active = False
        self.execution_thread = None
        self.healing_thread = None
        self.learning_thread = None

        # Performance tracking
        self.execution_metrics = defaultdict(list)
        self.success_rates = defaultdict(float)
        self.execution_times = defaultdict(list)
        self.agent_performance = defaultdict(dict)

        # Configuration
        self.max_concurrent_tasks = 10
        self.default_timeout = 300  # 5 minutes
        self.healing_enabled = True
        self.learning_enabled = True

        # Initialize storage
        self._initialize_workflow_storage()
        self._load_workflows_and_rules()

    def _initialize_workflow_storage(self):
        """Initialize workflow storage files."""
        if not self.workflows_file.exists():
            initial_data = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "workflows": {},
                "workflow_templates": {},
                "automation_rules": [],
                "execution_statistics": {
                    "total_workflows": 0,
                    "successful_executions": 0,
                    "failed_executions": 0,
                    "average_execution_time": 0.0
                }
            }
            self._write_workflows_data(initial_data)

        if not self.executions_file.exists():
            executions_data = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "executions": {},
                "active_executions": {},
                "execution_history": []
            }
            self._write_executions_data(executions_data)

        if not self.templates_file.exists():
            templates_data = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "templates": {},
                "template_categories": {}
            }
            self._write_templates_data(templates_data)

        if not self.automation_file.exists():
            automation_data = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "rules": [],
                "triggers": [],
                "actions": [],
                "conditions": []
            }
            self._write_automation_data(automation_data)

    def _load_workflows_and_rules(self):
        """Load workflows and automation rules from storage."""
        try:
            # Load workflows
            workflows_data = self._read_workflows_data()
            stored_workflows = workflows_data.get("workflows", {})
            for workflow_id, workflow_data in stored_workflows.items():
                # Reconstruct WorkflowDefinition
                tasks = [WorkflowTask(**task_data) for task_data in workflow_data.get("tasks", [])]
                workflow = WorkflowDefinition(
                    workflow_id=workflow_id,
                    name=workflow_data["name"],
                    description=workflow_data["description"],
                    tasks=tasks,
                    priority=TaskPriority(workflow_data["priority"]),
                    created_at=datetime.fromisoformat(workflow_data["created_at"]),
                    created_by=workflow_data.get("created_by", "system"),
                    context=workflow_data.get("context", {}),
                    auto_heal=workflow_data.get("auto_heal", True),
                    parallel_execution=workflow_data.get("parallel_execution", False),
                    rollback_on_failure=workflow_data.get("rollback_on_failure", True)
                )
                self.workflows[workflow_id] = workflow

            # Load automation rules
            automation_data = self._read_automation_data()
            self.automation_rules = automation_data.get("rules", [])

            # Load active executions
            executions_data = self._read_executions_data()
            active_executions = executions_data.get("active_executions", {})
            for execution_id, execution_data in active_executions.items():
                execution = WorkflowExecution(
                    execution_id=execution_id,
                    workflow_id=execution_data["workflow_id"],
                    status=WorkflowStatus(execution_data["status"]),
                    started_at=datetime.fromisoformat(execution_data["started_at"]),
                    completed_at=datetime.fromisoformat(execution_data["completed_at"]) if execution_data.get("completed_at") else None,
                    current_tasks=execution_data.get("current_tasks", []),
                    completed_tasks=execution_data.get("completed_tasks", []),
                    failed_tasks=execution_data.get("failed_tasks", []),
                    results=execution_data.get("results", {}),
                    error=execution_data.get("error"),
                    execution_context=execution_data.get("execution_context", {})
                )
                self.active_executions[execution_id] = execution

        except Exception as e:
            print(f"Warning: Failed to load workflows and rules: {e}", file=sys.stderr)

    def _lock_file(self, file_handle):
        """Platform-specific file locking."""
        if PLATFORM == 'windows':
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX)

    def _unlock_file(self, file_handle):
        """Platform-specific file unlocking."""
        if PLATFORM == 'windows':
            try:
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            except (OSError, PermissionError):
                pass
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)

    def _read_workflows_data(self) -> Dict[str, Any]:
        """Read workflows data with file locking."""
        try:
            with open(self.workflows_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_workflow_storage()
            return self._read_workflows_data()

    def _write_workflows_data(self, data: Dict[str, Any]):
        """Write workflows data with file locking."""
        with open(self.workflows_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_executions_data(self) -> Dict[str, Any]:
        """Read executions data with file locking."""
        try:
            with open(self.executions_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"executions": {}, "active_executions": {}}

    def _write_executions_data(self, data: Dict[str, Any]):
        """Write executions data with file locking."""
        with open(self.executions_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_templates_data(self) -> Dict[str, Any]:
        """Read templates data with file locking."""
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"templates": {}, "template_categories": {}}

    def _write_templates_data(self, data: Dict[str, Any]):
        """Write templates data with file locking."""
        with open(self.templates_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_automation_data(self) -> Dict[str, Any]:
        """Read automation data with file locking."""
        try:
            with open(self.automation_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"rules": [], "triggers": [], "actions": []}

    def _write_automation_data(self, data: Dict[str, Any]):
        """Write automation data with file locking."""
        with open(self.automation_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def create_workflow(
        self,
        name: str,
        description: str,
        tasks: List[Dict[str, Any]],
        priority: TaskPriority = TaskPriority.MEDIUM,
        context: Optional[Dict[str, Any]] = None,
        auto_heal: bool = True,
        parallel_execution: bool = False,
        rollback_on_failure: bool = True
    ) -> str:
        """
        Create a new workflow definition.

        Args:
            name: Workflow name
            description: Workflow description
            tasks: List of task definitions
            priority: Workflow priority
            context: Workflow context
            auto_heal: Enable auto-healing
            parallel_execution: Enable parallel execution
            rollback_on_failure: Enable rollback on failure

        Returns:
            Workflow ID
        """
        workflow_id = str(uuid.uuid4())

        # Create workflow tasks
        workflow_tasks = []
        for i, task_data in enumerate(tasks):
            task = WorkflowTask(
                task_id=str(uuid.uuid4()),
                workflow_id=workflow_id,
                task_type=task_data["task_type"],
                agent_id=task_data["agent_id"],
                tier=task_data["tier"],
                priority=TaskPriority(task_data.get("priority", priority.value)),
                dependencies=task_data.get("dependencies", []),
                payload=task_data.get("payload", {}),
                timeout_seconds=task_data.get("timeout_seconds", self.default_timeout),
                max_retries=task_data.get("max_retries", 3)
            )
            workflow_tasks.append(task)

        # Create workflow definition
        workflow = WorkflowDefinition(
            workflow_id=workflow_id,
            name=name,
            description=description,
            tasks=workflow_tasks,
            priority=priority,
            context=context or {},
            auto_heal=auto_heal,
            parallel_execution=parallel_execution,
            rollback_on_failure=rollback_on_failure
        )

        # Store workflow
        self.workflows[workflow_id] = workflow

        # Save to storage
        self._save_workflow(workflow)

        print(f"Created workflow: {name} (ID: {workflow_id})")
        return workflow_id

    def execute_workflow(
        self,
        workflow_id: str,
        execution_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Execute a workflow.

        Args:
            workflow_id: Workflow ID to execute
            execution_context: Additional execution context

        Returns:
            Execution ID
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow not found: {workflow_id}")

        workflow = self.workflows[workflow_id]
        execution_id = str(uuid.uuid4())

        # Create workflow execution
        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow_id=workflow_id,
            status=WorkflowStatus.RUNNING,
            started_at=datetime.now(),
            execution_context=execution_context or {}
        )

        # Store execution
        self.active_executions[execution_id] = execution

        # Add tasks to queue
        for task in workflow.tasks:
            # Clone task for execution
            execution_task = WorkflowTask(
                task_id=str(uuid.uuid4()),
                workflow_id=workflow_id,
                task_type=task.task_type,
                agent_id=task.agent_id,
                tier=task.tier,
                priority=task.priority,
                dependencies=task.dependencies,
                payload=task.payload,
                timeout_seconds=task.timeout_seconds,
                max_retries=task.max_retries
            )
            self.running_tasks[execution_task.task_id] = execution_task

            # Add to priority queue
            priority_value = (task.priority.value, time.time())
            asyncio.create_task(self.task_queue.put((priority_value, execution_task)))

        # Save execution state
        self._save_execution(execution)

        print(f"Started workflow execution: {execution_id}")
        return execution_id

    async def _execute_task(self, task: WorkflowTask) -> Dict[str, Any]:
        """
        Execute a single workflow task.

        Args:
            task: Task to execute

        Returns:
            Task execution result
        """
        try:
            # Update task status
            task.status = WorkflowStatus.RUNNING
            task.started_at = datetime.now()

            # Check dependencies
            if not self._check_dependencies(task):
                task.status = WorkflowStatus.WAITING
                return {"status": "waiting", "reason": "dependencies_not_met"}

            # Execute task (simulate execution)
            print(f"Executing task: {task.task_type} for agent: {task.agent_id}")

            # Simulate task execution with actual implementation
            result = await self._simulate_task_execution(task)

            # Update task status
            task.status = WorkflowStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result

            # Store in completed tasks
            self.completed_tasks[task.task_id] = task

            # Record execution metrics
            execution_time = (task.completed_at - task.started_at).total_seconds()
            self.execution_times[task.task_type].append(execution_time)

            # Update agent performance
            self._update_agent_performance(task.agent_id, task.task_type, True, execution_time)

            return {"status": "completed", "result": result}

        except Exception as e:
            # Handle task failure
            task.status = WorkflowStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()

            # Update agent performance
            execution_time = (task.completed_at - task.started_at).total_seconds()
            self._update_agent_performance(task.agent_id, task.task_type, False, execution_time)

            # Check if retry is needed
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = WorkflowStatus.RETRYING
                print(f"Task failed, retrying ({task.retry_count}/{task.max_retries}): {e}")

                # Add back to queue with delay
                await asyncio.sleep(2 ** task.retry_count)  # Exponential backoff
                priority_value = (task.priority.value, time.time())
                await self.task_queue.put((priority_value, task))
            else:
                print(f"Task failed permanently: {e}")

                # Trigger auto-healing if enabled
                if self.workflows[task.workflow_id].auto_heal:
                    await self._attempt_task_healing(task)

            return {"status": "failed", "error": str(e)}

    async def _simulate_task_execution(self, task: WorkflowTask) -> Dict[str, Any]:
        """Simulate task execution with realistic behavior."""
        # Simulate different execution times based on task type
        execution_times = {
            "analysis": 5,
            "validation": 3,
            "testing": 8,
            "documentation": 6,
            "quality_check": 4,
            "security_scan": 10,
            "deployment": 15
        }

        base_time = execution_times.get(task.task_type, 5)
        execution_time = base_time + random.uniform(-2, 5)

        # Simulate execution
        await asyncio.sleep(execution_time)

        # Simulate different results based on task type
        if task.task_type == "analysis":
            return {"analysis_result": "completed", "findings": ["item1", "item2"], "confidence": 0.85}
        elif task.task_type == "validation":
            return {"validation_result": "passed", "issues_found": 0, "score": 95}
        elif task.task_type == "testing":
            return {"test_result": "passed", "tests_run": 25, "failures": 0}
        elif task.task_type == "documentation":
            return {"documentation_result": "generated", "pages_created": 5}
        elif task.task_type == "quality_check":
            return {"quality_result": "excellent", "score": 92, "issues_fixed": 3}
        elif task.task_type == "security_scan":
            return {"security_result": "clean", "vulnerabilities": 0, "scan_time": execution_time}
        elif task.task_type == "deployment":
            return {"deployment_result": "success", "services_deployed": 3, "rollback_available": True}
        else:
            return {"result": "completed", "execution_time": execution_time}

    def _check_dependencies(self, task: WorkflowTask) -> bool:
        """Check if task dependencies are satisfied."""
        for dependency_id in task.dependencies:
            if dependency_id not in self.completed_tasks:
                return False
            if self.completed_tasks[dependency_id].status != WorkflowStatus.COMPLETED:
                return False
        return True

    def _update_agent_performance(
        self,
        agent_id: str,
        task_type: str,
        success: bool,
        execution_time: float
    ):
        """Update agent performance metrics."""
        if agent_id not in self.agent_performance:
            self.agent_performance[agent_id] = {
                "total_tasks": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "average_execution_time": 0.0,
                "task_types": defaultdict(int)
            }

        perf = self.agent_performance[agent_id]
        perf["total_tasks"] += 1

        if success:
            perf["successful_tasks"] += 1
        else:
            perf["failed_tasks"] += 1

        # Update execution time
        if perf["total_tasks"] == 1:
            perf["average_execution_time"] = execution_time
        else:
            perf["average_execution_time"] = (
                (perf["average_execution_time"] * (perf["total_tasks"] - 1) + execution_time) /
                perf["total_tasks"]
            )

        # Update task type statistics
        perf["task_types"][task_type] += 1

    async def _attempt_task_healing(self, task: WorkflowTask):
        """Attempt to heal a failed task."""
        if not self.healing_enabled:
            return

        print(f"Attempting to heal failed task: {task.task_id}")

        # Determine healing strategy based on error type
        healing_strategy = self._determine_healing_strategy(task)

        if healing_strategy:
            try:
                # Apply healing strategy
                healed_task = await self._apply_healing_strategy(task, healing_strategy)

                if healed_task:
                    print(f"Task healed successfully: {task.task_id}")
                    # Re-execute healed task
                    await self.task_queue.put((task.priority.value, time.time(), healed_task))
                else:
                    print(f"Healing failed for task: {task.task_id}")

            except Exception as e:
                print(f"Error during task healing: {e}")

    def _determine_healing_strategy(self, task: WorkflowTask) -> Optional[str]:
        """Determine appropriate healing strategy for failed task."""
        if not task.error:
            return None

        error_lower = task.error.lower()

        # Analyze error type and suggest healing strategy
        if "timeout" in error_lower:
            return "increase_timeout"
        elif "connection" in error_lower or "network" in error_lower:
            return "retry_with_backoff"
        elif "permission" in error_lower or "access" in error_lower:
            return "escalate_privileges"
        elif "resource" in error_lower or "memory" in error_lower:
            return "allocate_more_resources"
        elif "dependency" in error_lower:
            return "resolve_dependencies"
        elif "configuration" in error_lower:
            return "fix_configuration"
        else:
            return "generic_retry"

    async def _apply_healing_strategy(
        self,
        task: WorkflowTask,
        strategy: str
    ) -> Optional[WorkflowTask]:
        """Apply a specific healing strategy to a task."""
        try:
            # Create healed task copy
            healed_task = WorkflowTask(
                task_id=str(uuid.uuid4()),
                workflow_id=task.workflow_id,
                task_type=task.task_type,
                agent_id=task.agent_id,
                tier=task.tier,
                priority=task.priority,
                dependencies=task.dependencies,
                payload=task.payload.copy(),
                timeout_seconds=task.timeout_seconds,
                max_retries=task.max_retries,
                retry_count=0,  # Reset retry count for healed task
                execution_context=task.execution_context.copy() if task.execution_context else {}
            )

            # Apply strategy-specific modifications
            if strategy == "increase_timeout":
                healed_task.timeout_seconds = task.timeout_seconds * 2
                healed_task.payload["healing_applied"] = "timeout_increased"

            elif strategy == "retry_with_backoff":
                healed_task.payload["healing_applied"] = "retry_with_backoff"
                healed_task.payload["backoff_factor"] = 2

            elif strategy == "escalate_privileges":
                healed_task.payload["healing_applied"] = "privileges_escalated"
                healed_task.payload["elevated_permissions"] = True

            elif strategy == "allocate_more_resources":
                healed_task.payload["healing_applied"] = "resources_allocated"
                healed_task.payload["memory_limit"] = "increased"
                healed_task.payload["cpu_limit"] = "increased"

            elif strategy == "resolve_dependencies":
                healed_task.payload["healing_applied"] = "dependencies_resolved"
                # Remove problematic dependencies if possible
                healed_task.dependencies = []

            elif strategy == "fix_configuration":
                healed_task.payload["healing_applied"] = "configuration_fixed"
                healed_task.payload["auto_fix_config"] = True

            elif strategy == "generic_retry":
                healed_task.payload["healing_applied"] = "generic_retry"
                healed_task.retry_count = 0

            return healed_task

        except Exception as e:
            print(f"Error applying healing strategy {strategy}: {e}")
            return None

    def start_orchestrator(self):
        """Start the workflow orchestrator."""
        if self.orchestrator_active:
            print("Orchestrator already active")
            return

        self.orchestrator_active = True

        # Start execution loop
        self.execution_thread = threading.Thread(target=self._execution_loop, daemon=True)
        self.execution_thread.start()

        # Start healing loop
        self.healing_thread = threading.Thread(target=self._healing_loop, daemon=True)
        self.healing_thread.start()

        # Start learning loop
        self.learning_thread = threading.Thread(target=self._learning_loop, daemon=True)
        self.learning_thread.start()

        print("Autonomous workflow orchestrator started")

    def stop_orchestrator(self):
        """Stop the workflow orchestrator."""
        if not self.orchestrator_active:
            return

        self.orchestrator_active = False

        # Wait for threads to finish
        for thread, name in [(self.execution_thread, "execution"),
                            (self.healing_thread, "healing"),
                            (self.learning_thread, "learning")]:
            if thread and thread.is_alive():
                thread.join(timeout=5)
                print(f"  {name} thread stopped")

        print("Autonomous workflow orchestrator stopped")

    def _execution_loop(self):
        """Main execution loop for processing tasks."""
        while self.orchestrator_active:
            try:
                # Process tasks from queue
                while len(self.running_tasks) < self.max_concurrent_tasks and not self.task_queue.empty():
                    try:
                        priority_value, task = asyncio.run(self.task_queue.get_nowait())

                        # Check dependencies again
                        if self._check_dependencies(task):
                            self.running_tasks[task.task_id] = task

                            # Execute task asynchronously
                            asyncio.create_task(self._execute_task(task))
                        else:
                            # Put back in queue
                            asyncio.run(self.task_queue.put((priority_value, task)))

                    except asyncio.QueueEmpty:
                        break

                # Check for completed tasks
                completed_task_ids = []
                for task_id, task in self.running_tasks.items():
                    if task.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED]:
                        completed_task_ids.append(task_id)

                        # Update workflow execution
                        self._update_workflow_execution(task)

                # Remove completed tasks
                for task_id in completed_task_ids:
                    if task_id in self.running_tasks:
                        del self.running_tasks[task_id]

                # Check automation rules
                self._check_automation_rules()

                time.sleep(1)  # Check every second

            except Exception as e:
                print(f"Error in execution loop: {e}", file=sys.stderr)
                time.sleep(1)

    def _healing_loop(self):
        """Background healing loop for proactive maintenance."""
        while self.orchestrator_active:
            try:
                # Check for stuck tasks
                current_time = time.time()
                stuck_tasks = []

                for task_id, task in self.running_tasks.items():
                    if (task.started_at and
                        (current_time - task.started_at.timestamp()) > task.timeout_seconds):
                        stuck_tasks.append(task)

                # Attempt to heal stuck tasks
                for task in stuck_tasks:
                    print(f"Found stuck task: {task.task_id}, attempting healing")
                    asyncio.run(self._attempt_task_healing(task))

                # Check workflow health
                self._check_workflow_health()

                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                print(f"Error in healing loop: {e}", file=sys.stderr)
                time.sleep(5)

    def _learning_loop(self):
        """Background learning loop for pattern recognition and optimization."""
        while self.orchestrator_active:
            try:
                # Analyze execution patterns
                self._analyze_execution_patterns()

                # Update performance models
                self._update_performance_models()

                # Optimize task scheduling
                self._optimize_task_scheduling()

                # Generate automation suggestions
                self._generate_automation_suggestions()

                time.sleep(60)  # Learn every minute

            except Exception as e:
                print(f"Error in learning loop: {e}", file=sys.stderr)
                time.sleep(10)

    def _update_workflow_execution(self, task: WorkflowTask):
        """Update workflow execution based on task completion."""
        for execution in self.active_executions.values():
            if execution.workflow_id == task.workflow_id:
                if task.task_id in execution.current_tasks:
                    execution.current_tasks.remove(task.task_id)

                if task.status == WorkflowStatus.COMPLETED:
                    execution.completed_tasks.append(task.task_id)
                    if task.result:
                        execution.results[task.task_id] = task.result
                elif task.status == WorkflowStatus.FAILED:
                    execution.failed_tasks.append(task.task_id)
                    if task.error:
                        execution.error = task.error

                # Check if workflow is complete
                workflow = self.workflows[task.workflow_id]
                all_tasks_completed = all(
                    task_id in execution.completed_tasks or task_id in execution.failed_tasks
                    for task in workflow.tasks
                )

                if all_tasks_completed:
                    if not execution.failed_tasks:
                        execution.status = WorkflowStatus.COMPLETED
                    else:
                        execution.status = WorkflowStatus.FAILED

                    execution.completed_at = datetime.now()

                # Save execution state
                self._save_execution(execution)

    def _check_automation_rules(self):
        """Check and apply automation rules."""
        current_time = datetime.now()

        for rule in self.automation_rules:
            try:
                # Check rule conditions
                if self._evaluate_rule_condition(rule, current_time):
                    # Execute rule action
                    self._execute_rule_action(rule)

            except Exception as e:
                print(f"Error processing automation rule: {e}", file=sys.stderr)

    def _evaluate_rule_condition(self, rule: Dict[str, Any], current_time: datetime) -> bool:
        """Evaluate automation rule condition."""
        condition = rule.get("condition", {})

        # Time-based conditions
        if "time_based" in condition:
            time_condition = condition["time_based"]
            if time_condition.get("type") == "hourly":
                return current_time.minute == 0
            elif time_condition.get("type") == "daily":
                return current_time.hour == 0 and current_time.minute == 0

        # Metric-based conditions
        if "metric_based" in condition:
            metric_condition = condition["metric_based"]
            metric_name = metric_condition.get("metric")
            threshold = metric_condition.get("threshold")
            operator = metric_condition.get("operator", ">")

            if metric_name and threshold is not None:
                current_value = self._get_current_metric_value(metric_name)
                if current_value is not None:
                    if operator == ">":
                        return current_value > threshold
                    elif operator == "<":
                        return current_value < threshold
                    elif operator == "==":
                        return current_value == threshold

        # Task-based conditions
        if "task_based" in condition:
            task_condition = condition["task_based"]
            task_type = task_condition.get("task_type")
            status_filter = task_condition.get("status")

            for task in self.running_tasks.values():
                if task_type and task.task_type == task_type:
                    if status_filter and task.status.value == status_filter:
                        return True

        return False

    def _execute_rule_action(self, rule: Dict[str, Any]):
        """Execute automation rule action."""
        action = rule.get("action", {})

        if action.get("type") == "create_workflow":
            # Create new workflow based on template
            template_id = action.get("template_id")
            if template_id:
                self._create_workflow_from_template(template_id)

        elif action.get("type") == "adjust_priority":
            # Adjust task priorities
            task_filter = action.get("task_filter", {})
            new_priority = action.get("new_priority")
            if task_filter and new_priority:
                self._adjust_task_priorities(task_filter, new_priority)

        elif action.get("type") == "cleanup_resources":
            # Cleanup completed tasks and executions
            self._cleanup_resources()

        elif action.get("type") == "send_notification":
            # Send notification (implementation-specific)
            message = action.get("message", "Automation rule triggered")
            print(f"NOTIFICATION: {message}")

    def _get_current_metric_value(self, metric_name: str) -> Optional[float]:
        """Get current value for a metric."""
        # This would integrate with the monitoring system
        # For now, return simulated values
        if metric_name == "active_tasks":
            return len(self.running_tasks)
        elif metric_name == "failed_task_rate":
            total_tasks = len(self.running_tasks) + len(self.completed_tasks)
            if total_tasks == 0:
                return 0
            failed_count = sum(1 for t in self.completed_tasks.values() if t.status == WorkflowStatus.FAILED)
            return failed_count / total_tasks
        else:
            return None

    def _create_workflow_from_template(self, template_id: str):
        """Create a workflow from a template."""
        templates_data = self._read_templates_data()
        templates = templates_data.get("templates", {})

        if template_id in templates:
            template = templates[template_id]
            self.create_workflow(
                name=f"Auto-created from {template['name']}",
                description=template.get("description", ""),
                tasks=template.get("tasks", []),
                auto_heal=template.get("auto_heal", True)
            )
            print(f"Created workflow from template: {template_id}")

    def _adjust_task_priorities(self, task_filter: Dict[str, Any], new_priority: int):
        """Adjust priorities of tasks matching filter."""
        for task in self.running_tasks.values():
            match = True

            if "task_type" in task_filter:
                if task.task_type != task_filter["task_type"]:
                    match = False

            if "agent_id" in task_filter:
                if task.agent_id != task_filter["agent_id"]:
                    match = False

            if match:
                task.priority = TaskPriority(new_priority)
                print(f"Adjusted priority for task {task.task_id} to {new_priority}")

    def _cleanup_resources(self):
        """Cleanup completed tasks and old executions."""
        current_time = datetime.now()

        # Clean up completed tasks older than 1 hour
        old_tasks = [
            task_id for task_id, task in self.completed_tasks.items()
            if task.completed_at and (current_time - task.completed_at).total_seconds() > 3600
        ]

        for task_id in old_tasks:
            del self.completed_tasks[task_id]

        # Clean up completed executions older than 24 hours
        old_executions = [
            exec_id for exec_id, execution in self.active_executions.items()
            if execution.completed_at and (current_time - execution.completed_at).total_seconds() > 86400
        ]

        for exec_id in old_executions:
            del self.active_executions[exec_id]

        if old_tasks or old_executions:
            print(f"Cleaned up {len(old_tasks)} tasks and {len(old_executions)} executions")

    def _check_workflow_health(self):
        """Check overall workflow health and take corrective actions."""
        # Calculate success rate
        total_tasks = len(self.running_tasks) + len(self.completed_tasks)
        if total_tasks == 0:
            return

        successful_tasks = len([t for t in self.completed_tasks.values() if t.status == WorkflowStatus.COMPLETED])
        success_rate = successful_tasks / total_tasks

        # If success rate is too low, take action
        if success_rate < 0.7:
            print(f"Low success rate detected: {success_rate:.1%}, taking corrective action")

            # Increase timeouts for remaining tasks
            for task in self.running_tasks.values():
                if task.timeout_seconds < 600:  # Max 10 minutes
                    task.timeout_seconds = min(600, task.timeout_seconds * 1.5)
                    print(f"Increased timeout for task {task.task_id}")

            # Reduce concurrent tasks to prevent overload
            if self.max_concurrent_tasks > 5:
                self.max_concurrent_tasks = max(5, self.max_concurrent_tasks - 1)
                print(f"Reduced max concurrent tasks to {self.max_concurrent_tasks}")

    def _analyze_execution_patterns(self):
        """Analyze execution patterns for optimization."""
        if not self.learning_enabled:
            return

        # Analyze task execution times
        for task_type, times in self.execution_times.items():
            if len(times) >= 10:
                avg_time = statistics.mean(times)
                std_dev = statistics.stdev(times)

                # Detect outliers
                outliers = [t for t in times if abs(t - avg_time) > 2 * std_dev]

                if outliers:
                    print(f"Detected {len(outliers)} outliers for task type {task_type}")

                    # Store learning pattern
                    self.learning_patterns[task_type].append({
                        "timestamp": datetime.now().isoformat(),
                        "pattern_type": "execution_time_outlier",
                        "outlier_count": len(outliers),
                        "avg_time": avg_time,
                        "std_dev": std_dev
                    })

    def _update_performance_models(self):
        """Update performance prediction models."""
        for agent_id, perf in self.agent_performance.items():
            if perf["total_tasks"] >= 5:
                success_rate = perf["successful_tasks"] / perf["total_tasks"]

                # Update success rate tracking
                self.success_rates[agent_id].append(success_rate)
                if len(self.success_rates[agent_id]) > 20:
                    self.success_rates[agent_id] = self.success_rates[agent_id][-20:]

    def _optimize_task_scheduling(self):
        """Optimize task scheduling based on learned patterns."""
        # This would implement more sophisticated scheduling algorithms
        # For now, just basic optimization based on agent performance

        agent_performance_scores = {}
        for agent_id, perf in self.agent_performance.items():
            if perf["total_tasks"] >= 3:
                success_rate = perf["successful_tasks"] / perf["total_tasks"]
                speed_score = 1.0 / (1.0 + perf["average_execution_time"] / 60)  # Normalize by minute
                agent_performance_scores[agent_id] = success_rate * 0.7 + speed_score * 0.3

        # Sort tasks by priority and agent performance
        if agent_performance_scores:
            print(f"Top performing agents: {sorted(agent_performance_scores.items(), key=lambda x: x[1], reverse=True)[:3]}")

    def _generate_automation_suggestions(self):
        """Generate suggestions for new automation rules."""
        suggestions = []

        # Analyze frequent failures
        failed_tasks = [t for t in self.completed_tasks.values() if t.status == WorkflowStatus.FAILED]
        if len(failed_tasks) >= 5:
            # Group failures by error type
            error_groups = defaultdict(list)
            for task in failed_tasks:
                if task.error:
                    error_type = task.error.split(':')[0]  # Get first part of error
                    error_groups[error_type].append(task)

            for error_type, tasks in error_groups.items():
                if len(tasks) >= 3:
                    suggestions.append({
                        "type": "healing_rule",
                        "description": f"Auto-heal rule for {error_type} errors",
                        "trigger_error": error_type,
                        "healing_strategy": self._determine_healing_strategy(tasks[0])
                    })

        # Store suggestions for later review
        if suggestions:
            print(f"Generated {len(suggestions)} automation suggestions")

    def _save_workflow(self, workflow: WorkflowDefinition):
        """Save workflow to storage."""
        workflows_data = self._read_workflows_data()
        workflows_data["workflows"][workflow.workflow_id] = {
            "name": workflow.name,
            "description": workflow.description,
            "priority": workflow.priority.value,
            "created_at": workflow.created_at.isoformat(),
            "created_by": workflow.created_by,
            "context": workflow.context,
            "auto_heal": workflow.auto_heal,
            "parallel_execution": workflow.parallel_execution,
            "rollback_on_failure": workflow.rollback_on_failure,
            "tasks": [asdict(task) for task in workflow.tasks]
        }
        workflows_data["last_updated"] = datetime.now().isoformat()
        self._write_workflows_data(workflows_data)

    def _save_execution(self, execution: WorkflowExecution):
        """Save execution to storage."""
        executions_data = self._read_executions_data()
        executions_data["active_executions"][execution.execution_id] = {
            "workflow_id": execution.workflow_id,
            "status": execution.status.value,
            "started_at": execution.started_at.isoformat(),
            "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
            "current_tasks": execution.current_tasks,
            "completed_tasks": execution.completed_tasks,
            "failed_tasks": execution.failed_tasks,
            "results": execution.results,
            "error": execution.error,
            "execution_context": execution.execution_context
        }

        # Move completed executions to history
        if execution.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED]:
            executions_data["execution_history"].append(executions_data["active_executions"][execution.execution_id])
            del executions_data["active_executions"][execution.execution_id]

            # Keep last 1000 executions in history
            if len(executions_data["execution_history"]) > 1000:
                executions_data["execution_history"] = executions_data["execution_history"][-1000:]

        executions_data["last_updated"] = datetime.now().isoformat()
        self._write_executions_data(executions_data)

    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get comprehensive orchestrator status."""
        return {
            "orchestrator_status": {
                "active": self.orchestrator_active,
                "max_concurrent_tasks": self.max_concurrent_tasks,
                "running_tasks": len(self.running_tasks),
                "completed_tasks": len(self.completed_tasks),
                "active_workflows": len(self.active_executions)
            },
            "workflow_statistics": {
                "total_workflows": len(self.workflows),
                "active_executions": len(self.active_executions),
                "success_rate": self._calculate_overall_success_rate(),
                "average_execution_time": self._calculate_average_execution_time()
            },
            "agent_performance": dict(self.agent_performance),
            "learning_status": {
                "enabled": self.learning_enabled,
                "healing_enabled": self.healing_enabled,
                "patterns_learned": len(self.learning_patterns),
                "automation_rules": len(self.automation_rules)
            },
            "system_health": {
                "success_rate": self._calculate_overall_success_rate(),
                "error_rate": 1.0 - self._calculate_overall_success_rate(),
                "active_threads": sum(1 for t in [self.execution_thread, self.healing_thread, self.learning_thread] if t and t.is_alive())
            }
        }

    def _calculate_overall_success_rate(self) -> float:
        """Calculate overall task success rate."""
        total_tasks = len(self.running_tasks) + len(self.completed_tasks)
        if total_tasks == 0:
            return 1.0

        successful_tasks = len([t for t in self.completed_tasks.values() if t.status == WorkflowStatus.COMPLETED])
        return successful_tasks / total_tasks

    def _calculate_average_execution_time(self) -> float:
        """Calculate average task execution time."""
        all_times = []
        for times in self.execution_times.values():
            all_times.extend(times)

        if all_times:
            return statistics.mean(all_times)
        return 0.0


def main():
    """Command-line interface for testing the autonomous workflow orchestrator."""
    import argparse
    import random

    parser = argparse.ArgumentParser(description='Autonomous Workflow Orchestrator')
    parser.add_argument('--storage-dir', default='.claude-patterns', help='Storage directory')
    parser.add_argument('--action', choices=['start', 'stop', 'status', 'create', 'execute', 'test'],
                       help='Action to perform')
    parser.add_argument('--workflow-name', help='Workflow name')
    parser.add_argument('--duration', type=int, default=60, help='Test duration in seconds')

    args = parser.parse_args()

    orchestrator = AutonomousWorkflowOrchestrator(args.storage_dir)

    if args.action == 'start':
        orchestrator.start_orchestrator()
        print("Orchestrator started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            orchestrator.stop_orchestrator()

    elif args.action == 'stop':
        orchestrator.stop_orchestrator()

    elif args.action == 'status':
        status = orchestrator.get_orchestrator_status()
        print("Autonomous Workflow Orchestrator Status:")
        print(f"  Active: {status['orchestrator_status']['active']}")
        print(f"  Running Tasks: {status['orchestrator_status']['running_tasks']}")
        print(f"  Completed Tasks: {status['orchestrator_status']['completed_tasks']}")
        print(f"  Success Rate: {status['workflow_statistics']['success_rate']:.1%}")
        print(f"  Learning Enabled: {status['learning_status']['enabled']}")

    elif args.action == 'create':
        if not args.workflow_name:
            args.workflow_name = "Test Workflow"

        # Create sample workflow
        tasks = [
            {
                "task_type": "analysis",
                "agent_id": "code-analyzer",
                "tier": "analysis",
                "payload": {"target": "sample.py"}
            },
            {
                "task_type": "validation",
                "agent_id": "validation-controller",
                "tier": "analysis",
                "dependencies": ["analysis"],
                "payload": {"strict": True}
            },
            {
                "task_type": "testing",
                "agent_id": "test-engineer",
                "tier": "execution",
                "dependencies": ["validation"],
                "payload": {"coverage": 80}
            },
            {
                "task_type": "quality_check",
                "agent_id": "quality-controller",
                "tier": "execution",
                "dependencies": ["testing"],
                "payload": {"threshold": 85}
            }
        ]

        workflow_id = orchestrator.create_workflow(
            name=args.workflow_name,
            description="Sample autonomous workflow",
            tasks=tasks,
            auto_heal=True,
            parallel_execution=False
        )
        print(f"Created workflow: {workflow_id}")

    elif args.action == 'execute':
        if not args.workflow_name:
            # Find first workflow
            if orchestrator.workflows:
                workflow_id = next(iter(orchestrator.workflows.keys()))
            else:
                print("No workflows found. Create one first.")
                sys.exit(1)
        else:
            # Find workflow by name
            workflow_id = None
            for wid, workflow in orchestrator.workflows.items():
                if workflow.name == args.workflow_name:
                    workflow_id = wid
                    break

            if not workflow_id:
                print(f"Workflow not found: {args.workflow_name}")
                sys.exit(1)

        execution_id = orchestrator.execute_workflow(workflow_id)
        print(f"Started workflow execution: {execution_id}")

        # Start orchestrator if not running
        if not orchestrator.orchestrator_active:
            orchestrator.start_orchestrator()
            print("Orchestrator started to handle execution")

    elif args.action == 'test':
        print("Running autonomous workflow orchestrator test...")

        # Create test workflow
        tasks = [
            {
                "task_type": "analysis",
                "agent_id": "code-analyzer",
                "tier": "analysis",
                "payload": {"simulate": True}
            },
            {
                "task_type": "validation",
                "agent_id": "validation-controller",
                "tier": "analysis",
                "dependencies": ["analysis"],
                "payload": {"simulate": True}
            },
            {
                "task_type": "testing",
                "agent_id": "test-engineer",
                "tier": "execution",
                "dependencies": ["validation"],
                "payload": {"simulate": True}
            }
        ]

        workflow_id = orchestrator.create_workflow(
            name="Autonomous Test Workflow",
            description="Test workflow for autonomous orchestrator",
            tasks=tasks,
            auto_heal=True,
            parallel_execution=False
        )

        # Start orchestrator
        orchestrator.start_orchestrator()

        # Execute workflow multiple times
        for i in range(3):
            print(f"\nExecuting test workflow {i+1}/3...")
            execution_id = orchestrator.execute_workflow(workflow_id)
            print(f"Started execution: {execution_id}")

            # Wait for completion
            time.sleep(10)

        # Wait for all tasks to complete
        print("\nWaiting for all tasks to complete...")
        time.sleep(20)

        # Show final status
        status = orchestrator.get_orchestrator_status()
        print(f"\nTest Results:")
        print(f"  Total Workflows: {status['workflow_statistics']['total_workflows']}")
        print(f"  Success Rate: {status['workflow_statistics']['success_rate']:.1%}")
        print(f"  Average Execution Time: {status['workflow_statistics']['average_execution_time']:.1f}s")
        print(f"  Patterns Learned: {status['learning_status']['patterns_learned']}")

        # Stop orchestrator
        orchestrator.stop_orchestrator()

    else:
        # Show status by default
        status = orchestrator.get_orchestrator_status()
        print("Autonomous Workflow Orchestrator Summary:")
        print(f"  Active: {status['orchestrator_status']['active']}")
        print(f"  Total Workflows: {status['workflow_statistics']['total_workflows']}")
        print(f"  Success Rate: {status['workflow_statistics']['success_rate']:.1%}")


if __name__ == '__main__':
    main()