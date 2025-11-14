#!/usr/bin/env python3
#    Unified Storage Migration Script
"""

This script systematically replaces all legacy JSON file reading in dashboard.py
with unified storage calls only. This aligns with the automatic learning innovation
where every task makes the agent smarter through systematic data collection.

Key Principles:
1. Single Source of Truth: Unified storage only
2. Systematic Data Access: No more legacy file reading
3. Automatic Learning Integration: Direct access to learning system data
4. Error-Free Operation: Eliminates file-not-found and parsing errors
"""
import re
import json
from pathlib import Path


def migrate_dashboard_to_unified_storage():
"""
    Migrate dashboard.py to use unified storage exclusively.
"""

    dashboard_file = Path("lib/dashboard.py")
    if not dashboard_file.exists():
        dashboard_file = Path(".claude-patterns/dashboard.py")

    if not dashboard_file.exists():
        print("ERROR: dashboard.py not found")
        return False

    # Read the current dashboard file
    with open(dashboard_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Create the new unified-only content
    new_content = create_unified_storage_content()

    # Write the updated content
    with open(dashboard_file, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Successfully migrated {dashboard_file} to unified storage only")
    return True


"""
def create_unified_storage_content():
"""
    Create new dashboard content that uses unified storage only.
"""

    return '''
# Unified Storage-Only Dashboard Data Collector
# This version eliminates all legacy JSON file reading
# Uses ONLY unified parameter storage for systematic data access

"""
class DashboardDataCollector:
    """Collects and aggregates data from unified storage only."""

    def __init__(self, patterns_dir: str = ".claude-patterns"): ):
"""
        Initialize with unified storage only.

        Args:
            patterns_dir: Legacy parameter (ignored, unified storage used instead)
"""
        current_dir = Path(__file__).parent
        self.cache = {}
        self.cache_ttl = 60
        self.last_update = {}

        # Detect dashboard location and set up paths
        if current_dir.name == '.claude-patterns':
            self.patterns_dir = current_dir
            self.project_root = current_dir.parent
            self.is_local_copy = True
        elif current_dir.name == 'lib':
            self.patterns_dir = self._discover_patterns_dir()
            self.project_root = self._discover_project_root()
            self.is_local_copy = False
        else:
            self.patterns_dir = self._discover_patterns_dir()
            self.project_root = self._discover_project_root()
            self.is_local_copy = False

        # Initialize unified parameter storage ONLY
        if UNIFIED_STORAGE_AVAILABLE:
            storage_dirs = [
                self.patterns_dir / '.claude-unified',
                self.project_root / '.claude-unified',
                self.patterns_dir,
                self.project_root
            ]

            self.unified_storage = None
            self.use_unified_storage = False

            for storage_dir in storage_dirs:
                if storage_dir.exists():
                    try:
                        self.unified_storage = UnifiedParameterStorage(str(storage_dir))
                        self.use_unified_storage = True
                        enable_compatibility_mode(auto_patch=False, monkey_patch=False)
                        break
                    except Exception:
                        continue

            if not self.unified_storage:
                print("WARNING: Unified storage not available")
                self.unified_storage = None
                self.use_unified_storage = False
        else:
            print("WARNING: Unified storage not available")
            self.unified_storage = None
            self.use_unified_storage = False

"""
    def _load_unified_data():
"""
        
        Load data from unified parameter storage ONLY.
        This is the ONLY data source for all dashboard APIs.
"""
        if not self.use_unified_storage or not self.unified_storage:
            print("Warning: Unified storage not available, using empty data", file=sys.stderr)
            return {
                "quality": {"assessments": {"history": [], "current": {}}},
                "patterns": {},
                "performance": {"records": []},
                "skills": {"skill_effectiveness": {}},
                "agents": {"agent_effectiveness": {}}
            }

        try:
            unified_data = self.unified_storage._read_data()
            return unified_data
        except Exception as e:
            print(f"Error loading unified data: {e}", file=sys.stderr)
            return {
                "quality": {"assessments": {"history": [], "current": {}}},
                "patterns": {},
                "performance": {"records": []},
                "skills": {"skill_effectiveness": {}},
                "agents": {"agent_effectiveness": {}}
            }

"""
    def get_overview_metrics(self) -> Dict[str, Any]:
        """Get overview metrics from unified storage ONLY."""
        unified_data = self._load_unified_data()

        # Extract data from unified storage structure
        quality_data = unified_data.get("quality", {})
        patterns_data = unified_data.get("patterns", {})
        performance_data = unified_data.get("performance", {})
        skills_data = unified_data.get("skills", {})
        agents_data = unified_data.get("agents", {})

        # Get assessments from unified storage
        assessment_history = quality_data.get("assessments", {}).get("history", [])
        current_assessment = quality_data.get("assessments", {}).get("current", {})

        # Calculate metrics
        total_patterns = 0
        if isinstance(patterns_data, list):
            total_patterns += len(patterns_data)
        elif isinstance(patterns_data, dict):
            total_patterns += len(patterns_data.get("patterns", []))

        total_patterns += len(assessment_history)
        total_patterns += len(performance_data.get("records", []))

        total_skills = len(skills_data.get("skill_effectiveness", {}))
        total_agents = len(agents_data.get("agent_effectiveness", {}))

        # Calculate average quality score
        quality_scores = []

        # From patterns data
        if isinstance(patterns_data, list):
            quality_scores.extend([
                p.get("outcome", {}).get("quality_score", 0)
                for p in patterns_data
                if p.get("outcome", {}).get("quality_score") is not None
            ])
        elif isinstance(patterns_data, dict):
            quality_scores.extend([
                p.get("outcome", {}).get("quality_score", 0)
                for p in patterns_data.get("patterns", [])
                if p.get("outcome", {}).get("quality_score") is not None
            ])

        # From assessment history
        quality_scores.extend([
            a.get("overall_score", 0)
            for a in assessment_history
            if a.get("overall_score") is not None
        ])

        # From current assessment
        if current_assessment and current_assessment.get("overall_score") is not None:
            quality_scores.append(current_assessment.get("overall_score", 0))

        # From performance records
        performance_records = performance_data.get("records", [])
        quality_scores.extend([
            r.get("overall_score", 0)
            for r in performance_records
            if r.get("overall_score") is not None
        ])

        avg_quality = statistics.mean(quality_scores) if quality_scores else 0

        # Calculate learning velocity
        learning_velocity = self._calculate_learning_velocity_from_unified_assessments(assessment_history)

        return {
            "total_patterns": total_patterns,
            "total_skills": total_skills,
            "total_agents": total_agents,
            "average_quality_score": round(avg_quality, 1),
            "learning_velocity": learning_velocity,
            "data_sources": ["unified_storage"],
            "last_updated": datetime.now().isoformat()
        }

    def get_quality_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get quality trends from unified storage ONLY."""
        unified_data = self._load_unified_data()
        quality_data = unified_data.get("quality", {})

        assessment_history = quality_data.get("assessments", {}).get("history", [])
        current_assessment = quality_data.get("assessments", {}).get("current", {})

        trend_data = []
        cutoff_date = datetime.now() - timedelta(days=days)

        # Process assessment history
        for assessment in assessment_history:
            timestamp_str = assessment.get("timestamp")
            if not timestamp_str:
                continue

            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                if timestamp < cutoff_date:
                    continue

                quality_score = assessment.get("overall_score")
                if quality_score is None:
                    continue

                task_type = assessment.get("task_type", "unknown")
                model_used = assessment.get("details", {}).get("model_used", "Unknown")

                trend_data.append({
                    "timestamp": timestamp_str,
                    "date": timestamp.strftime("%Y-%m-%d"),
                    "time": timestamp.strftime("%H:%M"),
                    "quality_score": quality_score,
                    "task_type": task_type,
                    "model_used": model_used,
                    "data_source": "unified_storage"
                })

            except (ValueError, TypeError):
                continue

        # Add current assessment if available
        if current_assessment:
            current_timestamp = current_assessment.get("timestamp", datetime.now().isoformat())
            current_score = current_assessment.get("overall_score")

            if current_score is not None:
                trend_data.append({
                    "timestamp": current_timestamp,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M"),
                    "quality_score": current_score,
                    "task_type": current_assessment.get("task_type", "current"),
                    "model_used": current_assessment.get("details", {}).get("model_used", "Unknown"),
                    "data_source": "unified_storage_current"
                })

        # Sort by timestamp
        trend_data.sort(key=lambda x: x["timestamp"])

        return {
            "trend_data": trend_data,
            "data_sources": ["unified_storage"],
            "days": days
        }

    def get_skill_performance(self, top_k: int = 10) -> Dict[str, Any]:
        """Get skill performance from unified storage ONLY."""
        unified_data = self._load_unified_data()
        skills_data = unified_data.get("skills", {})

        skills_performance = []

        # From skill effectiveness
        for skill_name, metrics in skills_data.get("skill_effectiveness", {}).items():
            success_rate = metrics.get("success_rate", 0) or 0
            usage_count = metrics.get("total_uses", 0) or 0
            avg_quality = metrics.get("avg_contribution_score", 0)

            skills_performance.append({
                "name": skill_name,
                "success_rate": round(success_rate * 100, 1),
                "usage_count": usage_count,
                "avg_quality_impact": round(avg_quality, 1),
                "recommended_for": metrics.get("recommended_for", [])
            })

        # Sort by success rate
        skills_performance.sort(key=lambda x: x["success_rate"], reverse=True)

        return {
            "top_skills": skills_performance[:top_k],
            "total_skills": len(skills_performance)
        }

    def get_agent_performance(self, top_k: int = 10) -> Dict[str, Any]:
        """Get agent performance from unified storage ONLY."""
        unified_data = self._load_unified_data()
        agents_data = unified_data.get("agents", {})
        quality_data = unified_data.get("quality", {})

        agents_performance = []
        agent_stats = {}

        # Extract from assessment history
        assessment_history = quality_data.get("assessments", {}).get("history", [])
        for assessment in assessment_history:
            for agent_name, details in assessment.get("execution_details", {}).items():
                if agent_name not in agent_stats:
                    agent_stats[agent_name] = {
                        "success_count": 0,
                        "total_count": 0,
                        "total_duration": 0,
                        "total_quality": 0
                    }

                agent_stats[agent_name]["total_count"] += 1
                agent_stats[agent_name]["total_duration"] += details.get("duration", 0)
                agent_stats[agent_name]["total_quality"] += assessment.get("overall_score", 0)

                if details.get("success", False):
                    agent_stats[agent_name]["success_count"] += 1

        # Convert to dashboard format
        for agent_name, stats in agent_stats.items():
            if stats["total_count"] > 0:
                success_rate = stats["success_count"] / stats["total_count"]
                avg_duration = stats["total_duration"] / stats["total_count"]
                avg_quality = stats["total_quality"] / stats["total_count"]
                reliability = success_rate * (avg_quality / 100)

                agents_performance.append({
                    "name": agent_name,
                    "success_rate": round(success_rate * 100, 1),
                    "usage_count": stats["total_count"],
                    "avg_duration": round(avg_duration, 1),
                    "reliability": round(reliability * 100, 1)
                })

        # Sort by reliability
        agents_performance.sort(key=lambda x: x["reliability"], reverse=True)

        return {
            "top_agents": agents_performance[:top_k],
            "total_agents": len(agents_performance)
        }

    def get_task_distribution(self) -> Dict[str, Any]:
        """Get task distribution from unified storage ONLY."""
        unified_data = self._load_unified_data()

        task_counts = defaultdict(int)
        success_by_task = defaultdict(list)

        # From assessment history
        assessment_history = unified_data.get("quality", {}).get("assessments", {}).get("history", [])
        for assessment in assessment_history:
            task_type = assessment.get("task_type", "unknown")
            score = assessment.get("overall_score", 0)

            task_counts[task_type] += 1
            success_by_task[task_type].append(score)

        # Calculate success rates
        task_distribution = []
        for task_type, count in task_counts.items():
            scores = success_by_task[task_type]
            success_rate = len([s for s in scores if s >= 70]) / len(scores) if scores else 0
            avg_score = statistics.mean(scores) if scores else 0

            task_distribution.append({
                "task_type": task_type,
                "count": count,
                "success_rate": round(success_rate * 100, 1),
                "average_score": round(avg_score, 1)
            })

        # Sort by count
        task_distribution.sort(key=lambda x: x["count"], reverse=True)

        return {
            "task_distribution": task_distribution,
            "total_tasks": sum(task_counts.values())
        }

    def _calculate_learning_velocity_from_unified_assessments(self, assessment_history: list) -> str:
        """Calculate learning velocity from unified assessment history."""
        if len(assessment_history) < 3:
            return "insufficient_data"

"""
        # Sort by timestamp
        assessment_history.sort(key=lambda x: x.get("timestamp", ""))

        # Split into halves
        mid = len(assessment_history) // 2
        first_half = assessment_history[:mid]
        second_half = assessment_history[mid:]

        # Calculate averages
        first_avg = statistics.mean([
            a.get("overall_score", 0)
            for a in first_half
            if a.get("overall_score") is not None
        ]) if first_half else 0

        second_avg = statistics.mean([
            a.get("overall_score", 0)
            for a in second_half
            if a.get("overall_score") is not None
        ]) if second_half else 0

        improvement = second_avg - first_avg

        # Calculate velocity
        if improvement > 3:
            return "accelerating"
        elif improvement > 0:
            return "improving"
        elif improvement > -3:
            return "stable"
        else:
            return "declining"

if __name__ == "__main__":
    migrate_dashboard_to_unified_storage()
'''


if __name__ == "__main__":
    migrate_dashboard_to_unified_storage()
