#!/usr/bin/env python3
"""
Fix method definition syntax errors where docstring appears before parameters.

Example error:
    def method_name(
        \"\"\"Docstring.\"\"\"
        self, param1, param2
    ):

Should be:
    def method_name(
        self, param1, param2
    ):
        \"\"\"Docstring.\"\"\"
"""

import re
import sys
from pathlib import Path


def fix_method_syntax(content: str) -> tuple[str, int]:
    """Fix method definitions with misplaced docstrings."""
    fixes = 0

    # Pattern 1: def method_name(\n        """Docstring."""\n        self, ...
    pattern1 = r'(def\s+\w+\()\s*\n\s+("""[^"]*""")\s*\n\s+(self[^)]*\))\s*:'

    def replace_func1(match):
        nonlocal fixes
        fixes += 1
        method_def = match.group(1)  # "def method_name("
        docstring = match.group(2)   # '"""Docstring."""'
        params = match.group(3)       # "self, param1, param2)"
        return f'{method_def}\n        {params}:\n        {docstring}'

    fixed_content = re.sub(pattern1, replace_func1, content, flags=re.MULTILINE)

    # Pattern 2: def method_name(\n        """Docstring."""\n        self,
    # (multi-line params with docstring on line after opening paren)
    pattern2 = r'(def\s+\w+\()\s*\n\s+("""[^"]*""")\s*\n(\s+self[^)]+)\n(\s+\))\s*(->\s*[^:]+)?:'

    def replace_func2(match):
        nonlocal fixes
        fixes += 1
        method_def = match.group(1)
        docstring = match.group(2)
        params_start = match.group(3)
        closing_paren = match.group(4)
        return_type = match.group(5) or ''
        return f'{method_def}\n{params_start}\n{closing_paren}{return_type}:\n        {docstring}'

    fixed_content = re.sub(pattern2, replace_func2, fixed_content, flags=re.MULTILINE)

    return fixed_content, fixes


def main():
    """Fix all Python files in lib/ directory."""
    lib_dir = Path(__file__).parent / "lib"

    total_fixes = 0
    files_fixed = 0

    for py_file in lib_dir.glob("**/*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
            fixed_content, fixes = fix_method_syntax(content)

            if fixes > 0:
                py_file.write_text(fixed_content, encoding="utf-8")
                print(f"[OK] Fixed {fixes} method(s) in {py_file.name}")
                files_fixed += 1
                total_fixes += fixes

        except Exception as e:
            print(f"[ERROR] Failed to fix {py_file.name}: {e}")

    print(f"\n[SUMMARY] Fixed {total_fixes} methods in {files_fixed} files")
    return 0 if total_fixes > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
