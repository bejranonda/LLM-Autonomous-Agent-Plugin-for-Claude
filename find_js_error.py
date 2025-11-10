#!/usr/bin/env python3
"""
Find the exact JavaScript syntax error at line 1875:118
"""

import urllib.request
import re

def find_js_error():
    try:
        response = urllib.request.urlopen('http://127.0.0.1:5001', timeout=10)
        content = response.read().decode('utf-8')

        print("Searching for JavaScript syntax issues...")

        # Look for problematic patterns around line 1875
        lines = content.split('\n')

        # Find the JavaScript section
        js_start = -1
        for i, line in enumerate(lines):
            if '<script>' in line:
                js_start = i
                break

        if js_start == -1:
            print("No JavaScript section found")
            return

        # Look around line 1875 (but relative to JS start)
        js_line_1875 = js_start + 1875
        if js_line_1875 < len(lines):
            print(f"\nJavaScript line 1875:")
            print(f"Line {js_line_1875 + 1}: {lines[js_line_1875]}")

            # Check character 118
            line = lines[js_line_1875]
            if len(line) > 118:
                char_at_118 = line[117] if len(line) > 117 else ''
                context_start = max(0, 117 - 20)
                context_end = min(len(line), 117 + 20)
                context = line[context_start:context_end]
                print(f"\nCharacter 118: '{char_at_118}'")
                print(f"Context: ...{context}...")

        # Search for remaining syntax issues
        print("\nSearching for remaining template literals:")
        for i, line in enumerate(lines[js_start:js_start+2000], js_start+1):
            if '`' in line and ('${' in line or line.count('`') % 2 != 0):
                print(f"Line {i}: {line.strip()}")

        print("\nSearching for unmatched quotes:")
        for i, line in enumerate(lines[js_start:js_start+2000], js_start+1):
            if line.count("'") % 2 != 0 or line.count('"') % 2 != 0:
                print(f"Line {i}: {line.strip()}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    find_js_error()