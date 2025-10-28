#!/usr/bin/env python3
"""
Basic functionality test for unified parameter storage system.

This test verifies the core functionality and backward compatibility
without requiring the full test suite.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

def test_basic_storage():
    """Test basic storage functionality."""
    print("Testing basic storage functionality...")

    try:
        from unified_parameter_storage import UnifiedParameterStorage

        # Create temporary directory
        test_dir = tempfile.mkdtemp(prefix="basic_test_")

        try:
            # Initialize storage
            storage = UnifiedParameterStorage(test_dir)

            # Test quality score operations
            storage.set_quality_score(85.5, {
                "syntax_compliance": 90.0,
                "functionality": 85.0,
                "documentation": 80.0
            })

            score = storage.get_quality_score()
            assert abs(score - 85.5) < 0.01, f"Expected 85.5, got {score}"

            # Test model performance operations
            storage.update_model_performance("Claude", 92.0, "testing")
            perf = storage.get_model_performance("Claude")
            assert "error" not in perf, f"Model performance error: {perf}"

            # Test dashboard operations
            storage.update_dashboard_metrics({
                "active_tasks": 5,
                "system_health": 95.0
            })

            dashboard_data = storage.get_dashboard_data()
            assert "quality" in dashboard_data, "Dashboard data missing quality section"
            assert "models" in dashboard_data, "Dashboard data missing models section"

            print("+ Basic storage functionality works")
            return True

        finally:
            # Clean up
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir)

    except Exception as e:
        print(f"- Basic storage functionality failed: {e}")
        return False

def test_compatibility_layer():
    """Test compatibility layer functionality."""
    print("Testing compatibility layer...")

    try:
        from parameter_compatibility import (
            get_legacy_quality_tracker,
            get_legacy_model_performance_manager
        )

        # Test quality tracker compatibility
        tracker = get_legacy_quality_tracker()

        # Use legacy API (0-1 scale)
        success = tracker.record_quality("test_task", 0.85, {
            "syntax_compliance": 0.9,
            "functionality": 0.8
        })
        assert success, "Failed to record quality using legacy API"

        # Get average quality (should be in 0-1 scale)
        avg_quality = tracker.get_average_quality()
        assert abs(avg_quality - 0.85) < 0.05, f"Expected ~0.85, got {avg_quality}"

        # Test model performance compatibility
        manager = get_legacy_model_performance_manager()
        manager.add_performance_score("Claude", 92.5, "testing")

        summary = manager.get_model_summary("Claude")
        assert "error" not in summary, f"Model summary error: {summary}"

        print("+ Compatibility layer works")
        return True

    except Exception as e:
        print(f"- Compatibility layer failed: {e}")
        return False

def test_migration_system():
    """Test migration system functionality."""
    print("Testing migration system...")

    try:
        from unified_parameter_storage import UnifiedParameterStorage
        from parameter_migration import MigrationManager

        # Create temporary directories
        test_dir = tempfile.mkdtemp(prefix="migration_test_")
        legacy_dir = Path(test_dir) / "legacy"
        legacy_dir.mkdir()

        try:
            # Create legacy data
            legacy_quality = legacy_dir / "quality_history.json"
            import json
            with open(legacy_quality, 'w') as f:
                json.dump([{
                    "task_id": "test_task",
                    "quality_score": 0.88,
                    "timestamp": "2025-01-01T12:00:00Z",
                    "metrics": {"syntax_compliance": 0.9}
                }], f)

            # Initialize unified storage
            storage = UnifiedParameterStorage(test_dir)

            # Create migration manager
            migration_manager = MigrationManager(storage)

            # Analyze migration complexity
            analysis = migration_manager.analyze_migration_complexity()
            assert analysis["total_sources"] > 0, "No legacy sources detected"

            # Execute dry run migration
            dry_run_result = migration_manager.execute_gradual_migration(dry_run=True)
            assert dry_run_result["status"] == "dry_run_completed", "Dry run failed"

            print("+ Migration system works")
            return True

        finally:
            # Clean up
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir)

    except Exception as e:
        print(f"- Migration system failed: {e}")
        return False

def test_dashboard_integration():
    """Test dashboard integration."""
    print("Testing dashboard integration...")

    try:
        from lib.dashboard import DashboardDataCollector

        # Create collector (should auto-detect unified storage)
        collector = DashboardDataCollector()

        # Test unified storage methods
        quality_data = collector.get_unified_quality_data()
        assert "current_score" in quality_data, "Missing current score in quality data"
        assert "source" in quality_data, "Missing source indicator in quality data"

        model_data = collector.get_unified_model_data()
        assert "active_model" in model_data, "Missing active model in model data"
        assert "source" in model_data, "Missing source indicator in model data"

        dashboard_data = collector.get_unified_dashboard_data()
        assert "quality" in dashboard_data, "Missing quality in dashboard data"
        assert "models" in dashboard_data, "Missing models in dashboard data"
        assert "timestamp" in dashboard_data, "Missing timestamp in dashboard data"

        # Test update methods
        collector.record_quality_to_unified(90.0, {"test": 85.0})
        collector.update_model_performance_unified("TestModel", 88.0, "test_task")
        collector.update_unified_dashboard_metrics({"test_metric": 42})

        print("+ Dashboard integration works")
        return True

    except Exception as e:
        print(f"- Dashboard integration failed: {e}")
        return False

def main():
    """Run all basic functionality tests."""
    print("Running Basic Functionality Tests")
    print("=" * 40)

    tests = [
        test_basic_storage,
        test_compatibility_layer,
        test_migration_system,
        test_dashboard_integration
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 40)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("*** All tests passed! System is ready for production.")
        return True
    else:
        print(f"!!! {total - passed} test(s) failed. Review issues before deployment.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)