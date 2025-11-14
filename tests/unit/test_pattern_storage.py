"""
Unit tests for Pattern Storage System

Tests the core pattern learning functionality including:
- Pattern storage and retrieval
- JSON file handling with cross-platform compatibility
- File locking mechanisms
- Pattern validation and statistics
"""

import pytest
import json
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import sys

# Add lib directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from pattern_storage import PatternStorage


class TestPatternStorage:
    """Test suite for PatternStorage class"""

    @pytest.fixture
    def pattern_storage(self, temp_directory):
        """Create a PatternStorage instance with temporary directory"""
        return PatternStorage(temp_directory)

    @pytest.fixture
    def valid_pattern(self, sample_pattern_data):
        """Valid pattern data for testing"""
        return sample_pattern_data.copy()

    @pytest.fixture
    def existing_patterns_file(self, temp_directory):
        """Create an existing patterns.json file with test data"""
        patterns_file = Path(temp_directory) / "patterns.json"
        test_data = [
            {
                "pattern_id": "test_pattern_001",
                "task_type": "feature_implementation",
                "context": "Test feature",
                "skills_used": ["testing"],
                "approach": "Test approach",
                "quality_score": 0.85,
                "timestamp": "2025-01-01T00:00:00",
                "usage_count": 5,
                "success_rate": 0.9
            }
        ]
        with open(patterns_file, 'w') as f:
            json.dump(test_data, f)
        return patterns_file

    @pytest.mark.unit
    @pytest.mark.cross_platform
    def test_init_creates_directory_and_file(self, pattern_storage):
        """Test that initialization creates directory and files"""
        assert pattern_storage.patterns_dir.exists()
        assert pattern_storage.patterns_file.exists()

        # Verify file contains empty array
        with open(pattern_storage.patterns_file, 'r') as f:
            data = json.load(f)
            assert data == []

    @pytest.mark.unit
    def test_init_with_existing_file(self, existing_patterns_file):
        """Test initialization with existing patterns file"""
        temp_dir = existing_patterns_file.parent
        storage = PatternStorage(str(temp_dir))

        patterns = storage._read_patterns()
        assert len(patterns) == 1
        assert patterns[0]["pattern_id"] == "test_pattern_001"

    @pytest.mark.unit
    def test_store_pattern_valid_data(self, pattern_storage, valid_pattern):
        """Test storing a valid pattern"""
        pattern_id = pattern_storage.store_pattern(valid_pattern)

        assert pattern_id is not None
        assert pattern_id.startswith("pattern_")

        # Verify pattern was stored
        patterns = pattern_storage._read_patterns()
        assert len(patterns) == 1
        assert patterns[0]["pattern_id"] == pattern_id
        assert patterns[0]["task_type"] == valid_pattern["task_type"]

    @pytest.mark.unit
    def test_store_pattern_adds_metadata(self, pattern_storage, valid_pattern):
        """Test that store_pattern adds required metadata"""
        pattern_id = pattern_storage.store_pattern(valid_pattern)

        patterns = pattern_storage._read_patterns()
        stored_pattern = patterns[0]

        # Check auto-generated fields
        assert "pattern_id" in stored_pattern
        assert "timestamp" in stored_pattern
        assert "usage_count" in stored_pattern
        assert "success_rate" in stored_pattern

        assert stored_pattern["usage_count"] == 0
        assert stored_pattern["success_rate"] == 1.0  # High quality pattern

    @pytest.mark.unit
    def test_store_pattern_validation_missing_fields(self, pattern_storage):
        """Test pattern validation with missing required fields"""
        invalid_pattern = {
            "task_type": "feature_implementation",
            # Missing required fields: context, skills_used, approach, quality_score
        }

        with pytest.raises(ValueError, match="Missing required fields"):
            pattern_storage.store_pattern(invalid_pattern)

    @pytest.mark.unit
    def test_store_pattern_invalid_task_type(self, pattern_storage, valid_pattern):
        """Test pattern validation with invalid task type"""
        valid_pattern["task_type"] = "invalid_task_type"

        with pytest.raises(ValueError, match="Invalid task_type"):
            pattern_storage.store_pattern(valid_pattern)

    @pytest.mark.unit
    def test_store_pattern_invalid_quality_score(self, pattern_storage, valid_pattern):
        """Test pattern validation with invalid quality score"""
        valid_pattern["quality_score"] = 1.5  # Above 1.0

        with pytest.raises(ValueError, match="quality_score must be a number between 0 and 1"):
            pattern_storage.store_pattern(valid_pattern)

    @pytest.mark.unit
    def test_retrieve_patterns_basic(self, pattern_storage, valid_pattern):
        """Test basic pattern retrieval"""
        # Store a pattern first
        pattern_storage.store_pattern(valid_pattern)

        # Retrieve with context search
        results = pattern_storage.retrieve_patterns("authentication")

        assert len(results) == 1
        assert results[0]["task_type"] == valid_pattern["task_type"]

    @pytest.mark.unit
    def test_retrieve_patterns_with_filters(self, pattern_storage, valid_pattern):
        """Test pattern retrieval with filters"""
        # Store patterns with different quality scores
        high_quality = valid_pattern.copy()
        high_quality["quality_score"] = 0.9
        high_quality["context"] = "High quality implementation"

        low_quality = valid_pattern.copy()
        low_quality["quality_score"] = 0.6
        low_quality["context"] = "Low quality implementation"
        low_quality["task_type"] = "bug_fix"

        pattern_storage.store_pattern(high_quality)
        pattern_storage.store_pattern(low_quality)

        # Test quality filter
        results = pattern_storage.retrieve_patterns("implementation", min_quality=0.8)
        assert len(results) == 1
        assert results[0]["quality_score"] == 0.9

        # Test task type filter
        results = pattern_storage.retrieve_patterns("implementation", task_type="bug_fix")
        assert len(results) == 1
        assert results[0]["task_type"] == "bug_fix"

    @pytest.mark.unit
    def test_retrieve_patterns_relevance_scoring(self, pattern_storage):
        """Test that patterns are scored by relevance"""
        # Store patterns with different contexts
        pattern1 = {
            "task_type": "feature_implementation",
            "context": "User authentication with JWT tokens",
            "skills_used": ["security"],
            "approach": "JWT implementation",
            "quality_score": 0.8
        }

        pattern2 = {
            "task_type": "feature_implementation",
            "context": "Database connection management",
            "skills_used": ["database"],
            "approach": "Connection pooling",
            "quality_score": 0.9
        }

        pattern_storage.store_pattern(pattern1)
        pattern_storage.store_pattern(pattern2)

        # Search for "authentication" - should match pattern1 first
        results = pattern_storage.retrieve_patterns("authentication")
        assert len(results) == 1
        assert "authentication" in results[0]["context"].lower()

    @pytest.mark.unit
    def test_update_usage_statistics(self, pattern_storage, valid_pattern):
        """Test updating pattern usage statistics"""
        pattern_id = pattern_storage.store_pattern(valid_pattern)

        # Update with successful usage
        success = pattern_storage.update_usage(pattern_id, success=True)
        assert success is True

        patterns = pattern_storage._read_patterns()
        updated_pattern = next(p for p in patterns if p["pattern_id"] == pattern_id)

        assert updated_pattern["usage_count"] == 1
        assert updated_pattern["success_rate"] == 1.0
        assert "last_used" in updated_pattern

    @pytest.mark.unit
    def test_update_usage_nonexistent_pattern(self, pattern_storage):
        """Test updating usage for non-existent pattern"""
        success = pattern_storage.update_usage("nonexistent_pattern", success=True)
        assert success is False

    @pytest.mark.unit
    def test_get_skill_effectiveness(self, pattern_storage):
        """Test calculating skill effectiveness statistics"""
        # Store patterns with different skills and outcomes
        pattern1 = {
            "task_type": "feature_implementation",
            "context": "Test pattern 1",
            "skills_used": ["code-analysis", "testing"],
            "approach": "Approach 1",
            "quality_score": 0.9  # Success
        }

        pattern2 = {
            "task_type": "bug_fix",
            "context": "Test pattern 2",
            "skills_used": ["code-analysis", "debugging"],
            "approach": "Approach 2",
            "quality_score": 0.5  # Failure
        }

        pattern3 = {
            "task_type": "refactoring",
            "context": "Test pattern 3",
            "skills_used": ["testing"],
            "approach": "Approach 3",
            "quality_score": 0.8  # Success
        }

        pattern_storage.store_pattern(pattern1)
        pattern_storage.store_pattern(pattern2)
        pattern_storage.store_pattern(pattern3)

        # Test skill effectiveness
        code_analysis_stats = pattern_storage.get_skill_effectiveness("code-analysis")
        assert code_analysis_stats["skill"] == "code-analysis"
        assert code_analysis_stats["usage_count"] == 2
        assert code_analysis_stats["success_rate"] == 0.5  # 1 success out of 2 uses
        assert code_analysis_stats["avg_quality"] == 0.7  # (0.9 + 0.5) / 2

        testing_stats = pattern_storage.get_skill_effectiveness("testing")
        assert testing_stats["usage_count"] == 2
        assert testing_stats["success_rate"] == 1.0  # Both uses successful

    @pytest.mark.unit
    def test_get_skill_effectiveness_unused_skill(self, pattern_storage):
        """Test skill effectiveness for unused skill"""
        stats = pattern_storage.get_skill_effectiveness("unused_skill")
        assert stats["usage_count"] == 0
        assert stats["success_rate"] == 0.0
        assert stats["avg_quality"] == 0.0

    @pytest.mark.unit
    def test_get_statistics_empty_database(self, pattern_storage):
        """Test statistics calculation with empty database"""
        stats = pattern_storage.get_statistics()
        assert stats["total_patterns"] == 0
        assert stats["average_quality"] == 0.0
        assert stats["task_type_distribution"] == {}
        assert stats["most_used_skills"] == {}

    @pytest.mark.unit
    def test_get_statistics_with_data(self, pattern_storage):
        """Test statistics calculation with pattern data"""
        # Add test patterns
        for i in range(3):
            pattern = {
                "task_type": f"task_type_{i % 2}",  # Alternating task types
                "context": f"Test pattern {i}",
                "skills_used": [f"skill_{j}" for j in range(i + 1)],  # Increasing skills
                "approach": f"Approach {i}",
                "quality_score": 0.7 + (i * 0.1)  # Increasing quality
            }
            pattern_storage.store_pattern(pattern)

        stats = pattern_storage.get_statistics()
        assert stats["total_patterns"] == 3
        assert 0.7 <= stats["average_quality"] <= 0.9
        assert len(stats["task_type_distribution"]) == 2
        assert len(stats["most_used_skills"]) > 0

    @pytest.mark.unit
    @pytest.mark.parametrize("platform", ["Windows", "Linux", "Darwin"])
    def test_file_locking_cross_platform(self, pattern_storage, platform, mock_file_lock):
        """Test file locking mechanism across different platforms"""
        with patch('platform.system', return_value=platform):
            # Test reading with file lock
            patterns = pattern_storage._read_patterns()
            assert isinstance(patterns, list)

            # Test writing with file lock
            pattern_storage._write_patterns([])

    @pytest.mark.unit
    def test_json_corruption_handling(self, pattern_storage):
        """Test handling of corrupted JSON files"""
        # Write corrupted JSON
        with open(pattern_storage.patterns_file, 'w') as f:
            f.write("{ invalid json content")

        # Should handle corruption gracefully
        patterns = pattern_storage._read_patterns()
        assert patterns == []

    @pytest.mark.unit
    def test_backward_compatibility_patterns_array(self, pattern_storage, temp_directory):
        """Test backward compatibility with simple array format"""
        # Create patterns file in old format (simple array)
        old_format_data = [
            {"id": 1, "pattern": "test"},
            {"id": 2, "pattern": "test2"}
        ]

        with open(pattern_storage.patterns_file, 'w') as f:
            json.dump(old_format_data, f)

        # Should read old format correctly
        patterns = pattern_storage._read_patterns()
        assert len(patterns) == 2
        assert patterns[0]["id"] == 1

    @pytest.mark.unit
    def test_backward_compatibility_patterns_object(self, pattern_storage, temp_directory):
        """Test backward compatibility with object format containing patterns array"""
        # Create patterns file in object format
        object_format_data = {
            "patterns": [
                {"id": 1, "pattern": "test"},
                {"id": 2, "pattern": "test2"}
            ],
            "metadata": {"version": "1.0"}
        }

        with open(pattern_storage.patterns_file, 'w') as f:
            json.dump(object_format_data, f)

        # Should read patterns from object format
        patterns = pattern_storage._read_patterns()
        assert len(patterns) == 2
        assert patterns[0]["id"] == 1

    @pytest.mark.unit
    def test_unified_data_consolidation(self, pattern_storage):
        """Test data consolidation into unified format"""
        # Store a pattern first
        pattern = {
            "task_type": "feature_implementation",
            "context": "Test consolidation",
            "skills_used": ["testing"],
            "approach": "Test approach",
            "quality_score": 0.85
        }
        pattern_storage.store_pattern(pattern)

        # Test consolidation
        success = pattern_storage.consolidate_all_data()
        assert success is True

        # Check unified file was created
        unified_file = pattern_storage.patterns_dir / "unified_data.json"
        assert unified_file.exists()

        # Verify content
        with open(unified_file, 'r') as f:
            unified_data = json.load(f)

        assert "patterns" in unified_data
        assert "skill_metrics" in unified_data
        assert "system_health" in unified_data
        assert len(unified_data["patterns"]) == 1

    @pytest.mark.unit
    def test_error_handling_file_permissions(self, pattern_storage):
        """Test error handling when file operations fail"""
        # Mock file open to raise permission error
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            with pytest.raises(Exception):
                pattern_storage._read_patterns()

    @pytest.mark.unit
    def test_pattern_id_generation(self, pattern_storage, valid_pattern):
        """Test that pattern IDs are generated correctly"""
        # Remove pattern_id if present
        if "pattern_id" in valid_pattern:
            del valid_pattern["pattern_id"]

        pattern_id = pattern_storage.store_pattern(valid_pattern)

        # Should generate timestamp-based ID
        assert pattern_id.startswith("pattern_")
        assert len(pattern_id) > len("pattern_")  # Has timestamp suffix

    @pytest.mark.unit
    def test_custom_pattern_id_preservation(self, pattern_storage, valid_pattern):
        """Test that custom pattern IDs are preserved"""
        custom_id = "custom_pattern_123"
        valid_pattern["pattern_id"] = custom_id

        returned_id = pattern_storage.store_pattern(valid_pattern)

        # Should return and preserve the custom ID
        assert returned_id == custom_id

        patterns = pattern_storage._read_patterns()
        stored_pattern = next(p for p in patterns if p["pattern_id"] == custom_id)
        assert stored_pattern["pattern_id"] == custom_id