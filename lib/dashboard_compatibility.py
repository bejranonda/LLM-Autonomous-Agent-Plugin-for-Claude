#!/usr/bin/env python3
"""
Dashboard Compatibility Layer for Autonomous Agent

Ensures backward compatibility with previous versions of pattern data.
Migrates and transforms old data structures to new format as needed.

Version: 1.0.0
Author: Autonomous Agent Development Team
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
import platform

# Import file locking utilities
if platform.system() == 'Windows':
    import msvcrt
    def lock_file(f, exclusive=False):
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)
    def unlock_file(f):
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl
    def lock_file(f, exclusive=False):
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
    def unlock_file(f):
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class DashboardCompatibilityManager:
    """Manages compatibility between different versions of pattern data."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """
        Initialize compatibility manager.

        Args:
            patterns_dir: Directory containing pattern data
        """
        self.patterns_dir = Path(patterns_dir)
        self.patterns_file = self.patterns_dir / "patterns.json"
        self.model_performance_file = self.patterns_dir / "model_performance.json"
        self.quality_history_file = self.patterns_dir / "quality_history.json"

    def check_and_migrate_data(self) -> Dict[str, Any]:
        """
        Check data version and migrate if necessary.

        Returns:
            Dict containing migration status and any issues found
        """
        migration_report = {
            "timestamp": datetime.now().isoformat(),
            "migrations_performed": [],
            "issues_found": [],
            "data_status": {},
            "recommendations": []
        }

        # Check if patterns directory exists
        if not self.patterns_dir.exists():
            migration_report["issues_found"].append("Pattern directory does not exist")
            return migration_report

        # Migrate patterns.json if needed
        patterns_status = self._migrate_patterns_data()
        migration_report["data_status"]["patterns"] = patterns_status
        if patterns_status.get("migrated"):
            migration_report["migrations_performed"].append("patterns.json migrated")

        # Initialize model_performance.json if missing
        model_status = self._ensure_model_performance_data()
        migration_report["data_status"]["model_performance"] = model_status
        if model_status.get("created"):
            migration_report["migrations_performed"].append(
    "model_performance.json created",
)

        # Migrate quality history if exists
        quality_status = self._migrate_quality_history()
        migration_report["data_status"]["quality_history"] = quality_status
        if quality_status.get("migrated"):
            migration_report["migrations_performed"].append("quality_history migrated")

        # Generate recommendations
        migration_report["recommendations"] = self._generate_recommendations(migration_report)

        return migration_report

    def _migrate_patterns_data(self) -> Dict[str, Any]:
        """Migrate patterns.json to ensure compatibility with new dashboard."""
        status = {"exists": False, "version": "unknown", "migrated": False, "issues": []}

        if not self.patterns_file.exists():
            status["issues"].append("patterns.json does not exist")
            return status

        status["exists"] = True

        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                lock_file(f, exclusive=False)
                try:
                    data = json.load(f)
                finally:
                    unlock_file(f)

            # Check data structure version
            if "version" in data:
                status["version"] = data["version"]
            else:
                status["version"] = "legacy"

            # Ensure required fields exist for new dashboard
            changes_made = False

            # Ensure patterns array exists
            if "patterns" not in data:
                data["patterns"] = []
                changes_made = True

            # Ensure skill_effectiveness exists
            if "skill_effectiveness" not in data:
                data["skill_effectiveness"] = {}
                changes_made = True

            # Ensure agent_effectiveness exists
            if "agent_effectiveness" not in data:
                data["agent_effectiveness"] = {}
                changes_made = True

            # Ensure project_context exists
            if "project_context" not in data:
                data["project_context"] = {
                    "detected_languages": [],
                    "frameworks": [],
                    "project_type": "unknown"
                }
                changes_made = True

            # Add version if not present
            if "version" not in data:
                data["version"] = "2.0.0"
                changes_made = True

            # Save if changes were made
            if changes_made:
                with open(self.patterns_file, 'w', encoding='utf-8') as f:
                    lock_file(f, exclusive=True)
                    try:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    finally:
                        unlock_file(f)
                status["migrated"] = True

        except Exception as e:
            status["issues"].append(f"Error reading patterns.json: {e}")

        return status

    def _ensure_model_performance_data(self) -> Dict[str, Any]:
        """Ensure model_performance.json exists with correct structure."""
        status = {"exists": False, "created": False, "issues": []}

        if self.model_performance_file.exists():
            status["exists"] = True

            # Validate structure
            try:
                with open(self.model_performance_file, 'r', encoding='utf-8') as f:
                    lock_file(f, exclusive=False)
                    try:
                        data = json.load(f)
                    finally:
                        unlock_file(f)

                # Check if data has expected structure
                if not isinstance(data, dict):
                    status["issues"].append(
    "model_performance.json has invalid structure",
)
                    return status

                # Ensure all expected models exist
                default_models = ["Claude", "OpenAI", "GLM", "Gemini"]
                for model in default_models:
                    if model not in data:
                        data[model] = {
                            "recent_scores": [],
                            "total_tasks": 0,
                            "success_rate": 0.0,
                            "contribution_to_project": 0.0,
                            "first_seen": datetime.now().isoformat(),
                            "last_updated": datetime.now().isoformat()
                        }
                        status["created"] = True

                # Save if we added models
                if status["created"]:
                    with open(self.model_performance_file, 'w', encoding='utf-8') as f:
                        lock_file(f, exclusive=True)
                        try:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        finally:
                            unlock_file(f)

            except Exception as e:
                status["issues"].append(f"Error validating model_performance.json: {e}")

        else:
            # Create with default structure
            try:
                from model_performance import ModelPerformanceManager
                manager = ModelPerformanceManager(str(self.patterns_dir))
                status["created"] = True
            except Exception as e:
                status["issues"].append(f"Error creating model_performance.json: {e}")

        return status

    def _migrate_quality_history(self) -> Dict[str, Any]:
        """Migrate quality_history.json if it exists."""
        status = {"exists": False, "migrated": False, "issues": []}

        if not self.quality_history_file.exists():
            return status

        status["exists"] = True

        try:
            with open(self.quality_history_file, 'r', encoding='utf-8') as f:
                lock_file(f, exclusive=False)
                try:
                    data = json.load(f)
                finally:
                    unlock_file(f)

            # Check if migration is needed
            if isinstance(data, list) and len(data) > 0:
                # Old format was just a list of scores
                new_format = {
                    "version": "2.0.0",
                    "entries": []
                }

                for entry in data:
                    if isinstance(entry, dict):
                        # Already in new format
                        new_format["entries"].append(entry)
                    else:
                        # Old format - just a score
                        new_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "quality_score": entry,
                            "model": "Unknown",
                            "task_type": "Unknown"
                        }
                        new_format["entries"].append(new_entry)

                # Save migrated data
                with open(self.quality_history_file, 'w', encoding='utf-8') as f:
                    lock_file(f, exclusive=True)
                    try:
                        json.dump(new_format, f, indent=2, ensure_ascii=False)
                    finally:
                        unlock_file(f)

                status["migrated"] = True

        except Exception as e:
            status["issues"].append(f"Error migrating quality_history.json: {e}")

        return status

    def _generate_recommendations(self, migration_report: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on migration status."""
        recommendations = []

        # Check for issues
        if migration_report["issues_found"]:
            recommendations.append("[WARNING] Fix data issues before using dashboard")

        # Check if migrations were performed
        if migration_report["migrations_performed"]:
            recommendations.append(
    "[OK] Data successfully migrated for new dashboard features",
)

        # Check for missing data
        if not migration_report["data_status"].get("patterns", {}).get("exists"):
            recommendations.append(
    "[INFO] Run /learn-patterns to initialize pattern learning",
)

        if not migration_report["data_status"].get(
    "model_performance",
    {}).get("exists"):,
)
            recommendations.append(
    "[INFO] Model performance data will be created automatically",
)

        # If everything is good
        if not migration_report["issues_found"] and 
            not migration_report["migrations_performed"]:
            recommendations.append(
    "[OK] All data is compatible with new dashboard features",
)

        return recommendations

    def extract_model_performance_from_patterns(self) -> Dict[str, Any]:
        """
        Extract model performance information from existing patterns.
        This helps populate initial model performance data.

        Returns:
            Dict mapping model names to performance metrics
        """
        if not self.patterns_file.exists():
            return {}

        model_metrics = {}

        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                lock_file(f, exclusive=False)
                try:
                    data = json.load(f)
                finally:
                    unlock_file(f)

            patterns = data.get("patterns", [])

            # Group patterns by model
            model_patterns = {}
            for pattern in patterns:
                # Try to extract model from execution data
                execution = pattern.get("execution", {})
                model = execution.get("model_used", "Unknown")

                if model not in model_patterns:
                    model_patterns[model] = []
                model_patterns[model].append(pattern)

            # Calculate metrics for each model
            for model, patterns_list in model_patterns.items():
                quality_scores = []
                success_count = 0
                contributions = []

                for pattern in patterns_list:
                    outcome = pattern.get("outcome", {})
                    quality_scores.append(outcome.get("quality_score", 0))

                    if outcome.get("success", False):
                        success_count += 1

                    # Extract contribution if available
                    if "contribution_to_project" in outcome:
                        contributions.append(outcome["contribution_to_project"])

                model_metrics[model] = {
                    "total_patterns": len(patterns_list),
                    "success_rate": (
    success_count / len(patterns_list) * 100) if patterns_list else 0,,
)
                    "avg_quality_score": sum(
    quality_scores) / len(quality_scores) if quality_scores else 0,,
)
                    "avg_contribution": sum(
    contributions) / len(contributions) if contributions else 0,,
)
                    "recent_scores": quality_scores[-10:]  # Last 10 scores
                }

        except Exception as e:
            print(f"Error extracting model performance: {e}", file=sys.stderr)

        return model_metrics


