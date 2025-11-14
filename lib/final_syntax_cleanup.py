#!/usr/bin/env python3
"""
Final aggressive syntax cleanup for critical files.
Focuses on high-priority files that are likely imported.
"""

import sys
from pathlib import Path
import re


def aggressive_fix(file_path: Path) -> bool:
    """Apply aggressive fixes to make files compilable."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        original = content
        lines = content.split('\n')

        # Strategy: Remove all problematic module docstrings entirely
        # Keep only shebang, imports, and code

        new_lines = []
        skip_until_import = False
        found_shebang = False
        found_first_import = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Always keep shebang
            if line.startswith('#!'):
                new_lines.append(line)
                found_shebang = True
                continue

            # Keep normal comments after shebang
            if stripped.startswith('#') and not skip_until_import:
                # Convert problematic comment-like text to actual comments
                if not line.strip().startswith('#'):
                    line = '# ' + line.strip()
                new_lines.append(line)
                continue

            # Detect start of bad docstring area
            if stripped == '"""' and not found_first_import and i < 30:
                skip_until_import = True
                continue

            # Skip everything until we hit imports
            if skip_until_import:
                if stripped.startswith('import ') or stripped.startswith('from '):
                    skip_until_import = False
                    found_first_import = True
                    new_lines.append(line)
                elif stripped.startswith('class ') or stripped.startswith('def '):
                    skip_until_import = False
                    new_lines.append(line)
                continue

            # Keep everything else
            new_lines.append(line)

        # Only write if we made changes
        new_content = '\n'.join(new_lines)
        if new_content != original:
            # Validate the new content
            try:
                compile(new_content, str(file_path), 'exec')
                # It compiles! Write it
                file_path.write_text(new_content, encoding='utf-8')
                return True
            except:
                # Fix didn't work, don't write
                return False

        return False

    except Exception as e:
        return False


def main():
    """Process files that are likely to be imported."""
    lib_path = Path("lib")

    # Priority files - commonly imported utilities
    priority_patterns = [
        'pattern_storage.py',
        'quality_tracker.py',
        'task_queue.py',
        'learning_engine.py',
        'agent_*.py',
        'assessment*.py',
        'performance*.py',
        'user_preference*.py',
        'validation*.py'
    ]

    all_files = list(lib_path.rglob("*.py"))

    # Filter to priority files
    priority_files = []
    for pattern in priority_patterns:
        pattern_re = pattern.replace('*', '.*')
        for f in all_files:
            if re.match(pattern_re, f.name):
                priority_files.append(f)

    priority_files = list(set(priority_files))  # Remove duplicates

    print("=" * 70)
    print("  AGGRESSIVE FINAL SYNTAX CLEANUP")
    print("=" * 70)
    print(f"\nProcessing {len(priority_files)} priority files...")
    print()

    fixed = 0
    for py_file in priority_files:
        if aggressive_fix(py_file):
            fixed += 1
            print(f"  [FIXED] {py_file.name}")

    print()
    print("=" * 70)
    print(f"  Files Fixed: {fixed}")
    print("=" * 70)


if __name__ == "__main__":
    main()
