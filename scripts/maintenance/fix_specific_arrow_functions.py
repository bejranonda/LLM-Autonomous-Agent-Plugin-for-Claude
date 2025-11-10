#!/usr/bin/env python3
"""
Fix the specific arrow functions at lines 2916, 2940, and 2954 in the dashboard
"""

def fix_specific_arrow_functions():
    file_path = 'D:\\Git\\Werapol\\AutonomousAgent\\.claude-patterns\\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixes_applied = 0

    print("Fixing specific arrow functions...")

    # Fix the specific arrow functions that are causing syntax errors
    arrow_fixes = [
        # Fix 1: Reduce arrow function (line 2916)
        ("dateEntry[model] = scores.reduce((a, b) => a + b, 0) / scores.length;",
         "dateEntry[model] = scores.reduce(function(a, b) { return a + b; }, 0) / scores.length;"),

        # Fix 2: Map arrow function (line 2940)
        ("const scores = timelineData.timeline_data.map(day => day[model] || 0);",
         "const scores = timelineData.timeline_data.map(function(day) { return day[model] || 0; });"),

        # Fix 3: Map arrow function (line 2954) - the main error at line 1876:119
        ("const dateLabels = timelineData.timeline_data.map(day => day.date);",
         "const dateLabels = timelineData.timeline_data.map(function(day) { return day.date; });"),
    ]

    for old_pattern, new_pattern in arrow_fixes:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes_applied += 1
            print(f"Fixed: {old_pattern[:60]}...")

    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\nApplied {fixes_applied} fixes to dashboard.py")
        return True
    else:
        print("No arrow function fixes needed")
        return False

if __name__ == '__main__':
    fix_specific_arrow_functions()