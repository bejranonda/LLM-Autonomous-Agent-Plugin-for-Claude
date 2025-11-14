#!/usr/bin/env python3
"""
Test suite for adaptive_quality_thresholds.py
Boosts test coverage by focusing on core threshold calculation logic.
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

# Add the lib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from adaptive_quality_thresholds import (
    AdaptiveQualityThresholds,
    TaskType,
    ProjectPhase
)


class TestAdaptiveQualityThresholds:
    """Test cases for AdaptiveQualityThresholds class."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.thresholds = AdaptiveQualityThresholds(self.temp_dir)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test AdaptiveQualityThresholds initialization."""
        # Test with default directory
        thresholds = AdaptiveQualityThresholds()
        assert thresholds.storage_dir.exists()

        # Test with custom directory
        custom_dir = Path(self.temp_dir) / "custom"
        thresholds = AdaptiveQualityThresholds(str(custom_dir))
        assert custom_dir.exists()
        assert thresholds.history_file.exists()

    def test_get_threshold_basic(self):
        """Test basic threshold calculation."""
        # Test security task (should be high)
        threshold = self.thresholds.get_threshold("security")
        assert threshold >= 90

        # Test documentation task (should be lower)
        threshold = self.thresholds.get_threshold("documentation")
        assert threshold >= 70

        # Test exploratory task (should be lowest)
        threshold = self.thresholds.get_threshold("exploratory")
        assert threshold >= 60

    def test_get_threshold_with_phase(self):
        """Test threshold calculation with project phase."""
        base_threshold = self.thresholds.get_threshold("feature")

        # Pre-release should increase threshold
        pre_release_threshold = self.thresholds.get_threshold("feature", "pre-release")
        assert pre_release_threshold > base_threshold

        # Exploration should decrease threshold
        exploration_threshold = self.thresholds.get_threshold("feature", "exploration")
        assert exploration_threshold < base_threshold

    def test_get_threshold_with_criticality(self):
        """Test threshold calculation with criticality levels."""
        base_threshold = self.thresholds.get_threshold("feature")

        # Critical should increase threshold
        critical_threshold = self.thresholds.get_threshold("feature", criticality="critical")
        assert critical_threshold > base_threshold

        # Low should decrease threshold
        low_threshold = self.thresholds.get_threshold("feature", criticality="low")
        assert low_threshold < base_threshold

    def test_get_threshold_user_facing(self):
        """Test threshold calculation for user-facing code."""
        base_threshold = self.thresholds.get_threshold("feature")
        user_facing_threshold = self.thresholds.get_threshold("feature", is_user_facing=True)

        assert user_facing_threshold > base_threshold

    def test_get_threshold_with_recent_failures(self):
        """Test threshold adjustment with recent failures."""
        base_threshold = self.thresholds.get_threshold("feature")

        context = {
            "recent_failures": ["failure1", "failure2"],
            "recent_success_rate": 0.8  # Below 85%
        }

        failure_threshold = self.thresholds.get_threshold("feature", context=context)
        assert failure_threshold > base_threshold

    def test_get_threshold_bounds(self):
        """Test that thresholds stay within valid bounds."""
        # Test various combinations
        test_cases = [
            ("security", "pre-release", "critical", True, {"recent_failures": ["f1", "f2"]}),
            ("exploratory", "exploration", "trivial", False, {}),
            ("documentation", "maintenance", "low", True, {})
        ]

        for task_type, phase, criticality, user_facing, context in test_cases:
            threshold = self.thresholds.get_threshold(
                task_type, phase, criticality, user_facing, context
            )
            assert 60 <= threshold <= 100

    def test_get_threshold_invalid_task_type(self):
        """Test threshold calculation with invalid task type."""
        threshold = self.thresholds.get_threshold("invalid_task_type")
        # Should default to feature task type
        expected_base = self.thresholds.BASE_THRESHOLDS[TaskType.FEATURE]
        assert abs(threshold - expected_base) < 10  # Allow some variation

    def test_get_threshold_with_explanation(self):
        """Test threshold calculation with detailed explanation."""
        result = self.thresholds.get_threshold_with_explanation(
            "security", "pre-release", "critical", True
        )

        assert "threshold" in result
        assert "base_threshold" in result
        assert "task_type" in result
        assert "explanation" in result
        assert "rationale" in result

        assert isinstance(result["explanation"], list)
        assert len(result["explanation"]) > 0
        assert isinstance(result["rationale"], str)

    def test_get_rationale(self):
        """Test rationale generation for different threshold levels."""
        # Very high threshold
        rationale = self.thresholds._get_rationale(95, "security")
        assert "Very high standards" in rationale

        # High threshold
        rationale = self.thresholds._get_rationale(85, "feature")
        assert "High quality standards" in rationale

        # Standard threshold
        rationale = self.thresholds._get_rationale(75, "testing")
        assert "Standard quality requirements" in rationale

        # Low threshold
        rationale = self.thresholds._get_rationale(65, "exploratory")
        assert "Relaxed standards" in rationale

    def test_has_recent_failures(self):
        """Test recent failures detection."""
        # No context
        assert not self.thresholds._has_recent_failures(None)
        assert not self.thresholds._has_recent_failures({})

        # With failures
        context_with_failures = {"recent_failures": ["f1", "f2"]}
        assert self.thresholds._has_recent_failures(context_with_failures)

        # With low success rate
        context_low_success = {"recent_success_rate": 0.8}
        assert self.thresholds._has_recent_failures(context_low_success)

        # With good success rate
        context_good_success = {"recent_success_rate": 0.9}
        assert not self.thresholds._has_recent_failures(context_good_success)

    def test_record_threshold_decision(self):
        """Test recording threshold decisions."""
        # Mock file operations to avoid actual file I/O
        mock_data = {"threshold_history": [], "adjustments_applied": 0}

        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("json.dump"):
                self.thresholds._record_threshold_decision(
                    "security", 95, 90, {"project_phase": "pre-release"}
                )

    def test_get_statistics_empty(self):
        """Test statistics calculation with empty history."""
        # Create empty history file
        empty_data = {"threshold_history": []}
        with open(self.thresholds.history_file, "w") as f:
            json.dump(empty_data, f)

        stats = self.thresholds.get_statistics()
        assert stats["total_decisions"] == 0
        assert stats["average_threshold"] == 0
        assert stats["most_common_task_type"] is None

    def test_get_statistics_with_data(self):
        """Test statistics calculation with historical data."""
        # Create history file with test data
        test_data = {
            "threshold_history": [
                {"threshold": 90, "task_type": "security"},
                {"threshold": 80, "task_type": "feature"},
                {"threshold": 70, "task_type": "security"},
                {"threshold": 85, "task_type": "documentation"}
            ]
        }

        with open(self.thresholds.history_file, "w") as f:
            json.dump(test_data, f)

        stats = self.thresholds.get_statistics()
        assert stats["total_decisions"] == 4
        assert stats["average_threshold"] == 81.25
        assert stats["min_threshold"] == 70
        assert stats["max_threshold"] == 90
        assert stats["most_common_task_type"] == "security"

    def test_get_statistics_error_handling(self):
        """Test statistics calculation with corrupted file."""
        # Write invalid JSON
        with open(self.thresholds.history_file, "w") as f:
            f.write("invalid json")

        stats = self.thresholds.get_statistics()
        assert "error" in stats

    def test_get_timestamp(self):
        """Test timestamp generation."""
        timestamp = AdaptiveQualityThresholds._get_timestamp()
        assert isinstance(timestamp, str)
        assert "T" in timestamp  # ISO format check

    def test_base_thresholds_completeness(self):
        """Test that all task types have base thresholds."""
        for task_type in TaskType:
            assert task_type in self.thresholds.BASE_THRESHOLDS
            assert isinstance(self.thresholds.BASE_THRESHOLDS[task_type], int)
            assert 60 <= self.thresholds.BASE_THRESHOLDS[task_type] <= 100

    def test_phase_multipliers_completeness(self):
        """Test that all project phases have multipliers."""
        for phase in ProjectPhase:
            assert phase in self.thresholds.PHASE_MULTIPLIERS
            assert isinstance(self.thresholds.PHASE_MULTIPLIERS[phase], (int, float))

    def test_criticality_adjustments_completeness(self):
        """Test criticality adjustments."""
        criticalities = ["critical", "high", "medium", "low", "trivial"]
        for crit in criticalities:
            assert crit in self.thresholds.CRITICALITY_ADJUSTMENTS
            assert isinstance(self.thresholds.CRITICALITY_ADJUSTMENTS[crit], (int, float))

    @patch('adaptive_quality_thresholds.print')
    def test_record_threshold_decision_warning(self, mock_print):
        """Test warning when recording fails."""
        # Force an exception during recording
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            self.thresholds._record_threshold_decision("test", 80, 75, {})

        # Should print warning but not raise exception
        mock_print.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])