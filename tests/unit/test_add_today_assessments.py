#!/usr/bin/env python3
"""
Test suite for add_today_assessments.py
Boosts test coverage by focusing on assessment functionality and data management.
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
from datetime import datetime

# Add the lib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from add_today_assessments import add_todays_assessments


class TestAddTodayAssessments:
    """Test cases for add_today_assessments function."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.unified_dir = Path(self.temp_dir) / ".claude-unified"
        self.unified_dir.mkdir(parents=True)
        self.unified_file = self.unified_dir / "unified_parameters.json"

        # Create initial unified parameters structure
        initial_data = {
            "version": "1.0.0",
            "metadata": {
                "last_updated": "2025-01-01T00:00:00",
                "total_records_migrated": 0
            },
            "quality": {
                "assessments": {
                    "history": []
                }
            }
        }

        with open(self.unified_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=2, ensure_ascii=False)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_add_todays_assessments_success(self):
        """Test successful addition of today's assessments."""
        # Mock the working directory
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            result = add_todays_assessments()

        assert result is True

        # Check that assessments were added
        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]
        assert len(history) == 4  # Should add 4 assessments

        # Check specific assessments were added
        assessment_ids = [assessment["assessment_id"] for assessment in history]
        expected_ids = [
            "readme-update-v5.4.0-20251029-160800",
            "git-commit-readme-20251029-160900",
            "dashboard-monitoring-20251029-161000",
            "debugging-dashboard-issues-20251029-161500"
        ]

        for expected_id in expected_ids:
            assert expected_id in assessment_ids

    def test_add_todays_assessments_updates_metadata(self):
        """Test that metadata is updated correctly."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        metadata = data["metadata"]
        assert metadata["total_records_migrated"] == 4
        assert metadata["last_updated"] != "2025-01-01T00:00:00"  # Should be updated

    def test_add_todays_assessments_creates_backup(self):
        """Test that backup file is created."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        # Check backup file exists
        backup_file = self.unified_file.with_suffix(".json.backup")
        assert backup_file.exists()

        # Check backup contains original data
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        assert backup_data["quality"]["assessments"]["history"] == []  # Original empty history

    def test_assessment_data_structure(self):
        """Test that added assessments have correct structure."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]
        readme_assessment = next(
            (a for a in history if a["assessment_id"] == "readme-update-v5.4.0-20251029-160800"),
            None
        )

        assert readme_assessment is not None

        # Check required fields
        required_fields = [
            "assessment_id", "timestamp", "overall_score", "pass", "task_type",
            "breakdown", "details", "issues_found", "recommendations", "skills_used"
        ]

        for field in required_fields:
            assert field in readme_assessment

        # Check specific values
        assert readme_assessment["overall_score"] == 95
        assert readme_assessment["pass"] is True
        assert readme_assessment["task_type"] == "documentation"
        assert "files_modified" in readme_assessment["details"]
        assert "duration_seconds" in readme_assessment["details"]

    def test_assessment_breakdown_structure(self):
        """Test that assessment breakdowns have correct structure."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]
        commit_assessment = next(
            (a for a in history if a["assessment_id"] == "git-commit-readme-20251029-160900"),
            None
        )

        breakdown = commit_assessment["breakdown"]
        expected_keys = ["commit_quality", "message_clarity", "file_staging", "best_practices", "documentation"]

        for key in expected_keys:
            assert key in breakdown
            assert isinstance(breakdown[key], (int, float))
            assert breakdown[key] > 0

        # Check total adds up
        total = sum(breakdown.values())
        assert total == 100  # Should total 100 points

    def test_assessment_recommendations(self):
        """Test that assessments include recommendations."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]
        dashboard_assessment = next(
            (a for a in history if a["assessment_id"] == "dashboard-monitoring-20251029-161000"),
            None
        )

        recommendations = dashboard_assessment["recommendations"]
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all(isinstance(rec, str) for rec in recommendations)

    def test_assessment_issues_found(self):
        """Test that assessments record issues found."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]
        debugging_assessment = next(
            (a for a in history if a["assessment_id"] == "debugging-dashboard-issues-20251029-161500"),
            None
        )

        issues_found = debugging_assessment["issues_found"]
        assert isinstance(issues_found, list)
        assert len(issues_found) > 0
        assert all(isinstance(issue, str) for issue in issues_found)

    def test_assessment_skills_used(self):
        """Test that assessments record skills used."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]
        readme_assessment = next(
            (a for a in history if a["assessment_id"] == "readme-update-v5.4.0-20251029-160800"),
            None
        )

        skills_used = readme_assessment["skills_used"]
        assert isinstance(skills_used, list)
        assert len(skills_used) > 0
        assert "documentation-best-practices" in skills_used
        assert "pattern-learning" in skills_used

    def test_add_to_existing_history(self):
        """Test adding assessments to existing history."""
        # Add some existing assessments
        existing_assessment = {
            "assessment_id": "existing-assessment-001",
            "timestamp": "2025-01-01T10:00:00",
            "overall_score": 80,
            "pass": True,
            "task_type": "existing",
            "breakdown": {"test": 100},
            "details": {"test": "data"},
            "issues_found": [],
            "recommendations": [],
            "skills_used": []
        }

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        data["quality"]["assessments"]["history"].append(existing_assessment)

        with open(self.unified_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Add today's assessments
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        # Check both old and new assessments are present
        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]
        assert len(history) == 5  # 1 existing + 4 new

        assessment_ids = [a["assessment_id"] for a in history]
        assert "existing-assessment-001" in assessment_ids
        assert "readme-update-v5.4.0-20251029-160800" in assessment_ids

    def test_file_not_found_error(self):
        """Test handling when unified file doesn't exist."""
        # Remove the unified file
        self.unified_file.unlink()

        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            # Should handle FileNotFoundError gracefully
            with pytest.raises(FileNotFoundError):
                add_todays_assessments()

    def test_invalid_json_error(self):
        """Test handling when unified file contains invalid JSON."""
        # Write invalid JSON
        with open(self.unified_file, 'w') as f:
            f.write("{ invalid json content")

        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            # Should handle JSONDecodeError gracefully
            with pytest.raises(json.JSONDecodeError):
                add_todays_assessments()

    def test_timestamp_format(self):
        """Test that assessment timestamps are in correct format."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]

        for assessment in history:
            timestamp = assessment["timestamp"]
            # Should be parseable as ISO format
            parsed_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00') if timestamp.endswith('Z') else timestamp)
            assert isinstance(parsed_time, datetime)

    def test_assessment_scores_range(self):
        """Test that assessment scores are within valid ranges."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]

        for assessment in history:
            overall_score = assessment["overall_score"]
            assert isinstance(overall_score, (int, float))
            assert 0 <= overall_score <= 100

            # Check breakdown scores
            for score in assessment["breakdown"].values():
                assert isinstance(score, (int, float))
                assert 0 <= score <= 100

    def test_assessment_pass_consistency(self):
        """Test that pass status is consistent with scores."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]

        for assessment in history:
            score = assessment["overall_score"]
            passed = assessment["pass"]

            # Generally, scores >= 70 should pass
            if score >= 70:
                assert passed is True
            else:
                assert passed is False

    def test_unique_assessment_ids(self):
        """Test that all assessment IDs are unique."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]
        assessment_ids = [a["assessment_id"] for a in history]

        # All IDs should be unique
        assert len(assessment_ids) == len(set(assessment_ids))

    def test_task_type_coverage(self):
        """Test that different task types are represented."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        with open(self.unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data["quality"]["assessments"]["history"]
        task_types = set(a["task_type"] for a in history)

        # Should include multiple task types
        expected_types = ["documentation", "development", "monitoring", "debugging"]
        for expected_type in expected_types:
            assert expected_type in task_types

    @patch('builtins.print')
    def test_output_messages(self, mock_print):
        """Test that appropriate messages are printed."""
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            add_todays_assessments()

        # Check that success messages were printed
        print_calls = [str(call) for call in mock_print.call_args_list]

        success_found = any("[OK] Added 4 assessments" in call for call in print_calls)
        backup_found = any("[INFO] Backup saved to:" in call for call in print_calls)
        total_found = any("[INFO] Total assessments now: 4" in call for call in print_calls)

        assert success_found
        assert backup_found
        assert total_found

    def test_main_function(self):
        """Test the main function execution."""
        # Test that the main function can be called without errors
        with patch('pathlib.Path.cwd', return_value=Path(self.temp_dir)):
            # Import and call main
            from add_today_assessments import main

            # Should not raise an exception
            try:
                main()
                success = True
            except Exception:
                success = False

            assert success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])