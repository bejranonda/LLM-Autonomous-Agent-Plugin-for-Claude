#!/usr/bin/env python3
"""
Final comprehensive syntax fix for all remaining issues
"""

import re
from pathlib import Path


def fix_docstring_quotes(content):
    """Fix multiple or incomplete docstring quotes"""
    lines = content.split("\n")
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Fix incomplete docstring at beginning
        if line.strip() == '""' and i + 1 < len(lines):
            next_line = lines[i + 1]
            if not next_line.strip().startswith('"""') and not next_line.strip().startswith('"""'):
                # This is likely an incomplete docstring start
                fixed_lines.append('"""')
                fixed_lines.append(next_line)
                i += 2
                continue

        # Fix single quote docstring
        if line.strip() == '""' and i > 0:
            prev_line = lines[i - 1]
            if '"""' in prev_line:
                # This is likely the end of a docstring
                fixed_lines.append('"""')
                i += 1
                continue

        # Fix double quote starts
        if line.strip() == '""' and i + 2 < len(lines):
            # Look ahead to see if this is a complete docstring
            if '"""' in lines[i + 1] and '"""' in lines[i + 2]:
                # Multiple docstring quotes - collapse to one
                fixed_lines.append('"""')
                # Add the content from the middle line
                content_line = lines[i + 1].replace('"""', "").strip()
                if content_line:
                    fixed_lines.append(content_line)
                i += 3
                continue

        fixed_lines.append(line)
        i += 1

    return "\n".join(fixed_lines)


def fix_common_patterns(content):
    """Fix common syntax patterns"""
    # Fix incomplete docstrings
    content = re.sub(r'^""\s*$', '"""', content, flags=re.MULTILINE)

    # Fix double docstring quotes
    content = re.sub(r'"""\s*"""', '"""', content)

    # Fix missing import statements
    if "import sys" not in content and "sys." in content:
        content = "import sys\n" + content

    if "from datetime import" not in content and ("datetime" in content or "timezone" in content):
        content = "from datetime import datetime, timezone\n" + content

    if "from typing import" not in content and ("Dict" in content or "List" in content or "Any" in content):
        typing_imports = []
        if "Dict" in content:
            typing_imports.append("Dict")
        if "List" in content:
            typing_imports.append("List")
        if "Any" in content:
            typing_imports.append("Any")
        if typing_imports:
            content = f"from typing import {', '.join(typing_imports)}\n" + content

    # Fix import statement issues
    content = re.sub(r'"import\s+', "import ", content)
    content = re.sub(r'"from\s+', "from ", content)

    # Fix incomplete f-strings
    content = re.sub(r'f"([^"]*?)\}', r'f"\1"', content)

    # Fix incomplete function calls
    content = re.sub(r"time\.time\}", "time.time()", content)
    content = re.sub(r"datetime\.now\(\)\.isoformat\(\}", "datetime.now().isoformat()", content)

    # Fix missing commas in lists and dictionaries
    content = re.sub(r'("[^"]*"|\'[^\']*\'|\d+\.?\d*)\s*\n\s*("[^"]*"|\'[^\']*\'|\d+\.?\d*)', r"\1,\2", content)

    return content


def fix_file_syntax(file_path):
    """Fix syntax issues in a specific file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Apply fixes in order
        content = fix_docstring_quotes(content)
        content = fix_common_patterns(content)

        # Fix line-by-line issues
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            # Fix incomplete with statements
            if line.strip().startswith("with open(") and ":" not in line:
                line = line.rstrip() + ":"

            # Fix json.dump indentation
            if "json.dump(" in line and not line.strip().startswith("json.dump"):
                # Add proper indentation if needed
                line = "    " + line.strip()

            fixed_lines.append(line)

        content = "\n".join(fixed_lines)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Final comprehensive syntax fix"""
    error_files = [
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
        "simple_validation.py",
        "task_queue.py",
        "trigger_learning.py",
        "validate_plugin.py",
        "validation_hooks.py",
    ]

    lib_dir = Path("lib")
    fixed_count = 0

    print("Applying final comprehensive syntax fixes...")
    for filename in error_files:
        file_path = lib_dir / filename
        if file_path.exists():
            if fix_file_syntax(file_path):
                print(f"Fixed: {filename}")
                fixed_count += 1
            else:
                print(f"No changes needed: {filename}")
        else:
            print(f"File not found: {filename}")

    print(f"\nFinal fixes applied to {fixed_count} files")
    return fixed_count


if __name__ == "__main__":
    main()
