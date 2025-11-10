#!/usr/bin/env python3
"""
Check the actual JavaScript content being served by the dashboard
"""

import urllib.request
import re

def check_current_js():
    try:
        response = urllib.request.urlopen('http://127.0.0.1:5001', timeout=10)
        content = response.read().decode('utf-8')

        # Find the JavaScript section
        script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
        if script_match:
            js_content = script_match.group(1)
            js_lines = js_content.split('\n')

            print('Current JavaScript analysis:')
            print(f'Total JavaScript lines: {len(js_lines)}')

            # Check around line 1827
            if len(js_lines) > 1827:
                print('\\nLines around 1827:')
                for i in range(max(0, 1827 - 3), min(len(js_lines), 1827 + 4)):
                    line_num = i + 1
                    marker = ' ERROR -> ' if i == 1827 else '         '
                    line_content = js_lines[i]
                    print(f'{marker}Line {line_num:4d}: {repr(line_content[:80])}')

                    # Check for issues
                    if '=>' in line_content:
                        print(f'         ^ Arrow function found!')
                    if '`' in line_content:
                        print(f'         ^ Template literal found!')
            else:
                print(f'JavaScript section has only {len(js_lines)} lines (less than 1827)')

            # Count issues in the entire JavaScript
            template_literal_count = js_content.count('`')
            arrow_function_count = js_content.count('=>')

            print(f'\\nJavaScript issue summary:')
            print(f'Template literals: {template_literal_count}')
            print(f'Arrow functions: {arrow_function_count}')

            if template_literal_count > 0:
                print('TEMPLATE LITERAL ISSUES FOUND!')
                # Find first few template literals
                for i, line in enumerate(js_lines):
                    if '`' in line and i < 20:
                        print(f'  Line {i+1}: {repr(line[:60])}')

            if arrow_function_count > 0:
                print('ARROW FUNCTION ISSUES FOUND!')
                # Find first few arrow functions
                for i, line in enumerate(js_lines):
                    if '=>' in line and i < 20:
                        print(f'  Line {i+1}: {repr(line[:60])}')

            return template_literal_count > 0 or arrow_function_count > 0
        else:
            print('No JavaScript section found')
            return False

    except Exception as e:
        print(f'Error checking dashboard: {e}')
        return False

if __name__ == '__main__':
    has_issues = check_current_js()
    if has_issues:
        print('\\nJAVASCRIPT ERRORS CONFIRMED - Fixes not applied to running instance!')
    else:
        print('\\nJavaScript appears to be clean')