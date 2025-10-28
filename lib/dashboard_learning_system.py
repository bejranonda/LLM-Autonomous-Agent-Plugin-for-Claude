"""
Dashboard Learning System

Captures learning patterns from dashboard debugging work to continuously improve performance.
Every task makes the agent smarter through automatic pattern recognition and storage.

Key Innovation: Automatic Learning
- Every task makes the agent smarter
- Learns from successes and failures
- Continuously improves performance without manual intervention
- Stores patterns for future optimization
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

try:
    from unified_parameter_storage import UnifiedParameterStorage
    from dashboard_unified_adapter import DashboardUnifiedAdapter
    UNIFIED_STORAGE_AVAILABLE = True
except ImportError:
    UNIFIED_STORAGE_AVAILABLE = False


class DashboardLearningSystem:
    """
    Automatic learning system for dashboard debugging and improvements.
    Captures patterns from every task to continuously enhance performance.
    """

    def __init__(self):
        """Initialize the learning system."""
        self.patterns_dir = Path(".claude-patterns")
        self.patterns_dir.mkdir(exist_ok=True)

        self.patterns_file = self.patterns_dir / "dashboard_learning_patterns.json"
        self.success_metrics_file = self.patterns_dir / "dashboard_success_metrics.json"

        self.use_unified_storage = False
        self.unified_storage = None
        self.unified_adapter = None

        # Initialize unified storage if available
        if UNIFIED_STORAGE_AVAILABLE:
            try:
                self.unified_storage = UnifiedParameterStorage()
                self.unified_adapter = DashboardUnifiedAdapter()
                self.use_unified_storage = True
                print("DashboardLearningSystem initialized with unified storage")
            except Exception as e:
                print(f"Learning system using legacy storage: {e}")
        else:
            print("Learning system using legacy storage")

    def capture_debugging_pattern(self, task_data: Dict, performance_metrics: Dict, context: Dict = None) -> None:
        """
        Capture debugging task pattern for future learning.

        Args:
            task_data: Original debugging task data
            performance_metrics: Performance metrics from the task
            context: Additional context about the debugging session
        """
        try:
            pattern = {
                "pattern_id": f"debugging_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "task_type": "dashboard_debugging",
                "context": {
                    "problem_category": self._categorize_problem(task_data),
                    "complexity": context.get("complexity", "medium") if context else "medium",
                    "data_sources_analyzed": context.get("data_sources", []) if context else [],
                    "issues_found": len(task_data.get("issues_found", [])),
                    "sections_affected": context.get("sections_affected", []) if context else []
                },
                "execution": {
                    "approach_used": "unified_storage_migration",
                    "skills_applied": ["data_analysis", "api_integration", "unified_storage", "problem_diagnosis"],
                    "methods_used": self._extract_methods_used(task_data, context),
                    "time_invested_minutes": context.get("duration_minutes", 45) if context else 45,
                    "iterations": context.get("iterations", 1) if context else 1
                },
                "outcome": {
                    "success": task_data.get("pass", False),
                    "quality_score": performance_metrics.get("final_quality", 0),
                    "improvement_achieved": performance_metrics.get("quality_improvement", 0),
                    "performance_index": performance_metrics.get("performance_index", 0),
                    "user_satisfaction": self._calculate_satisfaction(task_data, performance_metrics),
                    "issues_resolved": len(task_data.get("issues_found", [])),
                    "consistency_improvement": self._calculate_consistency_improvement(task_data)
                },
                "technical_details": {
                    "apis_modified": context.get("apis_modified", []) if context else [],
                    "unified_storage_integration": True,
                    "backward_compatibility": "maintained",
                    "learning_points": self._extract_learning_points(task_data, performance_metrics)
                },
                "reuse_metrics": {
                    "reuse_count": 0,
                    "success_rate": 1.0 if task_data.get("pass", False) else 0.0,
                    "avg_performance": performance_metrics.get("performance_index", 0),
                    "last_used": datetime.now().isoformat(),
                    "applicable_contexts": self._identify_applicable_contexts(task_data)
                }
            }

            # Store pattern in unified storage if available
            if self.use_unified_storage and self.unified_storage:
                try:
                    self.unified_storage.set_learning_pattern(pattern)
                    print(f"Pattern stored in unified storage: {pattern['pattern_id']}")
                except Exception as e:
                    print(f"Error storing pattern in unified storage: {e}")
                    self._store_pattern_legacy(pattern)
            else:
                self._store_pattern_legacy(pattern)

            # Update success metrics
            self._update_success_metrics(pattern)

        except Exception as e:
            print(f"Error capturing debugging pattern: {e}")

    def _store_pattern_legacy(self, pattern: Dict) -> None:
        """Store pattern in legacy file system."""
        # Load existing patterns
        patterns = self._load_legacy_patterns()

        # Add new pattern
        patterns["patterns"].append(pattern)

        # Keep only last 100 patterns to avoid file bloat
        if len(patterns["patterns"]) > 100:
            patterns["patterns"] = patterns["patterns"][-100:]

        # Save patterns
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, indent=2, ensure_ascii=False)

        print(f"Pattern stored in legacy system: {pattern['pattern_id']}")

    def _load_legacy_patterns(self) -> Dict:
        """Load patterns from legacy file system."""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading legacy patterns: {e}")

        return {"patterns": [], "last_updated": datetime.now().isoformat()}

    def _categorize_problem(self, task_data: Dict) -> str:
        """Categorize the type of problem encountered."""
        issues = task_data.get("issues_found", [])
        task_type = task_data.get("task_type", "").lower()

        if "data consistency" in task_type or any("inconsistent" in issue.lower() for issue in issues):
            return "data_consistency"
        elif "performance" in task_type or any("slow" in issue.lower() or "performance" in issue.lower() for issue in issues):
            return "performance"
        elif "api" in task_type or any("api" in issue.lower() for issue in issues):
            return "api_integration"
        elif "model" in task_type or any("model" in issue.lower() for issue in issues):
            return "model_attribution"
        else:
            return "general_debugging"

    def _extract_methods_used(self, task_data: Dict, context: Dict) -> List[str]:
        """Extract the methods used during debugging."""
        methods = ["root_cause_analysis", "data_source_identification"]

        if context and "data_sources" in context:
            methods.extend(["unified_storage_migration", "api_standardization"])

        if task_data.get("issues_found"):
            methods.append("issue_classification")

        methods.extend(["pattern_recognition", "solution_implementation"])

        return methods

    def _calculate_satisfaction(self, task_data: Dict, performance_metrics: Dict) -> str:
        """Calculate user satisfaction based on outcomes."""
        quality_score = performance_metrics.get("final_quality", 0)
        improvement = performance_metrics.get("quality_improvement", 0)

        if quality_score >= 95 and improvement >= 40:
            return "very_high"
        elif quality_score >= 90 and improvement >= 30:
            return "high"
        elif quality_score >= 80 and improvement >= 20:
            return "medium"
        else:
            return "low"

    def _calculate_consistency_improvement(self, task_data: Dict) -> Dict[str, Any]:
        """Calculate the consistency improvement achieved."""
        task_type = task_data.get("task_type", "").lower()

        if "debugging" in task_type:
            return {
                "data_source_unification": True,
                "timestamp_consistency": True,
                "model_attribution_fix": True,
                "api_response_standardization": True
            }
        else:
            return {"improvement_areas": []}

    def _extract_learning_points(self, task_data: Dict, performance_metrics: Dict) -> List[str]:
        """Extract key learning points from the task."""
        learning_points = []

        # General debugging patterns
        learning_points.extend([
            "Unified storage eliminates data consistency issues",
            "Model attribution standardization improves user experience",
            "API migration requires careful backward compatibility planning",
            "Performance metrics should use consistent data sources"
        ])

        # Specific insights based on performance
        if performance_metrics.get("quality_improvement", 0) > 40:
            learning_points.append("Root cause analysis leads to significant quality improvements")

        if performance_metrics.get("performance_index", 0) > 85:
            learning_points.append("Comprehensive approach yields high performance index")

        return learning_points

    def _identify_applicable_contexts(self, task_data: Dict) -> List[str]:
        """Identify contexts where this pattern would be applicable."""
        contexts = [
            "dashboard_data_consistency_issues",
            "mixed_data_source_problems",
            "api_migration_projects",
            "model_attribution_fixes",
            "performance_metric_standardization"
        ]

        task_type = task_data.get("task_type", "").lower()
        if "debugging" in task_type:
            contexts.extend([
                "debugging_performance_analysis",
                "data_validation_automation",
                "quality_improvement_initiatives"
            ])

        return contexts

    def _update_success_metrics(self, pattern: Dict) -> None:
        """Update overall success metrics."""
        try:
            # Load existing metrics
            if self.success_metrics_file.exists():
                with open(self.success_metrics_file, 'r', encoding='utf-8') as f:
                    metrics = json.load(f)
            else:
                metrics = {
                    "total_tasks": 0,
                    "successful_tasks": 0,
                    "avg_quality_score": 0,
                    "avg_performance_index": 0,
                    "learning_patterns": [],
                    "improvement_trends": []
                }

            # Update metrics
            metrics["total_tasks"] += 1
            if pattern["outcome"]["success"]:
                metrics["successful_tasks"] += 1

            # Update averages
            quality_score = pattern["outcome"]["quality_score"]
            performance_index = pattern["outcome"]["performance_index"]

            current_total = metrics.get("total_tasks", 1)
            prev_avg_quality = metrics.get("avg_quality_score", 0)
            prev_avg_pi = metrics.get("avg_performance_index", 0)

            metrics["avg_quality_score"] = (prev_avg_quality * (current_total - 1) + quality_score) / current_total
            metrics["avg_performance_index"] = (prev_avg_pi * (current_total - 1) + performance_index) / current_total

            # Add learning pattern summary
            metrics["learning_patterns"].append({
                "pattern_id": pattern["pattern_id"],
                "problem_category": pattern["context"]["problem_category"],
                "success": pattern["outcome"]["success"],
                "quality_score": quality_score,
                "performance_index": performance_index,
                "timestamp": pattern["timestamp"]
            })

            # Keep only last 50 learning patterns
            if len(metrics["learning_patterns"]) > 50:
                metrics["learning_patterns"] = metrics["learning_patterns"][-50:]

            metrics["last_updated"] = datetime.now().isoformat()

            # Save metrics
            with open(self.success_metrics_file, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"Error updating success metrics: {e}")

    def get_learning_insights(self) -> Dict[str, Any]:
        """
        Get learning insights from accumulated patterns.

        Returns:
            Dictionary containing learning insights and recommendations
        """
        try:
            if self.use_unified_storage and self.unified_storage:
                # Get insights from unified storage
                storage_stats = self.unified_storage.get_storage_stats()
                validation = self.unified_storage.validate_data_integrity()

                return {
                    "data_source": "unified_storage",
                    "total_patterns": storage_stats.get("total_patterns", 0),
                    "data_integrity": validation,
                    "learning_active": True,
                    "insights": self._generate_insights_from_storage(storage_stats)
                }
            else:
                # Get insights from legacy files
                return self._get_legacy_insights()

        except Exception as e:
            print(f"Error getting learning insights: {e}")
            return {"error": str(e), "learning_active": False}

    def _get_legacy_insights(self) -> Dict[str, Any]:
        """Get insights from legacy pattern storage."""
        patterns = self._load_legacy_patterns()
        metrics = self._load_success_metrics()

        if not patterns["patterns"]:
            return {
                "data_source": "legacy_storage",
                "total_patterns": 0,
                "learning_active": False,
                "insights": ["No learning patterns captured yet"]
            }

        # Analyze patterns for insights
        insights = []

        # Most common problem categories
        categories = [p["context"]["problem_category"] for p in patterns["patterns"]]
        if categories:
            most_common = max(set(categories), key=categories.count)
            insights.append(f"Most common issue type: {most_common}")

        # Success rate trends
        if metrics["total_tasks"] > 0:
            success_rate = (metrics["successful_tasks"] / metrics["total_tasks"]) * 100
            insights.append(f"Overall success rate: {success_rate:.1f}%")

        # Performance trends
        if metrics["avg_performance_index"] > 80:
            insights.append("High average performance index indicates effective debugging approach")
        elif metrics["avg_performance_index"] < 60:
            insights.append("Performance index suggests room for improvement in debugging methodology")

        return {
            "data_source": "legacy_storage",
            "total_patterns": len(patterns["patterns"]),
            "learning_active": True,
            "insights": insights,
            "success_metrics": metrics
        }

    def _load_success_metrics(self) -> Dict:
        """Load success metrics from file."""
        if self.success_metrics_file.exists():
            try:
                with open(self.success_metrics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        return {
            "total_tasks": 0,
            "successful_tasks": 0,
            "avg_quality_score": 0,
            "avg_performance_index": 0,
            "learning_patterns": []
        }

    def auto_improve_approaches(self, task_context: Dict) -> Dict[str, Any]:
        """
        Automatically suggest improvements based on learned patterns.

        Args:
            task_context: Current task context

        Returns:
            Improvement suggestions based on historical patterns
        """
        try:
            # Get learning insights
            insights = self.get_learning_insights()

            if not insights.get("learning_active", False):
                return {
                    "suggestions": ["No learning data available yet - continue building pattern database"],
                    "confidence": "low"
                }

            # Generate suggestions based on insights
            suggestions = []

            # Based on common problem types
            problem_type = task_context.get("problem_type", "").lower()

            if "consistency" in problem_type:
                suggestions.extend([
                    "Use unified storage as single source of truth",
                    "Standardize data access patterns across all APIs",
                    "Implement validation checks for data consistency"
                ])

            if "performance" in problem_type:
                suggestions.extend([
                    "Profile data access patterns to identify bottlenecks",
                    "Consider caching strategies for frequently accessed data",
                    "Optimize data retrieval from unified storage"
                ])

            # Based on historical success patterns
            if insights.get("success_metrics", {}).get("avg_performance_index", 0) > 85:
                suggestions.append("Follow the established debugging methodology that has proven successful")

            return {
                "suggestions": suggestions,
                "confidence": "high" if len(suggestions) > 3 else "medium",
                "based_on_patterns": insights.get("total_patterns", 0),
                "historical_success_rate": (insights.get("success_metrics", {}).get("successful_tasks", 0) /
                                        max(1, insights.get("success_metrics", {}).get("total_tasks", 1))) * 100
            }

        except Exception as e:
            print(f"Error generating improvement suggestions: {e}")
            return {
                "suggestions": ["Continue with systematic debugging approach"],
                "confidence": "low",
                "error": str(e)
            }


# Global learning system instance
_learning_system = None

def get_learning_system() -> DashboardLearningSystem:
    """Get global learning system instance."""
    global _learning_system
    if _learning_system is None:
        _learning_system = DashboardLearningSystem()
    return _learning_system

def capture_debugging_pattern(task_data: Dict, performance_metrics: Dict, context: Dict = None) -> None:
    """Capture debugging pattern for automatic learning."""
    system = get_learning_system()
    system.capture_debugging_pattern(task_data, performance_metrics, context)

def get_learning_insights() -> Dict[str, Any]:
    """Get learning insights from accumulated patterns."""
    system = get_learning_system()
    return system.get_learning_insights()

def auto_suggest_improvements(task_context: Dict) -> Dict[str, Any]:
    """Get automatic improvement suggestions based on learned patterns."""
    system = get_learning_system()
    return system.auto_improve_approaches(task_context)