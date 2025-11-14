"""
Test configuration and fixtures for Autonomous Agent Plugin v7.9.0

This module provides common test utilities, fixtures, and configuration
for testing the autonomous agent plugin with four-tier architecture.

Cross-platform compatibility: Windows, Linux, macOS
Testing categories: Unit, Integration, Performance, Security
"""

import pytest
import tempfile
import shutil
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch
import sys

# Add lib directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

class TestConfig:
    """Test configuration constants"""

    # Test data directory
    TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')

    # Sample plugin paths
    SAMPLE_PLUGIN_PATHS = [
        os.path.join(os.path.dirname(__file__), '..'),
        os.path.join(os.path.dirname(__file__), '..', '.claude-plugin'),
        '/tmp/test_plugin'
    ]

    # Sample project patterns
    SAMPLE_PATTERNS = {
        "project_context": {
            "detected_languages": ["python", "javascript"],
            "frameworks": ["flask", "react"],
            "project_type": "web-application"
        },
        "patterns": [
            {
                "task_type": "refactoring",
                "context": {"language": "python", "complexity": "medium"},
                "execution": {
                    "skills_used": ["code-analysis", "quality-standards"],
                    "agents_delegated": ["code-analyzer"]
                },
                "outcome": {"success": True, "quality_score": 96},
                "reuse_count": 5
            }
        ],
        "skill_effectiveness": {
            "code-analysis": {
                "success_rate": 0.93,
                "recommended_for": ["refactoring", "bug-fix"]
            }
        }
    }

    # Sample quality history
    SAMPLE_QUALITY_HISTORY = {
        "assessments": [
            {
                "assessment_id": "quality-check-20250104-001",
                "timestamp": "2025-01-04T14:30:00Z",
                "task_type": "quality-control",
                "overall_score": 94,
                "breakdown": {
                    "tests_passing": 28,
                    "standards_compliance": 23,
                    "documentation": 18,
                    "pattern_adherence": 15,
                    "code_metrics": 10
                }
            }
        ]
    }

