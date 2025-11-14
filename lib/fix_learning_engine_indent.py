#!/usr/bin/env python3
"""
Fix indentation issues in learning_engine.py specifically.
"""

from pathlib import Path


def fix_learning_engine():
    """Fix the learning_engine.py file's indentation."""
    file_path = Path("lib/learning_engine.py")
    lines = file_path.read_text(encoding='utf-8', errors='ignore').split('\n')

    new_lines = []
    in_class = False
    in_method = False
    method_indent = ""

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect class definition
        if stripped.startswith('class '):
            new_lines.append(line)
            in_class = True
            continue

        # Detect method definition
        if in_class and stripped.startswith('def '):
            new_lines.append(line)
            in_method = True
            # Calculate method indent (should be 4 spaces more than current)
            current_indent = len(line) - len(line.lstrip())
            method_indent = ' ' * (current_indent + 4)
            continue

        # If we're in a method and the line has content
        if in_method and stripped:
            # Check if line is already properly indented
            if not line.startswith(method_indent) and not line.startswith(' ' * (len(method_indent) + 4)):
                # Fix the indentation
                line = method_indent + stripped

        # Check if we're exiting a method
        if in_method and stripped.startswith('def '):
            in_method = False

        new_lines.append(line)

    # Write fixed content
    file_path.write_text('\n'.join(new_lines), encoding='utf-8')
    print(f"Fixed indentation in {file_path}")


if __name__ == "__main__":
    fix_learning_engine()
