#!/usr/bin/env python3
#     Fix line length violations in Python files
"""
"""
import re
import textwrap
from pathlib import Path


def fix_line_length(filepath, max_length=88):
    """Fix line length violations in a file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        fixed_lines = []
        changes = 0

        for line in lines:
            line = line.rstrip("\n")

            # Skip if line is already within limit
            if len(line) <= max_length:
                fixed_lines.append(line + "\n")
                continue

            # Don't modify comments or strings that are too long
            if line.strip().startswith("#") or '"""' in line or "'''" in line:
                # For comments, try to wrap them
                if line.strip().startswith("#"):
                    comment_text = line.strip()[1:].strip()
                    if len(comment_text) > max_length - 3:
                        wrapped = textwrap.wrap(comment_text, width=max_length - 3)
                        for i, wrapped_line in enumerate(wrapped):
                            prefix = "# " if i == 0 else "# "
                            fixed_lines.append(prefix + wrapped_line + "\n")
                        changes += 1
                        continue
                fixed_lines.append(line + "\n")
                continue

            # Fix import statements
            if line.strip().startswith("import ") or line.strip().startswith("from "):
                fixed_lines.extend(fix_import_line(line, max_length))
                changes += 1
                continue

            # Fix function/method calls
            if "(" in line and ")" in line and "=" not in line.split("(")[0]:
                fixed_lines.extend(fix_function_call(line, max_length))
                changes += 1
                continue

            # Fix long string concatenations
            if " + " in line and ('"' in line or "'" in line):
                fixed_lines.extend(fix_string_concat(line, max_length))
                changes += 1
                continue

            # Fix long dictionary/list definitions
            if line.strip().startswith("{") or line.strip().startswith("["):
                fixed_lines.extend(fix_collection_definition(line, max_length))
                changes += 1
                continue

            # Generic line wrapping for other cases
            wrapped_lines = wrap_generic_line(line, max_length)
            if len(wrapped_lines) > 1:
                fixed_lines.extend(wrapped_lines)
                changes += 1
            else:
                fixed_lines.append(line + "\n")

        # Write back the file if changes were made
        if changes > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(fixed_lines)
            return changes
        return 0

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0


def fix_import_line(line, max_length):
    """Fix long import lines"""
    lines = []
    stripped = line.strip()

    if stripped.startswith("from "):
        # from x import (a, b, c) format
        parts = stripped.split(" import ")
        if len(parts) == 2:
            module = parts[0]
            imports = parts[1]
            if "(" in imports and ")" in imports:
                # Already in multi-line format, just wrap properly
                lines.append(module + " import (\n")
                imports = imports[1:-1].strip()
                import_items = [imp.strip() for imp in imports.split(",")]
                for imp in import_items:
                    lines.append(f"    {imp},\n")
                lines.append(")\n")
            else:
                # Convert to multi-line format
                lines.append(module + " import (\n")
                import_items = [imp.strip() for imp in imports.split(",")]
                for imp in import_items:
                    lines.append(f"    {imp},\n")
                lines.append(")\n")
    else:
        # Regular import statement
        imports = stripped[6:].strip()  # Remove 'import '
        lines.append("import (\n")
        import_items = [imp.strip() for imp in imports.split(",")]
        for imp in import_items:
            lines.append(f"    {imp},\n")
        lines.append(")\n")

    return lines


def fix_function_call(line, max_length):
    """Fix long function calls"""
    lines = []

    # Find function name and opening parenthesis
    paren_pos = line.find("(")
    if paren_pos == -1:
        return [line + "\n"]

    func_name = line[:paren_pos]
    args_content = line[paren_pos + 1 : -1] if line.endswith(")") else line[paren_pos + 1 :]

    lines.append(func_name + "(\n")

    # Split arguments
    args = split_arguments(args_content)
    for arg in args:
        lines.append(f"    {arg},\n")

    lines.append(")\n")
    return lines


def split_arguments(args_str):
    """Split arguments string considering nested parentheses"""
    args = []
    current_arg = ""
    paren_depth = 0

    for char in args_str:
        if char == "(":
            paren_depth += 1
        elif char == ")":
            paren_depth -= 1
        elif char == "," and paren_depth == 0:
            args.append(current_arg.strip())
            current_arg = ""
            continue
        current_arg += char

    if current_arg.strip():
        args.append(current_arg.strip())

    return args


def fix_string_concat(line, max_length):
    """Fix string concatenations"""
    lines = []

    # Find string parts
    parts = line.split(" + ")
    if len(parts) <= 1:
        return [line + "\n"]

    # Use string join instead
    strings = []
    for part in parts:
        part = part.strip()
        if part.startswith('"') and part.endswith('"'):
            strings.append(part[1:-1])
        elif part.startswith("'") and part.endswith("'"):
            strings.append(part[1:-1])

    if strings:
        lines.append("    ".join(strings) + "\n")
    else:
        lines.append(line + "\n")

    return lines


def fix_collection_definition(line, max_length):
    """Fix dictionary/list definitions"""
    lines = []
    stripped = line.strip()

    if stripped.startswith("{"):
        lines.append("{\n")
        content = stripped[1:-1].strip()
        if content:
            items = [item.strip() for item in content.split(",")]
            for item in items:
                if item:
                    lines.append(f"    {item},\n")
        lines.append("}\n")
    elif stripped.startswith("["):
        lines.append("[\n")
        content = stripped[1:-1].strip()
        if content:
            items = [item.strip() for item in content.split(",")]
            for item in items:
                if item:
                    lines.append(f"    {item},\n")
        lines.append("]\n")
    else:
        lines.append(line + "\n")

    return lines


def wrap_generic_line(line, max_length):
    """Generic line wrapper"""
    # Try to break at logical points
    break_points = [" and ", " or ", " if ", " else ", " in ", " == ", " != ", " < ", " > ", " <= ", " >= "]

    for bp in break_points:
        if bp in line:
            parts = line.split(bp)
            if len(parts) == 2:
                indent = " " * (len(line) - len(line.lstrip()))
                return [parts[0] + bp + "\n", indent + "    " + parts[1] + "\n"]

    # Default: simple wrap
    return [line + "\n"]


def main():
    """Main function"""
"""
    # Find all Python files
    py_files = list(Path(".").rglob("*.py"))
    py_files = [f for f in py_files if "__pycache__" not in str(f) and ".git" not in str(f)]

    total_changes = 0
    files_modified = 0

    for py_file in py_files:
        changes = fix_line_length(py_file)
        if changes > 0:
            print(f"{py_file}: {changes} lines fixed")
            total_changes += changes
            files_modified += 1

    print(f"\nTotal lines fixed: {total_changes}")
    print(f"Files modified: {files_modified}")


if __name__ == "__main__":
    main()
