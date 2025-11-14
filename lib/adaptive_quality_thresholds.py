#!/usr/bin/env python3
"""
Adaptive Quality Threshold System
Dynamically adjusts quality thresholds based on task type, criticality, and context.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum


class TaskType(Enum):
    """Task type enumeration."""

    SECURITY = "security"
    PRODUCTION = "production"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    EXPLORATORY = "exploratory"
    BUG_FIX = "bug-fix"
    FEATURE = "feature"
    OPTIMIZATION = "optimization"
    MAINTENANCE = "maintenance"


class ProjectPhase(Enum):
    """Project phase enumeration."""

    EXPLORATION = "exploration"
    DEVELOPMENT = "development"
    PRE_RELEASE = "pre-release"
    PRODUCTION = "production"
    MAINTENANCE = "maintenance"


class AdaptiveQualityThresholds:
    """Manages adaptive quality thresholds based on task context.

    Provides dynamic quality standards that adjust based on:
    - Task type (security vs exploratory)
    - Project phase (pre-release vs exploration)
    - Task criticality (user-facing vs internal)
    - Historical context (recent failures increase standards)
"""

    # Base threshold matrix by task type
    BASE_THRESHOLDS = {
        TaskType.SECURITY: 90,
        TaskType.PRODUCTION: 85,
        TaskType.REFACTORING: 80,
        TaskType.BUG_FIX: 82,
        TaskType.FEATURE: 80,
        TaskType.TESTING: 75,
        TaskType.OPTIMIZATION: 78,
        TaskType.DOCUMENTATION: 70,
        TaskType.MAINTENANCE: 75,
        TaskType.EXPLORATORY: 60,
    }

    # Phase multipliers
    PHASE_MULTIPLIERS = {
        ProjectPhase.EXPLORATION: 0.85,  # More lenient in exploration
        ProjectPhase.DEVELOPMENT: 0.95,  # Standard development
        ProjectPhase.PRE_RELEASE: 1.10,  # Stricter before release
        ProjectPhase.PRODUCTION: 1.05,  # Production code
        ProjectPhase.MAINTENANCE: 1.00,  # Maintenance standard
    }

    # Criticality adjustments
    CRITICALITY_ADJUSTMENTS = {
        "critical": 1.15,  # +15% for critical tasks
        "high": 1.08,  # +8% for high priority
        "medium": 1.00,  # Baseline
        "low": 0.92,  # -8% for low priority
        "trivial": 0.85,  # -15% for trivial tasks
    }

"""
    def __init__(self, storage_dir: str = ".claude-patterns"):
"""
        Initialize adaptive quality threshold system.

        Args:
            storage_dir: Directory for storing threshold history
"""
        self.storage_dir = Path(storage_dir)
        self.history_file = self.storage_dir / "quality_thresholds_history.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        if not self.history_file.exists():
            self._initialize_history()

"""
    def _initialize_history(self):
        """Initialize threshold history file."""
        initial_data = {"version": "1.0.0", "threshold_history": [], "recent_failures": [], "adjustments_applied": 0}

        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, indent=2)

    def get_threshold(
        self,
        task_type: str,
        project_phase: Optional[str] = None,
        criticality: str = "medium",
        is_user_facing: bool = False,
        context: Optional[Dict[str, Any]] = None,
    )-> int:
        """Get adaptive quality threshold for a task.

        Args:
            task_type: Type of task (security, testing, exploratory, etc.)
            project_phase: Current project phase
            criticality: Task criticality level
            is_user_facing: Whether task affects user-facing code
            context: Additional context (recent failures, etc.)

        Returns:
            Calculated quality threshold (60-100)
"""
        # Convert string to enum
        try:
            task_enum = TaskType(task_type.lower())
        except ValueError:
            # Default to feature if unknown type
            task_enum = TaskType.FEATURE

        # Get base threshold
        base_threshold = self.BASE_THRESHOLDS[task_enum]

        # Apply phase multiplier
        if project_phase:
            try:
                phase_enum = ProjectPhase(project_phase.lower())
                phase_multiplier = self.PHASE_MULTIPLIERS[phase_enum]
                base_threshold *= phase_multiplier
            except ValueError:
                pass  # Use base threshold if invalid phase

        # Apply criticality adjustment
        criticality_multiplier = self.CRITICALITY_ADJUSTMENTS.get(criticality.lower(), 1.0)
        base_threshold *= criticality_multiplier

        # User-facing code gets +5% stricter
        if is_user_facing:
            base_threshold *= 1.05

        # Check for recent failures
        if context and self._has_recent_failures(context):
            # Increase threshold by 10% after recent failures
            base_threshold *= 1.10

        # Clamp to valid range (60-100)
        threshold = max(60, min(100, int(base_threshold)))

        # Record this decision
        self._record_threshold_decision(
            task_type=task_type,
            threshold=threshold,
            base=self.BASE_THRESHOLDS[task_enum],
            context={
                "project_phase": project_phase,
                "criticality": criticality,
                "is_user_facing": is_user_facing,
                "had_recent_failures": self._has_recent_failures(context) if context else False,
            },
        )

        return threshold

"""
    def get_threshold_with_explanation(
        self,
        task_type: str,
        project_phase: Optional[str] = None,
        criticality: str = "medium",
        is_user_facing: bool = False,
        context: Optional[Dict[str, Any]] = None,
    )-> Dict[str, Any]:
        """Get Threshold With Explanation."""
        Get threshold with detailed explanation of how it was calculated.

        Returns:
            Dictionary with threshold and explanation
