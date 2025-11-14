#!/usr/bin/env python3
#     Group Performance Tracking System
"""
Tracks performance metrics at the group level to enable group-level
learning, optimization, and continuous improvement.

This complements agent_performance_tracker.py by aggregating metrics
at the group level for strategic analysis.
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Platform-specific imports for file locking
try:
    import msvcrt  # Windows

    PLATFORM = "windows"
except ImportError:
    import fcntl  # Unix/Linux/Mac

    PLATFORM = "unix"


class GroupPerformanceTracker:
"""
    Tracks performance metrics for agent groups to enable:
"""
    - Group-level performance trends
    - Cross-group comparisons
    - Group specialization identification
    - Optimal workflow identification
"""

    # Group definitions
    GROUPS = {
        1: "Strategic Analysis & Intelligence",
        2: "Decision Making & Planning",
        3: "Execution & Implementation",
        4: "Validation & Optimization",
    }

    # Agent to group mapping
    AGENT_GROUPS = {
        # Group 1
        "code-analyzer": 1,
        "security-auditor": 1,
        "performance-analytics": 1,
        "pr-reviewer": 1,
        "learning-engine": 1,
        # Group 2
        "strategic-planner": 2,
        "preference-coordinator": 2,
        "smart-recommender": 2,
        "orchestrator": 2,
        # Group 3
        "quality-controller": 3,
        "test-engineer": 3,
        "frontend-analyzer": 3,
        "documentation-generator": 3,
        "build-validator": 3,
        "git-repository-manager": 3,
        "api-contract-validator": 3,
        "gui-validator": 3,
        "dev-orchestrator": 3,
        "version-release-manager": 3,
        "workspace-organizer": 3,
        "claude-plugin-validator": 3,
        "background-task-manager": 3,
        "report-management-organizer": 3,
        # Group 4
        "validation-controller": 4,
        "post-execution-validator": 4,
        "performance-optimizer": 4,
        "continuous-improvement": 4,
    }

"""
    def __init__(self, storage_dir: str = ".claude-patterns"):
"""
        Initialize the group performance tracker.

        Args:
            storage_dir: Directory for storing performance data