def main():
    """Command-line interface for compatibility manager."""
    parser = argparse.ArgumentParser(description="Dashboard compatibility manager")
    parser.add_argument("--dir", default=".claude-patterns",
                       help="Pattern directory path")
    parser.add_argument("--check", action="store_true",
                       help="Check compatibility and show migration status")
    parser.add_argument("--migrate", action="store_true",
                       help="Perform migration to ensure compatibility")
    parser.add_argument("--extract-models", action="store_true",
                       help="Extract model performance from existing patterns")

    args = parser.parse_args()

    manager = DashboardCompatibilityManager(args.dir)

    if args.check or args.migrate:
        print("Checking dashboard compatibility...")
        report = manager.check_and_migrate_data()

        print("\nCompatibility Report:")
        print(f"Timestamp: {report['timestamp']}")

        if report['migrations_performed']:
            print("\nMigrations Performed:")
            for migration in report['migrations_performed']:
                print(f"  - {migration}")

        if report['issues_found']:
            print("\nIssues Found:")
            for issue in report['issues_found']:
                print(f"  - {issue}")

        print("\nData Status:")
        for key, status in report['data_status'].items():
            exists = "[OK]" if status.get('exists') else "[MISSING]"
            print(f"  {exists} {key}: {status.get('version', 'unknown')}")

        if report['recommendations']:
            print("\nRecommendations:")
            for rec in report['recommendations']:
                print(f"  {rec}")

    elif args.extract_models:
        print("Extracting model performance from patterns...")
        metrics = manager.extract_model_performance_from_patterns()

        if metrics:
            print("\nModel Performance Found:")
            for model, data in metrics.items():
                print(f"\n{model}:")
                print(f"  Total patterns: {data['total_patterns']}")
                print(f"  Success rate: {data['success_rate']:.1f}%")
                print(f"  Avg quality: {data['avg_quality_score']:.1f}")
                print(f"  Avg contribution: {data['avg_contribution']:.1f}")
        else:
            print("No model performance data found in patterns.")


if __name__ == "__main__":
    main()
