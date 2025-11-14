#!/usr/bin/env python3
"""
Fix test fixtures that use incorrect parameter names.
Many tests use data_dir= when classes expect storage_dir=
"""

import re
from pathlib import Path


def fix_fixture_params(content: str) -> tuple[str, int]:
    """Fix data_dir parameter to storage_dir."""
    fixes = 0

    # Pattern: data_dir=temp_directory or data_dir=temp_dir
    pattern = r'\bdata_dir\s*=\s*'
    replacement = r'storage_dir='

    matches = list(re.finditer(pattern, content))
    fixes = len(matches)

    if fixes > 0:
        fixed_content = re.sub(pattern, replacement, content)
        return fixed_content, fixes

    return content, 0


def main():
    """Fix all test files."""
    test_dir = Path(__file__).parent / "tests"

    total_fixes = 0
    files_fixed = 0

    for test_file in test_dir.glob("**/*.py"):
        try:
            content = test_file.read_text(encoding="utf-8")
            fixed_content, fixes = fix_fixture_params(content)

            if fixes > 0:
                test_file.write_text(fixed_content, encoding="utf-8")
                print(f"[OK] Fixed {fixes} fixture(s) in {test_file.name}")
                files_fixed += 1
                total_fixes += fixes

        except Exception as e:
            print(f"[ERROR] Failed to fix {test_file.name}: {e}")

    print(f"\n[SUMMARY] Fixed {total_fixes} fixtures in {files_fixed} files")
    return 0 if total_fixes > 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
