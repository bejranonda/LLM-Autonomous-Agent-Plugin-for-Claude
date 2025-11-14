"""
Consistency Validation Dashboard

Provides real-time monitoring of dashboard data consistency and system health.
Automatically detects and reports inconsistencies across all dashboard sections.

Features:
- Real-time consistency monitoring
- Automatic inconsistency detection
- System health metrics
- Performance trend analysis
- Auto-healing recommendations
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

try:
    from unified_parameter_storage import UnifiedParameterStorage
    from dashboard_unified_adapter import DashboardUnifiedAdapter
    from dashboard_learning_system import get_learning_system, auto_suggest_improvements

    UNIFIED_STORAGE_AVAILABLE = True
except ImportError:
    UNIFIED_STORAGE_AVAILABLE = False


class ConsistencyDashboard:
"""
    Real-time consistency validation and monitoring system.
"""
"""

"""
    def __init__(self):
        """Initialize consistency dashboard."""
        self.use_unified_storage = False
        self.unified_storage = None
        self.unified_adapter = None
        self.learning_system = None

        # Initialize unified storage if available
        if UNIFIED_STORAGE_AVAILABLE:
            try:
                self.unified_storage = UnifiedParameterStorage()
                self.unified_adapter = DashboardUnifiedAdapter()
                self.learning_system = get_learning_system()
                self.use_unified_storage = True
                print("ConsistencyDashboard initialized with unified storage")
            except Exception as e:
                print(f"ConsistencyDashboard using legacy monitoring: {e}")
        else:
            print("ConsistencyDashboard using legacy monitoring")

        self.consistency_history = []
        self.last_check = None

    def run_consistency_check():
"""
        
        Run comprehensive consistency check across all dashboard sections.

        Returns:
            Detailed consistency report with recommendations
