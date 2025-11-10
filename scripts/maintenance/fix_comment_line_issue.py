#!/usr/bin/env python3
"""
Fix the specific comment line issue at line 1875 with character 118
"""

def fix_comment_line_issue():
    file_path = 'D:\\Git\\Werapol\\AutonomousAgent\\.claude-patterns\\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixes_applied = 0

    print("Fixing comment line issue...")

    # The issue might be the quotes in the comment causing confusion
    # Let's fix the comment line that contains "Timeline" text
    old_comment = "            // Extract date labels (only dates, no \"Timeline\" text)"
    new_comment = "            // Extract date labels - only dates, no Timeline text"

    if old_comment in content:
        content = content.replace(old_comment, new_comment)
        fixes_applied += 1
        print(f"Fixed comment line quotes issue")

    # Also check for any other similar quote issues in comments nearby
    comment_fixes = [
        # Any other comment patterns that might be causing issues
        ("// Bar chart by time", "// Bar chart for timeline data"),
        ("// Only dates on x-axis", "// Dates only on x-axis"),
        ("// Models as colored bars", "// Models shown as colored bars"),
    ]

    for old_pattern, new_pattern in comment_fixes:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes_applied += 1
            print(f"Fixed comment pattern: {old_pattern}")

    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\nApplied {fixes_applied} comment fixes to dashboard.py")
        return True
    else:
        print("No comment fixes needed")
        return False

if __name__ == '__main__':
    fix_comment_line_issue()