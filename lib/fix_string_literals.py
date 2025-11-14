#!/usr/bin/env python3
"""
Fix missing quotes around string literals in Python files
"""

import re
from pathlib import Path


def fix_string_literals(file_path):
    """Fix missing quotes around string literals"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Fix specific string literal patterns
        patterns = [
            # Fix: "project_name": Autonomous Agent Plugin -> "project_name": "Autonomous Agent Plugin"
            (r'"project_name":\s*([A-Za-z][A-Za-z\s]+)', r'"project_name": "\1"'),
            (r'"project_type":\s*([a-z\-]+)', r'"project_type": "\1"'),
            (r'"team_size":\s*([a-z]+)', r'"team_size": "\1"'),
            (r'"development_stage":\s*([a-z]+)', r'"development_stage": "\1"'),
            (r'"task_complexity":\s*([a-z]+)', r'"task_complexity": "\1"'),
            (r'"language":\s*([a-z]+)', r'"language": "\1"'),
            (r'"framework":\s*([a-z\-]+)', r'"framework": "\1"'),
            (r'"module_type":\s*([a-z]+)', r'"module_type": "\1"'),
            (r'"approach_taken":\s*([A-Za-z][^,}]+)', r'"approach_taken": "\1"'),
            (r'"recorded_by":\s*([a-z_]+)', r'"recorded_by": "\1"'),
            (r'"integration_version":\s*([0-9\.+]+)', r'"integration_version": "\1"'),
            # Fix f-string patterns
            (r"fERROR storing ([^:]+):", r'f"ERROR storing \1:"'),
            (r"print\(fERROR ([^}]+)\}", r'print(f"ERROR \1}")'),
            # Fix other string literals
            (r'task_completed_with_recording""', r'"task_completed_with_recording"'),
            (r'\[summary""\]', r'["summary"]'),
            (r"if: trigger_type in", r"if trigger_type in"),
            # Fix incomplete lines
            (r"(\s+)json\.dump\(data, f, indent=2\)\s*$", r"\1json.dump(data, f, indent=2)"),
        ]

        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

        # Fix line-by-line issues
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            # Fix incomplete dictionary definitions
            if "self.current_task = {" in line and i > 0:
                prev_line = lines[i - 1] if i > 0 else ""
                if "self.task_start_time = time.time()" in prev_line:
                    # Complete the previous line first
                    fixed_lines[-1] = fixed_lines[-1].rstrip() + "}"
                    line = line.strip()

            # Fix incomplete performance metrics section
            if '"efficiency": min(' in line and i > 1:
                # Look for the incomplete section spanning multiple lines
                if i + 2 < len(lines):
                    combined_lines = line + "\n" + lines[i + 1] + "\n" + lines[i + 2]
                    if "100 - (duration / 60)" in combined_lines and "Simple efficiency calc" in combined_lines:
                        # Fix the incomplete function call
                        fixed_line = (
                            '                    "efficiency": min(100, 100 - (duration / 60)),  # Simple efficiency calc'
                        )
                        fixed_lines.append(fixed_line)
                        # Skip the next two broken lines
                        continue

            # Fix print statement with missing quotes
            if "except Exception as e: print(fERROR" in line:
                line = line.replace(
                    "except Exception as e: print(fERROR", 'except Exception as e:\n                print(f"ERROR'
                )
                if not line.rstrip().endswith('")'):
                    line = line.rstrip() + '")'

            # Fix incomplete json.dump calls
            if "json.dump(data, f, indent=2)" in line and not line.strip().endswith(")"):
                line = line.rstrip() + ")"

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
    """Fix string literals in auto_learning_trigger.py"""
    file_path = Path("lib/auto_learning_trigger.py")

    if file_path.exists():
        if fix_string_literals(file_path):
            print("Fixed string literals in auto_learning_trigger.py")
        else:
            print("No changes needed for auto_learning_trigger.py")
    else:
        print("File not found: lib/auto_learning_trigger.py")


if __name__ == "__main__":
    main()
