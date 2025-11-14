#!/usr/bin/env python3
"""
Auto-fix script for module-level docstring indentation issues.

Fixes two types of syntax errors:
1. IndentationError: Module-level docstrings with leading whitespace
2. SyntaxError: Unterminated triple-quoted strings

Creates backups before making changes.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class DocstringFixer:
    """Automatically fixes module-level docstring issues."""

    def __init__(self, target_dir: str = "lib"):
        self.target_dir = Path(target_dir)
        self.fixes_applied = []
        self.errors_found = []
        self.backup_dir = Path("lib_backup")

    def create_backup(self, file_path: Path) -> None:
        """Create backup of file before modification."""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir()

        backup_path = self.backup_dir / file_path.name
        backup_path.write_text(file_path.read_text())

    def fix_indented_module_docstring(self, content: str, file_path: str) -> Tuple[str, bool]:
        """Fix module-level docstrings that have incorrect indentation."""
        lines = content.split('\n')
        fixed = False

        # Pattern: shebang, comment, then indented docstring
        if len(lines) >= 3:
            # Check if line 3 (index 2) has indented triple quotes
            if lines[2].strip().startswith('"""') and lines[2][0] in (' ', '\t'):
                # This is an indented module docstring - fix it
                i = 2
                while i < len(lines):
                    if lines[i].strip():  # Non-empty line
                        # Remove leading whitespace
                        stripped = lines[i].lstrip()
                        if stripped.startswith('"""') or (i > 2 and not stripped.startswith('import') and not stripped.startswith('class') and not stripped.startswith('def')):
                            lines[i] = stripped
                        else:
                            # Hit actual code, stop
                            break
                    i += 1
                    # Stop if we hit closing quotes
                    if i > 2 and '"""' in lines[i-1] and lines[i-1].count('"""') >= 2:
                        break

                fixed = True
                self.fixes_applied.append(f"{file_path}: Fixed indented module docstring")

        return '\n'.join(lines), fixed

    def balance_triple_quotes(self, content: str, file_path: str) -> Tuple[str, bool]:
        """Ensure triple-quoted strings are properly closed."""
        triple_quote_count = content.count('"""')

        if triple_quote_count % 2 != 0:
            # Odd number of triple quotes - need to close
            # Find the last one and add closing quotes
            lines = content.split('\n')

            # Find last triple quote
            last_idx = -1
            for i in range(len(lines) - 1, -1, -1):
                if '"""' in lines[i]:
                    last_idx = i
                    break

            if last_idx >= 0:
                # Check if it's an opening quote (at start of line after strip)
                if lines[last_idx].strip().startswith('"""') and lines[last_idx].strip() == '"""':
                    # Add closing quotes after some reasonable content
                    # Look for where docstring content likely ends
                    insert_idx = last_idx + 1
                    while insert_idx < len(lines) and not lines[insert_idx].strip().startswith('import'):
                        insert_idx += 1

                    # Insert closing quotes before imports
                    lines.insert(insert_idx, '"""')
                    self.fixes_applied.append(f"{file_path}: Added missing closing triple-quotes")
                    return '\n'.join(lines), True

        return content, False

    def fix_file(self, file_path: Path) -> bool:
        """Fix a single Python file."""
        try:
            content = file_path.read_text()
            original_content = content

            # Create backup
            self.create_backup(file_path)

            # Apply fixes
            content, fixed1 = self.fix_indented_module_docstring(content, str(file_path))
            content, fixed2 = self.balance_triple_quotes(content, str(file_path))

            if fixed1 or fixed2:
                # Write fixed content
                file_path.write_text(content)
                return True

            return False

        except Exception as e:
            self.errors_found.append(f"{file_path}: {str(e)}")
            return False

    def process_directory(self) -> Dict[str, any]:
        """Process all Python files in directory."""
        python_files = list(self.target_dir.glob("*.py"))

        results = {
            "total_files": len(python_files),
            "files_fixed": 0,
            "files_unchanged": 0,
            "errors": []
        }

        for py_file in python_files:
            if self.fix_file(py_file):
                results["files_fixed"] += 1
            else:
                results["files_unchanged"] += 1

        results["errors"] = self.errors_found
        results["fixes_applied"] = self.fixes_applied

        return results


def main():
    """Run the auto-fix process."""
    print("=" * 60)
    print("  MODULE DOCSTRING AUTO-FIX UTILITY")
    print("=" * 60)
    print()

    fixer = DocstringFixer("lib")

    print("[1/3] Scanning lib/ directory for Python files...")
    results = fixer.process_directory()

    print(f"[2/3] Processing {results['total_files']} files...")
    print()

    print("[3/3] Auto-fix Results:")
    print(f"  Files Fixed: {results['files_fixed']}")
    print(f"  Files Unchanged: {results['files_unchanged']}")
    print(f"  Errors: {len(results['errors'])}")
    print()

    if results['fixes_applied']:
        print("Fixes Applied:")
        for fix in results['fixes_applied'][:10]:  # Show first 10
            print(f"  - {fix}")
        if len(results['fixes_applied']) > 10:
            print(f"  ... and {len(results['fixes_applied']) - 10} more")

    print()
    print("=" * 60)
    print(f"  AUTO-FIX COMPLETE: {results['files_fixed']} files repaired")
    print("  Backups saved to: lib_backup/")
    print("=" * 60)

    return 0 if results['files_fixed'] > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
