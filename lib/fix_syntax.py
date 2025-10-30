#!/usr/bin/env python3
"""
Script to systematically fix syntax errors in Python files.
"""

import os
import re
import subprocess
from pathlib import Path
import tempfile
import shutil


def fix_common_syntax_patterns(content):
    """Fix common syntax error patterns found in the codebase."""

    # Pattern 1: Fix malformed dictionary entries with extra commas and parentheses
    # From: 'key': value.get(\n    'subkey',\n    default),,\n)
    # To:   'key': value.get('subkey', default),
    content = re.sub(
        r"'([^']+)':\s*(\w+)\(\s*\n\s*'([^']+)',\s*\n\s*([^)]+)\s*\),,\s*\)",
        r"'\1': \2('\3', \4),",
        content
    )

    # Pattern 2: Fix malformed function calls
    # From: function_name(\n    param1,\n    param2\n)\n)
    # To:   function_name(param1, param2)
    content = re.sub(
        r"(\w+)\(\s*\n\s*([^)]+)\n\s*\)\s*\)",
        r"\1(\2)",
        content
    )

    # Pattern 3: Fix malformed dictionary literals with extra commas
    # From: { 'key': value,,\n)
    # To:   { 'key': value }
    content = re.sub(
        r",\s*,\s*\)\s*",
        "",
        content
    )

    # Pattern 4: Fix malformed multiline strings in docstrings
    # From: """description (\n    default: value,\n)"""
    # To:   """description (default: value)"""
    content = re.sub(
        r'"""([^"]*)\(\s*\n\s*([^)]*)\s*\)\s*"""',
        r'"""\1 (\2)"""',
        content
    )

    # Pattern 5: Fix malformed parameter lists
    # From: def func(\n    param1,\n    param2)\n):
    # To:   def func(param1, param2):
    content = re.sub(
        r"def\s+(\w+)\(\s*\n\s*([^)]*)\n\s*\)\s*\):",
        r"def \1(\2):",
        content
    )

    # Pattern 6: Fix malformed function return annotations
    # From: def func() -> type:,\n)
    # To:   def func() -> type:
    content = re.sub(
        r"def\s+(\w+)\([^)]*\)\s*->\s*([^:]+):,\s*\)",
        r"def \1() -> \2:",
        content
    )

    # Pattern 7: Fix malformed list/dict comprehensions
    # From: [x for x in items,\n)
    # To:   [x for x in items]
    content = re.sub(
        r"\[([^\]]+)\s*,\s*\)\s*\]",
        r"[\1]",
        content
    )

    # Pattern 8: Fix malformed import statements
    # From: from module import (\n    item1,\n    item2\n)
    # To:   from module import item1, item2
    content = re.sub(
        r"from\s+(\w+)\s+import\s*\(\s*\n\s*([^)]+)\s*\)",
        r"from \1 import \2",
        content
    )

    return content


def has_syntax_errors(filepath):
    """Check if a Python file has syntax errors."""
    try:
        result = subprocess.run(
            ['python', '-m', 'py_compile', str(filepath)],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode != 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return True


def fix_file_syntax(filepath):
    """Fix syntax errors in a Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try different encoding
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"Could not read {filepath}: {e}")
            return False

    original_content = content
    fixed_content = fix_common_syntax_patterns(content)

    # Only write if content changed
    if fixed_content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        except Exception as e:
            print(f"Could not write to {filepath}: {e}")
            return False

    return False


def main():
    """Main function to fix syntax errors in all Python files."""
    lib_dir = Path("lib")

    if not lib_dir.exists():
        print("lib directory not found")
        return

    # Find all Python files
    py_files = list(lib_dir.glob("*.py"))

    fixed_files = []
    error_files = []

    print(f"Checking {len(py_files)} Python files for syntax errors...")

    for filepath in py_files:
        if filepath.name == 'fix_syntax.py':
            continue  # Skip this script

        if has_syntax_errors(filepath):
            print(f"  Fixing: {filepath.name}")
            try:
                if fix_file_syntax(filepath):
                    fixed_files.append(filepath.name)
                    # Check if it's now fixed
                    if has_syntax_errors(filepath):
                        error_files.append(filepath.name)
                    else:
                        print(f"     Fixed successfully")
                else:
                    error_files.append(filepath.name)
                    print(f"     Could not fix")
            except Exception as e:
                error_files.append(filepath.name)
                print(f"     Error: {e}")

    print(f"\nSummary:")
    print(f"  Total files checked: {len(py_files)}")
    print(f"  Files fixed: {len(fixed_files)}")
    print(f"  Files still with errors: {len(error_files)}")

    if error_files:
        print(f"\nFiles still with syntax errors:")
        for filename in error_files:
            print(f"  - {filename}")

    print(f"\nDone!")


if __name__ == '__main__':
    main()