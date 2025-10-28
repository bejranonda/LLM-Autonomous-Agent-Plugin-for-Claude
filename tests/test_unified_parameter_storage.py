#!/usr/bin/env python3
"""
Comprehensive Test Suite for Unified Parameter Storage System

Tests all components of the unified parameter storage system including:
- Core storage functionality
- Thread safety and concurrency
- Migration system
- Compatibility layer
- Performance and reliability

Version: 1.0.0
Author: Autonomous Agent Development Team
"""

import unittest
import json
import tempfile
import shutil
import threading
import time
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any

# Add lib directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    from unified_parameter_storage import UnifiedParameterStorage, ParameterSchema
    from parameter_migration import MigrationManager, LegacyStorageAdapter
    from parameter_compatibility import (
        QualityTrackerCompatibility, ModelPerformanceManagerCompatibility,
        enable_compatibility_mode
    )
    UNIFIED_STORAGE_AVAILABLE = True
except ImportError as e:
    UNIFIED_STORAGE_AVAILABLE = False
    print(f"Warning: Unified parameter storage not available for testing: {e}", file=sys.stderr)


class TestUnifiedParameterStorage(unittest.TestCase):
    """Test core unified parameter storage functionality."""

    def setUp(self):
        """Set up test environment."""
        if not UNIFIED_STORAGE_AVAILABLE:
            self.skipTest("Unified parameter storage not available")

        # Create temporary directory for tests
        self.test_dir = tempfile.mkdtemp(prefix="unified_storage_test_")
        self.storage = UnifiedParameterStorage(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        if hasattr(self, 'test_dir') and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_initialization(self):
        """Test storage initialization."""
        # Check that storage file was created
        self.assertTrue(self.storage.storage_file.exists())

        # Check initial data structure
        data = self.storage._read_data()
        self.assertIn("version", data)
        self.assertIn("metadata", data)
        self.assertIn("parameters", data)
        self.assertEqual(data["version"], ParameterSchema.CURRENT_VERSION)

    def test_quality_score_operations(self):
        """Test quality score get/set operations."""
        # Test setting quality score
        test_score = 85.5
        test_metrics = {
            "syntax_compliance": 90.0,
            "functionality": 85.0,
            "documentation": 80.0,
            "pattern_adherence": 88.0,
            "code_metrics": 82.0
        }

        self.storage.set_quality_score(test_score, test_metrics)

        # Test getting quality score
        retrieved_score = self.storage.get_quality_score()
        self.assertEqual(retrieved_score, test_score)

        # Test quality history
        history = self.storage.get_quality_history(days=30)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["score"], test_score)

        # Check metrics were stored
        data = self.storage._read_data()
        stored_metrics = data["parameters"]["quality"]["metrics"]
        for key, value in test_metrics.items():
            self.assertEqual(stored_metrics[key], value)

    def test_quality_score_validation(self):
        """Test quality score validation."""
        # Test invalid scores
        with self.assertRaises(ValueError):
            self.storage.set_quality_score(-10.0)

        with self.assertRaises(ValueError):
            self.storage.set_quality_score(110.0)

        with self.assertRaises(ValueError):
            self.storage.set_quality_score("invalid")

        # Test invalid metrics
        with self.assertRaises(ValueError):
            self.storage.set_quality_score(85.0, {"invalid_metric": -5.0})

    def test_model_performance_operations(self):
        """Test model performance operations."""
        # Test setting active model
        test_model = "TestModel"
        self.storage.set_active_model(test_model)
        self.assertEqual(self.storage.get_active_model(), test_model)

        # Test updating model performance
        test_score = 92.0
        test_task_type = "testing"
        self.storage.update_model_performance(test_model, test_score, test_task_type)

        # Test getting model performance
        perf_data = self.storage.get_model_performance(test_model)
        self.assertNotIn("error", perf_data)
        self.assertEqual(perf_data["total_tasks"], 1)
        self.assertEqual(perf_data["recent_scores"][0]["score"], test_score)
        self.assertEqual(perf_data["recent_scores"][0]["task_type"], test_task_type)

    def test_dashboard_metrics_operations(self):
        """Test dashboard metrics operations."""
        test_metrics = {
            "active_tasks": 5,
            "completed_tasks": 10,
            "failed_tasks": 1,
            "average_response_time": 2.5,
            "system_health": 95.0
        }

        self.storage.update_dashboard_metrics(test_metrics)

        # Verify metrics were stored
        data = self.storage._read_data()
        stored_metrics = data["parameters"]["dashboard"]["metrics"]
        for key, value in test_metrics.items():
            self.assertEqual(stored_metrics[key], value)

        # Test real-time data update
        self.assertIn("last_activity", data["parameters"]["dashboard"]["real_time"])

    def test_learning_patterns_operations(self):
        """Test learning patterns operations."""
        test_patterns = {
            "skill_effectiveness": {
                "code-analysis": {"success_rate": 0.95, "usage_count": 20},
                "quality-standards": {"success_rate": 0.88, "usage_count": 15}
            },
            "task_patterns": [
                {"task_type": "refactoring", "success": True, "quality_score": 92.0}
            ]
        }

        self.storage.update_learning_patterns(test_patterns)

        # Verify patterns were stored
        retrieved_patterns = self.storage.get_learning_patterns()
        self.assertEqual(retrieved_patterns["skill_effectiveness"]["code-analysis"]["success_rate"], 0.95)
        self.assertEqual(len(retrieved_patterns["task_patterns"]), 1)

    def test_autofix_patterns_operations(self):
        """Test auto-fix patterns operations."""
        test_patterns = {
            "typescript": {
                "unused_imports": {
                    "priority": "auto",
                    "success_rate": 1.0,
                    "usage_count": 50
                }
            }
        }

        self.storage.update_autofix_patterns(test_patterns)

        # Verify patterns were stored
        retrieved_patterns = self.storage.get_autofix_patterns()
        self.assertEqual(retrieved_patterns["typescript"]["unused_imports"]["success_rate"], 1.0)

    def test_data_persistence(self):
        """Test that data persists across storage instances."""
        # Set some data
        test_score = 88.0
        self.storage.set_quality_score(test_score)

        # Create new storage instance with same directory
        new_storage = UnifiedParameterStorage(self.test_dir)

        # Verify data persisted
        retrieved_score = new_storage.get_quality_score()
        self.assertEqual(retrieved_score, test_score)

    def test_storage_stats(self):
        """Test storage statistics functionality."""
        # Add some data
        self.storage.set_quality_score(85.0)
        self.storage.set_active_model("TestModel")
        self.storage.update_model_performance("TestModel", 90.0)

        # Get stats
        stats = self.storage.get_storage_stats()

        self.assertIn("version", stats)
        self.assertIn("created_at", stats)
        self.assertIn("last_updated", stats)
        self.assertIn("storage_size", stats)
        self.assertIn("parameter_counts", stats)
        self.assertGreater(stats["storage_size"], 0)

    def test_data_validation(self):
        """Test data integrity validation."""
        # Test valid data
        validation = self.storage.validate_data_integrity()
        self.assertTrue(validation["valid"])
        self.assertEqual(len(validation["errors"]), 0)

        # Test with corrupted data (simulate corruption)
        with open(self.storage.storage_file, 'w') as f:
            f.write('{"invalid": "json"}')

        validation = self.storage.validate_data_integrity()
        self.assertFalse(validation["valid"])
        self.assertGreater(len(validation["errors"]), 0)

    def test_export_import(self):
        """Test data export and import functionality."""
        # Add test data
        self.storage.set_quality_score(87.5)
        self.storage.set_active_model("TestModel")

        # Test JSON export
        export_path = os.path.join(self.test_dir, "export.json")
        success = self.storage.export_data(export_path, "json")
        self.assertTrue(success)
        self.assertTrue(os.path.exists(export_path))

        # Test CSV export (quality scores)
        csv_path = os.path.join(self.test_dir, "export.csv")
        success = self.storage.export_data(csv_path, "csv")
        self.assertTrue(success)
        self.assertTrue(os.path.exists(csv_path))

        # Test import
        import_path = os.path.join(self.test_dir, "import.json")
        shutil.copy2(export_path, import_path)

        new_storage = UnifiedParameterStorage(os.path.join(self.test_dir, "new"))
        success = new_storage.import_data(import_path, "overwrite")
        self.assertTrue(success)

        # Verify imported data
        imported_score = new_storage.get_quality_score()
        self.assertEqual(imported_score, 87.5)

    def test_backup_restore(self):
        """Test backup and restore functionality."""
        # Add test data
        self.storage.set_quality_score(92.0)

        # Create backup
        self.storage._create_backup()
        backup_files = list(self.storage.backup_dir.glob("*.json"))
        self.assertEqual(len(backup_files), 1)

        # Corrupt current data
        with open(self.storage.storage_file, 'w') as f:
            f.write('{"corrupted": "data"}')

        # Restore from backup
        success = self.storage._restore_from_backup()
        self.assertTrue(success)

        # Verify data was restored
        restored_score = self.storage.get_quality_score()
        self.assertEqual(restored_score, 92.0)


