#!/usr/bin/env python3
"""
Detect and fix emoji usage in Python scripts for Windows compatibility

This script scans Python files for problematic emojis and provides ASCII alternatives.
"""

import os
import re
import sys
import argparse
from pathlib import Path

# List of problematic emojis and their ASCII alternatives
EMOJI_REPLACEMENTS = {
    '✅': '[OK]',
    '❌': '[ERROR]',
    '⚠️': '[WARN]',
    '🚀': '[INFO]',
    '💡': '[TIP]',
    '🔧': '[FIX]',
    '📊': '[DATA]',
    '🔍': '[SCAN]',
    '🎯': '[TARGET]',
    '📈': '[UP]',
    '📉': '[DOWN]',
    '📝': '[NOTE]',
    '💻': '[SYSTEM]',
    '🌟': '[STAR]',
    '⭐': '[STAR]',
    '🔥': '[HOT]',
    '💎': '[VALUABLE]',
    '🎉': '[CELEBRATE]',
    '🎵': '[AUDIO]',
    '🎮': '[GAME]',
    '🏆': '[WIN]',
    '🎨': '[DESIGN]',
    '🚩': '[FLAG]',
    '🌈': '[COLORFUL]',
    '🌸': '[FLOWER]',
    '🦄': '[SPECIAL]',
    '🐉': '[DRAGON]',
    '🔮': '[MAGIC]',
    '💰': '[MONEY]',
    '🎪': '[CIRCUS]',
    '🎭': '[DRAMA]',
    '🎪': '[EVENT]',
    '🎊': '[PARTY]',
    '🎁': '[GIFT]',
    '🌍': '[WORLD]',
    '🌐': '[GLOBE]',
    '🔗': '[LINK]',
    '📋': '[LIST]',
    '📁': '[FOLDER]',
    '📂': '[FOLDERS]',
    '🗂️': '[DRAWER]',
    '📄': '[FILE]',
    '📃': '[DOCUMENT]',
    '📑': '[DOCUMENTS]',
    '🗒️': '[NOTES]',
    '📜': '[SCROLL]',
    '📋': '[CLIPBOARD]',
    '📌': '[PIN]',
    '📍': '[LOCATION]',
    '📎': '[PAPERCLIP]',
    '🖇️': '[PAPERCLIPS]',
    '📏': '[RULER]',
    '📐': '[TRIANGLE]',
    '✏️': '[PENCIL]',
    '📝': '[WRITING]',
    '✒️': '[PEN]',
    '🖊️': '[MARKER]',
    '🖋️': '[PEN]',
    '📚': '[BOOKS]',
    '📖': '[BOOK]',
    '🔖': '[BOOKMARK]',
    '📛': '[NAMEPLATE]',
    '🔬': '[SCIENCE]',
    '🔭': '[TELESCOPE]',
    '📡': '[SATELLITE]',
    '🔧': '[TOOLS]',
    '🔨': '[HAMMER]',
    '⚙️': '[GEAR]',
    '🛠️': '[WRENCH]',
    '🔩': '[BOLT]',
    '⚡': '[ELECTRICITY]',
    '💡': '[IDEA]',
    '🕯️': '[CANDLE]',
    '💥': '[EXPLOSION]',
    '🔥': '[FIRE]',
    '🌫️': '[SMOKE]',
    '💨': '[WIND]',
    '🧊': '[ICE]',
    '❄️': '[SNOW]',
    '☄️': '[COMET]',
    '☀️': '[SUN]',
    '🌤️': '[SUNNY]',
    '⛅': '[CLOUDY]',
    '☁️': '[CLOUD]',
    '🌧️': '[RAIN]',
    '⛈️': '[STORM]',
    '🌩️': '[LIGHTNING]',
    '❄️': '[SNOW]'
}

