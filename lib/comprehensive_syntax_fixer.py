#!/usr/bin/env python3
#     Comprehensive Python Syntax Error Fixer
"""
Autonomously identifies and fixes syntax errors in Python files
"""
import ast
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional


class PythonSyntaxFixer:
    def __init__(self, lib_dir: str = "lib"):
        """Initialize the processor with default configuration."""
        self.lib_dir = Path(lib_dir)
        self.fixes_applied = []
        self.errors_found = []
        self.files_processed = 0
        self.files_fixed = 0

    def scan_for_syntax_errors(self) -> Dict[str, List[str]]:
        """Scan all Python files and identify syntax errors"""
        print("Scanning Python files for syntax errors...")

        syntax_errors = {}
        python_files = list(self.lib_dir.rglob("*.py"))

        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Try to parse with ast
                try:
                    ast.parse(content)
                except SyntaxError as e:
                    syntax_errors[str(file_path)] = [str(e)]
                    self.errors_found.append(f"{file_path}: {e}")

            except Exception as e:
                print(f"WARNING: Could not read {file_path}: {e}")

        print(f"Found {len(syntax_errors)} files with syntax errors")
        return syntax_errors

    def identify_error_patterns(self, content: str, file_path: str) -> List[Dict]:
        """Identify specific error patterns in content"""
        patterns = []

        # Pattern 1: Invalid Unicode characters (emojis)
        unicode_pattern = r"print\([^)]*[\\u][0-9a-fA-F]+[^)]*\)"
        if re.search(unicode_pattern, content):
            patterns.append(
                {
                    "type": "invalid_unicode",
                    "pattern": unicode_pattern,
                    "description": "Invalid Unicode characters in print statements",
                }
            )

        # Pattern 2: Unterminated triple-quoted strings
        triple_quote_issues = []
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            # Check for unclosed triple quotes
            if '"""' in line or "'''" in line:
                quote_count = line.count('"""') + line.count("'''")
                if quote_count % 2 != 0:
                    triple_quote_issues.append(f"Line {i}: {line.strip()}")

        if triple_quote_issues:
            patterns.append(
                {
                    "type": "unterminated_triple_quotes",
                    "issues": triple_quote_issues,
                    "description": "Unterminated triple-quoted strings",
                }
            )

        # Pattern 3: Malformed function definitions
        malformed_func_pattern = r'def\s+(\w+)\s*\([^)]*"[^"]*?"\s*[^:]*'
        if re.search(malformed_func_pattern, content):
            patterns.append(
                {
                    "type": "malformed_function_def",
                    "pattern": malformed_func_pattern,
                    "description": "Malformed function definitions with quotes instead of colons",
                }
            )

        # Pattern 4: Missing imports
        if "Path(" in content and "from pathlib import Path" not in content:
            patterns.append({"type": "missing_import_pathlib", "description": "Missing import for Path from pathlib"})

        if "json.loads" in content and "import json" not in content:
            patterns.append({"type": "missing_import_json", "description": "Missing import for json module"})

        return patterns

    def fix_unicode_characters(self, content: str) -> str:
        """Remove or fix invalid Unicode characters"""
        # Remove emojis from print statements
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Remove Unicode escape sequences and emojis
            if "print(" in line and ("\\u" in line or any(ord(c) > 127 for c in line)):
                # Remove Unicode characters, keep the print statement
                cleaned = re.sub(r"\\u[0-9a-fA-F]+", "", line)
                cleaned = re.sub(r"[^\x00-\x7F]+", "", cleaned)
                # Ensure print statement is still valid
                if "print(  )" in cleaned:
                    cleaned = cleaned.replace("print(  )", 'print("Starting process...")')
                fixed_lines.append(cleaned)
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_malformed_function_definitions(self, content: str) -> str:
        """Fix malformed function definitions"""
        # Pattern: def func(params)": """doc"""  →  def func(params): """doc""""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Fix malformed function definitions
            if re.match(r'\s*def\s+\w+\s*\([^)]*"[^"]*?"\s*[^:]*', line):
                # Extract function signature
                func_match = re.match(r'(\s*def\s+\w+\s*\([^)]*)"[^"]*?"(\s*)(.*)', line)
                if func_match:
                    indent = func_match.group(1)
                    rest = func_match.group(3)
                    # Fix the function definition
                    if rest and not rest.startswith(":"):
                        fixed_line = f"{indent}): {rest}"
                    else:
                        fixed_line = f"{indent}):"
                    fixed_lines.append(fixed_line)
                    self.fixes_applied.append(f"Fixed function definition: {line.strip()}")
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_unterminated_triple_quotes(self, content: str) -> str:
        """Fix unterminated triple-quoted strings"""
        lines = content.split("\n")
        fixed_lines = []
        in_triple_quote = False
        quote_type = None
        quote_start_line = None

        for i, line in enumerate(lines):
            original_line = line

            if not in_triple_quote:
                # Check for starting triple quotes
                if '"""' in line:
                    count = line.count('"""')
                    if count % 2 != 0:
                        in_triple_quote = True
                        quote_type = '"""'
                        quote_start_line = i
                elif "'''" in line:
                    count = line.count("'''")
                    if count % 2 != 0:
                        in_triple_quote = True
                        quote_type = "'''"
                        quote_start_line = i
            else:
                # Check for ending triple quotes
                if quote_type in line:
                    in_triple_quote = False
                    quote_type = None
                    quote_start_line = None

            # If we're at the end of file and still in triple quote, close it
            if i == len(lines) - 1 and in_triple_quote:
                line += f"\n{quote_type}"
                self.fixes_applied.append(f"Closed unterminated triple quote at line {quote_start_line + 1}")
                in_triple_quote = False

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def add_missing_imports(self, content: str) -> str:
        """Add missing import statements"""
        lines = content.split("\n")
        fixed_lines = []
        imports_added = []

        # Find where to add imports (after shebang or first comment)
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.startswith("#!") or line.startswith("# -*-") or line.startswith("# coding:"):
                insert_pos = i + 1
            elif line.strip() == "" or line.startswith("#"):
                continue
            else:
                break

        # Add missing imports
        if "Path(" in content and "from pathlib import Path" not in content:
            lines.insert(insert_pos, "from pathlib import Path")
            imports_added.append("pathlib.Path")
            insert_pos += 1

        if "json.loads" in content and "import json" not in content:
            lines.insert(insert_pos, "import json")
            imports_added.append("json")
            insert_pos += 1

        if imports_added:
            self.fixes_applied.append(f"Added imports: {', '.join(imports_added)}")

        return "\n".join(lines)

    def fix_file(self, file_path: Path) -> bool:
        """Fix syntax errors in a single file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            content = original_content
            file_fixes = []

            # Apply fixes in sequence
            patterns = self.identify_error_patterns(content, str(file_path))

            for pattern in patterns:
                if pattern["type"] == "invalid_unicode":
                    content = self.fix_unicode_characters(content)
                    file_fixes.append("Fixed Unicode characters")

                elif pattern["type"] == "malformed_function_def":
                    content = self.fix_malformed_function_definitions(content)
                    file_fixes.append("Fixed function definitions")

                elif pattern["type"] == "unterminated_triple_quotes":
                    content = self.fix_unterminated_triple_quotes(content)
                    file_fixes.append("Fixed triple quotes")

                elif pattern["type"] in ["missing_import_pathlib", "missing_import_json"]:
                    content = self.add_missing_imports(content)
                    file_fixes.append("Added missing imports")

            # Validate the fix
            try:
                ast.parse(content)
                # If parsing succeeds, write the fixed content
                if content != original_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    self.fixes_applied.extend([f"{file_path}: {fix}" for fix in file_fixes])
                    print(f"FIXED: {file_path}")
                    return True
                else:
                    print(f"No fixes needed: {file_path}")
                    return False
            except SyntaxError as e:
                print(f"ERROR: Still has syntax errors after fix: {file_path} - {e}")
                return False

        except Exception as e:
            print(f"ERROR: Processing {file_path}: {e}")
            return False

    def validate_compilation(self, file_path: Path) -> bool:
        """Validate that a Python file compiles successfully"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            ast.parse(content)
            return True
        except Exception:
            return False

    def fix_all_files(self) -> Dict:
        """Fix all Python files in the lib directory"""
        print("Starting comprehensive syntax error fixing...")

        python_files = list(self.lib_dir.rglob("*.py"))
        print(f"Found {len(python_files)} Python files")

        # First pass: identify syntax errors
        syntax_errors = self.scan_for_syntax_errors()

        if not syntax_errors:
            print("SUCCESS: No syntax errors found!")
            return {"status": "success", "files_processed": len(python_files), "files_fixed": 0, "fixes_applied": []}

        # Second pass: fix files with errors
        for file_path in python_files:
            self.files_processed += 1
            if self.fix_file(file_path):
                self.files_fixed += 1

        # Third pass: validate all files compile
        print("\nValidating all files compile successfully...")
        compilation_errors = []
        for file_path in python_files:
            if not self.validate_compilation(file_path):
                compilation_errors.append(str(file_path))

        result = {
            "status": "success" if not compilation_errors else "partial",
            "files_processed": self.files_processed,
            "files_fixed": self.files_fixed,
            "fixes_applied": self.fixes_applied,
            "compilation_errors": compilation_errors,
            "initial_syntax_errors": len(syntax_errors),
        }

        return result


def main():
    """Main execution function"""
    if len(sys.argv) > 1:
        lib_dir = sys.argv[1]
    else:
        lib_dir = "lib"

    fixer = PythonSyntaxFixer(lib_dir)
    result = fixer.fix_all_files()

    print("\n" + "=" * 60)
    print("COMPREHENSIVE SYNTAX FIX REPORT")
    print("=" * 60)
    print(f"Files processed: {result['files_processed']}")
    print(f"Files fixed: {result['files_fixed']}")
    print(f"Initial syntax errors: {result['initial_syntax_errors']}")
    print(f"Fixes applied: {len(result['fixes_applied'])}")

    if result["compilation_errors"]:
        print(f"ERROR: Still have compilation errors: {len(result['compilation_errors'])}")
        for error in result["compilation_errors"][:5]:  # Show first 5
            print(f"   - {error}")
    else:
        print("SUCCESS: All files now compile successfully!")

    if result["fixes_applied"]:
        print(f"\nSample fixes applied:")
        for fix in result["fixes_applied"][:10]:  # Show first 10
            print(f"   - {fix}")
        if len(result["fixes_applied"]) > 10:
            print(f"   ... and {len(result['fixes_applied']) - 10} more fixes")

    return result


if __name__ == "__main__":
    main()
