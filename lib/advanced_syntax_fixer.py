#!/usr/bin/env python3
"""
Advanced Python Syntax Error Fixer
Handles complex syntax error patterns with specific fixes
"""
import ast
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional


class AdvancedSyntaxFixer:
    def __init__(self, lib_dir: str = "lib"):
        """  Init  ."""
        self.lib_dir = Path(lib_dir)
        self.fixes_applied = []
        self.errors_fixed = 0

    def fix_docstring_patterns(self, content: str) -> str:
        """Fix malformed docstring patterns"""
        # Pattern: ""text"" → """text"""
        content = re.sub(r'""([^"]*?)""', r'"""\1"""', content)
        # Pattern: ''text'' → '''text'''
        content = re.sub(r"''([^']*?)''", r"'''\1'''", content)
        return content

    def fix_import_missing(self, content: str, file_path: str) -> str:
        """Add missing imports based on content analysis"""
        lines = content.split("\n")
        imports_to_add = []

        # Check what imports are needed
        if "Path(" in content and "from pathlib import Path" not in content and "import pathlib" not in content:
            imports_to_add.append("from pathlib import Path")

        if "json.loads" in content and "import json" not in content:
            imports_to_add.append("import json")

        if "datetime.datetime" in content and "import datetime" not in content:
            imports_to_add.append("import datetime")

        if "time.time" in content and "import time" not in content:
            imports_to_add.append("import time")

        if "typing." in content and "from typing import" not in content:
            typing_imports = set()
            for match in re.findall(r"typing\.(\w+)", content):
                typing_imports.add(match)
            if typing_imports:
                imports_to_add.append(f'from typing import {", ".join(sorted(typing_imports))}')

        if imports_to_add:
            # Find the right place to insert imports (after docstring, before first code)
            insert_line = 0
            docstring_ended = False

            for i, line in enumerate(lines):
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    docstring_ended = True
                    # Find end of docstring
                    if '"""' in line and line.count('"""') >= 2:
                        insert_line = i + 1
                        break
                    elif "'''" in line and line.count("'''") >= 2:
                        insert_line = i + 1
                        break
                elif docstring_ended and (line.strip().startswith('"""') or line.strip().startswith("'''")):
                    insert_line = i + 1
                    break
                elif docstring_ended and line.strip() and not line.strip().startswith("#"):
                    insert_line = i
                    break
                elif not docstring_ended and line.strip() and not line.startswith("#!") and not line.startswith("# -*-"):
                    insert_line = i
                    break

            # Insert imports
            for import_line in reversed(imports_to_add):
                lines.insert(insert_line, import_line)

            self.fixes_applied.append(f"Added imports: {', '.join(imports_to_add)}")

        return "\n".join(lines)

    def fix_unmatched_parentheses(self, content: str) -> str:
        """Fix unmatched parentheses in function definitions and method calls"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line

            # Fix function definitions with malformed signatures
            # Pattern: def func(params)"... → def func(params): ...
            func_match = re.match(r'(\s*def\s+\w+\s*\([^)]*)"\s*(.*)', line)
            if func_match:
                func_start = func_match.group(1)
                rest = func_match.group(2)
                # Check if there's a docstring following
                if rest.strip().startswith('"""') or rest.strip().startswith("'''"):
                    line = f"{func_start}): {rest}"
                else:
                    line = f"{func_start}):"
                if line != original_line:
                    self.fixes_applied.append(f"Fixed function definition: {original_line.strip()}")

            # Fix unmatched parentheses in print statements
            if (
                "print(" in line
                and not line.rstrip().endswith(")")
                and not line.rstrip().endswith('"""')
                and not line.rstrip().endswith("'''")
            ):
                # Count parentheses
                open_count = line.count("(")
                close_count = line.count(")")
                if open_count > close_count:
                    line = line + ")" * (open_count - close_count)
                    if line != original_line:
                        self.fixes_applied.append(f"Fixed unmatched parentheses: {original_line.strip()}")

            # Fix malformed return statements
            if (
                line.strip().startswith("return")
                and '"' in line
                and not line.strip().endswith('"')
                and not line.strip().endswith("'")
            ):
                # Check if it's a return statement with malformed string
                return_match = re.match(r'(\s*return\s+)([^"\n]*"[^"\n]*)', line)
                if return_match:
                    return_start = return_match.group(1)
                    return_value = return_match.group(2)
                    if return_value.count('"') % 2 != 0:
                        return_value += '"'
                        line = return_start + return_value
                        if line != original_line:
                            self.fixes_applied.append(f"Fixed return statement: {original_line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_unterminated_strings(self, content: str) -> str:
        """Fix unterminated string literals"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Check for unterminated string literals
            if ('"' in line or "'" in line) and not line.strip().startswith("#"):
                # Count quote pairs
                double_quotes = line.count('"')
                single_quotes = line.count("'")

                # Simple heuristic: if odd number of quotes, likely unterminated
                if double_quotes % 2 != 0 and not '"""' in line:
                    if line.strip().endswith('"'):
                        # Line ends with quote but count is odd - might be escaped
                        pass
                    else:
                        line = line + '"'
                        self.fixes_applied.append(f"Fixed unterminated double quote: {line.strip()}")

                elif single_quotes % 2 != 0 and not "'''" in line:
                    if line.strip().endswith("'"):
                        pass
                    else:
                        line = line + "'"
                        self.fixes_applied.append(f"Fixed unterminated single quote: {line.strip()}")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_unicode_characters(self, content: str) -> str:
        """Remove or replace Unicode characters that cause encoding issues"""
        # Replace common Unicode emojis and symbols
        unicode_replacements = {
            "\U0001f504": "[ROTATING]",
            "\U0001f680": "[ROCKET]",
            "\U00002705": "[CHECK]",
            "\U0000274c": "[X]",
            "\U000026a0": "[WARNING]",
            "\U00002139": "[INFO]",
            "\U0001f4ca": "[CHART]",
            "\U0001f4c1": "[FOLDER]",
            "\U0001f527": "[TOOL]",
            "\U0001f389": "[PARTY]",
            "\U0001f4a1": "[IDEA]",
            "\U0001fe5f": "[HOSPITAL]",
            "\U0001f4c8": "[UP_TREND]",
            "\U0001f4c9": "[DOWN_TREND]",
        }

        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            original_line = line
            for unicode_char, replacement in unicode_replacements.items():
                line = line.replace(unicode_char, replacement)

            # Remove any remaining non-ASCII characters from print statements
            if "print(" in line:
                # Remove any non-ASCII characters
                line = re.sub(r"[^\x00-\x7F]+", "", line)
                # Fix empty print statements
                if "print()" in line:
                    line = line.replace("print()", 'print("Processing...")')

            if line != original_line:
                self.fixes_applied.append(f"Fixed Unicode characters: {original_line[:50]}...")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_invalid_line_start(self, content: str) -> str:
        """Fix files that start with invalid syntax on line 2"""
        lines = content.split("\n")

        if len(lines) >= 2:
            line2 = lines[1]
            # Check for common invalid patterns on line 2
            if (
                line2.strip()
                and not line2.startswith("#")
                and not line2.startswith('"""')
                and not line2.startswith("'''")
                and not line2.startswith("import")
                and not line2.startswith("from")
            ):
                # If line 2 has invalid syntax, comment it out or fix it
                if re.match(r'^[^"\'#]*[\(\[\{]', line2):
                    lines[1] = f"# {line2}"
                    self.fixes_applied.append(f"Commented out invalid line 2: {line2[:30]}...")

        return "\n".join(lines)

    def fix_file(self, file_path: Path) -> bool:
        """Fix syntax errors in a single file with advanced techniques"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            content = original_content

            # Apply fixes in sequence
            content = self.fix_unicode_characters(content)
            content = self.fix_docstring_patterns(content)
            content = self.fix_invalid_line_start(content)
            content = self.fix_unmatched_parentheses(content)
            content = self.fix_unterminated_strings(content)
            content = self.fix_import_missing(content, str(file_path))

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
                # Try to provide more specific error info
                lines = content.split("\n")
                if e.lineno and e.lineno <= len(lines):
                    error_line = lines[e.lineno - 1]
                    print(f"       Error line {e.lineno}: {error_line.strip()}")
                return False

        except Exception as e:
            print(f"ERROR: Processing {file_path}: {e}")
            return False

    def fix_all_error_files(self) -> Dict:
        """Fix all files that currently have syntax errors"""
        print("Starting advanced syntax error fixing...")

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

    fixer = AdvancedSyntaxFixer(lib_dir)
    result = fixer.fix_all_error_files()

    print("\n" + "=" * 60)
    print("ADVANCED SYNTAX FIX REPORT")
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
