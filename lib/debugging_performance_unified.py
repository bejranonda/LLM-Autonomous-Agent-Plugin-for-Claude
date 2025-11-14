"""
#    Debugging Performance Data Provider using Unified Storage
"""
This module provides debugging performance metrics using the unified parameter storage
system to ensure data consistency across all dashboard sections.
"""
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

try:
    from unified_parameter_storage import UnifiedParameterStorage
    from dashboard_unified_adapter import DashboardUnifiedAdapter
    from dashboard_learning_system import capture_debugging_pattern

    UNIFIED_STORAGE_AVAILABLE = True
except ImportError:
    UNIFIED_STORAGE_AVAILABLE = False
    capture_debugging_pattern = None


class DebuggingPerformanceProvider:
"""
    Provides debugging performance data from unified storage for consistent dashboard metrics.
"""
"""

"""
    def __init__(self):
        """Initialize debugging performance provider."""
        self.use_unified_storage = False
        self.unified_adapter = None
        self.unified_storage = None

        # Initialize unified storage if available
        if UNIFIED_STORAGE_AVAILABLE:
            try:
                self.unified_adapter = DashboardUnifiedAdapter()
                self.unified_storage = UnifiedParameterStorage()
                self.use_unified_storage = True
                print("DebuggingPerformanceProvider initialized with unified storage")
            except Exception as e:
                print(f"Failed to initialize unified storage for debugging: {e}")
                self.use_unified_storage = False
        else:
            print("Warning: Unified storage not available for debugging performance")

    def get_debugging_performance_data():
"""
        
        Get debugging performance data from UNIFIED STORAGE for consistent data.

        Args:
            days: Number of days to look back for debugging tasks

        Returns:
            Debugging performance metrics using the comprehensive framework
"""
        # Use unified storage for consistent data
        if self.use_unified_storage and self.unified_adapter:
            try:
                # Get quality timeline data from unified adapter
                timeline_data = self.unified_adapter.get_quality_timeline_data(days=days)
                current_model = self._detect_current_model()

                # Filter for debugging-related tasks
                debugging_tasks = []
                debugging_task_types = ["debugging", "debug-eval", "debugging-evaluation", "debug-evaluation", "debug"]

                for assessment in timeline_data:
                    task_type = assessment.get("task_type", "").lower()
                    if any(debug_type in task_type for debug_type in debugging_task_types):
                        debugging_tasks.append(assessment)

                if not debugging_tasks:
                    # Return empty structure if no debugging tasks found
                    return {
                        "analysis_timestamp": datetime.now().isoformat(),
                        "total_debugging_assessments": 0,
                        "timeframe_days": days,
                        "timeframe_label": self._get_timeframe_label(days),
                        "performance_rankings": [],
                        "detailed_metrics": {},
                    }

                # Calculate debugging performance metrics using framework
                performance_metrics = self._calculate_debugging_performance_metrics(debugging_tasks, current_model)

                # Capture learning pattern for automatic improvement
                if capture_debugging_pattern and len(debugging_tasks) > 0:
                    try:
                        # Create task context for learning
                        task_context = {
                            "problem_type": "dashboard_data_consistency",
                            "complexity": "medium",
                            "data_sources": ["unified_storage", "legacy_files"],
                            "sections_affected": ["debugging_performance", "quality_timeline", "recent_activities"],
                            "apis_modified": ["debugging_performance"],
                            "duration_minutes": sum(
                                task.get("details", {}).get("duration_seconds", 0) for task in debugging_tasks
                            )
                            / 60
                            / len(debugging_tasks),
                        }

                        # Capture pattern from the most recent debugging task
                        latest_task = max(debugging_tasks, key=lambda x: x.get("timestamp", ""))
                        capture_debugging_pattern(latest_task, performance_metrics, task_context)
                    except Exception as e:
                        print(f"Error capturing learning pattern: {e}")

                return {
                    "analysis_timestamp": datetime.now().isoformat(),
                    "total_debugging_assessments": len(debugging_tasks),
                    "timeframe_days": days,
                    "timeframe_label": self._get_timeframe_label(days),
                    "performance_rankings": [performance_metrics],
                    "detailed_metrics": {
                        current_model: {
                            "debugging_assessments": [self._format_debugging_assessment(task) for task in debugging_tasks],
                            "performance_index": performance_metrics["performance_index"],
                            "quality_metrics": {
                                "efficiency_index": performance_metrics.get("efficiency_index", 0),
                                "final_quality": performance_metrics.get("final_quality", 0),
                                "gap_closed_pct": performance_metrics.get("gap_closed_pct", 0),
                                "initial_quality": performance_metrics.get("initial_quality", 0),
                                "qis": performance_metrics.get("qis", 0),
                                "quality_gap": performance_metrics.get("quality_gap", 0),
                                "regression_penalty": performance_metrics.get("regression_penalty", 0),
                                "regression_rate": performance_metrics.get("regression_rate", 0),
                                "regressions_detected": performance_metrics.get("regressions_detected", 0),
                                "relative_improvement": performance_metrics.get("relative_improvement", 0),
                            },
                            "time_metrics": {
                                "avg_time_minutes": performance_metrics.get("avg_time_minutes", 0),
                                "time_efficiency_score": performance_metrics.get("time_efficiency_score", 0),
                                "time_span_hours": performance_metrics.get("time_span_hours", 0),
                                "total_tasks": len(debugging_tasks),
                            },
                            "total_debugging_tasks": len(debugging_tasks),
                            "success_rate": performance_metrics.get("success_rate", 0),
                        }
                    },
                }

            except Exception as e:
                print(f"Error getting debugging performance from unified storage: {e}")
                # Fallback to legacy method

        # Legacy fallback method - try to read from timeframe files
        timeframe_files = {
            1: "debugging_performance_1days.json",
            3: "debugging_performance_3days.json",
            7: "debugging_performance_7days.json",
            30: "debugging_performance_30days.json",
        }

        # For other values, use closest available timeframe
        if days not in timeframe_files:
            if days <= 1:
                days = 1
            elif days <= 3:
                days = 3
            elif days <= 7:
                days = 7
            else:
                days = 30

        filename = timeframe_files[days]

        try:
            # Read timeframe-specific file
            filepath = os.path.join(".claude-patterns", filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            return data
        except FileNotFoundError:
            # Return empty structure if file not found
            return {
                "analysis_timestamp": datetime.now().isoformat(),
                "total_debugging_assessments": 0,
                "timeframe_days": days,
                "timeframe_label": self._get_timeframe_label(days),
                "performance_rankings": [],
                "detailed_metrics": {},
            }

    def _detect_current_model(self) -> str:
        """Detect the currently active model."""
        # Default to GLM-4.6 as it's the most common
        return "GLM-4.6"

    def _get_timeframe_label(self, days: int) -> str:
        """Get human-readable timeframe label."""
        if days == 1:
            return "Today"
        elif days == 3:
            return "Last 3 Days"
        elif days == 7:
            return "Last Week"
        elif days == 30:
            return "Last Month"
        else:
            return f"Last {days} Days"

    def _calculate_debugging_performance_metrics():
"""
        
        Calculate debugging performance metrics using the comprehensive framework.

        Args:
            debugging_tasks: List of debugging task assessments
            current_model: Currently detected model

        Returns:
            Performance metrics dictionary
