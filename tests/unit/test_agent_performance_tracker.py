#!/usr/bin/env python3
"""
Test suite for agent_performance_tracker.py
Boosts test coverage by focusing on performance tracking and analytics.
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
from datetime import datetime, timedelta

# Add the lib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from agent_performance_tracker import AgentPerformanceTracker


class TestAgentPerformanceTracker:
    """Test cases for AgentPerformanceTracker class."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = AgentPerformanceTracker(self.temp_dir)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test AgentPerformanceTracker initialization."""
        # Test with default directory
        tracker = AgentPerformanceTracker()
        assert tracker.storage_dir.exists()
        assert tracker.performance_file.exists()

        # Test with custom directory
        custom_dir = Path(self.temp_dir) / "custom"
        tracker = AgentPerformanceTracker(str(custom_dir))
        assert custom_dir.exists()
        assert tracker.performance_file.exists()

        # Check initial structure
        with open(tracker.performance_file) as f:
            data = json.load(f)
            assert "version" in data
            assert "metadata" in data
            assert "agent_metrics" in data
            assert "task_history" in data

    def test_record_task_execution(self):
        """Test recording a task execution."""
        self.tracker.record_task_execution(
            agent_name="test_agent",
            task_id="task_001",
            task_type="refactoring",
            success=True,
            quality_score=85.5,
            execution_time_seconds=120.0,
            iterations=1
        )

        # Verify task was recorded
        agent_perf = self.tracker.get_agent_performance("test_agent")
        assert agent_perf["total_tasks"] == 1
        assert agent_perf["successful_tasks"] == 1
        assert agent_perf["failed_tasks"] == 0
        assert agent_perf["average_quality_score"] == 85.5
        assert agent_perf["success_rate"] == 1.0
        assert agent_perf["average_execution_time"] == 120.0

    def test_record_multiple_tasks(self):
        """Test recording multiple tasks for the same agent."""
        tasks = [
            ("task_001", "refactoring", True, 85.0, 120.0),
            ("task_002", "testing", True, 90.0, 180.0),
            ("task_003", "documentation", False, 75.0, 60.0),
            ("task_004", "refactoring", True, 88.0, 150.0)
        ]

        for task_id, task_type, success, quality, time in tasks:
            self.tracker.record_task_execution(
                agent_name="test_agent",
                task_id=task_id,
                task_type=task_type,
                success=success,
                quality_score=quality,
                execution_time_seconds=time,
                iterations=1
            )

        perf = self.tracker.get_agent_performance("test_agent")
        assert perf["total_tasks"] == 4
        assert perf["successful_tasks"] == 3
        assert perf["failed_tasks"] == 1
        assert perf["success_rate"] == 0.75
        assert abs(perf["average_quality_score"] - ((85 + 90 + 75 + 88) / 4)) < 0.1
        assert abs(perf["average_execution_time"] - ((120 + 180 + 60 + 150) / 4)) < 0.1

    def test_record_task_with_context(self):
        """Test recording task with additional context."""
        context = {
            "files_modified": ["test.py", "utils.py"],
            "lines_changed": 150,
            "complexity": "high"
        }

        self.tracker.record_task_execution(
            agent_name="test_agent",
            task_id="task_001",
            task_type="refactoring",
            success=True,
            quality_score=85.0,
            execution_time_seconds=120.0,
            context=context
        )

        # Verify context is stored
        data = self.tracker._read_data()
        task_history = data["task_history"]
        assert len(task_history) == 1
        assert task_history[0]["context"] == context

    def test_record_task_with_recommendations(self):
        """Test recording task with recommendations followed."""
        self.tracker.record_task_execution(
            agent_name="analysis_agent",
            task_id="task_001",
            task_type="code_analysis",
            success=True,
            quality_score=90.0,
            execution_time_seconds=60.0,
            recommendations_followed=5
        )

        perf = self.tracker.get_agent_performance("analysis_agent")
        assert perf["recommendations_followed_total"] == 5

    def test_record_task_with_auto_fix(self):
        """Test recording task with auto-fix applied."""
        self.tracker.record_task_execution(
            agent_name="execution_agent",
            task_id="task_001",
            task_type="quality_control",
            success=True,
            quality_score=88.0,
            execution_time_seconds=90.0,
            auto_fix_applied=True
        )

        perf = self.tracker.get_agent_performance("execution_agent")
        assert perf["auto_fixes_applied"] == 1

    def test_get_agent_performance_nonexistent(self):
        """Test getting performance for non-existent agent."""
        perf = self.tracker.get_agent_performance("nonexistent_agent")
        assert perf["agent_name"] == "nonexistent_agent"
        assert perf["total_tasks"] == 0
        assert "No data available" in perf["performance"]

    def test_get_all_agent_performances(self):
        """Test getting performance for all agents."""
        # Add tasks for multiple agents
        agents_tasks = [
            ("agent1", "task_001", "refactoring", True, 85.0),
            ("agent1", "task_002", "testing", True, 90.0),
            ("agent2", "task_003", "documentation", True, 80.0),
            ("agent3", "task_004", "bug_fix", False, 70.0)
        ]

        for agent, task_id, task_type, success, quality in agents_tasks:
            self.tracker.record_task_execution(
                agent_name=agent,
                task_id=task_id,
                task_type=task_type,
                success=success,
                quality_score=quality,
                execution_time_seconds=100.0
            )

        all_perfs = self.tracker.get_all_agent_performances()
        assert len(all_perfs) == 3
        assert "agent1" in all_perfs
        assert "agent2" in all_perfs
        assert "agent3" in all_perfs

        # Check agent1 has 2 tasks
        assert all_perfs["agent1"]["total_tasks"] == 2

    def test_get_top_performers(self):
        """Test getting top performing agents."""
        # Create agents with different performance levels
        agents_data = [
            ("excellent_agent", 95.0, 1.0, 50.0),
            ("good_agent", 85.0, 0.9, 80.0),
            ("average_agent", 75.0, 0.8, 120.0),
            ("poor_agent", 65.0, 0.6, 200.0)
        ]

        for agent, quality, success_rate, time in agents_data:
            # Add multiple tasks to establish performance
            for i in range(5):
                self.tracker.record_task_execution(
                    agent_name=agent,
                    task_id=f"{agent}_task_{i}",
                    task_type="testing",
                    success=i < int(5 * success_rate),  # Simulate success rate
                    quality_score=quality + (i * 0.5),
                    execution_time_seconds=time + (i * 10)
                )

        # Test by quality score
        top_quality = self.tracker.get_top_performers("quality_score", limit=2)
        assert len(top_quality) == 2
        assert top_quality[0]["agent_name"] == "excellent_agent"

        # Test by success rate
        top_success = self.tracker.get_top_performers("success_rate", limit=2)
        assert len(top_success) == 2
        assert top_success[0]["agent_name"] == "excellent_agent"

    def test_get_weak_performers(self):
        """Test identifying weak performing agents."""
        # Add tasks for agents with different performance levels
        agents_performance = [
            ("strong_agent", 90.0),
            ("medium_agent", 80.0),
            ("weak_agent", 65.0),
            ("very_weak_agent", 55.0)
        ]

        for agent, quality in agents_performance:
            for i in range(5):  # Minimum tasks for evaluation
                self.tracker.record_task_execution(
                    agent_name=agent,
                    task_id=f"{agent}_task_{i}",
                    task_type="testing",
                    success=True,
                    quality_score=quality,
                    execution_time_seconds=100.0
                )

        weak_performers = self.tracker.get_weak_performers(threshold=75.0)
        assert len(weak_performers) == 2

        weak_agent_names = [agent["agent_name"] for agent in weak_performers]
        assert "weak_agent" in weak_agent_names
        assert "very_weak_agent" in weak_agent_names
        assert "strong_agent" not in weak_agent_names

        # Check improvement needed calculation
        weak_agent_data = next(agent for agent in weak_performers if agent["agent_name"] == "weak_agent")
        assert weak_agent_data["improvement_needed"] == 10.0  # 75 - 65

    def test_performance_rating_calculation(self):
        """Test performance rating calculation."""
        # Test different rating levels
        test_cases = [
            (95.0, 1.0, "Excellent"),      # Very high quality and success
            (85.0, 0.9, "Good"),           # High quality and success
            (75.0, 0.8, "Satisfactory"),    # Average quality and success
            (65.0, 0.7, "Needs Improvement"), # Below average
            (55.0, 0.5, "Poor")            # Poor performance
        ]

        for quality, success_rate, expected_rating in test_cases:
            metrics = {
                "total_tasks": 10,
                "average_quality_score": quality,
                "success_rate": success_rate
            }
            rating = self.tracker._calculate_performance_rating(metrics)
            assert rating == expected_rating

    def test_performance_trend_calculation(self):
        """Test performance trend calculation."""
        # Test improving trend
        improving_scores = [70, 75, 80, 85, 90]
        trend = self.tracker._calculate_trend(improving_scores)
        assert trend == "improving"

        # Test declining trend
        declining_scores = [90, 85, 80, 75, 70]
        trend = self.tracker._calculate_trend(declining_scores)
        assert trend == "declining"

        # Test stable trend
        stable_scores = [80, 82, 78, 81, 79]
        trend = self.tracker._calculate_trend(stable_scores)
        assert trend == "stable"

        # Test insufficient data
        few_scores = [80, 85]
        trend = self.tracker._calculate_trend(few_scores)
        assert trend == "insufficient_data"

    def test_specialization_update(self):
        """Test agent specialization identification and updates."""
        # Create an agent with clear specialization patterns
        specializations = [
            ("refactoring", 6),  # 50% of tasks
            ("testing", 3),      # 25% of tasks
            ("documentation", 3) # 25% of tasks
        ]

        for task_type, count in specializations:
            for i in range(count):
                self.tracker.record_task_execution(
                    agent_name="specialist_agent",
                    task_id=f"task_{task_type}_{i}",
                    task_type=task_type,
                    success=True,
                    quality_score=85.0,
                    execution_time_seconds=100.0
                )

        # Trigger specialization update
        self.tracker._update_specializations("specialist_agent")

        perf = self.tracker.get_agent_performance("specialist_agent")
        agent_specializations = perf["specializations"]

        # Should identify refactoring as specialization (>= 30% of tasks)
        refactoring_spec = next((spec for spec in agent_specializations if spec["task_type"] == "refactoring"), None)
        assert refactoring_spec is not None
        assert refactoring_spec["percentage"] == 50.0

    def test_task_type_tracking(self):
        """Test task type distribution tracking."""
        task_types = ["refactoring", "testing", "documentation", "bug_fix"]

        for i, task_type in enumerate(task_types):
            for j in range(i + 1):  # Different counts for each type
                self.tracker.record_task_execution(
                    agent_name="versatile_agent",
                    task_id=f"task_{task_type}_{j}",
                    task_type=task_type,
                    success=True,
                    quality_score=80.0,
                    execution_time_seconds=100.0
                )

        perf = self.tracker.get_agent_performance("versatile_agent")
        task_type_counts = perf["task_types"]

        assert task_type_counts["refactoring"] == 1
        assert task_type_counts["testing"] == 2
        assert task_type_counts["documentation"] == 3
        assert task_type_counts["bug_fix"] == 4

    def test_performance_summary(self):
        """Test overall performance summary calculation."""
        # Create multiple agents with varying performance
        agents_data = [
            ("agent1", [90, 85, 95], 1.0),
            ("agent2", [80, 75, 85], 0.8),
            ("agent3", [70, 65, 75], 0.6),
            ("agent4", [60, 55, 65], 0.4)  # Should be excluded (below 3 tasks initially)
        ]

        for agent, scores, success_rate in agents_data:
            task_count = len(scores)
            for i, score in enumerate(scores):
                self.tracker.record_task_execution(
                    agent_name=agent,
                    task_id=f"{agent}_task_{i}",
                    task_type="testing",
                    success=i < int(task_count * success_rate),
                    quality_score=score,
                    execution_time_seconds=100.0
                )

        # Add more tasks for agent4 to make it eligible
        for i in range(3):  # Total 6 tasks now
            self.tracker.record_task_execution(
                agent_name="agent4",
                task_id=f"agent4_task_extra_{i}",
                task_type="testing",
                success=True,
                quality_score=62.0,
                execution_time_seconds=100.0
            )

        summary = self.tracker.get_performance_summary()

        assert summary["total_agents"] == 4
        assert summary["total_tasks"] > 0
        assert summary["average_quality_score"] > 0
        assert summary["average_success_rate"] > 0
        assert "top_performers" in summary
        assert "weak_performers" in summary

    def test_quality_score_limit(self):
        """Test quality score history limit (last 100)."""
        agent_name = "test_agent"

        # Add more than 100 tasks
        for i in range(150):
            self.tracker.record_task_execution(
                agent_name=agent_name,
                task_id=f"task_{i}",
                task_type="testing",
                success=True,
                quality_score=80.0 + (i % 20),  # Vary scores slightly
                execution_time_seconds=100.0
            )

        perf = self.tracker.get_agent_performance(agent_name)

        # Should only keep last 100 quality scores
        assert len(perf["quality_scores"]) == 100

        # Total tasks should still be 150
        assert perf["total_tasks"] == 150

    def test_task_history_limit(self):
        """Test task history limit (last 1000)."""
        # Add more than 1000 tasks across multiple agents
        for i in range(1200):
            self.tracker.record_task_execution(
                agent_name=f"agent_{i % 10}",  # 10 different agents
                task_id=f"task_{i}",
                task_type="testing",
                success=True,
                quality_score=80.0,
                execution_time_seconds=100.0
            )

        data = self.tracker._read_data()
        task_history = data["task_history"]

        # Should only keep last 1000 tasks
        assert len(task_history) == 1000

    def test_file_operations_error_handling(self):
        """Test error handling in file operations."""
        # Test with corrupted JSON file
        with open(self.tracker.performance_file, "w") as f:
            f.write("invalid json")

        # Should initialize new storage
        self.tracker.record_task_execution("agent1", "task1", "testing", True, 85.0, 100.0)

        perf = self.tracker.get_agent_performance("agent1")
        assert perf["total_tasks"] == 1

    def test_metadata_updates(self):
        """Test metadata updates when recording tasks."""
        initial_data = self.tracker._read_data()
        initial_tasks = initial_data["metadata"]["total_tasks_tracked"]

        # Record a task
        self.tracker.record_task_execution("new_agent", "task1", "testing", True, 85.0, 100.0)

        updated_data = self.tracker._read_data()
        updated_tasks = updated_data["metadata"]["total_tasks_tracked"]
        updated_agents = updated_data["metadata"]["agents_active"]

        assert updated_tasks == initial_tasks + 1
        assert updated_agents >= initial_data["metadata"]["agents_active"]
        assert updated_data["metadata"]["last_updated"] != initial_data["metadata"]["last_updated"]

    @patch('agent_performance_tracker.PLATFORM', 'windows')
    def test_file_locking_windows(self):
        """Test file locking on Windows platform."""
        with patch('agent_performance_tracker.msvcrt') as mock_msvcrt:
            mock_msvcrt.locking = MagicMock()
            mock_msvcrt.LK_LOCK = 1
            mock_msvcrt.LK_UNLCK = 2

            # Test recording with file locking
            self.tracker.record_task_execution("agent1", "task1", "testing", True, 85.0, 100.0)

            # Verify locking was attempted
            assert mock_msvcrt.locking.called

    def test_iterations_tracking(self):
        """Test tracking of iterations required for tasks."""
        test_cases = [1, 2, 3, 5]  # Different iteration counts

        for iterations in test_cases:
            self.tracker.record_task_execution(
                agent_name="iterative_agent",
                task_id=f"task_{iterations}",
                task_type="testing",
                success=True,
                quality_score=85.0,
                execution_time_seconds=100.0,
                iterations=iterations
            )

        perf = self.tracker.get_agent_performance("iterative_agent")
        expected_avg = sum(test_cases) / len(test_cases)
        assert abs(perf["average_iterations"] - expected_avg) < 0.1
        assert perf["total_iterations"] == sum(test_cases)

    def test_performance_data_structure(self):
        """Test completeness of performance data structure."""
        self.tracker.record_task_execution(
            agent_name="comprehensive_agent",
            task_id="task_001",
            task_type="comprehensive_testing",
            success=True,
            quality_score=88.5,
            execution_time_seconds=125.75,
            recommendations_followed=3,
            auto_fix_applied=True,
            iterations=2,
            context={"test": "data"}
        )

        perf = self.tracker.get_agent_performance("comprehensive_agent")

        # Check all expected fields are present
        required_fields = [
            "agent_name", "total_tasks", "successful_tasks", "failed_tasks",
            "total_execution_time", "average_quality_score", "quality_scores",
            "task_types", "success_rate", "average_execution_time",
            "recommendations_followed_total", "auto_fixes_applied",
            "average_iterations", "total_iterations", "specializations",
            "first_task", "last_task", "performance_rating", "trend"
        ]

        for field in required_fields:
            assert field in perf


if __name__ == "__main__":
    pytest.main([__file__, "-v"])