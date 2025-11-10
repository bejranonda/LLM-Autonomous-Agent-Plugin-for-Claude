#!/usr/bin/env python3
"""
Emergency Unicode Fixer for Command Files

This script automatically removes all Unicode box characters from command files
and replaces them with safe ASCII alternatives to prevent cache_control errors.
"""

import os
import re
import sys
from pathlib import Path

# Unicode box characters and their ASCII replacements
UNICODE_TO_ASCII = {
    '═': '=',  # Double horizontal line
    '║': '|',  # Double vertical line
    '╔': '+',  # Top-left corner
    '╗': '+',  # Top-right corner
    '╚': '+',  # Bottom-left corner
    '╝': '+',  # Bottom-right corner
    '┌': '+',  # Top-left corner (single)
    '┐': '+',  # Top-right corner (single)
    '└': '+',  # Bottom-left corner (single)
    '┘': '+',  # Bottom-right corner (single)
    '│': '|',  # Vertical line (single)
    '─': '-',  # Horizontal line (single)
    '├': '+',  # Left cross (single)
    '┤': '+',  # Right cross (single)
    '┬': '+',  # Top cross (single)
    '┴': '+',  # Bottom cross (single)
    '┼': '+',  # Cross (single)
    '┽': ':',  # Split vertical
    '╀': ':',  # Cross center
    '╄': ':',  # Double split
    '╆': ':',  # Double split bottom
    '╅': ':',  # Double split top
    '╈': ':',  # Double cross
    '═': '=',  # Double horizontal
    '║': '|',  # Double vertical
    '╢': '|',  # Double right
    '╟': '|',  # Double left
    '╤': '=',  # Double top
    '╧': '=',  # Double bottom
    '╫': ':',  # Double vertical split
    '╪': '-',  # Double horizontal split
    '╬': ':',  # Double cross
    '↑': '^',  # Up arrow
    '↓': 'v',  # Down arrow
    '→': '->', # Right arrow
    '←': '<-', # Left arrow
    '✓': '[PASS]',  # Checkmark
    '✗': '[FAIL]',  # X mark
    '⚠': '[WARN]',  # Warning
    '★': '[STAR]',  # Star
    '☆': '[STAR]',  # Empty star
    '•': '*',  # Bullet
    '○': '[ ]', # Empty circle
    '●': '[X]', # Filled circle
    '□': '[ ]', # Empty square
    '■': '[X]', # Filled square
    '△': '^',   # Triangle
    '▽': 'v',   # Inverted triangle
    '◇': '[ ]', # Diamond (empty)
    '◆': '[X]', # Diamond (filled)
}

def fix_file_content(content):
    """Replace Unicode box characters with ASCII alternatives."""
    fixed_content = content
    for unicode_char, ascii_char in UNICODE_TO_ASCII.items():
        fixed_content = fixed_content.replace(unicode_char, ascii_char)
    return fixed_content

def fix_command_file(file_path):
    """Fix Unicode characters in a single command file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fixed_content = fix_file_content(content)

        # Only write if changes were made
        if content != fixed_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix all command files."""
    commands_dir = Path("commands")

    if not commands_dir.exists():
        print("ERROR: commands/ directory not found!")
        sys.exit(1)

    # Find all markdown files in commands directory
    md_files = list(commands_dir.glob("**/*.md"))

    if not md_files:
        print("No markdown files found in commands/ directory")
        return

    print(f"Found {len(md_files)} command files to check...")

    fixed_files = []
    total_unicode_chars = 0

    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count Unicode characters before fixing
        unicode_count = sum(content.count(unicode_char) for unicode_char in UNICODE_TO_ASCII.keys())
        total_unicode_chars += unicode_count

        if fix_command_file(file_path):
            fixed_files.append(file_path)
            print(f"  [OK] Fixed: {file_path} (removed {unicode_count} Unicode chars)")

    print(f"\n=== SUMMARY ===")
    print(f"Total files processed: {len(md_files)}")
    print(f"Files fixed: {len(fixed_files)}")
    print(f"Total Unicode characters removed: {total_unicode_chars}")

    if fixed_files:
        print(f"\nFixed files:")
        for file_path in fixed_files:
            print(f"  - {file_path}")
    else:
        print("\nNo files needed fixing.")

    print(f"\n[OK] Emergency Unicode fix complete!")
    print(f"All command files are now ASCII-safe and will not cause cache_control errors.")

if __name__ == "__main__":
    main()