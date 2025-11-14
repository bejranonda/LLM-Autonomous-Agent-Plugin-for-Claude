"""
Tests for Learning Visualizer (lib/learning_visualizer.py)

Tests the real-time learning feedback and visualization system
that provides transparent decision-making explanations.
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
    from learning_visualizer import LearningVisualizer
except ImportError:
    pytest.skip("learning_visualizer.py not available", allow_module_level=True)


class TestLearningVisualizer:
    """Test cases for Learning Visualizer"""

    @pytest.fixture
    def learning_visualizer(self, temp_directory):
        """Create a LearningVisualizer instance for testing"""
        return LearningVisualizer(storage_dir=temp_directory)

    @pytest.fixture
    def sample_learning_event(self):
        """Sample learning event data"""
        return {
            "event_type": "skill_selection",
            "description": "Selected code-analysis skill for refactoring task",
            "impact": "Improved prediction accuracy by 3%",
            "data": {
                "skill": "code-analysis",
                "confidence": 0.92,
                "task_type": "refactoring",
                "selected_over": ["quality-standards", "pattern-learning"]
            },
            "confidence": 0.92
        }

    def test_initialization(self, learning_visualizer):
        """Test system initialization"""
        assert learning_visualizer is not None
        assert hasattr(learning_visualizer, 'data_dir')
        assert hasattr(learning_visualizer, 'events_file')

    def test_record_learning_event(self, learning_visualizer, sample_learning_event):
        """Test recording a learning event"""
        result = learning_visualizer.record_learning_event(**sample_learning_event)

        assert result is True

    def test_record_invalid_event(self, learning_visualizer):
        """Test recording invalid learning event"""
        invalid_event = {
            "event_type": "",  # Invalid empty type
            "description": "test",
            "impact": "test",
            "data": {},
            "confidence": 0.5
        }

        result = learning_visualizer.record_learning_event(**invalid_event)
        assert result is False

    def test_get_learning_events(self, learning_visualizer, sample_learning_event):
        """Test retrieving learning events"""
        # Record event
        learning_visualizer.record_learning_event(**sample_learning_event)

        # Get events
        events = learning_visualizer.get_learning_events(days=7)

        assert isinstance(events, list)
        assert len(events) >= 1

        # Check event structure
        event = events[0]
        assert 'event_type' in event
        assert 'timestamp' in event
        assert 'description' in event
        assert 'confidence' in event

    def test_get_events_by_type(self, learning_visualizer):
        """Test retrieving events by type"""
        event_types = [
            {"event_type": "skill_selection", "description": "Selected skill"},
            {"event_type": "agent_routing", "description": "Routed to agent"},
            {"event_type": "quality_assessment", "description": "Assessed quality"},
            {"event_type": "pattern_learning", "description": "Learned pattern"}
        ]

        # Record different event types
        for event in event_types:
            full_event = {
                **event,
                "impact": "test impact",
                "data": {},
                "confidence": 0.8
            }
            learning_visualizer.record_learning_event(**full_event)

        # Get events by specific type
        skill_events = learning_visualizer.get_events_by_type("skill_selection", days=7)
        assert isinstance(skill_events, list)
        assert all(event['event_type'] == "skill_selection" for event in skill_events)

    def test_generate_learning_insights(self, learning_visualizer):
        """Test generation of learning insights"""
        # Record various learning events
        events = [
            {
                "event_type": "skill_selection",
                "description": f"Skill selection event {i}",
                "impact": f"Improved accuracy by {i}%",
                "data": {"skill": f"skill_{i}"},
                "confidence": 0.8 + (i * 0.02)
            }
            for i in range(5)
        ]

        for event in events:
            learning_visualizer.record_learning_event(**event)

        # Generate insights
        insights = learning_visualizer.generate_learning_insights(days=7)

        assert isinstance(insights, dict)
        assert 'total_events' in insights
        assert 'event_types' in insights
        assert 'confidence_trends' in insights
        assert 'learning_velocity' in insights

    def test_decision_explanation(self, learning_visualizer):
        """Test decision explanation generation"""
        decision_data = {
            "decision_type": "skill_selection",
            "selected_option": "code-analysis",
            "alternatives": ["quality-standards", "pattern-learning"],
            "confidence": 0.92,
            "factors": {
                "historical_success": 0.85,
                "task_similarity": 0.90,
                "user_preference": 0.95
            },
            "context": {
                "task_type": "refactoring",
                "language": "python",
                "complexity": "medium"
            }
        }

        explanation = learning_visualizer.generate_decision_explanation(decision_data)

        assert isinstance(explanation, dict)
        assert 'decision' in explanation
        assert 'reasoning' in explanation
        assert 'confidence_breakdown' in explanation
        assert 'alternatives_considered' in explanation

    def test_learning_progress_visualization(self, learning_visualizer):
        """Test learning progress visualization data"""
        # Record progress events
        for i in range(10):
            event = {
                "event_type": "learning_milestone",
                "description": f"Milestone {i+1} reached",
                "impact": f"Improved performance by {i*2}%",
                "data": {
                    "milestone_number": i + 1,
                    "performance_metric": 75 + i * 2.5
                },
                "confidence": 0.7 + (i * 0.03)
            }
            learning_visualizer.record_learning_event(**event)

        # Get visualization data
        viz_data = learning_visualizer.get_learning_progress_data(days=7)

        assert isinstance(viz_data, dict)
        assert 'timeline' in viz_data
        assert 'performance_trend' in viz_data
        assert 'confidence_evolution' in viz_data

    def test_agent_performance_visualization(self, learning_visualizer):
        """Test agent performance visualization data"""
        # Record agent performance events
        agents = ["code-analyzer", "quality-controller", "test-engineer"]
        for agent in agents:
            for i in range(5):
                event = {
                    "event_type": "agent_performance",
                    "description": f"{agent} performance update",
                    "impact": f"Score: {85 + i}",
                    "data": {
                        "agent_name": agent,
                        "performance_score": 85 + i,
                        "task_type": "test_task"
                    },
                    "confidence": 0.8 + (i * 0.02)
                }
                learning_visualizer.record_learning_event(**event)

        # Get agent performance data
        agent_data = learning_visualizer.get_agent_performance_data(days=7)

        assert isinstance(agent_data, dict)
        assert 'agent_rankings' in agent_data
        assert 'performance_trends' in agent_data
        assert 'specialization_effectiveness' in agent_data

    def test_skill_effectiveness_visualization(self, learning_visualizer):
        """Test skill effectiveness visualization data"""
        # Record skill effectiveness events
        skills = ["code-analysis", "quality-standards", "testing-strategies"]
        for skill in skills:
            for i in range(3):
                event = {
                    "event_type": "skill_effectiveness",
                    "description": f"{skill} effectiveness update",
                    "impact": f"Success rate: {0.8 + i * 0.05}",
                    "data": {
                        "skill_name": skill,
                        "success_rate": 0.8 + i * 0.05,
                        "average_quality": 88 + i * 2
                    },
                    "confidence": 0.85
                }
                learning_visualizer.record_learning_event(**event)

        # Get skill effectiveness data
        skill_data = learning_visualizer.get_skill_effectiveness_data(days=7)

        assert isinstance(skill_data, dict)
        assert 'skill_rankings' in skill_data
        assert 'effectiveness_trends' in skill_data
        assert 'usage_patterns' in skill_data

    def test_real_time_learning_dashboard(self, learning_visualizer):
        """Test real-time learning dashboard data"""
        # Record recent events
        current_time = datetime.now(timezone.utc)
        for i in range(20):
            event = {
                "event_type": ["skill_selection", "agent_routing", "quality_assessment"][i % 3],
                "description": f"Recent event {i+1}",
                "impact": f"Impact {i+1}",
                "data": {"event_id": i + 1},
                "confidence": 0.7 + (i % 5) * 0.05
            }
            learning_visualizer.record_learning_event(**event)

        # Get dashboard data
        dashboard_data = learning_visualizer.get_dashboard_data(hours=24)

        assert isinstance(dashboard_data, dict)
        assert 'recent_events' in dashboard_data
        assert 'learning_metrics' in dashboard_data
        assert 'active_agents' in dashboard_data
        assert 'top_skills' in dashboard_data

    def test_learning_analytics(self, learning_visualizer):
        """Test comprehensive learning analytics"""
        # Record diverse learning events
        event_categories = [
            ("skill_selection", 10),
            ("agent_routing", 8),
            ("quality_assessment", 6),
            ("pattern_learning", 12),
            ("user_adaptation", 4)
        ]

        for category, count in event_categories:
            for i in range(count):
                event = {
                    "event_type": category,
                    "description": f"{category} event {i+1}",
                    "impact": f"Impact {i+1}",
                    "data": {"category": category, "index": i + 1},
                    "confidence": 0.7 + (i % 5) * 0.05
                }
                learning_visualizer.record_learning_event(**event)

        # Get comprehensive analytics
        analytics = learning_visualizer.get_comprehensive_analytics(days=7)

        assert isinstance(analytics, dict)
        assert 'overview' in analytics
        assert 'event_analysis' in analytics
        assert 'performance_trends' in analytics
        assert 'learning_patterns' in analytics
        assert 'recommendations' in analytics

    def test_export_learning_data(self, learning_visualizer, sample_learning_event):
        """Test exporting learning data"""
        # Record event
        learning_visualizer.record_learning_event(**sample_learning_event)

        # Export data
        export_file = os.path.join(learning_visualizer.data_dir, "exported_learning.json")
        result = learning_visualizer.export_learning_data(export_file, days=7)

        assert result is True
        assert os.path.exists(export_file)

        # Verify exported data
        with open(export_file, 'r') as f:
            exported_data = json.load(f)

        assert 'events' in exported_data
        assert 'metadata' in exported_data
        assert len(exported_data['events']) > 0

    def test_learning_event_persistence(self, learning_visualizer, sample_learning_event):
        """Test that learning events persist across instances"""
        # Record event
        learning_visualizer.record_learning_event(**sample_learning_event)

        # Create new instance with same data directory
        new_visualizer = LearningVisualizer(storage_dir=learning_visualizer.data_dir)

        # Check events are available
        events = new_visualizer.get_learning_events(days=7)

        assert len(events) >= 1
        assert events[0]['event_type'] == sample_learning_event['event_type']

    def test_file_creation_and_format(self, temp_directory, sample_learning_event):
        """Test that events file is created correctly"""
        visualizer = LearningVisualizer(storage_dir=temp_directory)

        # Record event to trigger file creation
        visualizer.record_learning_event(**sample_learning_event)

        # Check file exists
        events_file = os.path.join(temp_directory, 'learning_events.json')
        assert os.path.exists(events_file)

        # Check file content
        with open(events_file, 'r') as f:
            data = json.load(f)

        assert 'events' in data
        assert 'metadata' in data
        assert len(data['events']) > 0

        # Check event structure
        event = data['events'][0]
        required_fields = ['event_type', 'timestamp', 'description', 'impact', 'data', 'confidence']
        for field in required_fields:
            assert field in event

    def test_confidence_tracking(self, learning_visualizer):
        """Test confidence tracking over time"""
        # Record events with varying confidence
        confidence_values = [0.7, 0.75, 0.82, 0.88, 0.91, 0.93, 0.95]

        for i, confidence in enumerate(confidence_values):
            event = {
                "event_type": "confidence_test",
                "description": f"Confidence test {i+1}",
                "impact": f"Confidence: {confidence}",
                "data": {"confidence_level": confidence},
                "confidence": confidence
            }
            learning_visualizer.record_learning_event(**event)

        # Get confidence trends
        trends = learning_visualizer.get_confidence_trends(days=7)

        assert isinstance(trends, dict)
        assert 'average_confidence' in trends
        assert 'confidence_progression' in trends
        assert 'improvement_rate' in trends

    def test_event_filtering(self, learning_visualizer):
        """Test filtering of learning events"""
        # Record events with different attributes
        event_types = ["skill_selection", "agent_routing", "quality_assessment"]
        confidences = [0.7, 0.8, 0.9]

        for i, event_type in enumerate(event_types):
            for j, confidence in enumerate(confidences):
                event = {
                    "event_type": event_type,
                    "description": f"{event_type} event {j+1}",
                    "impact": f"Impact {j+1}",
                    "data": {"index": j + 1},
                    "confidence": confidence
                }
                learning_visualizer.record_learning_event(**event)

        # Test filtering by confidence
        high_confidence_events = learning_visualizer.get_learning_events(
            days=7,
            min_confidence=0.85
        )
        assert all(event['confidence'] >= 0.85 for event in high_confidence_events)

        # Test filtering by event type
        skill_events = learning_visualizer.get_events_by_type("skill_selection", days=7)
        assert all(event['event_type'] == "skill_selection" for event in skill_events)

    def test_performance_metrics(self, learning_visualizer):
        """Test performance metrics for the visualizer"""
        # Record some events
        for i in range(10):
            event = {
                "event_type": "performance_test",
                "description": f"Performance test {i+1}",
                "impact": f"Impact {i+1}",
                "data": {"test_id": i + 1},
                "confidence": 0.8
            }
            learning_visualizer.record_learning_event(**event)

        # Get performance metrics
        metrics = learning_visualizer.get_performance_metrics(days=7)

        assert isinstance(metrics, dict)
        assert 'total_events' in metrics
        assert 'storage_usage' in metrics
        assert 'processing_speed' in metrics

    def test_error_handling(self, learning_visualizer):
        """Test error handling in various scenarios"""
        # Test with corrupted data file
        events_file = learning_visualizer.events_file

        # Create corrupted JSON file
        with open(events_file, 'w') as f:
            f.write("invalid json content")

        # Should handle gracefully
        events = learning_visualizer.get_learning_events(days=7)
        assert isinstance(events, list)

        # Test with invalid event data
        invalid_event = {
            "event_type": None,  # Invalid
            "description": "test",
            "impact": "test",
            "data": {},
            "confidence": "invalid"  # Invalid type
        }

        result = learning_visualizer.record_learning_event(**invalid_event)
        assert result is False

    def test_learning_summary_generation(self, learning_visualizer):
        """Test generation of learning summaries"""
        # Record diverse learning events
        event_types = [
            ("skill_selection", "Selected optimal skill for task"),
            ("agent_routing", "Routed task to best agent"),
            ("quality_improvement", "Improved quality score"),
            ("pattern_learning", "Learned new pattern"),
            ("user_adaptation", "Adapted to user preference")
        ]

        for event_type, description in event_types:
            event = {
                "event_type": event_type,
                "description": description,
                "impact": "Positive learning outcome",
                "data": {"category": event_type},
                "confidence": 0.85
            }
            learning_visualizer.record_learning_event(**event)

        # Generate summary
        summary = learning_visualizer.generate_learning_summary(days=7)

        assert isinstance(summary, dict)
        assert 'overview' in summary
        assert 'key_achievements' in summary
        assert 'learning_areas' in summary
        assert 'recommendations' in summary
        assert 'next_steps' in summary