#!/usr/bin/env python3
"""
Unicode Encoding Fix Script

This script fixes Unicode encoding issues in documentation files by replacing
Unicode characters with ASCII equivalents to ensure compatibility across
different platforms and environments.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class UnicodeFixer:
    """Fixes Unicode encoding issues in text files"""

    def __init__(self):
        # Unicode to ASCII mappings
        self.replacements = {
            # Check marks and crosses
            '✅': '[OK]',
            '❌': '[FAIL]',
            '⚠️': '[WARN]',
            '✔': '[OK]',
            '✘': '[FAIL]',
            '✓': '[OK]',

            # Colored circles and indicators
            '🔴': '[HIGH]',
            '🟡': '[MED]',
            '🟢': '[LOW]',
            '🔵': '[INFO]',
            '⚪': '[NONE]',

            # Arrows and directional indicators
            '→': '->',
            '←': '<-',
            '↑': '^',
            '↓': 'v',
            '⇒': '=>',
            '⇐': '<=',
            '⇑': '^^',
            '⇓': 'vv',

            # Common symbols
            '🚀': '[FAST]',
            '📊': '[DATA]',
            '📈': '[UP]',
            '📉': '[DOWN]',
            '🎯': '[TARGET]',
            '💡': '[IDEA]',
            '🔧': '[FIX]',
            '🛡️': '[SAFE]',
            '📋': '[LIST]',
            '🎉': '[SUCCESS]',
            '⭐': '[STAR]',
            '❗': '[NOTE]',
            'ℹ️': '[INFO]',
            '📝': '[WRITE]',
            '🔄': '[REPEAT]',
            '🗄️': '[STORAGE]',
            '🧠': '[SMART]',
            '👥': '[TEAM]',
            '⚡': '[FAST]',
            '🏆': '[TROPHY]',
            '🌟': '[STAR]',
            '💎': '[GEM]',
            '🔑': '[KEY]',
            '🔍': '[SEARCH]',
            '🌐': '[WEB]',
            '📱': '[PHONE]',
            '💻': '[COMPUTER]',

            # Faces and people
            '😊': '[HAPPY]',
            '🙂': '[SMILE]',
            '😐': '[NEUTRAL]',
            '😞': '[SAD]',
            '😢': '[CRY]',
            '😡': '[ANGRY]',
            '🤔': '[THINKING]',
            '😎': '[COOL]',
            '🤖': '[ROBOT]',

            # Hearts and favorites
            '❤️': '[LOVE]',
            '💔': '[BROKEN]',
            '💯': '[100]',

            # Weather and nature
            '☀️': '[SUN]',
            '🌙': '[MOON]',
            '⭐': '[STAR]',
            '🌧': '[WRENCH]',

            # Warning and error symbols
            '⚠': '[WARNING]',
            '⛔': '[NO]',
            '🚫': '[FORBIDDEN]',
            '🚨': '[ALERT]',

            # Math and symbols
            '×': 'x',
            '÷': '/',
            '±': '+/-',
            '∞': 'inf',
            '∑': 'SUM',
            '∏': 'PROD',
            '∆': 'DELTA',
            '∇': 'NABLA',
            '∂': 'PARTIAL',
            '∫': 'INTEGRAL',
            'π': 'PI',
            '∞': 'INFINITY',

            # Currency
            '€': 'EUR',
            '£': 'GBP',
            '¥': 'JPY',
            '₹': 'INR',

            # Other symbols
            '©': '(c)',
            '®': '(r)',
            '™': '(tm)',
            '°': 'deg',
            '′': "'",
            '″': '"',
            '…': '...',
            '—': '--',
            '–': '-',
        }

        # Compile regex pattern for Unicode characters
        unicode_pattern = '[' + ''.join(re.escape(char) for char in self.replacements.keys()) + ']'
        self.unicode_regex = re.compile(unicode_pattern)

    def fix_file(self, file_path: str) -> Tuple[bool, int]:
        """
        Fix Unicode characters in a file

        Args:
            file_path: Path to the file to fix

        Returns:
            Tuple of (success, number_of_replacements)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count Unicode characters
            unicode_count = len(self.unicode_regex.findall(content))

            if unicode_count == 0:
                return True, 0

            # Replace Unicode characters
            fixed_content = content
            replacements_made = 0

            for unicode_char, ascii_replacement in self.replacements.items():
                count = fixed_content.count(unicode_char)
                if count > 0:
                    fixed_content = fixed_content.replace(unicode_char, ascii_replacement)
                    replacements_made += count

            # Write fixed content back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)

            return True, replacements_made

        except Exception as e:
            print(f"Error fixing file {file_path}: {e}")
            return False, 0

    def fix_directory(self, directory: str, pattern: str = "*.md") -> Dict[str, any]:
        """
        Fix Unicode characters in all files in a directory

        Args:
            directory: Directory to scan
            pattern: File pattern to match

        Returns:
            Dictionary with results
        """
        directory_path = Path(directory)
        if not directory_path.exists():
            return {"error": f"Directory {directory} does not exist"}

        results = {
            "directory": directory,
            "pattern": pattern,
            "files_scanned": 0,
            "files_fixed": 0,
            "total_replacements": 0,
            "errors": [],
            "fixed_files": []
        }

        # Find all matching files
        files = list(directory_path.glob(pattern))
        results["files_scanned"] = len(files)

        for file_path in files:
            success, replacements = self.fix_file(str(file_path))

            if success:
                if replacements > 0:
                    results["files_fixed"] += 1
                    results["total_replacements"] += replacements
                    results["fixed_files"].append({
                        "file": str(file_path.relative_to(directory_path)),
                        "replacements": replacements
                    })
            else:
                results["errors"].append(str(file_path.relative_to(directory_path)))

        return results

    def generate_report(self, results: Dict[str, any]) -> str:
        """Generate a readable report from the results"""
        report = []
        report.append("Unicode Encoding Fix Report")
        report.append("=" * 50)
        report.append(f"Directory: {results['directory']}")
        report.append(f"Pattern: {results['pattern']}")
        report.append(f"Files Scanned: {results['files_scanned']}")
        report.append(f"Files Fixed: {results['files_fixed']}")
        report.append(f"Total Replacements: {results['total_replacements']}")

        if results["errors"]:
            report.append(f"Errors: {len(results['errors'])}")
            report.append("Files with errors:")
            for error in results["errors"]:
                report.append(f"  - {error}")

        if results["fixed_files"]:
            report.append("")
            report.append("Fixed Files:")
            for file_info in results["fixed_files"][:10]:  # Show first 10
                report.append(f"  - {file_info['file']}: {file_info['replacements']} replacements")

            if len(results["fixed_files"]) > 10:
                report.append(f"  ... and {len(results['fixed_files']) - 10} more files")

        return "\n".join(report)


def main():
    """Main function"""
    import sys

    # Directory containing files to fix
    docs_dir = "docs/reports/generated"

    if not os.path.exists(docs_dir):
        print(f"Directory {docs_dir} does not exist!")
        sys.exit(1)

    print("Fixing Unicode Encoding Issues...")
    print("-" * 50)

    fixer = UnicodeFixer()
    results = fixer.fix_directory(docs_dir, "*.md")

    print(fixer.generate_report(results))

    if results["total_replacements"] > 0:
        print(f"\n[OK] Successfully fixed {results['total_replacements']} Unicode characters!")
        print(f"   {results['files_fixed']} files were updated.")
    else:
        print("\n[OK] No Unicode encoding issues found!")

    if results["errors"]:
        print(f"\n[WARN] {len(results['errors'])} files had errors:")
        for error in results["errors"]:
            print(f"   - {error}")


if __name__ == "__main__":
    main()