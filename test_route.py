#!/usr/bin/env python3
"""
Test Flask route for timeline API
"""
import sys
import json
from flask import Flask, jsonify, request

sys.path.append('.')
from lib.dashboard import DashboardDataCollector

app = Flask(__name__)
collector = DashboardDataCollector()

@app.route('/test-timeline')
def test_timeline():
    """Test timeline route"""
    try:
        days = request.args.get('days', 30, type=int)
        print(f"Received days parameter: {days}")
        
        result = collector.get_quality_timeline_with_model_events(days)
        print(f"Function result: {type(result)}")
        
        return jsonify(result)
    except Exception as e:
        print(f"Error in route: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(port=5014, debug=True)
