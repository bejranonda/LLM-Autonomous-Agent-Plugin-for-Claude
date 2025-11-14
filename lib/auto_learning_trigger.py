#!/usr/bin/env python3
# Automatic Learning Engine Trigger v1.0

# This script automatically triggers the learning-engine agent after task completion
# to ensure consistent performance recording and pattern capture.

# Fixes the gap where tasks complete but don't automatically record performance.
import json
import time
import uuid
from pathlib import Path
import os
from datetime import datetime, timezone
from typing import Dict, Any, List


class AutomaticLearningTrigger:
    """Automatically triggers learning engine and performance recording after tasks."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """Initialize the processor with default configuration."""
        self.patterns_dir = Path(patterns_dir)
        self.patterns_dir.mkdir(exist_ok=True)

        # Data files
        self.performance_records_file = self.patterns_dir / "performance_records.json"
        self.patterns_file = self.patterns_dir / "patterns.json"
        self.trigger_log_file = self.patterns_dir / "auto_trigger_log.json"

        # Initialize files
        self._initialize_files()

        # Task tracking
        self.current_task = None
        self.task_start_time = None

    def _initialize_files(self):
        """Initialize required data files."""
        # Initialize performance records
        if not self.performance_records_file.exists():
            self._create_performance_records_file()

        # Initialize patterns
        if not self.patterns_file.exists():
            self._create_patterns_file()

        # Initialize trigger log
        if not self.trigger_log_file.exists():
            self._create_trigger_log_file()

    def _create_performance_records_file(self):
        """Create initial performance records file."""
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
        """Create initial patterns file."""
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

    def _create_trigger_log_file(self):
        """Create initial trigger log file."""
        initial_data = {
            "version": "1.0.0",
            "triggers": [],
            "metadata": {
                "created": datetime.now(timezone.utc).isoformat(),
                "last_trigger": None,
                "total_triggers": 0,
                "successful_triggers": 0,
            },
        }
        with open(self.trigger_log_file, "w") as f:
            json.dump(initial_data, f, indent=2)

    def detect_current_model(self) -> str:
        """Detect the current model being used."""
        # Check environment variables first
        model = os.getenv("CLAUDE_MODEL")
        if model:
            return model

        # Check for GLM
        if "glm" in os.getenv("TERM", "").lower() or "glm" in os.getenv("SHELL", "").lower():
            return "GLM-4.6"

        # Check for Claude
        if "claude" in os.getenv("TERM", "").lower():
            return "Claude Sonnet 4.5"

        # Default fallback
        return "Unknown Model"

    def start_task_tracking(self, task_description: str, task_type: str = "unknown"):
        """Start tracking a new task."""
        self.current_task = {
            "id": str(uuid.uuid4()),
            "description": task_description,
            "type": task_type,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "start_timestamp": time.time(),
        }
        self.task_start_time = time.time()

        # Log task start
        self._log_trigger(
            "task_started", {"task_id": self.current_task["id"], "description": task_description, "type": task_type}
        )

    def complete_task_with_recording(
        self,
        success: bool = True,
        quality_score: int = 85,
        files_modified: int = 0,
        lines_changed: int = 0,
        skills_used: List[str] = None,
        issues_found: List[str] = None,
        recommendations: List[str] = None,
    )-> Dict[str, Any]:
        """Complete Task With Recording."""
        Complete the current task and automatically trigger performance recording.

        This is the CRITICAL function that fixes the automatic recording gap.
"""
        if not self.current_task:
            print("WARNING: No task currently being tracked")
            return {}

        # Calculate task duration
        duration = time.time() - self.task_start_time

        # Create performance record
        performance_record = {
            "assessment_id": f"auto-{self.current_task['id']}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_type": self.current_task["type"],
            "overall_score": quality_score,
            "pass": quality_score >= 70,
            "skills_used": skills_used or ["autonomous-development"],
            "details": {
                "model_used": self.detect_current_model(),
                "duration_seconds": round(duration),
                "task_description": self.current_task["description"],
                "files_modified": files_modified,
                "lines_changed": lines_changed,
                "success": success,
                "auto_generated": True,
            },
            "issues_found": issues_found or [],
            "recommendations": recommendations or [],
            "auto_generated": True,
        }

        # Store performance record
        self._store_performance_record(performance_record)

        # Create learning pattern
        learning_pattern = {
            "task_id": self.current_task["id"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_type": self.current_task["type"],
            "task_description": self.current_task["description"],
            "task_complexity": "medium",  # Could be calculated
            "context": {
                "language": "python",
                "framework": "claude-code",
                "module_type": "automation",
                "file_count": files_modified,
                "lines_changed": lines_changed,
                "duration_seconds": round(duration),
                "success": success,
                "quality_score": quality_score,
            },
            "execution": {
                "skills_loaded": skills_used or ["autonomous-development"],
                "agents_delegated": ["automatic-learning-trigger"],
                "approach_taken": "Automatic task completion with performance recording",
                "tools_used": ["automatic"],
                "duration_seconds": round(duration),
                "performance_metrics": {
                    "overall_score": quality_score,
                    "success_rate": 1.0 if success else 0.0,
                    "efficiency": min(100, 100 - (duration / 60)),  # Simple efficiency calc
                },
            },
            "outcome": {
                "success": success,
                "quality_score": quality_score,
                "tests_passing": 0,  # Could be tracked
                "standards_compliance": quality_score,
                "documentation_coverage": 0,  # Could be tracked
                "errors_encountered": issues_found or [],
                "performance_recorded": True,
                "model_used": self.detect_current_model(),
                "task_completed_at": datetime.now(timezone.utc).isoformat(),
            },
            "insights": {
                "what_worked": ["Automatic performance recording enabled"],
                "what_failed": [] if success else ["Task completion issues"],
                "bottlenecks": [] if duration < 300 else ["Task took longer than expected"],
                "optimization_opportunities": recommendations or [],
                "lessons_learned": [f"Automatic recording successful for {self.current_task['type']} tasks"],
            },
            "reuse_count": 0,
            "last_reused": None,
            "reuse_success_rate": None,
            "performance_metadata": {
                "recorded_by": "automatic_learning_trigger",
                "integration_version": "1.0+",
                "dashboard_compatible": True,
                "auto_triggered": True,
            },
        }

        # Store learning pattern
        self._store_learning_pattern(learning_pattern)

        # Log successful trigger
        self._log_trigger(
            "task_completed_with_recording",
            {
                "task_id": self.current_task["id"],
                "performance_record_id": performance_record["assessment_id"],
                "pattern_id": learning_pattern["task_id"],
                "duration_seconds": round(duration),
                "quality_score": quality_score,
                "success": success,
            },
        )

        # Clear current task
        completed_task = self.current_task.copy()
        self.current_task = None
        self.task_start_time = None

        return {
            "success": True,
            "task": completed_task,
            "performance_record": performance_record,
            "learning_pattern": learning_pattern,
            "message": f"Task completed and performance recorded automatically",
        }

    def _store_performance_record(self, record: Dict[str, Any]):
        """Store performance record in performance_records.json."""
        try:
            # Load existing data
            with open(self.performance_records_file, "r") as f:
                data = json.load(f)

            # Add new record
            data["records"].append(record)
            data["metadata"]["total_records"] = len(data["records"])
            data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()

            # Update summary
            task_type = record["task_type"]
            if "summary" not in data:
                data["summary"] = {}
            if task_type not in data["summary"]:
                data["summary"][task_type] = {"count": 0, "avg_score": 0.0, "success_rate": 0.0}

            summary = data["summary"][task_type]
            summary["count"] += 1

            # Update average score
            total_score = summary["avg_score"] * (summary["count"] - 1) + record["overall_score"]
            summary["avg_score"] = total_score / summary["count"]

            # Update success rate
            successes = summary["success_rate"] * (summary["count"] - 1) + (1.0 if record["pass"] else 0.0)
            summary["success_rate"] = successes / summary["count"]

            # Save data
            with open(self.performance_records_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"ERROR storing performance record: {e}")

    def _store_learning_pattern(self, pattern: Dict[str, Any]):
        """Store learning pattern in patterns.json."""
        try:
            # Load existing data
            with open(self.patterns_file, "r") as f:
                data = json.load(f)

            # Add new pattern
            data["patterns"].append(pattern)
            data["metadata"]["total_tasks"] = len(data["patterns"])
            data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()

            # Save data
            with open(self.patterns_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"ERROR storing learning pattern: {e}")

    def _log_trigger(self, trigger_type: str, details: Dict[str, Any]):
        """Log trigger events for debugging."""
        try:
            # Load existing log
            with open(self.trigger_log_file, "r") as f:
                log_data = json.load(f)

            # Add trigger entry
            trigger_entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "type": trigger_type, "details": details}

            log_data["triggers"].append(trigger_entry)
            log_data["metadata"]["last_trigger"] = trigger_entry["timestamp"]
            log_data["metadata"]["total_triggers"] = len(log_data["triggers"])

            if trigger_type in ["task_completed_with_recording", "performance_recorded"]:
                log_data["metadata"]["successful_triggers"] += 1

            # Save log
            with open(self.trigger_log_file, "w") as f:
                json.dump(log_data, f, indent=2)

        except Exception as e:
            print(f"ERROR logging trigger: {e}")


