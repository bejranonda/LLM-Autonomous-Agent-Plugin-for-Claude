#!/usr/bin/env python3
"""
Parameter Migration Utility for Autonomous Agent Plugin

Provides backward compatibility and gradual migration from scattered parameter
storage systems to the unified parameter storage system.

Features:
- Automatic detection of legacy storage locations
- Gradual migration with fallback to original sources
- Compatibility layer for existing code
- Validation and verification of migrated data
- Rollback capabilities

Version: 1.0.0
Author: Autonomous Agent Development Team
"""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

from unified_parameter_storage import UnifiedParameterStorage


class LegacyStorageAdapter:
    """
    Adapter class to provide backward compatibility with legacy storage systems.

    Allows existing code to continue working while gradually migrating to the
    unified storage system.
    """

    def __init__(self, unified_storage: UnifiedParameterStorage):
        """
        Initialize legacy storage adapter.

        Args:
            unified_storage: Instance of unified parameter storage
        """
        self.unified_storage = unified_storage
        self.legacy_sources = self._detect_legacy_sources()

    def _detect_legacy_sources(self) -> Dict[str, Path]:
        """
        Detect available legacy storage sources.

        Returns:
            Dictionary mapping source types to file paths
        """
        sources = {}

        # Quality history sources
        quality_sources = [
            Path(".claude-quality/quality_history.json"),
            Path(".claude-patterns/quality_history.json")
        ]
        for source in quality_sources:
            if source.exists():
                sources[f"quality_history_{source.parent.name}"] = source

        # Model performance source
        model_perf_source = Path(".claude-patterns/model_performance.json")
        if model_perf_source.exists():
            sources["model_performance"] = model_perf_source

        # Learning patterns source
        patterns_source = Path(".claude-patterns/patterns.json")
        if patterns_source.exists():
            sources["learning_patterns"] = patterns_source

        # Auto-fix patterns source
        autofix_source = Path("patterns/autofix-patterns.json")
        if autofix_source.exists():
            sources["autofix_patterns"] = autofix_source

        # Additional assessment sources
        assessment_sources = [
            Path(".claude-quality/assessment_history.json"),
            Path(".claude-quality/recent_assessments.json")
        ]
        for source in assessment_sources:
            if source.exists():
                sources[f"assessments_{source.name}"] = source

        return sources

    def get_quality_score_legacy(self, source: str = "unified") -> float:
        """
        Get quality score with fallback to legacy sources.

        Args:
            source: Preferred source ("unified", "legacy", or specific source name)

        Returns:
            Current quality score
        """
        if source == "unified":
            try:
                return self.unified_storage.get_quality_score()
            except Exception:
                pass  # Fallback to legacy

        # Try legacy sources
        for source_name, source_path in self.legacy_sources.items():
            if "quality_history" in source_name:
                try:
                    with open(source_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list) and data:
                            # Get most recent quality score
                            latest = data[-1]
                            if "quality_score" in latest:
                                return latest["quality_score"] * 100  # Convert to 0-100 scale
                except Exception:
                    continue

        return 0.0  # Default if no source available

    def get_model_performance_legacy(self, model: str) -> Dict[str, Any]:
        """
        Get model performance with fallback to legacy sources.

        Args:
            model: Model name

        Returns:
            Model performance data
        """
        # Try unified storage first
        try:
            perf_data = self.unified_storage.get_model_performance(model)
            if "error" not in perf_data:
                return perf_data
        except Exception:
            pass

        # Try legacy source
        if "model_performance" in self.legacy_sources:
            try:
                with open(self.legacy_sources["model_performance"], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if model in data:
                        return data[model]
            except Exception:
                pass

        return {"error": f"No performance data for model '{model}'"}

    def record_quality_legacy(self, score: float, metrics: Dict[str, float] = None,
                            source: str = "unified"):
        """
        Record quality score with optional legacy backup.

        Args:
            score: Quality score (0-100)
            metrics: Optional detailed metrics
            source: Target storage ("unified", "legacy", or "both")
        """
        if source in ["unified", "both"]:
            try:
                self.unified_storage.set_quality_score(score, metrics)
            except Exception as e:
                print(f"Warning: Failed to record to unified storage: {e}", file=sys.stderr)

        if source in ["legacy", "both"]:
            self._record_quality_to_legacy(score, metrics)

    def _record_quality_to_legacy(self, score: float, metrics: Dict[str, float] = None):
        """Record quality score to legacy storage locations."""
        record = {
            "task_id": f"legacy_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "quality_score": score / 100,  # Convert to 0-1 scale for legacy
            "timestamp": datetime.now().isoformat()
        }
        if metrics:
            record["metrics"] = {k: v / 100 for k, v in metrics.items()}  # Convert scale

        # Update all legacy quality history files
        for source_name, source_path in self.legacy_sources.items():
            if "quality_history" in source_name:
                try:
                    with open(source_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    if not isinstance(data, list):
                        data = []

                    data.append(record)

                    # Keep only last 1000 entries
                    if len(data) > 1000:
                        data = data[-1000:]

                    with open(source_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)

                except Exception as e:
                    print(f"Warning: Failed to update legacy {source_path}: {e}", file=sys.stderr)


class MigrationManager:
    """
    Manages the migration process from legacy to unified storage.
    """

    def __init__(self, unified_storage: UnifiedParameterStorage):
        """
        Initialize migration manager.

        Args:
            unified_storage: Instance of unified parameter storage
        """
        self.unified_storage = unified_storage
        self.migration_log = []
        self.rollback_data = {}

    def analyze_migration_complexity(self) -> Dict[str, Any]:
        """
        Analyze the complexity of migration based on detected sources.

        Returns:
            Migration complexity analysis
        """
        adapter = LegacyStorageAdapter(self.unified_storage)

        analysis = {
            "total_sources": len(adapter.legacy_sources),
            "source_types": {},
            "estimated_time_minutes": 0,
            "complexity_level": "low",
            "recommendations": []
        }

        # Categorize sources
        for source_name, source_path in adapter.legacy_sources.items():
            if "quality" in source_name:
                analysis["source_types"]["quality"] = analysis["source_types"].get("quality", 0) + 1
            elif "model" in source_name:
                analysis["source_types"]["model_performance"] = analysis["source_types"].get("model_performance", 0) + 1
            elif "pattern" in source_name:
                analysis["source_types"]["patterns"] = analysis["source_types"].get("patterns", 0) + 1
            elif "assessment" in source_name:
                analysis["source_types"]["assessments"] = analysis["source_types"].get("assessments", 0) + 1

        # Estimate complexity
        if analysis["total_sources"] <= 2:
            analysis["complexity_level"] = "low"
            analysis["estimated_time_minutes"] = 5
        elif analysis["total_sources"] <= 5:
            analysis["complexity_level"] = "medium"
            analysis["estimated_time_minutes"] = 15
        else:
            analysis["complexity_level"] = "high"
            analysis["estimated_time_minutes"] = 30

        # Generate recommendations
        if "quality" in analysis["source_types"]:
            analysis["recommendations"].append("Quality score migration - High priority")
        if "model_performance" in analysis["source_types"]:
            analysis["recommendations"].append("Model performance migration - Critical for dashboard")
        if "patterns" in analysis["source_types"]:
            analysis["recommendations"].append("Learning patterns migration - Preserves historical learning")

        return analysis

    def execute_gradual_migration(self, source_types: List[str] = None,
                                dry_run: bool = False) -> Dict[str, Any]:
        """
        Execute gradual migration from legacy sources.

        Args:
            source_types: List of source types to migrate (None = all)
            dry_run: If True, only analyze without performing migration

        Returns:
            Migration results
        """
        adapter = LegacyStorageAdapter(self.unified_storage)

        if source_types is None:
            source_types = list(adapter.legacy_sources.keys())

        results = {
            "status": "started" if not dry_run else "dry_run_completed",
            "sources_processed": 0,
            "items_migrated": 0,
            "errors": [],
            "warnings": [],
            "source_results": {}
        }

        for source_name, source_path in adapter.legacy_sources.items():
            if not any(st in source_name for st in source_types):
                continue

            source_result = {
                "path": str(source_path),
                "size_bytes": source_path.stat().st_size,
                "items_migrated": 0,
                "errors": [],
                "warnings": []
            }

            try:
                if not dry_run:
                    # Create backup before migration
                    self._create_source_backup(source_path)

                if "quality_history" in source_name:
                    migrated_items = self._migrate_quality_source(source_path, dry_run)
                    source_result["items_migrated"] = migrated_items

                elif "model_performance" in source_name:
                    migrated_items = self._migrate_model_source(source_path, dry_run)
                    source_result["items_migrated"] = migrated_items

                elif "pattern" in source_name:
                    migrated_items = self._migrate_pattern_source(source_path, dry_run)
                    source_result["items_migrated"] = migrated_items

                elif "assessment" in source_name:
                    migrated_items = self._migrate_assessment_source(source_path, dry_run)
                    source_result["items_migrated"] = migrated_items

                results["sources_processed"] += 1
                results["items_migrated"] += source_result["items_migrated"]

                if not dry_run and source_result["items_migrated"] > 0:
                    # Optionally archive migrated source
                    self._archive_migrated_source(source_path)

            except Exception as e:
                error_msg = f"Failed to migrate {source_name}: {e}"
                source_result["errors"].append(error_msg)
                results["errors"].append(error_msg)

            results["source_results"][source_name] = source_result

        if not dry_run and results["sources_processed"] > 0:
            results["status"] = "completed"

        return results

    def _create_source_backup(self, source_path: Path):
        """Create backup of source file before migration."""
        backup_dir = Path(".claude-unified/migration_backups")
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{source_path.stem}_{timestamp}{source_path.suffix}"

        try:
            shutil.copy2(source_path, backup_path)
            self.migration_log.append(f"Created backup: {backup_path}")
        except Exception as e:
            self.migration_log.append(f"Warning: Failed to backup {source_path}: {e}")

    def _migrate_quality_source(self, source_path: Path, dry_run: bool) -> int:
        """Migrate quality history from source file."""
        with open(source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            return 0

        items_migrated = 0
        for record in data:
            if "quality_score" in record:
                if not dry_run:
                    score = record["quality_score"] * 100  # Convert to 0-100 scale
                    metrics = record.get("metrics", {})
                    if metrics:
                        metrics = {k: v * 100 for k, v in metrics.items()}
                    self.unified_storage.set_quality_score(score, metrics)
                items_migrated += 1

        return items_migrated

    def _migrate_model_source(self, source_path: Path, dry_run: bool) -> int:
        """Migrate model performance from source file."""
        with open(source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        items_migrated = 0
        for model_name, model_data in data.items():
            if isinstance(model_data, dict) and "recent_scores" in model_data:
                if not dry_run:
                    # Initialize model performance in unified storage
                    for score_entry in model_data["recent_scores"]:
                        score = score_entry.get("score", 0)
                        task_type = score_entry.get("task_type", "unknown")
                        self.unified_storage.update_model_performance(model_name, score, task_type)
                items_migrated += 1

        return items_migrated

    def _migrate_pattern_source(self, source_path: Path, dry_run: bool) -> int:
        """Migrate learning patterns from source file."""
        with open(source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        items_migrated = 0
        if "patterns" in data:
            if not dry_run:
                self.unified_storage.update_learning_patterns(data["patterns"])
            items_migrated += len(data["patterns"])

        return items_migrated

    def _migrate_assessment_source(self, source_path: Path, dry_run: bool) -> int:
        """Migrate assessment data from source file."""
        with open(source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        items_migrated = 0
        # Assessment data often contains quality-related information
        if isinstance(data, list):
            for record in data:
                if "score" in record or "quality" in record:
                    if not dry_run:
                        score = record.get("score", record.get("quality", 0)) * 100
                        self.unified_storage.set_quality_score(score)
                    items_migrated += 1

        return items_migrated

    def _archive_migrated_source(self, source_path: Path):
        """Archive successfully migrated source file."""
        archive_dir = Path(".claude-unified/migrated_sources")
        archive_dir.mkdir(parents=True, exist_ok=True)

        archive_path = archive_dir / source_path.name
        try:
            shutil.move(str(source_path), str(archive_path))
            self.migration_log.append(f"Archived migrated source: {source_path} -> {archive_path}")
        except Exception as e:
            self.migration_log.append(f"Warning: Failed to archive {source_path}: {e}")

    def validate_migration(self) -> Dict[str, Any]:
        """
        Validate migration results and data integrity.

        Returns:
            Validation results
        """
        validation_results = {
            "overall_status": "unknown",
            "data_integrity": {},
            "completeness": {},
            "issues": [],
            "recommendations": []
        }

        # Validate unified storage integrity
        storage_validation = self.unified_storage.validate_data_integrity()
        validation_results["data_integrity"] = storage_validation

        # Check completeness of migration
        adapter = LegacyStorageAdapter(self.unified_storage)

        # Check if all legacy sources have been processed
        remaining_sources = len(adapter.legacy_sources)
        if remaining_sources == 0:
            validation_results["completeness"]["status"] = "complete"
        elif remaining_sources <= 2:
            validation_results["completeness"]["status"] = "mostly_complete"
        else:
            validation_results["completeness"]["status"] = "incomplete"

        validation_results["completeness"]["remaining_sources"] = remaining_sources

        # Check for data consistency issues
        unified_quality = self.unified_storage.get_quality_score()
        legacy_quality = adapter.get_quality_score_legacy("legacy")

        if abs(unified_quality - legacy_quality) > 5.0:
            validation_results["issues"].append(
                f"Quality score discrepancy: Unified={unified_quality}, Legacy={legacy_quality}"
            )

        # Overall status
        if (storage_validation["valid"] and
            validation_results["completeness"]["status"] == "complete" and
            not validation_results["issues"]):
            validation_results["overall_status"] = "success"
        elif storage_validation["valid"] and not validation_results["issues"]:
            validation_results["overall_status"] = "acceptable"
        else:
            validation_results["overall_status"] = "needs_attention"

        # Generate recommendations
        if validation_results["completeness"]["status"] != "complete":
            validation_results["recommendations"].append(
                "Complete migration of remaining legacy sources"
            )

        if validation_results["issues"]:
            validation_results["recommendations"].append(
                "Address data consistency issues before retiring legacy storage"
            )

        return validation_results

    def rollback_migration(self, source_types: List[str] = None) -> Dict[str, Any]:
        """
        Rollback migration by restoring from backups.

        Args:
            source_types: List of source types to rollback (None = all)

        Returns:
            Rollback results
        """
        rollback_results = {
            "status": "started",
            "sources_restored": 0,
            "errors": [],
            "warnings": []
        }

        backup_dir = Path(".claude-unified/migration_backups")
        if not backup_dir.exists():
            rollback_results["status"] = "failed"
            rollback_results["errors"].append("No backup directory found")
            return rollback_results

        # Find backup files
        backup_files = list(backup_dir.glob("*.json"))
        if not backup_files:
            rollback_results["status"] = "completed"
            rollback_results["warnings"].append("No backup files found to restore")
            return rollback_results

        # Restore each backup file
        for backup_file in backup_files:
            if source_types and not any(st in backup_file.name for st in source_types):
                continue

            try:
                # Determine original location
                original_name = backup_file.name.split("_")[0] + ".json"
                original_path = None

                # Try to find original path
                potential_paths = [
                    Path(f".claude-quality/{original_name}"),
                    Path(f".claude-patterns/{original_name}"),
                    Path(f"patterns/{original_name}")
                ]

                for path in potential_paths:
                    if not path.exists():
                        original_path = path
                        break

                if original_path:
                    original_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_file, original_path)
                    rollback_results["sources_restored"] += 1
                    self.migration_log.append(f"Restored: {backup_file} -> {original_path}")

            except Exception as e:
                error_msg = f"Failed to restore {backup_file}: {e}"
                rollback_results["errors"].append(error_msg)

        if rollback_results["sources_restored"] > 0:
            rollback_results["status"] = "completed"
        else:
            rollback_results["status"] = "failed"

        return rollback_results


def main():
    """Command-line interface for parameter migration."""
    import argparse

    parser = argparse.ArgumentParser(description='Parameter Migration Utility')
    parser.add_argument('--storage-dir', default='.claude-unified', help='Unified storage directory')

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Analysis command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze migration complexity')

    # Migration commands
    migrate_parser = subparsers.add_parser('migrate', help='Execute migration')
    migrate_parser.add_argument('--sources', nargs='+', help='Source types to migrate')
    migrate_parser.add_argument('--dry-run', action='store_true', help='Analyze without migrating')

    # Validation command
    subparsers.add_parser('validate', help='Validate migration results')

    # Rollback command
    rollback_parser = subparsers.add_parser('rollback', help='Rollback migration')
    rollback_parser.add_argument('--sources', nargs='+', help='Source types to rollback')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    unified_storage = UnifiedParameterStorage(args.storage_dir)
    migration_manager = MigrationManager(unified_storage)

    try:
        if args.action == 'analyze':
            analysis = migration_manager.analyze_migration_complexity()
            print(json.dumps(analysis, indent=2))

        elif args.action == 'migrate':
            results = migration_manager.execute_gradual_migration(
                source_types=args.sources,
                dry_run=args.dry_run
            )
            print(json.dumps(results, indent=2))

        elif args.action == 'validate':
            validation = migration_manager.validate_migration()
            print(json.dumps(validation, indent=2))

        elif args.action == 'rollback':
            results = migration_manager.rollback_migration(args.sources)
            print(json.dumps(results, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()