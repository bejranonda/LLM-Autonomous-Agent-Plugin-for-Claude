#!/usr/bin/env python3
#     Identify Python files with syntax errors
    """
import py_compile
import sys
from pathlib import Path


def check_syntax(file_path):
    """Check if a Python file has syntax errors"""
    try:
        py_compile.compile(str(file_path), doraise=True)
        return None
    except py_compile.PyCompileError as e:
        return str(e)
    except Exception as e:
        return f"Unexpected error: {e}"


def main():
    """Check all Python files for syntax errors"""
    lib_dir = Path("lib")
    error_files = []
    good_files = []

    for py_file in lib_dir.glob("*.py"):
        error = check_syntax(py_file)
        if error:
            error_files.append((py_file.name, error))
        else:
            good_files.append(py_file.name)

    print("=== SYNTAX ERROR ANALYSIS ===")
    print(f"Files checked: {len(error_files) + len(good_files)}")
    print(f"Files with errors: {len(error_files)}")
    print(f"Files without errors: {len(good_files)}")
    print()

    if error_files:
        print("FILES WITH SYNTAX ERRORS:")
        for filename, error in error_files:
            print(f"ERROR: {filename}")
            # Extract first line of error for summary
            first_line = error.split("\n")[0] if "\n" in error else error
            print(f"   {first_line}")
        print()

    if good_files:
        print("FILES WITHOUT SYNTAX ERRORS:")
        for filename in sorted(good_files):
            print(f"OK: {filename}")

    return error_files


if __name__ == "__main__":
    error_files = main()
    sys.exit(len(error_files))
