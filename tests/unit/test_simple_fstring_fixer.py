"""
Tests for simple_fstring_fixer.py utility
"""

import pytest
import sys
import os

# Add lib to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from simple_fstring_fixer import fix_fstring_patterns


class TestSimpleFstringFixer:
    """Test cases for f-string pattern fixing"""

    def test_fix_pattern_1_mismatched_quotes(self):
        """Fix f"text{var": "format"} → f"text{var}: format"""
        content = 'f"Hello {name": "World"}"'
        expected = 'f"Hello {name}: World"'
        result = fix_fstring_patterns(content)
        assert result == expected

    def test_fix_pattern_2_single_quotes(self):
        """Fix f'text{var': 'format'} → f'text{var}: format"""
        content = "f'Hello {name': 'World'}'"
        expected = "f'Hello {name}: World'"
        result = fix_fstring_patterns(content)
        assert result == expected

    def test_fix_pattern_3_format_specifier(self):
        """Fix f"text{var": ".1f"} → f"text{var:.1f}"""
        content = 'f"Value {number": ".1f"}"'
        expected = 'f"Value {number:.1f}"'
        result = fix_fstring_patterns(content)
        assert result == expected

    def test_fix_pattern_4_general_format(self):
        """Fix {var: "format"} → {var:format}"""
        content = '{price: ".2f"}'
        expected = '{price:.2f}'
        result = fix_fstring_patterns(content)
        assert result == expected

    def test_no_changes_needed(self):
        """Test that correctly formatted f-strings are not changed"""
        content = 'f"Hello {name}: {value:.2f}"'
        result = fix_fstring_patterns(content)
        assert result == content  # Should be unchanged

    def test_multiple_patterns_in_one_string(self):
        """Test multiple f-string patterns in the same content"""
        content = '''
        f"Hello {name": "World"}
        f'Value {num': '.2f'}
        f"Price {price": ".1f"}
        {amount: ".2f"}
        '''
        expected = '''
        f"Hello {name}: World"
        f'Value {num}: .2f'
        f"Price {price:.1f}"
        {amount:.2f}
        '''
        result = fix_fstring_patterns(content)
        assert result == expected

    def test_empty_string(self):
        """Test with empty string"""
        content = ""
        result = fix_fstring_patterns(content)
        assert result == ""

    def test_non_fstring_content(self):
        """Test with content that doesn't contain f-strings"""
        content = 'print("Hello world")\nprint(name)'
        result = fix_fstring_patterns(content)
        assert result == content

    def test_complex_nested_fstrings(self):
        """Test with more complex nested patterns"""
        content = 'f"User {user_name": "Admin"} has {count": "5"} messages"'
        expected = 'f"User {user_name}: Admin} has {count: 5} messages"'
        result = fix_fstring_patterns(content)
        assert result == expected

    def test_mixed_quote_types(self):
        """Test with mixed single and double quotes"""
        content = 'f"Hello {name": \'World\'}'
        result = fix_fstring_patterns(content)
        # Should handle the double quote pattern
        assert 'f"Hello {name}: World"}' in result

    def test_partial_patterns_only(self):
        """Test that partial patterns don't affect the rest of the string"""
        content = 'f"Hello {name": "World"} and f"Goodbye {other}"'
        expected = 'f"Hello {name}: World} and f"Goodbye {other}"'
        result = fix_fstring_patterns(content)
        assert result == expected

    def test_special_characters_in_content(self):
        """Test with special characters"""
        content = 'f"Value {amount": "$1,234.56"}"'
        expected = 'f"Value {amount}: $1,234.56}"'
        result = fix_fstring_patterns(content)
        assert result == expected