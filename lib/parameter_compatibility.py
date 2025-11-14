#!/usr/bin/env python3
#     Parameter Compatibility Layer for Autonomous Agent Plugin
"""
Provides backward compatibility for existing code that uses the old scattered
parameter storage systems. Automatically redirects calls to the unified storage
system while maintaining the same API.

This allows for gradual migration without breaking existing functionality.

Version: 1.0.0
Author: Autonomous Agent Development Team
"""
import json
import sys
import warnings
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from functools import wraps

from unified_parameter_storage import UnifiedParameterStorage


class DeprecationWarning(UserWarning):
    """Custom deprecation warning for legacy parameter storage APIs."""

    pass


def deprecated(use_instead: str = None):
"""
    Decorator to mark functions as deprecated.

    Args:
        use_instead: Suggested replacement function
"""

"""
    def decorator(func):
        """Decorator."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper."""
            msg = f"Call to deprecated function '{func.__name__}'"
            if use_instead:
                msg += f". Use '{use_instead}' instead."
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator


class CompatibilityLayer:
"""
    Provides backward compatibility for legacy parameter storage APIs.
"""

    Automatically intercepts calls to old storage systems and redirects them
    to the unified storage system while maintaining the same interface.
"""

"""
    def __init__(self, unified_storage: UnifiedParameterStorage, auto_migrate: bool = True):
"""
        Initialize compatibility layer.

        Args:
            unified_storage: Instance of unified parameter storage
            auto_migrate: Whether to automatically migrate legacy data
"""
        self.unified_storage = unified_storage
        self.auto_migrate = auto_migrate
        self._compatibility_cache = {}

"""
    def _show_deprecation_warning(self, old_api: str, new_api: str = None):
        """Show deprecation warning for legacy API usage."""
        msg = f"Using deprecated parameter storage API: {old_api}"
        if new_api:
            msg += f". Consider migrating to: {new_api}"
        warnings.warn(msg, DeprecationWarning, stacklevel=3)

    def _ensure_unified_data(self):
        """Ensure unified storage has data by migrating if necessary."""
        if self.auto_migrate:
            try:
                # Check if unified storage has any quality data
                current_score = self.unified_storage.get_quality_score()
                if current_score == 0.0:
                    # No data in unified storage, attempt migration
                    from parameter_migration import MigrationManager

                    migration_manager = MigrationManager(self.unified_storage)
                    migration_result = migration_manager.execute_gradual_migration(source_types=["quality"], dry_run=False)
                    if migration_result["items_migrated"] > 0:
                        print(f"Migrated {migration_result['items_migrated']} items to unified storage")
            except Exception as e:
                warnings.warn(f"Failed to auto-migrate: {e}", DeprecationWarning)


# Legacy QualityTracker Compatibility
class QualityTrackerCompatibility:
"""
    Compatibility layer for legacy QualityTracker API.
"""
"""

"""
    def __init__(self, tracker_dir: str = ".claude-patterns"):
"""
        Initialize compatibility wrapper.

        Args:
            tracker_dir: Legacy tracker directory (ignored, uses unified storage)
"""
        # Use unified storage from .claude-unified directory
        unified_dir = ".claude-unified"
        self.unified_storage = UnifiedParameterStorage(unified_dir)
        self.compatibility = CompatibilityLayer(self.unified_storage)

        # Show deprecation warning
        warnings.warn(
            "QualityTracker(tracker_dir) is deprecated. Use UnifiedParameterStorage() instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        self._ensure_unified_data()

"""
    def _ensure_unified_data(self):
        """Ensure unified storage has data by migrating if necessary."""
        if self.compatibility.auto_migrate:
            try:
                # Check if unified storage has any quality data
                current_score = self.unified_storage.get_quality_score()
                if current_score == 0.0:
                    # No data in unified storage, attempt migration
                    from parameter_migration import MigrationManager

                    migration_manager = MigrationManager(self.unified_storage)
                    migration_result = migration_manager.execute_gradual_migration(source_types=["quality"], dry_run=False)
                    if migration_result["items_migrated"] > 0:
                        print(f"Migrated {migration_result['items_migrated']} items to unified storage")
            except Exception as e:
                warnings.warn(f"Failed to auto-migrate: {e}", DeprecationWarning)

    @deprecated("UnifiedParameterStorage.set_quality_score()")
    def record_quality():
