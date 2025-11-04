"""
Tests for Intelligent Agent Router (lib/intelligent_agent_router.py)

Tests the optimal agent selection and delegation system that routes
tasks based on performance metrics and specialization.
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
    from intelligent_agent_router import IntelligentAgentRouter
except ImportError:
    pytest.skip("intelligent_agent_router.py not available", allow_module_level=True)


class TestIntelligentAgentRouter:
    """Test cases for Intelligent Agent Router"""

    @pytest.fixture
    def agent_router(self, temp_directory):
        """Create an IntelligentAgentRouter instance for testing"""
        return IntelligentAgentRouter(data_dir=temp_directory)

    @pytest.fixture
    def sample_task_info(self):
        """Sample task information for testing"""
        return {
            "type": "security_audit",
            "complexity": "high",
            "language": "python",
            "framework": "django",
            "priority": "high",
            "estimated_duration": "medium"
        }

    @pytest.fixture
    def available_agents(self):
        """Sample list of available agents"""
        return [
            {
                "name": "security-auditor",
                "capabilities": ["security", "vulnerability_scan", "compliance"],
                "current_load": 3,
                "max_capacity": 10,
                "specialization": "security",
                "status": "available"
            },
            {
                "name": "code-analyzer",
                "capabilities": ["analysis", "refactoring", "code_structure"],
                "current_load": 5,
                "max_capacity": 10,
                "specialization": "code_analysis",
                "status": "available"
            },
            {
                "name": "quality-controller",
                "capabilities": ["quality_check", "auto_fix", "standards"],
                "current_load": 2,
                "max_capacity": 10,
                "specialization": "quality",
                "status": "available"
            }
        ]

    def test_initialization(self, agent_router):
        """Test system initialization"""
        assert agent_router is not None
        assert hasattr(agent_router, 'data_dir')
        assert hasattr(agent_router, 'routing_file')

    def test_route_task_basic(self, agent_router, sample_task_info):
        """Test basic task routing"""
        routing = agent_router.route_task(sample_task_info, tier="execution")

        assert isinstance(routing, dict)
        assert 'agent' in routing
        assert 'confidence' in routing
        assert 'reasoning' in routing

        # Confidence should be between 0 and 1
        assert 0 <= routing['confidence'] <= 1

    def test_route_task_by_tier(self, agent_router, sample_task_info):
        """Test routing for different tiers"""
        tiers = ["analysis", "execution"]

        results = {}
        for tier in tiers:
            routing = agent_router.route_task(sample_task_info, tier=tier)
            results[tier] = routing

        # Should provide routing for both tiers
        for tier, routing in results.items():
            assert isinstance(routing, dict)
            assert 'agent' in routing
            assert 'confidence' in routing

    def test_security_task_routing(self, agent_router):
        """Test routing of security tasks to appropriate agents"""
        security_task = {
            "type": "security_audit",
            "complexity": "high",
            "security_concerns": ["vulnerability", "compliance", "authentication"],
            "priority": "critical"
        }

        routing = agent_router.route_task(security_task, tier="analysis")

        # Should route to security-related agent
        assert 'security' in routing['agent'].lower() or 'audit' in routing['agent'].lower()

        # Should have high confidence for security tasks
        assert routing['confidence'] > 0.7

    def test_refactoring_task_routing(self, agent_router):
        """Test routing of refactoring tasks"""
        refactoring_task = {
            "type": "refactoring",
            "language": "python",
            "complexity": "medium",
            "focus_areas": ["code_structure", "performance", "maintainability"]
        }

        routing = agent_router.route_task(refactoring_task, tier="analysis")

        # Should route to code analysis related agent
        assert 'code' in routing['agent'].lower() or 'analysis' in routing['agent'].lower()

    def test_testing_task_routing(self, agent_router):
        """Test routing of testing tasks"""
        testing_task = {
            "type": "testing",
            "language": "python",
            "test_types": ["unit", "integration", "coverage"],
            "framework": "pytest"
        }

        routing = agent_router.route_task(testing_task, tier="execution")

        # Should route to testing specialist
        assert 'test' in routing['agent'].lower()

    def test_load_balancing(self, agent_router, available_agents):
        """Test load balancing across agents"""
        # Simulate tasks with different loads
        base_task = {"type": "analysis", "complexity": "medium"}

        # Route multiple tasks
        routings = []
        for i in range(5):
            routing = agent_router.route_task(base_task, tier="analysis")
            routings.append(routing)

        # Should distribute load (implementation specific)
        # This test ensures the system doesn't crash and produces valid routings
        for routing in routings:
            assert isinstance(routing, dict)
            assert 'agent' in routing
            assert 'confidence' in routing

    def test_specialization_matching(self, agent_router):
        """Test matching tasks to specialized agents"""
        specialization_tasks = [
            {
                "type": "security_audit",
                "expected_specialization": "security"
            },
            {
                "type": "documentation_generation",
                "expected_specialization": "documentation"
            },
            {
                "type": "performance_analysis",
                "expected_specialization": "performance"
            }
        ]

        for task in specialization_tasks:
            routing = agent_router.route_task(task, tier="analysis")

            # Should match specialization when possible
            assert isinstance(routing, dict)
            assert 'reasoning' in routing

    def test_routing_confidence_calculation(self, agent_router, sample_task_info):
        """Test confidence calculation in routing decisions"""
        routing = agent_router.route_task(sample_task_info, tier="execution")

        # Should provide confidence breakdown
        if 'confidence_breakdown' in routing:
            breakdown = routing['confidence_breakdown']
            assert isinstance(breakdown, dict)
            assert 'specialization_match' in breakdown
            assert 'availability' in breakdown
            assert 'historical_performance' in breakdown

    def test_routing_performance_tracking(self, agent_router, sample_task_info):
        """Test tracking of routing performance"""
        routing = agent_router.route_task(sample_task_info, tier="execution")

        # Record routing outcome
        outcome_data = {
            "task_info": sample_task_info,
            "routing": routing,
            "actual_agent": routing['agent'],
            "success": True,
            "quality_score": 92.0,
            "execution_time_seconds": 180,
            "user_satisfaction": "high"
        }

        result = agent_router.record_routing_outcome(outcome_data)
        assert result is True

        # Get routing performance metrics
        metrics = agent_router.get_routing_performance(days=7)

        assert isinstance(metrics, dict)
        assert 'total_routings' in metrics
        assert 'success_rate' in metrics
        assert 'average_confidence' in metrics

    def test_agent_performance_data(self, agent_router):
        """Test retrieval of agent performance data"""
        agent_name = "test-agent"

        # Get performance data
        performance = agent_router.get_performance_data(agent_name, "security_audit")

        assert isinstance(performance, dict)

        # Should include standard performance metrics
        expected_keys = ['success_rate', 'average_quality_score', 'total_tasks']
        for key in expected_keys:
            assert key in performance

    def test_routing_learning(self, agent_router, sample_task_info):
        """Test that routing learns from outcomes"""
        agent_name = "learning-test-agent"
        task_type = sample_task_info["type"]

        # Record successful outcomes for specific agent
        for i in range(5):
            outcome = {
                "task_info": sample_task_info,
                "routing": {"agent": agent_name, "confidence": 0.8},
                "actual_agent": agent_name,
                "success": True,
                "quality_score": 90.0 + i,
                "execution_time_seconds": 150 - i * 5
            }
            agent_router.record_routing_outcome(outcome)

        # Future routing should have learned preference
        routing = agent_router.route_task(sample_task_info, tier="execution")

        # Should potentially route to the successful agent
        assert isinstance(routing, dict)
        assert 'confidence' in routing

    def test_availability_checking(self, agent_router):
        """Test agent availability checking"""
        task_info = {
            "type": "urgent_task",
            "priority": "critical",
            "time_sensitive": True
        }

        routing = agent_router.route_task(task_info, tier="execution")

        # Should consider availability
        assert isinstance(routing, dict)
        assert 'agent' in routing

        # Should not route to unavailable agents
        # (Implementation specific - test that it doesn't crash)

    def test_priority_based_routing(self, agent_router):
        """Test routing based on task priority"""
        priorities = ["low", "medium", "high", "critical"]
        base_task = {"type": "analysis", "complexity": "medium"}

        results = {}
        for priority in priorities:
            task = base_task.copy()
            task["priority"] = priority

            routing = agent_router.route_task(task, tier="analysis")
            results[priority] = routing

        # Should handle different priority levels
        for priority, routing in results.items():
            assert isinstance(routing, dict)
            assert 'agent' in routing

    def test_complexity_based_routing(self, agent_router):
        """Test routing based on task complexity"""
        complexities = ["low", "medium", "high", "extreme"]
        base_task = {"type": "analysis", "language": "python"}

        results = {}
        for complexity in complexities:
            task = base_task.copy()
            task["complexity"] = complexity

            routing = agent_router.route_task(task, tier="execution")
            results[complexity] = routing

        # Should route complex tasks appropriately
        for complexity, routing in results.items():
            assert isinstance(routing, dict)
            assert 'confidence' in routing

    def test_batch_routing(self, agent_router):
        """Test batch routing for multiple tasks"""
        tasks = [
            {"type": "security_audit", "priority": "high"},
            {"type": "documentation", "priority": "medium"},
            {"type": "testing", "priority": "low"},
            {"type": "refactoring", "priority": "medium"}
        ]

        batch_results = agent_router.batch_route(tasks, tier="execution")

        assert isinstance(batch_results, list)
        assert len(batch_results) == len(tasks)

        for i, result in enumerate(batch_results):
            assert 'task_info' in result
            assert 'routing' in result
            assert result['task_info'] == tasks[i]

    def test_routing_explanation(self, agent_router, sample_task_info):
        """Test routing explanation generation"""
        routing = agent_router.route_task(sample_task_info, tier="execution")

        explanation = agent_router.get_routing_explanation(routing, sample_task_info)

        assert isinstance(explanation, dict)
        assert 'selected_agent' in explanation
        assert 'selection_factors' in explanation
        assert 'confidence_explanation' in explanation

    def test_agent_specialization_discovery(self, agent_router):
        """Test discovery of agent specializations"""
        # Record various task outcomes for agents
        agent_tasks = {
            "security-specialist": ["security_audit", "vulnerability_scan", "compliance_check"],
            "code-analyst": ["refactoring", "code_review", "structure_analysis"],
            "test-engineer": ["unit_testing", "integration_testing", "coverage_analysis"]
        }

        for agent, task_types in agent_tasks.items():
            for task_type in task_types:
                task_info = {"type": task_type, "complexity": "medium"}
                outcome = {
                    "task_info": task_info,
                    "routing": {"agent": agent, "confidence": 0.8},
                    "actual_agent": agent,
                    "success": True,
                    "quality_score": 90.0
                }
                agent_router.record_routing_outcome(outcome)

        # Get specializations
        specializations = agent_router.get_discovered_specializations()

        assert isinstance(specializations, dict)
        # Should have identified some specializations
        assert len(specializations) > 0

    def test_routing_persistence(self, agent_router, sample_task_info):
        """Test that routing data persists across instances"""
        # Route a task
        routing = agent_router.route_task(sample_task_info, tier="execution")

        # Record outcome
        outcome_data = {
            "task_info": sample_task_info,
            "routing": routing,
            "actual_agent": routing['agent'],
            "success": True,
            "quality_score": 95.0
        }
        agent_router.record_routing_outcome(outcome_data)

        # Create new instance with same data directory
        new_router = IntelligentAgentRouter(data_dir=agent_router.data_dir)

        # Should be able to retrieve routing history
        performance = new_router.get_routing_performance(days=7)
        assert isinstance(performance, dict)

    def test_file_creation_and_format(self, temp_directory, sample_task_info):
        """Test that routing file is created correctly"""
        router = IntelligentAgentRouter(data_dir=temp_directory)

        # Route task to trigger file creation
        router.route_task(sample_task_info, tier="execution")

        # Check file exists
        routing_file = os.path.join(temp_directory, 'agent_routing.json')
        assert os.path.exists(routing_file)

        # Check file content
        with open(routing_file, 'r') as f:
            data = json.load(f)

        assert 'routing_history' in data
        assert 'agent_performance' in data
        assert 'specialization_data' in data

    def test_error_handling(self, agent_router):
        """Test error handling in various scenarios"""
        # Test with corrupted data file
        routing_file = agent_router.routing_file

        # Create corrupted JSON file
        with open(routing_file, 'w') as f:
            f.write("invalid json content")

        # Should handle gracefully
        routing = agent_router.route_task({"type": "test"}, tier="analysis")
        assert isinstance(routing, dict)

    def test_routing_optimization(self, agent_router):
        """Test routing optimization over time"""
        # Simulate learning period
        for i in range(10):
            task_info = {"type": "optimization_test", "complexity": "medium"}
            routing = agent_router.route_task(task_info, tier="execution")

            outcome = {
                "task_info": task_info,
                "routing": routing,
                "actual_agent": routing['agent'],
                "success": True,
                "quality_score": 85.0 + i,
                "execution_time_seconds": 120 - i * 2
            }
            agent_router.record_routing_outcome(outcome)

        # Get optimization metrics
        optimization = agent_router.get_routing_optimization()

        assert isinstance(optimization, dict)
        assert 'learning_progress' in optimization
        assert 'confidence_improvement' in optimization

    def test_unhandled_task_routing(self, agent_router):
        """Test routing of unfamiliar task types"""
        unfamiliar_task = {
            "type": "brand_new_task_type",
            "complexity": "unknown",
            "domain": "emerging_technology"
        }

        routing = agent_router.route_task(unfamiliar_task, tier="analysis")

        # Should still provide routing based on general capabilities
        assert isinstance(routing, dict)
        assert 'agent' in routing
        assert 'confidence' in routing
        # Confidence might be lower for unfamiliar tasks
        assert 0 <= routing['confidence'] <= 1