#!/usr/bin/env python3
#     Test script to check dashboard data access
    """
import sys
import os
import json
from pathlib import Path


def test_patterns_data():
    """Test if patterns data is accessible"""
    patterns_dir = Path(".claude-patterns")

    print("Testing Dashboard Data Access...")
    print(f"Patterns directory: {patterns_dir}")
    print(f"Exists: {patterns_dir.exists()}")

    if patterns_dir.exists():
        # Test patterns.json
        patterns_file = patterns_dir / "patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, "r") as f:
                    patterns_data = json.load(f)
                print(f"[OK] patterns.json loaded: {len(patterns_data.get('patterns', []))} patterns")

                if patterns_data.get("patterns"):
                    first_pattern = patterns_data["patterns"][0]
                    print(f"   First pattern keys: {list(first_pattern.keys())}")
            except Exception as e:
                print(f"[ERROR] Error loading patterns.json: {e}")
        else:
            print("[ERROR] patterns.json not found")

        # Test performance records
        perf_file = patterns_dir / "performance_records.json"
        if perf_file.exists():
            try:
                with open(perf_file, "r") as f:
                    perf_data = json.load(f)
                print(f"[OK] performance_records.json loaded: {len(perf_data.get('records', []))} records")
            except Exception as e:
                print(f"[ERROR] Error loading performance_records.json: {e}")

        # Test skill metrics
        skill_file = patterns_dir / "skill_metrics.json"
        if skill_file.exists():
            try:
                with open(skill_file, "r") as f:
                    skill_data = json.load(f)
                print(f"[OK] skill_metrics.json loaded: {list(skill_data.keys())}")
            except Exception as e:
                print(f"[ERROR] Error loading skill_metrics.json: {e}")

        # Test unified data
        unified_file = patterns_dir / "unified_data.json"
        if unified_file.exists():
            try:
                with open(unified_file, "r") as f:
                    unified_data = json.load(f)
                print(f"[OK] unified_data.json loaded: {list(unified_data.keys())}")
            except Exception as e:
                print(f"[ERROR] Error loading unified_data.json: {e}")

    else:
        print("[ERROR] Patterns directory not found")


if __name__ == "__main__":
    test_patterns_data()
