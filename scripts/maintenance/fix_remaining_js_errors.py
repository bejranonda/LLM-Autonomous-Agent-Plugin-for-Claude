#!/usr/bin/env python3
"""
Fix the remaining JavaScript syntax errors at specific locations
"""

def fix_remaining_js_errors():
    file_path = 'D:\Git\Werapol\AutonomousAgent\.claude-patterns\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixes_applied = 0

    print("Fixing remaining JavaScript syntax errors...")

    # Fix 1: Look for any remaining template literals in JavaScript
    template_pattern = r'\]*\$\{[^}]+\}[^'
    matches = re.findall(template_pattern, content)

    if matches:
        print(f"Found {len(matches)} remaining template literals")
        for match in matches:
            print(f"  - {match[:50]}...")
            # Replace with string concatenation
            parts = re.split(r'\$\{([^}]+)\}', match)
            result = "'"
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    escaped_part = part.replace("'", "\'")
                    result += escaped_part
                else:
                    result += "' + (" + part + ") + '"
            result += "'"
            content = content.replace(f'', result)
            fixes_applied += 1

    # Fix 2: Look for any remaining arrow functions in JavaScript
    arrow_patterns = [
        (r'(\w+)\s*=>\s*\{', r'function() {'),
        (r'(\w+)\s*=>\s*([^,
\}]+)', r'function() { return ; }'),
        (r'\(([^)]+)\)\s*=>\s*\{', r'function() {'),
        (r'\(([^)]+)\)\s*=>\s*([^,
\}]+)', r'function() { return ; }'),
    ]

    for pattern, replacement in arrow_patterns:
        matches = re.findall(pattern, content)
        if matches:
            print(f"Found {len(matches)} arrow functions with pattern: {pattern}")
            content = re.sub(pattern, replacement, content)
            fixes_applied += len(matches)

    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"
Applied {fixes_applied} additional JavaScript fixes to dashboard.py")
        return True
    else:
        print("No additional JavaScript fixes needed")
        return False

if __name__ == '__main__':
    fix_remaining_js_errors()
