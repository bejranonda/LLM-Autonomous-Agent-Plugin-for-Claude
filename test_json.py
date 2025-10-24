#!/usr/bin/env python3
"""
Test JSON serialization of timeline data
"""
import sys
import json
sys.path.append('.')
from lib.dashboard import DashboardDataCollector

def test_json_serialization():
    """Test JSON serialization of timeline function"""
    collector = DashboardDataCollector()
    
    print("Testing JSON serialization...")
    try:
        result = collector.get_quality_timeline_with_model_events(days=30)
        print(f"Result type: {type(result)}")
        
        # Try to serialize to JSON
        json_str = json.dumps(result)
        print("SUCCESS: JSON serialization works")
        print(f"JSON length: {len(json_str)}")
        
        # Try to deserialize
        parsed = json.loads(json_str)
        print("SUCCESS: JSON deserialization works")
        print(f"Timeline data length: {len(parsed.get('timeline_data', []))}")
        
        return True
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_json_serialization()
