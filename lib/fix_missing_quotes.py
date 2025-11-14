#!/usr/bin/env python3
"""
Fix missing quotes around dictionary keys in Python files
"""

import re
from pathlib import Path


def fix_missing_quotes(file_path):
    """Fix missing quotes around dictionary keys"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Fix patterns for missing quotes around dictionary keys
        patterns = [
            # Fix: version: 2.0.0 -> "version": 2.0.0
            (
                r"(\s+)(version|project_name|project_type|team_size|development_stage|task_complexity|language|framework|module_type|approach_taken|recorded_by|integration_version|summary):\s*([^,\n}]+)",
                r'\1"\2": \3',
            ),
            # Fix: project_type: ai-plugin -> "project_type": "ai-plugin"
            (
                r"(\s+)(project_name|project_type|team_size|development_stage|task_complexity|language|framework|module_type|approach_taken|recorded_by|integration_version):\s*([a-zA-Z][a-zA-Z0-9_\-\s]*)",
                r'\1"\2": "\3"',
            ),
            # Fix specific known keys
            (r"(\s+)(version):(\s*)(\d+\.\d+\.\d+)", r'\1"\2":\3\4'),
            (r"(\s+)(project_name):(\s*)([a-zA-Z\s]+)", r'\1"\2":\3"\4"'),
            (r"(\s+)(project_type):(\s*)([a-zA-Z\-]+)", r'\1"\2":\3"\4"'),
            (r"(\s+)(team_size):(\s*)([a-z]+)", r'\1"\2":\3"\4"'),
            (r"(\s+)(development_stage):(\s*)([a-z]+)", r'\1"\2":\3"\4"'),
            (r"(\s+)(task_complexity):(\s*)([a-z]+)", r'\1"\2":\3"\4"'),
            (r"(\s+)(language):(\s*)([a-z]+)", r'\1"\2":\3"\4"'),
            (r"(\s+)(framework):(\s*)([a-z\-]+)", r'\1"\2":\3"\4"'),
            (r"(\s+)(module_type):(\s*)([a-z]+)", r'\1"\2":\3"\4"'),
            (r"(\s+)(approach_taken):(\s*)([^,}]+)", r'\1"\2": \3'),
            (r"(\s+)(recorded_by):(\s*)([^,}]+)", r'\1"\2": \3'),
            (r"(\s+)(integration_version):(\s*)([^,}]+)", r'\1"\2": \3'),
            # Fix missing quotes in string literals
            (r"fERROR storing ([^:]+):", r'f"ERROR storing \1:'),
            (r"if: trigger_type in \[([^\]]+)\]", r"if trigger_type in [\1]"),
            (r'task_completed_with_recording""', r'"task_completed_with_recording"'),
            (r'\[summary""\]', r'["summary"]'),
            (r"json\.dump\(data, f, indent=2\)\s*$", r"json.dump(data, f, indent=2)"),
            # Fix incomplete lines
            (r"(\s+)json\.dump\(data, f, indent=2\)\s*$", r"\1json.dump(data, f, indent=2)"),
            (r"except Exception as e: print\(fERROR ([^}]+)\}$", r'except Exception as e:\n\1print(f"ERROR \1")'),
        ]

        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

        # Fix specific line-by-line issues
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Fix missing closing brackets
            if "self.current_task = {" in line and not line.rstrip().endswith("}"):
                line = line.rstrip() + "}"

            # Fix incomplete dictionary entries
            if '"duration_seconds": round(duration),' in line:
                line = line.replace('"duration_seconds": round(duration),', '"duration_seconds": round(duration)')

            # Fix print statements
            if "print(fERROR" in line:
                line = line.replace("print(fERROR", 'print(f"ERROR')
                if not line.rstrip().endswith('")'):
                    line = line.rstrip() + '")'

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
    """Fix missing quotes in all Python files in lib directory"""
    lib_dir = Path("lib")
    fixed_count = 0

    # Focus on the most critical files first
    critical_files = [
        "auto_learning_trigger.py",
        "assessment_storage.py",
        "task_queue.py",
        "backup_manager.py",
        "calculate_debugging_performance.py",
        "calculate_real_performance.py",
    ]

    for filename in critical_files:
        file_path = lib_dir / filename
        if file_path.exists():
            if fix_missing_quotes(file_path):
                print(f"Fixed missing quotes: {filename}")
                fixed_count += 1
            else:
                print(f"No changes needed: {filename}")

    print(f"\nFixed {fixed_count} critical files")


if __name__ == "__main__":
    main()
