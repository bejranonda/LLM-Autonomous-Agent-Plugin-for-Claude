#!/usr/bin/env python3
"""
Fix emoji usage in Python files for Windows compatibility.
Replaces common emojis with ASCII alternatives.
"""

import os
import re
from pathlib import Path

# Emoji to ASCII replacement mapping
EMOJI_REPLACEMENTS = {
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
    '🎪': '[CIRCUS]',
    '🎭': '[DRAMA]',
    '🎪': '[EVENT]',
    '🌈': '[RAINBOW]',
    '🔥': '[FIRE]',
    '💯': '[100]',
    '🎉': '[PARTY]',
    '🎊': '[CONFETTI]',
    '🏁': '[FINISH]',
    '📍': '[PIN]',
    '🗺️': '[MAP]',
    '🧭': '[COMPASS]',
    '⚡': '[BOLT]',
    '🔋': '[BATTERY]',
    '💻': '[COMPUTER]',
    '🖥️': '[DESKTOP]',
    '📱': '[PHONE]',
    '⌚': '[WATCH]',
    '🖱️': '[MOUSE]',
    '⌨️': '[KEYBOARD]',
    '🖨️': '[PRINTER]',
    '📡': '[SIGNAL]',
    '📞': '[PHONE]',
    '📟': '[PAGER]',
    '📠': '[FAX]',
    '🔔': '[BELL]',
    '📢': '[SPEAKER]',
    '📣': '[MEGAPHONE]',
    '📯': '[BULLSEYE]',
    '🎙️': '[MIC]',
    '🎚️': ['SLIDERS'],
    '🎛️': ['CONTROL_KNOB'],
    '🧩': '[PUZZLE]',
    '🔐': '[LOCK]',
    '🔒': '[LOCKED]',
    '🔓': '[UNLOCK]',
    '🔑': '[KEY]',
    '🗝️': '[KEY]',
    '🔨': '[HAMMER]',
    '⛏️': '[PICK]',
    '🔧': '[WRENCH]',
    '⚙️': '[GEAR]',
    '🔩': '[BOLT_NUT]',
    '⚖️': '[SCALES]',
    '🦽': '[WHEELCHAIR]',
    '🦼': '[WHEELCHAIR_MANUAL]',
    '🦾': '[MECHANICAL_ARM]',
    '🦿': '[MECHANICAL_LEG]',
    '🛹': '[SKATEBOARD]',
    '🛼': '[ROLLER_SKATE]',
    '🚲': '[PROHIBITED]',
    '🛴': '[SCOOTER]',
    '🛵': ['MOTOR_SCOOTER'],
    '🚲': '[NO_ACCESS]',
    '🚭': '[NO_SMOKING]',
    '🚮': '[NO_LITTERING]',
    '🚰': '[NO_PED"],
    '🚱': '[NO_PEDESTRIANS]',
    '🚷': '[NO_ACCESS]',
    '📵': '[NO_PHONES]',
    '🔞': '[NO_UNDER_18]',
    '☢️': '[RADIATION]',
    '☣️': '[BIOHAZARD]',
    '⬆️': '[UP]',
    '↗️': '[UP_RIGHT]',
    '➡️': '[RIGHT]',
    '↘️': ['DOWN_RIGHT'],
    '⬇️': '[DOWN]',
    '↙️': ['DOWN_LEFT'],
    '⬅️': '[LEFT]',
    '↖️': '[UP_LEFT]',
    '↕️': '[UP_DOWN]',
    '↔️': ['LEFT_RIGHT'],
    '↩️': '[UNDO]',
    '↪️': '[REDO]',
    '⤴️': '[UP_CYCLE]',
    '⤵️': ['DOWN_CYCLE'],
    '🔃': '[SYNC]',
    '🔄': '[REPEAT]',
    '🔙': '[BACK]',
    '🔚': '[END]',
    '🔛': ['ON_OFF'],
    '🔜': '[SOON]',
    '🔝': '[TOP]',
}

def fix_emoji_in_file(file_path):
    """Replace emojis with ASCII alternatives in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Replace each emoji with its ASCII alternative
        for emoji, replacement in EMOJI_REPLACEMENTS.items():
            content = content.replace(emoji, replacement)

        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"[ERROR] Could not process {file_path}: {e}")
        return False

def main():
    """Fix emoji usage in all Python files in lib/ directory."""
    lib_dir = Path("lib")
    fixed_files = []
    error_files = []

    print("[INFO] Starting emoji compatibility fix...")
    print(f"[INFO] Target directory: {lib_dir.absolute()}")

    # Find all Python files
    python_files = list(lib_dir.rglob("*.py"))

    print(f"[INFO] Found {len(python_files)} Python files to check")

    for file_path in python_files:
        print(f"[INFO] Processing: {file_path.relative_to(lib_dir)}")
        if fix_emoji_in_file(file_path):
            fixed_files.append(file_path)
            print(f"   [OK] Fixed emojis in {file_path.name}")
        else:
            print(f"   [SKIP] No emojis found")

    print(f"\n[SUMMARY] Emoji Fix Complete:")
    print(f"   Files fixed: {len(fixed_files)}")
    print(f"   Files skipped: {len(python_files) - len(fixed_files)}")
    print(f"   Errors: {len(error_files)}")

    if fixed_files:
        print(f"\n[SUCCESS] Fixed files:")
        for file_path in fixed_files:
            print(f"   - {file_path}")

    if error_files:
        print(f"\n[ERROR] Could not process:")
        for file_path in error_files:
            print(f"   - {file_path}")

    print(f"\n[COMPLETE] Python files now Windows-compatible!")

if __name__ == "__main__":
    main()