class TestThreadSafety(unittest.TestCase):
    """Test thread safety of unified parameter storage."""

    def setUp(self):
        """Set up test environment."""
        if not UNIFIED_STORAGE_AVAILABLE:
            self.skipTest("Unified parameter storage not available")

        self.test_dir = tempfile.mkdtemp(prefix="thread_safety_test_")
        self.storage = UnifiedParameterStorage(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        if hasattr(self, 'test_dir') and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_concurrent_quality_updates(self):
        """Test concurrent quality score updates."""
        num_threads = 10
        updates_per_thread = 50

        def update_quality(thread_id):
            for i in range(updates_per_thread):
                score = 70.0 + (thread_id * 10 + i) % 30  # Scores 70-100
                metrics = {
                    "syntax_compliance": score,
                    "functionality": score - 5.0,
                    "documentation": score - 10.0
                }
                self.storage.set_quality_score(score, metrics)
                time.sleep(0.001)  # Small delay to increase contention

        # Run concurrent updates
        threads = []
        for thread_id in range(num_threads):
            thread = threading.Thread(target=update_quality, args=(thread_id,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify data integrity
        history = self.storage.get_quality_history(days=30)
        expected_updates = num_threads * updates_per_thread
        self.assertEqual(len(history), expected_updates)

        # Verify final state is consistent
        final_score = self.storage.get_quality_score()
        self.assertGreaterEqual(final_score, 70.0)
        self.assertLessEqual(final_score, 100.0)

    def test_concurrent_model_updates(self):
        """Test concurrent model performance updates."""
        models = ["Claude", "OpenAI", "GLM", "Gemini"]
        num_threads = 20
        updates_per_thread = 25

        def update_model_performance(thread_id):
            for i in range(updates_per_thread):
                model = models[thread_id % len(models)]
                score = 75.0 + (thread_id * 5 + i) % 25  # Scores 75-100
                task_type = f"task_{thread_id}_{i}"
                self.storage.update_model_performance(model, score, task_type)
                time.sleep(0.001)

        # Run concurrent updates
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(update_model_performance, thread_id)
                for thread_id in range(num_threads)
            ]

            # Wait for completion
            for future in as_completed(futures):
                future.result()

        # Verify data integrity
        for model in models:
            perf_data = self.storage.get_model_performance(model)
            if "error" not in perf_data:
                expected_updates = (num_threads // len(models)) * updates_per_thread
                if num_threads % len(models) > models.index(model):
                    expected_updates += updates_per_thread
                self.assertEqual(perf_data["total_tasks"], expected_updates)

    def test_concurrent_read_write(self):
        """Test concurrent read and write operations."""
        num_writers = 5
        num_readers = 10
        operations_per_thread = 100

        def writer_operation(writer_id):
            for i in range(operations_per_thread):
                score = 80.0 + (writer_id * 10 + i) % 20
                self.storage.set_quality_score(score)

        def reader_operation(reader_id):
            scores_read = []
            for i in range(operations_per_thread):
                score = self.storage.get_quality_score()
                history = self.storage.get_quality_history(days=30)
                scores_read.append((score, len(history)))
                time.sleep(0.0001)
            return scores_read

        # Start writers
        writer_threads = []
        for writer_id in range(num_writers):
            thread = threading.Thread(target=writer_operation, args=(writer_id,))
            writer_threads.append(thread)
            thread.start()

        # Start readers
        reader_threads = []
        for reader_id in range(num_readers):
            thread = threading.Thread(target=reader_operation, args=(reader_id,))
            reader_threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in writer_threads + reader_threads:
            thread.join()

        # Verify final consistency
        final_history = self.storage.get_quality_history(days=30)
        expected_writes = num_writers * operations_per_thread
        self.assertEqual(len(final_history), expected_writes)


class TestMigrationSystem(unittest.TestCase):
    """Test migration system functionality."""

    def setUp(self):
        """Set up test environment."""
        if not UNIFIED_STORAGE_AVAILABLE:
            self.skipTest("Unified parameter storage not available")

        self.test_dir = tempfile.mkdtemp(prefix="migration_test_")
        self.unified_storage = UnifiedParameterStorage(self.test_dir)
        self.migration_manager = MigrationManager(self.unified_storage)

        # Create legacy data files for testing
        self.create_legacy_data()

    def tearDown(self):
        """Clean up test environment."""
        if hasattr(self, 'test_dir') and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def create_legacy_data(self):
        """Create legacy data files for migration testing."""
        # Create legacy quality history
        quality_dir = Path(self.test_dir) / ".claude-quality"
        quality_dir.mkdir(exist_ok=True)

        quality_history = [
            {
                "task_id": "legacy_task_1",
                "quality_score": 0.85,
                "timestamp": "2025-01-01T10:00:00Z",
                "metrics": {"syntax_compliance": 0.9, "functionality": 0.8}
            },
            {
                "task_id": "legacy_task_2",
                "quality_score": 0.92,
                "timestamp": "2025-01-02T11:00:00Z",
                "metrics": {"syntax_compliance": 0.95, "functionality": 0.88}
            }
        ]

        with open(quality_dir / "quality_history.json", 'w') as f:
            json.dump(quality_history, f)

        # Create legacy model performance
        patterns_dir = Path(self.test_dir) / ".claude-patterns"
        patterns_dir.mkdir(exist_ok=True)

        model_performance = {
            "Claude": {
                "recent_scores": [
                    {"score": 88.5, "timestamp": "2025-01-01T10:00:00Z", "task_type": "feature"},
                    {"score": 91.2, "timestamp": "2025-01-02T11:00:00Z", "task_type": "bugfix"}
                ],
                "total_tasks": 25,
                "success_rate": 0.92,
                "contribution_to_project": 85.0
            },
            "GLM": {
                "recent_scores": [
                    {"score": 82.3, "timestamp": "2025-01-01T12:00:00Z", "task_type": "testing"}
                ],
                "total_tasks": 8,
                "success_rate": 0.75,
                "contribution_to_project": 70.0
            }
        }

        with open(patterns_dir / "model_performance.json", 'w') as f:
            json.dump(model_performance, f)

        # Create legacy patterns
        patterns_data = {
            "patterns": [
                {
                    "task_type": "refactoring",
                    "context": {"language": "python", "framework": "flask"},
                    "execution": {"skills_used": ["code-analysis", "quality-standards"]},
                    "outcome": {"success": True, "quality_score": 0.88}
                }
            ],
            "skill_effectiveness": {
                "code-analysis": {"success_rate": 0.95, "usage_count": 15},
                "quality-standards": {"success_rate": 0.88, "usage_count": 12}
            }
        }

        with open(patterns_dir / "patterns.json", 'w') as f:
            json.dump(patterns_data, f)

    def test_migration_complexity_analysis(self):
        """Test migration complexity analysis."""
        analysis = self.migration_manager.analyze_migration_complexity()

        self.assertIn("total_sources", analysis)
        self.assertIn("source_types", analysis)
        self.assertIn("estimated_time_minutes", analysis)
        self.assertIn("complexity_level", analysis)
        self.assertIn("recommendations", analysis)

        self.assertGreater(analysis["total_sources"], 0)
        self.assertIn("quality", analysis["source_types"])
        self.assertIn("model_performance", analysis["source_types"])
        self.assertIn("patterns", analysis["source_types"])

    def test_dry_run_migration(self):
        """Test dry run migration."""
        result = self.migration_manager.execute_gradual_migration(dry_run=True)

        self.assertEqual(result["status"], "dry_run_completed")
        self.assertEqual(result["sources_processed"], 0)  # Dry run doesn't process
        self.assertEqual(result["items_migrated"], 0)
        self.assertGreater(len(result["source_results"]), 0)

    def test_actual_migration(self):
        """Test actual migration execution."""
        result = self.migration_manager.execute_gradual_migration(dry_run=False)

        self.assertEqual(result["status"], "completed")
        self.assertGreater(result["sources_processed"], 0)
        self.assertGreater(result["items_migrated"], 0)

        # Verify migrated data in unified storage
        quality_history = self.unified_storage.get_quality_history(days=30)
        self.assertGreater(len(quality_history), 0)

        # Check specific migrated items
        migrated_scores = [entry["score"] for entry in quality_history]
        self.assertIn(85.0, migrated_scores)  # 0.85 * 100 from legacy
        self.assertIn(92.0, migrated_scores)  # 0.92 * 100 from legacy

        # Verify model performance migration
        claude_perf = self.unified_storage.get_model_performance("Claude")
        self.assertNotIn("error", claude_perf)
        self.assertGreater(claude_perf["total_tasks"], 0)

        # Verify learning patterns migration
        learning_patterns = self.unified_storage.get_learning_patterns()
        self.assertIn("skill_effectiveness", learning_patterns)
        self.assertIn("code-analysis", learning_patterns["skill_effectiveness"])

    def test_migration_validation(self):
        """Test migration validation."""
        # Execute migration first
        self.migration_manager.execute_gradual_migration(dry_run=False)

        # Validate migration
        validation = self.migration_manager.validate_migration()

        self.assertIn("overall_status", validation)
        self.assertIn("data_integrity", validation)
        self.assertIn("completeness", validation)
        self.assertIn("issues", validation)
        self.assertIn("recommendations", validation)

        # Should be successful with our test data
        self.assertIn(validation["overall_status"], ["success", "acceptable"])

    def test_rollback_functionality(self):
        """Test migration rollback functionality."""
        # Execute migration
        self.migration_manager.execute_gradual_migration(dry_run=False)

        # Verify migration occurred
        quality_history = self.unified_storage.get_quality_history(days=30)
        original_count = len(quality_history)
        self.assertGreater(original_count, 0)

        # Test rollback (note: this tests the rollback mechanism structure)
        # In practice, rollback would restore from backup files
        rollback_result = self.migration_manager.rollback_migration()

        self.assertIn("status", rollback_result)
        self.assertIn("sources_restored", rollback_result)


class TestCompatibilityLayer(unittest.TestCase):
    """Test compatibility layer functionality."""

    def setUp(self):
        """Set up test environment."""
        if not UNIFIED_STORAGE_AVAILABLE:
            self.skipTest("Unified parameter storage not available")

        self.test_dir = tempfile.mkdtemp(prefix="compatibility_test_")
        self.unified_storage = UnifiedParameterStorage(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        if hasattr(self, 'test_dir') and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_quality_tracker_compatibility(self):
        """Test QualityTracker compatibility wrapper."""
        # Create compatibility wrapper
        compat_tracker = QualityTrackerCompatibility()

        # Test legacy API (0-1 scale)
        legacy_score = 0.85
        legacy_metrics = {"syntax_compliance": 0.9, "functionality": 0.8}

        success = compat_tracker.record_quality("test_task", legacy_score, legacy_metrics)
        self.assertTrue(success)

        # Test retrieval (should convert back to 0-1 scale)
        retrieved_score = compat_tracker.get_average_quality()
        self.assertAlmostEqual(retrieved_score, legacy_score, places=5)

        # Test trends
        trends = compat_tracker.get_quality_trends(days=30)
        self.assertIn("period_days", trends)
        self.assertIn("trend", trends)

    def test_model_performance_compatibility(self):
        """Test ModelPerformanceManager compatibility wrapper."""
        # Create compatibility wrapper
        compat_manager = ModelPerformanceManagerCompatibility()

        # Test legacy API
        compat_manager.add_performance_score("TestModel", 92.5, "testing", 85.0)

        # Test retrieval
        summary = compat_manager.get_model_summary("TestModel")
        self.assertNotIn("error", summary)
        self.assertGreater(summary["total_tasks"], 0)

        # Test active model
        active_model = compat_manager.get_active_model()
        self.assertIsInstance(active_model, str)

    def test_compatibility_mode_enable(self):
        """Test enabling compatibility mode."""
        # This should not raise an exception
        enable_compatibility_mode(auto_patch=False, monkey_patch=False)

        # Test that compatibility functions are available
        from parameter_compatibility import (
            get_legacy_quality_tracker, get_legacy_model_performance_manager
        )

        tracker = get_legacy_quality_tracker()
        self.assertIsNotNone(tracker)

        manager = get_legacy_model_performance_manager()
        self.assertIsNotNone(manager)


class TestPerformanceAndReliability(unittest.TestCase):
    """Test performance and reliability aspects."""

    def setUp(self):
        """Set up test environment."""
        if not UNIFIED_STORAGE_AVAILABLE:
            self.skipTest("Unified parameter storage not available")

        self.test_dir = tempfile.mkdtemp(prefix="performance_test_")
        self.storage = UnifiedParameterStorage(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        if hasattr(self, 'test_dir') and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_large_data_handling(self):
        """Test handling of large datasets."""
        # Test with large quality history
        num_entries = 1000
        start_time = time.time()

        for i in range(num_entries):
            score = 70.0 + (i % 30)  # Vary scores between 70-100
            self.storage.set_quality_score(score)

        write_time = time.time() - start_time

        # Test retrieval performance
        start_time = time.time()
        history = self.storage.get_quality_history(days=365)
        read_time = time.time() - start_time

        # Verify data integrity
        self.assertEqual(len(history), num_entries)

        # Performance assertions (should complete within reasonable time)
        self.assertLess(write_time, 5.0)  # Should write 1000 entries in < 5 seconds
        self.assertLess(read_time, 1.0)   # Should read in < 1 second

    def test_cache_performance(self):
        """Test caching functionality."""
        # Add data
        self.storage.set_quality_score(85.0)

        # First read (should cache)
        start_time = time.time()
        data1 = self.storage._read_data(use_cache=True)
        first_read_time = time.time() - start_time

        # Second read (should use cache)
        start_time = time.time()
        data2 = self.storage._read_data(use_cache=True)
        second_read_time = time.time() - start_time

        # Verify cache hit
        self.assertEqual(data1, data2)
        self.assertLess(second_read_time, first_read_time)

    def test_memory_usage(self):
        """Test memory usage with large datasets."""
        import psutil
        import gc

        # Get baseline memory
        gc.collect()
        process = psutil.Process()
        baseline_memory = process.memory_info().rss

        # Add large amount of data
        for i in range(2000):
            self.storage.set_quality_score(75.0 + (i % 25))
            if i % 100 == 0:
                # Periodically check memory
                current_memory = process.memory_info().rss
                memory_increase = current_memory - baseline_memory
                # Should not increase excessively (less than 100MB)
                self.assertLess(memory_increase, 100 * 1024 * 1024)

        # Final memory check
        gc.collect()
        final_memory = process.memory_info().rss
        total_increase = final_memory - baseline_memory

        # Total memory increase should be reasonable
        self.assertLess(total_increase, 200 * 1024 * 1024)  # Less than 200MB

    def test_concurrent_performance(self):
        """Test performance under concurrent load."""
        num_threads = 20
        operations_per_thread = 100

        def worker_operation(thread_id):
            start_time = time.time()
            for i in range(operations_per_thread):
                score = 70.0 + (thread_id * 10 + i) % 30
                self.storage.set_quality_score(score)

                # Occasionally read data
                if i % 10 == 0:
                    self.storage.get_quality_score()
                    self.storage.get_quality_history(days=7)

            return time.time() - start_time

        # Run concurrent operations
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(worker_operation, thread_id)
                for thread_id in range(num_threads)
            ]

            execution_times = []
            for future in as_completed(futures):
                execution_times.append(future.result())

        # Performance assertions
        avg_time = sum(execution_times) / len(execution_times)
        max_time = max(execution_times)

        # All threads should complete within reasonable time
        self.assertLess(avg_time, 10.0)  # Average < 10 seconds
        self.assertLess(max_time, 15.0)  # Maximum < 15 seconds

        # Verify data integrity
        final_history = self.storage.get_quality_history(days=30)
        expected_entries = num_threads * operations_per_thread
        self.assertEqual(len(final_history), expected_entries)


def run_tests():
    """Run all tests and generate report."""
    print("Running Unified Parameter Storage Test Suite")
    print("=" * 50)

    if not UNIFIED_STORAGE_AVAILABLE:
        print("ERROR: Unified parameter storage not available")
        print("Please ensure the unified_parameter_storage module is in the lib directory")
        return False

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test cases
    test_classes = [
        TestUnifiedParameterStorage,
        TestThreadSafety,
        TestMigrationSystem,
        TestCompatibilityLayer,
        TestPerformanceAndReliability
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Generate summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")

    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")

    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun
    print(f"\nSuccess Rate: {success_rate * 100:.1f}%")

    if success_rate >= 0.95:
        print("✅ EXCELLENT: Test suite passed with high success rate")
    elif success_rate >= 0.85:
        print("✅ GOOD: Test suite passed with acceptable success rate")
    elif success_rate >= 0.70:
        print("⚠️  MARGINAL: Test suite passed but needs improvement")
    else:
        print("❌ POOR: Test suite failed - significant issues found")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)