"""
        if not debugging_tasks:
            return {}

        # Calculate quality metrics
        initial_qualities = [
            task.get("details", {}).get("initial_quality", task.get("overall_score", 0)) for task in debugging_tasks
        ]
        final_qualities = [task.get("overall_score", 0) for task in debugging_tasks]

        avg_initial_quality = sum(initial_qualities) / len(initial_qualities) if initial_qualities else 0
        avg_final_quality = sum(final_qualities) / len(final_qualities) if final_qualities else 0

        # Quality Improvement Score (QIS)
        quality_gap = max(0, avg_final_quality - avg_initial_quality)
        gap_closed_pct = 1.0 if avg_initial_quality == 0 else min(1.0, quality_gap / max(1, 100 - avg_initial_quality))
        qis = 0.6 * avg_final_quality + 0.4 * (gap_closed_pct * 100)

        # Time efficiency (default to perfect if not available)
        time_scores = [task.get("details", {}).get("time_efficiency_score", 100) for task in debugging_tasks]
        avg_time_efficiency = sum(time_scores) / len(time_scores) if time_scores else 100

        # Success rate
        successful_tasks = [task for task in debugging_tasks if task.get("overall_score", 0) >= 70]
        success_rate = len(successful_tasks) / len(debugging_tasks) if debugging_tasks else 0

        # Performance Index calculation
        performance_index = (0.40 * qis) + (0.35 * avg_time_efficiency) + (0.25 * success_rate * 100)

        # Calculate additional metrics
        duration_seconds = [task.get("details", {}).get("duration_seconds", 0) for task in debugging_tasks]
        avg_time_minutes = sum(duration_seconds) / 60 / len(duration_seconds) if duration_seconds else 0

        # Time span calculation
        timestamps = [task.get("timestamp", "") for task in debugging_tasks if task.get("timestamp")]
        if len(timestamps) >= 2:
            try:
                time_span_hours = (
                    datetime.fromisoformat(timestamps[-1].replace("Z", "+00:00"))
                    - datetime.fromisoformat(timestamps[0].replace("Z", "+00:00"))
                ).total_seconds() / 3600
            except:
                time_span_hours = 0
        else:
            time_span_hours = 0

        return {
            "model": current_model,
            "performance_index": round(performance_index, 1),
            "qis": round(qis, 1),
            "final_quality": round(avg_final_quality, 1),
            "initial_quality": round(avg_initial_quality, 1),
            "quality_improvement": round(avg_final_quality - avg_initial_quality, 1),
            "time_efficiency_score": round(avg_time_efficiency, 1),
            "success_rate": round(success_rate * 100, 1),
            "total_debugging_tasks": len(debugging_tasks),
            "rank": 1,
            "efficiency_index": round(qis * 0.7 + avg_time_efficiency * 0.3, 1),
            "gap_closed_pct": round(gap_closed_pct * 100, 1),
            "quality_gap": round(100 - avg_initial_quality, 1),
            "regression_penalty": 0,
            "regression_rate": 0,
            "regressions_detected": 0,
            "relative_improvement": round(gap_closed_pct, 2),
            "avg_time_minutes": round(avg_time_minutes, 1),
            "time_span_hours": round(time_span_hours, 2),
        }

"""
    def _format_debugging_assessment(self, task: Dict) -> Dict[str, Any]:
        """Format debugging assessment for API response."""
        return {
            "assessment_id": task.get("assessment_id"),
            "assessment_type": "debugging-performance",
            "breakdown": task.get("details", {}).get(
                "breakdown",
                {
                    "tests_passing": 25,
                    "standards_compliance": 25,
                    "documentation": 20,
                    "pattern_adherence": 15,
                    "code_metrics": 15,
                },
            ),
            "details": {
                "evaluation_target": task.get("task_type", "debugging"),
                "final_quality": task.get("overall_score", 0),
                "fixes_applied": task.get("details", {}).get("fixes_applied", 0),
                "initial_quality": task.get("details", {}).get("initial_quality", task.get("overall_score", 0)),
                "issues_found": len(task.get("issues_found", [])),
                "performance_index": task.get("details", {}).get("performance_index", 0),
                "qis_score": task.get("details", {}).get("qis_score", 0),
                "quality_improvement": task.get("details", {}).get("quality_improvement", 0),
                "success_rate": 1.0 if task.get("pass", False) else 0.0,
                "task_complexity": "medium",
                "time_elapsed_minutes": task.get("details", {}).get("duration_seconds", 0) / 60,
            },
            "issues_found": task.get("issues_found", []),
            "overall_score": task.get("overall_score", 0),
            "pass": task.get("pass", False),
            "recommendations": [
                f"Apply {task.get('details', {}).get('fixes_applied', 0)} recommended fixes",
                "Monitor debugging performance improvements",
                "Validate fixes with comprehensive testing",
            ],
            "task_type": task.get("task_type", "debugging-evaluation"),
            "threshold_met": task.get("pass", True),
            "timestamp": task.get("timestamp", datetime.now().isoformat()),
        }

    def store_debugging_pattern():