# Global instance for automatic recording
_auto_trigger = None


def initialize_automatic_recording(patterns_dir: str = ".claude-patterns"):
    """Initialize automatic recording system."""
    global _auto_trigger
    _auto_trigger = AutomaticLearningTrigger(patterns_dir)
    return _auto_trigger


def start_task(task_description: str, task_type: str = "unknown"):
    """Start tracking a task for automatic recording."""
    global _auto_trigger
    if not _auto_trigger:
        initialize_automatic_recording()
    _auto_trigger.start_task_tracking(task_description, task_type)


def complete_task(**kwargs):
    """Complete current task with automatic performance recording."""
    global _auto_trigger
    if not _auto_trigger:
        print("WARNING: No task started. Use start_task() first.")
        return {}
    return _auto_trigger.complete_task_with_recording(**kwargs)


"""
# Example usage for testing
if __name__ == "__main__":
    # Test the automatic recording system
    trigger = initialize_automatic_recording()

    print("Testing automatic learning trigger...")

    # Start a test task
    start_task("Test automatic recording functionality", "testing")

    # Simulate some work
    time.sleep(2)

    # Complete the task with recording
    result = complete_task(
        success=True,
        quality_score=92,
        files_modified=1,
        lines_changed=50,
        skills_used=["automatic-learning", "performance-recording"],
        issues_found=[],
        recommendations=["Continue using automatic recording"],
    )

    print(f"[OK] Automatic recording test completed: {result['message']}")
    print(f"   Performance ID: {result['performance_record']['assessment_id']}")
    print(f"   Pattern ID: {result['learning_pattern']['task_id']}")
    print(f"   Quality Score: {result['performance_record']['overall_score']}")
