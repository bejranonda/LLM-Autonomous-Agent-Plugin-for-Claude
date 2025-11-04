#!/usr/bin/env python3
"""
Dashboard Unified Adapter
Integrates the dashboard with the unified parameter storage system
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Import the unified parameter storage
try:
    from unified_parameter_storage import UnifiedParameterStorage
except ImportError:
    print("Error: unified_parameter_storage.py not found", file=sys.stderr)
    sys.exit(1)

class DashboardUnifiedAdapter:
    """
    Adapter layer that provides dashboard-specific data access
    to the unified parameter storage system.
    """

    def __init__(self, storage_dir: str = ".claude-unified"):
        """
        Initialize the dashboard unified adapter.

        Args:
            storage_dir: Directory containing unified parameter storage
        """
        self.storage = UnifiedParameterStorage(storage_dir)
        self.cache = {}
        self.cache_timestamp = 0
        self.cache_ttl = 10  # 10 seconds cache for dashboard

    def _get_cached_data(self, key: str) -> Any:
        """Get cached data if available and fresh."""
        current_time = datetime.now().timestamp()
        if (key in self.cache and
            current_time - self.cache_timestamp < self.cache_ttl):
            return self.cache[key]
        return None

    def _set_cached_data(self, key: str, data: Any):
        """Set cached data with timestamp."""
        self.cache[key] = data
        self.cache_timestamp = datetime.now().timestamp()

    def get_quality_timeline_data(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get quality timeline data for charts.

        Args:
            days: Number of days to include

        Returns:
            List of timeline entries with score, model, and timestamp
        """
        cache_key = f"quality_timeline_{days}"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        try:
            # Read unified data
            unified_data = self.storage._read_data()
            timeline = []

            # Get quality timeline from unified storage
            if "quality" in unified_data and "timeline" in unified_data["quality"]:
                timeline = unified_data["quality"]["timeline"]
            else:
                # Fallback: Build timeline from assessment history
                assessments = unified_data.get("quality", {}).get("assessments", {}).get("history", [])
                for assessment in assessments:
                    timeline_entry = {
                        "timestamp": assessment.get("timestamp"),
                        "score": assessment.get("overall_score", 0),
                        "model_used": assessment.get("details", {}).get("model_used", "Unknown"),
                        "task_type": assessment.get("task_type", "unknown"),
                        "assessment_id": assessment.get("assessment_id")
                    }
                    timeline.append(timeline_entry)

            # Filter by date range and sort
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_timeline = []

            for entry in timeline:
                try:
                    timestamp_str = entry.get("timestamp", "")
                    if not timestamp_str:
                        continue

                    # Handle different timestamp formats
                    if timestamp_str.endswith('Z'):
                        timestamp_str = timestamp_str[:-1] + '+00:00'

                    entry_date = datetime.fromisoformat(timestamp_str)
                    # Make both dates comparable (remove timezone info if needed)
                    if entry_date.tzinfo:
                        entry_date = entry_date.replace(tzinfo=None)

                    if entry_date >= cutoff_date:
                        filtered_timeline.append(entry)
                except (ValueError, AttributeError):
                    continue

            # Sort by timestamp
            filtered_timeline.sort(key=lambda x: x.get("timestamp", ""))

            self._set_cached_data(cache_key, filtered_timeline)
            return filtered_timeline

        except Exception as e:
            print(f"Error getting quality timeline: {e}", file=sys.stderr)
            return []

    def get_model_performance_data(self) -> Dict[str, Any]:
        """
        Get model performance data for dashboard.

        Returns:
            Dictionary with model performance metrics
        """
        cache_key = "model_performance"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        try:
            unified_data = self.storage._read_data()
            model_data = unified_data.get("models", {})

            # Process model performance
            performance = {}
            for model_name, model_stats in model_data.get("performance", {}).items():
                performance[model_name] = {
                    "scores": model_stats.get("scores", []),
                    "success_rate": model_stats.get("success_rate", 0.0),
                    "total_tasks": model_stats.get("total_tasks", 0),
                    "last_updated": model_stats.get("last_updated"),
                    "contribution": model_stats.get("contribution", 0.0)
                }

            # Calculate additional metrics
            for model_name, stats in performance.items():
                scores = stats.get("scores", [])
                if scores:
                    stats["average_score"] = sum(s.get("score", 0) for s in scores) / len(scores)
                    stats["recent_score"] = scores[-1].get("score", 0) if scores else 0
                    # Calculate actual trend from score history
                    score_values = [s.get("score", 0) for s in scores]
                    stats["score_trend"] = self._calculate_trend(score_values)
                else:
                    stats["average_score"] = 0.0
                    stats["recent_score"] = 0.0
                    stats["score_trend"] = "no_data"

            result = {
                "active_model": model_data.get("active_model", "Unknown"),
                "models": performance,
                "usage_stats": model_data.get("usage_stats", {}),
                "total_models": len(performance)
            }

            self._set_cached_data(cache_key, result)
            return result

        except Exception as e:
            print(f"Error getting model performance: {e}", file=sys.stderr)
            return {"active_model": "Unknown", "models": {}, "usage_stats": {}, "total_models": 0}

    def get_quality_metrics(self) -> Dict[str, Any]:
        """
        Get current quality metrics for dashboard.

        Returns:
            Dictionary with current quality metrics
        """
        cache_key = "quality_metrics"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        try:
            unified_data = self.storage._read_data()
            quality_data = unified_data.get("quality", {})

            # Get current assessment
            current_assessment = quality_data.get("assessments", {}).get("current", {})

            # Get historical data for statistics
            history = quality_data.get("assessments", {}).get("history", [])
            statistics = quality_data.get("assessments", {}).get("statistics", {})

            # Calculate metrics
            current_score = current_assessment.get("overall_score", 0)
            scores = [a.get("overall_score", 0) for a in history if a.get("overall_score")]

            metrics = {
                "current_score": current_score,
                "current_assessment": current_assessment,
                "total_assessments": len(history),
                "average_score": statistics.get("average_score", sum(scores) / len(scores) if scores else 0),
                "pass_rate": statistics.get("pass_rate", 0),
                "latest_timestamp": current_assessment.get("timestamp"),
                "trend_direction": self._calculate_trend(scores),
                "score_distribution": self._calculate_score_distribution(scores),
                "recent_performance": self._calculate_recent_performance(scores)
            }

            self._set_cached_data(cache_key, metrics)
            return metrics

        except Exception as e:
            print(f"Error getting quality metrics: {e}", file=sys.stderr)
            return {"current_score": 0, "total_assessments": 0, "average_score": 0, "pass_rate": 0}

    def get_learning_analytics(self) -> Dict[str, Any]:
        """
        Get learning analytics for dashboard.

        Returns:
            Dictionary with learning analytics data
        """
        cache_key = "learning_analytics"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        try:
            unified_data = self.storage._read_data()
            learning_data = unified_data.get("learning", {})

            patterns = learning_data.get("patterns", {})
            pattern_list = patterns.get("patterns", [])
            skill_effectiveness = patterns.get("skill_effectiveness", {})
            agent_performance = patterns.get("agent_performance", {})

            # Calculate learning trend from pattern success rates over time
            pattern_success_values = []
            for pattern in pattern_list:
                quality_score = pattern.get("outcome", {}).get("quality_score", 0)
                if quality_score > 0:
                    pattern_success_values.append(quality_score)

            analytics = {
                "total_patterns": len(pattern_list),
                "skill_effectiveness": skill_effectiveness,
                "agent_performance": agent_performance,
                "project_context": patterns.get("project_context", {}),
                "recent_patterns": pattern_list[-10:],  # Last 10 patterns
                "pattern_success_rate": self._calculate_pattern_success_rate(pattern_list),
                "top_skills": self._get_top_skills(skill_effectiveness),
                "learning_trend": self._calculate_trend(pattern_success_values)
            }

            self._set_cached_data(cache_key, analytics)
            return analytics

        except Exception as e:
            print(f"Error getting learning analytics: {e}", file=sys.stderr)
            return {"total_patterns": 0, "skill_effectiveness": {}, "agent_performance": {}}

    def get_validation_status(self) -> Dict[str, Any]:
        """
        Get validation status for dashboard.

        Returns:
            Dictionary with validation status information
        """
        cache_key = "validation_status"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        try:
            unified_data = self.storage._read_data()
            validation_data = unified_data.get("validation", {})

            recent_validations = validation_data.get("recent_validations", [])
            plugin_validations = validation_data.get("plugin_validations", [])
            compliance_status = validation_data.get("compliance_status", {})

            # Get latest validation results
            latest_validation = recent_validations[-1] if recent_validations else {}
            latest_plugin_validation = plugin_validations[-1] if plugin_validations else {}

            # Calculate validation trend from historical scores
            validation_scores = [v.get("overall_score", 0) for v in recent_validations
                               if v.get("overall_score", 0) > 0]

            status = {
                "latest_validation": latest_validation,
                "latest_plugin_validation": latest_plugin_validation,
                "compliance_status": compliance_status,
                "total_validations": len(recent_validations),
                "plugin_validation_count": len(plugin_validations),
                "validation_score": latest_validation.get("overall_score", 0),
                "plugin_ready": latest_plugin_validation.get("overall_score", 0) >= 70,
                "last_validation_time": latest_validation.get("timestamp"),
                "validation_trend": self._calculate_trend(validation_scores)
            }

            self._set_cached_data(cache_key, status)
            return status

        except Exception as e:
            print(f"Error getting validation status: {e}", file=sys.stderr)
            return {"validation_score": 0, "total_validations": 0, "plugin_ready": False}

    def get_agent_feedback_metrics(self) -> Dict[str, Any]:
        """
        Get agent feedback and collaboration metrics.

        Returns:
            Dictionary with feedback metrics
        """
        cache_key = "agent_feedback_metrics"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        try:
            unified_data = self.storage._read_data()
            feedback_data = unified_data.get("agent_feedback", {})

            metrics = {
                "total_feedbacks": len(feedback_data.get("exchanges", [])),
                "collaboration_matrix": feedback_data.get("collaboration_matrix", {}),
                "learning_insights": feedback_data.get("learning_insights", {}),
                "effectiveness_metrics": feedback_data.get("effectiveness_metrics", {}),
                "recent_feedbacks": feedback_data.get("exchanges", [])[-10:] if feedback_data.get("exchanges") else []
            }

            self._set_cached_data(cache_key, metrics)
            return metrics

        except Exception as e:
            print(f"Error getting agent feedback metrics: {e}", file=sys.stderr)
            return {"total_feedbacks": 0}

    def get_agent_performance_metrics(self) -> Dict[str, Any]:
        """
        Get agent performance metrics and trends.

        Returns:
            Dictionary with agent performance data
        """
        cache_key = "agent_performance_metrics"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        try:
            unified_data = self.storage._read_data()
            performance_data = unified_data.get("agent_performance", {})

            metrics = {
                "individual_metrics": performance_data.get("individual_metrics", {}),
                "top_performers": performance_data.get("top_performers", []),
                "weak_performers": performance_data.get("weak_performers", []),
                "specializations": performance_data.get("specializations", {}),
                "performance_trends": performance_data.get("performance_trends", {}),
                "recent_tasks": performance_data.get("task_history", [])[-20:] if performance_data.get("task_history") else []
            }

            self._set_cached_data(cache_key, metrics)
            return metrics

        except Exception as e:
            print(f"Error getting agent performance metrics: {e}", file=sys.stderr)
            return {"individual_metrics": {}}

    def get_user_preference_summary(self) -> Dict[str, Any]:
        """
        Get user preference learning summary.

        Returns:
            Dictionary with user preferences
        """
        cache_key = "user_preference_summary"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        try:
            unified_data = self.storage._read_data()
            pref_data = unified_data.get("user_preferences", {})

            summary = {
                "learning_confidence": pref_data.get("learning_confidence", 0.0),
                "coding_style": pref_data.get("coding_style", {}),
                "workflow_preferences": pref_data.get("workflow_preferences", {}),
                "quality_weights": pref_data.get("quality_weights", {}),
                "communication_style": pref_data.get("communication_style", {}),
                "task_preferences": pref_data.get("task_preferences", {}),
                "total_interactions": len(pref_data.get("interaction_history", []))
            }

            self._set_cached_data(cache_key, summary)
            return summary

        except Exception as e:
            print(f"Error getting user preference summary: {e}", file=sys.stderr)
            return {"learning_confidence": 0.0}

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard summary.

        Returns:
            Dictionary with all dashboard data
        """
        cache_key = "dashboard_summary"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        try:
            # Collect all dashboard data
            summary = {
                "timestamp": datetime.now().isoformat(),
                "quality_metrics": self.get_quality_metrics(),
                "model_performance": self.get_model_performance_data(),
                "quality_timeline": self.get_quality_timeline_data(30),
                "learning_analytics": self.get_learning_analytics(),
                "validation_status": self.get_validation_status(),
                "system_health": self._calculate_system_health(),
                # NEW: Two-tier agent architecture metrics
                "agent_feedback": self.get_agent_feedback_metrics(),
                "agent_performance": self.get_agent_performance_metrics(),
                "user_preferences": self.get_user_preference_summary()
            }

            self._set_cached_data(cache_key, summary)
            return summary

        except Exception as e:
            print(f"Error getting dashboard summary: {e}", file=sys.stderr)
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def _calculate_score_distribution(self, scores: List[float]) -> Dict[str, int]:
        """Calculate score distribution across ranges."""
        if not scores:
            return {"0-20": 0, "21-40": 0, "41-60": 0, "61-80": 0, "81-100": 0}

        distribution = {"0-20": 0, "21-40": 0, "41-60": 0, "61-80": 0, "81-100": 0}

        for score in scores:
            if score <= 20:
                distribution["0-20"] += 1
            elif score <= 40:
                distribution["21-40"] += 1
            elif score <= 60:
                distribution["41-60"] += 1
            elif score <= 80:
                distribution["61-80"] += 1
            else:
                distribution["81-100"] += 1

        return distribution

    def _calculate_recent_performance(self, scores: List[float]) -> Dict[str, float]:
        """Calculate recent performance metrics."""
        if not scores:
            return {"last_7": 0, "last_30": 0, "improvement": 0}

        # Get recent scores
        recent_7 = scores[-7:] if len(scores) >= 7 else scores
        recent_30 = scores[-30:] if len(scores) >= 30 else scores

        avg_7 = sum(recent_7) / len(recent_7) if recent_7 else 0
        avg_30 = sum(recent_30) / len(recent_30) if recent_30 else 0

        # Calculate improvement (compare recent 7 vs previous 7)
        improvement = 0
        if len(scores) >= 14:
            previous_7 = scores[-14:-7]
            avg_previous = sum(previous_7) / len(previous_7) if previous_7 else 0
            improvement = avg_7 - avg_previous

        return {
            "last_7": avg_7,
            "last_30": avg_30,
            "improvement": improvement
        }

    def _calculate_pattern_success_rate(self, patterns: List[Dict[str, Any]]) -> float:
        """Calculate overall pattern success rate."""
        if not patterns:
            return 0.0

        successful_patterns = sum(1 for p in patterns
                                 if p.get("outcome", {}).get("success", False))
        return successful_patterns / len(patterns)

    def _get_top_skills(self, skill_effectiveness: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get top performing skills."""
        if not skill_effectiveness:
            return []

        # Convert to list and sort by effectiveness
        skills = []
        for skill, data in skill_effectiveness.items():
            if isinstance(data, dict):
                effectiveness = data.get("success_rate", data.get("effectiveness", 0))
                # Ensure effectiveness is a number
                try:
                    effectiveness = float(effectiveness) if effectiveness is not None else 0.0
                except (ValueError, TypeError):
                    effectiveness = 0.0
                skills.append({"skill": skill, "effectiveness": effectiveness})

        return sorted(skills, key=lambda x: x["effectiveness"], reverse=True)[:5]

    def _calculate_trend(self, values: List[float], min_data_points: int = 3) -> str:
        """
        Calculate trend direction based on historical values.

        Args:
            values: List of numerical values ordered chronologically
            min_data_points: Minimum data points required for trend calculation

        Returns:
            Trend direction: "improving", "declining", "stable", or "no_data"
        """
        if not values or len(values) < min_data_points:
            return "no_data"

        # Compare recent half vs older half
        mid_point = len(values) // 2
        older_half = values[:mid_point]
        recent_half = values[mid_point:]

        if not older_half or not recent_half:
            return "stable"

        avg_older = sum(older_half) / len(older_half)
        avg_recent = sum(recent_half) / len(recent_half)

        # Calculate percentage change
        if avg_older == 0:
            return "stable"

        change_pct = ((avg_recent - avg_older) / avg_older) * 100

        # Classify trend based on change threshold
        if change_pct > 5:  # More than 5% improvement
            return "improving"
        elif change_pct < -5:  # More than 5% decline
            return "declining"
        else:
            return "stable"

    def _calculate_system_health(self) -> Dict[str, Any]:
        """Calculate overall system health metrics."""
        try:
            unified_data = self.storage._read_data()

            # Basic health checks
            health = {
                "storage_accessible": True,
                "data_integrity": 100.0,
                "last_updated": unified_data.get("metadata", {}).get("last_updated"),
                "version": unified_data.get("version", "unknown"),
                "migration_status": unified_data.get("metadata", {}).get("migration_status", "unknown"),
                "total_records": unified_data.get("metadata", {}).get("total_records_migrated", 0)
            }

            # Calculate data completeness
            sections = ["quality", "models", "learning", "validation", "autofix"]
            complete_sections = sum(1 for section in sections if section in unified_data)
            health["data_completeness"] = (complete_sections / len(sections)) * 100

            # Overall health score
            health["overall_score"] = (health["data_integrity"] + health["data_completeness"]) / 2

            return health

        except Exception as e:
            return {
                "storage_accessible": False,
                "data_integrity": 0,
                "overall_score": 0,
                "error": str(e)
            }

    def invalidate_cache(self):
        """Invalidate all cached data."""
        self.cache.clear()
        self.cache_timestamp = 0

