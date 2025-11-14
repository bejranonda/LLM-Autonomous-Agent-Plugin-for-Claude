"""
Unit tests for Agent Feedback System

Tests the agent feedback functionality including:
- Feedback exchange between agent groups
- Cross-platform file locking
- Collaboration matrix tracking
- Learning insights management
- Performance statistics
"""

import pytest
import json
import tempfile
import shutil
import os
import sys
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta

# Add lib directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from agent_feedback_system import AgentFeedbackSystem


class TestAgentFeedbackSystem:
    """Test suite for AgentFeedbackSystem class"""

    @pytest.fixture
    def feedback_system(self, temp_directory):
        """Create an AgentFeedbackSystem instance with temporary directory"""
        return AgentFeedbackSystem(temp_directory)

    @pytest.fixture
    def sample_feedback_data(self):
        """Sample feedback data for testing"""
        return {
            "from_agent": "code-analyzer",
            "to_agent": "quality-controller",
            "task_id": "task_001",
            "feedback_type": "improvement",
            "message": "Consider adding more comprehensive error handling",
            "impact": "quality_score +5 points",
            "data": {
                "suggestions": ["add try-catch blocks", "validate inputs"],
                "priority": "medium"
            }
        }

    @pytest.fixture
    def existing_feedback_data(self, temp_directory):
        """Create existing feedback data for testing"""
        feedback_file = Path(temp_directory) / "agent_feedback.json"
        existing_data = {
            "version": "1.0.0",
            "last_updated": "2025-01-10T10:00:00",
            "metadata": {
                "total_feedbacks": 2,
                "analysis_to_execution": 1,
                "execution_to_analysis": 1,
                "cross_agent_learnings": 0
            },
            "feedback_exchanges": [
                {
                    "feedback_id": "feedback_20250110_001",
                    "from_agent": "code-analyzer",
                    "to_agent": "quality-controller",
                    "task_id": "task_existing_001",
                    "feedback_type": "success",
                    "message": "Code analysis was comprehensive",
                    "timestamp": "2025-01-10T09:00:00",
                    "read": False,
                    "applied": False
                },
                {
                    "feedback_id": "feedback_20250110_002",
                    "from_agent": "quality-controller",
                    "to_agent": "code-analyzer",
                    "task_id": "task_existing_002",
                    "feedback_type": "warning",
                    "message": "Some edge cases not covered",
                    "timestamp": "2025-01-10T11:00:00",
                    "read": True,
                    "applied": False
                }
            ],
            "learning_insights": {
                "common_patterns": [],
                "successful_collaborations": [],
                "improvement_areas": []
            },
            "agent_collaboration_matrix": {}
        }
        with open(feedback_file, 'w') as f:
            json.dump(existing_data, f)
        return feedback_file

    @pytest.mark.unit
    @pytest.mark.cross_platform
    def test_init_creates_directory_and_file(self, feedback_system):
        """Test that initialization creates directory and feedback file"""
        assert feedback_system.storage_dir.exists()
        assert feedback_system.feedback_file.exists()

        # Verify file contains initial structure
        data = feedback_system._read_data()
        assert "version" in data
        assert "metadata" in data
        assert "feedback_exchanges" in data
        assert "learning_insights" in data
        assert "agent_collaboration_matrix" in data

    @pytest.mark.unit
    def test_init_with_existing_file(self, existing_feedback_data):
        """Test initialization with existing feedback file"""
        temp_dir = existing_feedback_data.parent
        system = AgentFeedbackSystem(str(temp_dir))

        data = system._read_data()
        assert len(data["feedback_exchanges"]) == 2
        assert data["metadata"]["total_feedbacks"] == 2

    @pytest.mark.unit
    def test_add_feedback_success(self, feedback_system, sample_feedback_data):
        """Test successful feedback addition"""
        feedback_id = feedback_system.add_feedback(
            sample_feedback_data["from_agent"],
            sample_feedback_data["to_agent"],
            sample_feedback_data["task_id"],
            sample_feedback_data["feedback_type"],
            sample_feedback_data["message"],
            sample_feedback_data["impact"],
            sample_feedback_data["data"]
        )

        assert feedback_id is not None
        assert feedback_id.startswith("feedback_")

        # Verify feedback was stored
        data = feedback_system._read_data()
        assert len(data["feedback_exchanges"]) == 1

        stored_feedback = data["feedback_exchanges"][0]
        assert stored_feedback["feedback_id"] == feedback_id
        assert stored_feedback["from_agent"] == sample_feedback_data["from_agent"]
        assert stored_feedback["to_agent"] == sample_feedback_data["to_agent"]
        assert stored_feedback["task_id"] == sample_feedback_data["task_id"]
        assert stored_feedback["feedback_type"] == sample_feedback_data["feedback_type"]
        assert stored_feedback["message"] == sample_feedback_data["message"]
        assert stored_feedback["impact"] == sample_feedback_data["impact"]
        assert stored_feedback["data"] == sample_feedback_data["data"]
        assert "timestamp" in stored_feedback
        assert stored_feedback["read"] is False
        assert stored_feedback["applied"] is False

    @pytest.mark.unit
    def test_add_feedback_updates_metadata(self, feedback_system, sample_feedback_data):
        """Test that add_feedback updates metadata correctly"""
        # Add feedback from analysis to execution agent
        feedback_system.add_feedback(
            "code-analyzer",  # Analysis agent
            "quality-controller",  # Execution agent
            "task_001",
            "success",
            "Great work"
        )

        data = feedback_system._read_data()
        metadata = data["metadata"]

        assert metadata["total_feedbacks"] == 1
        assert metadata["analysis_to_execution"] == 1
        assert metadata["execution_to_analysis"] == 0
        assert metadata["cross_agent_learnings"] == 0

        # Add feedback from execution to analysis agent
        feedback_system.add_feedback(
            "quality-controller",  # Execution agent
            "code-analyzer",  # Analysis agent
            "task_002",
            "improvement",
            "Consider edge cases"
        )

        data = feedback_system._read_data()
        metadata = data["metadata"]

        assert metadata["total_feedbacks"] == 2
        assert metadata["analysis_to_execution"] == 1
        assert metadata["execution_to_analysis"] == 1

    @pytest.mark.unit
    def test_add_feedback_updates_collaboration_matrix(self, feedback_system):
        """Test that add_feedback updates collaboration matrix"""
        feedback_system.add_feedback(
            "agent_a",
            "agent_b",
            "task_001",
            "success",
            "Good collaboration"
        )

        data = feedback_system._read_data()
        matrix = data["agent_collaboration_matrix"]

        collab_key = "agent_a->agent_b"
        assert collab_key in matrix
        assert matrix[collab_key]["total_feedbacks"] == 1
        assert matrix[collab_key]["feedback_types"]["success"] == 1

    @pytest.mark.unit
    def test_get_feedback_for_agent(self, feedback_system, sample_feedback_data):
        """Test retrieving feedback for a specific agent"""
        # Add feedback for different agents
        feedback_data_list = [
            {
                "from_agent": "agent_a",
                "to_agent": "agent_b",
                "task_id": "task_001",
                "feedback_type": "success",
                "message": "Good work"
            },
            {
                "from_agent": "agent_c",
                "to_agent": "agent_b",
                "task_id": "task_002",
                "feedback_type": "improvement",
                "message": "Consider improvements"
            },
            {
                "from_agent": "agent_a",
                "to_agent": "agent_d",
                "task_id": "task_003",
                "feedback_type": "warning",
                "message": "Warning message"
            }
        ]

        for feedback_data in feedback_data_list:
            feedback_system.add_feedback(**feedback_data)

        # Get feedback for agent_b
        feedback_for_b = feedback_system.get_feedback_for_agent("agent_b")

        assert len(feedback_for_b) == 2
        assert all(fb["to_agent"] == "agent_b" for fb in feedback_for_b)

        # Should be sorted by timestamp (most recent first)
        timestamps = [fb["timestamp"] for fb in feedback_for_b]
        assert timestamps == sorted(timestamps, reverse=True)

    @pytest.mark.unit
    def test_get_feedback_for_agent_unread_only(self, feedback_system, sample_feedback_data):
        """Test retrieving only unread feedback for an agent"""
        # Add feedback
        feedback_id1 = feedback_system.add_feedback(
            "agent_a", "agent_b", "task_001", "success", "Good work"
        )
        feedback_id2 = feedback_system.add_feedback(
            "agent_c", "agent_b", "task_002", "improvement", "Consider improvements"
        )

        # Mark one as read
        feedback_system.mark_feedback_read(feedback_id1)

        # Get unread feedback only
        unread_feedback = feedback_system.get_feedback_for_agent("agent_b", unread_only=True)

        assert len(unread_feedback) == 1
        assert unread_feedback[0]["feedback_id"] == feedback_id2

        # Get all feedback
        all_feedback = feedback_system.get_feedback_for_agent("agent_b", unread_only=False)

        assert len(all_feedback) == 2

    @pytest.mark.unit
    def test_get_feedback_for_agent_with_limit(self, feedback_system):
        """Test retrieving feedback with limit"""
        # Add multiple feedback entries
        for i in range(10):
            feedback_system.add_feedback(
                f"agent_a",
                "agent_b",
                f"task_{i:03d}",
                "success",
                f"Message {i}"
            )

        # Test with limit
        limited_feedback = feedback_system.get_feedback_for_agent("agent_b", limit=5)

        assert len(limited_feedback) == 5

    @pytest.mark.unit
    def test_mark_feedback_read(self, feedback_system, sample_feedback_data):
        """Test marking feedback as read"""
        feedback_id = feedback_system.add_feedback(**sample_feedback_data)

        # Verify it's unread initially
        data = feedback_system._read_data()
        feedback = next(fb for fb in data["feedback_exchanges"] if fb["feedback_id"] == feedback_id)
        assert feedback["read"] is False

        # Mark as read
        feedback_system.mark_feedback_read(feedback_id)

        # Verify it's now read
        data = feedback_system._read_data()
        feedback = next(fb for fb in data["feedback_exchanges"] if fb["feedback_id"] == feedback_id)
        assert feedback["read"] is True

    @pytest.mark.unit
    def test_mark_feedback_applied(self, feedback_system, sample_feedback_data):
        """Test marking feedback as applied"""
        feedback_id = feedback_system.add_feedback(**sample_feedback_data)

        # Mark as applied
        feedback_system.mark_feedback_applied(feedback_id)

        # Verify it's applied
        data = feedback_system._read_data()
        feedback = next(fb for fb in data["feedback_exchanges"] if fb["feedback_id"] == feedback_id)
        assert feedback["applied"] is True
        assert "applied_at" in feedback

    @pytest.mark.unit
    def test_get_collaboration_stats(self, feedback_system):
        """Test getting collaboration statistics"""
        # Add various feedback entries
        feedback_entries = [
            ("code-analyzer", "quality-controller", "success"),
            ("quality-controller", "code-analyzer", "improvement"),
            ("code-analyzer", "test-engineer", "warning"),
            ("test-engineer", "code-analyzer", "success"),
            ("code-analyzer", "quality-controller", "improvement")  # Applied feedback
        ]

        feedback_ids = []
        for from_agent, to_agent, feedback_type in feedback_entries:
            feedback_id = feedback_system.add_feedback(
                from_agent, to_agent, "task_001", feedback_type, f"Message {feedback_type}"
            )
            feedback_ids.append(feedback_id)

        # Mark last feedback as applied
        feedback_system.mark_feedback_applied(feedback_ids[-1])

        stats = feedback_system.get_collaboration_stats()

        assert stats["total_feedbacks"] == 5
        assert stats["analysis_to_execution"] >= 1
        assert stats["execution_to_analysis"] >= 1

        # Check feedback effectiveness (40% applied = 2 out of 5)
        assert stats["feedback_effectiveness"] == 40.0

        # Check collaboration matrix exists
        assert "collaboration_matrix" in stats
        assert "most_active_pairs" in stats

    @pytest.mark.unit
    def test_add_learning_insight(self, feedback_system):
        """Test adding learning insights"""
        insight_data = {
            "insight_type": "common_pattern",
            "description": "Code analysis consistently finds security issues",
            "agents_involved": ["code-analyzer", "security-auditor"],
            "impact": "Improved code security by 25%"
        }

        feedback_system.add_learning_insight(**insight_data)

        data = feedback_system._read_data()
        insights = data["learning_insights"]

        assert "common_pattern" in insights
        assert len(insights["common_pattern"]) == 1

        insight = insights["common_pattern"][0]
        assert insight["type"] == "common_pattern"
        assert insight["description"] == insight_data["description"]
        assert insight["agents_involved"] == insight_data["agents_involved"]
        assert insight["impact"] == insight_data["impact"]
        assert "insight_id" in insight
        assert "timestamp" in insight

    @pytest.mark.unit
    def test_get_insights(self, feedback_system):
        """Test retrieving learning insights"""
        # Add insights of different types
        insights_data = [
            ("common_pattern", "Pattern 1", ["agent1", "agent2"]),
            ("successful_collaboration", "Success 1", ["agent3", "agent4"]),
            ("improvement_area", "Improvement 1", ["agent5", "agent6"]),
            ("common_pattern", "Pattern 2", ["agent7", "agent8"])
        ]

        for insight_type, description, agents in insights_data:
            feedback_system.add_learning_insight(insight_type, description, agents)

        # Get all insights
        all_insights = feedback_system.get_insights()
        assert len(all_insights) == 4

        # Should be sorted by timestamp (most recent first)
        timestamps = [insight["timestamp"] for insight in all_insights]
        assert timestamps == sorted(timestamps, reverse=True)

        # Get insights of specific type
        pattern_insights = feedback_system.get_insights("common_pattern")
        assert len(pattern_insights) == 2
        assert all(insight["type"] == "common_pattern" for insight in pattern_insights)

    @pytest.mark.unit
    def test_agent_group_classifications(self, feedback_system):
        """Test agent group classification constants"""
        # Check that known agents are in correct groups
        assert "code-analyzer" in feedback_system.ANALYSIS_AGENTS
        assert "quality-controller" in feedback_system.EXECUTION_AGENTS

        # Test classification logic
        assert "code-analyzer" in feedback_system.ANALYSIS_AGENTS
        assert "test-engineer" in feedback_system.EXECUTION_AGENTS
        assert "smart-recommender" in feedback_system.ANALYSIS_AGENTS
        assert "documentation-generator" in feedback_system.EXECUTION_AGENTS

    @pytest.mark.unit
    @pytest.mark.parametrize("platform", ["Windows", "Linux", "Darwin"])
    def test_file_locking_cross_platform(self, feedback_system, platform):
        """Test file locking mechanism across different platforms"""
        with patch('platform.system', return_value=platform):
            # Test reading with file lock
            data = feedback_system._read_data()
            assert isinstance(data, dict)

            # Test writing with file lock
            feedback_system._write_data(data)

    @pytest.mark.unit
    def test_file_corruption_handling(self, feedback_system):
        """Test handling of corrupted feedback file"""
        # Write corrupted JSON
        with open(feedback_system.feedback_file, 'w') as f:
            f.write("{ invalid json content")

        # Should handle corruption gracefully and reinitialize
        data = feedback_system._read_data()
        assert isinstance(data, dict)
        assert "version" in data
        assert "feedback_exchanges" in data

    @pytest.mark.unit
    def test_feedback_id_generation(self, feedback_system, sample_feedback_data):
        """Test that feedback IDs are generated correctly"""
        feedback_id = feedback_system.add_feedback(**sample_feedback_data)

        # Should generate timestamp-based ID
        assert feedback_id.startswith("feedback_")
        assert len(feedback_id) > len("feedback_")  # Has timestamp suffix

        # Should be unique
        feedback_id2 = feedback_system.add_feedback(**sample_feedback_data)
        assert feedback_id != feedback_id2

    @pytest.mark.unit
    def test_metadata_update_consistency(self, feedback_system):
        """Test that metadata is updated consistently"""
        # Add feedback across different directions
        feedback_system.add_feedback("code-analyzer", "quality-controller", "task1", "success", "msg1")
        feedback_system.add_feedback("quality-controller", "code-analyzer", "task2", "improvement", "msg2")
        feedback_system.add_feedback("test-engineer", "test-engineer", "task3", "warning", "msg3")  # Same group

        data = feedback_system._read_data()
        metadata = data["metadata"]

        assert metadata["total_feedbacks"] == 3
        assert metadata["analysis_to_execution"] == 1
        assert metadata["execution_to_analysis"] == 1
        assert metadata["cross_agent_learnings"] == 1

    @pytest.mark.unit
    def test_collaboration_matrix_tracking(self, feedback_system):
        """Test collaboration matrix tracking functionality"""
        # Add multiple feedback between same agent pair
        agent_pairs = [
            ("agent_a", "agent_b", "success"),
            ("agent_a", "agent_b", "improvement"),
            ("agent_a", "agent_b", "success")
        ]

        for from_agent, to_agent, feedback_type in agent_pairs:
            feedback_system.add_feedback(from_agent, to_agent, "task", feedback_type, "msg")

        stats = feedback_system.get_collaboration_stats()
        matrix = stats["collaboration_matrix"]

        # Check matrix entry for agent_a->agent_b
        collab_key = "agent_a->agent_b"
        assert collab_key in matrix

        entry = matrix[collab_key]
        assert entry["total_feedbacks"] == 3
        assert entry["feedback_types"]["success"] == 2
        assert entry["feedback_types"]["improvement"] == 1

        # Check most active pairs
        most_active = stats["most_active_pairs"]
        assert len(most_active) >= 1
        assert most_active[0]["pair"] == collab_key
        assert most_active[0]["total_feedbacks"] == 3

    @pytest.mark.unit
    def test_feedback_effectiveness_calculation(self, feedback_system):
        """Test feedback effectiveness calculation"""
        # Add feedback entries
        feedback_ids = []
        for i in range(10):
            feedback_id = feedback_system.add_feedback(
                f"agent_a", f"agent_b", f"task_{i}", "success", f"Message {i}"
            )
            feedback_ids.append(feedback_id)

        # Apply some of them
        for i in range(4):  # Apply 4 out of 10
            feedback_system.mark_feedback_applied(feedback_ids[i])

        stats = feedback_system.get_collaboration_stats()
        effectiveness = stats["feedback_effectiveness"]

        assert effectiveness == 40.0  # 4/10 * 100

    @pytest.mark.unit
    def test_empty_system_behavior(self, feedback_system):
        """Test system behavior with no data"""
        # Test getting feedback for non-existent agent
        feedback = feedback_system.get_feedback_for_agent("nonexistent_agent")
        assert len(feedback) == 0

        # Test getting insights with no data
        insights = feedback_system.get_insights()
        assert len(insights) == 0

        # Test collaboration stats with no data
        stats = feedback_system.get_collaboration_stats()
        assert stats["total_feedbacks"] == 0
        assert stats["feedback_effectiveness"] == 0.0

    @pytest.mark.unit
    def test_large_volume_performance(self, feedback_system):
        """Test performance with large volume of feedback"""
        import time

        # Add many feedback entries
        start_time = time.time()
        feedback_count = 1000

        feedback_ids = []
        for i in range(feedback_count):
            from_agent = f"agent_{i % 10}"  # 10 different agents
            to_agent = f"agent_{(i + 1) % 10}"
            feedback_id = feedback_system.add_feedback(
                from_agent, to_agent, f"task_{i}", "success", f"Message {i}"
            )
            feedback_ids.append(feedback_id)

        add_time = time.time() - start_time

        # Should complete within reasonable time
        assert add_time < 5.0  # 5 seconds for 1000 entries

        # Test retrieval performance
        start_time = time.time()
        stats = feedback_system.get_collaboration_stats()
        stats_time = time.time() - start_time

        assert stats_time < 1.0  # Stats calculation should be fast
        assert stats["total_feedbacks"] == feedback_count

    @pytest.mark.unit
    def test_concurrent_feedback_simulation(self, feedback_system):
        """Test simulated concurrent feedback addition"""
        # Simulate rapid feedback additions
        feedback_ids = []
        for i in range(50):
            feedback_id = feedback_system.add_feedback(
                f"agent_{i % 5}",  # 5 different agents
                f"agent_{(i + 1) % 5}",
                f"task_{i}",
                ["success", "improvement", "warning"][i % 3],
                f"Concurrent message {i}"
            )
            feedback_ids.append(feedback_id)

        # All should succeed
        assert len(feedback_ids) == 50
        assert len(set(feedback_ids)) == 50  # All unique IDs

        # Verify all feedback was stored
        data = feedback_system._read_data()
        assert len(data["feedback_exchanges"]) == 50

    @pytest.mark.unit
    def test_edge_case_empty_strings(self, feedback_system):
        """Test handling of empty strings and special characters"""
        feedback_id = feedback_system.add_feedback(
            "",  # Empty from_agent
            "",  # Empty to_agent
            "",  # Empty task_id
            "",  # Empty feedback_type
            "",  # Empty message
            None  # Empty impact
        )

        assert feedback_id is not None

        # Verify data integrity
        data = feedback_system._read_data()
        feedback = data["feedback_exchanges"][0]
        assert feedback["from_agent"] == ""
        assert feedback["to_agent"] == ""
        assert feedback["task_id"] == ""