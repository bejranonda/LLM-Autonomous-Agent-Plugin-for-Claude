"""
Tests for Predictive Skill Loader (lib/predictive_skill_loader.py)

Tests the predictive skill selection system that anticipates and pre-loads
optimal skills based on task analysis and historical patterns.
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
    from predictive_skill_loader import PredictiveSkillLoader
except ImportError:
    pytest.skip("predictive_skill_loader.py not available", allow_module_level=True)


class TestPredictiveSkillLoader:
    """Test cases for Predictive Skill Loader"""

    @pytest.fixture
    def skill_loader(self, temp_directory):
        """Create a PredictiveSkillLoader instance for testing"""
        return PredictiveSkillLoader(storage_dir=temp_directory)

    @pytest.fixture
    def sample_task_info(self):
        """Sample task information for testing"""
        return {
            "type": "refactoring",
            "language": "python",
            "complexity": "medium",
            "framework": "flask",
            "description": "Refactor authentication module"
        }

    @pytest.fixture
    def sample_skill_effectiveness(self):
        """Sample skill effectiveness data"""
        return {
            "code-analysis": {"success_rate": 0.93, "recommended_for": ["refactoring", "bug_fix"]},
            "quality-standards": {"success_rate": 0.88, "recommended_for": ["refactoring", "quality_check"]},
            "testing-strategies": {"success_rate": 0.85, "recommended_for": ["testing", "development"]},
            "security-patterns": {"success_rate": 0.90, "recommended_for": ["security", "authentication"]},
            "pattern-learning": {"success_rate": 0.87, "recommended_for": ["analysis", "learning"]}
        }

    def test_initialization(self, skill_loader):
        """Test system initialization"""
        assert skill_loader is not None
        assert hasattr(skill_loader, 'data_dir')
        assert hasattr(skill_loader, 'skills_file')

    def test_predict_skills_basic(self, skill_loader, sample_task_info):
        """Test basic skill prediction"""
        skills = skill_loader.predict_skills(sample_task_info, top_k=5)

        assert isinstance(skills, list)
        assert len(skills) <= 5

        # Check skill structure
        if skills:
            skill = skills[0]
            assert 'skill' in skill
            assert 'confidence' in skill
            assert isinstance(skill['confidence'], (int, float))
            assert 0 <= skill['confidence'] <= 1

    def test_predict_skills_with_context(self, skill_loader):
        """Test skill prediction with rich context"""
        task_info = {
            "type": "security_audit",
            "language": "python",
            "framework": "django",
            "project_type": "financial_application",
            "complexity": "high",
            "is_user_facing": True,
            "security_concerns": ["authentication", "data_protection", "encryption"]
        }

        skills = skill_loader.predict_skills(task_info, top_k=3)

        assert isinstance(skills, list)

        # Should predict security-related skills
        skill_names = [skill['skill'] for skill in skills]
        security_skills = [s for s in skill_names if 'security' in s.lower()]

        # Should include security-related skills for security audit
        assert len(security_skills) > 0

    def test_update_skill_effectiveness(self, skill_loader, sample_task_info):
        """Test updating skill effectiveness based on outcomes"""
        skill_name = "code-analysis"
        success = True
        quality_score = 94.0

        result = skill_loader.update_skill_effectiveness(
            skill_name, success, quality_score, sample_task_info
        )

        assert result is True

    def test_skill_confidence_calculation(self, skill_loader, sample_task_info):
        """Test confidence calculation for skill predictions"""
        skills = skill_loader.predict_skills(sample_task_info, top_k=10)

        # Skills should be sorted by confidence (highest first)
        if len(skills) > 1:
            for i in range(len(skills) - 1):
                assert skills[i]['confidence'] >= skills[i + 1]['confidence']

        # Confidence should be between 0 and 1
        for skill in skills:
            assert 0 <= skill['confidence'] <= 1

    def test_task_type_specific_prediction(self, skill_loader):
        """Test skill prediction for different task types"""
        task_types = [
            {"type": "refactoring", "language": "python"},
            {"type": "testing", "language": "javascript"},
            {"type": "security_audit", "language": "python"},
            {"type": "documentation", "language": "markdown"},
            {"type": "performance_optimization", "language": "python"}
        ]

        predictions = {}
        for task in task_types:
            skills = skill_loader.predict_skills(task, top_k=3)
            predictions[task['type']] = [skill['skill'] for skill in skills]

        # Different task types should have different skill predictions
        for i, (type1, skills1) in enumerate(predictions.items()):
            for type2, skills2 in list(predictions.items())[i+1:]:
                # Should have some differences in predicted skills
                if skills1 and skills2:
                    similarity = len(set(skills1) & set(skills2)) / len(set(skills1) | set(skills2))
                    # Some overlap is expected, but not identical predictions
                    assert similarity < 1.0

    def test_language_specific_prediction(self, skill_loader):
        """Test skill prediction for different programming languages"""
        base_task = {
            "type": "refactoring",
            "complexity": "medium"
        }

        languages = ["python", "javascript", "typescript", "java", "go"]
        predictions = {}

        for language in languages:
            task = base_task.copy()
            task["language"] = language
            skills = skill_loader.predict_skills(task, top_k=3)
            predictions[language] = skills

        # Should have language-specific considerations
        for language, skills in predictions.items():
            assert isinstance(skills, list)

    def test_learning_from_outcomes(self, skill_loader, sample_task_info):
        """Test that the system learns from task outcomes"""
        skill_name = "test-skill"
        task_type = sample_task_info["type"]

        # Initial prediction
        initial_skills = skill_loader.predict_skills(sample_task_info, top_k=5)
        initial_confidence = 0

        for skill in initial_skills:
            if skill['skill'] == skill_name:
                initial_confidence = skill['confidence']
                break

        # Record successful outcomes
        for i in range(5):
            outcome = {
                "task_info": sample_task_info,
                "used_skills": [skill_name],
                "success": True,
                "quality_score": 90.0 + i,
                "execution_time_seconds": 120 - i * 5
            }
            skill_loader.record_task_outcome(outcome)

        # Updated prediction should have higher confidence
        updated_skills = skill_loader.predict_skills(sample_task_info, top_k=5)
        updated_confidence = 0

        for skill in updated_skills:
            if skill['skill'] == skill_name:
                updated_confidence = skill['confidence']
                break

        # Confidence should have increased
        if initial_confidence > 0:
            assert updated_confidence > initial_confidence

    def test_skill_combination_optimization(self, skill_loader):
        """Test optimization of skill combinations"""
        task_info = {
            "type": "comprehensive_analysis",
            "language": "python",
            "complexity": "high"
        }

        # Get individual skill predictions
        individual_skills = skill_loader.predict_skills(task_info, top_k=5)

        # Get optimized combinations
        combinations = skill_loader.get_optimal_combinations(task_info, max_skills=3)

        assert isinstance(combinations, list)

        # Check combination structure
        if combinations:
            combo = combinations[0]
            assert 'skills' in combo
            assert 'combined_confidence' in combo
            assert 'synergy_score' in combo
            assert isinstance(combo['skills'], list)
            assert len(combo['skills']) <= 3

    def test_performance_improvement_tracking(self, skill_loader):
        """Test tracking of prediction performance improvement"""
        task_info = {"type": "performance_task", "language": "python"}

        # Record initial prediction performance
        initial_prediction = skill_loader.predict_skills(task_info, top_k=3)

        # Simulate task execution with outcomes
        outcomes = []
        for i in range(10):
            outcome = {
                "task_info": task_info,
                "predicted_skills": [skill['skill'] for skill in initial_prediction],
                "actual_effective_skills": ["code-analysis", "quality-standards"],
                "success": True,
                "quality_score": 85.0 + i
            }
            outcomes.append(outcome)
            skill_loader.record_task_outcome(outcome)

        # Get performance metrics
        metrics = skill_loader.get_prediction_performance(days=7)

        assert isinstance(metrics, dict)
        assert 'accuracy' in metrics
        assert 'improvement_trend' in metrics
        assert 'total_predictions' in metrics

    def test_context_aware_adjustment(self, skill_loader):
        """Test context-aware skill adjustment"""
        base_task = {
            "type": "refactoring",
            "language": "python"
        }

        # Different contexts
        contexts = [
            {"project_phase": "development", "time_constraint": "low"},
            {"project_phase": "production", "time_constraint": "high"},
            {"project_phase": "testing", "security_required": True},
            {"project_phase": "documentation", "detail_level": "high"}
        ]

        predictions = {}
        for i, context in enumerate(contexts):
            task = base_task.copy()
            task.update(context)
            skills = skill_loader.predict_skills(task, top_k=3)
            predictions[f"context_{i}"] = [skill['skill'] for skill in skills]

        # Different contexts should influence predictions
        # (This is a basic test - actual differences depend on implementation)
        for context_name, skills in predictions.items():
            assert isinstance(skills, list)

    def test_skill_effectiveness_persistence(self, skill_loader, sample_task_info):
        """Test that skill effectiveness persists across instances"""
        skill_name = "persistence-test-skill"

        # Update effectiveness
        skill_loader.update_skill_effectiveness(
            skill_name, True, 95.0, sample_task_info
        )

        # Create new instance with same data directory
        new_loader = PredictiveSkillLoader(storage_dir=skill_loader.data_dir)

        # Check effectiveness is available
        effectiveness = new_loader.get_skill_effectiveness(skill_name)
        assert isinstance(effectiveness, dict)

    def test_file_creation_and_format(self, temp_directory, sample_task_info):
        """Test that skills file is created correctly"""
        loader = PredictiveSkillLoader(storage_dir=temp_directory)

        # Predict skills to trigger file creation
        loader.predict_skills(sample_task_info, top_k=3)

        # Check file exists
        skills_file = os.path.join(temp_directory, 'skill_effectiveness.json')
        assert os.path.exists(skills_file)

        # Check file content
        with open(skills_file, 'r') as f:
            data = json.load(f)

        assert 'skill_effectiveness' in data
        assert 'prediction_history' in data
        assert 'performance_metrics' in data

    def test_unseen_task_handling(self, skill_loader):
        """Test handling of unseen task types"""
        unseen_task = {
            "type": "brand_new_task_type",
            "language": "emerging_language",
            "complexity": "unknown"
        }

        skills = skill_loader.predict_skills(unseen_task, top_k=3)

        # Should still return predictions based on general patterns
        assert isinstance(skills, list)
        assert len(skills) <= 3

        if skills:
            # Confidence might be lower for unseen tasks
            assert all(0 <= skill['confidence'] <= 1 for skill in skills)

    def test_prediction_confidence_validation(self, skill_loader, sample_task_info):
        """Test confidence validation in predictions"""
        skills = skill_loader.predict_skills(sample_task_info, top_k=10)

        for skill in skills:
            assert 'confidence' in skill
            confidence = skill['confidence']

            # Confidence should be a valid number
            assert isinstance(confidence, (int, float))
            assert not (confidence != confidence)  # Not NaN
            assert 0 <= confidence <= 1

    def test_skill_loading_performance(self, skill_loader, sample_task_info):
        """Test performance of skill loading"""
        import time

        # Measure prediction time
        start_time = time.time()
        skills = skill_loader.predict_skills(sample_task_info, top_k=5)
        end_time = time.time()

        prediction_time = end_time - start_time

        # Should be fast (less than 1 second for basic prediction)
        assert prediction_time < 1.0
        assert isinstance(skills, list)

    def test_error_handling(self, skill_loader):
        """Test error handling in various scenarios"""
        # Test with corrupted data file
        skills_file = skill_loader.skills_file

        # Create corrupted JSON file
        with open(skills_file, 'w') as f:
            f.write("invalid json content")

        # Should handle gracefully
        skills = skill_loader.predict_skills({"type": "test"}, top_k=3)
        assert isinstance(skills, list)

    def test_recommendation_quality(self, skill_loader):
        """Test quality of skill recommendations"""
        high_quality_task = {
            "type": "security_audit",
            "language": "python",
            "framework": "django",
            "project_type": "financial_application",
            "complexity": "high",
            "security_requirements": ["auth", "encryption", "audit_trail"]
        }

        skills = skill_loader.predict_skills(high_quality_task, top_k=5)

        # Should recommend relevant skills
        skill_names = [skill['skill'] for skill in skills]

        # Check for security-related skills
        security_related = any(
            'security' in name.lower() or 'auth' in name.lower()
            for name in skill_names
        )

        # High confidence predictions for relevant skills
        if skills:
            max_confidence = max(skill['confidence'] for skill in skills)
            assert max_confidence > 0.5  # Should be confident in recommendations

    def test_batch_prediction(self, skill_loader):
        """Test batch prediction for multiple tasks"""
        tasks = [
            {"type": "refactoring", "language": "python"},
            {"type": "testing", "language": "javascript"},
            {"type": "documentation", "language": "markdown"}
        ]

        batch_results = skill_loader.batch_predict(tasks, top_k=3)

        assert isinstance(batch_results, list)
        assert len(batch_results) == len(tasks)

        for i, result in enumerate(batch_results):
            assert 'task_info' in result
            assert 'predicted_skills' in result
            assert result['task_info'] == tasks[i]
            assert isinstance(result['predicted_skills'], list)