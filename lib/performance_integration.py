#!/usr/bin/env python3
# Performance Integration Module v1.0

# Integration layer for automatic performance recording in agents.

#     This module provides a simple interface that all agents can import and use
    """

to automatically record their performance without any manual intervention.

Usage in any agent:
    from lib.performance_integration import record_performance

    # At the start of task execution
    task_id = start_performance_recording("Task description", "task_type")

    # At the end of task execution
    record_performance(task_id, success=True, quality_score=95, ...)
import json
import time
import uuid
from pathlib import Path
from datetime import datetime, timezone

# Global performance tracking
_performance_tracker = None


class PerformanceIntegrator:
    """Simple performance recording integration for agents."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """Initialize the processor with default configuration."""
        self.patterns_dir = Path(patterns_dir)
        self.patterns_dir.mkdir(exist_ok=True)

        # Performance files
        self.performance_records_file = self.patterns_dir / "performance_records.json"
        self.patterns_file = self.patterns_dir / "patterns.json"

        # Active tasks tracking
        self.active_tasks = {}

        # Initialize files if needed
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Ensure required files exist."""
        if not self.performance_records_file.exists():
            self._create_performance_records_file()

        if not self.patterns_file.exists():
            self._create_patterns_file()

    def _create_performance_records_file(self):
        """Create performance records file if it doesn't exist."""
        initial_data = {
            "version": "2.0.0",
            "records": [],
            "summary": {},
            "model_metrics": {},
            "metadata": {
                "auto_recording_enabled": True,
                "created": datetime.now(timezone.utc).isoformat(),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total_records": 0,
            },
        }
        with open(self.performance_records_file, "w") as f:
            json.dump(initial_data, f, indent=2)

    def _create_patterns_file(self):
        """Create patterns file if it doesn't exist."""
        initial_data = {
            "version": "2.1.2",
            "cross_model_compatibility": True,
            "metadata": {
                "project_name": "Autonomous Agent Plugin",
                "created": datetime.now(timezone.utc).isoformat(),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total_tasks": 0,
                "global_learning_enabled": True,
            },
            "project_context": {
                "detected_languages": ["python", "markdown"],
                "frameworks": ["claude-code"],
                "project_type": "ai-plugin",
                "team_size": "individual",
                "development_stage": "active",
            },
            "patterns": [],
            "skill_effectiveness": {},
            "agent_performance": {},
            "trends": {},
            "optimizations": {},
        }
        with open(self.patterns_file, "w") as f:
            json.dump(initial_data, f, indent=2)

    def start_task():
        """
        
        Start tracking a task for performance recording.

                Args:
                    description: Task description
                    task_type: Type of task (
            e.g.,
            "code-analysis",
            "validation",
            "documentation",
        )

                Returns:
                    str: Task ID for later completion
        """
        task_id = str(uuid.uuid4())

        self.active_tasks[task_id] = {
            "id": task_id,
            "description": description,
            "type": task_type,
            "start_time": time.time(),
            "start_timestamp": datetime.now(timezone.utc).isoformat(),
        }

        return task_id

    def complete_task(
        self,
        task_id: str,
        success: bool = True,
        quality_score: int = 85,
        files_modified: int = 0,
        lines_changed: int = 0,
        skills_used: List[str] = None,
        agents_used: List[str] = None,
        issues_found: List[str] = None,
        recommendations: List[str] = None,
        duration_seconds: int = None,
        model_used: str = None,
    )-> bool:
        """Complete Task."""
        Complete a task and record its performance automatically.

        Args:
            task_id: Task ID from start_task()
            success: Whether task was successful
            quality_score: Quality score (0-100)
            files_modified: Number of files modified
            lines_changed: Number of lines changed
            skills_used: List of skills used
            agents_used: List of agents used
            issues_found: List of issues found
            recommendations: List of recommendations
            duration_seconds: Optional duration (calculated if not provided)
            model_used: Optional model name (detected if not provided)

        Returns:
            bool: True if recording was successful
        """
        if task_id not in self.active_tasks:
            return False

        task = self.active_tasks[task_id]

        # Calculate duration if not provided
        if duration_seconds is None:
            duration_seconds = round(time.time() - task["start_time"])

        # Detect model if not provided
        if model_used is None:
            model_used = self._detect_model()

        # Create performance record
        performance_record = {
            "assessment_id": f"auto-{task_id}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_type": task["type"],
            "overall_score": quality_score,
            "pass": quality_score >= 70,
            "skills_used": skills_used or ["autonomous"],
            "details": {
                "model_used": model_used,
                "duration_seconds": duration_seconds,
                "task_description": task["description"],
                "files_modified": files_modified,
                "lines_changed": lines_changed,
                "success": success,
                "auto_generated": True,
                "agents_used": agents_used or [],
            },
            "issues_found": issues_found or [],
            "recommendations": recommendations or [],
            "auto_generated": True,
        }

        # Store performance record
        success_perf = self._store_performance_record(performance_record)

        # Create learning pattern
        learning_pattern = {
            "task_id": task_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_type": task["type"],
            "task_description": task["description"],
            "task_complexity": "medium",
            "context": {
                "language": "python",
                "framework": "claude-code",
                "module_type": "automation",
                "file_count": files_modified,
                "lines_changed": lines_changed,
                "duration_seconds": duration_seconds,
                "success": success,
                "quality_score": quality_score,
            },
            "execution": {
                "skills_loaded": skills_used or ["autonomous"],
                "agents_delegated": agents_used or [],
                "approach_taken": "Automatic task execution with performance recording",
                "tools_used": ["automatic"],
                "duration_seconds": duration_seconds,
                "performance_metrics": {
                    "overall_score": quality_score,
                    "success_rate": 1.0 if success else 0.0,
                    "efficiency": max(0, min(100, 100 - (duration_seconds / 60))),
                },
            },
            "outcome": {
                "success": success,
                "quality_score": quality_score,
                "tests_passing": 0,
                "standards_compliance": quality_score,
                "documentation_coverage": 0,
                "errors_encountered": issues_found or [],
                "performance_recorded": True,
                "model_used": model_used,
                "task_completed_at": datetime.now(timezone.utc).isoformat(),
            },
            "insights": {
                "what_worked": ["Automatic performance recording"],
                "what_failed": [] if success else ["Task completion issues"],
                "bottlenecks": ([] if duration_seconds < 300 else ["Task took longer than expected"]),
                "optimization_opportunities": recommendations or [],
                "lessons_learned": [f"Automatic recording successful for {task['type']} tasks"],
            },
            "reuse_count": 0,
            "last_reused": None,
            "reuse_success_rate": None,
            "performance_metadata": {
                "recorded_by": "performance_integration",
                "integration_version": "1.0+",
                "dashboard_compatible": True,
                "auto_triggered": True,
            },
        }

        # Store learning pattern
        success_pattern = self._store_learning_pattern(learning_pattern)

        # Clean up active task
        del self.active_tasks[task_id]

        return success_perf and success_pattern

    def _detect_model(self) -> str:
        """Simple model detection."""
        import os

        # Check environment variables
        model = os.getenv("CLAUDE_MODEL")
        if model:
            return model

        # Default based on common patterns
        return "GLM-4.6"  # Current detected model

    def _store_performance_record(self, record: Dict[str, Any]) -> bool:
        """Store performance record."""
        try:
            with open(self.performance_records_file, "r") as f:
                data = json.load(f)

            data["records"].append(record)
            data["metadata"]["total_records"] = len(data["records"])
            data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()

            # Update summary
            task_type = record["task_type"]
            if "summary" not in data:
                data["summary"] = {}
            if task_type not in data["summary"]:
                data["summary"][task_type] = {
                    "count": 0,
                    "avg_score": 0.0,
                    "success_rate": 0.0,
                }

            summary = data["summary"][task_type]
            summary["count"] += 1

            # Update average score
            total_score = summary["avg_score"] * (summary["count"] - 1) + record["overall_score"]
            summary["avg_score"] = total_score / summary["count"]

            # Update success rate
            successes = summary["success_rate"] * (summary["count"] - 1) + (1.0 if record["pass"] else 0.0)
            summary["success_rate"] = successes / summary["count"]

            with open(self.performance_records_file, "w") as f:
                json.dump(data, f, indent=2)

            return True

        except Exception as e:
            print(f"ERROR storing performance record: {e}")
            return False

    def _store_learning_pattern(self, pattern: Dict[str, Any]) -> bool:
        """Store learning pattern."""
        try:
            with open(self.patterns_file, "r") as f:
                data = json.load(f)

            data["patterns"].append(pattern)
            data["metadata"]["total_tasks"] = len(data["patterns"])
            data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()

            with open(self.patterns_file, "w") as f:
                json.dump(data, f, indent=2)

            return True

        except Exception as e:
            print(f"ERROR storing learning pattern: {e}")
            return False


# Global instance
def get_performance_integrator() -> PerformanceIntegrator:
    """Get or create the global performance integrator."""
    global _performance_tracker
    if _performance_tracker is None:
        _performance_tracker = PerformanceIntegrator()
    return _performance_tracker


# Simple functions for agents to use
def start_performance_recording():
        """
        
        Start recording performance for a task.

    Simple function for agents to call at the start of task execution.

    Args:
        description: Task description
        task_type: Type of task

    Returns:
        str: Task ID to use when completing the task
    """
    integrator = get_performance_integrator()
    return integrator.start_task(description, task_type)


def record_performance():
        """
        
        Record task performance automatically.

    Simple function for agents to call at the end of task execution.

    Args:
        task_id: Task ID from start_performance_recording()
        success: Whether task was successful
        quality_score: Quality score (0-100)
        files_modified: Number of files modified
        lines_changed: Number of lines changed
        skills_used: List of skills used
        agents_used: List of agents used
        issues_found: List of issues found
        recommendations: List of recommendations
        duration_seconds: Optional duration (calculated if not provided)
        model_used: Optional model name (detected if not provided)

    Returns:
        bool: True if recording was successful
    """
    integrator = get_performance_integrator()
    return integrator.complete_task(
        task_id=task_id,
        success=success,
        quality_score=quality_score,
        files_modified=files_modified,
        lines_changed=lines_changed,
        skills_used=skills_used,
        agents_used=agents_used,
        issues_found=issues_found,
        recommendations=recommendations,
        duration_seconds=duration_seconds,
        model_used=model_used,
    )


# Example usage and testing
if __name__ == "__main__":
    # Test the integration system
    print("Testing Performance Integration...")

    # Start a task
    task_id = start_performance_recording("Test integration system", "testing")
    print(f"Started task: {task_id}")

    # Simulate work
    time.sleep(1)

    # Complete and record
    success = record_performance(
        task_id=task_id,
        success=True,
        quality_score=88,
        files_modified=1,
        lines_changed=25,
        skills_used=["performance-integration", "testing"],
        agents_used=["performance-integrator"],
        issues_found=[],
        recommendations=["Use this for all agent tasks"],
    )

    print(f"Performance recording successful: {success}")
