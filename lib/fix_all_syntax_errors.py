#!/usr/bin/env python3
"""
Comprehensive syntax error fixer for all remaining issues.
Handles multiple error patterns systematically.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict


class ComprehensiveSyntaxFixer:
    """Fixes all types of syntax errors in Python files."""

    def __init__(self):
        self.fixes_applied = []
        self.errors = []

    def fix_indented_header_text(self, content: str, file_path: str) -> Tuple[str, bool]:
        """Fix indented text on line 2 that should be a comment."""
        lines = content.split('\n')
        if len(lines) < 3:
            return content, False

        # Check if line 2 (index 1) has indented text without # comment
        if len(lines) > 1 and lines[1].strip() and not lines[1].strip().startswith('#'):
            # Check if it starts with whitespace
            if lines[1] and lines[1][0] in (' ', '\t'):
                # Convert to comment
                lines[1] = '#' + lines[1]
                self.fixes_applied.append(f"{file_path}: Fixed indented header text on line 2")
                return '\n'.join(lines), True

        return content, False

    def fix_missing_closing_quotes(self, content: str, file_path: str) -> Tuple[str, bool]:
        """Fix unterminated triple-quoted strings."""
        # Count triple quotes
        triple_count = content.count('"""')

        if triple_count % 2 == 0:
            return content, False

        lines = content.split('\n')

        # Find all triple quote positions
        quote_positions = []
        for i, line in enumerate(lines):
            if '"""' in line:
                quote_positions.append(i)

        if len(quote_positions) < 1:
            return content, False

        # For odd number, we need to add a closing quote
        # Find the last opening quote and determine where to close
        last_quote_idx = quote_positions[-1]

        # Look for where docstring content ends
        close_idx = -1
        for i in range(last_quote_idx + 1, len(lines)):
            line = lines[i].strip()
            # Docstring ends before code/imports
            if (line.startswith('import ') or
                line.startswith('from ') or
                line.startswith('class ') or
                line.startswith('def ') or
                line.startswith('@') or
                (line and line[0] == '#')):
                close_idx = i
                break

        if close_idx > 0:
            lines.insert(close_idx, '"""')
            self.fixes_applied.append(f"{file_path}: Added missing closing triple-quotes")
            return '\n'.join(lines), True

        return content, False

    def fix_docstring_at_line_3(self, content: str, file_path: str) -> Tuple[str, bool]:
        """Fix unclosed docstrings starting at line 3."""
        lines = content.split('\n')

        if len(lines) < 4:
            return content, False

        # Pattern: line 0=shebang, line 1=comment/text, line 2="""
        if (len(lines) > 2 and
            lines[2].strip() == '"""' and
            lines[0].startswith('#!')):

            # Count quotes after line 2
            quote_count_after = 0
            close_idx = -1

            for i in range(3, min(len(lines), 100)):
                if '"""' in lines[i]:
                    quote_count_after += lines[i].count('"""')

                # Stop at code
                line = lines[i].strip()
                if (line.startswith('import ') or
                    line.startswith('from ') or
                    line.startswith('class ') or
                    line.startswith('def ')):
                    close_idx = i
                    break

            # If odd number of quotes, need to add closing
            if quote_count_after % 2 == 0 and close_idx > 0:  # Including opening at line 2
                lines.insert(close_idx, '"""')
                self.fixes_applied.append(f"{file_path}: Closed docstring at line 3")
                return '\n'.join(lines), True

        return content, False

    def fix_file(self, file_path: Path) -> bool:
        """Apply all fixes to a file."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            original = content
            fixed = False

            # Apply all fix methods
            content, f1 = self.fix_indented_header_text(content, str(file_path))
            fixed = fixed or f1

            content, f2 = self.fix_missing_closing_quotes(content, str(file_path))
            fixed = fixed or f2

            content, f3 = self.fix_docstring_at_line_3(content, str(file_path))
            fixed = fixed or f3

            if fixed:
                file_path.write_text(content, encoding='utf-8')
                return True

            return False

        except Exception as e:
            self.errors.append(f"{file_path}: {str(e)}")
            return False

    def process_directory(self, directory: str) -> Dict:
        """Process all Python files in directory and subdirectories."""
        dir_path = Path(directory)
        python_files = list(dir_path.rglob("*.py"))

        results = {
            "total": len(python_files),
            "fixed": 0,
            "errors": []
        }

        for py_file in python_files:
            if self.fix_file(py_file):
                results["fixed"] += 1

        results["errors"] = self.errors
        results["fixes"] = self.fixes_applied

        return results


def main():
    """Run comprehensive syntax fixing."""
    print("=" * 70)
    print("  COMPREHENSIVE SYNTAX ERROR FIXER - FINAL PASS")
    print("=" * 70)
    print()

    fixer = ComprehensiveSyntaxFixer()

    print("[1/3] Scanning for all Python files...")
    results = fixer.process_directory("lib")

    print(f"[2/3] Processing {results['total']} files...")
    print()

    print("[3/3] Fix Results:")
    print(f"  Files Fixed: {results['fixed']}")
    print(f"  Errors: {len(results['errors'])}")
    print()

    if results['fixes']:
        print("Sample Fixes Applied:")
        for fix in results['fixes'][:15]:
            print(f"  - {fix}")
        if len(results['fixes']) > 15:
            print(f"  ... and {len(results['fixes']) - 15} more")

    print()
    print("=" * 70)
    print(f"  COMPREHENSIVE FIX COMPLETE: {results['fixed']} files repaired")
    print("=" * 70)


if __name__ == "__main__":
    main()
