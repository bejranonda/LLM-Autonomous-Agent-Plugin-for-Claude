#!/usr/bin/env python3
"""
Unicode Contamination Prevention System

This script prevents Unicode contamination from getting into Claude's message context
by automatically sanitizing generated content in critical directories.

The system monitors and cleans:
- .claude/reports/ - Generated reports that agents load
- .claude-patterns/ - Pattern data that agents use
- Other critical directories that affect Claude context

Usage:
    python lib/unicode_contamination_prevention.py --check
    python lib/unicode_contamination_prevention.py --fix
    python lib/unicode_contamination_prevention.py --monitor
"""

import os
import re
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

# Comprehensive Unicode to ASCII mapping
UNICODE_TO_ASCII = {
    # Box drawing characters
    '═': '=', '║': '|', '╔': '+', '╗': '+', '╚': '+', '╝': '+',
    '┌': '+', '┐': '+', '└': '+', '┘': '+', '│': '|', '─': '-',
    '├': '+', '┤': '+', '┬': '+', '┴': '+', '┼': '+', '┽': ':',
    '╀': ':', '╄': ':', '╆': ':', '╈': ':', '╪': '-', '╫': ':',
    '╢': '|', '╟': '|', '╤': '=', '╧': '=',

    # Arrows and symbols
    '↑': '^', '↓': 'v', '→': '->', '←': '<-', '↔': '<->',
    '⇒': '=>', '⇐': '<=', '⇔': '<=>',

    # Checkmarks and status symbols
    '✓': '[PASS]', '✗': '[FAIL]', '✓': '[PASS]', '✕': '[FAIL]',
    '✔': '[PASS]', '✖': '[FAIL]', '✘': '[FAIL]',
    '⚠': '[WARN]', '⚡': '[EXEC]', '⭐': '[STAR]',

    # Stars and symbols
    '★': '[STAR]', '☆': '[STAR]', '☆': '[STAR]', '★': '[STAR]',

    # Bullets and shapes
    '•': '*', '○': '[ ]', '●': '[X]', '□': '[ ]', '■': '[X]',
    '△': '^', '▽': 'v', '◇': '[ ]', '◆': '[X]',

    # Mathematical symbols
    '±': '+/-', '×': 'x', '÷': '/', '≠': '!=', '≈': '~=',
    '≤': '<=', '≥': '>=', '∞': 'inf', '√': 'sqrt',

    # Currency
    '€': 'EUR', '£': 'GBP', '¥': 'JPY', '₹': 'INR',

    # Common Unicode that causes issues
    '"': '"', '"': '"', ''': "'", ''': "'", '…': '...',
    '–': '-', '—': '--', '‘': "'", ''': "'", '“': '"', '"': '"',

    # Degrees and symbols
    '°': 'deg', '℃': 'C', '℉': 'F',

    # Copyright and trademark
    '©': '(c)', '®': '(R)', '™': '(TM)',

    # Fractions
    '½': '1/2', '⅓': '1/3', '⅔': '2/3', '¼': '1/4', '¾': '3/4',
}

# Directories that affect Claude's context
CRITICAL_DIRECTORIES = [
    '.claude/reports/',
    '.claude-patterns/',
    '.claude-quality/',
    'docs/reports/generated/',
]

# File patterns to monitor
MONITOR_PATTERNS = [
    '*.md',
    '*.txt',
    '*.json',
    '*.log'
]

class UnicodeContaminationPrevention:
    """Prevents Unicode contamination in Claude's context."""

    def __init__(self):
        self.unicode_count = 0
        self.fixed_files = 0

    def check_directory(self, directory: str) -> Tuple[int, List[str]]:
        """Check a directory for Unicode characters."""
        dir_path = Path(directory)
        if not dir_path.exists():
            return 0, []

        unicode_files = []
        total_unicode = 0

        for pattern in MONITOR_PATTERNS:
            for file_path in dir_path.rglob(pattern):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Count Unicode characters
                    unicode_count = sum(content.count(char) for char in UNICODE_TO_ASCII.keys())
                    if unicode_count > 0:
                        total_unicode += unicode_count
                        unicode_files.append(str(file_path))

                except Exception as e:
                    print(f"Error checking {file_path}: {e}")

        return total_unicode, unicode_files

    def fix_directory(self, directory: str) -> Tuple[int, int]:
        """Fix Unicode characters in a directory."""
        dir_path = Path(directory)
        if not dir_path.exists():
            return 0, 0

        fixed_files = 0
        total_unicode = 0

        for pattern in MONITOR_PATTERNS:
            for file_path in dir_path.rglob(pattern):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Count Unicode characters before fixing
                    unicode_count = sum(content.count(char) for char in UNICODE_TO_ASCII.keys())
                    if unicode_count > 0:
                        # Replace Unicode characters
                        fixed_content = content
                        for unicode_char, ascii_char in UNICODE_TO_ASCII.items():
                            fixed_content = fixed_content.replace(unicode_char, ascii_char)

                        # Write back the fixed content
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(fixed_content)

                        fixed_files += 1
                        total_unicode += unicode_count
                        print(f"[OK] Fixed: {file_path} (removed {unicode_count} Unicode chars)")

                except Exception as e:
                    print(f"Error fixing {file_path}: {e}")

        return fixed_files, total_unicode

    def check_all_directories(self) -> Dict[str, Tuple[int, List[str]]]:
        """Check all critical directories."""
        results = {}

        for directory in CRITICAL_DIRECTORIES:
            unicode_count, files = self.check_directory(directory)
            if unicode_count > 0:
                results[directory] = (unicode_count, files)

        return results

    def fix_all_directories(self) -> Tuple[int, int]:
        """Fix all critical directories."""
        total_files = 0
        total_unicode = 0

        print("[OK] Starting Unicode contamination prevention...")

        for directory in CRITICAL_DIRECTORIES:
            print(f"\nChecking {directory}:")
            files_fixed, unicode_removed = self.fix_directory(directory)
            total_files += files_fixed
            total_unicode += unicode_removed

        return total_files, total_unicode

    def create_monitor_hook(self) -> str:
        """Create a monitoring hook script."""
        hook_content = '''#!/bin/bash
# Unicode contamination prevention hook
# This script should be called after any content generation

python "$(dirname "$0")/../lib/unicode_contamination_prevention.py" --fix
'''

        hook_path = Path(".git/hooks/unicode-prevention")
        hook_path.parent.mkdir(exist_ok=True)

        with open(hook_path, 'w') as f:
            f.write(hook_content)

        # Make it executable
        os.chmod(hook_path, 0o755)

        return str(hook_path)

    def monitor_continuously(self, interval: int = 60):
        """Monitor directories continuously for new Unicode characters."""
        print(f"[OK] Starting continuous Unicode monitoring (interval: {interval}s)")
        print("Press Ctrl+C to stop...")

        try:
            while True:
                contamination = self.check_all_directories()

                if contamination:
                    print(f"\n[WARN] Unicode contamination detected!")
                    for directory, (count, files) in contamination.items():
                        print(f"  {directory}: {count} Unicode chars in {len(files)} files")

                    print("[INFO] Auto-fixing contamination...")
                    self.fix_all_directories()
                    print("[OK] Contamination fixed")

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n[OK] Stopping continuous monitoring")

def main():
    parser = argparse.ArgumentParser(description="Prevent Unicode contamination in Claude's context")
    parser.add_argument('--check', action='store_true', help='Check for Unicode characters')
    parser.add_argument('--fix', action='store_true', help='Fix Unicode characters')
    parser.add_argument('--monitor', action='store_true', help='Monitor continuously')
    parser.add_argument('--interval', type=int, default=60, help='Monitoring interval in seconds')
    parser.add_argument('--install-hook', action='store_true', help='Install git hook')

    args = parser.parse_args()

    prevention = UnicodeContaminationPrevention()

    if args.install_hook:
        hook_path = prevention.create_monitor_hook()
        print(f"[OK] Git hook installed: {hook_path}")
        return

    if args.check:
        print("[OK] Checking for Unicode contamination...")
        contamination = prevention.check_all_directories()

        if contamination:
            print(f"\n[WARN] Unicode contamination found:")
            total_unicode = 0
            total_files = 0

            for directory, (count, files) in contamination.items():
                print(f"  {directory}: {count} Unicode chars in {len(files)} files")
                total_unicode += count
                total_files += len(files)

            print(f"\nTotal: {total_unicode} Unicode chars in {total_files} files")
            print("Run with --fix to clean up contamination")
        else:
            print("[OK] No Unicode contamination found")

    elif args.fix:
        files_fixed, unicode_removed = prevention.fix_all_directories()

        print(f"\n=== UNICODE CONTAMINATION PREVENTION COMPLETE ===")
        print(f"Files fixed: {files_fixed}")
        print(f"Unicode characters removed: {unicode_removed}")

        if files_fixed > 0:
            print(f"[OK] Claude's context is now safe from Unicode contamination")
        else:
            print(f"[OK] No Unicode contamination found")

    elif args.monitor:
        prevention.monitor_continuously(args.interval)

    else:
        print("Usage: python unicode_contamination_prevention.py [--check|--fix|--monitor]")
        print("  --check     Check for Unicode contamination")
        print("  --fix       Fix Unicode contamination")
        print("  --monitor   Monitor continuously for contamination")
        print("  --install-hook Install git hook for automatic prevention")

if __name__ == "__main__":
    main()