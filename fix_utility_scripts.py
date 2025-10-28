#!/usr/bin/env python3
"""
Systematically fix utility script syntax errors
"""

import re
from pathlib import Path

def fix_common_syntax_issues(content):
    """Fix common syntax issues found in utility scripts"""
    original_content = content

    # Fix 1: Missing quotes around string values in dictionaries
    patterns = [
        # Fix missing quotes around dictionary keys
        (r'(\s+)(version|project_name|project_type|team_size|development_stage|task_complexity|language|framework|module_type|approach_taken|recorded_by|integration_version|summary):\s*([^,\n}]+)',
         r'\1"\2": \3'),

        # Fix string values without quotes
        (r'(\s+)"([^"]+)":\s*([a-zA-Z][a-zA-Z0-9_\-\s]*)', r'\1"\2": "\3"'),

        # Fix incomplete function calls
        (r'time\.time\}', r'time.time()'),
        (r'datetime\.now\(timezone\.utc\)\.isoformat\(\}', r'datetime.now(timezone.utc).isoformat()'),

        # Fix f-string issues
        (r'f"ERROR ([^:]+):', r'f"ERROR \1:"'),
        (r'print\(f"ERROR ([^}]+)\}', r'print(f"ERROR \1}")'),

        # Fix missing commas in dictionaries
        (r'(".*":\s*[^,}\n]*\n)(\s*"[^"]+":)', r'\1,\2'),

        # Fix unmatched parentheses common patterns
        (r'\)\s*\)', r')'),
        (r'\}\s*\}', r'}'),

        # Fix incomplete json.dump calls
        (r'json\.dump\(data, f, indent=2\)\s*$', r'json.dump(data, f, indent=2)'),

        # Fix common string literal issues
        (r'task_completed_with_recording""', r'"task_completed_with_recording"'),
        (r'\[summary""\]', r'["summary"]'),

        # Fix conditional statements
        (r'if: trigger_type in', r'if trigger_type in'),

        # Fix incomplete lines ending with operators
        (r'(\s+)\+\s*$', r''),
        (r'(\s*),\s*$', r''),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # Fix line-by-line issues
    lines = content.split('\n')
    fixed_lines = []

    for i, line in enumerate(lines):
        # Fix incomplete print statements
        if 'except Exception as e: print(fERROR' in line:
            line = line.replace('except Exception as e: print(fERROR', 'except Exception as e:\n                print(f"ERROR')
            if not line.rstrip().endswith('")'):
                line = line.rstrip() + '")'

        # Fix incomplete with statements
        if line.strip().startswith('with open(') and ':' not in line:
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line.strip().startswith('json.dump'):
                    line = line.rstrip() + ':'
                    lines[i + 1] = '    ' + next_line

        # Fix indentation issues with json.dump
        if 'json.dump(data, f, indent=2)' in line and not line.strip().startswith('json.dump'):
            if 'with open(' in '\n'.join(lines[max(0, i-5):i]):
                line = '                ' + line.strip()

        fixed_lines.append(line)

    content = '\n'.join(fixed_lines)
    return content != original_content, content

def fix_specific_file(file_path):
    """Fix syntax issues in a specific file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changed, new_content = fix_common_syntax_issues(content)

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all utility scripts with syntax errors"""
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
        "validation_hooks.py"
    ]

    lib_dir = Path("lib")
    fixed_count = 0

    print("Fixing utility scripts...")
    for filename in error_files:
        file_path = lib_dir / filename
        if file_path.exists():
            if fix_specific_file(file_path):
                print(f"Fixed: {filename}")
                fixed_count += 1
            else:
                print(f"No changes needed: {filename}")
        else:
            print(f"File not found: {filename}")

    print(f"\nFixed {fixed_count} utility scripts")
    return fixed_count

if __name__ == "__main__":
    main()