def detect_emojis(file_path):
    """Detect emoji usage in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()

        emoji_issues = []
        line_num = 0

        for line in lines:
            line_num += 1
            line_content = line
            original_line = line

            for emoji, replacement in EMOJI_REPLACEMENTS.items():
                if emoji in line_content:
                    emoji_issues.append({
                        'line': line_num,
                        'original': original_line.strip(),
                        'emoji': emoji,
                        'replacement': replacement,
                        'suggested': line_content.replace(emoji, replacement).strip()
                    })

        return emoji_issues

    except UnicodeDecodeError:
        return [{'error': f'UnicodeDecodeError reading {file_path}'}]
    except Exception as e:
        return [{'error': f'Error reading {file_path}: {str(e)}'}]

def scan_directory(directory='.'):
    """Scan directory for Python files with emojis."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        # Skip .git and __pycache__ directories
        if '.git' in root or '__pycache__' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    return python_files

def fix_emojis(file_path, dry_run=True):
    """Fix emoji usage in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = []

        for emoji, replacement in EMOJI_REPLACEMENTS.items():
            if emoji in content:
                content = content.replace(emoji, replacement)
                changes_made.append((emoji, replacement))

        if changes_made and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return changes_made, original_content != content, None

    except Exception as e:
        return [], False, str(e)

def main():
    parser = argparse.ArgumentParser(description="Detect and fix emoji usage in Python scripts")
    parser.add_argument('--directory', default='.', help='Directory to scan (default: current)')
    parser.add_argument('--fix', action='store_true', help='Fix emojis automatically')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Show changes without applying (default)')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    args = parser.parse_args()

    print("Emoji Detection and Fix Tool")
    print("=" * 50)
    print(f"Scanning directory: {args.directory}")
    print()

    # Find all Python files
    python_files = scan_directory(args.directory)
    print(f"Found {len(python_files)} Python files")

    files_with_issues = 0
    total_issues = 0

    for file_path in python_files:
        issues = detect_emojis(file_path)

        if 'error' in [issue.get('error') for issue in issues]:
            print(f"Error processing {file_path}: {issues[0]['error']}")
            continue

        if issues:
            files_with_issues += 1
            total_issues += len(issues)

            rel_path = os.path.relpath(file_path, args.directory)
            print(f"\n[FILE] {rel_path}")
            print(f"   Issues found: {len(issues)}")

            for issue in issues:
                emoji_code = f"U+{ord(issue['emoji'][0]):04X}"
                if args.verbose:
                    print(f"   Line {issue['line']}: {emoji_code} -> {issue['replacement']}")
                    print(f"     Original: {issue['original']}")
                    print(f"     Suggested: {issue['suggested']}")
                else:
                    print(f"   Line {issue['line']}: {emoji_code} -> {issue['replacement']}")

    print("\n" + "=" * 50)
    print(f"SUMMARY:")
    print(f"Files scanned: {len(python_files)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Total emoji issues: {total_issues}")

    if args.fix and files_with_issues > 0:
        print(f"\n[FIX] Fixing emojis in {files_with_issues} files...")

        files_fixed = 0
        emojis_fixed = 0

        for file_path in python_files:
            changes_made, content_changed, error = fix_emojis(file_path, dry_run=args.dry_run)

            if error:
                print(f"Error fixing {file_path}: {error}")
                continue

            if content_changed:
                files_fixed += 1
                emojis_fixed += len(changes_made)

                if args.verbose:
                    rel_path = os.path.relpath(file_path, args.directory)
                    print(f"   Fixed {rel_path}: {len(changes_made)} emojis")

        if not args.dry_run:
            print(f"\n[DONE] Fixed {emojis_fixed} emojis in {files_fixed} files")
        else:
            print(f"\n[INFO] Would fix {emojis_fixed} emojis in {files_fixed} files")
            print("   Use --fix --no-dry-run to apply changes")

    elif files_with_issues == 0:
        print("\n[DONE] No emoji issues found!")
    else:
        print(f"\n[INFO] Run with --fix to automatically fix these issues")

    return 0

if __name__ == "__main__":
    sys.exit(main())