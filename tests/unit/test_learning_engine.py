"""
Unit tests for Learning Engine

Tests the learning engine functionality including:
- Learning system initialization
- Pattern capture and storage
- Quality assessment tracking
- Status reporting and analytics
- Cross-platform file operations
"""

import pytest
import json
import tempfile
import shutil
import os
import sys
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta

# Add lib directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from learning_engine import LearningEngine


class TestLearningEngine:
    """Test suite for LearningEngine class"""

    @pytest.fixture
    def learning_engine(self, temp_directory):
        """Create a LearningEngine instance with temporary directory"""
        return LearningEngine(temp_directory)

    @pytest.fixture
    def sample_project_context(self):
        """Sample project context for testing"""
        return {
            "type": "web_application",
            "frameworks": ["fastapi", "react"],
            "detected_languages": ["python", "javascript", "typescript"],
            "project_size": "medium",
            "complexity": "high"
        }

    @pytest.fixture
    def sample_pattern_data(self):
        """Sample pattern data for testing"""
        return {
            "task_type": "feature_implementation",
            "context": "User authentication system",
            "approach": "JWT-based authentication with refresh tokens",
            "skills_used": ["security-audit", "code-analysis", "testing"],
            "quality_score": 0.92,
            "execution_time_seconds": 180,
            "agents_involved": ["code-analyzer", "quality-controller"]
        }

    @pytest.fixture
    def sample_quality_data(self):
        """Sample quality assessment data"""
        return {
            "task_id": "auth_implementation_001",
            "quality_score": 0.88,
            "metrics": {
                "code_quality": 0.90,
                "test_quality": 0.85,
                "documentation": 0.80,
                "patterns": 0.95,
                "security": 0.92
            },
            "assessment_type": "comprehensive",
            "agent": "quality-controller"
        }

    @pytest.fixture
    def existing_learning_system(self, temp_directory):
        """Create an existing learning system with data"""
        # Create patterns.json with existing data
        patterns_file = Path(temp_directory) / "patterns.json"
        existing_data = {
            "project_context": {
                "type": "existing_project",
                "frameworks": ["django"]
            },
            "patterns": [
                {
                    "id": 1,
                    "timestamp": "2025-01-01T10:00:00",
                    "pattern": {
                        "task_type": "bug_fix",
                        "quality_score": 0.85
                    },
                    "captured_by": "learning_engine",
                    "processed": True
                }
            ],
            "skill_effectiveness": {
                "code-analysis": {"success_rate": 0.9}
            },
            "learning_metrics": {
                "total_patterns": 1,
                "last_updated": "2025-01-01T10:00:00"
            }
        }
        with open(patterns_file, 'w') as f:
            json.dump(existing_data, f)

        return temp_directory

    @pytest.mark.unit
    @pytest.mark.cross_platform
    def test_init_creates_directory_structure(self, learning_engine):
        """Test that initialization creates required directory and files"""
        assert learning_engine.data_dir.exists()

        # Check all required files are created
        assert learning_engine.patterns_file.exists()
        assert learning_engine.quality_history_file.exists()
        assert learning_engine.task_queue_file.exists()
        assert learning_engine.config_file.exists()

        # Verify initial content
        with open(learning_engine.patterns_file, 'r') as f:
            patterns_data = json.load(f)
            assert "project_context" in patterns_data
            assert "patterns" in patterns_data
            assert "skill_effectiveness" in patterns_data
            assert "learning_metrics" in patterns_data

    @pytest.mark.unit
    def test_initialize_learning_system_new_system(self, learning_engine, sample_project_context):
        """Test learning system initialization for new system"""
        # Remove existing files to simulate new system
        for file_path in learning_engine.data_dir.glob("*.json"):
            file_path.unlink()

        result = learning_engine.initialize_learning_system(sample_project_context)

        assert result["status"] == "initialized"
        assert "timestamp" in result
        assert result["project_context"] == sample_project_context
        assert len(result["files_created"]) == 4  # patterns, quality, task_queue, config

        # Verify files were created with correct content
        with open(learning_engine.patterns_file, 'r') as f:
            patterns_data = json.load(f)
            assert patterns_data["project_context"] == sample_project_context
            assert patterns_data["patterns"] == []

        with open(learning_engine.config_file, 'r') as f:
            config_data = json.load(f)
            assert config_data["auto_capture"] is True
            assert config_data["learning_enabled"] is True

    @pytest.mark.unit
    def test_initialize_learning_system_existing_system(self, learning_engine, sample_project_context):
        """Test learning system initialization with existing data"""
        # Initialize once
        learning_engine.initialize_learning_system(sample_project_context)

        # Initialize again - should not overwrite existing data
        result = learning_engine.initialize_learning_system(sample_project_context)

        assert result["status"] == "initialized"
        # Files should not be created again
        assert len(result["files_created"]) == 0

    @pytest.mark.unit
    def test_initialize_learning_system_default_context(self, learning_engine):
        """Test initialization with default project context"""
        result = learning_engine.initialize_learning_system()

        assert result["status"] == "initialized"
        assert result["project_context"]["type"] == "unknown"
        assert result["project_context"]["frameworks"] == []
        assert "detected_at" in result["project_context"]

    @pytest.mark.unit
    def test_capture_pattern_success(self, learning_engine, sample_pattern_data):
        """Test successful pattern capture"""
        # Initialize system first
        learning_engine.initialize_learning_system()

        result = learning_engine.capture_pattern(sample_pattern_data)

        assert result["status"] == "success"
        assert "pattern_id" in result
        assert result["total_patterns"] == 1
        assert result["message"] == "Pattern captured successfully"

        # Verify pattern was stored correctly
        with open(learning_engine.patterns_file, 'r') as f:
            patterns_data = json.load(f)
            assert len(patterns_data["patterns"]) == 1

            stored_pattern = patterns_data["patterns"][0]
            assert stored_pattern["id"] == 1
            assert stored_pattern["pattern"] == sample_pattern_data
            assert stored_pattern["captured_by"] == "learning_engine"
            assert stored_pattern["processed"] is True
            assert "timestamp" in stored_pattern

    @pytest.mark.unit
    def test_capture_pattern_with_existing_patterns(self, learning_engine, sample_pattern_data):
        """Test pattern capture with existing patterns"""
        # Initialize and add existing pattern
        learning_engine.initialize_learning_system()

        # Add pattern directly to file to simulate existing data
        with open(learning_engine.patterns_file, 'r') as f:
            data = json.load(f)

        existing_pattern = {
            "id": 1,
            "timestamp": "2025-01-01T10:00:00",
            "pattern": {"task_type": "existing"},
            "captured_by": "learning_engine",
            "processed": True
        }
        data["patterns"].append(existing_pattern)
        data["learning_metrics"]["total_patterns"] = 1

        with open(learning_engine.patterns_file, 'w') as f:
            json.dump(data, f)

        # Capture new pattern
        result = learning_engine.capture_pattern(sample_pattern_data)

        assert result["status"] == "success"
        assert result["pattern_id"] == 2  # Should increment ID
        assert result["total_patterns"] == 2

    @pytest.mark.unit
    def test_capture_pattern_file_not_exists(self, learning_engine, sample_pattern_data):
        """Test pattern capture when patterns file doesn't exist"""
        # Remove patterns file
        learning_engine.patterns_file.unlink()

        result = learning_engine.capture_pattern(sample_pattern_data)

        assert result["status"] == "success"
        # Should create new structure and add pattern
        assert result["pattern_id"] == 1

    @pytest.mark.unit
    def test_capture_pattern_error_handling(self, learning_engine, sample_pattern_data):
        """Test error handling during pattern capture"""
        # Mock file operation to raise error
        with patch('builtins.open', side_effect=IOError("Disk full")):
            result = learning_engine.capture_pattern(sample_pattern_data)

        assert result["status"] == "error"
        assert result["message"] == "Failed to capture pattern"
        assert "error" in result

    @pytest.mark.unit
    def test_get_status_comprehensive(self, learning_engine, sample_project_context, sample_pattern_data):
        """Test comprehensive status reporting"""
        # Initialize system with data
        learning_engine.initialize_learning_system(sample_project_context)
        learning_engine.capture_pattern(sample_pattern_data)

        # Add quality history
        quality_data = {
            "task_id": "test_task",
            "quality_score": 0.85,
            "metrics": {"code_quality": 0.90}
        }
        learning_engine.add_quality_assessment(quality_data)

        status = learning_engine.get_status()

        assert status["timestamp"] is not None
        assert status["data_directory"] == str(learning_engine.data_dir)
        assert status["system_status"] == "operational"

        # Check file status
        files = status["files"]
        assert files["patterns.json"] is True
        assert files["quality_history.json"] is True
        assert files["task_queue.json"] is True
        assert files["config.json"] is True

        # Check analytics
        analytics = status["analytics"]
        assert analytics["total_patterns"] == 1
        assert analytics["project_context"] == sample_project_context
        assert analytics["quality_assessments"] == 1
        assert analytics["latest_quality_score"] == 0.85

    @pytest.mark.unit
    def test_get_status_empty_system(self, learning_engine):
        """Test status reporting for empty system"""
        status = learning_engine.get_status()

        assert status["system_status"] == "operational"
        assert status["analytics"]["total_patterns"] == 0
        assert "quality_assessments" not in status["analytics"]

    @pytest.mark.unit
    def test_get_status_file_missing(self, learning_engine):
        """Test status reporting when some files are missing"""
        # Remove patterns file
        learning_engine.patterns_file.unlink()

        status = learning_engine.get_status()

        assert status["files"]["patterns.json"] is False
        assert status["analytics"]["total_patterns"] == 0

    @pytest.mark.unit
    def test_add_quality_assessment_success(self, learning_engine, sample_quality_data):
        """Test successful quality assessment addition"""
        result = learning_engine.add_quality_assessment(sample_quality_data)

        assert result["status"] == "success"
        assert result["total_assessments"] == 1
        assert result["latest_score"] == sample_quality_data["quality_score"]

        # Verify assessment was stored
        with open(learning_engine.quality_history_file, 'r') as f:
            history = json.load(f)
            assert len(history) == 1

            assessment = history[0]
            assert assessment["task_id"] == sample_quality_data["task_id"]
            assert assessment["quality_score"] == sample_quality_data["quality_score"]
            assert "timestamp" in assessment

    @pytest.mark.unit
    def test_add_quality_assessment_existing_history(self, learning_engine, sample_quality_data):
        """Test adding quality assessment to existing history"""
        # Create existing history
        existing_history = [
            {
                "task_id": "existing_task",
                "quality_score": 0.80,
                "timestamp": "2025-01-01T10:00:00"
            }
        ]
        with open(learning_engine.quality_history_file, 'w') as f:
            json.dump(existing_history, f)

        result = learning_engine.add_quality_assessment(sample_quality_data)

        assert result["status"] == "success"
        assert result["total_assessments"] == 2

        # Verify both assessments exist
        with open(learning_engine.quality_history_file, 'r') as f:
            history = json.load(f)
            assert len(history) == 2

    @pytest.mark.unit
    def test_add_quality_assessment_error_handling(self, learning_engine, sample_quality_data):
        """Test error handling during quality assessment addition"""
        # Mock file operation to raise error
        with patch('builtins.open', side_effect=IOError("Permission denied")):
            result = learning_engine.add_quality_assessment(sample_quality_data)

        assert result["status"] == "error"
        assert result["message"] == "Failed to add quality assessment"

    @pytest.mark.unit
    def test_learning_metrics_update(self, learning_engine, sample_pattern_data):
        """Test that learning metrics are updated correctly"""
        learning_engine.initialize_learning_system()

        # Capture multiple patterns
        for i in range(3):
            pattern = sample_pattern_data.copy()
            pattern["task_id"] = f"task_{i}"
            learning_engine.capture_pattern(pattern)

        # Check metrics
        with open(learning_engine.patterns_file, 'r') as f:
            data = json.load(f)
            metrics = data["learning_metrics"]

            assert metrics["total_patterns"] == 3
            assert "last_updated" in metrics

    @pytest.mark.unit
    def test_cross_platform_file_paths(self, learning_engine, cross_platform_temp_dir):
        """Test cross-platform file path handling"""
        temp_dir, platform_info = cross_platform_temp_dir
        engine = LearningEngine(temp_dir)

        # Test initialization with cross-platform paths
        engine.initialize_learning_system()

        # Verify all files exist with platform-specific paths
        for file_name in ["patterns.json", "quality_history.json", "task_queue.json", "config.json"]:
            file_path = Path(temp_dir) / file_name
            assert file_path.exists()

        # Test pattern capture with cross-platform paths
        pattern_data = {"task_type": "test"}
        result = engine.capture_pattern(pattern_data)
        assert result["status"] == "success"

    @pytest.mark.unit
    def test_json_serialization_edge_cases(self, learning_engine):
        """Test JSON serialization with edge cases"""
        learning_engine.initialize_learning_system()

        # Pattern with special characters and unicode
        complex_pattern = {
            "task_type": "special_characters",
            "description": "Test with émojis 🚀 and spëcial chars",
            "unicode_data": {"测试": "中文", "русский": "текст"},
            "nested_data": {"deep": {"deeper": {"value": None}}},
            "array_data": [1, "string", 3.14, True, None],
            "boolean_data": True
        }

        result = learning_engine.capture_pattern(complex_pattern)
        assert result["status"] == "success"

        # Verify data integrity
        with open(learning_engine.patterns_file, 'r') as f:
            data = json.load(f)
            stored_pattern = data["patterns"][0]["pattern"]
            assert stored_pattern["description"] == complex_pattern["description"]
            assert stored_pattern["unicode_data"] == complex_pattern["unicode_data"]

    @pytest.mark.unit
    def test_concurrent_access_simulation(self, learning_engine, sample_pattern_data):
        """Test simulated concurrent access scenarios"""
        learning_engine.initialize_learning_system()

        # Simulate multiple rapid captures
        results = []
        for i in range(10):
            pattern = sample_pattern_data.copy()
            pattern["task_id"] = f"concurrent_task_{i}"
            result = learning_engine.capture_pattern(pattern)
            results.append(result)

        # All should succeed
        for result in results:
            assert result["status"] == "success"

        # Verify all patterns stored
        with open(learning_engine.patterns_file, 'r') as f:
            data = json.load(f)
            assert len(data["patterns"]) == 10

        # Verify pattern IDs are sequential
        pattern_ids = [p["id"] for p in data["patterns"]]
        assert pattern_ids == list(range(1, 11))

    @pytest.mark.unit
    def test_large_pattern_data(self, learning_engine):
        """Test handling of large pattern data"""
        learning_engine.initialize_learning_system()

        # Create large pattern data
        large_pattern = {
            "task_type": "large_data_test",
            "large_array": list(range(1000)),
            "large_string": "x" * 10000,
            "nested_structure": {}
        }

        # Create deeply nested structure
        current = large_pattern["nested_structure"]
        for i in range(100):
            current[f"level_{i}"] = {}
            current = current[f"level_{i}"]
        current["final_value"] = "deep_value"

        result = learning_engine.capture_pattern(large_pattern)
        assert result["status"] == "success"

        # Verify large data was stored correctly
        with open(learning_engine.patterns_file, 'r') as f:
            data = json.load(f)
            stored_pattern = data["patterns"][0]["pattern"]
            assert len(stored_pattern["large_array"]) == 1000
            assert len(stored_pattern["large_string"]) == 10000

            # Navigate the nested structure to find the final value
            current = stored_pattern["nested_structure"]
            for i in range(100):
                current = current[f"level_{i}"]
            assert current["final_value"] == "deep_value"

    @pytest.mark.unit
    def test_data_integrity_validation(self, learning_engine, sample_pattern_data):
        """Test data integrity and validation"""
        learning_engine.initialize_learning_system()

        # Capture pattern
        result = learning_engine.capture_pattern(sample_pattern_data)
        assert result["status"] == "success"

        # Verify file is valid JSON
        with open(learning_engine.patterns_file, 'r') as f:
            try:
                data = json.load(f)
                assert isinstance(data, dict)
                assert "patterns" in data
                assert isinstance(data["patterns"], list)
            except json.JSONDecodeError:
                pytest.fail("File contains invalid JSON")

        # Verify required fields exist
        pattern = data["patterns"][0]
        required_fields = ["id", "timestamp", "pattern", "captured_by", "processed"]
        for field in required_fields:
            assert field in pattern

    @pytest.mark.unit
    def test_performance_benchmark(self, learning_engine):
        """Test performance with reasonable data volumes"""
        import time

        learning_engine.initialize_learning_system()

        # Benchmark pattern capture performance
        start_time = time.time()
        pattern_count = 100

        for i in range(pattern_count):
            pattern = {
                "task_id": f"perf_test_{i}",
                "quality_score": 0.5 + (i % 50) / 100.0,
                "data": "x" * 100  # 100 bytes per pattern
            }
            learning_engine.capture_pattern(pattern)

        capture_time = time.time() - start_time

        # Should complete within reasonable time (< 2 seconds for 100 patterns)
        assert capture_time < 2.0

        # Benchmark status retrieval
        start_time = time.time()
        status = learning_engine.get_status()
        status_time = time.time() - start_time

        # Status should be fast (< 0.1 seconds)
        assert status_time < 0.1
        assert status["analytics"]["total_patterns"] == pattern_count

    @pytest.mark.unit
    def test_error_recovery_corrupted_file(self, learning_engine, sample_pattern_data):
        """Test recovery from corrupted data files"""
        learning_engine.initialize_learning_system()

        # Corrupt the patterns file
        with open(learning_engine.patterns_file, 'w') as f:
            f.write("{ invalid json content")

        # Should handle corruption gracefully
        result = learning_engine.capture_pattern(sample_pattern_data)

        # The implementation should recover and create new file
        assert result["status"] == "success"

        # Verify file is now valid
        with open(learning_engine.patterns_file, 'r') as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert "patterns" in data