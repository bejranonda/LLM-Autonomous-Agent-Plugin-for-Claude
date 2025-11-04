"""
Tests for Context-Aware Skill Recommendations (lib/context_aware_skill_recommendations.py)

Tests the enhanced skill recommendation system that provides
intelligent suggestions based on contextual factors.
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
    from context_aware_skill_recommendations import ContextAwareSkillRecommendations
except ImportError:
    pytest.skip("context_aware_skill_recommendations.py not available", allow_module_level=True)


class TestContextAwareSkillRecommendations:
    """Test cases for Context-Aware Skill Recommendations"""

    @pytest.fixture
    def recommendation_system(self, temp_directory):
        """Create a ContextAwareSkillRecommendations instance for testing"""
        return ContextAwareSkillRecommendations(data_dir=temp_directory)

    @pytest.fixture
    def base_recommendations(self):
        """Base skill recommendations for testing"""
        return [
            {"skill": "code-analysis", "confidence": 0.85},
            {"skill": "quality-standards", "confidence": 0.78},
            {"skill": "testing-strategies", "confidence": 0.72}
        ]

    @pytest.fixture
    def sample_task_info(self):
        """Sample task information for testing"""
        return {
            "type": "refactoring",
            "language": "python",
            "complexity": "medium",
            "framework": "flask"
        }

    @pytest.fixture
    def sample_context(self):
        """Sample context information for testing"""
        return {
            "time_of_day": "morning",
            "recent_outcomes": ["success", "success"],
            "user_preferences": {"prefer_fast_solutions": True},
            "project_phase": "development",
            "deadline_pressure": "medium",
            "team_size": 3
        }

    def test_initialization(self, recommendation_system):
        """Test system initialization"""
        assert recommendation_system is not None
        assert hasattr(recommendation_system, 'data_dir')
        assert hasattr(recommendation_system, 'recommendations_file')

    def test_recommend_with_context_basic(self, recommendation_system, base_recommendations, sample_task_info, sample_context):
        """Test basic context-aware recommendations"""
        recommendations = recommendation_system.recommend_skills_with_context(
            base_recommendations, sample_task_info, sample_context
        )

        assert isinstance(recommendations, list)
        assert len(recommendations) <= len(base_recommendations)

        # Check recommendation structure
        if recommendations:
            rec = recommendations[0]
            assert 'skill' in rec
            assert 'confidence' in rec
            assert 'context_factors' in rec
            assert 'adjusted_confidence' in rec

    def test_time_of_day_influence(self, recommendation_system, base_recommendations, sample_task_info):
        """Test time of day influence on recommendations"""
        time_contexts = ["early_morning", "morning", "afternoon", "evening", "night"]
        results = {}

        for time_period in time_contexts:
            context = {
                "time_of_day": time_period,
                "recent_outcomes": ["success"]
            }

            recommendations = recommendation_system.recommend_skills_with_context(
                base_recommendations, sample_task_info, context
            )

            results[time_period] = recommendations

        # Different times should potentially influence recommendations
        # (Implementation specific - test that it runs without error)
        for time_period, recs in results.items():
            assert isinstance(recs, list)

    def test_recent_outcomes_influence(self, recommendation_system, base_recommendations, sample_task_info):
        """Test influence of recent outcomes on recommendations"""
        outcome_patterns = [
            ["success", "success", "success"],  # Hot streak
            ["failure", "failure"],  # Cold streak
            ["success", "failure", "success"],  # Mixed
            []  # No history
        ]

        results = {}
        for outcomes in outcome_patterns:
            context = {
                "recent_outcomes": outcomes,
                "time_of_day": "morning"
            }

            recommendations = recommendation_system.recommend_skills_with_context(
                base_recommendations, sample_task_info, context
            )

            results[str(outcomes)] = recommendations

        # Should handle different outcome patterns
        for pattern, recs in results.items():
            assert isinstance(recs, list)

    def test_user_preferences_integration(self, recommendation_system, base_recommendations, sample_task_info):
        """Test integration of user preferences"""
        user_preferences = [
            {"prefer_fast_solutions": True, "detail_level": "minimal"},
            {"prefer_comprehensive_solutions": True, "detail_level": "comprehensive"},
            {"prefer_balanced_approach": True, "detail_level": "balanced"},
            {}  # No preferences
        ]

        results = {}
        for prefs in user_preferences:
            context = {
                "user_preferences": prefs,
                "time_of_day": "morning"
            }

            recommendations = recommendation_system.recommend_skills_with_context(
                base_recommendations, sample_task_info, context
            )

            results[str(prefs)] = recommendations

        # Should adapt to different user preferences
        for prefs_str, recs in results.items():
            assert isinstance(recs, list)

    def test_deadline_pressure_adjustment(self, recommendation_system, base_recommendations, sample_task_info):
        """Test deadline pressure influence on recommendations"""
        deadline_levels = ["low", "medium", "high", "critical"]
        results = {}

        for pressure in deadline_levels:
            context = {
                "deadline_pressure": pressure,
                "time_of_day": "morning"
            }

            recommendations = recommendation_system.recommend_skills_with_context(
                base_recommendations, sample_task_info, context
            )

            results[pressure] = recommendations

        # Higher pressure should potentially recommend faster approaches
        for pressure, recs in results.items():
            assert isinstance(recs, list)

    def test_team_size_consideration(self, recommendation_system, base_recommendations, sample_task_info):
        """Test team size influence on recommendations"""
        team_sizes = [1, 2, 5, 10]  # Solo to large team
        results = {}

        for size in team_sizes:
            context = {
                "team_size": size,
                "time_of_day": "morning"
            }

            recommendations = recommendation_system.recommend_skills_with_context(
                base_recommendations, sample_task_info, context
            )

            results[size] = recommendations

        # Should adapt recommendations based on team size
        for size, recs in results.items():
            assert isinstance(recs, list)

    def test_project_phase_context(self, recommendation_system, base_recommendations, sample_task_info):
        """Test project phase influence on recommendations"""
        phases = ["planning", "development", "testing", "deployment", "maintenance"]
        results = {}

        for phase in phases:
            context = {
                "project_phase": phase,
                "time_of_day": "morning"
            }

            recommendations = recommendation_system.recommend_skills_with_context(
                base_recommendations, sample_task_info, context
            )

            results[phase] = recommendations

        # Different phases should get different recommendations
        for phase, recs in results.items():
            assert isinstance(recs, list)

    def test_complexity_based_adjustment(self, recommendation_system, base_recommendations):
        """Test complexity-based recommendation adjustment"""
        complexity_levels = ["low", "medium", "high", "extreme"]
        task_info_base = {"type": "refactoring", "language": "python"}

        results = {}
        for complexity in complexity_levels:
            task_info = task_info_base.copy()
            task_info["complexity"] = complexity

            context = {"time_of_day": "morning"}

            recommendations = recommendation_system.recommend_skills_with_context(
                base_recommendations, task_info, context
            )

            results[complexity] = recommendations

        # Higher complexity should influence recommendations
        for complexity, recs in results.items():
            assert isinstance(recs, list)

    def test_recommendation_effectiveness_tracking(self, recommendation_system):
        """Test tracking of recommendation effectiveness"""
        recommendation_id = "test_rec_001"

        # Record recommendation effectiveness
        effectiveness_data = {
            "recommendation_id": recommendation_id,
            "task_info": {"type": "test", "language": "python"},
            "recommended_skills": ["code-analysis", "quality-standards"],
            "actual_used_skills": ["code-analysis", "quality-standards", "testing-strategies"],
            "success": True,
            "quality_score": 92.0,
            "user_satisfaction": "high"
        }

        result = recommendation_system.record_recommendation_effectiveness(effectiveness_data)
        assert result is True

        # Get effectiveness data
        effectiveness = recommendation_system.get_recommendation_effectiveness(recommendation_id)
        assert isinstance(effectiveness, dict)

    def test_learning_from_recommendations(self, recommendation_system, base_recommendations, sample_task_info):
        """Test that the system learns from recommendation outcomes"""
        # Record several successful recommendations
        for i in range(5):
            effectiveness_data = {
                "recommendation_id": f"learn_test_{i}",
                "task_info": sample_task_info,
                "recommended_skills": [rec["skill"] for rec in base_recommendations[:2]],
                "actual_used_skills": [rec["skill"] for rec in base_recommendations[:2]],
                "success": True,
                "quality_score": 90.0 + i,
                "user_satisfaction": "high"
            }
            recommendation_system.record_recommendation_effectiveness(effectiveness_data)

        # Get improved recommendations
        context = {"time_of_day": "morning"}
        improved_recs = recommendation_system.recommend_skills_with_context(
            base_recommendations, sample_task_info, context
        )

        assert isinstance(improved_recs, list)

        # Should have learned from previous successes
        for rec in improved_recs:
            assert 'adjusted_confidence' in rec

    def test_multi_factor_scoring(self, recommendation_system, base_recommendations, sample_task_info):
        """Test multi-factor scoring of recommendations"""
        rich_context = {
            "time_of_day": "morning",
            "recent_outcomes": ["success", "success"],
            "user_preferences": {
                "prefer_fast_solutions": False,
                "prefer_comprehensive_solutions": True
            },
            "project_phase": "development",
            "deadline_pressure": "medium",
            "team_size": 3,
            "project_type": "web_application",
            "security_requirements": ["authentication", "data_protection"]
        }

        recommendations = recommendation_system.recommend_skills_with_context(
            base_recommendations, sample_task_info, rich_context
        )

        assert isinstance(recommendations, list)

        # Check multi-factor scoring
        if recommendations:
            rec = recommendations[0]
            assert 'context_factors' in rec
            assert isinstance(rec['context_factors'], dict)

            # Should have multiple factors considered
            assert len(rec['context_factors']) > 0

    def test_recommendation_explanation(self, recommendation_system, base_recommendations, sample_task_info, sample_context):
        """Test recommendation explanation generation"""
        recommendations = recommendation_system.recommend_skills_with_context(
            base_recommendations, sample_task_info, sample_context
        )

        if recommendations:
            # Get explanation for top recommendation
            explanation = recommendation_system.get_recommendation_explanation(
                recommendations[0], sample_task_info, sample_context
            )

            assert isinstance(explanation, dict)
            assert 'reasoning' in explanation
            assert 'key_factors' in explanation
            assert 'confidence_breakdown' in explanation

    def test_context_validation(self, recommendation_system, base_recommendations, sample_task_info):
        """Test validation of context data"""
        invalid_contexts = [
            {"time_of_day": "invalid_time"},
            {"deadline_pressure": "invalid_pressure"},
            {"team_size": -1},
            {"user_preferences": "invalid_format"}
        ]

        for invalid_context in invalid_contexts:
            # Should handle invalid context gracefully
            recommendations = recommendation_system.recommend_skills_with_context(
                base_recommendations, sample_task_info, invalid_context
            )

            assert isinstance(recommendations, list)

    def test_recommendation_persistence(self, recommendation_system, base_recommendations, sample_task_info, sample_context):
        """Test that recommendation data persists across instances"""
        # Make recommendations
        recommendations = recommendation_system.recommend_skills_with_context(
            base_recommendations, sample_task_info, sample_context
        )

        # Record effectiveness
        if recommendations:
            effectiveness_data = {
                "recommendation_id": "persistence_test",
                "task_info": sample_task_info,
                "recommended_skills": [rec["skill"] for rec in recommendations],
                "actual_used_skills": [rec["skill"] for rec in recommendations],
                "success": True,
                "quality_score": 95.0,
                "user_satisfaction": "high"
            }
            recommendation_system.record_recommendation_effectiveness(effectiveness_data)

        # Create new instance with same data directory
        new_system = ContextAwareSkillRecommendations(data_dir=recommendation_system.data_dir)

        # Should be able to retrieve recommendation history
        effectiveness = new_system.get_recommendation_effectiveness("persistence_test")
        assert isinstance(effectiveness, dict)

    def test_file_creation_and_format(self, temp_directory, base_recommendations, sample_task_info, sample_context):
        """Test that recommendations file is created correctly"""
        system = ContextAwareSkillRecommendations(data_dir=temp_directory)

        # Make recommendations to trigger file creation
        system.recommend_skills_with_context(base_recommendations, sample_task_info, sample_context)

        # Check file exists
        recs_file = os.path.join(temp_directory, 'context_recommendations.json')
        assert os.path.exists(recs_file)

        # Check file content
        with open(recs_file, 'r') as f:
            data = json.load(f)

        assert 'recommendation_history' in data
        assert 'effectiveness_tracking' in data
        assert 'context_patterns' in data

    def test_batch_recommendations(self, recommendation_system, base_recommendations):
        """Test batch recommendations for multiple tasks"""
        tasks = [
            {"type": "refactoring", "language": "python"},
            {"type": "testing", "language": "javascript"},
            {"type": "documentation", "language": "markdown"}
        ]

        contexts = [
            {"time_of_day": "morning", "deadline_pressure": "low"},
            {"time_of_day": "afternoon", "deadline_pressure": "medium"},
            {"time_of_day": "evening", "deadline_pressure": "high"}
        ]

        batch_results = recommendation_system.batch_recommend_with_context(
            base_recommendations, tasks, contexts
        )

        assert isinstance(batch_results, list)
        assert len(batch_results) == len(tasks)

        for i, result in enumerate(batch_results):
            assert 'task_info' in result
            assert 'recommendations' in result
            assert 'context' in result
            assert result['task_info'] == tasks[i]

    def test_performance_optimization(self, recommendation_system, base_recommendations, sample_task_info, sample_context):
        """Test performance of recommendation generation"""
        import time

        start_time = time.time()
        recommendations = recommendation_system.recommend_skills_with_context(
            base_recommendations, sample_task_info, sample_context
        )
        end_time = time.time()

        processing_time = end_time - start_time

        # Should be fast (less than 1 second)
        assert processing_time < 1.0
        assert isinstance(recommendations, list)

    def test_error_handling(self, recommendation_system):
        """Test error handling in various scenarios"""
        # Test with corrupted data file
        recs_file = recommendation_system.recommendations_file

        # Create corrupted JSON file
        with open(recs_file, 'w') as f:
            f.write("invalid json content")

        # Should handle gracefully
        recommendations = recommendation_system.recommend_skills_with_context(
            [], {"type": "test"}, {}
        )
        assert isinstance(recommendations, list)

    def test_recommendation_quality_metrics(self, recommendation_system, base_recommendations, sample_task_info):
        """Test quality metrics for recommendations"""
        context = {
            "time_of_day": "morning",
            "recent_outcomes": ["success"]
        }

        recommendations = recommendation_system.recommend_skills_with_context(
            base_recommendations, sample_task_info, context
        )

        if recommendations:
            # Get quality metrics
            metrics = recommendation_system.get_recommendation_quality_metrics(recommendations)

            assert isinstance(metrics, dict)
            assert 'overall_confidence' in metrics
            assert 'context_alignment' in metrics
            assert 'diversity_score' in metrics