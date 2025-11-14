#!/usr/bin/env python3
"""
Simple f-string syntax fixer for specific patterns
"""
import re


def fix_fstring_patterns(content):
    """Fix f-string patterns with mismatched quotes"""

    # Pattern 1: f"text{var": "format"} → f"text{var}: format"
    content = re.sub(r'f"([^"]*)\{([^}]*)": "([^"]*)"}', r'f"\1{\2}: \3"', content)

    # Pattern 2: f'text{var': 'format'} → f'text{var}: format'
    content = re.sub(r"f'([^']*)\{([^}]*)': '([^']*)'}", r"f'\1{\2}: \3'", content)

    # Pattern 3: f"text{var": ".1f"} → f"text{var:.1f}"
    content = re.sub(r'f"([^"]*)\{([^}]*): "([^"]*)"}', r'f"\1{\2:\3}"', content)

    # Pattern 4: Fix specific format patterns
    content = re.sub(r'\{([^}]*): "([^"]*)"}', r"{\1:\2}", content)

    return content


# Read the file
with open("lib/calculate_success_rate.py", "r", encoding="utf-8") as f:
    content = f.read()

# Apply fixes
fixed_content = fix_fstring_patterns(content)

# Write back
with open("lib/calculate_success_rate.py", "w", encoding="utf-8") as f:
    f.write(fixed_content)

print("Fixed calculate_success_rate.py")
