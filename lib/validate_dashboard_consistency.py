"""
Validate Dashboard Data Consistency

This script verifies that the Recent Activity and Recent Performance Records
sections in the dashboard show consistent data from the same sources.
"""

import requests
import json
from datetime import datetime

def validate_dashboard_consistency():
    """Validate that dashboard sections show consistent data."""

    base_url = "http://127.0.0.1:5001"

    print("=" * 80)
    print("Dashboard Data Consistency Validation")
    print("=" * 80)
    print()

    # Fetch data from both endpoints
    try:
        recent_activity_response = requests.get(f"{base_url}/api/recent-activity")
        recent_activity_data = recent_activity_response.json()

        recent_performance_response = requests.get(f"{base_url}/api/recent-performance-records")
        recent_performance_data = recent_performance_response.json()

    except Exception as e:
        print(f"[ERROR] Error fetching dashboard data: {e}")
        print("\nMake sure the dashboard is running on http://127.0.0.1:5001")
        return False

    # Extract records
    activity_records = recent_activity_data.get('recent_activity', [])
    performance_records = recent_performance_data.get('records', [])

    print(f"Recent Activity Records: {len(activity_records)}")
    print(f"Recent Performance Records: {len(performance_records)}")
    print()

    # Get timestamps
    if activity_records:
        activity_latest = max(r.get('timestamp', '') for r in activity_records)
        activity_oldest = min(r.get('timestamp', '') for r in activity_records)
        print(f"Recent Activity Date Range:")
        print(f"  Latest:  {activity_latest}")
        print(f"  Oldest:  {activity_oldest}")
    else:
        print("[WARN] No records in Recent Activity")
        activity_latest = None

    print()

    if performance_records:
        perf_latest = max(r.get('timestamp', '') for r in performance_records)
        perf_oldest = min(r.get('timestamp', '') for r in performance_records)
        print(f"Recent Performance Records Date Range:")
        print(f"  Latest:  {perf_latest}")
        print(f"  Oldest:  {perf_oldest}")
    else:
        print("[WARN] No records in Recent Performance Records")
        perf_latest = None

    print()
    print("-" * 80)

    # Validate consistency
    issues = []

    # Check if both have the latest record
    if activity_latest and perf_latest:
        # Compare dates (allow for small timestamp differences)
        activity_date = datetime.fromisoformat(activity_latest.replace('Z', '+00:00'))
        perf_date = datetime.fromisoformat(perf_latest.replace('Z', '+00:00'))

        time_diff = abs((activity_date - perf_date).total_seconds())

        if time_diff < 60:  # Within 1 minute
            print(f"[PASS] Both sections show records from the same timeframe")
            print(f"       Time difference: {time_diff:.1f} seconds")
        else:
            issues.append(f"Latest timestamps differ by {time_diff/60:.1f} minutes")
            print(f"[FAIL] Latest timestamps differ significantly:")
            print(f"       Recent Activity: {activity_latest}")
            print(f"       Performance Records: {perf_latest}")
            print(f"       Difference: {time_diff/60:.1f} minutes")

    print()

    # Check for overlapping records
    activity_timestamps = set(r.get('timestamp', '') for r in activity_records)
    performance_timestamps = set(r.get('timestamp', '') for r in performance_records)

    overlap = activity_timestamps & performance_timestamps
    activity_only = activity_timestamps - performance_timestamps
    performance_only = performance_timestamps - activity_timestamps

    print(f"Timestamp Analysis:")
    print(f"  Overlapping records: {len(overlap)}")
    print(f"  Only in Recent Activity: {len(activity_only)}")
    print(f"  Only in Performance Records: {len(performance_only)}")

    print()

    # Show sample records from each section
    print("-" * 80)
    print("Sample Records (Latest 3):")
    print()

    print("Recent Activity (Latest 3):")
    for i, record in enumerate(activity_records[:3], 1):
        timestamp = record.get('timestamp', 'N/A')
        task_type = record.get('task_type', 'N/A')
        quality = record.get('quality_score', 'N/A')
        print(f"  {i}. {timestamp} | {task_type} | Score: {quality}")

    print()
    print("Recent Performance Records (Latest 3):")
    for i, record in enumerate(performance_records[:3], 1):
        timestamp = record.get('timestamp', 'N/A')
        task_type = record.get('task_type', 'N/A')
        quality = record.get('overall_score', 'N/A')
        print(f"  {i}. {timestamp} | {task_type} | Score: {quality}")

    print()
    print("=" * 80)

    # Final verdict
    if not issues:
        print("[PASS] VALIDATION PASSED: Dashboard sections are consistent!")
        print()
        print("Both Recent Activity and Recent Performance Records show data")
        print("from the same timeframe and sources.")
        return True
    else:
        print("[FAIL] VALIDATION FAILED: Data consistency issues detected")
        print()
        for issue in issues:
            print(f"  - {issue}")
        return False

if __name__ == "__main__":
    validate_dashboard_consistency()
