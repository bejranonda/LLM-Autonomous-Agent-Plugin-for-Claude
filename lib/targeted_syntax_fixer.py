#!/usr/bin/env python3
#     Targeted Python Syntax Error Fixer
    """
Fixes specific patterns identified in the error analysis
import ast
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional


class TargetedSyntaxFixer:
    def __init__(self, lib_dir: str = "lib"):
        self.lib_dir = Path(lib_dir)
        self.fixes_applied = []
        self.errors_fixed = 0

    def fix_function_signature_patterns(self, content: str) -> str:
        """Fix the specific function signature patterns found"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line

            # Pattern 1: def func(params))): """"doc"""
            if re.match(r'\s*def\s+\w+\s*\([^)]*\)\)\)\):\s*""""', line):
                # Fix by removing extra ))): and extra quotes
                line = re.sub(r'\)\)\)\):\s*""""', '): """', line)
                self.fixes_applied.append(f"Fixed function signature: {original_line.strip()}")

            # Pattern 2: def func(params)): """"doc"""
            elif re.match(r'\s*def\s+\w+\s*\([^)]*\)\)\:\s*""""', line):
                line = re.sub(r'\)\:\s*""""', '): """', line)
                self.fixes_applied.append(f"Fixed function signature: {original_line.strip()}")

            # Pattern 3: def func(params)): "doc"
            elif re.match(r'\s*def\s+\w+\s*\([^)]*\)\)\:\s*"', line):
                line = re.sub(r'\)\:\s*"', '): """', line)
                # Need to add closing quotes at end of docstring
                self.fixes_applied.append(f"Fixed function signature: {original_line.strip()}")

            # Pattern 4: def func(params))): """doc"""
            elif re.match(r'\s*def\s+\w+\s*\([^)]*\)\)\)\):\s*"""', line):
                line = re.sub(r'\)\)\)\):\s*"""', '): """', line)
                self.fixes_applied.append(f"Fixed function signature: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_unterminated_docstrings(self, content: str) -> str:
        """Fix unterminated docstring patterns"""
        lines = content.split("\n")
        fixed_lines = []
        in_docstring = False
        docstring_start = None

        for i, line in enumerate(lines):
            original_line = line

            # Fix lines that are just """
            if line.strip() == '"""' and not in_docstring:
                # This might be an unterminated docstring start
                # Check if the next line has content
                if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].strip().startswith('"""'):
                    # Likely needs to be closed
                    line = '"""'
                    in_docstring = True
                    docstring_start = i
                    self.fixes_applied.append(f"Fixed docstring start at line {i+1}")

            elif line.strip() == '"""' and in_docstring:
                # Close the docstring
                in_docstring = False
                docstring_start = None

            # Fix pattern: """"text"""
            if '""""' in line:
                line = line.replace('""""', '"""')
                self.fixes_applied.append(f"Fixed quadruple quotes: {original_line.strip()}")

            fixed_lines.append(line)

        # If we're still in a docstring at the end, close it
        if in_docstring and docstring_start is not None:
            fixed_lines.append('"""')
            self.fixes_applied.append(f"Closed unterminated docstring starting at line {docstring_start+1}")

        return "\n".join(fixed_lines)

    def fix_f_string_errors(self, content: str) -> str:
        """Fix f-string syntax errors"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line

            # Fix pattern: f"text{var": "format"
            f_string_pattern = r'f["\']([^"\']*\{[^}]*["\'][^"\']*)["\']'
            matches = re.findall(f_string_pattern, line)
            if matches:
                for match in matches:
                    # This pattern has mismatched quotes inside f-string
                    fixed_match = match.replace('": "', "}: '")
                    line = line.replace(match, fixed_match)
                    self.fixes_applied.append(f"Fixed f-string quotes: {original_line.strip()}")

            # Fix pattern: f"text{var}": ".format"
            if re.search(r'f["\'][^"\']*}[^"\']*["\']:\s*["\'][^"\']*format', line):
                # This is malformed f-string + format mix
                line = re.sub(r'f(["\'][^"\']*}[^"\']*)["\']:\s*["\'][^"\']*format', r"\1.format", line)
                self.fixes_applied.append(f"Fixed f-string/format mix: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_invalid_syntax_lines(self, content: str) -> str:
        """Fix invalid syntax on specific lines"""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            original_line = line

            # Line 2-4: Comment out invalid description lines
            if 1 <= i <= 3:  # Lines 2-4 (0-indexed)
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
                    and " " in line
                ):
                    line = f"# {line}"
                    self.fixes_applied.append(f"Commented out invalid line {i+1}: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_bracket_mismatches(self, content: str) -> str:
        """Fix bracket/brace mismatches"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line

            # Fix pattern: "key": value})  - extra closing brace
            if re.search(r'["\'][^"\']*["\']:\s*[^,\s]*\}\)', line):
                line = re.sub(r"\}\)", "}", line)
                self.fixes_applied.append(f"Fixed extra closing brace: {original_line.strip()}")

            # Fix pattern: [item,}  - wrong closing bracket
            if re.search(r"\[[^\]]*,\s*\}", line):
                line = re.sub(r",\s*\}", "]", line)
                self.fixes_applied.append(f"Fixed bracket mismatch: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_file(self, file_path: Path) -> bool:
        """Apply targeted fixes to a single file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            content = original_content

            # Apply fixes in sequence
            content = self.fix_function_signature_patterns(content)
            content = self.fix_unterminated_docstrings(content)
            content = self.fix_f_string_errors(content)
            content = self.fix_invalid_syntax_lines(content)
            content = self.fix_bracket_mismatches(content)

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

    def manual_fix_specific_files(self) -> None:
        """Manually fix some of the most problematic files"""
        # List of files that need manual intervention
        problem_files = [
            "lib/debug_evaluator.py",
            "lib/fix_plugin.py",
            "lib/git_operations.py",
            "lib/trigger_learning.py",
            "lib/validate_plugin.py",
        ]

        for file_path in problem_files:
            full_path = self.lib_dir / file_path
            if full_path.exists():
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    lines = content.split("\n")
                    fixed_lines = []

                    for i, line in enumerate(lines):
                        # Comment out problematic description lines
                        if (
                            i < 5
                            and line.strip()
                            and not line.startswith("#")
                            and not line.startswith('"""')
                            and not line.startswith("'''")
                            and not line.startswith("import")
                            and not line.startswith("from")
                        ):
                            line = f"# {line}"
                        fixed_lines.append(line)

                    fixed_content = "\n".join(fixed_lines)

                    try:
                        ast.parse(fixed_content)
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(fixed_content)
                        print(f"MANUAL FIX: {file_path}")
                        self.errors_fixed += 1
                        self.fixes_applied.append(f"Manual fix for {file_path}: commented out description lines")
                    except SyntaxError:
                        print(f"Could not fix: {file_path}")

                except Exception as e:
                    print(f"Error with {file_path}: {e}")

    def fix_all_error_files(self) -> Dict:
        """Apply targeted fixes to all files with syntax errors"""
        print("Starting targeted syntax error fixing...")

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

        # Apply manual fixes to specific problematic files
        self.manual_fix_specific_files()

        # Fix remaining error files
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

    fixer = TargetedSyntaxFixer(lib_dir)
    result = fixer.fix_all_error_files()

    print("\n" + "=" * 60)
    print("TARGETED SYNTAX FIX REPORT")
    print("=" * 60)
    print(f"Total Python files: {result['total_files']}")
    print(f"Initial syntax errors: {result['initial_errors']}")
    print(f"Files fixed: {result['files_fixed']}")
    print(f"Remaining errors: {result['remaining_errors']}")
    print(f"Total fixes applied: {len(result['fixes_applied'])}")

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
