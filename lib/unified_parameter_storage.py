#!/usr/bin/env python3
"""
Unified Parameter Storage System for Autonomous Agent Plugin

Centralizes all parameter storage including quality scores, model performance,
success rates, learning patterns, and dashboard metrics. Provides thread-safe
access, backward compatibility, and migration capabilities.

Features:
- Thread-safe read/write operations with file locking
- Version-controlled parameter schemas
- Automatic migration from scattered storage
- Backward compatibility layer
- Performance optimized for real-time dashboard updates
- Cross-platform compatibility (Windows/Linux/Mac)
- Backup and recovery mechanisms

Version: 1.0.0
Author: Autonomous Agent Development Team
"""

import json
import sys
import threading
import time
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Callable
from collections import defaultdict
import platform

# Handle Windows compatibility for file locking
if platform.system() == "Windows":
    import msvcrt

    def lock_file(f, exclusive=False):
        """Windows file locking using msvcrt."""
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        """Windows file unlocking."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass

else:
    import fcntl

    def lock_file(f, exclusive=False):
        """Unix file locking using fcntl."""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)

    def unlock_file(f):
        """Unix file unlocking."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class ParameterSchema:
    """Parameter schema definition and validation."""

    CURRENT_VERSION = "1.0.0"

    SCHEMA = {
        "version": CURRENT_VERSION,
        "metadata": {"created_at": str, "last_updated": str, "migration_history": list},
        "parameters": {
            "quality": {
                "scores": {"current": float, "history": list, "trends": dict, "averages": dict},
                "metrics": {
                    "syntax_compliance": float,
                    "functionality": float,
                    "maintainability": float,
                    "documentation": float,
                    "pattern_adherence": float,
                    "code_metrics": float,
                },
            },
            "models": {
                "active_model": str,
                "performance": {
                    "model_name": {
                        "scores": list,
                        "success_rate": float,
                        "contribution": float,
                        "total_tasks": int,
                        "last_updated": str,
                    }
                },
                "usage_stats": {"total_queries": int, "model_switches": int, "preferred_models": list},
            },
            "learning": {
                "patterns": {
                    "skill_effectiveness": dict,
                    "agent_performance": dict,
                    "task_patterns": list,
                    "success_rates": dict,
                },
                "analytics": {"learning_rate": float, "prediction_accuracy": float, "optimization_suggestions": list},
            },
            "dashboard": {
                "metrics": {
                    "active_tasks": int,
                    "completed_tasks": int,
                    "failed_tasks": int,
                    "average_response_time": float,
                    "system_health": float,
                },
                "real_time": {"current_model": str, "last_activity": str, "active_agents": list, "resource_usage": dict},
            },
            "autofix": {"patterns": dict, "success_rates": dict, "usage_statistics": dict},
            "agent_feedback": {
                "exchanges": list,
                "collaboration_matrix": dict,
                "learning_insights": dict,
                "effectiveness_metrics": dict,
            },
            "agent_performance": {
                "individual_metrics": dict,
                "task_history": list,
                "specializations": dict,
                "performance_trends": dict,
                "top_performers": list,
                "weak_performers": list,
            },
            "user_preferences": {
                "coding_style": dict,
                "workflow_preferences": dict,
                "quality_weights": dict,
                "communication_style": dict,
                "task_preferences": dict,
                "interaction_history": list,
                "learning_confidence": float,
            },
        },
    }


