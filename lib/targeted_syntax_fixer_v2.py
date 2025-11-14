#!/usr/bin/env python3
"""
Targeted Syntax Fixer v2
Fixes specific syntax errors identified in the 31 files with pattern-based fixes.
"""

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
        self.files_fixed = []
        self.files_failed = []

    def check_syntax(self, file_path: Path) -> Tuple[bool, Optional[str]]:
        """Check if a Python file has valid syntax."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            ast.parse(content)
            return True, None
        except SyntaxError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error reading file: {str(e)}"

    def fix_malformed_shebang(self, content: str) -> str:
        """Fix malformed shebang lines like #!/usr/bin/env python3,\"\"\" """
        lines = content.split("\n")
        if lines and lines[0].startswith("#!/usr/bin/env python3"):
            # Fix various shebang issues
            lines[0] = "#!/usr/bin/env python3"
        return "\n".join(lines)

    def fix_malformed_docstring_start(self, content: str) -> str:
        """Fix malformed docstring starts"""
        # Pattern: #!/usr/bin/env python3,"""  ->  #!/usr/bin/env python3\n"""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            if i == 0 and line.startswith("#!/usr/bin/env python3"):
                # Handle shebang
                if line.count('"') >= 3:
                    # Extract just the shebang part
                    fixed_lines.append("#!/usr/bin/env python3")
                    # Start docstring on next line
                    if '"""' in line:
                        remaining = line.split('"""', 1)[1].strip()
                        if remaining:
                            fixed_lines.append('"""')
                            fixed_lines.append(remaining)
                        else:
                            fixed_lines.append('"""')
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

        for i, line in enumerate(lines):
            if not in_triple_quote:
                # Count triple quotes in this line
                double_triple = line.count('"""')
                single_triple = line.count("'''")

                if double_triple % 2 != 0:
                    in_triple_quote = True
                    quote_type = '"""'
                elif single_triple % 2 != 0:
                    in_triple_quote = True
                    quote_type = "'''"

                fixed_lines.append(line)
            else:
                # We're in a triple quote, look for the end
                if quote_type in line:
                    in_triple_quote = False
                    quote_type = None
                fixed_lines.append(line)

        # If we ended while still in triple quote, close it
        if in_triple_quote:
            fixed_lines.append(quote_type)
            self.fixes_applied.append("Closed unterminated triple quote")

        return "\n".join(fixed_lines)

    def fix_unmatched_parentheses(self, content: str) -> str:
        """Fix unmatched parentheses in function definitions and other structures"""
        # Fix malformed function definitions
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Fix function definitions with malformed parameters
            if re.match(r'\s*def\s+\w+\s*\([^)]*"[^"]*?"', line):
                # Remove quotes from function parameters
                fixed_line = re.sub(r'"([^"]*?)"', r"\1", line)
                fixed_lines.append(fixed_line)
                if fixed_line != line:
                    self.fixes_applied.append(f"Fixed function definition: {line.strip()}")
            else:
                fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_invalid_syntax_start(self, content: str) -> str:
        """Fix invalid syntax at the start of files"""
        lines = content.split("\n")

        # Fix files that start with invalid syntax
        if len(lines) > 0:
            first_line = lines[0].strip()

            # If first line is just a quote or malformed
            if first_line == '"' or first_line == "'" or first_line.startswith('"""') and not first_line.endswith('"""'):
                # Insert proper shebang and docstring
                lines.insert(0, "#!/usr/bin/env python3")
                lines.insert(1, "")
                lines.insert(2, '"""')
                if not lines[3].endswith('"""'):
                    lines.append('"""')
                self.fixes_applied.append("Fixed invalid file start")

        return "\n".join(lines)

    def fix_string_literals(self, content: str) -> str:
        """Fix various string literal issues"""
        # Fix common string literal patterns
        content = re.sub(r'print\(\s*([^")\'][^)]*)\s*\)', r'print("\1")', content)

        # Fix malformed dictionary keys
        content = re.sub(
            r"(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)(\s*,|\s*\})", r'\1"\2": "\3"\4', content
        )

        return content

    def apply_all_fixes(self, content: str) -> str:
        """Apply all fixes in sequence"""
        original = content

        content = self.fix_malformed_shebang(content)
        content = self.fix_malformed_docstring_start(content)
        content = self.fix_invalid_syntax_start(content)
        content = self.fix_unmatched_parentheses(content)
        content = self.fix_string_literals(content)
        content = self.fix_unterminated_triple_quotes(content)

        if content != original:
            self.fixes_applied.append("Applied comprehensive fixes")

        return content

    def fix_file(self, file_path: Path) -> bool:
        """Fix syntax errors in a single file"""
        print(f"Processing: {file_path.name}")

        try:
            # Read with error handling for encoding issues
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                original_content = f.read()

            # Check if it already has valid syntax
            is_valid, error = self.check_syntax(file_path)
            if is_valid:
                print(f"  [OK] Already valid")
                return True

            print(f"  [ERROR] {error}")

            # Apply fixes
            fixed_content = self.apply_all_fixes(original_content)

            # Write fixed content to temp file and test
            temp_file = file_path.with_suffix(".tmp")
            try:
                with open(temp_file, "w", encoding="utf-8") as f:
                    f.write(fixed_content)

                # Test the fixed content
                is_valid, new_error = self.check_syntax(temp_file)

                if is_valid:
                    # Success! Replace the original
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(fixed_content)
                    print(f"  [FIXED] Successfully")
                    self.files_fixed.append(file_path.name)
                    return True
                else:
                    print(f"  [FAILED] Still has errors: {new_error}")
                    self.files_failed.append(file_path.name)
                    return False

            finally:
                # Clean up temp file
                if temp_file.exists():
                    temp_file.unlink()

        except Exception as e:
            print(f"  [EXCEPTION] {e}")
            self.files_failed.append(file_path.name)
            return False

    def fix_targeted_files(self) -> Dict:
        """Fix the 31 specific files mentioned in the task"""
        files_to_fix = [
            "backfill_assessments.py",
            "backup_manager.py",
            "calculate_debugging_performance.py",
            "calculate_real_performance.py",
            "calculate_success_rate.py",
            "calculate_time_based_debugging_performance.py",
            "calculate_time_based_performance.py",
            "command_validator.py",
            "dashboard_compatibility.py",
            "dashboard_validator.py",
            "debug_evaluator.py",
            "dependency_graph.py",
            "dependency_scanner.py",
            "enhanced_learning_broken.py",
            "fix_plugin.py",
            "git_operations.py",
            "learning_analytics.py",
            "linter_orchestrator.py",
            "model_performance.py",
            "model_switcher.py",
            "performance_recorder.py",
            "plugin_validator.py",
            "predictive_analytics.py",
            "predictive_skills.py",
            "quality_tracker_broken.py",
            "recovery_manager.py",
            "simple_backfill.py",
            "smart_agent_suggester.py",
            "trigger_learning.py",
            "validate_plugin.py",
            "validation_hooks.py",
        ]

        print(f"Starting targeted syntax fixing for {len(files_to_fix)} files...")
        print("=" * 60)

        for filename in files_to_fix:
            file_path = self.lib_dir / filename
            if file_path.exists():
                self.fix_file(file_path)
            else:
                print(f"NOT FOUND: {filename}")
                self.files_failed.append(filename)
            print()

        return {
            "files_fixed": self.files_fixed,
            "files_failed": self.files_failed,
            "fixes_applied": self.fixes_applied,
            "total_targeted": len(files_to_fix),
        }


