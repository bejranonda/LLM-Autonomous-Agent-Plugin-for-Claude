#!/usr/bin/env python3
"""
ENFORCED: Pattern Loading Safety Validator

CRITICAL: This script prevents cache_control errors by validating patterns
exist before ANY attempt to load them with cache_control.

This MUST be called by the orchestrator agent before ANY pattern loading.
"""

import json
import sys
from pathlib import Path


def validate_pattern_loading():
    """
    Validate if patterns can be safely loaded with cache_control.

    Returns:
        tuple: (can_load_patterns, status_message, patterns_data)
    """
    patterns_file = Path(".claude-patterns/patterns.json")

    # Check if patterns file exists
    if not patterns_file.exists():
        return False, "No patterns file found", None

    try:
        # Read patterns file
        with open(patterns_file, "r", encoding="utf-8") as f:
            patterns_data = json.load(f)

        # Check if patterns file is empty
        if not patterns_data:
            return False, "Patterns file is empty", None

        # Check if patterns list is empty
        if isinstance(patterns_data, list) and len(patterns_data) == 0:
            return False, "Patterns list is empty", None

        # Check if patterns have meaningful content
        if isinstance(patterns_data, list):
            has_content = any(
                pattern.get("approach")
                or pattern.get("context")
                or pattern.get("task_description")
                or pattern.get("skills_used")
                for pattern in patterns_data
            )
            if not has_content:
                return False, "Patterns exist but no meaningful content", None

        # Patterns are valid and can be loaded
        return True, f"Valid patterns found: {len(patterns_data) if isinstance(patterns_data, list) else 1}", patterns_data

    except json.JSONDecodeError as e:
        return False, f"Patterns file corrupted (JSON error): {e}", None
    except Exception as e:
        return False, f"Error reading patterns: {e}", None


def main():
    """Main validation function."""
    can_load, message, data = validate_pattern_loading()

    if can_load:
        print(f"[SAFE] Patterns can be loaded: {message}")
        sys.exit(0)  # Success exit code
    else:
        print(f"[UNSAFE] Skip pattern loading: {message}")
        sys.exit(1)  # Error exit code to indicate skip pattern learning


if __name__ == "__main__":
    main()
