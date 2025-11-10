#!/usr/bin/env python3
"""
Simple Unicode Fix Script

Quick fix for Unicode contamination in critical directories.
"""

import os
from pathlib import Path

# Basic Unicode to ASCII mapping
UNICODE_TO_ASCII = {
    '═': '=', '║': '|', '╔': '+', '╗': '+', '╚': '+', '╝': '+',
    '┌': '+', '┐': '+', '└': '+', '┘': '+', '│': '|', '─': '-',
    '├': '+', '┤': '+', '┬': '+', '┴': '+', '┼': '+',
    '↑': '^', '↓': 'v', '→': '->', '←': '<-',
    '✓': '[PASS]', '✗': '[FAIL]', '⚠': '[WARN]', '★': '[STAR]',
    '•': '*', '○': '[ ]', '●': '[X]', '□': '[ ]', '■': '[X]',
}

def fix_directory(directory):
    """Fix Unicode characters in a directory."""
    dir_path = Path(directory)
    if not dir_path.exists():
        return 0, 0

    fixed_files = 0
    total_unicode = 0

    for file_path in dir_path.rglob('*.md'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Count Unicode characters
            unicode_count = sum(content.count(char) for char in UNICODE_TO_ASCII.keys())
            if unicode_count > 0:
                # Replace Unicode characters
                fixed_content = content
                for unicode_char, ascii_char in UNICODE_TO_ASCII.items():
                    fixed_content = fixed_content.replace(unicode_char, ascii_char)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)

                fixed_files += 1
                total_unicode += unicode_count
                print(f'[OK] Fixed: {file_path} (removed {unicode_count} Unicode chars)')

        except Exception as e:
            print(f'Error fixing {file_path}: {e}')

    return fixed_files, total_unicode

def main():
    print('[OK] Simple Unicode Fix - Cleaning critical directories...')

    critical_dirs = ['.claude/reports/', '.claude-patterns/']
    total_fixed = 0
    total_unicode = 0

    for directory in critical_dirs:
        print(f'\nChecking {directory}:')
        fixed, unicode_count = fix_directory(directory)
        total_fixed += fixed
        total_unicode += unicode_count

    print(f'\n=== SUMMARY ===')
    print(f'Files fixed: {total_fixed}')
    print(f'Unicode characters removed: {total_unicode}')

    if total_unicode > 0:
        print(f'[OK] Unicode contamination eliminated!')
    else:
        print(f'[OK] No Unicode contamination found')

if __name__ == '__main__':
    main()