def main():
    """Main execution function"""
    if len(sys.argv) > 1:
        lib_dir = sys.argv[1]
    else:
        lib_dir = "lib"

    fixer = TargetedSyntaxFixer(lib_dir)
    result = fixer.fix_targeted_files()

    print("=" * 60)
    print("TARGETED SYNTAX FIX REPORT")
    print("=" * 60)
    print(f"Files targeted: {result['total_targeted']}")
    print(f"Files fixed: {len(result['files_fixed'])}")
    print(f"Files failed: {len(result['files_failed'])}")
    print()

    if result["files_fixed"]:
        print("SUCCESSFULLY FIXED:")
        for filename in result["files_fixed"]:
            print(f"  [FIXED] {filename}")
        print()

    if result["files_failed"]:
        print("FAILED TO FIX:")
        for filename in result["files_failed"]:
            print(f"  [FAILED] {filename}")
        print()

    if result["fixes_applied"]:
        print("FIXES APPLIED:")
        for i, fix in enumerate(result["fixes_applied"][:10]):
            print(f"  {i+1}. {fix}")
        if len(result["fixes_applied"]) > 10:
            print(f"  ... and {len(result['fixes_applied']) - 10} more fixes")
        print()

    success_rate = len(result["files_fixed"]) / result["total_targeted"] * 100
    print(f"Success rate: {success_rate:.1f}%")

    if len(result["files_failed"]) == 0:
        print("SUCCESS: ALL TARGETED FILES FIXED!")
    else:
        print(f"WARNING: {len(result['files_failed'])} files still need manual attention")


if __name__ == "__main__":
    main()
