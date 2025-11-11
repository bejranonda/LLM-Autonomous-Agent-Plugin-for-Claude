#!/usr/bin/env python3
"""
USER PLUGIN FIX SCRIPT

Run this script in your LLM-Autonomous-Agent-Plugin-for-Claude installation directory
to fix ALL consecutive empty lines that cause cache_control errors.

USAGE:
1. Navigate to your plugin directory:
   cd ~/.claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude/

2. Run this script:
   python3 USER_FIX_SCRIPT.py

This will fix all 41+ files with consecutive empty lines and resolve the cache_control error.
"""

import os
import re

def fix_consecutive_empty_lines(filepath):
    """Fix consecutive empty lines in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count consecutive empty lines before fix
        original_consecutive = len(re.findall(r'\n\s*\n\s*\n+', content))

        # Replace multiple consecutive empty lines with single empty line
        # This preserves single empty lines (needed for readability)
        # but removes consecutive empty lines (that cause empty text blocks)
        fixed_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)

        # Count consecutive empty lines after fix
        fixed_consecutive = len(re.findall(r'\n\s*\n\s*\n+', fixed_content))

        if original_consecutive > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return filepath, original_consecutive, fixed_consecutive
        else:
            return filepath, 0, 0

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return filepath, -1, -1

def main():
    print("=" * 60)
    print("FIXING CONSECUTIVE EMPTY LINES IN YOUR PLUGIN")
    print("=" * 60)
    print("This will fix the cache_control cannot be set for empty text blocks error")
    print()

    total_files_fixed = 0
    total_consecutive_removed = 0

    # Get current directory
    current_dir = os.getcwd()
    print(f"Working in: {current_dir}")
    print()

    # Process ALL markdown files in the plugin
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                filepath, removed, remaining = fix_consecutive_empty_lines(filepath)

                if removed > 0:
                    print(f"✅ FIXED: {filepath}")
                    print(f"   Removed {removed} consecutive empty line instances")
                    total_files_fixed += 1
                    total_consecutive_removed += removed
                elif removed == 0:
                    print(f"✅ OK: {filepath} (no consecutive empty lines)")
                else:
                    print(f"❌ ERROR: {filepath}")

    print("\n" + "=" * 60)
    print("FIX SUMMARY:")
    print(f"Files fixed: {total_files_fixed}")
    print(f"Total consecutive empty line instances removed: {total_consecutive_removed}")

    if total_files_fixed > 0:
        print("\n🎉 SUCCESS: All consecutive empty lines removed!")
        print("\nNOW TEST YOUR PLUGIN:")
        print("1. Restart Claude Code")
        print("2. Run: /learn:init")
        print("3. Should work without cache_control errors!")
    else:
        print("\n✅ No consecutive empty lines found.")

if __name__ == "__main__":
    main()