#!/usr/bin/env python3
#     Comprehensive Python Syntax Fixer
"""
Fixes all common syntax errors in the Autonomous Agent Plugin project
"""
import os
import re
from pathlib import Path


def fix_common_syntax_errors(content):
    """Fix common syntax errors found in the project files"""

    # Fix 1: Multiple docstring quotes
    content = re.sub(r'"""[ \t]*\n[ \t]*"""[ \t]*\n[ \t]*"""[ \t]*\n[ \t]*"""[ \t]*\n', '"""\n', content)
    content = re.sub(r'"""[ \t]*\n[ \t]*"""[ \t]*\n[ \t]*"""[ \t]*\n', '"""\n', content)
    content = re.sub(r'"""[ \t]*\n[ \t]*"""[ \t]*\n', '"""\n', content)

    # Fix 2: Malformed function parameters (remove extra quotes)
    content = re.sub(r'"([^"]+)":\s*"([^"\[\]]+)"', r"\1: \2", content)

    # Fix 3: Fix function parameter types with brackets
    content = re.sub(r'"([^"]+)":\s*"([^"]+)\[([^]]+)\]"', r"\1: \2[\3]", content)

    # Fix 4: Fix malformed try/except statements
    content = re.sub(r'"try":\s*"([^"]+)"', r"try:\n        \1", content)
    content = re.sub(r'"except":\s*"([^"]+)"', r"except:\n        \1", content)

    # Fix 5: Fix malformed with statements
    content = re.sub(r'"with open\(([^)]+)\)":\s*"([^"]+)"', r"with open(\1):\n            \2", content)

    # Fix 6: Fix extra quotes in json.dump calls
    content = re.sub(r'json\.dump\("([^"]+)",\s*f,', r"json.dump(\1, f,", content)

    # Fix 7: Fix extra quotes in print statements
    content = re.sub(r'print\("([^"]+)"\)', r"print(\1)", content)

    # Fix 8: Fix time.time() calls with wrong brackets
    content = re.sub(r"time\.time(\})", "time.time()", content)

    # Fix 9: Fix return statements with extra quotes
    content = re.sub(r'"return":\s*"([^"]+)"', r"return \1", content)

    # Fix 10: Fix dictionary entries with extra quotes
    content = re.sub(r'"([^"]+)":\s*"([^"]+)"\s*([,}\]])', r'"\1": \2\3', content)

    return content


def fix_file(filepath):
    """Fix syntax errors in a single file"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            original_content = f.read()

        fixed_content = fix_common_syntax_errors(original_content)

        if fixed_content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            return True
        return False

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False


def test_file_syntax(filepath):
    """Test if a file has valid Python syntax"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            compile(f.read(), filepath, "exec")
        return True
    except SyntaxError:
        return False
    except Exception:
        return False


def main():
    """Main function to fix all Python files in lib directory"""
    lib_dir = Path("lib")

    if not lib_dir.exists():
        print("lib directory not found!")
        return

    python_files = list(lib_dir.glob("*.py"))
    fixed_files = []
    still_broken = []

    print(f"Found {len(python_files)} Python files to check...")

    for filepath in python_files:
        print(f"Processing {filepath.name}...", end=" ")

        if test_file_syntax(filepath):
            print("Already OK")
            continue

        if fix_file(filepath):
            if test_file_syntax(filepath):
                print("FIXED ")
                fixed_files.append(filepath.name)
            else:
                print("Still broken ")
                still_broken.append(filepath.name)
        else:
            print("No changes made")
            still_broken.append(filepath.name)

    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Files fixed: {len(fixed_files)}")
    print(f"Still broken: {len(still_broken)}")

    if fixed_files:
        print("\nFixed files:")
        for f in fixed_files:
            print(f"   {f}")

    if still_broken:
        print("\nStill broken files:")
        for f in still_broken:
            print(f"   {f}")


if __name__ == "__main__":
    main()
