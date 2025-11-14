#!/usr/bin/env python3
"""
Targeted fix for remaining docstring indentation issues.
"""

import sys
from pathlib import Path


def fix_indented_docstring_after_comment(file_path: Path) -> bool:
    """Fix docstrings that are indented after comment lines."""
    try:
        lines = file_path.read_text(encoding='utf-8', errors='ignore').split('\n')
        fixed = False

        for i in range(len(lines)):
            line = lines[i]

            # Find indented """ that should be at column 0
            if line.strip() == '"""' and line[0] in (' ', '\t'):
                # De-indent it
                lines[i] = '"""'
                fixed = True

                # Find where this docstring should close
                close_idx = -1
                for j in range(i + 1, min(len(lines), i + 100)):
                    check_line = lines[j].strip()
                    if (check_line.startswith('import ') or
                        check_line.startswith('from ') or
                        check_line.startswith('class ') or
                        check_line.startswith('def ') or
                        check_line.startswith('@')):
                        close_idx = j
                        break
                    # Check if closing """ already exists
                    if '"""' in lines[j] and j > i:
                        close_idx = -1  # Already closed
                        break

                # Add closing """ if needed
                if close_idx > 0:
                    lines.insert(close_idx, '"""')
                    print(f"  Fixed: {file_path.name} - de-indented and closed docstring")
                elif fixed:
                    print(f"  Fixed: {file_path.name} - de-indented docstring")

        if fixed:
            file_path.write_text('\n'.join(lines), encoding='utf-8')
            return True

        return False

    except Exception as e:
        print(f"  Error: {file_path.name} - {str(e)}")
        return False


def main():
    """Process all Python files."""
    lib_path = Path("lib")
    python_files = list(lib_path.rglob("*.py"))

    print("=" * 70)
    print("  TARGETED DOCSTRING INDENTATION FIX")
    print("=" * 70)
    print()

    fixed_count = 0
    for py_file in python_files:
        if fix_indented_docstring_after_comment(py_file):
            fixed_count += 1

    print()
    print("=" * 70)
    print(f"  Files Fixed: {fixed_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()
