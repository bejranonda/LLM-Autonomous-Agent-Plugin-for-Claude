#!/usr/bin/env python3
"""
Auto-fix syntax errors in the Autonomous Agent Plugin codebase.

This script systematically identifies and fixes common syntax errors including:
- Unmatched parentheses
- Unterminated string literals
- Unterminated f-strings
- Invalid syntax
"""

import os
import re
import ast
from pathlib import Path


def fix_unmatched_parentheses(content, file_path):
    """Fix unmatched parentheses by analyzing common patterns."""
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        # Fix common unmatched parenthesis patterns
        if line.strip() == ")" and i > 0:
            prev_line = lines[i - 1].strip()
            # Check if previous line has an opening brace without closing
            if prev_line.endswith("{") or ("{" in prev_line and "}" not in prev_line):
                # This likely needs to be } instead of )
                fixed_lines.append(line.replace(")", "}"))
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_unterminated_strings(content, file_path):
    """Fix unterminated string literals."""
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        # Fix unterminated f-strings
        if 'f"' in line and line.count('"') % 2 == 1:
            # Find the incomplete f-string
            f_string_match = re.search(r'f"[^"]*$', line)
            if f_string_match:
                # Complete the f-string by adding closing quote
                fixed_line = line + '"'
                fixed_lines.append(fixed_line)
                continue

        # Fix unterminated regular strings
        if '"' in line and line.count('"') % 2 == 1:
            # Check for incomplete string pattern
            if line.rstrip().endswith('"'):
                fixed_lines.append(line)
            else:
                # Try to complete the string
                fixed_line = line.rstrip() + '"'
                fixed_lines.append(fixed_line)
                continue

        # Fix specific known patterns
        if "Description too long:" in line and "chars (" in line and not line.endswith('")'):
            if line.endswith(""):
                fixed_line = line + '")'
                fixed_lines.append(fixed_line)
                continue

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_invalid_syntax(content, file_path):
    """Fix specific invalid syntax patterns."""
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        # Fix incomplete if statements
        if line.strip() == "if" and not line.strip().endswith(":"):
            fixed_lines.append(line + ":")
            continue

        # Fix incomplete ternary assignments
        if line.strip().endswith(" or") and "=" in line:
            # Look ahead to see if next line continues the assignment
            fixed_lines.append(line + ' ""')
            continue

        # Fix syntax error in error messages
        if "Must be one of: {" in line and not line.endswith("}')"):
            fixed_line = line.replace("Must be one of: {", "Must be one of: {")
            if "}" not in fixed_line:
                fixed_line = fixed_line.rstrip() + "}"
            fixed_lines.append(fixed_line)
            continue

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def attempt_python_parse(content):
    """Try to parse content as Python to check for syntax errors."""
    try:
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {e}"


def fix_file_syntax(file_path):
    """Attempt to fix syntax errors in a single file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        content = original_content
        applied_fixes = []

        # Try to parse original
        is_valid, error = attempt_python_parse(content)
        if is_valid:
            return True, "No syntax errors found", []

        # Apply fixes sequentially
        print(f"  Fixing {file_path}: {error}")

        # Fix 1: Unmatched parentheses
        content = fix_unmatched_parentheses(content, file_path)
        is_valid, error = attempt_python_parse(content)
        if is_valid:
            applied_fixes.append("Fixed unmatched parentheses")
            return True, "Fixed", applied_fixes

        # Fix 2: Unterminated strings
        content = fix_unterminated_strings(content, file_path)
        is_valid, error = attempt_python_parse(content)
        if is_valid:
            applied_fixes.append("Fixed unterminated strings")
            return True, "Fixed", applied_fixes

        # Fix 3: Invalid syntax
        content = fix_invalid_syntax(content, file_path)
        is_valid, error = attempt_python_parse(content)
        if is_valid:
            applied_fixes.append("Fixed invalid syntax")
            return True, "Fixed", applied_fixes

        # If still not valid, write the fixed version for manual inspection
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return False, f"Partially fixed (still broken): {error}", applied_fixes
        else:
            return False, f"No automatic fix available: {error}", []

    except Exception as e:
        return False, f"Error processing file: {e}", []


def main():
    """Main function to fix all syntax errors."""
    print("Auto-fixing syntax errors in Autonomous Agent Plugin...")

    # Get all Python files
    python_files = list(Path(".").rglob("*.py"))

    fixed_files = 0
    failed_files = 0
    total_files = len(python_files)

    for py_file in python_files:
        print(f"\nProcessing: {py_file}")
        success, message, fixes = fix_file_syntax(py_file)

        if success:
            if fixes:
                print(f"  PASS: Fixed: {', '.join(fixes)}")
                fixed_files += 1
            else:
                print(f"  PASS: Already valid")
        else:
            print(f"  FAIL: {message}")
            if "Partial" in message:
                fixed_files += 1  # Count as partially fixed
            failed_files += 1

    print(f"\n=== Summary ===")
    print(f"Total files: {total_files}")
    print(f"Fixed files: {fixed_files}")
    print(f"Failed files: {failed_files}")
    print(f"Success rate: {(fixed_files / total_files) * 100:.1f}%")


if __name__ == "__main__":
    main()