class UnifiedParameterStorage:
    """
    Centralized parameter storage system for the Autonomous Agent Plugin.

    Provides thread-safe access to all parameters with automatic migration
    from legacy storage systems.
    """

    def __init__(self, storage_dir: str = ".claude-unified"):
        """
        Initialize unified parameter storage.

        Args:
            storage_dir: Directory for unified parameter storage
        """
        self.storage_dir = Path(storage_dir)
        self.storage_file = self.storage_dir / "unified_parameters.json"
        self.backup_dir = self.storage_dir / "backups"
        self.lock_file = self.storage_dir / "storage.lock"

        # Thread safety
        self._lock = threading.RLock()
        self._cache = {}
        self._cache_timestamp = 0
        self._cache_ttl = 30  # 30 seconds cache TTL

        # Migration status
        self._migration_completed = False

        self._ensure_directories()
        self._initialize_storage()

    def _ensure_directories(self):
        """Create necessary directories."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def _initialize_storage(self):
        """Initialize storage with default structure if needed."""
        if not self.storage_file.exists():
            default_data = {
                "version": ParameterSchema.CURRENT_VERSION,
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "migration_history": [],
                },
                "parameters": {
                    "quality": {
                        "scores": {"current": 0.0, "history": [], "trends": {}, "averages": {}},
                        "metrics": {
                            "syntax_compliance": 0.0,
                            "functionality": 0.0,
                            "maintainability": 0.0,
                            "documentation": 0.0,
                            "pattern_adherence": 0.0,
                            "code_metrics": 0.0,
                        },
                    },
                    "models": {
                        "active_model": "Claude",
                        "performance": {},
                        "usage_stats": {"total_queries": 0, "model_switches": 0, "preferred_models": []},
                    },
                    "learning": {
                        "patterns": {
                            "skill_effectiveness": {},
                            "agent_performance": {},
                            "task_patterns": [],
                            "success_rates": {},
                        },
                        "analytics": {"learning_rate": 0.0, "prediction_accuracy": 0.0, "optimization_suggestions": []},
                    },
                    "dashboard": {
                        "metrics": {
                            "active_tasks": 0,
                            "completed_tasks": 0,
                            "failed_tasks": 0,
                            "average_response_time": 0.0,
                            "system_health": 100.0,
                        },
                        "real_time": {
                            "current_model": "Claude",
                            "last_activity": "",
                            "active_agents": [],
                            "resource_usage": {},
                        },
                    },
                    "autofix": {"patterns": {}, "success_rates": {}, "usage_statistics": {}},
                },
            }
            self._write_data(default_data)

    def _read_data(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Read unified parameter data with caching support.

        Args:
            use_cache: Whether to use cached data if available

        Returns:
            Dictionary containing unified parameters
        """
        current_time = time.time()

        # Check cache
        if use_cache and self._cache and current_time - self._cache_timestamp < self._cache_ttl:
            return self._cache

        with self._lock:
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    lock_file(f, exclusive=False)
                    try:
                        data = json.load(f)
                        self._cache = data
                        self._cache_timestamp = current_time
                        return data
                    finally:
                        unlock_file(f)
            except FileNotFoundError:
                self._initialize_storage()
                return self._read_data(use_cache)
            except json.JSONDecodeError as e:
                print(f"Error: Malformed JSON in {self.storage_file}: {e}", file=sys.stderr)
                # Try to restore from backup
                if self._restore_from_backup():
                    return self._read_data(use_cache)
                return self._get_default_data()
            except Exception as e:
                print(f"Error reading unified parameters: {e}", file=sys.stderr)
                return self._get_default_data()

    def _write_data(self, data: Dict[str, Any], create_backup: bool = True):
        """
        Write unified parameter data with backup support.

        Args:
            data: Parameter data to write
            create_backup: Whether to create backup before writing
        """
        with self._lock:
            try:
                # Create backup if requested
                if create_backup and self.storage_file.exists():
                    self._create_backup()

                # Update metadata
                data["metadata"]["last_updated"] = datetime.now().isoformat()

                with open(self.storage_file, "w", encoding="utf-8") as f:
                    lock_file(f, exclusive=True)
                    try:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                        # Update cache
                        self._cache = data
                        self._cache_timestamp = time.time()
                    finally:
                        unlock_file(f)

            except Exception as e:
                print(f"Error writing unified parameters: {e}", file=sys.stderr)
                raise

    def _create_backup(self):
        """Create a backup of the current storage file."""
        if not self.storage_file.exists():
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"unified_parameters_{timestamp}.json"

        try:
            shutil.copy2(self.storage_file, backup_file)
            # Keep only last 10 backups
            self._cleanup_old_backups()
        except Exception as e:
            print(f"Warning: Failed to create backup: {e}", file=sys.stderr)

    def _cleanup_old_backups(self):
        """Keep only the most recent backups."""
        backups = sorted(self.backup_dir.glob("unified_parameters_*.json"))
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                try:
                    old_backup.unlink()
                except Exception as e:
                    print(f"Warning: Failed to delete old backup {old_backup}: {e}", file=sys.stderr)

    def _restore_from_backup(self) -> bool:
        """
        Restore data from the most recent backup.

        Returns:
            True if restoration was successful
        """
        backups = sorted(self.backup_dir.glob("unified_parameters_*.json"))
        if not backups:
            return False

        latest_backup = backups[-1]
        try:
            shutil.copy2(latest_backup, self.storage_file)
            print(f"Restored from backup: {latest_backup}", file=sys.stderr)
            return True
        except Exception as e:
            print(f"Failed to restore from backup: {e}", file=sys.stderr)
            return False

    def _get_default_data(self) -> Dict[str, Any]:
        """Get default parameter structure."""
        return {
            "version": ParameterSchema.CURRENT_VERSION,
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "migration_history": [],
            },
            "parameters": {
                "quality": {"scores": {"current": 0.0}, "metrics": {}},
                "models": {"active_model": "Claude", "performance": {}, "usage_stats": {}},
                "learning": {"patterns": {}, "analytics": {}},
                "dashboard": {"metrics": {}, "real_time": {}},
                "autofix": {"patterns": {}, "success_rates": {}, "usage_statistics": {}},
            },
        }

    # Quality parameter methods
    def set_quality_score(self, score: float, metrics: Dict[str, float] = None):
        """
        Set current quality score with optional detailed metrics.

        Args:
            score: Quality score (0-100)
            metrics: Optional detailed metrics dictionary
        """
        if not isinstance(score, (int, float)) or not (0 <= score <= 100):
            raise ValueError("Quality score must be a number between 0 and 100")

        data = self._read_data()

        # Update current score
        data["parameters"]["quality"]["scores"]["current"] = float(score)

        # Add to history
        history_entry = {"score": float(score), "timestamp": datetime.now().isoformat()}
        if metrics:
            history_entry["metrics"] = metrics

        data["parameters"]["quality"]["scores"]["history"].append(history_entry)

        # Keep only last 1000 entries in history
        if len(data["parameters"]["quality"]["scores"]["history"]) > 1000:
            data["parameters"]["quality"]["scores"]["history"] = data["parameters"]["quality"]["scores"]["history"][-1000:]

        # Update metrics if provided
        if metrics:
            data["parameters"]["quality"]["metrics"].update(metrics)

        self._write_data(data)

    def get_quality_score(self) -> float:
        """Get current quality score."""
        data = self._read_data()
        return data["parameters"]["quality"]["scores"]["current"]

    def get_quality_history(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get quality score history.

        Args:
            days: Number of days to include in history

        Returns:
            List of historical quality records
        """
        data = self._read_data()
        all_history = data["parameters"]["quality"]["scores"]["history"]

        if not all_history:
            return []

        cutoff_date = datetime.now() - timedelta(days=days)
        filtered_history = []

        for entry in all_history:
            entry_date = datetime.fromisoformat(entry["timestamp"])
            if entry_date >= cutoff_date:
                filtered_history.append(entry)

        return filtered_history

    # Model parameter methods
    def set_active_model(self, model: str):
        """
        Set the currently active model.

        Args:
            model: Model name (e.g., "Claude", "OpenAI", "GLM")
        """
        data = self._read_data()

        # Track model switch if different from current
        current_model = data["parameters"]["models"]["active_model"]
        if current_model != model:
            data["parameters"]["models"]["usage_stats"]["model_switches"] += 1

        data["parameters"]["models"]["active_model"] = model
        data["parameters"]["dashboard"]["real_time"]["current_model"] = model

        self._write_data(data)

    def get_active_model(self) -> str:
        """Get the currently active model."""
        data = self._read_data()
        return data["parameters"]["models"]["active_model"]

    def update_model_performance(self, model: str, score: float, task_type: str = "unknown"):
        """
        Update performance metrics for a specific model.

        Args:
            model: Model name
            score: Performance score (0-100)
            task_type: Type of task performed
        """
        if not isinstance(score, (int, float)) or not (0 <= score <= 100):
            raise ValueError("Performance score must be a number between 0 and 100")

        data = self._read_data()

        if model not in data["parameters"]["models"]["performance"]:
            data["parameters"]["models"]["performance"][model] = {
                "scores": [],
                "success_rate": 0.0,
                "contribution": 0.0,
                "total_tasks": 0,
                "last_updated": datetime.now().isoformat(),
            }

        model_data = data["parameters"]["models"]["performance"][model]

        # Add new score
        score_entry = {"score": float(score), "timestamp": datetime.now().isoformat(), "task_type": task_type}
        model_data["scores"].append(score_entry)

        # Keep only last 100 scores per model
        if len(model_data["scores"]) > 100:
            model_data["scores"] = model_data["scores"][-100:]

        # Update metrics
        model_data["total_tasks"] += 1
        model_data["last_updated"] = datetime.now().isoformat()

        # Calculate success rate (scores >= 70 are successful)
        successful_tasks = sum(1 for s in model_data["scores"] if s["score"] >= 70)
        model_data["success_rate"] = successful_tasks / len(model_data["scores"])

        self._write_data(data)

    def get_model_performance(self, model: str) -> Dict[str, Any]:
        """
        Get performance data for a specific model.

        Args:
            model: Model name

        Returns:
            Dictionary with model performance data
        """
        data = self._read_data()

        if model not in data["parameters"]["models"]["performance"]:
            return {"error": f"No performance data for model '{model}'"}

        return data["parameters"]["models"]["performance"][model]

    # Dashboard parameter methods
    def update_dashboard_metrics(self, metrics: Dict[str, Any]):
        """
        Update dashboard metrics.

        Args:
            metrics: Dictionary of dashboard metrics to update
        """
        data = self._read_data()
        data["parameters"]["dashboard"]["metrics"].update(metrics)
        data["parameters"]["dashboard"]["real_time"]["last_activity"] = datetime.now().isoformat()

        self._write_data(data)

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all dashboard data."""
        data = self._read_data()
        return {
            "quality": data["parameters"]["quality"],
            "models": data["parameters"]["models"],
            "dashboard": data["parameters"]["dashboard"],
            "learning": data["parameters"]["learning"],
        }

    # Learning parameter methods
    def update_learning_patterns(self, patterns: Dict[str, Any]):
        """
        Update learning patterns data.

        Args:
            patterns: Learning patterns data
        """
        data = self._read_data()
        data["parameters"]["learning"]["patterns"].update(patterns)

        self._write_data(data)

    def get_learning_patterns(self) -> Dict[str, Any]:
        """Get learning patterns data."""
        data = self._read_data()
        return data["parameters"]["learning"]["patterns"]

    # Auto-fix parameter methods
    def update_autofix_patterns(self, patterns: Dict[str, Any]):
        """
        Update auto-fix patterns data.

        Args:
            patterns: Auto-fix patterns data
        """
        data = self._read_data()
        data["parameters"]["autofix"]["patterns"].update(patterns)

        self._write_data(data)

    def get_autofix_patterns(self) -> Dict[str, Any]:
        """Get auto-fix patterns data."""
        data = self._read_data()
        return data["parameters"]["autofix"]["patterns"]

    # Migration methods
    def migrate_from_legacy_storage(self, force: bool = False) -> Dict[str, Any]:
        """
        Migrate data from legacy storage systems.

        Args:
            force: Force migration even if already completed

        Returns:
            Migration result dictionary
        """
        if self._migration_completed and not force:
            return {"status": "already_completed", "migrated_items": 0}

        migration_result = {"status": "started", "migrated_items": 0, "errors": [], "sources": {}}

        data = self._read_data()

        try:
            # 1. Migrate from .claude-quality/quality_history.json
            quality_history_path = Path(".claude-quality/quality_history.json")
            if quality_history_path.exists():
                self._migrate_quality_history(quality_history_path, data, migration_result)

            # 2. Migrate from .claude-patterns/quality_history.json
            patterns_quality_path = Path(".claude-patterns/quality_history.json")
            if patterns_quality_path.exists():
                self._migrate_quality_history(patterns_quality_path, data, migration_result)

            # 3. Migrate from .claude-patterns/model_performance.json
            model_performance_path = Path(".claude-patterns/model_performance.json")
            if model_performance_path.exists():
                self._migrate_model_performance(model_performance_path, data, migration_result)

            # 4. Migrate from .claude-patterns/patterns.json
            patterns_path = Path(".claude-patterns/patterns.json")
            if patterns_path.exists():
                self._migrate_patterns(patterns_path, data, migration_result)

            # 5. Migrate from patterns/autofix-patterns.json
            autofix_path = Path("patterns/autofix-patterns.json")
            if autofix_path.exists():
                self._migrate_autofix_patterns(autofix_path, data, migration_result)

            # Update migration history
            migration_entry = {
                "timestamp": datetime.now().isoformat(),
                "items_migrated": migration_result["migrated_items"],
                "sources": list(migration_result["sources"].keys()),
                "errors": migration_result["errors"],
            }
            data["metadata"]["migration_history"].append(migration_entry)

            self._write_data(data)
            self._migration_completed = True

            migration_result["status"] = "completed"

        except Exception as e:
            migration_result["status"] = "failed"
            migration_result["errors"].append(str(e))

        return migration_result

    def _migrate_quality_history(self, source_path: Path, data: Dict[str, Any], result: Dict[str, Any]):
        """Migrate quality history from legacy file."""
        try:
            with open(source_path, "r", encoding="utf-8") as f:
                legacy_data = json.load(f)

            if isinstance(legacy_data, list):
                for record in legacy_data:
                    if "quality_score" in record:
                        # Convert to new format
                        history_entry = {
                            "score": record["quality_score"] * 100,  # Convert to 0-100 scale
                            "timestamp": record.get("timestamp", datetime.now().isoformat()),
                        }
                        if "metrics" in record:
                            history_entry["metrics"] = {k: v * 100 for k, v in record["metrics"].items()}

                        data["parameters"]["quality"]["scores"]["history"].append(history_entry)
                        result["migrated_items"] += 1

                result["sources"][str(source_path)] = "quality_history"

        except Exception as e:
            result["errors"].append(f"Failed to migrate {source_path}: {e}")

    def _migrate_model_performance(self, source_path: Path, data: Dict[str, Any], result: Dict[str, Any]):
        """Migrate model performance from legacy file."""
        try:
            with open(source_path, "r", encoding="utf-8") as f:
                legacy_data = json.load(f)

            for model_name, model_data in legacy_data.items():
                if isinstance(model_data, dict) and "recent_scores" in model_data:
                    data["parameters"]["models"]["performance"][model_name] = {
                        "scores": model_data["recent_scores"],
                        "success_rate": model_data.get("success_rate", 0.0),
                        "contribution": model_data.get("contribution_to_project", 0.0),
                        "total_tasks": model_data.get("total_tasks", 0),
                        "last_updated": model_data.get("last_updated", datetime.now().isoformat()),
                    }
                    result["migrated_items"] += 1

            result["sources"][str(source_path)] = "model_performance"

        except Exception as e:
            result["errors"].append(f"Failed to migrate {source_path}: {e}")

    def _migrate_patterns(self, source_path: Path, data: Dict[str, Any], result: Dict[str, Any]):
        """Migrate learning patterns from legacy file."""
        try:
            with open(source_path, "r", encoding="utf-8") as f:
                legacy_data = json.load(f)

            if "patterns" in legacy_data:
                data["parameters"]["learning"]["patterns"].update(legacy_data["patterns"])
                result["migrated_items"] += len(legacy_data["patterns"])

            if "skill_effectiveness" in legacy_data:
                data["parameters"]["learning"]["patterns"]["skill_effectiveness"] = legacy_data["skill_effectiveness"]

            result["sources"][str(source_path)] = "learning_patterns"

        except Exception as e:
            result["errors"].append(f"Failed to migrate {source_path}: {e}")

    def _migrate_autofix_patterns(self, source_path: Path, data: Dict[str, Any], result: Dict[str, Any]):
        """Migrate auto-fix patterns from legacy file."""
        try:
            with open(source_path, "r", encoding="utf-8") as f:
                legacy_data = json.load(f)

            data["parameters"]["autofix"]["patterns"].update(legacy_data)
            result["migrated_items"] += 1

            result["sources"][str(source_path)] = "autofix_patterns"

        except Exception as e:
            result["errors"].append(f"Failed to migrate {source_path}: {e}")

    # Utility methods
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        data = self._read_data()

        stats = {
            "version": data["version"],
            "created_at": data["metadata"]["created_at"],
            "last_updated": data["metadata"]["last_updated"],
            "migration_count": len(data["metadata"]["migration_history"]),
            "storage_size": self.storage_file.stat().st_size if self.storage_file.exists() else 0,
            "backup_count": len(list(self.backup_dir.glob("*.json"))),
            "parameter_counts": {},
        }

        # Count parameters in each category
        for category, params in data["parameters"].items():
            if isinstance(params, dict):
                stats["parameter_counts"][category] = len(params)

        return stats

    def validate_data_integrity(self) -> Dict[str, Any]:
        """Validate the integrity of stored data."""
        data = self._read_data()

        validation_result = {"valid": True, "errors": [], "warnings": []}

        # Check version
        if data.get("version") != ParameterSchema.CURRENT_VERSION:
            validation_result["warnings"].append(
                f"Version mismatch: expected {ParameterSchema.CURRENT_VERSION}, got {data.get('version')}"
            )

        # Check required sections
        required_sections = ["quality", "models", "learning", "dashboard", "autofix"]
        for section in required_sections:
            if section not in data["parameters"]:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Missing required section: {section}")

        # Validate quality scores
        quality_scores = data["parameters"]["quality"]["scores"]
        if "current" in quality_scores:
            current_score = quality_scores["current"]
            if not isinstance(current_score, (int, float)) or not (0 <= current_score <= 100):
                validation_result["valid"] = False
                validation_result["errors"].append(f"Invalid current quality score: {current_score}")

        return validation_result

    def export_data(self, export_path: str, format: str = "json") -> bool:
        """
        Export unified data to external file.

        Args:
            export_path: Path to export file
            format: Export format ("json" or "csv")

        Returns:
            True if export was successful
        """
        try:
            data = self._read_data()
            export_file = Path(export_path)

            if format.lower() == "json":
                with open(export_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif format.lower() == "csv":
                # Export quality scores as CSV
                import csv

                with open(export_file, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Timestamp", "Score", "Task ID"])

                    for entry in data["parameters"]["quality"]["scores"]["history"]:
                        writer.writerow([entry.get("timestamp", ""), entry.get("score", ""), entry.get("task_id", "")])
            else:
                raise ValueError(f"Unsupported export format: {format}")

            return True

        except Exception as e:
            print(f"Export failed: {e}", file=sys.stderr)
            return False

    def import_data(self, import_path: str, merge_strategy: str = "overwrite") -> bool:
        """
        Import data from external file.

        Args:
            import_path: Path to import file
            merge_strategy: How to merge with existing data ("overwrite", "merge", "skip")

        Returns:
            True if import was successful
        """
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                raise FileNotFoundError(f"Import file not found: {import_path}")

            with open(import_file, "r", encoding="utf-8") as f:
                imported_data = json.load(f)

            if merge_strategy == "overwrite":
                self._write_data(imported_data)
            elif merge_strategy == "merge":
                current_data = self._read_data()
                # Deep merge the data
                self._deep_merge(current_data, imported_data)
                self._write_data(current_data)
            elif merge_strategy == "skip":
                # Only import if no existing data
                current_data = self._read_data()
                if not current_data["parameters"]["quality"]["scores"]["history"]:
                    self._write_data(imported_data)
                else:
                    print("Skipping import - existing data found", file=sys.stderr)
                    return False
            else:
                raise ValueError(f"Unsupported merge strategy: {merge_strategy}")

            return True

        except Exception as e:
            print(f"Import failed: {e}", file=sys.stderr)
            return False

    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]):
        """Deep merge two dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value


def main():
    """Command-line interface for unified parameter storage."""
    import argparse

    parser = argparse.ArgumentParser(description="Unified Parameter Storage System")
    parser.add_argument("--dir", default=".claude-unified", help="Storage directory path")

    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Quality commands
    quality_parser = subparsers.add_parser("set-quality", help="Set quality score")
    quality_parser.add_argument("--score", type=float, required=True, help="Quality score (0-100)")

    # Model commands
    model_parser = subparsers.add_parser("set-model", help="Set active model")
    model_parser.add_argument("--model", required=True, help="Model name")

    # Migration commands
    migrate_parser = subparsers.add_parser("migrate", help="Migrate from legacy storage")
    migrate_parser.add_argument("--force", action="store_true", help="Force re-migration")

    # Stats commands
    subparsers.add_parser("stats", help="Show storage statistics")

    # Validation commands
    subparsers.add_parser("validate", help="Validate data integrity")

    # Export commands
    export_parser = subparsers.add_parser("export", help="Export data")
    export_parser.add_argument("--path", required=True, help="Export file path")
    export_parser.add_argument("--format", default="json", choices=["json", "csv"], help="Export format")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    storage = UnifiedParameterStorage(args.dir)

    try:
        if args.action == "set-quality":
            storage.set_quality_score(args.score)
            print(f"Quality score set to {args.score}")

        elif args.action == "set-model":
            storage.set_active_model(args.model)
            print(f"Active model set to {args.model}")

        elif args.action == "migrate":
            result = storage.migrate_from_legacy_storage(args.force)
            print(f"Migration {result['status']}: {result['migrated_items']} items migrated")
            if result["errors"]:
                print("Errors:", result["errors"])

        elif args.action == "stats":
            stats = storage.get_storage_stats()
            print(json.dumps(stats, indent=2))

        elif args.action == "validate":
            validation = storage.validate_data_integrity()
            print(f"Data integrity: {'Valid' if validation['valid'] else 'Invalid'}")
            if validation["errors"]:
                print("Errors:", validation["errors"])
            if validation["warnings"]:
                print("Warnings:", validation["warnings"])

        elif args.action == "export":
            success = storage.export_data(args.path, args.format)
            print(f"Export {'successful' if success else 'failed'}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
