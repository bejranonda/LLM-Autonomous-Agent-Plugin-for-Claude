#!/usr/bin/env python3
"""
Comprehensive fix for all JavaScript issues in the correct dashboard file
"""

import re

def fix_all_js_issues():
    file_path = '.claude-patterns/dashboard.py'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print('Applying comprehensive JavaScript fixes to .claude-patterns/dashboard.py')
    original_arrow_count = content.count('=>')
    original_template_count = content.count('`')
    print(f'Before fixes - Arrow functions: {original_arrow_count}, Template literals: {original_template_count}')

    original_content = content

    # Fix 1: Replace all arrow functions with traditional functions
    # Simple arrow functions in callbacks
    arrow_fixes = [
        (r'\.forEach\(([^)]*=>[^)]*)\)', r'.forEach(function(\1))'),
        (r'\.map\(([^)]*=>[^)]*)\)', r'.map(function(\1))'),
        (r'\.filter\(([^)]*=>[^)]*)\)', r'.filter(function(\1))'),
        (r'\.reduce\(([^)]*=>[^)]*)\)', r'.reduce(function(\1))'),
        (r'setTimeout\(([^)]*=>[^)]*)\)', r'setTimeout(function(\1)'),
        (r'setInterval\(([^)]*=>[^)]*)\)', r'setInterval(function(\1)'),
        (r'(\w+)\(([^)]*=>[^)]*)\)', r'\1(function(\2))'),
    ]

    for pattern, replacement in arrow_fixes:
        content = re.sub(pattern, replacement, content)

    # Fix 2: Replace template literals with string concatenation
    def replace_template_literal(match):
        template_content = match.group(1)
        # Split on ${} expressions
        parts = re.split(r'\$\{([^}]+)\}', template_content)
        result = "'"
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Regular text - escape single quotes
                escaped_part = part.replace("'", "\\'")
                result += escaped_part
            else:
                # Variable/expression
                result += "' + (" + part + ") + '"
        result += "'"
        return result

    # Replace all template literals
    content = re.sub(r'`([^`]*)`', replace_template_literal, content)

    # Fix 3: Handle specific complex patterns
    # Fix arrow functions in object properties
    content = re.sub(r'(\w+):\s*\(([^)]*)\)\s*=>', r'\1: function(\2)', content)

    # Fix arrow functions in arrays
    content = re.sub(r'\[(\w+)\s*=>\s*([^\]]+)\]', r'[function(\1) { return \2; }]', content)

    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    final_arrow_count = content.count('=>')
    final_template_count = content.count('`')
    print(f'After fixes  - Arrow functions: {final_arrow_count}, Template literals: {final_template_count}')

    if final_arrow_count == 0 and final_template_count == 0:
        print('SUCCESS: All JavaScript issues have been resolved!')
    else:
        print(f'WARNING: {final_arrow_count} arrow functions and {final_template_count} template literals remain')

    return content != original_content

if __name__ == '__main__':
    fix_all_js_issues()