"""
        
        Record quality assessment (legacy API).

        Args:
            task_id: ID of the task assessed
            quality_score: Overall quality score (0.0 to 1.0) - legacy format
            metrics: Dictionary of metric scores

        Returns:
            True on success
"""
        self.compatibility._ensure_unified_data()

        # Convert from legacy 0-1 scale to unified 0-100 scale
        unified_score = quality_score * 100
        unified_metrics = {k: v * 100 for k, v in metrics.items()}

        try:
            self.unified_storage.set_quality_score(unified_score, unified_metrics)
            return True
        except Exception as e:
            print(f"Error recording quality: {e}", file=sys.stderr)
            return False

"""
    @deprecated("UnifiedParameterStorage.get_quality_score()")
    def get_average_quality():
"""
        
        Get average quality score (legacy API).

        Args:
            days: Number of days to analyze

        Returns:
            Average quality score (0.0 to 1.0) - legacy format
"""
        self.compatibility._ensure_unified_data()

        try:
            # Get current score from unified storage and convert to legacy format
            unified_score = self.unified_storage.get_quality_score()
            return unified_score / 100.0  # Convert to 0-1 scale
        except Exception:
            return 0.0

"""
    @deprecated("UnifiedParameterStorage.get_quality_history()")
    def get_quality_trends():
