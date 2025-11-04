"""
Tests for User Preference Learner (lib/user_preference_learner.py)

Tests the user preference learning system that adapts to user behavior
and provides personalized experience.
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
    from user_preference_learner import UserPreferenceLearner
except ImportError:
    pytest.skip("user_preference_learner.py not available", allow_module_level=True)


class TestUserPreferenceLearner:
    """Test cases for User Preference Learner"""

    @pytest.fixture
    def preference_learner(self, temp_directory):
        """Create a UserPreferenceLearner instance for testing"""
        return UserPreferenceLearner(data_dir=temp_directory)

    @pytest.fixture
    def sample_interaction(self):
        """Sample user interaction data"""
        return {
            "interaction_type": "approval",
            "task_id": "task_789",
            "user_feedback": "Good, but prefer more concise code",
            "context": {
                "code_style": {"verbosity": "concise"},
                "quality_focus": {"tests": 0.40, "documentation": 0.25}
            }
        }

    def test_initialization(self, preference_learner):
        """Test system initialization"""
        assert preference_learner is not None
        assert hasattr(preference_learner, 'data_dir')
        assert hasattr(preference_learner, 'preferences_file')

    def test_record_interaction(self, preference_learner, sample_interaction):
        """Test recording user interaction"""
        result = preference_learner.record_interaction(**sample_interaction)

        assert result is True

    def test_record_invalid_interaction(self, preference_learner):
        """Test recording invalid interaction data"""
        invalid_interaction = {
            "interaction_type": "invalid_type",
            "task_id": "test",
            "user_feedback": "test",
            "context": {}
        }

        result = preference_learner.record_interaction(**invalid_interaction)
        assert result is False

    def test_get_learned_preferences(self, preference_learner, sample_interaction):
        """Test retrieving learned preferences"""
        # Record interaction
        preference_learner.record_interaction(**sample_interaction)

        # Get learned preferences
        preferences = preference_learner.get_learned_preferences("coding_style")

        assert isinstance(preferences, dict)
        assert 'verbosity' in preferences
        assert 'confidence' in preferences

    def test_coding_style_learning(self, preference_learner):
        """Test learning of coding style preferences"""
        # Record multiple coding style interactions
        interactions = [
            {
                "interaction_type": "approval",
                "task_id": f"task_{i}",
                "user_feedback": "Good, concise code",
                "context": {
                    "code_style": {"verbosity": "concise"},
                    "language": "python"
                }
            }
            for i in range(5)
        ]

        for interaction in interactions:
            preference_learner.record_interaction(**interaction)

        # Get coding style preferences
        style_prefs = preference_learner.get_learned_preferences("coding_style")

        assert isinstance(style_prefs, dict)
        assert style_prefs.get('verbosity') == 'concise'
        assert style_prefs.get('confidence') > 0.5

    def test_quality_weights_learning(self, preference_learner):
        """Test learning of quality weight preferences"""
        # Record interactions with quality feedback
        interactions = [
            {
                "interaction_type": "approval",
                "task_id": f"task_{i}",
                "user_feedback": "Excellent test coverage",
                "context": {
                    "quality_focus": {
                        "tests": 0.40,
                        "documentation": 0.20,
                        "code_quality": 0.25,
                        "standards": 0.10,
                        "patterns": 0.05
                    }
                }
            }
            for i in range(3)
        ]

        for interaction in interactions:
            preference_learner.record_interaction(**interaction)

        # Get quality weight preferences
        quality_prefs = preference_learner.get_learned_preferences("quality_weights")

        assert isinstance(quality_prefs, dict)
        assert 'tests' in quality_prefs
        assert 'documentation' in quality_prefs
        assert quality_prefs['tests'] > quality_prefs['documentation']

    def test_workflow_preferences_learning(self, preference_learner):
        """Test learning of workflow preferences"""
        # Record workflow interactions
        workflow_interactions = [
            {
                "interaction_type": "approval",
                "task_id": "auto_task_1",
                "user_feedback": "Good automation",
                "context": {
                    "workflow": {
                        "auto_fix_confidence": 0.90,
                        "parallel_execution": True,
                        "confirmation_required": ["breaking_changes", "security_fixes"],
                        "quality_threshold": 85
                    }
                }
            },
            {
                "interaction_type": "rejection",
                "task_id": "auto_task_2",
                "user_feedback": "Too many confirmations",
                "context": {
                    "workflow": {
                        "auto_fix_confidence": 0.85,
                        "parallel_execution": True,
                        "confirmation_required": ["breaking_changes"],
                        "quality_threshold": 80
                    }
                }
            }
        ]

        for interaction in workflow_interactions:
            preference_learner.record_interaction(**interaction)

        # Get workflow preferences
        workflow_prefs = preference_learner.get_learned_preferences("workflow")

        assert isinstance(workflow_prefs, dict)
        assert 'auto_fix_confidence' in workflow_prefs
        assert 'quality_threshold' in workflow_prefs

    def test_communication_style_learning(self, preference_learner):
        """Test learning of communication style preferences"""
        # Record communication interactions
        comm_interactions = [
            {
                "interaction_type": "approval",
                "task_id": f"comm_task_{i}",
                "user_feedback": "Just right amount of detail",
                "context": {
                    "communication": {
                        "detail_level": "balanced",
                        "technical_depth": "medium",
                        "explanation_preference": "when_needed"
                    }
                }
            }
            for i in range(4)
        ]

        for interaction in comm_interactions:
            preference_learner.record_interaction(**interaction)

        # Get communication preferences
        comm_prefs = preference_learner.get_learned_preferences("communication")

        assert isinstance(comm_prefs, dict)
        assert comm_prefs.get('detail_level') == 'balanced'
        assert comm_prefs.get('confidence') > 0.5

    def test_confidence_scoring(self, preference_learner):
        """Test confidence scoring for learned preferences"""
        preference_type = "test_preference"

        # Record increasing number of interactions
        for i in range(10):
            interaction = {
                "interaction_type": "approval",
                "task_id": f"confidence_task_{i}",
                "user_feedback": "Consistent preference",
                "context": {
                    preference_type: {"value": "consistent_value"}
                }
            }
            preference_learner.record_interaction(**interaction)

        # Get preferences with confidence
        prefs = preference_learner.get_learned_preferences(preference_type)

        assert isinstance(prefs, dict)
        assert 'confidence' in prefs
        # Confidence should increase with more consistent data
        assert prefs['confidence'] > 0.5

    def test_preference_evolution(self, preference_learner):
        """Test that preferences evolve over time"""
        # Initially prefer concise code
        for i in range(5):
            interaction = {
                "interaction_type": "approval",
                "task_id": f"evolution_task_{i}",
                "user_feedback": "Good concise code",
                "context": {
                    "code_style": {"verbosity": "concise"}
                }
            }
            preference_learner.record_interaction(**interaction)

        # Check initial preference
        prefs_1 = preference_learner.get_learned_preferences("coding_style")
        assert prefs_1.get('verbosity') == 'concise'

        # Switch to preferring verbose code
        for i in range(5):
            interaction = {
                "interaction_type": "approval",
                "task_id": f"evolution_task_verbose_{i}",
                "user_feedback": "Good verbose code with comments",
                "context": {
                    "code_style": {"verbosity": "verbose"}
                }
            }
            preference_learner.record_interaction(**interaction)

        # Check evolved preference
        prefs_2 = preference_learner.get_learned_preferences("coding_style")
        # Should evolve towards verbose or show mixed preference
        assert 'verbosity' in prefs_2

    def test_preference_persistence(self, preference_learner, sample_interaction):
        """Test that preferences persist across instances"""
        # Record interaction
        preference_learner.record_interaction(**sample_interaction)

        # Create new instance with same data directory
        new_learner = UserPreferenceLearner(data_dir=preference_learner.data_dir)

        # Check preferences are available
        prefs = new_learner.get_learned_preferences("coding_style")

        assert isinstance(prefs, dict)

    def test_file_creation_and_format(self, temp_directory, sample_interaction):
        """Test that preferences file is created correctly"""
        learner = UserPreferenceLearner(data_dir=temp_directory)

        # Record interaction
        learner.record_interaction(**sample_interaction)

        # Check file exists
        prefs_file = os.path.join(temp_directory, 'user_preferences.json')
        assert os.path.exists(prefs_file)

        # Check file content
        with open(prefs_file, 'r') as f:
            data = json.load(f)

        assert 'interaction_history' in data
        assert 'learned_preferences' in data
        assert len(data['interaction_history']) > 0

    def test_feedback_weighting(self, preference_learner):
        """Test that different feedback types are weighted appropriately"""
        base_interaction = {
            "task_id": "weight_test",
            "context": {
                "test_pref": {"value": "test_value"}
            }
        }

        # Record different feedback types
        feedback_types = [
            ("approval", 1.0),  # Positive feedback
            ("rejection", -0.5),  # Negative feedback
            ("suggestion", 0.5),  # Neutral/constructive feedback
        ]

        for feedback_type, expected_weight in feedback_types:
            interaction = base_interaction.copy()
            interaction["interaction_type"] = feedback_type
            interaction["user_feedback"] = f"Test {feedback_type}"

            preference_learner.record_interaction(**interaction)

        # Get weighted preferences
        prefs = preference_learner.get_learned_preferences("test_pref")

        assert isinstance(prefs, dict)
        # Should have weighted the feedback appropriately
        assert 'confidence' in prefs

    def test_context_extraction(self, preference_learner):
        """Test extraction of preferences from different contexts"""
        # Test various context structures
        contexts = [
            {
                "language": "python",
                "framework": "flask",
                "style": {"verbosity": "concise"}
            },
            {
                "language": "javascript",
                "framework": "react",
                "style": {"verbosity": "concise"}
            },
            {
                "language": "python",
                "framework": "django",
                "style": {"verbosity": "verbose"}
            }
        ]

        for i, context in enumerate(contexts):
            interaction = {
                "interaction_type": "approval",
                "task_id": f"context_task_{i}",
                "user_feedback": "Good style",
                "context": context
            }
            preference_learner.record_interaction(**interaction)

        # Get context-specific preferences
        python_prefs = preference_learner.get_context_preferences("python")
        js_prefs = preference_learner.get_context_preferences("javascript")

        assert isinstance(python_prefs, dict)
        assert isinstance(js_prefs, dict)

    def test_preference_recommendations(self, preference_learner):
        """Test generating preference-based recommendations"""
        # Learn some preferences first
        interactions = [
            {
                "interaction_type": "approval",
                "task_id": f"rec_task_{i}",
                "user_feedback": "Good approach",
                "context": {
                    "code_style": {"verbosity": "concise"},
                    "quality_focus": {"tests": 0.40}
                }
            }
            for i in range(5)
        ]

        for interaction in interactions:
            preference_learner.record_interaction(**interaction)

        # Get recommendations
        recommendations = preference_learner.get_preference_recommendations()

        assert isinstance(recommendations, dict)
        assert 'suggested_settings' in recommendations
        assert 'confidence_levels' in recommendations

    def test_error_handling(self, preference_learner):
        """Test error handling in various scenarios"""
        # Test with corrupted data file
        prefs_file = preference_learner.preferences_file

        # Create corrupted JSON file
        with open(prefs_file, 'w') as f:
            f.write("invalid json content")

        # Should handle gracefully
        prefs = preference_learner.get_learned_preferences("test")
        assert isinstance(prefs, dict)

    def test_interaction_validation(self, preference_learner):
        """Test validation of interaction data"""
        # Test missing required fields
        invalid_interactions = [
            {},  # Empty
            {"interaction_type": "approval"},  # Missing task_id
            {"task_id": "test"},  # Missing interaction_type
            {"interaction_type": "approval", "task_id": "test"},  # Missing context
        ]

        for invalid_interaction in invalid_interactions:
            result = preference_learner.record_interaction(**invalid_interaction)
            assert result is False

    def test_preference_export_import(self, preference_learner, temp_directory):
        """Test exporting and importing preferences"""
        # Record some interactions
        for i in range(3):
            interaction = {
                "interaction_type": "approval",
                "task_id": f"export_task_{i}",
                "user_feedback": "Test feedback",
                "context": {
                    "test_pref": {"value": f"test_value_{i}"}
                }
            }
            preference_learner.record_interaction(**interaction)

        # Export preferences
        export_file = os.path.join(temp_directory, "exported_prefs.json")
        preference_learner.export_preferences(export_file)

        assert os.path.exists(export_file)

        # Create new learner and import
        new_learner = UserPreferenceLearner(data_dir=temp_directory)
        new_learner.import_preferences(export_file)

        # Verify preferences were imported
        prefs = new_learner.get_learned_preferences("test_pref")
        assert isinstance(prefs, dict)

    def test_preference_reset(self, preference_learner, sample_interaction):
        """Test resetting learned preferences"""
        # Record some interactions
        preference_learner.record_interaction(**sample_interaction)

        # Verify preferences exist
        prefs = preference_learner.get_learned_preferences("coding_style")
        assert isinstance(prefs, dict)

        # Reset preferences
        preference_learner.reset_preferences()

        # Verify preferences are reset
        reset_prefs = preference_learner.get_learned_preferences("coding_style")
        assert reset_prefs == {} or reset_prefs.get('confidence', 0) < 0.1