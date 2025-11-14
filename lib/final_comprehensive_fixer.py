#!/usr/bin/env python3
#     Final Comprehensive Python Syntax Fixer
    """
Addresses all remaining syntax error patterns with specific fixes
import ast
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional


class FinalComprehensiveFixer:
    def __init__(self, lib_dir: str = "lib"):
        """Initialize the processor with default configuration."""
        self.lib_dir = Path(lib_dir)
        self.fixes_applied = []
        self.errors_fixed = 0

    def fix_function_definition_patterns(self, content: str) -> str:
        """Fix malformed function definitions"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line

            # Pattern: def func(params)": """doc"""
            if re.match(r'\s*def\s+\w+\s*\([^)]*\)"\s*"""', line):
                line = re.sub(r'\)"?\s*"""', '): """', line)
                self.fixes_applied.append(f"Fixed function def: {original_line.strip()}")

            # Pattern: def func(params))): """doc"""
            elif re.match(r'\s*def\s+\w+\s*\([^)]*\)\)\)\:\s*"""', line):
                line = re.sub(r"\)\)\)\:", "):", line)
                self.fixes_applied.append(f"Fixed function def: {original_line.strip()}")

            # Pattern: def func(params)): """doc"""
            elif re.match(r'\s*def\s+\w+\s*\([^)]*\)\)\:\s*"""', line):
                line = re.sub(r"\)\)\:", "):", line)
                self.fixes_applied.append(f"Fixed function def: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_fstring_patterns(self, content: str) -> str:
        """Fix all f-string syntax errors"""
        # Pattern 1: f"text{var": "format"} → f"text{var}: format"
        content = re.sub(r'f"([^"]*)\{([^}]*)": "([^"]*)"}', r'f"\1{\2}: \3"', content)
        content = re.sub(r"f'([^']*)\{([^}]*)': '([^']*)'}", r"f'\1{\2}: \3'", content)

        # Pattern 2: f"text{var": ".1f"} → f"text{var:.1f}"
        content = re.sub(r'f"([^"]*)\{([^}]*): "([^.]*\.[^f]*)f"}', r'f"\1{\2:\3f}"', content)
        content = re.sub(r"f'([^']*)\{([^}]*): '([^.]*\.[^f]*)f'}", r"f'\1{\2:\3f}'", content)

        # Pattern 3: f"text{var": "%"} → f"text{var:%}"
        content = re.sub(r'f"([^"]*)\{([^}]*): "([%]*)"}', r'f"\1{\2:\3}"', content)

        # Pattern 4: Fix remaining quote mismatches in f-strings
        content = re.sub(r'\{([^}]*): "([^"]*)"}', r"{\1:\2}", content)

        # Fix the specific pattern seen in calculate_success_rate.py
        content = re.sub(r'f"([^"]*)": "([^"]*)"}', r'f"\1: \2"', content)

        return content

    def fix_docstring_patterns(self, content: str) -> str:
        """Fix docstring patterns"""
        lines = content.split("\n")
        fixed_lines = []
        in_docstring = False
        docstring_line_start = None

        for i, line in enumerate(lines):
            original_line = line

            # Fix quadruple quotes
            if '""""' in line:
                line = line.replace('""""', '"""')
                self.fixes_applied.append(f"Fixed quadruple quotes: {original_line.strip()}")

            # Fix pattern: """text"""" (extra quote at end)
            if line.endswith('""""') and not line.endswith('"""'):
                line = line[:-1]
                self.fixes_applied.append(f"Fixed extra quote: {original_line.strip()}")

            # Pattern: """"text""" → """text"""
            if '""""' in line and line.count('"""') >= 2:
                parts = line.split('"""')
                if len(parts) >= 3:
                    # Reconstruct with proper triple quotes
                    line = '"""' + '"""'.join(parts[1:-1]) + '"""'
                    self.fixes_applied.append(f"Fixed malformed docstring: {original_line.strip()}")

            # Fix lines that are just """
            if line.strip() == '"""' and not in_docstring:
                in_docstring = True
                docstring_line_start = i
            elif line.strip() == '"""' and in_docstring:
                in_docstring = False
                docstring_line_start = None

            fixed_lines.append(line)

        # Close any open docstrings
        if in_docstring and docstring_line_start is not None:
            fixed_lines.append('"""')
            self.fixes_applied.append(f"Closed docstring at line {docstring_line_start+1}")

        return "\n".join(fixed_lines)

    def fix_invalid_description_lines(self, content: str) -> str:
        """Comment out invalid description lines at start of file"""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            original_line = line

            # Lines 2-5: Comment out invalid description lines
            if 1 <= i <= 4:
                if (
                    line.strip()
                    and not line.startswith("#")
                    and not line.startswith('"""')
                    and not line.startswith("'''")
                    and not line.startswith("import")
                    and not line.startswith("from")
                    and not "=" in line
                    and not "def " in line
                    and not "class " in line
                    and not line.strip().endswith(":")
                    and not line.strip().endswith(".")
                ):
                    line = f"# {line}"
                    self.fixes_applied.append(f"Commented out line {i+1}: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_bracket_and_parentheses_issues(self, content: str) -> str:
        """Fix bracket and parentheses mismatches"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line

            # Fix pattern: "key": value}) → "key": value}
            if re.search(r'["\'][^"\']*["\']:\s*[^,\s]*\}\)', line):
                line = re.sub(r"\}\)", "}", line)
                self.fixes_applied.append(f"Fixed extra ): {original_line.strip()}")

            # Fix pattern: [item,} → [item]
            if re.search(r"\[[^\]]*,\s*\}", line):
                line = re.sub(r",\s*\}", "]", line)
                self.fixes_applied.append(f"Fixed bracket mismatch: {original_line.strip()}")

            # Fix orphaned closing brackets/parentheses
            if line.strip() in [")", "]", "}"]:
                line = f"# {line}"
                self.fixes_applied.append(f"Commented out orphaned bracket: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_string_literal_patterns(self, content: str) -> str:
        """Fix string literal patterns"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line

            # Fix pattern: "text" at end of line without closing
            if line.count('"') % 2 != 0 and not line.rstrip().endswith('"'):
                line = line + '"'
                self.fixes_applied.append(f"Added closing quote: {original_line.strip()}")

            # Fix pattern: 'text' at end of line without closing
            elif line.count("'") % 2 != 0 and not line.rstrip().endswith("'"):
                line = line + "'"
                self.fixes_applied.append(f"Added closing quote: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_file(self, file_path: Path) -> bool:
        """Apply all fixes to a single file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            content = original_content

            # Apply fixes in sequence
            content = self.fix_invalid_description_lines(content)
            content = self.fix_function_definition_patterns(content)
            content = self.fix_fstring_patterns(content)
            content = self.fix_docstring_patterns(content)
            content = self.fix_string_literal_patterns(content)
            content = self.fix_bracket_and_parentheses_issues(content)

            # Validate the fix
            try:
                ast.parse(content)
                # If parsing succeeds, write the fixed content
                if content != original_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"FIXED: {file_path}")
                    self.errors_fixed += 1
                    return True
                else:
                    print(f"No changes needed: {file_path}")
                    return False
            except SyntaxError as e:
                print(f"ERROR: Still has syntax errors: {file_path} - {e}")
                # Show the problematic line
                lines = content.split("\n")
                if e.lineno and e.lineno <= len(lines):
                    error_line = lines[e.lineno - 1]
                    print(f"       Error line {e.lineno}: {error_line.strip()}")
                return False

        except Exception as e:
            print(f"ERROR: Processing {file_path}: {e}")
            return False

    def fix_all_error_files(self) -> Dict:
        """Apply comprehensive fixes to all files with syntax errors"""
        print("Starting final comprehensive syntax error fixing...")

        # First, identify files with syntax errors
        error_files = []
        python_files = list(self.lib_dir.rglob("*.py"))

        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                ast.parse(content)
            except SyntaxError:
                error_files.append(file_path)
            except Exception:
                pass  # Skip files that can't be read

        print(f"Found {len(error_files)} files with syntax errors")

        # Fix each error file
        for file_path in error_files:
            self.fix_file(file_path)

        # Validate all files now compile
        final_errors = []
        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                ast.parse(content)
            except SyntaxError:
                final_errors.append(str(file_path))
            except Exception:
                pass

        return {
            "total_files": len(python_files),
            "initial_errors": len(error_files),
            "files_fixed": self.errors_fixed,
            "remaining_errors": len(final_errors),
            "error_files": final_errors,
            "fixes_applied": self.fixes_applied,
        }


def main():
    """Main execution function"""
    if len(sys.argv) > 1:
        lib_dir = sys.argv[1]
    else:
        lib_dir = "lib"

    fixer = FinalComprehensiveFixer(lib_dir)
    result = fixer.fix_all_error_files()

    print("\n" + "=" * 60)
    print("FINAL COMPREHENSIVE SYNTAX FIX REPORT")
    print("=" * 60)
    print(f"Total Python files: {result['total_files']}")
    print(f"Initial syntax errors: {result['initial_errors']}")
    print(f"Files fixed: {result['files_fixed']}")
    print(f"Remaining errors: {result['remaining_errors']}")
    print(f"Total fixes applied: {len(result['fixes_applied'])}")

    success_rate = (result["files_fixed"] / result["initial_errors"] * 100) if result["initial_errors"] > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")

    if result["remaining_errors"] > 0:
        print(f"\nRemaining files with errors:")
        for error_file in result["error_files"][:10]:
            print(f"  - {error_file}")
        if len(result["error_files"]) > 10:
            print(f"  ... and {len(result['error_files']) - 10} more")
    else:
        print("\nSUCCESS: All Python files now compile successfully!")

    if result["fixes_applied"]:
        print(f"\nSample fixes applied:")
        for fix in result["fixes_applied"][:15]:
            print(f"  - {fix}")
        if len(result["fixes_applied"]) > 15:
            print(f"  ... and {len(result['fixes_applied']) - 15} more fixes")

    return result


if __name__ == "__main__":
    main()
