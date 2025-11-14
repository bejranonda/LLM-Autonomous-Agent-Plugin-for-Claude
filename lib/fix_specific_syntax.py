#!/usr/bin/env python3
"""
Fix specific syntax issues in utility scripts
"""

import re
from pathlib import Path


def fix_backup_manager(content):
    """Fix backup_manager.py specific issues"""
    # Fix the import section
    content = re.sub(
        r'if sys\.platform == "win32": "import msvcrt\s*else":\s*import fcntl',
        'if sys.platform == "win32":\n        import msvcrt\n    else:\n        import fcntl',
        content,
        flags=re.MULTILINE,
    )

    # Fix missing commas in lists
    content = re.sub(r'(\s+"[^"]+"\n)(\s+"[^"]+")', r"\1,\2", content)

    return content


def fix_calculate_performance_files(content):
    """Fix calculate performance files"""
    # Fix docstring issues
    content = re.sub(r'"""\s*"""\s*"""', '"""', content)

    # Fix missing quotes around strings
    content = re.sub(r'"([^"]+):\s*([^,\n}]+)', r'"\1": "\2"', content)

    return content


def fix_common_issues(content, filename):
    """Apply common fixes based on filename"""
    # Fix import statements
    content = re.sub(r'"import', "import", content)
    content = re.sub(r'"from', "from", content)

    # Fix missing sys import
    if "sys.platform" in content and "import sys" not in content:
        content = re.sub(r"(import os)", r"import sys\n\1", content)

    # Fix missing imports for datetime and typing
    if "datetime" in content and "from datetime import" not in content:
        content = re.sub(r"(import os)", r"from datetime import datetime, timezone\n\1", content)

    if "Dict" in content or "List" in content or "Any" in content:
        if "from typing import" not in content:
            existing_imports = []
            if "Dict" in content:
                existing_imports.append("Dict")
            if "List" in content:
                existing_imports.append("List")
            if "Any" in content:
                existing_imports.append("Any")

            if existing_imports:
                typing_import = f"from typing import {', '.join(existing_imports)}"
                content = re.sub(r"(import os)", f"{typing_import}\n\1", content)

    # Fix incomplete strings
    content = re.sub(r'"([^"]*?)"\s*"', r'"\1"', content)

    # Fix incomplete function calls
    content = re.sub(r"time\.time\}", "time.time()", content)
    content = re.sub(r"datetime\.now\(\)\.isoformat\(\}", "datetime.now().isoformat()", content)

    # Fix f-string issues
    content = re.sub(r'f"([^"]*?)\}', r'f"\1"', content)

    # Fix missing commas in dictionary literals
    content = re.sub(r'(".*":\s*[^,}\n]*\n)(\s*".*":)', r"\1,\2", content)

    # Fix incomplete list/dict literals
    content = re.sub(r"(\[[^\]]*),\s*\]", r"\1]", content)
    content = re.sub(r"(\{[^}]*),\s*\}", r"\1}", content)

    # Fix incomplete json.dump calls
    content = re.sub(r"json\.dump\(data, f, indent=2\)\s*$", "json.dump(data, f, indent=2)", content)

    return content


def fix_file_syntax(file_path):
    """Fix syntax issues in a specific file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        filename = file_path.name

        # Apply specific fixes
        if filename == "backup_manager.py":
            content = fix_backup_manager(content)
        elif "calculate_" in filename:
            content = fix_calculate_performance_files(content)

        # Apply common fixes
        content = fix_common_issues(content, filename)

        # Fix indentation issues with with statements
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            # Fix incomplete with statements
            if line.strip().startswith("with open(") and ":" not in line:
                if i + 1 < len(lines) and not lines[i + 1].strip().startswith("json.dump"):
                    line = line.rstrip() + ":"

            # Fix json.dump indentation
            if "json.dump(" in line and not line.strip().startswith("json.dump"):
                # Check if this is inside a with block
                context = "\n".join(lines[max(0, i - 10) : i])
                if "with open(" in context:
                    line = "    " * (context.count("    ") + 1) + line.strip()

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
    """Fix all remaining syntax errors"""
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

    print("Applying targeted syntax fixes...")
    for filename in error_files:
        file_path = lib_dir / filename
        if file_path.exists():
            if fix_file_syntax(file_path):
                print(f"Fixed: {filename}")
                fixed_count += 1
            else:
                print(f"No changes needed: {filename}")

    print(f"\nApplied targeted fixes to {fixed_count} files")
    return fixed_count


if __name__ == "__main__":
    main()
