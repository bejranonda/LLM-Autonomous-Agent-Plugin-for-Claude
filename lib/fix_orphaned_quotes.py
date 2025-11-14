#!/usr/bin/env python3
"""
Fix orphaned triple-quote markers in files.
"""

import sys
from pathlib import Path


def fix_orphaned_quotes(file_path: Path) -> bool:
    """Remove orphaned triple-quotes that appear alone on lines."""
    try:
        lines = file_path.read_text(encoding='utf-8', errors='ignore').split('\n')
        fixed = False
        new_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Check for orphaned """ (alone on a line, not part of pair)
            if stripped == '"""':
                # Look ahead and behind
                has_code_before = i > 0 and lines[i-1].strip() and not lines[i-1].strip().startswith('#')

                # Check if next line looks like docstring content or code
                has_content_after = False
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    has_content_after = next_line and not next_line.startswith('"""') and not next_line.startswith('def ') and not next_line.startswith('class ')

                # If this looks like an orphaned quote, remove it
                if has_code_before and not has_content_after:
                    fixed = True
                    print(f"  Removed orphaned quote at line {i+1}")
                    i += 1
                    continue

            new_lines.append(line)
            i += 1

        if fixed:
            file_path.write_text('\n'.join(new_lines), encoding='utf-8')
            return True

        return False

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Fix specific critical files."""
    files_to_fix = [
        'lib/pattern_storage.py',
        'lib/quality_tracker.py',
        'lib/task_queue.py',
        'lib/learning_engine.py'
    ]

    print("=" * 70)
    print("  FIX ORPHANED TRIPLE-QUOTES")
    print("=" * 70)
    print()

    for file_path in files_to_fix:
        p = Path(file_path)
        if p.exists():
            print(f"Processing: {file_path}")
            if fix_orphaned_quotes(p):
                print(f"  [FIXED]\n")
            else:
                print(f"  [NO CHANGES]\n")


if __name__ == "__main__":
    main()
