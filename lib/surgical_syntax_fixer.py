#!/usr/bin/env python3
#     Surgical Python Syntax Error Fixer
    """
Targets specific syntax error patterns identified in the analysis
import ast
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional


class SurgicalSyntaxFixer:
    def __init__(self, lib_dir: str = "lib"):
        self.lib_dir = Path(lib_dir)
        self.fixes_applied = []
        self.errors_fixed = 0

    def fix_malformed_function_definitions(self, content: str) -> str:
        """Fix the specific pattern: def func(params): docstring"""
        # Pattern: def function_name(params)": """docstring"""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            original_line = line

            # Fix malformed function definitions
            if "def " in line and '":' in line:
                # Pattern: def func(params)": """doc"""
                if '": """' in line:
                    line = line.replace('": """', '): """')
                    self.fixes_applied.append(f"Fixed function def: {original_line.strip()}")
                elif '":' in line and not line.strip().endswith(":"):
                    line = line.replace('":', "):")
                    self.fixes_applied.append(f"Fixed function def: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_unterminated_triple_quotes(self, content: str) -> str:
        """Fix unterminated triple-quoted docstrings"""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            original_line = line

            # Fix malformed triple quotes at function level
            # Pattern: """"text"""" → """text"""
            if '""""' in line:
                line = line.replace('""""', '"""')
                self.fixes_applied.append(f"Fixed quadruple quotes: {original_line.strip()}")

            # Fix pattern: """"text""" → """text"""
            if '""""' in line:
                line = line.replace('""""', '"""')
                self.fixes_applied.append(f"Fixed malformed triple quotes: {original_line.strip()}")

            # Fix pattern: """" → """ (at start of docstring)
            if line.strip() == '""""':
                line = line.replace('""""', '"""')
                self.fixes_applied.append(f"Fixed docstring start: {original_line.strip()}")

            # Fix pattern: """text"""" (extra quote at end)
            if line.endswith('""""') and not line.endswith('"""'):
                line = line[:-1]  # Remove last quote
                self.fixes_applied.append(f"Fixed docstring end: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_unmatched_f_string_braces(self, content: str) -> str:
        """Fix f-string brace mismatches"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line

            # Fix pattern: f"text{var" → f"text{var}"
            if 'f"' in line or "f'" in line:
                # Count opening and closing braces in f-strings
                f_string_match = re.search(r'f["\']([^"\']*)["\']', line)
                if f_string_match:
                    f_content = f_string_match.group(1)
                    open_braces = f_content.count("{")
                    close_braces = f_content.count("}")
                    if open_braces > close_braces:
                        # Add missing closing braces
                        missing_braces = open_braces - close_braces
                        line = line.replace(
                            f_string_match.group(0),
                            f_string_match.group(0)[:-1] + "}" * missing_braces + f_string_match.group(0)[-1],
                        )
                        self.fixes_applied.append(f"Fixed f-string braces: {original_line.strip()}")
                    elif close_braces > open_braces:
                        # Remove extra closing braces
                        extra_braces = close_braces - open_braces
                        line = line.replace(f_string_match.group(0), f_string_match.group(0).replace("}" * extra_braces, ""))
                        self.fixes_applied.append(f"Fixed f-string braces: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_malformed_docstring_lines(self, content: str) -> str:
        """Fix lines that contain malformed docstring patterns"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line

            # Fix pattern: """"text""" (malformed docstring)
            if '""""' in line and line.count('"""') >= 2:
                # This is likely a malformed docstring
                line = line.replace('""""', '"""')
                # If there are still 4 quotes, fix it
                if line.count('"""') > 2:
                    # Find the first occurrence and keep only 3 quotes
                    first_pos = line.find('"""')
                    line = line[:first_pos] + '"""' + line[first_pos + 4 :].replace('"""', "", 1)
                self.fixes_applied.append(f"Fixed malformed docstring: {original_line.strip()}")

            # Fix pattern: single line with "text""" (missing opening quote)
            if not line.startswith('"""') and line.endswith('"""') and '"' in line and line.count('"') >= 4:
                # Likely needs opening triple quotes
                line = line.replace('"', '"""', 1)
                self.fixes_applied.append(f"Fixed docstring opening: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_invalid_line_syntax(self, content: str) -> str:
        """Fix files with invalid syntax on specific lines"""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            original_line = line

            # Line 2 issue: comment out invalid non-comment, non-import lines
            if i == 1:  # Line 2 (0-indexed)
                if (
                    line.strip()
                    and not line.startswith("#")
                    and not line.startswith('"""')
                    and not line.startswith("'''")
                    and not line.startswith("import")
                    and not line.startswith("from")
                    and not "=" in line  # Not a variable assignment
                    and not "def " in line  # Not a function definition
                    and not "class " in line
                ):  # Not a class definition
                    line = f"# {line}"
                    self.fixes_applied.append(f"Commented out invalid line 2: {original_line.strip()}")

            # Line 3 issue: similar check for line 3
            elif i == 2:  # Line 3 (0-indexed)
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
                    and " " in line
                    and not line.strip().endswith(".")
                ):
                    # Likely a description line that should be a comment
                    line = f"# {line}"
                    self.fixes_applied.append(f"Commented out invalid line 3: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_bare_parentheses_lines(self, content: str) -> str:
        """Fix lines that contain just closing parentheses or brackets"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line

            # Remove lines that are just bare closing brackets
            if line.strip() in [")", "]", "}"]:
                # This is likely an orphaned closing bracket
                line = f"# {line}"
                self.fixes_applied.append(f"Commented out orphaned bracket: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_file(self, file_path: Path) -> bool:
        """Apply surgical fixes to a single file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            content = original_content

            # Apply fixes in sequence
            content = self.fix_malformed_function_definitions(content)
            content = self.fix_unterminated_triple_quotes(content)
            content = self.fix_malformed_docstring_lines(content)
            content = self.fix_unmatched_f_string_braces(content)
            content = self.fix_invalid_line_syntax(content)
            content = self.fix_bare_parentheses_lines(content)

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
        """Apply surgical fixes to all files with syntax errors"""
        print("Starting surgical syntax error fixing...")

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

    fixer = SurgicalSyntaxFixer(lib_dir)
    result = fixer.fix_all_error_files()

    print("\n" + "=" * 60)
    print("SURGICAL SYNTAX FIX REPORT")
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
        for fix in result["fixes_applied"][:20]:
            print(f"  - {fix}")
        if len(result["fixes_applied"]) > 20:
            print(f"  ... and {len(result['fixes_applied']) - 20} more fixes")

    return result


if __name__ == "__main__":
    main()
