#!/usr/bin/env python3
"""
Test script for backward compatibility of performance recording system.

This script tests:
1. Backward compatibility with existing performance records
2. New automatic performance recording functionality
3. Dashboard integration with mixed data sources
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add lib directory to path for imports
sys.path.insert(0, 'lib')

try:
    from performance_recorder import AutomaticPerformanceRecorder
except ImportError as e:
    print(f"Error importing performance_recorder: {e}")
    print("Make sure the lib/performance_recorder.py file exists")
    sys.exit(1)


def test_backward_compatibility():
    """Test that existing performance records still work."""
    print("Testing backward compatibility with existing records...")

    # Check existing files exist
    patterns_dir = Path(".claude-patterns")
    required_files = [
        "quality_history.json",
        "debugging_performance.json",
        "model_performance.json"
    ]

    missing_files = []
    for file_name in required_files:
        file_path = patterns_dir / file_name
        if not file_path.exists():
            missing_files.append(file_name)
        else:
            print(f"  [OK] Found existing file: {file_name}")

    if missing_files:
        print(f"  [WARN] Missing expected files: {missing_files}")
        print("  This is normal for new installations")

    # Test loading existing data
    try:
        quality_file = patterns_dir / "quality_history.json"
        if quality_file.exists():
            with open(quality_file, 'r', encoding='utf-8') as f:
                quality_data = json.load(f)

            assessments = quality_data.get("quality_assessments", [])
            print(f"  ✓ Loaded {len(assessments)} existing quality assessments")

            # Check data structure compatibility
            if assessments:
                sample_assessment = assessments[0]
                required_fields = ["assessment_id", "timestamp", "task_type", "overall_score"]
                missing_fields = [field for field in required_fields if field not in sample_assessment]

                if missing_fields:
                    print(f"  [FAIL] Existing assessments missing required fields: {missing_fields}")
                    return False
                else:
                    print(f"  [OK] Existing assessments have compatible structure")

        # Test debugging performance data
        debug_file = patterns_dir / "debugging_performance.json"
        if debug_file.exists():
            with open(debug_file, 'r', encoding='utf-8') as f:
                debug_data = json.load(f)

            rankings = debug_data.get("performance_rankings", [])
            print(f"  ✓ Loaded {len(rankings)} existing performance rankings")

    except Exception as e:
        print(f"  ❌ Error loading existing data: {e}")
        return False

    return True


def test_new_performance_recording():
    """Test new automatic performance recording functionality."""
    print("\n🆕 Testing new automatic performance recording...")

    try:
        recorder = AutomaticPerformanceRecorder(".claude-patterns")

        # Test recording a sample task
        sample_task = {
            "task_type": "refactoring",
            "description": "Test refactoring task for performance recording",
            "complexity": "medium",
            "duration": 120,  # 2 minutes
            "success": True,
            "skills_used": ["code-analysis", "quality-standards"],
            "agents_delegated": ["code-analyzer"],
            "files_modified": 2,
            "lines_changed": 45,
            "quality_improvement": 8,
            "issues_found": ["Minor style issue"],
            "recommendations": ["Add unit tests"],
            "best_practices_followed": True,
            "documentation_updated": False
        }

        assessment_id = recorder.record_task_performance(sample_task, "Test Model")
        print(f"  ✓ Recorded test task with ID: {assessment_id}")

        # Test performance summary
        summary = recorder.get_performance_summary(30)
        print(f"  ✓ Generated performance summary: {summary['total_tasks']} tasks")

        # Check that files were created/updated
        if recorder.performance_records_file.exists():
            with open(recorder.performance_records_file, 'r', encoding='utf-8') as f:
                perf_data = json.load(f)
            records = perf_data.get("records", [])
            print(f"  ✓ Performance records file contains {len(records)} records")

        # Verify compatibility with quality history
        if recorder.quality_history_file.exists():
            with open(recorder.quality_history_file, 'r', encoding='utf-8') as f:
                quality_data = json.load(f)
            assessments = quality_data.get("quality_assessments", [])
            print(f"  ✓ Quality history contains {len(assessments)} assessments")

            # Check that our new record is there
            test_record = next((a for a in assessments if a.get("assessment_id") == assessment_id), None)
            if test_record:
                print(f"  ✓ New record successfully added to quality history")
            else:
                print(f"  ❌ New record not found in quality history")
                return False

    except Exception as e:
        print(f"  ❌ Error in new performance recording: {e}")
        return False

    return True


def test_dashboard_compatibility():
    """Test that dashboard can handle mixed old and new data."""
    print("\n📊 Testing dashboard compatibility...")

    try:
        # Simulate the API endpoint logic from dashboard.py
        patterns_dir = Path(".claude-patterns")
        all_records = []

        # Load quality history (new auto-recorded + existing assessments)
        quality_file = patterns_dir / "quality_history.json"
        if quality_file.exists():
            with open(quality_file, 'r', encoding='utf-8') as f:
                quality_data = json.load(f)

            for assessment in quality_data.get("quality_assessments", []):
                model = assessment.get("details", {}).get("model_used", "Claude Sonnet 4.5")
                record = {
                    'timestamp': assessment.get('timestamp'),
                    'model': model,
                    'assessment_id': assessment.get('assessment_id'),
                    'task_type': assessment.get('task_type', 'unknown'),
                    'overall_score': assessment.get('overall_score', 0),
                    'performance_index': assessment.get('details', {}).get('performance_index', 0),
                    'evaluation_target': assessment.get('details', {}).get('evaluation_target', assessment.get('task_type', 'Unknown')),
                    'quality_improvement': assessment.get('details', {}).get('quality_improvement', 0),
                    'issues_found': len(assessment.get('issues_found', [])),
                    'fixes_applied': assessment.get('details', {}).get('fixes_applied', 0),
                    'time_elapsed_minutes': assessment.get('details', {}).get('duration_seconds', 0) / 60,
                    'success_rate': 100 if assessment.get('pass', False) else 0,
                    'pass': assessment.get('pass', False),
                    'auto_generated': assessment.get('auto_generated', False)
                }
                all_records.append(record)

        # Load performance records (new format)
        perf_records_file = patterns_dir / "performance_records.json"
        if perf_records_file.exists():
            with open(perf_records_file, 'r', encoding='utf-8') as f:
                perf_data = json.load(f)

            for record in perf_data.get('records', []):
                dashboard_record = {
                    'timestamp': record.get('timestamp'),
                    'model': record.get('model_used', 'Claude Sonnet 4.5'),
                    'assessment_id': record.get('assessment_id'),
                    'task_type': record.get('task_type', 'unknown'),
                    'overall_score': record.get('overall_score', 0),
                    'performance_index': record.get('details', {}).get('performance_index', 0),
                    'evaluation_target': record.get('task_type', 'Unknown'),
                    'quality_improvement': record.get('details', {}).get('quality_improvement', 0),
                    'issues_found': len(record.get('issues_found', [])),
                    'fixes_applied': record.get('details', {}).get('fixes_applied', 0),
                    'time_elapsed_minutes': record.get('details', {}).get('duration_seconds', 0) / 60,
                    'success_rate': 100 if record.get('pass', False) else 0,
                    'pass': record.get('pass', False),
                    'auto_generated': record.get('auto_generated', True)
                }
                all_records.append(dashboard_record)

        # Load debugging performance (existing format)
        debug_file = patterns_dir / "debugging_performance.json"
        if debug_file.exists():
            with open(debug_file, 'r', encoding='utf-8') as f:
                debug_data = json.load(f)

            for model_name, model_data in debug_data.get('detailed_metrics', {}).items():
                for assessment in model_data.get('debugging_assessments', []):
                    record = {
                        'timestamp': assessment.get('timestamp'),
                        'model': model_name,
                        'assessment_id': assessment.get('assessment_id'),
                        'task_type': assessment.get('task_type', 'debugging'),
                        'overall_score': assessment.get('overall_score', 0),
                        'performance_index': assessment.get('details', {}).get('performance_index', 0),
                        'evaluation_target': assessment.get('details', {}).get('evaluation_target', 'Unknown'),
                        'quality_improvement': assessment.get('details', {}).get('quality_improvement', 0),
                        'issues_found': len(assessment.get('issues_found', [])),
                        'fixes_applied': assessment.get('details', {}).get('fixes_applied', 0),
                        'time_elapsed_minutes': assessment.get('details', {}).get('time_elapsed_minutes', 0),
                        'success_rate': assessment.get('details', {}).get('success_rate', 0) * 100,
                        'pass': assessment.get('pass', False),
                        'auto_generated': False
                    }
                    all_records.append(record)

        # Test data consistency
        print(f"  ✓ Loaded {len(all_records)} total records from all sources")

        # Check for required fields in all records
        required_fields = ['timestamp', 'model', 'task_type', 'overall_score', 'pass']
        inconsistent_records = []

        for i, record in enumerate(all_records):
            missing_fields = [field for field in required_fields if field not in record or record[field] is None]
            if missing_fields:
                inconsistent_records.append((i, missing_fields))

        if inconsistent_records:
            print(f"  ❌ Found {len(inconsistent_records)} records with missing fields")
            for idx, fields in inconsistent_records[:3]:  # Show first 3
                print(f"    Record {idx}: missing {fields}")
            return False
        else:
            print(f"  ✓ All records have consistent structure")

        # Test task type diversity
        task_types = set(record.get('task_type', 'unknown') for record in all_records)
        print(f"  ✓ Found {len(task_types)} different task types: {sorted(task_types)}")

        # Test model diversity
        models = set(record.get('model', 'unknown') for record in all_records)
        print(f"  ✓ Found {len(models)} different models: {sorted(models)}")

        # Test auto vs manual classification
        auto_count = sum(1 for record in all_records if record.get('auto_generated', False))
        manual_count = len(all_records) - auto_count
        print(f"  ✓ Classification: {auto_count} auto-generated, {manual_count} manual assessments")

    except Exception as e:
        print(f"  ❌ Error in dashboard compatibility test: {e}")
        return False

    return True


def cleanup_test_data():
    """Clean up test data created during testing."""
    print("\n🧹 Cleaning up test data...")

    try:
        patterns_dir = Path(".claude-patterns")

        # Remove test record from quality history if it exists
        quality_file = patterns_dir / "quality_history.json"
        if quality_file.exists():
            with open(quality_file, 'r', encoding='utf-8') as f:
                quality_data = json.load(f)

            original_count = len(quality_data.get("quality_assessments", []))

            # Remove test records (those with "test" indicators)
            assessments = quality_data.get("quality_assessments", [])
            filtered_assessments = []

            for a in assessments:
                # Remove if test indicators found
                task_type = a.get("task_type", "").lower()
                task_desc = a.get("details", {}).get("task_description", "").lower()
                model_used = a.get("details", {}).get("model_used", "").lower()
                assessment_id = a.get("assessment_id", "").lower()

                is_test = ("test" in task_type or
                          "test" in task_desc or
                          "test" in model_used or
                          "test" in assessment_id or
                          a.get("auto_generated", False) and "test" in task_type)

                if not is_test:
                    filtered_assessments.append(a)

            if len(filtered_assessments) < original_count:
                quality_data["quality_assessments"] = filtered_assessments

                # Update statistics
                total_assessments = len(filtered_assessments)
                if total_assessments > 0:
                    passing_assessments = sum(1 for a in filtered_assessments if a.get("pass", False))
                    avg_score = sum(a.get("overall_score", 0) for a in filtered_assessments) / total_assessments
                else:
                    passing_assessments = 0
                    avg_score = 0

                quality_data["statistics"] = {
                    "avg_quality_score": round(avg_score, 1),
                    "total_assessments": total_assessments,
                    "passing_rate": passing_assessments / total_assessments if total_assessments > 0 else 0,
                    "trend": quality_data["statistics"].get("trend", "stable")
                }

                # Update last assessment timestamp
                if filtered_assessments:
                    last_timestamp = max(a.get("timestamp", "") for a in filtered_assessments)
                    quality_data["metadata"]["last_assessment"] = last_timestamp
                else:
                    quality_data["metadata"]["last_assessment"] = ""

                # Update auto recording count
                auto_count = sum(1 for a in filtered_assessments if a.get("auto_generated", False))
                quality_data["metadata"]["auto_recording_count"] = auto_count

                with open(quality_file, 'w', encoding='utf-8') as f:
                    json.dump(quality_data, f, indent=2, ensure_ascii=False)

                print(f"  ✓ Removed {original_count - len(filtered_assessments)} test records from quality history")

        # Remove test models from model performance
        model_perf_file = patterns_dir / "model_performance.json"
        if model_perf_file.exists():
            with open(model_perf_file, 'r', encoding='utf-8') as f:
                model_data = json.load(f)

            original_count = len(model_data)

            # Remove test models
            filtered_models = {}
            for model_name, model_stats in model_data.items():
                if "test" not in model_name.lower():
                    filtered_models[model_name] = model_stats

            if len(filtered_models) != original_count:
                with open(model_perf_file, 'w', encoding='utf-8') as f:
                    json.dump(filtered_models, f, indent=2, ensure_ascii=False)
                print(f"  ✓ Removed {original_count - len(filtered_models)} test models from model performance")

        # Remove performance records file if it was created by test
        perf_records_file = patterns_dir / "performance_records.json"
        if perf_records_file.exists():
            with open(perf_records_file, 'r', encoding='utf-8') as f:
                perf_data = json.load(f)

            original_count = len(perf_data.get("records", []))

            # Remove test records
            records = perf_data.get("records", [])
            filtered_records = [
                r for r in records
                if "test" not in r.get("task_type", "").lower()
                and "test" not in r.get("details", {}).get("task_description", "").lower()
                and "test" not in r.get("model_used", "").lower()
            ]

            if len(filtered_records) < original_count:
                perf_data["records"] = filtered_records
                perf_data["metadata"]["total_records"] = len(filtered_records)

                with open(perf_records_file, 'w', encoding='utf-8') as f:
                    json.dump(perf_data, f, indent=2, ensure_ascii=False)

                print(f"  ✓ Removed {original_count - len(filtered_records)} test records from performance records")

                # Remove file if empty
                if not filtered_records:
                    perf_records_file.unlink()
                    print(f"  ✓ Removed empty performance records file")

    except Exception as e:
        print(f"  ⚠️  Error during cleanup: {e}")


def main():
    """Run all compatibility tests."""
    print("Automatic Performance Recording System - Compatibility Tests\n")

    # Create .claude-patterns directory if it doesn't exist
    patterns_dir = Path(".claude-patterns")
    patterns_dir.mkdir(exist_ok=True)

    # Run tests
    test_results = []

    test_results.append(("Backward Compatibility", test_backward_compatibility()))
    test_results.append(("New Performance Recording", test_new_performance_recording()))
    test_results.append(("Dashboard Compatibility", test_dashboard_compatibility()))

    # Cleanup test data
    cleanup_test_data()

    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)

    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1

    print(f"\nResult: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The performance recording system is ready for use.")
        print("\nFeatures enabled:")
        print("  ✓ Automatic performance recording for all tasks")
        print("  ✓ Backward compatibility with existing data")
        print("  ✓ Enhanced dashboard integration")
        print("  ✓ Model-specific performance tracking")
        print("  ✓ Task-type performance analysis")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())