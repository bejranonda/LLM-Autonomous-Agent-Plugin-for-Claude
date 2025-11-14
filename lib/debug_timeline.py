#!/usr/bin/env python3
#     Debug script for quality timeline function
"""
"""
from lib.dashboard import DashboardDataCollector
import sys

sys.path.append(".")


def test_quality_timeline():
    """Test the quality timeline function directly"""
    collector = DashboardDataCollector()

    print("Testing quality timeline function...")
    try:
        result = collector.get_quality_timeline_with_model_events(days=30)
        print("SUCCESS: Function executed without error")
        print(f"Timeline data length: {len(result.get('timeline_data', []))}")
        print(f"Implemented models: {result.get('implemented_models', [])}")
        if result.get("timeline_data"):
            print(f"First timeline entry: {result['timeline_data'][0]}")
        return result
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_quality_timeline()
