"""
Unit tests for Quality Tracker System

Tests the quality tracking functionality including:
- Quality score recording and retrieval
- Trend analysis and statistics
- Cross-platform file handling with locking
- Data aggregation and reporting
"""

import pytest
import json
import tempfile
import shutil
import os
import sys
from pathlib import Path
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta

# Add lib directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from quality_tracker import QualityTracker


class TestQualityTracker:
    """Test suite for QualityTracker class"""

    @pytest.fixture
    def quality_tracker(self, temp_directory):
        """Create a QualityTracker instance with temporary directory"""
        return QualityTracker(temp_directory)

    @pytest.fixture
    def sample_quality_record(self):
        """Sample quality record for testing"""
        return {
            "task_id": "test_task_001",
            "quality_score": 0.87,
            "metrics": {
                "code_quality": 0.90,
                "test_quality": 0.85,
                "documentation": 0.80,
                "patterns": 0.95,
                "performance": 0.88
            }
        }

    @pytest.fixture
    def existing_quality_file(self, temp_directory):
        """Create an existing quality_history.json file with test data"""
        quality_file = Path(temp_directory) / "quality_history.json"
        test_data = [
            {
                "task_id": "existing_task_001",
                "quality_score": 0.85,
                "timestamp": "2025-01-10T10:00:00",
                "metrics": {
                    "code_quality": 0.90,
                    "test_quality": 0.80,
                    "documentation": 0.85
                }
            },
            {
                "task_id": "existing_task_002",
                "quality_score": 0.92,
                "timestamp": "2025-01-11T14:30:00",
                "metrics": {
                    "code_quality": 0.95,
                    "test_quality": 0.90,
                    "documentation": 0.90
                }
            }
        ]
        with open(quality_file, 'w') as f:
            json.dump(test_data, f)
        return quality_file

    @pytest.mark.unit
    @pytest.mark.cross_platform
    def test_init_creates_directory_and_file(self, quality_tracker):
        """Test that initialization creates directory and files"""
        assert quality_tracker.tracker_dir.exists()
        assert quality_tracker.quality_file.exists()

        # Verify file contains empty array
        records = quality_tracker._read_quality_records()
        assert records == []

    @pytest.mark.unit
    def test_init_with_existing_file(self, existing_quality_file):
        """Test initialization with existing quality file"""
        temp_dir = existing_quality_file.parent
        tracker = QualityTracker(str(temp_dir))

        records = tracker._read_quality_records()
        assert len(records) == 2
        assert records[0]["task_id"] == "existing_task_001"

    @pytest.mark.unit
    def test_record_quality_valid_data(self, quality_tracker, sample_quality_record):
        """Test recording quality assessment with valid data"""
        success = quality_tracker.record_quality(
            sample_quality_record["task_id"],
            sample_quality_record["quality_score"],
            sample_quality_record["metrics"]
        )

        assert success is True

        # Verify record was stored
        records = quality_tracker._read_quality_records()
        assert len(records) == 1
        assert records[0]["task_id"] == sample_quality_record["task_id"]
        assert records[0]["quality_score"] == sample_quality_record["quality_score"]
        assert "timestamp" in records[0]

    @pytest.mark.unit
    def test_record_quality_validation_invalid_score(self, quality_tracker, sample_quality_record):
        """Test quality score validation"""
        # Test score > 1.0
        with pytest.raises(ValueError, match="quality_score must be a number between 0 and 1"):
            quality_tracker.record_quality(
                sample_quality_record["task_id"],
                1.5,  # Invalid score
                sample_quality_record["metrics"]
            )

        # Test score < 0
        with pytest.raises(ValueError, match="quality_score must be a number between 0 and 1"):
            quality_tracker.record_quality(
                sample_quality_record["task_id"],
                -0.1,  # Invalid score
                sample_quality_record["metrics"]
            )

    @pytest.mark.unit
    def test_record_quality_validation_invalid_metrics(self, quality_tracker, sample_quality_record):
        """Test metrics validation"""
        # Test metric value > 1.0
        invalid_metrics = sample_quality_record["metrics"].copy()
        invalid_metrics["code_quality"] = 1.5

        with pytest.raises(ValueError, match="Metric 'code_quality' must be a number between 0 and 1"):
            quality_tracker.record_quality(
                sample_quality_record["task_id"],
                sample_quality_record["quality_score"],
                invalid_metrics
            )

    @pytest.mark.unit
    def test_record_quality_backward_compatibility(self, quality_tracker):
        """Test backward compatibility method with different parameter names"""
        # Test with old parameter names
        success = quality_tracker.record_quality_score(
            task_type="legacy_task",
            score=85.0,  # 0-100 scale
            components={
                "code_quality": 90.0,
                "test_quality": 80.0
            }
        )

        assert success is True

        records = quality_tracker._read_quality_records()
        assert len(records) == 1

        # Should convert 0-100 scale to 0-1 scale
        record = records[0]
        assert record["task_id"] == "legacy_task"
        assert record["quality_score"] == 0.85  # 85/100
        assert record["metrics"]["code_quality"] == 0.90  # 90/100

    @pytest.mark.unit
    def test_get_quality_history(self, quality_tracker, sample_quality_record):
        """Test retrieving quality history"""
        # Record multiple quality assessments
        for i in range(5):
            record = sample_quality_record.copy()
            record["task_id"] = f"task_{i:03d}"
            record["quality_score"] = 0.8 + (i * 0.02)
            quality_tracker.record_quality(
                record["task_id"],
                record["quality_score"],
                record["metrics"]
            )

        # Test with default limit
        history = quality_tracker.get_quality_history()
        assert len(history) <= 10  # Default limit

        # Test with custom limit
        history = quality_tracker.get_quality_history(limit=3)
        assert len(history) == 3

        # Verify most recent first
        assert history[0]["score"] >= history[-1]["score"]

    @pytest.mark.unit
    def test_get_quality_trend_insufficient_data(self, quality_tracker):
        """Test trend calculation with insufficient data"""
        trend = quality_tracker.get_quality_trend()
        assert trend["direction"] == "stable"
        assert trend["average"] == 0.0
        assert trend["improvement"] == 0.0

    @pytest.mark.unit
    def test_get_quality_trend_with_data(self, quality_tracker, sample_quality_record):
        """Test trend calculation with sufficient data"""
        # Add quality data over time (simulating improvement)
        base_time = datetime.now() - timedelta(days=10)

        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = base_time

            # Record older assessments
            for i in range(5):
                record = sample_quality_record.copy()
                record["task_id"] = f"old_task_{i}"
                record["quality_score"] = 0.75 + (i * 0.01)  # Improving slowly
                quality_tracker.record_quality(
                    record["task_id"],
                    record["quality_score"],
                    record["metrics"]
                )

        # Record recent assessments with higher quality
        current_time = datetime.now()
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = current_time

            for i in range(5):
                record = sample_quality_record.copy()
                record["task_id"] = f"new_task_{i}"
                record["quality_score"] = 0.85 + (i * 0.01)  # Higher quality
                quality_tracker.record_quality(
                    record["task_id"],
                    record["quality_score"],
                    record["metrics"]
                )

        trend = quality_tracker.get_quality_trend()
        assert trend["direction"] == "improving"
        assert trend["average"] > 80  # Should be on 0-100 scale
        assert trend["improvement"] > 0

    @pytest.mark.unit
    def test_get_task_type_performance(self, quality_tracker, sample_quality_record):
        """Test performance analysis by task type"""
        # Record assessments for different task types
        task_data = [
            ("feature_implementation", [0.85, 0.90, 0.88]),
            ("bug_fix", [0.92, 0.89]),
            ("refactoring", [0.87])
        ]

        for task_type, scores in task_data:
            for score in scores:
                record = sample_quality_record.copy()
                record["task_id"] = f"{task_type}_{score}"
                record["quality_score"] = score
                quality_tracker.record_quality(
                    record["task_id"],
                    record["quality_score"],
                    record["metrics"]
                )

        performance = quality_tracker.get_task_type_performance()

        # Check calculations for each task type
        assert "feature_implementation" in performance
        assert performance["feature_implementation"]["count"] == 3
        assert abs(performance["feature_implementation"]["avg_score"] - ((0.85 + 0.90 + 0.88) / 3 * 100)) < 0.01

        assert "bug_fix" in performance
        assert performance["bug_fix"]["count"] == 2
        assert abs(performance["bug_fix"]["avg_score"] - ((0.92 + 0.89) / 2 * 100)) < 0.01

    @pytest.mark.unit
    def test_get_quality_trends_with_days_filter(self, quality_tracker, sample_quality_record):
        """Test trend analysis with time filtering"""
        # Record data across different time periods
        base_time = datetime.now() - timedelta(days=40)

        for i in range(20):
            record_time = base_time + timedelta(days=i * 2)
            with patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value = record_time

                record = sample_quality_record.copy()
                record["task_id"] = f"task_{i}"
                record["quality_score"] = 0.75 + (i * 0.01)
                quality_tracker.record_quality(
                    record["task_id"],
                    record["quality_score"],
                    record["metrics"]
                )

        # Test with 30-day filter
        trends = quality_tracker.get_quality_trends(days=30)
        assert trends["period_days"] == 30
        assert trends["data_points"] < 20  # Should be filtered by time

        # Test with specific metric
        code_quality_trends = quality_tracker.get_quality_trends(days=30, metric="code_quality")
        assert code_quality_trends["metric"] == "code_quality"

    @pytest.mark.unit
    def test_get_average_quality(self, quality_tracker, sample_quality_record):
        """Test average quality calculation"""
        # Record no data
        avg = quality_tracker.get_average_quality()
        assert avg == 0.0

        # Record some data
        scores = [0.85, 0.90, 0.88, 0.92]
        for i, score in enumerate(scores):
            record = sample_quality_record.copy()
            record["task_id"] = f"task_{i}"
            record["quality_score"] = score
            quality_tracker.record_quality(
                record["task_id"],
                record["quality_score"],
                record["metrics"]
            )

        avg = quality_tracker.get_average_quality()
        expected_avg = sum(scores) / len(scores)
        assert abs(avg - expected_avg) < 0.001

    @pytest.mark.unit
    def test_get_average_quality_with_days_filter(self, quality_tracker, sample_quality_record):
        """Test average quality with time filtering"""
        # Record recent and old data
        current_time = datetime.now()
        old_time = current_time - timedelta(days=40)

        # Old record
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = old_time
            record = sample_quality_record.copy()
            record["task_id"] = "old_task"
            record["quality_score"] = 0.95  # High quality
            quality_tracker.record_quality(
                record["task_id"],
                record["quality_score"],
                record["metrics"]
            )

        # Recent records
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = current_time
            for i in range(3):
                record = sample_quality_record.copy()
                record["task_id"] = f"recent_task_{i}"
                record["quality_score"] = 0.80  # Lower quality
                quality_tracker.record_quality(
                    record["task_id"],
                    record["quality_score"],
                    record["metrics"]
                )

        # Average without time filter should include old high-quality record
        avg_all = quality_tracker.get_average_quality()
        assert avg_all > 0.80

        # Average with 30-day filter should exclude old record
        avg_recent = quality_tracker.get_average_quality(days=30)
        assert abs(avg_recent - 0.80) < 0.001

    @pytest.mark.unit
    def test_get_metric_statistics(self, quality_tracker, sample_quality_record):
        """Test metric statistics calculation"""
        # Record data with varying metric values
        metric_data = [
            {"code_quality": 0.90, "test_quality": 0.85, "performance": 0.88},
            {"code_quality": 0.85, "test_quality": 0.90, "performance": 0.92},
            {"code_quality": 0.95, "test_quality": 0.80, "performance": 0.87}
        ]

        for i, metrics in enumerate(metric_data):
            record = sample_quality_record.copy()
            record["task_id"] = f"task_{i}"
            record["metrics"] = metrics
            record["quality_score"] = sum(metrics.values()) / len(metrics)
            quality_tracker.record_quality(
                record["task_id"],
                record["quality_score"],
                record["metrics"]
            )

        stats = quality_tracker.get_metric_statistics()

        # Check code_quality statistics
        code_quality_stats = stats["code_quality"]
        assert code_quality_stats["count"] == 3
        assert code_quality_stats["minimum"] == 0.85
        assert code_quality_stats["maximum"] == 0.95
        assert abs(code_quality_stats["average"] - ((0.90 + 0.85 + 0.95) / 3)) < 0.001

        # Check test_quality statistics
        test_quality_stats = stats["test_quality"]
        assert test_quality_stats["minimum"] == 0.80
        assert test_quality_stats["maximum"] == 0.90

    @pytest.mark.unit
    def test_get_recent_records(self, quality_tracker, sample_quality_record):
        """Test retrieving recent quality records"""
        # Record multiple assessments
        record_count = 15
        for i in range(record_count):
            record = sample_quality_record.copy()
            record["task_id"] = f"task_{i:03d}"
            record["quality_score"] = 0.8 + (i * 0.01)
            quality_tracker.record_quality(
                record["task_id"],
                record["quality_score"],
                record["metrics"]
            )

        # Test default limit (should be 10)
        recent = quality_tracker.get_recent_records()
        assert len(recent) == 10

        # Test custom limit
        recent = quality_tracker.get_recent_records(limit=5)
        assert len(recent) == 5

        # Test limit larger than available
        recent = quality_tracker.get_recent_records(limit=50)
        assert len(recent) == record_count

        # Verify most recent first
        timestamps = [r["timestamp"] for r in recent]
        assert timestamps == sorted(timestamps, reverse=True)

    @pytest.mark.unit
    def test_get_low_quality_tasks(self, quality_tracker, sample_quality_record):
        """Test retrieving low-quality tasks"""
        # Record tasks with varying quality levels
        quality_levels = [0.95, 0.92, 0.88, 0.75, 0.68, 0.85, 0.72]

        for i, quality in enumerate(quality_levels):
            record = sample_quality_record.copy()
            record["task_id"] = f"task_{i}"
            record["quality_score"] = quality
            quality_tracker.record_quality(
                record["task_id"],
                record["quality_score"],
                record["metrics"]
            )

        # Test with default threshold (0.7)
        low_quality = quality_tracker.get_low_quality_tasks()
        low_scores = [r["quality_score"] for r in low_quality]

        assert len(low_quality) == 2  # 0.68 and 0.72 (if threshold is 0.7, only 0.68)
        assert all(score < 0.7 for score in low_scores)

        # Test with custom threshold
        low_quality = quality_tracker.get_low_quality_tasks(threshold=0.80)
        low_scores = [r["quality_score"] for r in low_quality]

        assert len(low_quality) == 3  # 0.68, 0.72, 0.75
        assert all(score < 0.80 for score in low_scores)

        # Verify sorted by quality (lowest first)
        assert low_scores == sorted(low_scores)

    @pytest.mark.unit
    def test_empty_file_handling(self, quality_tracker):
        """Test handling of empty quality files"""
        # Create empty file
        with open(quality_tracker.quality_file, 'w') as f:
            f.write("")

        # Should handle empty file gracefully
        records = quality_tracker._read_quality_records()
        assert records == []

    @pytest.mark.unit
    def test_json_corruption_handling(self, quality_tracker):
        """Test handling of corrupted JSON files"""
        # Write corrupted JSON
        with open(quality_tracker.quality_file, 'w') as f:
            f.write("{ invalid json content")

        # Should handle corruption gracefully
        records = quality_tracker._read_quality_records()
        assert records == []

    @pytest.mark.unit
    @pytest.mark.parametrize("platform", ["Windows", "Linux", "Darwin"])
    def test_file_locking_cross_platform(self, quality_tracker, platform):
        """Test file locking mechanism across different platforms"""
        with patch('platform.system', return_value=platform):
            # Test reading with file lock
            records = quality_tracker._read_quality_records()
            assert isinstance(records, list)

            # Test writing with file lock
            quality_tracker._write_quality_records([])

    @pytest.mark.unit
    def test_error_handling_write_failure(self, quality_tracker, sample_quality_record):
        """Test error handling when write operations fail"""
        # Mock file open to raise error
        with patch('builtins.open', side_effect=IOError("Disk full")):
            with pytest.raises(Exception):
                quality_tracker._write_quality_records([sample_quality_record])

    @pytest.mark.unit
    def test_edge_case_metric_calculation(self, quality_tracker, sample_quality_record):
        """Test edge cases in metric calculations"""
        # Record a single assessment
        quality_tracker.record_quality(
            "single_task",
            0.85,
            {"single_metric": 0.90}
        )

        # Statistics should handle single data point
        stats = quality_tracker.get_metric_statistics()
        assert stats["single_metric"]["count"] == 1
        assert stats["single_metric"]["minimum"] == 0.90
        assert stats["single_metric"]["maximum"] == 0.90
        assert stats["single_metric"]["average"] == 0.90

    @pytest.mark.unit
    def test_timestamp_format_consistency(self, quality_tracker, sample_quality_record):
        """Test that timestamps are stored in consistent ISO format"""
        quality_tracker.record_quality(
            sample_quality_record["task_id"],
            sample_quality_record["quality_score"],
            sample_quality_record["metrics"]
        )

        records = quality_tracker._read_quality_records()
        timestamp = records[0]["timestamp"]

        # Should be parseable ISO format
        parsed_time = datetime.fromisoformat(timestamp)
        assert isinstance(parsed_time, datetime)

    @pytest.mark.unit
    def test_large_dataset_performance(self, quality_tracker, sample_quality_record):
        """Test performance with large datasets"""
        import time

        # Record many assessments
        start_time = time.time()
        for i in range(1000):
            record = sample_quality_record.copy()
            record["task_id"] = f"perf_test_{i}"
            record["quality_score"] = 0.5 + (i % 50) / 100.0
            quality_tracker.record_quality(
                record["task_id"],
                record["quality_score"],
                record["metrics"]
            )
        record_time = time.time() - start_time

        # Should complete within reasonable time (< 5 seconds for 1000 records)
        assert record_time < 5.0

        # Test reading performance
        start_time = time.time()
        stats = quality_tracker.get_metric_statistics()
        stats_time = time.time() - start_time

        # Statistics calculation should be fast
        assert stats_time < 1.0
        assert len(stats) > 0