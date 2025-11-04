"""
Tests for Agent Feedback System (lib/agent_feedback_system.py)

Tests the cross-tier communication system that enables feedback exchange
between analysis and execution agents for continuous improvement.
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
    from agent_feedback_system import AgentFeedbackSystem
except ImportError:
    pytest.skip("agent_feedback_system.py not available", allow_module_level=True)


class TestAgentFeedbackSystem:
    """Test cases for Agent Feedback System"""

    @pytest.fixture
    def feedback_system(self, temp_directory):
        """Create an AgentFeedbackSystem instance for testing"""
        return AgentFeedbackSystem(storage_dir=temp_directory)

    @pytest.fixture
    def sample_feedback(self):
        """Sample feedback data for testing"""
        return {
            "from_agent": "quality-controller",
            "to_agent": "code-analyzer",
            "task_id": "task_123",
            "feedback_type": "success",
            "message": "Recommendations highly effective, quality score +12 points",
            "impact": "quality_score +12"
        }

    def test_initialization(self, feedback_system):
        """Test system initialization"""
        assert feedback_system is not None
        assert hasattr(feedback_system, 'data_dir')
        assert hasattr(feedback_system, 'feedback_file')

    def test_add_feedback_success(self, feedback_system, sample_feedback):
        """Test adding feedback successfully"""
        result = feedback_system.add_feedback(**sample_feedback)

        assert result is True
        assert feedback_system.feedback_file is not None

    def test_add_feedback_invalid_type(self, feedback_system, sample_feedback):
        """Test adding feedback with invalid type"""
        sample_feedback['feedback_type'] = 'invalid_type'

        result = feedback_system.add_feedback(**sample_feedback)
        assert result is False

    def test_add_feedback_missing_required(self, feedback_system):
        """Test adding feedback with missing required fields"""
        incomplete_feedback = {
            "from_agent": "quality-controller",
            "to_agent": "code-analyzer"
            # Missing required fields
        }

        result = feedback_system.add_feedback(**incomplete_feedback)
        assert result is False

    def test_get_feedback_for_agent(self, feedback_system, sample_feedback):
        """Test retrieving feedback for a specific agent"""
        # Add feedback
        feedback_system.add_feedback(**sample_feedback)

        # Get feedback for the target agent
        feedback_list = feedback_system.get_feedback_for_agent(
            "code-analyzer",
            days=7
        )

        assert isinstance(feedback_list, list)
        assert len(feedback_list) >= 1

        # Check the feedback contains expected data
        feedback = feedback_list[0]
        assert feedback['from_agent'] == "quality-controller"
        assert feedback['to_agent'] == "code-analyzer"

    def test_get_feedback_insights(self, feedback_system):
        """Test generating feedback insights"""
        # Add multiple feedback entries
        feedback_entries = [
            {
                "from_agent": "quality-controller",
                "to_agent": "code-analyzer",
                "task_id": "task_1",
                "feedback_type": "success",
                "message": "Good recommendations",
                "impact": "quality_score +10"
            },
            {
                "from_agent": "test-engineer",
                "to_agent": "code-analyzer",
                "task_id": "task_2",
                "feedback_type": "improvement",
                "message": "Consider edge cases",
                "impact": "analysis_depth +1"
            }
        ]

        for feedback in feedback_entries:
            feedback_system.add_feedback(**feedback)

        # Get insights
        insights = feedback_system.get_feedback_insights("code-analyzer", days=7)

        assert isinstance(insights, dict)
        assert 'total_feedback' in insights
        assert 'feedback_types' in insights
        assert 'collaboration_matrix' in insights

    def test_collaboration_effectiveness(self, feedback_system):
        """Test collaboration effectiveness calculation"""
        # Add collaborative feedback
        feedback_system.add_feedback(
            from_agent="code-analyzer",
            to_agent="quality-controller",
            task_id="task_1",
            feedback_type="success",
            message="Found all issues",
            impact="comprehensive_analysis"
        )

        feedback_system.add_feedback(
            from_agent="quality-controller",
            to_agent="code-analyzer",
            task_id="task_1",
            feedback_type="success",
            message="Recommendations were accurate",
            impact="precision +15%"
        )

        # Get collaboration effectiveness
        effectiveness = feedback_system.get_collaboration_effectiveness(days=7)

        assert isinstance(effectiveness, dict)
        assert 'top_collaborations' in effectiveness
        assert 'effectiveness_score' in effectiveness

    def test_feedback_persistence(self, feedback_system, sample_feedback):
        """Test that feedback persists across system instances"""
        # Add feedback
        feedback_system.add_feedback(**sample_feedback)

        # Create new instance with same data directory
        new_system = AgentFeedbackSystem(storage_dir=feedback_system.data_dir)

        # Check feedback is available
        feedback_list = new_system.get_feedback_for_agent(
            sample_feedback['to_agent'],
            days=7
        )

        assert len(feedback_list) >= 1
        assert feedback_list[0]['task_id'] == sample_feedback['task_id']

    def test_feedback_file_creation(self, temp_directory, sample_feedback):
        """Test that feedback file is created correctly"""
        feedback_system = AgentFeedbackSystem(storage_dir=temp_directory)

        # Add feedback
        feedback_system.add_feedback(**sample_feedback)

        # Check file exists
        feedback_file = os.path.join(temp_directory, 'agent_feedback.json')
        assert os.path.exists(feedback_file)

        # Check file content
        with open(feedback_file, 'r') as f:
            data = json.load(f)

        assert 'feedback_history' in data
        assert len(data['feedback_history']) > 0

    def test_feedback_timestamps(self, feedback_system):
        """Test that feedback timestamps are recorded correctly"""
        before_time = datetime.now(timezone.utc).isoformat()

        feedback_system.add_feedback(
            from_agent="agent1",
            to_agent="agent2",
            task_id="test_task",
            feedback_type="success",
            message="Test message",
            impact="test_impact"
        )

        after_time = datetime.now(timezone.utc).isoformat()

        # Get the feedback
        feedback_list = feedback_system.get_feedback_for_agent("agent2", days=1)
        assert len(feedback_list) == 1

        feedback = feedback_list[0]
        assert 'timestamp' in feedback

        # Check timestamp is within expected range
        feedback_time = feedback['timestamp']
        assert before_time <= feedback_time <= after_time

    def test_feedback_validation(self, feedback_system):
        """Test feedback data validation"""
        # Test with None values
        result = feedback_system.add_feedback(
            from_agent=None,
            to_agent="agent2",
            task_id="test",
            feedback_type="success",
            message="test",
            impact="test"
        )
        assert result is False

        # Test with empty strings
        result = feedback_system.add_feedback(
            from_agent="",
            to_agent="agent2",
            task_id="test",
            feedback_type="success",
            message="test",
            impact="test"
        )
        assert result is False

    def test_feedback_filtering(self, feedback_system):
        """Test filtering feedback by agent and time"""
        # Add feedback at different times
        base_time = datetime.now(timezone.utc)

        feedback_entries = [
            {
                "from_agent": "agent1",
                "to_agent": "agent2",
                "task_id": f"task_{i}",
                "feedback_type": "success",
                "message": f"Message {i}",
                "impact": f"impact_{i}"
            }
            for i in range(3)
        ]

        for i, feedback in enumerate(feedback_entries):
            feedback_system.add_feedback(**feedback)
            # Small delay to ensure different timestamps
            time.sleep(0.01)

        # Test filtering by days
        recent_feedback = feedback_system.get_feedback_for_agent("agent2", days=0)
        assert len(recent_feedback) == 3

        # Test filtering by from_agent
        agent_specific = feedback_system.get_feedback_for_agent(
            "agent2",
            days=7,
            from_agent="agent1"
        )
        assert len(agent_specific) == 3

    def test_error_handling(self, feedback_system):
        """Test error handling in various scenarios"""
        # Test with corrupted data file
        feedback_file = feedback_system.feedback_file

        # Create corrupted JSON file
        with open(feedback_file, 'w') as f:
            f.write("invalid json content")

        # Should handle gracefully
        feedback_list = feedback_system.get_feedback_for_agent("agent2", days=7)
        assert isinstance(feedback_list, list)

    def test_performance_metrics(self, feedback_system):
        """Test performance-related metrics"""
        # Add performance-related feedback
        performance_feedback = {
            "from_agent": "performance-analytics",
            "to_agent": "code-analyzer",
            "task_id": "perf_task",
            "feedback_type": "improvement",
            "message": "Analysis took 5 minutes, consider optimization",
            "impact": "execution_time +30%"
        }

        feedback_system.add_feedback(**performance_feedback)

        # Get performance insights
        insights = feedback_system.get_performance_insights(days=7)

        assert isinstance(insights, dict)
        assert 'performance_feedback' in insights

    def test_learning_effectiveness(self, feedback_system):
        """Test learning effectiveness tracking"""
        # Add feedback showing learning improvement
        learning_feedback = [
            {
                "from_agent": "learning-engine",
                "to_agent": "code-analyzer",
                "task_id": f"learning_task_{i}",
                "feedback_type": "success",
                "message": f"Pattern recognition improved by {i*5}%",
                "impact": f"learning_velocity +{i*5}%"
            }
            for i in range(1, 4)
        ]

        for feedback in learning_feedback:
            feedback_system.add_feedback(**feedback)

        # Get learning effectiveness
        effectiveness = feedback_system.get_learning_effectiveness(days=7)

        assert isinstance(effectiveness, dict)
        assert 'improvement_trend' in effectiveness
        assert 'learning_velocity' in effectiveness