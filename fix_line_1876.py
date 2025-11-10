#!/usr/bin/env python3
"""
Targeted fix for the JavaScript syntax error at line 1876:119
"""

def fix_line_1876():
    file_path = 'D:\\Git\\Werapol\\AutonomousAgent\\.claude-patterns\\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for potential issues around line 1876
    lines = content.split('\n')

    # Search for problematic patterns around line 1876
    for i, line in enumerate(lines):
        if i >= 1870 and i <= 1885:  # Check around line 1876
            # Look for potential JavaScript syntax issues
            if 'csvContent' in line and ('\\n' in line or "'" in line):
                print(f"Line {i+1}: {line}")

                # Check for malformed escape sequences
                if '\\n' in line and line.count("'") % 2 != 0:
                    print(f"  -> Potential unmatched quote issue")
                elif line.endswith(' + \'\\n\''):
                    print(f"  -> Correctly escaped newline")
                else:
                    print(f"  -> Checking syntax...")

            # Look for any remaining template literals or syntax issues
            if '`' in line and ('${' in line or line.count('`') % 2 != 0):
                print(f"Line {i+1}: Template literal issue: {line}")

            # Look for incomplete string concatenations
            if line.strip().endswith('+') and i < len(lines) - 1:
                next_line = lines[i + 1]
                if next_line.strip().startswith("'"):
                    print(f"Line {i+1}-{i+2}: Split string concatenation")
                    print(f"  Line {i+1}: {line}")
                    print(f"  Line {i+2}: {next_line}")

if __name__ == '__main__':
    fix_line_1876()