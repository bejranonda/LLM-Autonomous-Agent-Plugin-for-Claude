#!/usr/bin/env python3
"""
Improved auto-fix script for module-level docstring issues.

Fixes missing closing triple-quotes in module docstrings.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple


def fix_file(file_path: Path) -> Tuple[bool, str]:
    """Fix a single Python file's docstring issues."""
    try:
        content = file_path.read_text()
        lines = content.split('\n')

        # Look for pattern: shebang, comment, opening """ without closing
        if len(lines) < 3:
            return False, "File too short"

        # Check if line 2 (index 2) has opening """
        if lines[2].strip() == '"""':
            # Find where docstring should end (before imports/code)
            close_idx = -1
            for i in range(3, min(len(lines), 50)):  # Check first 50 lines
                line = lines[i].strip()
                # Docstring likely ends before imports or code
                if (line.startswith('import ') or
                    line.startswith('from ') or
                    line.startswith('class ') or
                    line.startswith('def ') or
                    line.startswith('@') or
                    (line and not line[0].isalpha() and line != '"""')):
                    close_idx = i
                    break

            if close_idx > 0:
                # Check if closing """ already exists before this point
                has_closing = False
                for i in range(3, close_idx):
                    if '"""' in lines[i]:
                        has_closing = True
                        break

                if not has_closing:
                    # Insert closing """ before the import/code line
                    lines.insert(close_idx, '"""')

                    # Write fixed content
                    file_path.write_text('\n'.join(lines))
                    return True, f"Added closing quotes before line {close_idx}"

        return False, "No fix needed"

    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    """Run the auto-fix process."""
    lib_dir = Path("lib")
    python_files = list(lib_dir.glob("*.py"))

    print("=" * 60)
    print("  DOCSTRING CLOSING QUOTES FIX - V2")
    print("=" * 60)
    print()

    fixed_count = 0
    errors = []

    for py_file in python_files:
        fixed, msg = fix_file(py_file)
        if fixed:
            fixed_count += 1
            print(f"[FIXED] {py_file.name}: {msg}")
        elif "Error" in msg:
            errors.append(f"{py_file.name}: {msg}")

    print()
    print("=" * 60)
    print(f"  Files Fixed: {fixed_count}")
    print(f"  Errors: {len(errors)}")
    print("=" * 60)

    if errors:
        print("\nErrors encountered:")
        for err in errors[:10]:
            print(f"  - {err}")


if __name__ == "__main__":
    main()
