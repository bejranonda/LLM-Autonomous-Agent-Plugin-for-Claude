#!/usr/bin/env python3
#     Fix multiple docstring quote issues in Python files
    """
import os
import re
from pathlib import Path


def fix_docstring_quotes(file_path):
    """Fix files with multiple docstring quotes at the beginning"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Fix pattern: multiple """ at the beginning
        lines = content.split("\n")
        if len(lines) >= 10:
            # Check for the pattern of multiple docstring quotes
            quote_count = 0
            for i, line in enumerate(lines[:10]):
                if line.strip() == '"""':
                    quote_count += 1
                elif quote_count > 0 and line.strip() and not line.startswith('"""'):
                    break

            # If we found more than 2 opening quotes, fix it
            if quote_count > 2:
                # Find the actual content start
                content_start = -1
                docstring_end = -1

                for i, line in enumerate(lines):
                    if line.strip() and not line.strip() == '"""':
                        content_start = i
                        break

                # Find the end of the real docstring
                in_docstring = False
                for i in range(content_start, len(lines)):
                    if '"""' in lines[i]:
                        if in_docstring:
                            docstring_end = i
                            break
                        else:
                            in_docstring = True

                if content_start > 0 and docstring_end > content_start:
                    # Reconstruct the file with proper docstring
                    new_lines = ["#!/usr/bin/env python3"] if lines[0].startswith("#!") else []
                    new_lines.append('"""')

                    # Add the actual docstring content
                    for i in range(content_start, docstring_end):
                        if '"""' not in lines[i]:
                            new_lines.append(lines[i])

                    new_lines.append('"""')
                    new_lines.extend(lines[docstring_end + 1 :])

                    content = "\n".join(new_lines)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Fix docstring issues in lib directory"""
    lib_dir = Path("lib")
    fixed_count = 0

    for py_file in lib_dir.glob("*.py"):
        if fix_docstring_quotes(py_file):
            print(f"Fixed docstring quotes: {py_file}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} files with docstring issues")


if __name__ == "__main__":
    main()
