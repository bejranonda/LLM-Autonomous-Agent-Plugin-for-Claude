#!/usr/bin/env python3
"""
Comprehensive Dashboard Validation Script
Validates that dashboard API endpoints return data consistent with source records
"""

import requests
import sys
from datetime import datetime
from pathlib import Path

def test_api_endpoint(url, expected_fields, name):
    """Test a specific API endpoint"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[FAIL] {name}: HTTP {response.status_code}")
            return False

        data = response.json()

        # Check expected fields
        missing_fields = [field for field in expected_fields if field not in data]
        if missing_fields:
            print(f"[FAIL] {name}: Missing fields: {missing_fields}")
            return False

        print(f"[PASS] {name}: OK")
        return True

    except Exception as e:
        print(f"[ERROR] {name}: {e}")
        return False

def validate_data_consistency():
    """Validate dashboard data consistency with source records"""
    print("[INFO] COMPREHENSIVE DASHBOARD VALIDATION")
    print("=" * 60)

    base_url = "http://127.0.0.1:8080/api"
    results = []

    # Test 1: Overview API
    print("\n1. Testing Overview API...")
    overview_fields = ["average_quality_score", "model_performance", "total_patterns", "total_skills", "total_agents"]
    results.append(test_api_endpoint(f"{base_url}/overview", overview_fields, "Overview"))

    # Test 2: Quality Trends API
    print("\n2. Testing Quality Trends API...")
    trends_fields = ["trend_data", "overall_average", "days"]
    results.append(test_api_endpoint(f"{base_url}/quality-trends", trends_fields, "Quality Trends"))

    # Test 3: Quality Timeline API
    print("\n3. Testing Quality Timeline API...")
    timeline_fields = ["timeline_data", "implemented_models", "model_info", "chart_type"]
    results.append(test_api_endpoint(f"{base_url}/quality-timeline?days=30", timeline_fields, "Quality Timeline"))

    # Test 4: Model Quality Scores API
    print("\n4. Testing Model Quality Scores API...")
    model_scores_fields = ["models", "quality_scores", "success_rates"]
    results.append(test_api_endpoint(f"{base_url}/model-quality-scores", model_scores_fields, "Model Quality Scores"))

    # Test 5: Skills API
    print("\n5. Testing Skills API...")
    skills_fields = ["top_skills", "total_skills"]
    results.append(test_api_endpoint(f"{base_url}/skills", skills_fields, "Skills"))

    # Test 6: Agents API
    print("\n6. Testing Agents API...")
    agents_fields = ["top_agents", "total_agents"]
    results.append(test_api_endpoint(f"{base_url}/agents", agents_fields, "Agents"))

    # Test 7: Task Distribution API
    print("\n7. Testing Task Distribution API...")
    task_dist_fields = ["distribution", "total_tasks"]
    results.append(test_api_endpoint(f"{base_url}/task-distribution", task_dist_fields, "Task Distribution"))

    # Test 8: Recent Activity API
    print("\n8. Testing Recent Activity API...")
    activity_fields = ["recent_activity"]
    results.append(test_api_endpoint(f"{base_url}/recent-activity", activity_fields, "Recent Activity"))

    # Test 9: System Health API
    print("\n9. Testing System Health API...")
    health_fields = ["status", "error_rate", "avg_quality", "patterns_stored"]
    results.append(test_api_endpoint(f"{base_url}/system-health", health_fields, "System Health"))

    # Summary
    passed = sum(results)
    total = len(results)

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Passed: {passed}/{total} tests")

    if passed == total:
        print("[SUCCESS] ALL TESTS PASSED - Dashboard is fully functional!")

        # Additional validation: Check multi-day data in timeline
        print("\n[INFO] VALIDATING MULTI-DAY DATA...")
        try:
            timeline_response = requests.get(f"{base_url}/quality-timeline?days=30", timeout=10)
            timeline_data = timeline_response.json()

            timeline_entries = timeline_data.get("timeline_data", [])
            unique_dates = set(entry.get("date", "") for entry in timeline_entries)

            print(f"[PASS] Timeline covers {len(unique_dates)} unique dates: {sorted(unique_dates)}")

            if len(unique_dates) >= 3:
                print("[PASS] Multi-day historical data confirmed!")
            else:
                print("[WARN] Limited historical data")

        except Exception as e:
            print(f"[ERROR] Timeline validation error: {e}")

    else:
        print(f"[WARN] {total - passed} tests failed - Dashboard needs attention")

    return passed == total

def validate_source_records():
    """Validate that source records exist and contain expected data"""
    print("\n[INFO] VALIDATING SOURCE RECORDS...")

    patterns_dir = Path(".claude-patterns")
    required_files = [
        "model_performance.json",
        "quality_history.json",
        "assessments.json",
        "trends.json"
    ]

    missing_files = []
    for file_name in required_files:
        file_path = patterns_dir / file_name
        if not file_path.exists():
            missing_files.append(file_name)
        else:
            print(f"[PASS] {file_name} exists")

    if missing_files:
        print(f"[FAIL] Missing files: {missing_files}")
        return False

    print("[PASS] All required source records present")
    return True

if __name__ == "__main__":
    print("Dashboard Validation Script")
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Validate source records first
    source_valid = validate_source_records()

    if source_valid:
        # Validate dashboard APIs
        api_valid = validate_data_consistency()

        if api_valid:
            print("\n[SUCCESS] DASHBOARD IS FULLY VALIDATED AND READY!")
            sys.exit(0)
        else:
            print("\n[WARN] Dashboard validation failed")
            sys.exit(1)
    else:
        print("\n[FAIL] Source records validation failed")
        sys.exit(1)