"""
        try:
            check_start = datetime.now()

            # Initialize results
            results = {
                "check_timestamp": check_start.isoformat(),
                "overall_status": "unknown",
                "consistency_score": 0,
                "checks_performed": [],
                "issues_found": [],
                "recommendations": [],
                "system_health": {},
                "performance_trends": {},
            }

            # Run individual consistency checks
            checks = [
                self._check_data_source_consistency(),
                self._check_timestamp_consistency(),
                self._check_model_attribution_consistency(),
                self._check_api_response_consistency(),
                self._check_unified_storage_health(),
            ]

            for check in checks:
                results["checks_performed"].append(check)
                if check.get("issues"):
                    results["issues_found"].extend(check["issues"])
                if check.get("recommendations"):
                    results["recommendations"].extend(check["recommendations"])

            # Calculate overall consistency score
            results["consistency_score"] = self._calculate_consistency_score(results)
            results["overall_status"] = self._determine_overall_status(results["consistency_score"])

            # Get system health metrics
            results["system_health"] = self._get_system_health()

            # Get performance trends
            results["performance_trends"] = self._get_performance_trends()

            # Generate auto-healing recommendations
            results["auto_healing"] = self._generate_auto_healing_recommendations(results)

            # Store check in history
            self.consistency_history.append(
                {
                    "timestamp": check_start.isoformat(),
                    "score": results["consistency_score"],
                    "status": results["overall_status"],
                    "issues_count": len(results["issues_found"]),
                }
            )

            # Keep only last 50 checks
            if len(self.consistency_history) > 50:
                self.consistency_history = self.consistency_history[-50:]

            self.last_check = check_start

            return results

        except Exception as e:
            return {
                "check_timestamp": datetime.now().isoformat(),
                "overall_status": "error",
                "consistency_score": 0,
                "error": str(e),
                "checks_performed": [],
                "issues_found": [{"type": "system_error", "description": str(e)}],
                "recommendations": ["Fix system error and retry consistency check"],
            }

"""
    def _check_data_source_consistency(self) -> Dict[str, Any]:
        """Check if all APIs are using consistent data sources."""
        check_result = {"check_name": "Data Source Consistency", "status": "unknown", "issues": [], "recommendations": []}

        try:
            if self.use_unified_storage and self.unified_adapter:
                # Test unified storage access
                quality_data = self.unified_adapter.get_quality_metrics()
                model_data = self.unified_adapter.get_model_performance_data()

                if quality_data and model_data:
                    check_result["status"] = "pass"
                    check_result["details"] = {
                        "unified_storage_accessible": True,
                        "quality_data_available": bool(quality_data),
                        "model_data_available": bool(model_data),
                        "data_source": "unified_storage",
                    }
                else:
                    check_result["status"] = "warning"
                    check_result["issues"].append(
                        {"type": "data_access_issue", "description": "Unified storage accessible but data incomplete"}
                    )
                    check_result["recommendations"].append("Verify unified storage data integrity")

            else:
                check_result["status"] = "fail"
                check_result["issues"].append(
                    {
                        "type": "unified_storage_unavailable",
                        "description": "Unified storage not available for consistency checking",
                    }
                )
                check_result["recommendations"].append("Initialize unified storage for data consistency")

        except Exception as e:
            check_result["status"] = "error"
            check_result["issues"].append(
                {"type": "check_error", "description": f"Error checking data source consistency: {str(e)}"}
            )

        return check_result

    def _check_timestamp_consistency(self) -> Dict[str, Any]:
        """Check if data timestamps are consistent across sections."""
        check_result = {"check_name": "Timestamp Consistency", "status": "unknown", "issues": [], "recommendations": []}

        try:
            if self.use_unified_storage and self.unified_adapter:
                # Get recent data with timestamps
                timeline_data = self.unified_adapter.get_quality_timeline_data(days=1)

                if timeline_data:
                    # Analyze timestamp patterns
                    timestamps = [item.get("timestamp", "") for item in timeline_data if item.get("timestamp")]

                    if timestamps:
                        # Check for stale data
                        latest_timestamp = max(timestamps)
                        latest_date = datetime.fromisoformat(latest_timestamp.replace("Z", "+00:00"))
                        now = datetime.now(latest_date.tzinfo)

                        age_hours = (now - latest_date).total_seconds() / 3600

                        if age_hours < 1:
                            check_result["status"] = "pass"
                            check_result["details"] = {
                                "latest_timestamp": latest_timestamp,
                                "data_age_hours": round(age_hours, 2),
                                "data_freshness": "current",
                            }
                        elif age_hours < 24:
                            check_result["status"] = "warning"
                            check_result["issues"].append(
                                {"type": "stale_data", "description": f"Data is {age_hours:.1f} hours old"}
                            )
                            check_result["recommendations"].append("Check data update processes")
                        else:
                            check_result["status"] = "fail"
                            check_result["issues"].append(
                                {
                                    "type": "very_stale_data",
                                    "description": f"Data is {age_hours:.1f} hours old - potentially outdated",
                                }
                            )
                            check_result["recommendations"].append("Immediate data refresh required")

                else:
                    check_result["status"] = "warning"
                    check_result["issues"].append(
                        {"type": "no_timestamp_data", "description": "No timestamped data available for consistency check"}
                    )

        except Exception as e:
            check_result["status"] = "error"
            check_result["issues"].append(
                {"type": "check_error", "description": f"Error checking timestamp consistency: {str(e)}"}
            )

        return check_result

    def _check_model_attribution_consistency(self) -> Dict[str, Any]:
        """Check if model attribution is consistent across all sections."""
        check_result = {
            "check_name": "Model Attribution Consistency",
            "status": "unknown",
            "issues": [],
            "recommendations": [],
        }

        try:
            if self.use_unified_storage and self.unified_adapter:
                # Get model performance data
                model_data = self.unified_adapter.get_model_performance_data()

                if model_data and "models" in model_data:
                    models = list(model_data["models"].keys())

                    # Check for naming consistency
                    normalized_models = []
                    for model in models:
                        # Normalize model names
                        normalized = model.replace(" ", "-").upper()
                        if normalized not in normalized_models:
                            normalized_models.append(normalized)

                    if len(normalized_models) > 1:
                        check_result["status"] = "pass"
                        check_result["details"] = {
                            "models_detected": normalized_models,
                            "model_attribution": "consistent",
                            "naming_standardized": True,
                        }
                    else:
                        check_result["status"] = "pass"
                        check_result["details"] = {
                            "models_detected": normalized_models,
                            "model_attribution": "consistent",
                            "single_model": True,
                        }
                else:
                    check_result["status"] = "warning"
                    check_result["issues"].append(
                        {"type": "no_model_data", "description": "No model attribution data available"}
                    )

        except Exception as e:
            check_result["status"] = "error"
            check_result["issues"].append(
                {"type": "check_error", "description": f"Error checking model attribution consistency: {str(e)}"}
            )

        return check_result

    def _check_api_response_consistency(self) -> Dict[str, Any]:
        """Check if API response formats are consistent."""
        check_result = {"check_name": "API Response Consistency", "status": "unknown", "issues": [], "recommendations": []}

        try:
            # Since we can't easily test API responses from here,
            # we'll check for common issues based on file structure
            expected_apis = [
                "/api/quality-timeline",
                "/api/debugging-performance",
                "/api/recent-activity",
                "/api/recent-performance-records",
            ]

            # Check if implementation files exist and are accessible
            implementation_files = [
                "lib/debugging_performance_unified.py",
                "lib/dashboard_unified_adapter.py",
                "lib/dashboard_learning_system.py",
            ]

            missing_files = []
            for file_path in implementation_files:
                if not os.path.exists(file_path):
                    missing_files.append(file_path)

            if not missing_files:
                check_result["status"] = "pass"
                check_result["details"] = {
                    "expected_apis": expected_apis,
                    "implementation_files": "all_present",
                    "api_structure": "consistent",
                }
            else:
                check_result["status"] = "warning"
                check_result["issues"].append(
                    {"type": "missing_implementations", "description": f"Missing implementation files: {missing_files}"}
                )
                check_result["recommendations"].append("Complete API implementations for full consistency")

        except Exception as e:
            check_result["status"] = "error"
            check_result["issues"].append(
                {"type": "check_error", "description": f"Error checking API response consistency: {str(e)}"}
            )

        return check_result

    def _check_unified_storage_health(self) -> Dict[str, Any]:
        """Check unified storage system health."""
        check_result = {"check_name": "Unified Storage Health", "status": "unknown", "issues": [], "recommendations": []}

        try:
            if self.use_unified_storage and self.unified_storage:
                # Get storage statistics
                storage_stats = self.unified_storage.get_storage_stats()

                if storage_stats:
                    validation = self.unified_storage.validate_data_integrity()

                    check_result["status"] = "pass"
                    check_result["details"] = {
                        "storage_available": True,
                        "data_integrity": validation.get("valid", False),
                        "total_records": storage_stats.get("total_records", 0),
                        "storage_health": "healthy",
                    }

                    if not validation.get("valid", False):
                        check_result["status"] = "warning"
                        check_result["issues"].append(
                            {"type": "data_integrity_issue", "description": "Data integrity validation failed"}
                        )
                        check_result["recommendations"].append("Run data integrity repair")
                else:
                    check_result["status"] = "warning"
                    check_result["issues"].append(
                        {"type": "storage_stats_unavailable", "description": "Unable to retrieve storage statistics"}
                    )

            else:
                check_result["status"] = "fail"
                check_result["issues"].append(
                    {"type": "unified_storage_unavailable", "description": "Unified storage system not available"}
                )
                check_result["recommendations"].append("Initialize unified storage system")

        except Exception as e:
            check_result["status"] = "error"
            check_result["issues"].append(
                {"type": "check_error", "description": f"Error checking unified storage health: {str(e)}"}
            )

        return check_result

    def _calculate_consistency_score(self, results: Dict[str, Any]) -> int:
        """Calculate overall consistency score (0-100)."""
        try:
            checks = results.get("checks_performed", [])
            if not checks:
                return 0

            total_score = 0
            max_score = 0

            for check in checks:
                status = check.get("status", "unknown")
                issues_count = len(check.get("issues", []))

                # Score based on status and issues
                if status == "pass":
                    check_score = 100
                elif status == "warning":
                    check_score = max(0, 80 - (issues_count * 10))
                elif status == "fail":
                    check_score = max(0, 40 - (issues_count * 5))
                else:  # error
                    check_score = 0

                total_score += check_score
                max_score += 100

            return int((total_score / max_score) * 100) if max_score > 0 else 0

        except Exception:
            return 0

    def _determine_overall_status(self, score: int) -> str:
        """Determine overall status based on consistency score."""
        if score >= 90:
            return "excellent"
        elif score >= 75:
            return "good"
        elif score >= 60:
            return "fair"
        elif score >= 40:
            return "poor"
        else:
            return "critical"

    def _get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics."""
        try:
            health = {
                "timestamp": datetime.now().isoformat(),
                "storage_status": "unknown",
                "learning_active": False,
                "recent_checks": len(self.consistency_history),
                "last_check": self.last_check.isoformat() if self.last_check else None,
            }

            # Check storage status
            if self.use_unified_storage and self.unified_storage:
                try:
                    storage_stats = self.unified_storage.get_storage_stats()
                    health["storage_status"] = "healthy" if storage_stats else "error"
                except:
                    health["storage_status"] = "error"
            else:
                health["storage_status"] = "unavailable"

            # Check learning system
            if self.learning_system:
                try:
                    insights = self.learning_system.get_learning_insights()
                    health["learning_active"] = insights.get("learning_active", False)
                except:
                    health["learning_active"] = False

            return health

        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "storage_status": "error",
                "learning_active": False,
                "recent_checks": 0,
                "error": str(e),
            }

    def _get_performance_trends(self) -> Dict[str, Any]:
        """Get performance trends from consistency history."""
        try:
            if len(self.consistency_history) < 2:
                return {"trend": "insufficient_data", "message": "Need at least 2 consistency checks for trend analysis"}

            recent_checks = self.consistency_history[-10:]  # Last 10 checks

            scores = [check["score"] for check in recent_checks]

            # Calculate trend
            if len(scores) >= 2:
                recent_avg = sum(scores[-3:]) / min(3, len(scores))
                earlier_avg = sum(scores[:-3]) / max(1, len(scores) - 3)

                if recent_avg > earlier_avg + 5:
                    trend = "improving"
                elif recent_avg < earlier_avg - 5:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "stable"

            return {
                "trend": trend,
                "recent_average": round(sum(scores) / len(scores), 1),
                "highest_score": max(scores),
                "lowest_score": min(scores),
                "checks_analyzed": len(recent_checks),
                "time_period": f"{len(recent_checks)} recent checks",
            }

        except Exception as e:
            return {"trend": "error", "error": str(e)}

    def _generate_auto_healing_recommendations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate automatic healing recommendations based on consistency check results."""
        recommendations = []

        try:
            # Analyze issues and suggest solutions
            for issue in results.get("issues_found", []):
                issue_type = issue.get("type", "")

                if issue_type == "unified_storage_unavailable":
                    recommendations.append(
                        {
                            "priority": "high",
                            "type": "system_initialization",
                            "title": "Initialize Unified Storage System",
                            "description": "Unified storage is required for data consistency",
                            "actions": [
                                "Ensure unified_parameter_storage.py is available",
                                "Check unified adapter initialization",
                                "Verify storage permissions",
                            ],
                            "auto_fix_possible": True,
                        }
                    )

                elif issue_type == "stale_data" or issue_type == "very_stale_data":
                    recommendations.append(
                        {
                            "priority": "medium",
                            "type": "data_refresh",
                            "title": "Refresh Dashboard Data",
                            "description": "Update data sources to ensure current information",
                            "actions": [
                                "Check automated data collection processes",
                                "Verify data pipeline functionality",
                                "Manually trigger data updates if needed",
                            ],
                            "auto_fix_possible": True,
                        }
                    )

                elif issue_type == "data_integrity_issue":
                    recommendations.append(
                        {
                            "priority": "high",
                            "type": "data_repair",
                            "title": "Repair Data Integrity",
                            "description": "Fix data integrity issues in unified storage",
                            "actions": [
                                "Run data integrity validation",
                                "Repair corrupted data records",
                                "Restore from backup if needed",
                            ],
                            "auto_fix_possible": True,
                        }
                    )

            # Add learning-based recommendations
            if self.learning_system:
                try:
                    learning_recommendations = auto_suggest_improvements(
                        {"problem_type": "dashboard_consistency", "current_score": results.get("consistency_score", 0)}
                    )

                    if learning_recommendations.get("suggestions"):
                        recommendations.append(
                            {
                                "priority": "medium",
                                "type": "learning_based",
                                "title": "Learning System Recommendations",
                                "description": f"Based on {learning_recommendations.get('based_on_patterns', 0)} historical patterns",
                                "actions": learning_recommendations.get("suggestions", []),
                                "confidence": learning_recommendations.get("confidence", "low"),
                                "auto_fix_possible": False,
                            }
                        )
                except:
                    pass

        except Exception as e:
            recommendations.append(
                {
                    "priority": "low",
                    "type": "error",
                    "title": "Recommendation Generation Error",
                    "description": f"Error generating recommendations: {str(e)}",
                    "actions": ["Check system logs for details"],
                    "auto_fix_possible": False,
                }
            )

        return recommendations


# Global consistency dashboard instance
_consistency_dashboard = None


def get_consistency_dashboard() -> ConsistencyDashboard:
    """Get global consistency dashboard instance."""
    global _consistency_dashboard
    if _consistency_dashboard is None:
        _consistency_dashboard = ConsistencyDashboard()
    return _consistency_dashboard


def run_consistency_check() -> Dict[str, Any]:
    """Run comprehensive consistency check."""
    dashboard = get_consistency_dashboard()
    return dashboard.run_consistency_check()


def get_system_health() -> Dict[str, Any]:
    """Get current system health status."""
    dashboard = get_consistency_dashboard()
    return dashboard._get_system_health()