"""
        self.storage_dir = Path(storage_dir)
        self.performance_file = self.storage_dir / "group_performance.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize performance file if it doesn't exist
        if not self.performance_file.exists():
            self._initialize_performance_storage()

"""
    def _initialize_performance_storage(self):
        """Initialize the performance storage with default structure."""
        initial_data = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "metadata": {"total_tasks_tracked": 0, "tracking_start_date": datetime.now().isoformat()},
            "group_definitions": self.GROUPS,
            "group_metrics": {},
            "task_history_by_group": {},
            "group_specializations": {},
            "workflow_efficiency": {},
            "collaboration_metrics": {},
        }

        # Initialize group metrics
        for group_num in self.GROUPS.keys():
            initial_data["group_metrics"][str(group_num)] = {
                "total_tasks": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "total_execution_time": 0,
                "average_quality_score": 0,
                "quality_scores": [],
                "success_rate": 0,
                "average_execution_time": 0,
                "first_time_success_rate": 0,
                "average_iterations": 0,
                "total_iterations": 0,
                "task_types": {},
                "specializations": [],
                "performance_rating": "Insufficient Data",
                "trend": "insufficient_data",
            }

        self._write_data(initial_data)

    def _lock_file(self, file_handle):
        """Platform-specific file locking."""
        if PLATFORM == "windows":
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX)

    def _unlock_file(self, file_handle):
        """Platform-specific file unlocking."""
        if PLATFORM == "windows":
            try:
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            except (OSError, PermissionError):
                pass
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)

    def _read_data(self) -> Dict[str, Any]:
        """Read performance data with file locking."""
        try:
            with open(self.performance_file, "r", encoding="utf-8") as f:
                self._lock_file(f)
                try:
                    data = json.load(f)
                finally:
                    self._unlock_file(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_performance_storage()
            return self._read_data()

    def _write_data(self, data: Dict[str, Any]):
        """Write performance data with file locking."""
        with open(self.performance_file, "w", encoding="utf-8") as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def record_group_task(
        self,
        group_num: int,
        task_id: str,
        task_type: str,
        success: bool,
        quality_score: float,
        execution_time_seconds: float,
        iterations: int = 1,
        agents_involved: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Record Group Task."""
        Record a task execution for a group.

        Args:
            group_num: Group number (1-4)
            task_id: Unique task identifier
            task_type: Type of task
            success: Whether task was successful
            quality_score: Quality score (0-100)
            execution_time_seconds: Time taken in seconds
            iterations: Number of iterations required
            agents_involved: List of agents from this group involved
            context: Additional context data
"""
        if group_num not in self.GROUPS:
            raise ValueError(f"Invalid group number: {group_num}")

        perf_data = self._read_data()

        group_key = str(group_num)
        group_metrics = perf_data["group_metrics"][group_key]

        # Update metrics
        group_metrics["total_tasks"] += 1
        group_metrics["total_execution_time"] += execution_time_seconds
        group_metrics["total_iterations"] += iterations

        if success:
            group_metrics["successful_tasks"] += 1
        else:
            group_metrics["failed_tasks"] += 1

        # Update quality scores
        group_metrics["quality_scores"].append(quality_score)
        if len(group_metrics["quality_scores"]) > 100:  # Keep last 100
            group_metrics["quality_scores"] = group_metrics["quality_scores"][-100:]

        group_metrics["average_quality_score"] = sum(group_metrics["quality_scores"]) / len(group_metrics["quality_scores"])

        # Update success rate
        group_metrics["success_rate"] = group_metrics["successful_tasks"] / group_metrics["total_tasks"]

        # Update first-time success rate
        first_time_successes = sum(
            1
            for t in perf_data.get("task_history_by_group", {}).get(group_key, [])
            if t.get("iterations", 1) == 1 and t.get("success", False)
        )
        group_metrics["first_time_success_rate"] = (
            first_time_successes / group_metrics["total_tasks"] if group_metrics["total_tasks"] > 0 else 0
        )

        # Update average execution time
        group_metrics["average_execution_time"] = group_metrics["total_execution_time"] / group_metrics["total_tasks"]

        # Update average iterations
        group_metrics["average_iterations"] = group_metrics["total_iterations"] / group_metrics["total_tasks"]

        # Track task types
        if task_type not in group_metrics["task_types"]:
            group_metrics["task_types"][task_type] = 0
        group_metrics["task_types"][task_type] += 1

        # Update performance rating
        group_metrics["performance_rating"] = self._calculate_group_rating(group_metrics)

        # Update trend
        group_metrics["trend"] = self._calculate_trend(group_metrics["quality_scores"])

        # Add to task history
        if group_key not in perf_data["task_history_by_group"]:
            perf_data["task_history_by_group"][group_key] = []

        task_record = {
            "task_id": task_id,
            "group_num": group_num,
            "task_type": task_type,
            "success": success,
            "quality_score": quality_score,
            "execution_time_seconds": execution_time_seconds,
            "iterations": iterations,
            "agents_involved": agents_involved or [],
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
        }

        perf_data["task_history_by_group"][group_key].append(task_record)

        # Keep last 1000 task records per group
        if len(perf_data["task_history_by_group"][group_key]) > 1000:
            perf_data["task_history_by_group"][group_key] = perf_data["task_history_by_group"][group_key][-1000:]

        # Update metadata
        perf_data["metadata"]["total_tasks_tracked"] += 1
        perf_data["metadata"]["last_updated"] = datetime.now().isoformat()

        self._write_data(perf_data)

        # Update specializations
        self._update_group_specializations(group_num)

"""
    def _calculate_group_rating(self, metrics: Dict[str, Any]) -> str:
        """Calculate overall performance rating for a group."""
        if metrics["total_tasks"] < 5:
            return "Insufficient Data"

        quality = metrics["average_quality_score"]
        success_rate = metrics["success_rate"] * 100
        first_time_success = metrics["first_time_success_rate"] * 100

        # Weighted score
        combined_score = (quality * 0.5) + (success_rate * 0.3) + (first_time_success * 0.2)

        if combined_score >= 90:
            return "Excellent"
        elif combined_score >= 80:
            return "Very Good"
        elif combined_score >= 70:
            return "Good"
        elif combined_score >= 60:
            return "Satisfactory"
        else:
            return "Needs Improvement"

    def _calculate_trend(self, scores: List[float]) -> str:
        """Calculate performance trend."""
        if len(scores) < 10:
            return "insufficient_data"

        mid_point = len(scores) // 2
        older_half = scores[:mid_point]
        recent_half = scores[mid_point:]

        avg_older = sum(older_half) / len(older_half)
        avg_recent = sum(recent_half) / len(recent_half)

        if avg_older == 0:
            return "stable"

        change_pct = ((avg_recent - avg_older) / avg_older) * 100

        if change_pct > 5:
            return "improving"
        elif change_pct < -5:
            return "declining"
        else:
            return "stable"

    def _update_group_specializations(self, group_num: int):
        """Update group specializations based on task type performance."""
        perf_data = self._read_data()

        group_key = str(group_num)
        group_metrics = perf_data["group_metrics"][group_key]
        task_types = group_metrics.get("task_types", {})

        if not task_types:
            return

        # Find task types this group excels at
        total_tasks = group_metrics["total_tasks"]
        specializations = []

        for task_type, count in task_types.items():
            if count / total_tasks >= 0.20:  # At least 20% of tasks
                # Calculate success rate for this task type
                task_history = perf_data["task_history_by_group"].get(group_key, [])
                type_tasks = [t for t in task_history if t["task_type"] == task_type]

                if type_tasks:
                    type_success_rate = sum(1 for t in type_tasks if t["success"]) / len(type_tasks)
                    avg_quality = sum(t["quality_score"] for t in type_tasks) / len(type_tasks)

                    specializations.append(
                        {
                            "task_type": task_type,
                            "percentage": (count / total_tasks) * 100,
                            "total_tasks": count,
                            "success_rate": type_success_rate,
                            "average_quality": avg_quality,
                        }
                    )

        group_metrics["specializations"] = sorted(
            specializations, key=lambda x: (x["success_rate"], x["average_quality"]), reverse=True
        )

        self._write_data(perf_data)

    def get_group_performance(self, group_num: int) -> Dict[str, Any]:
        """Get performance metrics for a specific group."""
        if group_num not in self.GROUPS:
            raise ValueError(f"Invalid group number: {group_num}")

        perf_data = self._read_data()
        group_key = str(group_num)
        group_metrics = perf_data["group_metrics"][group_key]

        return {"group_number": group_num, "group_name": self.GROUPS[group_num], **group_metrics}

    def get_all_group_performances(self) -> Dict[int, Dict[str, Any]]:
        """Get performance metrics for all groups."""
        performances = {}
        for group_num in self.GROUPS.keys():
            performances[group_num] = self.get_group_performance(group_num)
        return performances

    def compare_groups():
"""
        
        Compare groups by a specific metric.

        Args:
            metric: Metric to compare (quality_score, success_rate, efficiency)

        Returns:
            List of groups ranked by metric
"""
        all_performances = self.get_all_group_performances()

        comparisons = []
        for group_num, perf in all_performances.items():
            if perf["total_tasks"] < 3:  # Minimum tasks for comparison
                continue

            if metric == "quality_score":
                score = perf["average_quality_score"]
            elif metric == "success_rate":
                score = perf["success_rate"] * 100
            elif metric == "efficiency":
                # Lower execution time and fewer iterations is better
                if perf["average_execution_time"] > 0:
                    score = 100 / (perf["average_execution_time"] / 60)  # Convert to minutes
                else:
                    score = 0
            else:
                score = 0

            comparisons.append(
                {
                    "group_number": group_num,
                    "group_name": self.GROUPS[group_num],
                    "score": score,
                    "total_tasks": perf["total_tasks"],
                }
            )

        return sorted(comparisons, key=lambda x: x["score"], reverse=True)

"""
    def analyze_workflow_efficiency():
"""
        
        Analyze workflow efficiency across groups.

        Returns:
            Workflow efficiency analysis
"""
        perf_data = self._read_data()

        # Typical workflow: G1 → G2 → G3 → G4
        # Analyze how efficiently tasks flow through groups

        # Get task history for all groups
        all_tasks = []
        for group_key, history in perf_data["task_history_by_group"].items():
            all_tasks.extend(history)

        # Group tasks by task_id to track workflow
        task_workflows = defaultdict(list)
        for task in all_tasks:
            task_workflows[task["task_id"]].append(task)

        # Analyze complete workflows
        complete_workflows = []
        for task_id, workflow in task_workflows.items():
            if len(workflow) >= 3:  # At least 3 groups involved
                # Sort by timestamp
                workflow.sort(key=lambda x: x["timestamp"])

                total_time = sum(t["execution_time_seconds"] for t in workflow)
                total_iterations = sum(t["iterations"] for t in workflow)
                groups_involved = [t["group_num"] for t in workflow]
                final_quality = workflow[-1]["quality_score"]

                complete_workflows.append(
                    {
                        "task_id": task_id,
                        "groups_involved": groups_involved,
                        "total_time": total_time,
                        "total_iterations": total_iterations,
                        "final_quality": final_quality,
                        "workflow_pattern": " → ".join([f"G{g}" for g in groups_involved]),
                    }
                )

        if not complete_workflows:
            return {"total_workflows": 0, "message": "Insufficient workflow data"}

        # Calculate efficiency metrics
        avg_time = sum(w["total_time"] for w in complete_workflows) / len(complete_workflows)
        avg_iterations = sum(w["total_iterations"] for w in complete_workflows) / len(complete_workflows)
        avg_quality = sum(w["final_quality"] for w in complete_workflows) / len(complete_workflows)

        # Find most common workflow patterns
        pattern_frequency = defaultdict(int)
        for workflow in complete_workflows:
            pattern_frequency[workflow["workflow_pattern"]] += 1

        most_common_patterns = sorted(pattern_frequency.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "total_workflows": len(complete_workflows),
            "average_total_time": avg_time,
            "average_iterations": avg_iterations,
            "average_final_quality": avg_quality,
            "most_common_patterns": [{"pattern": pattern, "frequency": freq} for pattern, freq in most_common_patterns],
            "efficiency_rating": self._calculate_workflow_efficiency_rating(avg_time, avg_iterations, avg_quality),
        }

"""
    def _calculate_workflow_efficiency_rating(self, avg_time: float, avg_iterations: float, avg_quality: float) -> str:
        """Calculate workflow efficiency rating."""
        # Ideal: Low time, low iterations, high quality
        # Normalize to 0-100 scale

        # Time score (lower is better)
        time_score = max(0, 100 - (avg_time / 60))  # Penalize every minute

        # Iterations score (lower is better)
        iteration_score = max(0, 100 - (avg_iterations - 1) * 20)  # Penalize extra iterations

        # Quality score (higher is better)
        quality_score = avg_quality

        # Combined score
        efficiency_score = (time_score * 0.3) + (iteration_score * 0.3) + (quality_score * 0.4)

        if efficiency_score >= 90:
            return "Excellent"
        elif efficiency_score >= 80:
            return "Very Good"
        elif efficiency_score >= 70:
            return "Good"
        elif efficiency_score >= 60:
            return "Satisfactory"
        else:
            return "Needs Improvement"

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary across all groups."""
        perf_data = self._read_data()

        all_performances = self.get_all_group_performances()

        # Calculate system-wide averages
        total_tasks = sum(p["total_tasks"] for p in all_performances.values())
        avg_quality = (
            sum(p["average_quality_score"] * p["total_tasks"] for p in all_performances.values()) / total_tasks
            if total_tasks > 0
            else 0
        )
        avg_success_rate = (
            sum(p["success_rate"] * p["total_tasks"] for p in all_performances.values()) / total_tasks
            if total_tasks > 0
            else 0
        )

        # Find top and weak performing groups
        quality_ranking = self.compare_groups("quality_score")

        return {
            "total_tasks": total_tasks,
            "average_quality_score": avg_quality,
            "average_success_rate": avg_success_rate * 100,
            "group_count": len(self.GROUPS),
            "top_performing_group": quality_ranking[0] if quality_ranking else None,
            "group_performances": {
                group_num: {
                    "rating": perf["performance_rating"],
                    "quality": perf["average_quality_score"],
                    "success_rate": perf["success_rate"] * 100,
                }
                for group_num, perf in all_performances.items()
            },
            "workflow_efficiency": self.analyze_workflow_efficiency(),
            "tracking_period": {
                "start": perf_data["metadata"]["tracking_start_date"],
                "last_updated": perf_data["metadata"]["last_updated"],
            },
        }


def main():
    """Command-line interface for testing the group performance tracker."""
    import argparse

    parser = argparse.ArgumentParser(description="Group Performance Tracker")
    parser.add_argument("--storage-dir", default=".claude-patterns", help="Storage directory")
    parser.add_argument("--action", choices=["record", "get", "compare", "workflow", "summary"], help="Action to perform")
    parser.add_argument("--group", type=int, help="Group number (1-4)")
    parser.add_argument("--task-id", help="Task ID")
    parser.add_argument("--task-type", help="Task type")
    parser.add_argument("--quality", type=float, help="Quality score")
    parser.add_argument("--success", action="store_true", help="Task successful")
    parser.add_argument("--time", type=float, default=60, help="Execution time in seconds")

    args = parser.parse_args()

    tracker = GroupPerformanceTracker(args.storage_dir)

    if args.action == "record":
        if not all([args.group, args.task_id, args.task_type, args.quality is not None]):
            print("Error: --group, --task-id, --task-type, and --quality required for record")
            sys.exit(1)

        tracker.record_group_task(args.group, args.task_id, args.task_type, args.success, args.quality, args.time)
        print(f"Task recorded for Group {args.group}")

    elif args.action == "get":
        if not args.group:
            print("Error: --group required for get")
            sys.exit(1)

        perf = tracker.get_group_performance(args.group)
        print(f"Group {perf['group_number']}: {perf['group_name']}")
        print(f"  Total Tasks: {perf['total_tasks']}")
        print(f"  Success Rate: {perf['success_rate']*100:.1f}%")
        print(f"  Avg Quality: {perf['average_quality_score']:.1f}")
        print(f"  Rating: {perf['performance_rating']}")

    elif args.action == "compare":
        comparison = tracker.compare_groups("quality_score")
        print("Group Performance Comparison (by quality):")
        for i, group in enumerate(comparison, 1):
            print(f"  {i}. Group {group['group_number']}: {group['score']:.1f}")

    elif args.action == "workflow":
        workflow = tracker.analyze_workflow_efficiency()
        print("Workflow Efficiency Analysis:")
        print(f"  Total Workflows: {workflow['total_workflows']}")
        if workflow["total_workflows"] > 0:
            print(f"  Avg Time: {workflow['average_total_time']:.1f}s")
            print(f"  Avg Quality: {workflow['average_final_quality']:.1f}")
            print(f"  Efficiency Rating: {workflow['efficiency_rating']}")

    elif args.action == "summary":
        summary = tracker.get_performance_summary()
        print("Group Performance Summary:")
        print(f"  Total Tasks: {summary['total_tasks']}")
        print(f"  Avg Quality: {summary['average_quality_score']:.1f}")
        print(f"  Avg Success Rate: {summary['average_success_rate']:.1f}%")
        if summary["top_performing_group"]:
            print(f"  Top Group: {summary['top_performing_group']['group_name']}")

    else:
        # Show summary
        print("Group Performance Tracker Initialized")
        print(f"Storage: {tracker.performance_file}")
        summary = tracker.get_performance_summary()
        print(f"Total Tasks: {summary['total_tasks']}")


if __name__ == "__main__":
    main()
