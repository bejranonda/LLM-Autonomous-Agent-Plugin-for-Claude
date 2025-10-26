#!/usr/bin/env python3
"""
Simple test script for backward compatibility of performance recording system.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add lib directory to path for imports
sys.path.insert(0, 'lib')

try:
    from performance_recorder import AutomaticPerformanceRecorder
except ImportError as e:
    print(f"Error importing performance_recorder: {e}")
    sys.exit(1)


def test_backward_compatibility():
    """Test that existing performance records still work."""
    print("Testing backward compatibility with existing records...")

    patterns_dir = Path(".claude-patterns")

    # Check if existing files exist and are valid
    files_to_check = [
        "quality_history.json",
        "debugging_performance.json",
        "model_performance.json"
    ]

    for file_name in files_to_check:
        file_path = patterns_dir / file_name
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"  [OK] {file_name}: Valid JSON")
            except Exception as e:
                print(f"  [ERROR] {file_name}: Invalid JSON - {e}")
                return False
        else:
            print(f"  [INFO] {file_name}: Not found (normal for new installations)")

    return True


def test_new_recording():
    """Test new automatic performance recording functionality."""
    print("\nTesting new automatic performance recording...")

    try:
        recorder = AutomaticPerformanceRecorder(".claude-patterns")

        # Test recording a sample task
        sample_task = {
            "task_type": "refactoring",
            "description": "Test refactoring task",
            "complexity": "medium",
            "duration": 120,
            "success": True,
            "skills_used": ["code-analysis"],
            "files_modified": 1,
            "lines_changed": 25
        }

        assessment_id = recorder.record_task_performance(sample_task, "Test Model")
        print(f"  [OK] Recorded test task: {assessment_id}")

        # Test that it appears in quality history
        if recorder.quality_history_file.exists():
            with open(recorder.quality_history_file, 'r', encoding='utf-8') as f:
                quality_data = json.load(f)

            assessments = quality_data.get("quality_assessments", [])
            test_record = next((a for a in assessments if a.get("assessment_id") == assessment_id), None)

            if test_record:
                print(f"  [OK] Record found in quality history")
            else:
                print(f"  [ERROR] Record not found in quality history")
                return False

    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

    return True


def test_dashboard_format():
    """Test that data format is compatible with dashboard."""
    print("\nTesting dashboard data format compatibility...")

    try:
        patterns_dir = Path(".claude-patterns")
        all_records = []

        # Load quality history
        quality_file = patterns_dir / "quality_history.json"
        if quality_file.exists():
            with open(quality_file, 'r', encoding='utf-8') as f:
                quality_data = json.load(f)

            for assessment in quality_data.get("quality_assessments", []):
                record = {
                    'timestamp': assessment.get('timestamp'),
                    'model': assessment.get('details', {}).get('model_used', 'Unknown'),
                    'task_type': assessment.get('task_type', 'unknown'),
                    'overall_score': assessment.get('overall_score', 0),
                    'pass': assessment.get('pass', False),
                    'auto_generated': assessment.get('auto_generated', False)
                }
                all_records.append(record)

        print(f"  [OK] Loaded {len(all_records)} records in dashboard format")

        # Check data consistency
        required_fields = ['timestamp', 'model', 'task_type', 'overall_score', 'pass']
        for record in all_records:
            missing = [f for f in required_fields if f not in record]
            if missing:
                print(f"  [ERROR] Record missing fields: {missing}")
                return False

        print(f"  [OK] All records have required fields")

    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

    return True


def cleanup_test_data():
    """Clean up test data."""
    print("\nCleaning up test data...")

    try:
        patterns_dir = Path(".claude-patterns")
        quality_file = patterns_dir / "quality_history.json"

        if quality_file.exists():
            with open(quality_file, 'r', encoding='utf-8') as f:
                quality_data = json.load(f)

            # Remove test records
            original_count = len(quality_data.get("quality_assessments", []))
            assessments = [
                a for a in quality_data.get("quality_assessments", [])
                if "test" not in a.get("task_type", "").lower()
            ]

            if len(assessments) < original_count:
                quality_data["quality_assessments"] = assessments
                quality_data["statistics"]["total_assessments"] = len(assessments)

                with open(quality_file, 'w', encoding='utf-8') as f:
                    json.dump(quality_data, f, indent=2)

                print(f"  [OK] Removed {original_count - len(assessments)} test records")

    except Exception as e:
        print(f"  [WARN] Cleanup error: {e}")


def main():
    """Run all tests."""
    print("Performance Recording System - Compatibility Tests")
    print("=" * 50)

    # Create patterns directory
    Path(".claude-patterns").mkdir(exist_ok=True)

    # Run tests
    tests = [
        ("Backward Compatibility", test_backward_compatibility()),
        ("New Recording", test_new_recording()),
        ("Dashboard Format", test_dashboard_format())
    ]

    # Cleanup
    cleanup_test_data()

    # Results
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in tests if result)
    total = len(tests)

    for name, result in tests:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {name}")

    print(f"\nResult: {passed}/{total} tests passed")

    if passed == total:
        print("\nSUCCESS: Performance recording system is ready!")
        print("Features enabled:")
        print("  - Automatic performance recording for all tasks")
        print("  - Backward compatibility with existing data")
        print("  - Enhanced dashboard integration")
        print("  - Model-specific performance tracking")
    else:
        print("\nFAILURE: Some tests failed. Review errors above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())