"""
        
        Get quality trends (legacy API).

        Args:
            days: Number of days to analyze
            metric: Specific metric to analyze

        Returns:
            Dictionary with trend analysis in legacy format
"""
        self.compatibility._ensure_unified_data()

        try:
            history = self.unified_storage.get_quality_history(days)

            if not history:
                return {
                    "period_days": days,
                    "metric": metric or "quality_score",
                    "data_points": 0,
                    "trend": "no_data",
                    "current_average": 0.0,
                    "previous_average": 0.0,
                    "change_percentage": 0.0,
                    "timeline": [],
                }

            # Convert to legacy format
            values = []
            timeline = []
            for entry in history:
                value = entry.get("score", 0) / 100.0  # Convert to 0-1 scale
                values.append(value)
                timeline.append({"timestamp": entry.get("timestamp", ""), "task_id": entry.get("task_id", ""), "value": value})

            # Calculate trends (simplified)
            if len(values) >= 2:
                first_half = values[: len(values) // 2]
                second_half = values[len(values) // 2 :]

                first_avg = sum(first_half) / len(first_half)
                second_avg = sum(second_half) / len(second_half)

                if first_avg > 0:
                    change_pct = ((second_avg - first_avg) / first_avg) * 100
                else:
                    change_pct = 0.0

                if change_pct > 5:
                    trend = "improving"
                elif change_pct < -5:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "stable"
                first_avg = values[0] if values else 0.0
                second_avg = values[0] if values else 0.0
                change_pct = 0.0

            return {
                "period_days": days,
                "metric": metric or "quality_score",
                "data_points": len(values),
                "trend": trend,
                "current_average": second_avg,
                "previous_average": first_avg,
                "change_percentage": change_pct,
                "timeline": timeline,
            }

        except Exception as e:
            print(f"Error getting quality trends: {e}", file=sys.stderr)
            return {
                "period_days": days,
                "metric": metric or "quality_score",
                "data_points": 0,
                "trend": "error",
                "current_average": 0.0,
                "previous_average": 0.0,
                "change_percentage": 0.0,
                "timeline": [],
            }


# Legacy ModelPerformanceManager Compatibility
"""
class ModelPerformanceManagerCompatibility:
"""
    Compatibility layer for legacy ModelPerformanceManager API.
"""
"""

"""
    def __init__(self, patterns_dir: str = ".claude-patterns"):
"""
        Initialize compatibility wrapper.

        Args:
            patterns_dir: Legacy patterns directory (ignored, uses unified storage)
"""
        # Use unified storage from .claude-unified directory
        unified_dir = ".claude-unified"
        self.unified_storage = UnifiedParameterStorage(unified_dir)
        self.compatibility = CompatibilityLayer(self.unified_storage)

        # Show deprecation warning
        warnings.warn(
            "ModelPerformanceManager(patterns_dir) is deprecated. Use UnifiedParameterStorage() with model methods instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        self._ensure_unified_data()

"""
    def _ensure_unified_data(self):
        """Ensure unified storage has data by migrating if necessary."""
        if self.compatibility.auto_migrate:
            try:
                # Check if unified storage has any model data
                dashboard_data = self.unified_storage.get_dashboard_data()
                model_data = dashboard_data["models"]["performance"]
                if not model_data:
                    # No data in unified storage, attempt migration
                    from parameter_migration import MigrationManager

                    migration_manager = MigrationManager(self.unified_storage)
                    migration_result = migration_manager.execute_gradual_migration(
                        source_types=["model_performance"], dry_run=False
                    )
                    if migration_result["items_migrated"] > 0:
                        print(f"Migrated {migration_result['items_migrated']} model items to unified storage")
            except Exception as e:
                warnings.warn(f"Failed to auto-migrate: {e}", DeprecationWarning)

    @deprecated("UnifiedParameterStorage.update_model_performance()")
    def add_performance_score(self, model: str, score: float, task_type: str = "unknown", contribution: float = 0.0):
"""
        Add performance score for model (legacy API).

        Args:
            model: Model name
            score: Performance score (0-100)
            task_type: Type of task performed
            contribution: Contribution to project (0-100)
"""
        self.compatibility._ensure_unified_data()

        try:
            self.unified_storage.update_model_performance(model, score, task_type)
        except Exception as e:
            print(f"Error adding performance score: {e}", file=sys.stderr)

"""
    @deprecated("UnifiedParameterStorage.get_model_performance()")
    def get_model_summary():
"""
        
        Get performance summary for model (legacy API).

        Args:
            model: Model name

        Returns:
            Model performance summary
"""
        self.compatibility._ensure_unified_data()

        try:
            return self.unified_storage.get_model_performance(model)
        except Exception as e:
            print(f"Error getting model summary: {e}", file=sys.stderr)
            return {"error": f"Failed to get summary for model '{model}'"}

"""
    @deprecated("UnifiedParameterStorage.get_active_model()")
    def get_active_model(self) -> str:
        """Get currently active model."""
        self.compatibility._ensure_unified_data()

        try:
            return self.unified_storage.get_active_model()
        except Exception:
            return "Claude"  # Default fallback


# Dashboard Data Collector Compatibility
class DashboardDataCollectorCompatibility:
"""
    Compatibility layer for legacy DashboardDataCollector API.
"""
"""

"""
    def __init__(self, patterns_dir: str = ".claude-patterns"):
"""
        Initialize compatibility wrapper.

        Args:
            patterns_dir: Legacy patterns directory (ignored, uses unified storage)
"""
        self._show_deprecation_warning(
            "DashboardDataCollector(patterns_dir)", "UnifiedParameterStorage().get_dashboard_data()"
        )

        # Use unified storage from .claude-unified directory
        unified_dir = ".claude-unified"
        self.unified_storage = UnifiedParameterStorage(unified_dir)
        self.compatibility = CompatibilityLayer(self.unified_storage)

"""
    @deprecated("UnifiedParameterStorage.get_dashboard_data()")
    def collect_all_data():
"""
        
        Collect all dashboard data (legacy API).

        Returns:
            Dictionary with dashboard data
"""
        self.compatibility._ensure_unified_data()

        try:
            return self.unified_storage.get_dashboard_data()
        except Exception as e:
            print(f"Error collecting dashboard data: {e}", file=sys.stderr)
            return {
                "quality": {"scores": {"current": 0.0}, "metrics": {}},
                "models": {"active_model": "Claude", "performance": {}},
                "dashboard": {"metrics": {}, "real_time": {}},
                "learning": {"patterns": {}, "analytics": {}},
            }

"""
    @deprecated("UnifiedParameterStorage.update_dashboard_metrics()")
    def update_activity_metrics(self, metrics: Dict[str, Any]):
"""
        Update activity metrics (legacy API).

        Args:
            metrics: Dictionary of metrics to update
"""
        self.compatibility._ensure_unified_data()

        try:
            self.unified_storage.update_dashboard_metrics(metrics)
        except Exception as e:
            print(f"Error updating activity metrics: {e}", file=sys.stderr)


# Module-level compatibility functions
"""
def get_legacy_quality_tracker():
"""
        
        Get legacy QualityTracker with compatibility layer.

    Args:
        tracker_dir: Legacy tracker directory

    Returns:
        Compatibility wrapper for QualityTracker
"""
    return QualityTrackerCompatibility(tracker_dir)


"""
def get_legacy_model_performance_manager():
"""
        
        Get legacy ModelPerformanceManager with compatibility layer.

    Args:
        patterns_dir: Legacy patterns directory

    Returns:
        Compatibility wrapper for ModelPerformanceManager
"""
    return ModelPerformanceManagerCompatibility(patterns_dir)


"""
def get_legacy_dashboard_collector():
"""
        
        Get legacy DashboardDataCollector with compatibility layer.

    Args:
        patterns_dir: Legacy patterns directory

    Returns:
        Compatibility wrapper for DashboardDataCollector
"""
    return DashboardDataCollectorCompatibility(patterns_dir)


# Auto-patch existing modules
"""
def auto_patch_legacy_modules():
"""
    Automatically patch imports of legacy modules to use compatibility layer.

    This function should be called early in the application startup to ensure
    all legacy module imports are redirected to the compatibility layer.
"""
"""
    import sys

    # Create compatibility modules
    compatibility_modules = {
        "quality_tracker": QualityTrackerCompatibility,
        "model_performance": ModelPerformanceManagerCompatibility,
        "dashboard": DashboardDataCollectorCompatibility,
    }

    # Store original modules
    original_modules = {}

    for module_name, compatibility_class in compatibility_modules.items():
        try:
            # Try to import the original module
            original_module = __import__(f"lib.{module_name}", fromlist=[module_name])
            original_modules[module_name] = original_module

            # Replace with compatibility wrapper
            compatibility_instance = compatibility_class()
            sys.modules[f"lib.{module_name}"] = compatibility_instance

        except ImportError:
            # Module doesn't exist, create compatibility module from scratch
            compatibility_instance = compatibility_class()
            sys.modules[f"lib.{module_name}"] = compatibility_instance

    return original_modules


# Monkey patch functions for common legacy APIs
def monkey_patch_quality_functions():
    """Monkey patch common quality tracking functions."""

    def legacy_record_quality(task_id: str, quality_score: float, metrics: Dict[str, float]):
        """Legacy record_quality function."""
        tracker = get_legacy_quality_tracker()
        return tracker.record_quality(task_id, quality_score, metrics)

    def legacy_get_quality_score() -> float:
        """Legacy get_quality_score function."""
        tracker = get_legacy_quality_tracker()
        return tracker.get_average_quality()

    # Add to module's global namespace
    globals()["record_quality"] = legacy_record_quality
    globals()["get_quality_score"] = legacy_get_quality_score


def monkey_patch_model_functions():
    """Monkey patch common model performance functions."""

    def legacy_add_model_score(model: str, score: float, task_type: str = "unknown"):
        """Legacy add_model_score function."""
        manager = get_legacy_model_performance_manager()
        manager.add_performance_score(model, score, task_type)

    def legacy_get_model_summary(model: str) -> Dict[str, Any]:
        """Legacy get_model_summary function."""
        manager = get_legacy_model_performance_manager()
        return manager.get_model_summary(model)

    # Add to module's global namespace
    globals()["add_model_score"] = legacy_add_model_score
    globals()["get_model_summary"] = legacy_get_model_summary


# Enable compatibility mode
def enable_compatibility_mode(auto_patch: bool = True, monkey_patch: bool = True):
"""
    Enable full compatibility mode for legacy parameter storage APIs.

    Args:
        auto_patch: Whether to auto-patch module imports
        monkey_patch: Whether to monkey patch common functions
"""
    if auto_patch:
        original_modules = auto_patch_legacy_modules()
        print("Compatibility mode enabled: Legacy modules auto-patched")

    if monkey_patch:
        monkey_patch_quality_functions()
        monkey_patch_model_functions()
        print("Compatibility mode enabled: Common functions monkey-patched")

    # Configure warnings to show deprecation warnings
    warnings.filterwarnings("default", category=DeprecationWarning)

    print("Parameter compatibility layer is active")
    print("Legacy APIs will work but show deprecation warnings")
    print("Consider migrating to UnifiedParameterStorage for new code")


# Initialize compatibility mode if this module is imported directly
if __name__ != "__main__" and "parameter_compatibility" in sys.modules:
    # Auto-enable compatibility mode when imported
    enable_compatibility_mode(auto_patch=False, monkey_patch=False)


"""
def main():
    """Command-line interface for compatibility layer."""
    import argparse

    parser = argparse.ArgumentParser(description="Parameter Compatibility Layer")
    parser.add_argument("--enable", action="store_true", help="Enable compatibility mode")
    parser.add_argument("--test", action="store_true", help="Test compatibility layer")
    parser.add_argument("--storage-dir", default=".claude-unified", help="Unified storage directory")

    args = parser.parse_args()

    if args.enable:
        enable_compatibility_mode()
        print("Compatibility layer enabled")

    elif args.test:
        print("Testing compatibility layer...")

        # Test quality tracker compatibility
        tracker = get_legacy_quality_tracker()
        success = tracker.record_quality("test_task", 0.85, {"code_quality": 0.9, "test_quality": 0.8})
        print(f"Quality tracking test: {'PASSED' if success else 'FAILED'}")

        # Test model performance compatibility
        model_manager = get_legacy_model_performance_manager()
        model_manager.add_performance_score("Claude", 92.5, "testing")
        summary = model_manager.get_model_summary("Claude")
        print(f"Model performance test: {'PASSED' if 'error' not in summary else 'FAILED'}")

        # Test dashboard compatibility
        dashboard = get_legacy_dashboard_collector()
        data = dashboard.collect_all_data()
        print(f"Dashboard test: {'PASSED' if data else 'FAILED'}")

        print("Compatibility layer test completed")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
