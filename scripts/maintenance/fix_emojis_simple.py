#!/usr/bin/env python3
"""
Simple emoji fixer for Python files - Windows compatibility
"""

import os
from pathlib import Path

def fix_emojis_in_file(file_path):
    """Replace common emojis with ASCII alternatives."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Common emoji replacements
        replacements = {
            '🧠': '[BRAIN]',
            '✅': '[OK]',
            '❌': '[ERROR]',
            '⚠️': '[WARN]',
            '🎯': '[TARGET]',
            '📊': '[DATA]',
            '🛠️': '[TOOLS]',
            '🔧': '[FIX]',
            '💡': '[INFO]',
            '🚀': '[START]',
            '🧪': '[TEST]',
            '📈': '[TREND]',
            '🎨': '[STYLE]',
            '📝': '[NOTE]',
            '🔍': '[SEARCH]',
            '⭐': '[STAR]',
            '🏆': '[AWARD]',
            '🔄': '[RETRY]',
            '📋': '[LIST]',
            '💾': '[SAVE]',
            '🌟': '[SPARKLE]',
            '✨': '[SHINE]',
            '🎪': '[EVENT]',
            '🎉': '[PARTY]',
            '🏁': '[FINISH]',
            '📍': '[PIN]',
            '⚡': '[BOLT]',
            '🔋': '[BATTERY]',
            '💻': '[COMPUTER]',
            '🖥️': '[DESKTOP]',
            '📱': '[PHONE]',
            '🔔': '[BELL]',
            '📢': '[SPEAKER]',
            '🎙️': '[MIC]',
            '🧩': '[PUZZLE]',
            '🔐': '[LOCK]',
            '🔒': '[LOCKED]',
            '🔓': '[UNLOCK]',
            '🔑': '[KEY]',
            '🔨': '[HAMMER]',
            '⛏️': '[PICK]',
            '⚙️': '[GEAR]',
            '⬆️': '[UP]',
            '➡️': '[RIGHT]',
            '⬇️': '[DOWN]',
            '⬅️': '[LEFT]',
            '🔃': '[SYNC]',
            '🔙': '[BACK]',
            '🔚': '[END]',
            '🔝': '[TOP]',
        }

        # Apply replacements
        for emoji, replacement in replacements.items():
            content = content.replace(emoji, replacement)

        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return False

def main():
    """Main function."""
    lib_dir = Path("lib")
    fixed_count = 0
    total_count = 0

    print("[INFO] Fixing emojis for Windows compatibility...")

    for py_file in lib_dir.rglob("*.py"):
        total_count += 1
        if fix_emojis_in_file(py_file):
            fixed_count += 1
            print(f"[FIXED] {py_file.name}")

    print(f"\n[COMPLETE] Fixed {fixed_count}/{total_count} files")
    print("[SUCCESS] Python files now Windows-compatible!")

if __name__ == "__main__":
    main()