#!/usr/bin/env python3
# Fix hardcoded Python script paths in documentation.

# Replaces all instances of 'python lib/' with 'python <plugin_path>/lib/'
# in markdown files to ensure the plugin works when installed from marketplace.
import os
import sys
from pathlib import Path
import re


def fix_file(file_path: Path) -> int:
    """Fix hardcoded paths in a single file."""
    changes_made = 0

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Pattern to match python lib/ (but not inside code blocks that explain it)
        # We'll replace all instances as documentation should show the correct usage
        original_content = content

        # Replace python lib/ with python <plugin_path>/lib/
        content = re.sub(r"python lib/", "python <plugin_path>/lib/", content)

        # Count changes
        if content != original_content:
            changes_made = len(re.findall(r"python <plugin_path>/lib/", content))

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"  [OK] Fixed {changes_made} reference(s) in {file_path.name}")

        return changes_made

    except Exception as e:
        print(f"  [ERR] Error processing {file_path}: {e}")
        return 0


def main():
    """Fix hardcoded paths in all markdown files."""
    print("Fixing hardcoded Python script paths in documentation...")
    print("=" * 60)

    # Find all markdown files
    current_dir = Path(__file__).parent.parent
    md_files = list(current_dir.rglob("*.md"))

    # Skip certain directories
    skip_dirs = {".git", "__pycache__", "node_modules", ".claude"}
    md_files = [f for f in md_files if not any(skip_dir in f.parts for skip_dir in skip_dirs)]

    total_changes = 0
    files_changed = 0

    for md_file in sorted(md_files):
        changes = fix_file(md_file)
        if changes > 0:
            total_changes += changes
            files_changed += 1

    print("=" * 60)
    print(f"Summary:")
    print(f"  Files modified: {files_changed}")
    print(f"  Total references fixed: {total_changes}")

    if total_changes > 0:
        print("\nAll 'python lib/' references have been replaced with 'python <plugin_path>/lib/'")
        print("This ensures the plugin works correctly when installed from marketplace.")


if __name__ == "__main__":
    main()