@pytest.fixture
def temp_directory():
    """Create a temporary directory for test files"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def test_patterns_file(temp_directory):
    """Create a test patterns.json file"""
    patterns_file = os.path.join(temp_directory, 'patterns.json')
    with open(patterns_file, 'w') as f:
        json.dump(TestConfig.SAMPLE_PATTERNS, f)
    return patterns_file

@pytest.fixture
def test_quality_file(temp_directory):
    """Create a test quality_history.json file"""
    quality_file = os.path.join(temp_directory, 'quality_history.json')
    with open(quality_file, 'w') as f:
        json.dump(TestConfig.SAMPLE_QUALITY_HISTORY, f)
    return quality_file

@pytest.fixture
def mock_plugin_path(temp_directory):
    """Create a mock plugin directory structure"""
    plugin_dir = os.path.join(temp_directory, '.claude-plugin')
    os.makedirs(plugin_dir)

    # Create plugin.json
    plugin_json = {
        "name": "Autonomous Agent",
        "version": "7.7.0",
        "description": "Four-Tier Architecture with Enhanced Smart Recommendations"
    }

    with open(os.path.join(plugin_dir, 'plugin.json'), 'w') as f:
        json.dump(plugin_json, f)

    return plugin_dir

@pytest.fixture
def sample_task_info():
    """Sample task information for testing"""
    return {
        "type": "refactoring",
        "language": "python",
        "complexity": "medium",
        "framework": "flask",
        "description": "Refactor authentication module"
    }

@pytest.fixture
def sample_agent_performance():
    """Sample agent performance data"""
    return {
        "agent_name": "code-analyzer",
        "task_type": "refactoring",
        "success": True,
        "quality_score": 94.0,
        "execution_time_seconds": 120,
        "iterations": 1
    }

@pytest.fixture
def sample_user_interaction():
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

@pytest.fixture
def sample_feedback_data():
    """Sample agent feedback data"""
    return {
        "from_agent": "quality-controller",
        "to_agent": "code-analyzer",
        "task_id": "task_123",
        "feedback_type": "success",
        "message": "Recommendations highly effective, quality score +12 points",
        "impact": "quality_score +12"
    }

class MockResponse:
    """Mock response object for testing"""
    def __init__(self, data=None, status_code=200):
        self.data = data or {}
        self.status_code = status_code

    def json(self):
        return self.data

def create_test_files(directory, files_data):
    """Helper to create test files with given data"""
    created_files = []
    for filename, content in files_data.items():
        file_path = os.path.join(directory, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if isinstance(content, dict):
            with open(file_path, 'w') as f:
                json.dump(content, f)
        else:
            with open(file_path, 'w') as f:
                f.write(content)

        created_files.append(file_path)

    return created_files

def assert_file_exists(file_path):
    """Helper to assert a file exists"""
    assert os.path.exists(file_path), f"File {file_path} does not exist"

def assert_file_content(file_path, expected_content):
    """Helper to assert file content matches expected"""
    assert_file_exists(file_path)

    with open(file_path, 'r') as f:
        actual_content = f.read()

    if isinstance(expected_content, dict):
        actual_data = json.loads(actual_content)
        assert actual_data == expected_content
    else:
        assert actual_content == expected_content


@pytest.fixture
def cross_platform_temp_dir():
    """
    Create a cross-platform temporary directory that handles path separators correctly.
    This fixture is essential for testing file operations on Windows vs Unix systems.
    """
    import platform
    temp_dir = tempfile.mkdtemp()

    # Store platform info for tests
    platform_info = {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'path_separator': os.sep,
        'temp_dir': temp_dir
    }

    yield temp_dir, platform_info
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_file_lock():
    """
    Mock file locking mechanisms for cross-platform testing.
    Windows uses msvcrt, Unix uses fcntl.
    """
    import platform

    if platform.system() == 'Windows':
        with patch('msvcrt.locking') as mock_lock:
            yield {
                'lock': mock_lock,
                'unlock': mock_lock,  # Same function used for both lock and unlock
                'platform': 'Windows'
            }
    else:
        with patch('fcntl.flock') as mock_lock, \
             patch('os.O_LOCK') as mock_lock_flag:
            yield {
                'lock': mock_lock,
                'platform': 'Unix'
            }


@pytest.fixture(params=['Windows', 'Linux', 'Darwin'])
def mock_platform(request):
    """
    Parametrized fixture to test behavior on different platforms.
    Tests will run three times, once for each platform.
    """
    with patch('platform.system', return_value=request.param), \
         patch('sys.platform', return_value=request.param.lower()):
        yield request.param


@pytest.fixture
def sample_pattern_data():
    """Sample pattern data for testing pattern storage"""
    return {
        'task_type': 'feature_implementation',
        'context': 'Add user authentication system',
        'skills_used': ['code-analysis', 'security-audit', 'testing'],
        'approach': 'Implemented JWT-based authentication with proper validation',
        'quality_score': 0.87,
        'timestamp': '2025-01-12T10:30:00Z',
        'usage_count': 0,
        'success_rate': 1.0
    }


@pytest.fixture
def sample_quality_metrics():
    """Sample quality metrics for testing"""
    return {
        'task_id': 'task_001',
        'quality_score': 0.88,
        'metrics': {
            'code_quality': 0.90,
            'test_quality': 0.85,
            'documentation': 0.80,
            'patterns': 0.95,
            'performance': 0.87
        }
    }


@pytest.fixture
def mock_agent_groups():
    """Mock four-tier agent group structure"""
    return {
        'Group1_Analysis': [
            'code-analyzer', 'smart-recommender', 'security-auditor',
            'performance-analytics', 'pr-reviewer', 'learning-engine',
            'validation-controller'
        ],
        'Group2_Decision': [
            'strategic-planner', 'resource-allocator'
        ],
        'Group3_Execution': [
            'quality-controller', 'test-engineer', 'frontend-analyzer',
            'documentation-generator', 'build-validator', 'git-repository-manager',
            'api-contract-validator', 'gui-validator', 'dev-orchestrator',
            'version-release-manager', 'workspace-organizer', 'report-management-organizer',
            'background-task-manager', 'claude-plugin-validator'
        ],
        'Group4_Validation': [
            'post-execution-validator', 'quality-assurance-validator',
            'performance-validator', 'integration-validator'
        ]
    }


@pytest.fixture
def optimizer():
    """Mock agent communication optimizer fixture for testing"""
    from unittest.mock import Mock

    mock_optimizer = Mock()
    mock_optimizer.optimize_communication.return_value = {
        'success': True,
        'optimizations': [
            {'component': 'cache', 'improvement': 25},
            {'component': 'compression', 'improvement': 15}
        ],
        'efficiency_gain': 0.30
    }
    mock_optimizer.get_metrics.return_value = {
        'total_messages': 100,
        'optimized_messages': 85,
        'efficiency_rate': 0.85
    }
    return mock_optimizer


@pytest.fixture
def budget_manager():
    """Mock dynamic budget manager fixture for testing"""
    from unittest.mock import Mock

    mock_budget_manager = Mock()
    mock_budget_manager.total_budget = 1000.0
    mock_budget_manager.allocate_budget.return_value = True
    mock_budget_manager.get_allocation.return_value = {
        'component': 'test_agent',
        'allocated': 250.0,
        'used': 180.5,
        'remaining': 69.5
    }
    mock_budget_manager.update_performance_metrics.return_value = None
    mock_budget_manager.get_efficiency.return_value = 0.87
    return mock_budget_manager


@pytest.fixture
def preference_learner(temp_directory):
    """Real UserPreferenceLearner fixture for testing"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

    from user_preference_learner import UserPreferenceLearner

    # Use the temp directory for preference storage
    learner = UserPreferenceLearner(storage_dir=temp_directory)
    return learner


@pytest.fixture
def intelligent_agent_router(temp_directory):
    """Mock IntelligentAgentRouter fixture for testing"""
    from unittest.mock import Mock

    mock_router = Mock()
    mock_router.route_task.return_value = {
        'success': True,
        'agent': 'test-agent',
        'confidence': 0.92,
        'reason': 'Task complexity and type match'
    }
    mock_router.get_routing_stats.return_value = {
        'total_tasks': 50,
        'successful_routes': 48,
        'average_confidence': 0.89
    }
    return mock_router


@pytest.fixture
def learning_visualizer(temp_directory):
    """Mock LearningVisualizer fixture for testing"""
    from unittest.mock import Mock

    mock_visualizer = Mock()
    mock_visualizer.record_learning_event.return_value = True
    mock_visualizer.generate_learning_insights.return_value = {
        'insights': ['Pattern A improved by 15%', 'Success rate: 94%'],
        'trends': {'improving': True, 'rate': 0.23}
    }
    mock_visualizer.get_learning_events.return_value = []
    return mock_visualizer


@pytest.fixture
def predictive_skill_loader(temp_directory):
    """Mock PredictiveSkillLoader fixture for testing"""
    from unittest.mock import Mock

    mock_loader = Mock()
    mock_loader.predict_skills.return_value = [
        {'skill': 'code-analysis', 'confidence': 0.94, 'reason': 'High relevance'},
        {'skill': 'quality-standards', 'confidence': 0.87, 'reason': 'Type match'}
    ]
    mock_loader.update_skill_effectiveness.return_value = None
    mock_loader.get_prediction_accuracy.return_value = 0.91
    return mock_loader