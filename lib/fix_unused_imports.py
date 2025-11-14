#!/usr/bin/env python3
"""
Fix unused imports in Python files
"""

import ast
from pathlib import Path


def find_unused_imports(filepath):
    """Find unused imports in a Python file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse AST
        tree = ast.parse(content)

        # Collect all imports
        imports = []
        import_lines = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports.append(name)
                    import_lines[name] = node.lineno
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    full_name = f"{module}.{name}" if module else name
                    imports.append(name)
                    import_lines[name] = node.lineno

        # Find all used names
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                # Get the base name for attribute access
                if isinstance(node.value, ast.Name):
                    used_names.add(node.value.id)

        # Find unused imports
        unused = []
        for imp in imports:
            # Special cases that might be used in ways AST doesn't catch
            if imp in ["__all__", "__version__"]:
                continue
            if imp not in used_names:
                unused.append((imp, import_lines.get(imp, 0)))

        return unused
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return []


def remove_unused_imports(filepath, unused_imports):
    """Remove unused imports from a file"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Sort by line number in reverse order to avoid shifting indices
    unused_imports.sort(key=lambda x: x[1], reverse=True)

    for import_name, line_num in unused_imports:
        if line_num > 0 and line_num <= len(lines):
            # Find the import statement
            line = lines[line_num - 1]

            # Handle multi-line imports
            if "(" in line and ")" not in line:
                # Find the closing parenthesis
                end_line = line_num
                while end_line <= len(lines) and ")" not in lines[end_line - 1]:
                    end_line += 1

                # Remove the entire multi-line import
                for i in range(end_line - line_num + 1):
                    if line_num - 1 < len(lines):
                        lines.pop(line_num - 1)
            else:
                # Remove single line import
                lines.pop(line_num - 1)

    # Write back the file
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)


def main():
    """Main function"""
    # Find all Python files
    py_files = list(Path(".").rglob("*.py"))

    # Filter out __pycache__ and other non-source directories
    py_files = [f for f in py_files if "__pycache__" not in str(f) and ".git" not in str(f)]

    total_unused = 0

    for py_file in py_files:
        unused = find_unused_imports(py_file)
        if unused:
            print(f"{py_file}: {len(unused)} unused imports")
            for imp, line in unused:
                print(f"  Line {line}: {imp}")

            # Automatically remove unused imports
            remove_unused_imports(py_file, unused)
            total_unused += len(unused)
            print(f"  Removed {len(unused)} unused imports")

    print(f"\nTotal unused imports removed: {total_unused}")


if __name__ == "__main__":
    main()
