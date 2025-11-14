#!/usr/bin/env python3
# FIX ALL CONSECUTIVE EMPTY LINES - IMMEDIATE SOLUTION

#     This script removes ALL consecutive empty lines from markdown files
# to fix the cache_control cannot be set for empty text blocks error.
# import os
# import re
# def fix_consecutive_empty_lines(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Count consecutive empty lines before fix
        original_consecutive = len(re.findall(r"\n\s*\n\s*\n+", content))

        # Replace multiple consecutive empty lines with single empty line
        # This preserves single empty lines (needed for readability)
        # but removes consecutive empty lines (that cause empty text blocks)
        fixed_content = re.sub(r"\n\s*\n\s*\n+", "\n\n", content)

        # Count consecutive empty lines after fix
        fixed_consecutive = len(re.findall(r"\n\s*\n\s*\n+", fixed_content))

        if original_consecutive > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            return filepath, original_consecutive, fixed_consecutive
        else:
            return filepath, 0, 0

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return filepath, -1, -1


def main():
    """Main."""
    print("[OK] FIXING ALL CONSECUTIVE EMPTY LINES")
    print("=" * 50)

    total_files_fixed = 0
    total_consecutive_removed = 0

"""
    # Process ALL markdown files
    for root, dirs, files in os.walk("."):
        # Skip .git and .claude directories
        if ".git" in root or ".claude" in root or "node_modules" in root:
            continue

        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                filepath, removed, remaining = fix_consecutive_empty_lines(filepath)

                if removed > 0:
                    print(f"[OK] FIXED: {filepath}")
                    print(f"   Removed {removed} consecutive empty line instances")
                    total_files_fixed += 1
                    total_consecutive_removed += removed
                elif removed == 0:
                    print(f"[OK] OK: {filepath} (no consecutive empty lines)")
                else:
                    print(f"[ERROR] ERROR: {filepath}")

    print("\n" + "=" * 50)
    print("[SUMMARY]:")
    print(f"Files fixed: {total_files_fixed}")
    print(f"Total consecutive empty line instances removed: {total_consecutive_removed}")

    if total_files_fixed > 0:
        print("\n[OK] SUCCESS: All consecutive empty lines removed!")
        print("Try running /learn:init now - it should work perfectly!")
    else:
        print("\n[OK] No consecutive empty lines found.")


if __name__ == "__main__":
    main()
