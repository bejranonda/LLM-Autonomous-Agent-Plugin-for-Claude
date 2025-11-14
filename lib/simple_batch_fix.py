#!/usr/bin/env python3
"""
Simple batch fix for common patterns.
"""

import py_compile
from pathlib import Path


def simple_fix(file_path: Path) -> bool:
    """Apply simple, safe fixes."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        original = content

        # Fix 1: Remove standalone triple-quotes at start of lines
        lines = content.split('\n')
        new_lines = []

        for i, line in enumerate(lines):
            # Skip standalone """ that looks orphaned
            if line.strip() == '"""' and i > 5:
                # Check context
                prev_line = lines[i-1].strip() if i > 0 else ""
                next_line = lines[i+1].strip() if i < len(lines) - 1 else ""

                # Skip if it looks like an orphan (after code, before code)
                if (prev_line and not prev_line.startswith('#') and not prev_line.endswith('"""') and
                    next_line and not next_line.startswith('"""')):
                    continue  # Skip this line

            new_lines.append(line)

        content = '\n'.join(new_lines)

        if content != original:
            # Test if it compiles now
            try:
                compile(content, str(file_path), 'exec')
                # Success! Write it
                file_path.write_text(content, encoding='utf-8')
                return True
            except:
                # Didn't work, don't write
                pass

        return False
    except:
        return False


def main():
    """Process all broken files."""
    lib_files = list(Path('lib').glob('*.py'))

    print("Simple Batch Fix - Processing files...")
    fixed = 0

    for f in lib_files:
        if 'fix_' not in f.name and 'nuclear' not in f.name:
            try:
                # Check if currently broken
                py_compile.compile(str(f), doraise=True)
            except:
                # It's broken, try to fix
                if simple_fix(f):
                    fixed += 1
                    print(f"  Fixed: {f.name}")

    print(f"\nTotal fixed: {fixed}")


if __name__ == "__main__":
    main()
