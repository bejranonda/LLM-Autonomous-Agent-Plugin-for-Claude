#!/usr/bin/env python3
"""
Fix all JavaScript template literals in dashboard.py
Converts template literals to string concatenation for better compatibility
"""

import re

def fix_template_literals():
    file_path = 'D:\\Git\\Werapol\\AutonomousAgent\\.claude-patterns\\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match template literals with ${} expressions
    template_pattern = r'`([^`]*\$\{[^}]*\}[^`]*)`'

    def replace_template_literal(match):
        template_content = match.group(1)

        # Replace ${var} with concatenation
        # Split by ${} patterns and keep the parts
        parts = re.split(r'\$\{([^}]+)\}', template_content)

        # Build string concatenation
        result = "'"
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # This is a literal string part
                # Escape single quotes
                escaped_part = part.replace("'", "\\'")
                result += escaped_part
            else:
                # This is a variable/expression part
                result += "' + (" + part + ") + '"

        result += "'"
        return result

    # Apply the replacement
    fixed_content = re.sub(template_pattern, replace_template_literal, content)

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print("Fixed all template literals in dashboard.py")

if __name__ == '__main__':
    fix_template_literals()