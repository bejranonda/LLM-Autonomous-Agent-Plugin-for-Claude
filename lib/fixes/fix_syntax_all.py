#!/usr/bin/env python3
#    Advanced Syntax Fixer for All Python Files
"""
Fixes complex syntax errors with regex patterns
"""
import re
import ast
from pathlib import Path


def fix_python_syntax(content: str) -> str:
    """Apply comprehensive syntax fixes"""

    # Fix 1: Missing quotes around string literals in print statements
    content = re.sub(
        r'print\(([^"\']*)\)',
        lambda m: (
            f'print("{m.group(1)}")' if not m.group(1).strip().startswith(('"', "'")) and not "(" in m.group(1) else m.group(0)
        ),
        content,
    )

    # Fix 2: Missing quotes in dictionary keys (most critical issue)
    content = re.sub(r"(\n\s+)([a-zA-Z_][a-zA-Z0-9_]*)\s*:", r'\1"\2":', content)

    # Fix 3: Fix malformed newline escape sequences
    content = re.sub(r"print\(\\n", 'print("\\n', content)

    # Fix 4: Fix malformed dictionary values with missing quotes
    content = re.sub(r":\s*([a-zA-Z_][a-zA-Z0-9_]*)(?=\s*[,}])", r': "\1"', content)

    # Fix 5: Fix conditional expressions without quotes
    content = re.sub(
        r":\s*(ready|compatible|needs_improvement|ready_with_minor_improvements|conditional)(?=\s*[,}])", r': "\1"', content
    )

    # Fix 6: Fix version numbers and strings
    content = re.sub(r":\s*([0-9]+\.[0-9]+\.[0-9]+)(?=\s*[,}])", r': "\1"', content)

    # Fix 7: Fix validation_type and other string constants
    content = re.sub(
        r":\s*(claude-plugin-guidelines|comprehensive-plugin-validation|Claude Code Official Development Guidelines)(?=\s*[,}])",
        r': "\1"',
        content,
    )

    # Fix 8: Fix percentage values
    content = re.sub(r":\s*(>[0-9]+%)(?=\s*[,}])", r': "\1"', content)

    # Fix 9: Fix command names with hyphens
    content = re.sub(r":\s*([a-z]+-[a-z]+)(?=\s*[,}])", r': "\1"', content)

    # Fix 10: Fix broken string concatenation
    content = re.sub(r'([a-zA-Z0-9_])"([a-zA-Z0-9_])', r"\1\2", content)

    return content


def test_syntax(content: str) -> bool:
    """Test if content has valid Python syntax"""
    try:
        ast.parse(content)
        return True
    except SyntaxError:
        return False


def fix_all_files():
    """Fix all Python files in lib directory"""
    lib_dir = Path("lib")
    fixed_count = 0
    total_errors = 0

    print("Advanced syntax fixing started...")

    for py_file in lib_dir.glob("*.py"):
        try:
            original_content = py_file.read_text(encoding="utf-8")

"""
            # Skip if already valid
            if test_syntax(original_content):
                print(f"OK {py_file.name} - Already valid")
                continue

            # Apply fixes
            fixed_content = fix_python_syntax(original_content)

            # Test if fixed
            if test_syntax(fixed_content):
                py_file.write_text(fixed_content, encoding="utf-8")
                print(f"FIXED {py_file.name}")
                fixed_count += 1
            else:
                print(f"BROKEN {py_file.name} - Still broken")
                total_errors += 1

        except Exception as e:
            print(f"ERROR {py_file.name} - {e}")
            total_errors += 1

    print(f"\nResults: {fixed_count} files fixed, {total_errors} still have errors")


if __name__ == "__main__":
    fix_all_files()
