#!/usr/bin/env python3
#     Agent Performance Tracking System
    """
Tracks individual agent performance metrics for continuous improvement
and specialization identification.
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


class AgentPerformanceTracker:
    """
    Tracks performance metrics for individual agents to enable:
    """
    - Performance trend analysis
    - Specialization identification
    - Weak agent detection
    - Optimal agent selection
    """

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the agent performance tracker.

        Args:
            storage_dir: Directory for storing performance data
        """
        self.storage_dir = Path(storage_dir)
        self.performance_file = self.storage_dir / "agent_performance.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize performance file if it doesn't exist
        if not self.performance_file.exists():
            self._initialize_performance_storage()

    def _initialize_performance_storage(self):
        """Initialize the performance storage with default structure."""
        initial_data = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "metadata": {"total_tasks_tracked": 0, "agents_active": 0, "tracking_start_date": datetime.now().isoformat()},
            "agent_metrics": {},
            "task_history": [],
            "specializations": {},
            "performance_trends": {},
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
                # File may already be unlocked on Windows
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

    def record_task_execution(
        self,
        agent_name: str,
        task_id: str,
        task_type: str,
        success: bool,
        quality_score: float,
        execution_time_seconds: float,
        recommendations_followed: Optional[int] = None,
        auto_fix_applied: Optional[bool] = None,
        iterations: int = 1,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Record Task Execution."""
        Record a task execution for performance tracking.

        Args:
            agent_name: Name of the agent
            task_id: Unique task identifier
            task_type: Type of task (refactoring, bug-fix, etc.)
            success: Whether task was successful
            quality_score: Quality score (0-100)
            execution_time_seconds: Time taken in seconds
            recommendations_followed: Number of recommendations followed (for analysis agents)
            auto_fix_applied: Whether auto-fix was applied (for execution agents)
            iterations: Number of iterations required
            context: Additional context data
        """
        perf_data = self._read_data()

        # Initialize agent metrics if not exists
        if agent_name not in perf_data["agent_metrics"]:
            perf_data["agent_metrics"][agent_name] = {
                "total_tasks": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "total_execution_time": 0,
                "average_quality_score": 0,
                "quality_scores": [],
                "task_types": defaultdict(int),
                "success_rate": 0,
                "average_execution_time": 0,
                "recommendations_followed_total": 0,
                "auto_fixes_applied": 0,
                "average_iterations": 0,
                "total_iterations": 0,
                "specializations": [],
                "first_task": datetime.now().isoformat(),
                "last_task": datetime.now().isoformat(),
            }

        agent_metrics = perf_data["agent_metrics"][agent_name]

        # Update metrics
        agent_metrics["total_tasks"] += 1
        agent_metrics["total_execution_time"] += execution_time_seconds
        agent_metrics["total_iterations"] += iterations

        if success:
            agent_metrics["successful_tasks"] += 1
        else:
            agent_metrics["failed_tasks"] += 1

        # Update quality scores
        agent_metrics["quality_scores"].append(quality_score)
        if len(agent_metrics["quality_scores"]) > 100:  # Keep last 100
            agent_metrics["quality_scores"] = agent_metrics["quality_scores"][-100:]

        agent_metrics["average_quality_score"] = sum(agent_metrics["quality_scores"]) / len(agent_metrics["quality_scores"])

        # Update success rate
        agent_metrics["success_rate"] = agent_metrics["successful_tasks"] / agent_metrics["total_tasks"]

        # Update average execution time
        agent_metrics["average_execution_time"] = agent_metrics["total_execution_time"] / agent_metrics["total_tasks"]

        # Update average iterations
        agent_metrics["average_iterations"] = agent_metrics["total_iterations"] / agent_metrics["total_tasks"]

        # Track task types
        if isinstance(agent_metrics["task_types"], dict):
            agent_metrics["task_types"][task_type] = agent_metrics["task_types"].get(task_type, 0) + 1

        # Update recommendations followed (for analysis agents)
        if recommendations_followed is not None:
            agent_metrics["recommendations_followed_total"] += recommendations_followed

        # Update auto-fixes (for execution agents)
        if auto_fix_applied:
            agent_metrics["auto_fixes_applied"] += 1

        # Update timestamps
        agent_metrics["last_task"] = datetime.now().isoformat()

        # Add to task history
        task_record = {
            "task_id": task_id,
            "agent_name": agent_name,
            "task_type": task_type,
            "success": success,
            "quality_score": quality_score,
            "execution_time_seconds": execution_time_seconds,
            "iterations": iterations,
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
        }

        perf_data["task_history"].append(task_record)

        # Keep last 1000 task records
        if len(perf_data["task_history"]) > 1000:
            perf_data["task_history"] = perf_data["task_history"][-1000:]

        # Update metadata
        perf_data["metadata"]["total_tasks_tracked"] += 1
        perf_data["metadata"]["agents_active"] = len(perf_data["agent_metrics"])
        perf_data["metadata"]["last_updated"] = datetime.now().isoformat()

        self._write_data(perf_data)

        # Update specializations asynchronously
        self._update_specializations(agent_name)

    def get_agent_performance(self, agent_name: str) -> Dict[str, Any]:
        """Get performance metrics for a specific agent."""
        perf_data = self._read_data()

        if agent_name not in perf_data["agent_metrics"]:
            return {"agent_name": agent_name, "total_tasks": 0, "performance": "No data available"}

        agent_metrics = perf_data["agent_metrics"][agent_name]

        # Calculate additional derived metrics
        performance = {
            "agent_name": agent_name,
            **agent_metrics,
            "performance_rating": self._calculate_performance_rating(agent_metrics),
            "trend": self._calculate_trend(agent_metrics["quality_scores"]),
            "specializations": self._get_agent_specializations(agent_name, perf_data),
        }

        return performance

    def get_all_agent_performances(self) -> Dict[str, Dict[str, Any]]:
        """Get performance metrics for all agents."""
        perf_data = self._read_data()

        all_performances = {}
        for agent_name in perf_data["agent_metrics"]:
            all_performances[agent_name] = self.get_agent_performance(agent_name)

        return all_performances

    def get_top_performers():
        """
        
        Get top performing agents by metric.

        Args:
            metric: Metric to rank by (quality_score, success_rate, efficiency)
            limit: Number of agents to return

        Returns:
            List of top performers
        """
        perf_data = self._read_data()

        performers = []
        for agent_name, metrics in perf_data["agent_metrics"].items():
            if metrics["total_tasks"] < 3:  # Minimum tasks for ranking
                continue

            if metric == "quality_score":
                score = metrics["average_quality_score"]
            elif metric == "success_rate":
                score = metrics["success_rate"] * 100
            elif metric == "efficiency":
                # Lower execution time is better
                score = 100 - min(metrics["average_execution_time"] / 60, 100)
            else:
                score = 0

            performers.append({"agent_name": agent_name, "score": score, "total_tasks": metrics["total_tasks"]})

        return sorted(performers, key=lambda x: x["score"], reverse=True)[:limit]

    def get_weak_performers():
        """
        
        Identify agents performing below threshold.

        Args:
            threshold: Quality score threshold

        Returns:
            List of weak performers
        """
        perf_data = self._read_data()

        weak_performers = []
        for agent_name, metrics in perf_data["agent_metrics"].items():
            if metrics["total_tasks"] < 3:  # Minimum tasks for evaluation
                continue

            if metrics["average_quality_score"] < threshold:
                weak_performers.append(
                    {
                        "agent_name": agent_name,
                        "average_quality_score": metrics["average_quality_score"],
                        "success_rate": metrics["success_rate"],
                        "total_tasks": metrics["total_tasks"],
                        "improvement_needed": threshold - metrics["average_quality_score"],
                    }
                )

        return sorted(weak_performers, key=lambda x: x["average_quality_score"])

    def _calculate_performance_rating(self, metrics: Dict[str, Any]) -> str:
        """Calculate overall performance rating."""
        if metrics["total_tasks"] < 3:
            return "Insufficient Data"

        quality = metrics["average_quality_score"]
        success_rate = metrics["success_rate"] * 100

        combined_score = (quality * 0.7) + (success_rate * 0.3)

        if combined_score >= 90:
            return "Excellent"
        elif combined_score >= 80:
            return "Good"
        elif combined_score >= 70:
            return "Satisfactory"
        elif combined_score >= 60:
            return "Needs Improvement"
        else:
            return "Poor"

    def _calculate_trend(self, scores: List[float]) -> str:
        """Calculate performance trend."""
        if len(scores) < 5:
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

    def _update_specializations(self, agent_name: str):
        """Update agent specializations based on task type performance."""
        perf_data = self._read_data()

        if agent_name not in perf_data["agent_metrics"]:
            return

        agent_metrics = perf_data["agent_metrics"][agent_name]
        task_types = agent_metrics.get("task_types", {})

        if not task_types or not isinstance(task_types, dict):
            return

        # Find task types this agent excels at
        total_tasks = agent_metrics["total_tasks"]
        specializations = []

        for task_type, count in task_types.items():
            if count / total_tasks >= 0.3:  # At least 30% of tasks
                specializations.append(
                    {"task_type": task_type, "percentage": (count / total_tasks) * 100, "total_tasks": count}
                )

        agent_metrics["specializations"] = sorted(specializations, key=lambda x: x["percentage"], reverse=True)

        self._write_data(perf_data)

    def _get_agent_specializations(self, agent_name: str, perf_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get agent specializations."""
        if agent_name not in perf_data["agent_metrics"]:
            return []

        return perf_data["agent_metrics"][agent_name].get("specializations", [])

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary across all agents."""
        perf_data = self._read_data()

        total_agents = len(perf_data["agent_metrics"])
        total_tasks = perf_data["metadata"]["total_tasks_tracked"]

        if total_agents == 0:
            return {"total_agents": 0, "total_tasks": 0, "summary": "No performance data available"}

        # Calculate averages across all agents
        all_quality_scores = []
        all_success_rates = []

        for metrics in perf_data["agent_metrics"].values():
            if metrics["total_tasks"] >= 3:
                all_quality_scores.append(metrics["average_quality_score"])
                all_success_rates.append(metrics["success_rate"])

        avg_quality = sum(all_quality_scores) / len(all_quality_scores) if all_quality_scores else 0
        avg_success_rate = sum(all_success_rates) / len(all_success_rates) if all_success_rates else 0

        summary = {
            "total_agents": total_agents,
            "total_tasks": total_tasks,
            "average_quality_score": avg_quality,
            "average_success_rate": avg_success_rate * 100,
            "top_performers": self.get_top_performers(limit=3),
            "weak_performers": self.get_weak_performers(),
            "tracking_period": {
                "start": perf_data["metadata"]["tracking_start_date"],
                "last_updated": perf_data["metadata"]["last_updated"],
            },
        }

        return summary


def main():
    """Command-line interface for testing the performance tracker."""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Performance Tracker")
    parser.add_argument("--storage-dir", default=".claude-patterns", help="Storage directory")
    parser.add_argument("--action", choices=["record", "get", "top", "weak", "summary"], help="Action to perform")
    parser.add_argument("--agent", help="Agent name")
    parser.add_argument("--task-id", help="Task ID")
    parser.add_argument("--task-type", help="Task type")
    parser.add_argument("--quality", type=float, help="Quality score")
    parser.add_argument("--success", action="store_true", help="Task successful")
    parser.add_argument("--time", type=float, default=60, help="Execution time in seconds")

    args = parser.parse_args()

    tracker = AgentPerformanceTracker(args.storage_dir)

    if args.action == "record":
        if not all([args.agent, args.task_id, args.task_type, args.quality is not None]):
            print("Error: --agent, --task-id, --task-type, and --quality required for record")
            sys.exit(1)

        tracker.record_task_execution(args.agent, args.task_id, args.task_type, args.success, args.quality, args.time)
        print(f"Task recorded for {args.agent}")

    elif args.action == "get":
        if not args.agent:
            print("Error: --agent required for get")
            sys.exit(1)

        perf = tracker.get_agent_performance(args.agent)
        print(f"Performance for {args.agent}:")
        print(f"  Total Tasks: {perf['total_tasks']}")
        print(f"  Success Rate: {perf['success_rate']*100:.1f}%")
        print(f"  Avg Quality: {perf['average_quality_score']:.1f}")
        print(f"  Rating: {perf['performance_rating']}")

    elif args.action == "top":
        top = tracker.get_top_performers()
        print("Top Performers:")
        for i, agent in enumerate(top, 1):
            print(f"  {i}. {agent['agent_name']}: {agent['score']:.1f}")

    elif args.action == "weak":
        weak = tracker.get_weak_performers()
        print(f"Weak Performers ({len(weak)} agents):")
        for agent in weak:
            print(f"  {agent['agent_name']}: {agent['average_quality_score']:.1f} (needs +{agent['improvement_needed']:.1f})")

    elif args.action == "summary":
        summary = tracker.get_performance_summary()
        print("Performance Summary:")
        print(f"  Total Agents: {summary['total_agents']}")
        print(f"  Total Tasks: {summary['total_tasks']}")
        print(f"  Avg Quality: {summary['average_quality_score']:.1f}")
        print(f"  Avg Success Rate: {summary['average_success_rate']:.1f}%")

    else:
        # Show summary
        print("Agent Performance Tracker Initialized")
        print(f"Storage: {tracker.performance_file}")
        summary = tracker.get_performance_summary()
        print(f"Total Agents: {summary['total_agents']}")
        print(f"Total Tasks: {summary['total_tasks']}")


if __name__ == "__main__":
    main()