def main():
    """Command-line interface for testing the adapter."""
    import argparse

    parser = argparse.ArgumentParser(description='Dashboard Unified Adapter Test')
    parser.add_argument('--storage-dir', default='.claude-unified', help='Storage directory')
    parser.add_argument('--test', choices=['timeline', 'models', 'quality', 'learning', 'validation', 'summary'],
                       help='Test specific data retrieval')

    args = parser.parse_args()

    adapter = DashboardUnifiedAdapter(args.storage_dir)

    if args.test == 'timeline':
        data = adapter.get_quality_timeline_data()
        print(f"Quality Timeline Entries: {len(data)}")
        for entry in data[-3:]:  # Show last 3
            print(f"  {entry['timestamp']}: {entry['score']} ({entry['model_used']})")

    elif args.test == 'models':
        data = adapter.get_model_performance_data()
        print(f"Active Model: {data['active_model']}")
        print(f"Total Models: {data['total_models']}")
        for model, stats in data['models'].items():
            print(f"  {model}: {stats['success_rate']:.1%} success rate")

    elif args.test == 'quality':
        data = adapter.get_quality_metrics()
        print(f"Current Score: {data['current_score']}")
        print(f"Total Assessments: {data['total_assessments']}")
        print(f"Average Score: {data['average_score']:.1f}")

    elif args.test == 'learning':
        data = adapter.get_learning_analytics()
        print(f"Total Patterns: {data['total_patterns']}")
        print(f"Top Skills: {len(data['top_skills'])}")

    elif args.test == 'validation':
        data = adapter.get_validation_status()
        print(f"Latest Validation Score: {data['validation_score']}")
        print(f"Plugin Ready: {data['plugin_ready']}")
        print(f"Total Validations: {data['total_validations']}")

    elif args.test == 'summary':
        data = adapter.get_dashboard_summary()
        print(f"Dashboard Summary Generated at: {data['timestamp']}")
        print(f"System Health: {data['system_health']['overall_score']:.1f}%")
        print(f"Current Quality Score: {data['quality_metrics']['current_score']}")

    else:
        # Test all
        print("Testing Dashboard Unified Adapter...")
        summary = adapter.get_dashboard_summary()
        print(f"✅ Summary generated successfully")
        print(f"   System Health: {summary['system_health']['overall_score']:.1f}%")
        print(f"   Quality Score: {summary['quality_metrics']['current_score']}")
        print(f"   Active Model: {summary['model_performance']['active_model']}")
        print(f"   Timeline Entries: {len(summary['quality_timeline'])}")

if __name__ == '__main__':
    main()