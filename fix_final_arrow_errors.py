#!/usr/bin/env python3
"""
Fix the final 2 remaining arrow function JavaScript errors
"""

def fix_final_arrow_errors():
    file_path = 'D:\\Git\\Werapol\\AutonomousAgent\\.claude-patterns\\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Fixing final 2 arrow function JavaScript errors...")
    original_content = content
    fixes_applied = 0

    # Fix the specific remaining arrow function errors
    final_fixes = [
        # Line 2482: labels: data.trend_data.map(function(d => d.display_time))),
        ("labels: data.trend_data.map(function(d => d.display_time))",
         "labels: data.trend_data.map(function(d) { return d.display_time })"),

        # Line 2534: labels: data.distribution.map(function(d => d.task_type))),
        ("labels: data.distribution.map(function(d => d.task_type))",
         "labels: data.distribution.map(function(d) { return d.task_type })"),
    ]

    for old_pattern, new_pattern in final_fixes:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes_applied += 1
            print(f"Fixed final arrow function error {fixes_applied}: {old_pattern}")

    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\nApplied {fixes_applied} final fixes - all JavaScript errors should be resolved!")
        return True
    else:
        print("No final fixes needed")
        return False

if __name__ == '__main__':
    fix_final_arrow_errors()