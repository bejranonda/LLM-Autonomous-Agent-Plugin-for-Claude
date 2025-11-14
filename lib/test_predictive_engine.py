#!/usr/bin/env python3
"""
Test script for the advanced predictive engine
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from advanced_predictive_engine import AdvancedPredictiveEngine
import json


def test_predictive_engine():
    """Test the advanced predictive engine functionality"""
    print("Testing Advanced Predictive Engine...")

    # Initialize engine
    engine = AdvancedPredictiveEngine()
    print("Engine initialized successfully")

    # Test prediction
    test_task = {"task_type": "refactoring", "context": {"complexity": "medium", "language": "python", "framework": "flask"}}

    result = engine.predict_task_completion(test_task)
    print(f"Prediction completed: {result['ensemble_prediction']:.3f}")
    print(f"   Confidence: {result['ensemble_confidence']:.3f}")
    print(f"   Recommendations: {len(result['recommendations'])} generated")

    # Test feature extraction
    features = engine._extract_features(test_task)
    print(f"Features extracted: {len(features)} dimensions")

    # Test model loading
    engine._load_models()
    print("Models loaded successfully")

    print("\nAll tests passed! Predictive engine is operational.")
    return result


if __name__ == "__main__":
    try:
        result = test_predictive_engine()
        print("\nFinal Result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
