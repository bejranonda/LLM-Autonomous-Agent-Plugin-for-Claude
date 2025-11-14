"""
Integration tests for Autonomous Agent Plugin core components

Tests the integration between:
- Pattern Storage and Quality Tracker
- Learning Engine and Feedback System
- Plugin Path Resolver and all components
- Cross-platform file operations
- End-to-end workflows
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

# Add lib directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from pattern_storage import PatternStorage
from quality_tracker import QualityTracker
from learning_engine import LearningEngine
from agent_feedback_system import AgentFeedbackSystem
from plugin_path_resolver import get_plugin_path, get_script_path


class TestCoreIntegration:
    """Integration tests for core components"""

    @pytest.fixture
    def integrated_system(self, temp_directory):
        """Create an integrated system with all components sharing the same directory"""
        return {
            'pattern_storage': PatternStorage(temp_directory),
            'quality_tracker': QualityTracker(temp_directory),
            'learning_engine': LearningEngine(temp_directory),
            'feedback_system': AgentFeedbackSystem(temp_directory),
            'data_dir': temp_directory
        }

    @pytest.fixture
    def sample_task_data(self):
        """Complete sample task data for integration testing"""
        return {
            'task_id': 'integration_task_001',
            'task_type': 'feature_implementation',
            'context': 'Implement user authentication with JWT',
            'quality_score': 0.87,
            'metrics': {
                'code_quality': 0.90,
                'test_quality': 0.85,
                'documentation': 0.80,
                'patterns': 0.95,
                'performance': 0.86
            },
            'skills_used': ['code-analysis', 'security-audit', 'testing'],
            'approach': 'JWT-based authentication with refresh tokens',
            'execution_time_seconds': 240,
            'agents_involved': ['code-analyzer', 'quality-controller', 'test-engineer']
        }

    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_complete_task_workflow(self, integrated_system, sample_task_data):
        """Test complete task execution workflow across all components"""
        system = integrated_system

        # 1. Initialize learning system
        project_context = {
            'type': 'web_application',
            'frameworks': ['fastapi', 'react'],
            'detected_languages': ['python', 'javascript']
        }

        init_result = system['learning_engine'].initialize_learning_system(project_context)
        assert init_result['status'] == 'initialized'

        # 2. Store task pattern
        pattern_data = {
            'task_type': sample_task_data['task_type'],
            'context': sample_task_data['context'],
            'skills_used': sample_task_data['skills_used'],
            'approach': sample_task_data['approach'],
            'quality_score': sample_task_data['quality_score']
        }

        pattern_id = system['pattern_storage'].store_pattern(pattern_data)
        assert pattern_id is not None

        # 3. Record quality assessment
        quality_result = system['quality_tracker'].record_quality(
            sample_task_data['task_id'],
            sample_task_data['quality_score'],
            sample_task_data['metrics']
        )
        assert quality_result is True

        # 4. Add quality assessment to learning engine
        learning_quality_result = system['learning_engine'].add_quality_assessment({
            'task_id': sample_task_data['task_id'],
            'quality_score': sample_task_data['quality_score'],
            'metrics': sample_task_data['metrics']
        })
        assert learning_quality_result['status'] == 'success'

        # 5. Capture pattern in learning engine
        capture_result = system['learning_engine'].capture_pattern({
            'task_type': sample_task_data['task_type'],
            'context': sample_task_data['context'],
            'approach': sample_task_data['approach'],
            'skills_used': sample_task_data['skills_used'],
            'quality_score': sample_task_data['quality_score'],
            'execution_time_seconds': sample_task_data['execution_time_seconds'],
            'agents_involved': sample_task_data['agents_involved']
        })
        assert capture_result['status'] == 'success'

        # 6. Add feedback between agents
        feedback_id = system['feedback_system'].add_feedback(
            from_agent='quality-controller',
            to_agent='code-analyzer',
            task_id=sample_task_data['task_id'],
            feedback_type='success',
            message='Code quality exceeded expectations',
            impact='quality_score +8 points'
        )
        assert feedback_id is not None

        # 7. Verify data consistency across systems
        # Check pattern storage
        patterns = system['pattern_storage']._read_patterns()
        assert len(patterns) == 1
        assert patterns[0]['pattern_id'] == pattern_id

        # Check quality tracker
        quality_records = system['quality_tracker']._read_quality_records()
        assert len(quality_records) == 1
        assert quality_records[0]['task_id'] == sample_task_data['task_id']

        # Check learning engine status
        status = system['learning_engine'].get_status()
        assert status['analytics']['total_patterns'] == 1
        assert status['analytics']['quality_assessments'] == 1

        # Check feedback system
        feedback_data = system['feedback_system']._read_data()
        assert len(feedback_data['feedback_exchanges']) == 1
        assert feedback_data['metadata']['total_feedbacks'] == 1

    @pytest.mark.integration
    def test_pattern_quality_correlation(self, integrated_system, sample_task_data):
        """Test correlation between patterns and quality metrics"""
        system = integrated_system

        # Initialize and add multiple tasks with varying quality
        tasks = []
        quality_scores = [0.65, 0.78, 0.92, 0.85, 0.71]

        for i, score in enumerate(quality_scores):
            task = sample_task_data.copy()
            task['task_id'] = f'correlation_task_{i}'
            task['quality_score'] = score
            task['metrics']['code_quality'] = score + 0.05  # Slightly higher
            tasks.append(task)

            # Store pattern
            pattern_data = {
                'task_type': task['task_type'],
                'context': task['context'],
                'skills_used': task['skills_used'],
                'approach': task['approach'],
                'quality_score': task['quality_score']
            }
            system['pattern_storage'].store_pattern(pattern_data)

            # Record quality
            system['quality_tracker'].record_quality(
                task['task_id'],
                task['quality_score'],
                task['metrics']
            )

        # Analyze correlation
        # Get skill effectiveness from pattern storage
        code_analysis_effectiveness = system['pattern_storage'].get_skill_effectiveness('code-analysis')
        assert code_analysis_effectiveness['usage_count'] == 5

        # Calculate success rate (quality >= 0.8 considered success)
        successful_tasks = sum(1 for score in quality_scores if score >= 0.8)
        expected_success_rate = successful_tasks / len(quality_scores)
        assert abs(code_analysis_effectiveness['success_rate'] - expected_success_rate) < 0.1

        # Get quality trends
        quality_trends = system['quality_tracker'].get_quality_trends()
        assert quality_trends['data_points'] == 5

        # Get average quality
        avg_quality = system['quality_tracker'].get_average_quality()
        expected_avg = sum(quality_scores) / len(quality_scores)
        assert abs(avg_quality - expected_avg) < 0.01

    @pytest.mark.integration
    def test_agent_feedback_loop(self, integrated_system):
        """Test feedback loop between agents"""
        system = integrated_system

        # Simulate agent workflow with feedback
        feedback_loop = [
            ('code-analyzer', 'quality-controller', 'success', 'Code analysis comprehensive'),
            ('quality-controller', 'test-engineer', 'improvement', 'Add more edge case tests'),
            ('test-engineer', 'code-analyzer', 'warning', 'Some unhandled exceptions found'),
            ('code-analyzer', 'test-engineer', 'success', 'Edge cases now handled'),
            ('test-engineer', 'quality-controller', 'success', 'All tests passing')
        ]

        feedback_ids = []
        for from_agent, to_agent, feedback_type, message in feedback_loop:
            feedback_id = system['feedback_system'].add_feedback(
                from_agent=from_agent,
                to_agent=to_agent,
                task_id='feedback_loop_task',
                feedback_type=feedback_type,
                message=message
            )
            feedback_ids.append(feedback_id)

        # Mark some feedback as applied
        system['feedback_system'].mark_feedback_applied(feedback_ids[1])
        system['feedback_system'].mark_feedback_applied(feedback_ids[3])

        # Get collaboration statistics
        stats = system['feedback_system'].get_collaboration_stats()
        assert stats['total_feedbacks'] == 5
        assert stats['feedback_effectiveness'] == 40.0  # 2 out of 5 applied

        # Get feedback for specific agent
        test_engineer_feedback = system['feedback_system'].get_feedback_for_agent('test-engineer')
        assert len(test_engineer_feedback) == 2  # Received from quality-controller and code-analyzer

        # Check most active collaboration pairs
        most_active = stats['most_active_pairs']
        assert len(most_active) > 0

    @pytest.mark.integration
    def test_learning_insights_generation(self, integrated_system, sample_task_data):
        """Test generation of learning insights from integrated data"""
        system = integrated_system

        # Execute multiple tasks to generate learning data
        task_scenarios = [
            {
                'task_type': 'feature_implementation',
                'context': 'User authentication',
                'quality_score': 0.90,
                'skills_used': ['security-audit', 'code-analysis']
            },
            {
                'task_type': 'bug_fix',
                'context': 'Memory leak in caching',
                'quality_score': 0.85,
                'skills_used': ['performance-analytics', 'debugging']
            },
            {
                'task_type': 'refactoring',
                'context': 'Optimize database queries',
                'quality_score': 0.88,
                'skills_used': ['performance-analytics', 'code-analysis']
            }
        ]

        # Execute tasks and capture data
        for scenario in task_scenarios:
            # Store pattern
            pattern_data = {
                'task_type': scenario['task_type'],
                'context': scenario['context'],
                'skills_used': scenario['skills_used'],
                'approach': f'Approach for {scenario["context"]}',
                'quality_score': scenario['quality_score']
            }
            system['pattern_storage'].store_pattern(pattern_data)

            # Record quality
            system['quality_tracker'].record_quality(
                f'task_{scenario["task_type"]}',
                scenario['quality_score'],
                {'overall': scenario['quality_score']}
            )

        # Generate learning insights based on patterns
        # Find most effective skill
        skill_effects = {}
        for scenario in task_scenarios:
            for skill in scenario['skills_used']:
                if skill not in skill_effects:
                    effectiveness = system['pattern_storage'].get_skill_effectiveness(skill)
                    skill_effects[skill] = effectiveness

        # Verify skill effectiveness tracking
        assert len(skill_effects) >= 2  # At least 2 different skills used
        assert all(effect['usage_count'] > 0 for effect in skill_effects.values())

        # Add learning insights based on analysis
        system['feedback_system'].add_learning_insight(
            insight_type='successful_collaboration',
            description='Performance analytics and code-analysis work well together',
            agents_involved=['performance-analytics', 'code-analysis'],
            impact='Average quality 87.3% when used together'
        )

        # Retrieve and verify insights
        insights = system['feedback_system'].get_insights()
        assert len(insights) >= 1

        collaboration_insights = system['feedback_system'].get_insights('successful_collaboration')
        assert len(collaboration_insights) >= 1

    @pytest.mark.integration
    def test_cross_platform_data_consistency(self, integrated_system, cross_platform_temp_dir):
        """Test data consistency across different platforms"""
        temp_dir, platform_info = cross_platform_temp_dir

        # Create system on this platform
        system = {
            'pattern_storage': PatternStorage(temp_dir),
            'quality_tracker': QualityTracker(temp_dir),
            'learning_engine': LearningEngine(temp_dir)
        }

        # Store data
        pattern_data = {
            'task_type': 'feature_implementation',
            'context': f'Cross-platform test on {platform_info["system"]}',
            'skills_used': ['testing'],
            'approach': 'Cross-platform approach',
            'quality_score': 0.85
        }

        pattern_id = system['pattern_storage'].store_pattern(pattern_data)
        system['quality_tracker'].record_quality('cross_platform_task', 0.85, {'test': 0.85})

        # Verify all files were created with platform-appropriate paths
        assert system['pattern_storage'].patterns_file.exists()
        assert system['quality_tracker'].quality_file.exists()
        assert system['learning_engine'].patterns_file.exists()

        # Verify data integrity (JSON should be consistent across platforms)
        patterns = system['pattern_storage']._read_patterns()
        assert len(patterns) == 1
        assert patterns[0]['pattern_id'] == pattern_id

        quality_records = system['quality_tracker']._read_quality_records()
        assert len(quality_records) == 1

        # Test path separator handling
        assert str(temp_dir).count(os.sep) >= 1  # Should contain platform-specific separators

    @pytest.mark.integration
    def test_error_propagation_and_recovery(self, integrated_system):
        """Test error handling and recovery across integrated systems"""
        system = integrated_system

        # Test graceful handling of corrupted data
        # Corrupt one file and ensure others still work
        with open(system['pattern_storage'].patterns_file, 'w') as f:
            f.write('invalid json content')

        # Pattern storage should recover
        patterns = system['pattern_storage']._read_patterns()
        assert patterns == []  # Should recover with empty list

        # Other systems should continue working
        quality_result = system['quality_tracker'].record_quality(
            'recovery_test', 0.90, {'test': 0.90}
        )
        assert quality_result is True

        # Test error isolation
        learning_result = system['learning_engine'].capture_pattern({
            'task_type': 'test',
            'context': 'recovery test'
        })
        assert learning_result['status'] == 'success'

    @pytest.mark.integration
    def test_performance_under_load(self, integrated_system):
        """Test system performance under realistic load"""
        import time
        system = integrated_system

        # Simulate realistic workload
        task_count = 100
        skills_pool = ['code-analysis', 'security-audit', 'testing', 'performance-analytics', 'documentation']

        start_time = time.time()

        # Process tasks
        for i in range(task_count):
            # Generate realistic task data
            task_data = {
                'task_type': ['feature_implementation', 'bug_fix', 'refactoring'][i % 3],
                'context': f'Task {i}: Implement functionality',
                'skills_used': skills_pool[:2],  # Use 2 skills per task
                'approach': f'Standard approach for task {i}',
                'quality_score': 0.6 + (i % 40) / 100.0  # Range from 0.6 to 0.99
            }

            # Store pattern
            system['pattern_storage'].store_pattern(task_data)

            # Record quality
            system['quality_tracker'].record_quality(
                f'task_{i}',
                task_data['quality_score'],
                {'code_quality': task_data['quality_score']}
            )

        processing_time = time.time() - start_time

        # Performance assertions
        assert processing_time < 10.0  # Should complete within 10 seconds
        assert len(system['pattern_storage']._read_patterns()) == task_count
        assert len(system['quality_tracker']._read_quality_records()) == task_count

        # Test analytics performance
        start_time = time.time()
        stats = system['pattern_storage'].get_statistics()
        quality_trends = system['quality_tracker'].get_quality_trends()
        analytics_time = time.time() - start_time

        assert analytics_time < 2.0  # Analytics should be fast
        assert stats['total_patterns'] == task_count
        assert quality_trends['data_points'] == task_count

    @pytest.mark.integration
    def test_data_consolidation_workflow(self, integrated_system, sample_task_data):
        """Test unified data consolidation workflow"""
        system = integrated_system

        # Add data to multiple systems
        # Pattern storage
        system['pattern_storage'].store_pattern({
            'task_type': sample_task_data['task_type'],
            'context': sample_task_data['context'],
            'skills_used': sample_task_data['skills_used'],
            'approach': sample_task_data['approach'],
            'quality_score': sample_task_data['quality_score']
        })

        # Quality tracker
        system['quality_tracker'].record_quality(
            sample_task_data['task_id'],
            sample_task_data['quality_score'],
            sample_task_data['metrics']
        )

        # Learning engine
        system['learning_engine'].initialize_learning_system({
            'type': 'integration_test',
            'frameworks': ['pytest']
        })

        # Agent feedback system
        system['feedback_system'].add_feedback(
            from_agent='test-agent',
            to_agent='integration-agent',
            task_id=sample_task_data['task_id'],
            feedback_type='success',
            message='Integration test successful'
        )

        # Consolidate data
        consolidation_success = system['pattern_storage'].consolidate_all_data()
        assert consolidation_success is True

        # Verify consolidated file exists
        unified_file = Path(system['data_dir']) / "unified_data.json"
        assert unified_file.exists()

        # Verify consolidated content
        with open(unified_file, 'r') as f:
            unified_data = json.load(f)

        assert 'patterns' in unified_data
        assert 'skill_metrics' in unified_data
        assert 'agent_metrics' in unified_data
        assert 'quality_history' in unified_data
        assert 'performance_records' in unified_data
        assert 'system_health' in unified_data
        assert 'project_context' in unified_data

        # Verify data migration
        assert len(unified_data['patterns']) >= 1
        assert unified_data['system_health']['status'] == 'healthy'

    @pytest.mark.integration
    def test_plugin_discovery_integration(self, integrated_system):
        """Test integration with plugin path discovery"""
        system = integrated_system

        # Create mock plugin structure in data directory
        plugin_dir = Path(system['data_dir']) / "mock_plugin"
        plugin_dir.mkdir()

        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()

        (claude_plugin_dir / "plugin.json").write_text('{"name": "Mock Plugin", "version": "1.0.0"}')

        lib_dir = plugin_dir / "lib"
        lib_dir.mkdir()

        # Test script resolution
        with patch('plugin_path_resolver.get_plugin_path', return_value=plugin_dir):
            from plugin_path_resolver import get_script_path

            # Create test script
            test_script = lib_dir / "test_integration.py"
            test_script.write_text("# Integration test script")

            resolved_path = get_script_path("test_integration.py")
            assert resolved_path is not None
            assert resolved_path.name == "test_integration.py"

            # Test non-existent script
            nonexistent = get_script_path("nonexistent.py")
            assert nonexistent is None

    @pytest.mark.integration
    def test_comprehensive_system_status(self, integrated_system, sample_task_data):
        """Test comprehensive system status reporting"""
        system = integrated_system

        # Add comprehensive data
        # 1. Multiple patterns
        for i in range(5):
            pattern = {
                'task_type': ['feature', 'bug_fix', 'refactor'][i % 3],
                'context': f'Task {i} context',
                'skills_used': ['skill1', 'skill2'],
                'approach': f'Approach {i}',
                'quality_score': 0.7 + (i * 0.05)
            }
            system['pattern_storage'].store_pattern(pattern)

        # 2. Quality history
        for i in range(3):
            system['quality_tracker'].record_quality(
                f'quality_task_{i}',
                0.8 + (i * 0.05),
                {'metric1': 0.8, 'metric2': 0.85}
            )

        # 3. Learning engine data
        system['learning_engine'].initialize_learning_system({
            'type': 'comprehensive_test',
            'frameworks': ['pytest', 'unittest']
        })

        # 4. Feedback data
        for i in range(4):
            system['feedback_system'].add_feedback(
                f'agent_{i}',
                f'agent_{(i + 1) % 4}',
                f'task_{i}',
                ['success', 'improvement'][i % 2],
                f'Feedback message {i}'
            )

        # Generate comprehensive status
        status_report = {
            'pattern_storage': system['pattern_storage'].get_statistics(),
            'quality_tracker': {
                'total_records': len(system['quality_tracker']._read_quality_records()),
                'average_quality': system['quality_tracker'].get_average_quality(),
                'trends': system['quality_tracker'].get_quality_trends()
            },
            'learning_engine': system['learning_engine'].get_status(),
            'feedback_system': system['feedback_system'].get_collaboration_stats(),
            'system_health': {
                'total_files': len(list(Path(system['data_dir']).glob("*.json"))),
                'data_integrity': 'verified'
            }
        }

        # Verify comprehensive status
        assert status_report['pattern_storage']['total_patterns'] == 5
        assert status_report['quality_tracker']['total_records'] == 3
        assert status_report['learning_engine']['analytics']['total_patterns'] == 0  # Separate from pattern_storage
        assert status_report['feedback_system']['total_feedbacks'] == 4
        assert status_report['system_health']['total_files'] >= 4  # At least 4 JSON files

        # Verify data consistency
        assert status_report['quality_tracker']['average_quality'] > 0.8
        assert status_report['quality_tracker']['trends']['data_points'] == 3
        assert status_report['learning_engine']['system_status'] == 'operational'