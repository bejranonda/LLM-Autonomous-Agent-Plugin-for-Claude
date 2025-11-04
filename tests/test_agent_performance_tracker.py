"""
Tests for Agent Performance Tracker (lib/agent_performance_tracker.py)

Tests the individual agent performance tracking system that identifies
specializations and monitors agent effectiveness over time.
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
    from agent_performance_tracker import AgentPerformanceTracker
except ImportError:
    pytest.skip("agent_performance_tracker.py not available", allow_module_level=True)


class TestAgentPerformanceTracker:
    """Test cases for Agent Performance Tracker"""

    @pytest.fixture
    def performance_tracker(self, temp_directory):
        """Create an AgentPerformanceTracker instance for testing"""
        return AgentPerformanceTracker(data_dir=temp_directory)

    @pytest.fixture
    def sample_performance_data(self):
        """Sample performance data for testing"""
        return {
            "agent_name": "code-analyzer",
            "task_id": "task_456",
            "task_type": "refactoring",
            "success": True,
            "quality_score": 94.0,
            "execution_time_seconds": 120,
            "iterations": 1
        }

    def test_initialization(self, performance_tracker):
        """Test system initialization"""
        assert performance_tracker is not None
        assert hasattr(performance_tracker, 'data_dir')
        assert hasattr(performance_tracker, 'performance_file')

    def test_record_task_execution(self, performance_tracker, sample_performance_data):
        """Test recording task execution"""
        result = performance_tracker.record_task_execution(**sample_performance_data)

        assert result is True

    def test_record_invalid_data(self, performance_tracker):
        """Test recording invalid performance data"""
        invalid_data = {
            "agent_name": "",  # Invalid empty name
            "task_id": "test",
            "task_type": "test",
            "success": True,
            "quality_score": 95.0,
            "execution_time_seconds": 60,
            "iterations": 1
        }

        result = performance_tracker.record_task_execution(**invalid_data)
        assert result is False

    def test_get_agent_performance(self, performance_tracker, sample_performance_data):
        """Test retrieving agent performance data"""
        # Record task execution
        performance_tracker.record_task_execution(**sample_performance_data)

        # Get performance data
        performance = performance_tracker.get_agent_performance(
            sample_performance_data['agent_name']
        )

        assert isinstance(performance, dict)
        assert 'success_rate' in performance
        assert 'average_quality_score' in performance
        assert 'total_tasks' in performance

    def test_get_top_performers(self, performance_tracker):
        """Test getting top performing agents"""
        # Add performance data for multiple agents
        agents_data = [
            {
                "agent_name": "code-analyzer",
                "task_id": "task_1",
                "task_type": "refactoring",
                "success": True,
                "quality_score": 94.0,
                "execution_time_seconds": 120,
                "iterations": 1
            },
            {
                "agent_name": "test-engineer",
                "task_id": "task_2",
                "task_type": "testing",
                "success": True,
                "quality_score": 98.0,
                "execution_time_seconds": 90,
                "iterations": 1
            },
            {
                "agent_name": "quality-controller",
                "task_id": "task_3",
                "task_type": "quality_control",
                "success": False,
                "quality_score": 75.0,
                "execution_time_seconds": 180,
                "iterations": 2
            }
        ]

        for data in agents_data:
            performance_tracker.record_task_execution(**data)

        # Get top performers
        top_performers = performance_tracker.get_top_performers(limit=3)

        assert isinstance(top_performers, list)
        assert len(top_performers) <= 3

        # Check structure of performer data
        if top_performers:
            performer = top_performers[0]
            assert 'agent_name' in performer
            assert 'performance_score' in performer
            assert 'success_rate' in performer

    def test_performance_trends(self, performance_tracker):
        """Test performance trend analysis"""
        agent_name = "test-agent"

        # Add performance data over time
        for i in range(5):
            performance_data = {
                "agent_name": agent_name,
                "task_id": f"task_{i}",
                "task_type": "test",
                "success": True,
                "quality_score": 80.0 + (i * 2),  # Improving scores
                "execution_time_seconds": 100 - (i * 5),  # Improving speed
                "iterations": 1
            }
            performance_tracker.record_task_execution(**performance_data)
            time.sleep(0.01)  # Small delay for timestamps

        # Get trends
        trends = performance_tracker.get_performance_trends(agent_name, days=7)

        assert isinstance(trends, dict)
        assert 'quality_trend' in trends
        assert 'speed_trend' in trends
        assert 'trend_direction' in trends

    def test_agent_specialization(self, performance_tracker):
        """Test agent specialization identification"""
        agent_name = "code-analyzer"

        # Add performance data for different task types
        task_types = [
            ("refactoring", 95.0, True),
            ("refactoring", 92.0, True),
            ("bug_fix", 88.0, True),
            ("bug_fix", 90.0, True),
            ("documentation", 75.0, False),
            ("documentation", 78.0, True)
        ]

        for task_type, quality_score, success in task_types:
            performance_data = {
                "agent_name": agent_name,
                "task_id": f"task_{task_type}_{quality_score}",
                "task_type": task_type,
                "success": success,
                "quality_score": quality_score,
                "execution_time_seconds": 120,
                "iterations": 1
            }
            performance_tracker.record_task_execution(**performance_data)

        # Get specializations
        specializations = performance_tracker.get_agent_specializations(agent_name)

        assert isinstance(specializations, dict)
        assert 'primary_specialization' in specializations
        assert 'specialization_scores' in specializations

    def test_performance_rating(self, performance_tracker):
        """Test performance rating calculation"""
        # Test different performance levels
        test_cases = [
            ("excellent_agent", 95.0, 100),  # Should be Excellent
            ("good_agent", 85.0, 100),       # Should be Good
            ("satisfactory_agent", 75.0, 100),  # Should be Satisfactory
            ("needs_improvement_agent", 65.0, 100),  # Should be Needs Improvement
            ("poor_agent", 55.0, 100),      # Should be Poor
        ]

        for agent_name, quality_score, success_rate in test_cases:
            # Add multiple tasks to establish performance
            for i in range(10):
                success = i < (success_rate // 10)  # Simulate success rate
                performance_data = {
                    "agent_name": agent_name,
                    "task_id": f"task_{i}",
                    "task_type": "test",
                    "success": success,
                    "quality_score": quality_score,
                    "execution_time_seconds": 100,
                    "iterations": 1
                }
                performance_tracker.record_task_execution(**performance_data)

            # Get performance rating
            rating = performance_tracker.get_performance_rating(agent_name)
            assert isinstance(rating, dict)
            assert 'rating' in rating
            assert 'score' in rating

    def test_weak_performer_detection(self, performance_tracker):
        """Test detection of weak performing agents"""
        # Add data for a weak performer
        weak_agent = "weak-agent"
        for i in range(10):
            performance_data = {
                "agent_name": weak_agent,
                "task_id": f"task_{i}",
                "task_type": "test",
                "success": i < 3,  # 30% success rate
                "quality_score": 60.0,  # Low quality scores
                "execution_time_seconds": 200,  # Slow execution
                "iterations": 3  # Multiple iterations
            }
            performance_tracker.record_task_execution(**performance_data)

        # Get weak performers
        weak_performers = performance_tracker.get_weak_performers()

        assert isinstance(weak_performers, list)
        # Should identify the weak agent
        weak_agent_names = [p['agent_name'] for p in weak_performers]
        assert weak_agent in weak_agent_names

    def test_performance_persistence(self, performance_tracker, sample_performance_data):
        """Test that performance data persists across instances"""
        # Record performance
        performance_tracker.record_task_execution(**sample_performance_data)

        # Create new instance with same data directory
        new_tracker = AgentPerformanceTracker(data_dir=performance_tracker.data_dir)

        # Check data is available
        performance = new_tracker.get_agent_performance(
            sample_performance_data['agent_name']
        )

        assert performance['total_tasks'] >= 1

    def test_file_creation_and_format(self, temp_directory, sample_performance_data):
        """Test that performance file is created correctly"""
        tracker = AgentPerformanceTracker(data_dir=temp_directory)

        # Record performance
        tracker.record_task_execution(**sample_performance_data)

        # Check file exists
        performance_file = os.path.join(temp_directory, 'agent_performance.json')
        assert os.path.exists(performance_file)

        # Check file content
        with open(performance_file, 'r') as f:
            data = json.load(f)

        assert 'performance_history' in data
        assert 'agent_summaries' in data
        assert len(data['performance_history']) > 0

    def test_performance_metrics_calculation(self, performance_tracker):
        """Test calculation of various performance metrics"""
        agent_name = "metrics-agent"

        # Add varied performance data
        scores = [95, 88, 92, 78, 96, 85, 90, 93, 87, 91]
        times = [120, 150, 100, 180, 90, 110, 130, 105, 140, 95]
        successes = [True, True, False, True, True, True, False, True, True, True]

        for i, (score, time, success) in enumerate(zip(scores, times, successes)):
            performance_data = {
                "agent_name": agent_name,
                "task_id": f"task_{i}",
                "task_type": "test",
                "success": success,
                "quality_score": float(score),
                "execution_time_seconds": time,
                "iterations": 1 if success else 2
            }
            performance_tracker.record_task_execution(**performance_data)

        # Get comprehensive performance metrics
        metrics = performance_tracker.get_comprehensive_metrics(agent_name)

        assert isinstance(metrics, dict)
        assert 'success_rate' in metrics
        assert 'average_quality_score' in metrics
        assert 'average_execution_time' in metrics
        assert 'total_tasks' in metrics
        assert 'performance_consistency' in metrics

        # Validate calculations
        expected_success_rate = sum(successes) / len(successes)
        assert abs(metrics['success_rate'] - expected_success_rate) < 0.01

        expected_avg_score = sum(scores) / len(scores)
        assert abs(metrics['average_quality_score'] - expected_avg_score) < 0.01

    def test_task_type_performance_analysis(self, performance_tracker):
        """Test performance analysis by task type"""
        agent_name = "multi-task-agent"

        # Add data for different task types
        task_data = [
            ("refactoring", [95, 92, 88]),
            ("testing", [98, 96, 94]),
            ("documentation", [85, 87, 83]),
            ("security_audit", [92, 94, 90])
        ]

        for task_type, scores in task_data:
            for score in scores:
                performance_data = {
                    "agent_name": agent_name,
                    "task_id": f"task_{task_type}_{score}",
                    "task_type": task_type,
                    "success": True,
                    "quality_score": float(score),
                    "execution_time_seconds": 120,
                    "iterations": 1
                }
                performance_tracker.record_task_execution(**performance_data)

        # Get task type analysis
        analysis = performance_tracker.get_task_type_performance(agent_name)

        assert isinstance(analysis, dict)
        assert 'task_type_performance' in analysis
        assert 'best_task_type' in analysis
        assert 'performance_by_type' in analysis

    def test_error_handling(self, performance_tracker):
        """Test error handling in various scenarios"""
        # Test with corrupted data file
        performance_file = performance_tracker.performance_file

        # Create corrupted JSON file
        with open(performance_file, 'w') as f:
            f.write("invalid json content")

        # Should handle gracefully
        performance = performance_tracker.get_agent_performance("test-agent")
        assert isinstance(performance, dict)

    def test_concurrent_access(self, performance_tracker):
        """Test handling of concurrent access"""
        # This is a basic test - in real scenarios, file locking would be tested
        agent_name = "concurrent-agent"

        # Record multiple tasks rapidly
        for i in range(10):
            performance_data = {
                "agent_name": agent_name,
                "task_id": f"concurrent_task_{i}",
                "task_type": "test",
                "success": True,
                "quality_score": 90.0,
                "execution_time_seconds": 100,
                "iterations": 1
            }
            result = performance_tracker.record_task_execution(**performance_data)
            assert result is True

        # Verify all tasks were recorded
        performance = performance_tracker.get_agent_performance(agent_name)
        assert performance['total_tasks'] == 10