"""
        threshold = self.get_threshold(task_type, project_phase, criticality, is_user_facing, context)

        try:
            task_enum = TaskType(task_type.lower())
            base = self.BASE_THRESHOLDS[task_enum]
        except ValueError:
            task_enum = TaskType.FEATURE
            base = self.BASE_THRESHOLDS[task_enum]

        explanation_parts = [f"Base threshold for {task_type}: {base}/100"]

        if project_phase:
            try:
                phase_enum = ProjectPhase(project_phase.lower())
                multiplier = self.PHASE_MULTIPLIERS[phase_enum]
                explanation_parts.append(f"Phase adjustment ({project_phase}): ×{multiplier:.2f}")
            except ValueError:
                pass

        criticality_multiplier = self.CRITICALITY_ADJUSTMENTS.get(criticality.lower(), 1.0)
        if criticality_multiplier != 1.0:
            explanation_parts.append(f"Criticality adjustment ({criticality}): ×{criticality_multiplier:.2f}")

        if is_user_facing:
            explanation_parts.append("User-facing code: ×1.05")

        if context and self._has_recent_failures(context):
            explanation_parts.append("Recent failures detected: ×1.10")

        return {
            "threshold": threshold,
            "base_threshold": base,
            "task_type": task_type,
            "explanation": explanation_parts,
            "rationale": self._get_rationale(threshold, task_type),
        }

"""
    def _get_rationale(self, threshold: int, task_type: str) -> str:
        """Get human-readable rationale for threshold."""
        if threshold >= 90:
            return f"Very high standards required for {task_type} tasks to ensure safety and reliability"
        elif threshold >= 80:
            return f"High quality standards for {task_type} to maintain production readiness"
        elif threshold >= 70:
            return f"Standard quality requirements for {task_type} tasks"
        else:
            return f"Relaxed standards for {task_type} to prioritize speed and exploration"

    def _has_recent_failures(self, context: Optional[Dict[str, Any]]) -> bool:
        """Check if there have been recent failures requiring stricter standards."""
        if not context:
            return False

        # Check context for recent failure indicators
        recent_failures = context.get("recent_failures", [])
        if len(recent_failures) >= 2:  # 2+ failures recently
            return True

        # Check failure rate
        recent_success_rate = context.get("recent_success_rate", 1.0)
        if recent_success_rate < 0.85:  # Below 85% success
            return True

        return False

    def _record_threshold_decision(self, task_type: str, threshold: int, base: int, context: Dict[str, Any]):
        """Record threshold decision for analysis."""
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)

            history["threshold_history"].append(
                {
                    "task_type": task_type,
                    "threshold": threshold,
                    "base_threshold": base,
                    "adjustment": threshold - base,
                    "context": context,
                    "timestamp": self._get_timestamp(),
                }
            )

            # Keep last 100 decisions
            if len(history["threshold_history"]) > 100:
                history["threshold_history"] = history["threshold_history"][-100:]

            history["adjustments_applied"] += 1

            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            # Don't fail if recording fails
            print(f"Warning: Failed to record threshold decision: {e}", file=sys.stderr)

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics on threshold usage."""
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)

            threshold_history = history["threshold_history"]

            if not threshold_history:
                return {"total_decisions": 0, "average_threshold": 0, "most_common_task_type": None}

            thresholds = [d["threshold"] for d in threshold_history]
            task_types = [d["task_type"] for d in threshold_history]

            from collections import Counter

            task_type_counts = Counter(task_types)

            return {
                "total_decisions": len(threshold_history),
                "average_threshold": sum(thresholds) / len(thresholds),
                "min_threshold": min(thresholds),
                "max_threshold": max(thresholds),
                "most_common_task_type": task_type_counts.most_common(1)[0][0] if task_type_counts else None,
                "task_type_distribution": dict(task_type_counts),
            }

        except Exception as e:
            print(f"Error getting statistics: {e}", file=sys.stderr)
            return {"error": str(e)}

    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp."""
        from datetime import datetime

        return datetime.now().isoformat()


def main():
    """Command-line interface for testing adaptive quality thresholds."""
"""
    import argparse

    parser = argparse.ArgumentParser(description="Adaptive Quality Thresholds")
    parser.add_argument("--storage-dir", default=".claude-patterns", help="Storage directory")
    parser.add_argument("--task-type", default="feature", help="Task type")
    parser.add_argument("--phase", help="Project phase")
    parser.add_argument("--criticality", default="medium", help="Task criticality")
    parser.add_argument("--user-facing", action="store_true", help="User-facing task")
    parser.add_argument("--explain", action="store_true", help="Show explanation")
    parser.add_argument("--stats", action="store_true", help="Show statistics")

    args = parser.parse_args()

    system = AdaptiveQualityThresholds(args.storage_dir)

    if args.stats:
        stats = system.get_statistics()
        print("Adaptive Quality Threshold Statistics:")
        print(f"  Total Decisions: {stats.get('total_decisions', 0)}")
        print(f"  Average Threshold: {stats.get('average_threshold', 0):.1f}/100")
        if stats.get("min_threshold"):
            print(f"  Range: {stats['min_threshold']}-{stats['max_threshold']}/100")
        if stats.get("most_common_task_type"):
            print(f"  Most Common Type: {stats['most_common_task_type']}")
    elif args.explain:
        result = system.get_threshold_with_explanation(args.task_type, args.phase, args.criticality, args.user_facing)
        print(f"Quality Threshold: {result['threshold']}/100")
        print(f"\nCalculation:")
        for step in result["explanation"]:
            print(f"  {step}")
        print(f"\nRationale: {result['rationale']}")
    else:
        threshold = system.get_threshold(args.task_type, args.phase, args.criticality, args.user_facing)
        print(f"Quality Threshold for {args.task_type}: {threshold}/100")


if __name__ == "__main__":
    main()
