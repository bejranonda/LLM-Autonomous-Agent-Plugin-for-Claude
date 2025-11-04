"""
Tests for Adaptive Quality Thresholds (lib/adaptive_quality_thresholds.py)

Tests the dynamic quality threshold system that adapts standards
based on project context, complexity, and historical performance.
"""

import pytest
import json
import os
import time
from unittest.mock import patch, mock_open
from datetime import datetime, timezone

# Import the module under test
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

try:
    from adaptive_quality_thresholds import AdaptiveQualityThresholds
except ImportError:
    pytest.skip("adaptive_quality_thresholds.py not available", allow_module_level=True)


class TestAdaptiveQualityThresholds:
    """Test cases for Adaptive Quality Thresholds"""

    @pytest.fixture
    def quality_thresholds(self, temp_directory):
        """Create an AdaptiveQualityThresholds instance for testing"""
        return AdaptiveQualityThresholds(storage_dir=temp_directory)

    @pytest.fixture
    def sample_task_info(self):
        """Sample task information for testing"""
        return {
            "type": "security_audit",
            "language": "python",
            "complexity": "high",
            "framework": "flask",
            "project_type": "financial_application",
            "is_user_facing": True,
            "project_phase": "pre_release"
        }

    def test_initialization(self, quality_thresholds):
        """Test system initialization"""
        assert quality_thresholds is not None
        assert hasattr(quality_thresholds, 'data_dir')
        assert hasattr(quality_thresholds, 'thresholds_file')

    def test_get_threshold_basic(self, quality_thresholds, sample_task_info):
        """Test getting basic threshold"""
        threshold = quality_thresholds.get_threshold(**sample_task_info)

        assert isinstance(threshold, (int, float))
        assert 0 <= threshold <= 100

    def test_get_context_score(self, quality_thresholds, sample_task_info):
        """Test context score calculation"""
        context_score = quality_thresholds.calculate_context_score(sample_task_info)

        assert isinstance(context_score, (int, float))
        assert 0 <= context_score <= 100

    def test_security_audit_high_threshold(self, quality_thresholds):
        """Test that security audits have higher thresholds"""
        security_task = {
            "type": "security_audit",
            "project_phase": "pre_release",
            "criticality": "high",
            "is_user_facing": True,
            "project_type": "financial_application"
        }

        threshold = quality_thresholds.get_threshold(**security_task)

        # Security tasks should have high thresholds
        assert threshold >= 90

    def test_prototype_low_threshold(self, quality_thresholds):
        """Test that prototypes have lower thresholds"""
        prototype_task = {
            "type": "feature_development",
            "project_phase": "development",
            "criticality": "low",
            "is_user_facing": False,
            "project_type": "prototype"
        }

        threshold = quality_thresholds.get_threshold(**prototype_task)

        # Prototype tasks should have lower thresholds
        assert threshold <= 75

    def test_project_type_adjustments(self, quality_thresholds):
        """Test threshold adjustments based on project type"""
        base_task = {
            "type": "feature_development",
            "project_phase": "development",
            "criticality": "medium",
            "is_user_facing": True
        }

        project_types = [
            ("prototype", 60),
            ("internal_tool", 70),
            ("customer_facing", 80),
            ("financial_system", 95),
            ("medical_system", 100)
        ]

        thresholds = {}
        for project_type, expected_min in project_types:
            task = base_task.copy()
            task["project_type"] = project_type
            threshold = quality_thresholds.get_threshold(**task)
            thresholds[project_type] = threshold

        # Verify thresholds increase with project criticality
        assert thresholds["prototype"] < thresholds["internal_tool"]
        assert thresholds["internal_tool"] < thresholds["customer_facing"]
        assert thresholds["customer_facing"] < thresholds["financial_system"]
        assert thresholds["financial_system"] <= thresholds["medical_system"]

    def test_phase_based_adjustments(self, quality_thresholds):
        """Test threshold adjustments based on project phase"""
        base_task = {
            "type": "feature_development",
            "project_type": "customer_facing",
            "criticality": "medium",
            "is_user_facing": True
        }

        phases = ["development", "testing", "pre_release", "production"]
        thresholds = {}

        for phase in phases:
            task = base_task.copy()
            task["project_phase"] = phase
            threshold = quality_thresholds.get_threshold(**task)
            thresholds[phase] = threshold

        # Verify thresholds generally increase toward production
        assert thresholds["development"] <= thresholds["testing"]
        assert thresholds["testing"] <= thresholds["pre_release"]
        assert thresholds["pre_release"] <= thresholds["production"]

    def test_criticality_factor(self, quality_thresholds):
        """Test criticality factor in threshold calculation"""
        base_task = {
            "type": "feature_development",
            "project_phase": "testing",
            "project_type": "customer_facing",
            "is_user_facing": True
        }

        criticality_levels = ["low", "medium", "high", "critical"]
        thresholds = {}

        for criticality in criticality_levels:
            task = base_task.copy()
            task["criticality"] = criticality
            threshold = quality_thresholds.get_threshold(**task)
            thresholds[criticality] = threshold

        # Verify thresholds increase with criticality
        assert thresholds["low"] <= thresholds["medium"]
        assert thresholds["medium"] <= thresholds["high"]
        assert thresholds["high"] <= thresholds["critical"]

    def test_user_facing_factor(self, quality_thresholds):
        """Test user-facing factor in threshold calculation"""
        base_task = {
            "type": "feature_development",
            "project_phase": "testing",
            "project_type": "internal_tool",
            "criticality": "medium"
        }

        # Test user-facing vs internal
        user_facing_task = base_task.copy()
        user_facing_task["is_user_facing"] = True

        internal_task = base_task.copy()
        internal_task["is_user_facing"] = False

        user_facing_threshold = quality_thresholds.get_threshold(**user_facing_task)
        internal_threshold = quality_thresholds.get_threshold(**internal_task)

        # User-facing should have higher threshold
        assert user_facing_threshold > internal_threshold

    def test_historical_performance_integration(self, quality_thresholds):
        """Test integration with historical performance data"""
        # Simulate historical performance
        historical_data = [
            {"task_type": "refactoring", "average_score": 92, "success_rate": 0.95},
            {"task_type": "testing", "average_score": 88, "success_rate": 0.90},
            {"task_type": "documentation", "average_score": 78, "success_rate": 0.85}
        ]

        for data in historical_data:
            quality_thresholds.update_historical_performance(data["task_type"], data)

        # Test thresholds reflect historical performance
        refactoring_threshold = quality_thresholds.get_threshold(
            task_type="refactoring",
            project_phase="testing"
        )

        documentation_threshold = quality_thresholds.get_threshold(
            task_type="documentation",
            project_phase="testing"
        )

        # Refactoring (better historical performance) should have higher threshold
        assert refactoring_threshold >= documentation_threshold

    def test_threshold_learning(self, quality_thresholds):
        """Test that thresholds learn from outcomes"""
        task_type = "custom_task"
        base_threshold = 70

        # Initial threshold
        initial_threshold = quality_thresholds.get_threshold(
            task_type=task_type,
            project_phase="testing"
        )

        # Record successful outcomes above current threshold
        for i in range(5):
            outcome = {
                "task_type": task_type,
                "actual_score": 85 + i,  # Consistently high scores
                "threshold_met": True,
                "user_satisfaction": "high"
            }
            quality_thresholds.record_outcome(outcome)

        # Updated threshold should be higher
        updated_threshold = quality_thresholds.get_threshold(
            task_type=task_type,
            project_phase="testing"
        )

        assert updated_threshold > initial_threshold

    def test_threshold_persistence(self, quality_thresholds, sample_task_info):
        """Test that thresholds persist across instances"""
        # Get initial threshold
        initial_threshold = quality_thresholds.get_threshold(**sample_task_info)

        # Create new instance with same data directory
        new_thresholds = AdaptiveQualityThresholds(data_dir=quality_thresholds.data_dir)

        # Should get similar threshold
        new_threshold = new_thresholds.get_threshold(**sample_task_info)

        assert abs(new_threshold - initial_threshold) < 5  # Allow small variation

    def test_file_creation_and_format(self, temp_directory, sample_task_info):
        """Test that thresholds file is created correctly"""
        thresholds = AdaptiveQualityThresholds(data_dir=temp_directory)

        # Get threshold to trigger file creation
        thresholds.get_threshold(**sample_task_info)

        # Check file exists
        thresholds_file = os.path.join(temp_directory, 'adaptive_thresholds.json')
        assert os.path.exists(thresholds_file)

        # Check file content
        with open(thresholds_file, 'r') as f:
            data = json.load(f)

        assert 'threshold_history' in data
        assert 'learned_adjustments' in data
        assert 'base_thresholds' in data

    def test_edge_cases(self, quality_thresholds):
        """Test edge cases and boundary conditions"""
        # Test with missing context
        minimal_task = {"type": "simple_task"}
        threshold = quality_thresholds.get_threshold(**minimal_task)
        assert isinstance(threshold, (int, float))

        # Test with extreme values
        extreme_task = {
            "type": "critical_task",
            "criticality": "critical",
            "project_phase": "production",
            "project_type": "medical_system",
            "is_user_facing": True,
            "complexity": "extreme"
        }
        threshold = quality_thresholds.get_threshold(**extreme_task)
        assert threshold >= 90  # Should be very high

    def test_threshold_validation(self, quality_thresholds):
        """Test threshold validation and bounds checking"""
        # Test threshold bounds
        for _ in range(10):
            task = {
                "type": "test_task",
                "project_phase": "testing"
            }
            threshold = quality_thresholds.get_threshold(**task)
            assert 0 <= threshold <= 100

    def test_multi_factor_scoring(self, quality_thresholds):
        """Test multi-factor context scoring"""
        complex_context = {
            "type": "security_audit",
            "language": "python",
            "framework": "django",
            "project_type": "financial_application",
            "project_phase": "pre_release",
            "criticality": "critical",
            "is_user_facing": True,
            "complexity": "high",
            "team_size": 5,
            "deadline_pressure": "high"
        }

        context_score = quality_thresholds.calculate_context_score(complex_context)
        threshold = quality_thresholds.get_threshold(**complex_context)

        # Complex, critical context should result in high threshold
        assert context_score > 70
        assert threshold >= 90

    def test_adaptation_speed(self, quality_thresholds):
        """Test speed of threshold adaptation"""
        task_type = "adaptive_task"

        # Get baseline
        baseline = quality_thresholds.get_threshold(
            task_type=task_type,
            project_phase="testing"
        )

        # Rapidly record high-performing outcomes
        high_outcomes = [
            {"task_type": task_type, "actual_score": 95, "threshold_met": True, "user_satisfaction": "high"}
            for _ in range(10)
        ]

        for outcome in high_outcomes:
            quality_thresholds.record_outcome(outcome)

        # Check adaptation
        adapted = quality_thresholds.get_threshold(
            task_type=task_type,
            project_phase="testing"
        )

        # Should show upward adaptation
        assert adapted > baseline

    def test_task_type_specific_learning(self, quality_thresholds):
        """Test learning specific to task types"""
        task_types = ["refactoring", "testing", "documentation", "security"]

        initial_thresholds = {}
        for task_type in task_types:
            initial_thresholds[task_type] = quality_thresholds.get_threshold(
                task_type=task_type,
                project_phase="testing"
            )

        # Simulate different performance patterns
        performance_patterns = {
            "refactoring": 90,  # High performance
            "testing": 85,      # Good performance
            "documentation": 75,  # Moderate performance
            "security": 95      # Excellent performance
        }

        for task_type, avg_score in performance_patterns.items():
            for _ in range(5):
                outcome = {
                    "task_type": task_type,
                    "actual_score": avg_score,
                    "threshold_met": avg_score > 70,
                    "user_satisfaction": "high" if avg_score > 80 else "medium"
                }
                quality_thresholds.record_outcome(outcome)

        # Check learned thresholds
        learned_thresholds = {}
        for task_type in task_types:
            learned_thresholds[task_type] = quality_thresholds.get_threshold(
                task_type=task_type,
                project_phase="testing"
            )

        # Higher-performing task types should have higher thresholds
        assert learned_thresholds["security"] > learned_thresholds["documentation"]
        assert learned_thresholds["refactoring"] > learned_thresholds["documentation"]

    def test_error_handling(self, quality_thresholds):
        """Test error handling in various scenarios"""
        # Test with corrupted data file
        thresholds_file = quality_thresholds.thresholds_file

        # Create corrupted JSON file
        with open(thresholds_file, 'w') as f:
            f.write("invalid json content")

        # Should handle gracefully
        threshold = quality_thresholds.get_threshold(task_type="test")
        assert isinstance(threshold, (int, float))

    def test_threshold_recommendations(self, quality_thresholds):
        """Test threshold recommendations and explanations"""
        task_info = {
            "type": "security_audit",
            "project_type": "financial_application",
            "project_phase": "pre_release",
            "criticality": "critical",
            "is_user_facing": True
        }

        threshold = quality_thresholds.get_threshold(**task_info)
        explanation = quality_threshold.get_threshold_explanation(**task_info)

        assert isinstance(explanation, dict)
        assert 'calculated_threshold' in explanation
        assert 'factors' in explanation
        assert 'recommendations' in explanation

        # Should explain why threshold is high
        assert explanation['calculated_threshold'] >= 90
        assert any('security' in factor.lower() for factor in explanation['factors'])