"""
Test configuration and fixtures for Autonomous Agent Plugin v6.0.0

This module provides common test utilities, fixtures, and configuration
for testing all 8 Phase 1 learning systems.
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
        "version": "6.0.0",
        "description": "Revolutionary Two-Tier Architecture with Learning Systems"
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