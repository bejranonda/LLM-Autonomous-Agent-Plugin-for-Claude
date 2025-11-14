#!/usr/bin/env python3
# Utility to update dashboard activity data with current timestamps.
# This generates sample activity data to demonstrate the dashboard functionality.
import json
from datetime import datetime, timedelta
from pathlib import Path
import random


def create_sample_activity():
    """Create sample activity entries with current timestamps."""

    # Current activity types
    task_types = [
        "gui-design-enhancement",
        "dashboard-improvement",
        "design-system-update",
        "responsive-design",
        "accessibility-improvement",
        "component-development",
        "user-interface-refactor",
        "theme-implementation",
        "performance-optimization",
        "pattern-learning",
    ]

    skills_options = [
        ["gui-design-principles", "quality-standards", "pattern-learning"],
        ["gui-design-principles", "validation-standards"],
        ["code-analysis", "quality-standards", "gui-design-principles"],
        ["pattern-learning", "autonomous-development"],
        ["quality-standards", "documentation-best-practices"],
    ]

    activities = []

    # Generate activities for the last few hours
    base_time = datetime.now()

    for i in range(15):  # Create 15 recent activities
        # Random time offset within last 2 hours
        minutes_ago = random.randint(5, 120)
        timestamp = base_time - timedelta(minutes=minutes_ago)

        activity = {
            "timestamp": timestamp.isoformat() + "Z",
            "task_type": random.choice(task_types),
            "quality_score": random.randint(85, 100),
            "success": random.choice([True, True, True, False]),  # 75% success rate
            "duration": random.randint(60, 300),  # 1-5 minutes
            "skills_used": random.choice(skills_options),
            "auto_generated": True,
        }

        activities.append(activity)

    # Sort by timestamp (newest first)
    activities.sort(key=lambda x: x["timestamp"], reverse=True)

    return activities


def update_patterns_directory():
    """Update the patterns directory with current activity data."""

    patterns_dir = Path(".claude-patterns")
    if not patterns_dir.exists():
        patterns_dir.mkdir(parents=True)
        print(f"Created patterns directory: {patterns_dir}")

    # Generate new activity data
    new_activities = create_sample_activity()

    # Load existing data
    performance_file = patterns_dir / "performance_records.json"
    existing_data = {"records": []}

    if performance_file.exists():
        try:
            with open(performance_file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except Exception as e:
            print(f"Error loading existing data: {e}")

    # Add new activities
    if "records" not in existing_data:
        existing_data["records"] = []

    # Add new activities at the beginning
    existing_data["records"] = new_activities + existing_data["records"]

    # Keep only the most recent 50 activities
    existing_data["records"] = existing_data["records"][:50]

    # Save updated data
    with open(performance_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)

    print(f"Updated activity data with {len(new_activities)} new entries")
    print(f"Total activities in database: {len(existing_data['records'])}")

    # Also update quality history
    quality_file = patterns_dir / "quality_history.json"
    quality_data = {"quality_assessments": []}

    if quality_file.exists():
        try:
            with open(quality_file, "r", encoding="utf-8") as f:
                quality_data = json.load(f)
        except BaseException:
            pass

    if "quality_assessments" not in quality_data:
        quality_data["quality_assessments"] = []

    # Add some quality assessments
    for activity in new_activities[:5]:  # Add 5 most recent
        assessment = {
            "timestamp": activity["timestamp"],
            "task_type": activity["task_type"],
            "overall_score": activity["quality_score"],
            "pass": activity["success"],
            "details": {
                "duration_seconds": activity["duration"],
                "skills_used": activity["skills_used"],
            },
            "skills_used": activity["skills_used"],
            "auto_generated": activity["auto_generated"],
        }
        quality_data["quality_assessments"].append(assessment)

    # Keep only recent assessments
    quality_data["quality_assessments"] = quality_data["quality_assessments"][-20:]

    with open(quality_file, "w", encoding="utf-8") as f:
        json.dump(quality_data, f, indent=2, ensure_ascii=False)

    print(f"Updated quality history with {len(new_activities[:5])} new assessments")


def main():
    """Main function to update activity data."""
    print("Updating dashboard activity data...")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    update_patterns_directory()

    print("\nActivity data updated successfully!")
    print("Refresh your dashboard at http://127.0.0.1:5000 to see the latest activity.")


if __name__ == "__main__":
    main()
