#!/usr/bin/env python3
"""
Fix multi-line HTML template literals in dashboard.py
Converts them to regular string concatenation
"""

import re

def fix_html_templates():
    file_path = 'D:\\Git\\Werapol\\AutonomousAgent\\.claude-patterns\\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match multi-line template literals starting with `
    # and ending with `; (including the closing backtick and semicolon)
    html_template_pattern = r'`\s*\n([^`]*?)\n\s*`;'

    def replace_html_template(match):
        template_content = match.group(1)

        # Convert to regular string by escaping newlines and quotes
        # Replace newlines with \n and escape single quotes
        escaped_content = template_content.replace('\n', '\\n').replace("'", "\\'")

        # Return as regular string concatenation
        return "' + \\\n        '" + escaped_content + "'"

    # Apply the replacement
    fixed_content = re.sub(html_template_pattern, replace_html_template, content, flags=re.MULTILINE | re.DOTALL)

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print("Fixed all HTML template literals in dashboard.py")

if __name__ == '__main__':
    fix_html_templates()