#!/usr/bin/env python3
"""
Manual Syntax Fixer - Systematic file-by-file fixing approach
"""

import ast
import os
import re
from pathlib import Path


def clean_content(content):
    """Clean content by removing non-printable characters and fixing common issues"""
    # Remove non-printable characters except \n, \t
    cleaned = "".join(char for char in content if char.isprintable() or char in "\n\t")

    # Fix malformed shebang
    lines = cleaned.split("\n")
    if lines and lines[0].startswith("#!/usr/bin/env python3"):
        if lines[0].count('"') > 0:
            lines[0] = "#!/usr/bin/env python3"

    return "\n".join(lines)


def fix_file_syntax(file_path):
    """Fix syntax errors in a single file manually"""
    print(f"Fixing: {file_path.name}")

    try:
        # Read the file carefully
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Clean the content
        content = clean_content(content)

        # Apply specific fixes based on common patterns

        # 1. Fix malformed shebang and docstring start
        lines = content.split("\n")
        if lines and 'python3,"""' in lines[0]:
            lines[0] = "#!/usr/bin/env python3"
            if len(lines) > 1 and lines[1].strip().startswith('"""'):
                # Keep the docstring as is
                pass
            else:
                # Insert docstring start if needed
                lines.insert(1, '"""')
                if len(lines) > 2 and not lines[2].strip().endswith('"""'):
                    lines.append('"""')

        content = "\n".join(lines)

        # 2. Fix unterminated triple quotes by ensuring proper closing
        triple_quote_count = content.count('"""')
        if triple_quote_count % 2 != 0:
            # Add closing triple quote at the end
            content += '\n"""'
            print(f"  Added closing triple quote")

        # 3. Fix unmatched parentheses in function definitions
        # Look for malformed function signatures
        content = re.sub(r'def\s+(\w+)\s*\(\s*([^)]*?)"\s*[^)]*?\)', r"def \1(\2)", content)

        # 4. Fix missing quotes in dictionary keys
        # Simple pattern: word: value (where value looks like a string)
        content = re.sub(r"(\s)([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)(\s*[,\}])", r'\1"\2": "\3"\4', content)

        # Write the fixed content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Test if it's now valid
        try:
            ast.parse(content)
            print(f"  [SUCCESS] Fixed successfully")
            return True
        except SyntaxError as e:
            print(f"  [FAILED] Still has syntax errors: {e}")
            return False

    except Exception as e:
        print(f"  [ERROR] Exception: {e}")
        return False


def main():
    """Main function"""
    # Files to fix (from the task)
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
        "debug_evaluator.py",  # Already fixed
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

    lib_dir = Path("lib")
    fixed_count = 0
    failed_count = 0

    print("MANUAL SYNTAX FIXER - Processing files one by one")
    print("=" * 60)

    for filename in files_to_fix:
        file_path = lib_dir / filename
        if file_path.exists():
            if fix_file_syntax(file_path):
                fixed_count += 1
            else:
                failed_count += 1
        else:
            print(f"NOT FOUND: {filename}")
            failed_count += 1
        print()

    print("=" * 60)
    print("SUMMARY:")
    print(f"Files processed: {len(files_to_fix)}")
    print(f"Successfully fixed: {fixed_count}")
    print(f"Failed to fix: {failed_count}")
    print(f"Success rate: {fixed_count / len(files_to_fix) * 100:.1f}%")

    if failed_count == 0:
        print("SUCCESS: All files fixed!")
    else:
        print(f"WARNING: {failed_count} files still need attention")


if __name__ == "__main__":
    main()