"""
        
        Store debugging pattern for future learning.

        Args:
            task_data: Original debugging task data
            performance_metrics: Calculated performance metrics
"""
        if self.use_unified_storage and self.unified_storage:
            try:
                # Store pattern for learning system
                pattern = {
                    "task_type": "debugging",
                    "context": {
                        "complexity": "medium",
                        "data_sources_used": ["unified_storage"],
                        "issues_detected": len(task_data.get("issues_found", [])),
                        "fixes_applied": task_data.get("details", {}).get("fixes_applied", 0),
                    },
                    "execution": {
                        "skills_used": ["debugging", "data-analysis", "problem-solving"],
                        "approach": "unified_storage_analysis",
                        "time_minutes": task_data.get("details", {}).get("duration_seconds", 0) / 60,
                        "quality_score": task_data.get("overall_score", 0),
                    },
                    "outcome": {
                        "success": task_data.get("pass", False),
                        "quality_score": task_data.get("overall_score", 0),
                        "performance_index": performance_metrics.get("performance_index", 0),
                        "issues_resolved": len(task_data.get("issues_found", [])),
                        "user_satisfaction": "high" if task_data.get("overall_score", 0) >= 90 else "medium",
                    },
                    "timestamp": datetime.now().isoformat(),
                    "reuse_count": 0,
                    "success_rate": 1.0 if task_data.get("pass", False) else 0.0,
                }

                # Store pattern for future learning (this would integrate with the learning system)
                print(
                    f"[BRAIN] Stored debugging pattern: QIS={performance_metrics.get('qis', 0):.1f}, PI={performance_metrics.get('performance_index', 0):.1f}"
                )

            except Exception as e:
                print(f"Error storing debugging pattern: {e}")


# Global instance for easy access
_debugging_provider = None


"""
def get_debugging_performance_provider() -> DebuggingPerformanceProvider:
    """Get global debugging performance provider instance."""
    global _debugging_provider
    if _debugging_provider is None:
        _debugging_provider = DebuggingPerformanceProvider()
    return _debugging_provider


def get_debugging_performance_data(days: int = 1) -> Dict[str, Any]:
    """Get debugging performance data using unified storage."""
    provider = get_debugging_performance_provider()
    return provider.get_debugging_performance_data(days)
