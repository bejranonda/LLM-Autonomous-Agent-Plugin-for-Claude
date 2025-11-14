#!/usr/bin/env python3
"""
Nuclear option: Remove all problematic module docstrings.
Convert them to comments instead.
"""

import sys
from pathlib import Path


def nuclear_fix_file(file_path: Path) -> bool:
    """Remove problematic module docstrings, keep only comments."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')

        if len(lines) < 3:
            return False

        # Find if we have a module docstring issue (""" not at top level after shebang/comments)
        fixed = False
        new_lines = []
        in_bad_docstring = False
        docstring_start = -1

        for i, line in enumerate(lines):
            # Keep shebang and normal comments
            if i == 0 and line.startswith('#!'):
                new_lines.append(line)
            elif line.strip().startswith('#') and not in_bad_docstring:
                new_lines.append(line)
            elif line.strip() == '"""' and i < 20:  # Module docstring area
                # Check if this is problematic (indented or after code)
                if i > 0 and (line[0] in (' ', '\t') or any(imp in ''.join(new_lines) for imp in ['import ', 'from ', 'class ', 'def '])):
                    # Skip this opening quote, enter bad docstring mode
                    in_bad_docstring = True
                    docstring_start = i
                    fixed = True
                    continue
                else:
                    new_lines.append(line)
                    if in_bad_docstring:
                        in_bad_docstring = False
            elif in_bad_docstring:
                # Convert docstring content to comments
                if '"""' in line:
                    # Closing quote - exit bad docstring mode
                    in_bad_docstring = False
                    continue
                else:
                    # Convert to comment
                    stripped = line.strip()
                    if stripped:
                        new_lines.append('# ' + stripped)
            else:
                new_lines.append(line)

        if fixed:
            file_path.write_text('\n'.join(new_lines), encoding='utf-8')
            return True

        return False

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Process all files."""
    lib_path = Path("lib")
    all_py_files = list(lib_path.rglob("*.py"))

    print("=" * 70)
    print("  NUCLEAR FIX: Remove Problematic Module Docstrings")
    print("=" * 70)
    print()

    fixed_count = 0
    for py_file in all_py_files:
        if nuclear_fix_file(py_file):
            fixed_count += 1
            print(f"  Fixed: {py_file.relative_to(lib_path)}")

    print()
    print("=" * 70)
    print(f"  Files Fixed: {fixed_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()
