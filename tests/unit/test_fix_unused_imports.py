"""
Tests for fix_unused_imports.py utility
"""

import pytest
import ast
import sys
import os
from unittest.mock import patch, mock_open

# Add lib to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from fix_unused_imports import find_unused_imports, remove_unused_imports, main


class TestFixUnusedImports:
    """Test cases for unused import fixing functionality"""

    def test_find_unused_imports_basic(self):
        """Test finding basic unused imports"""
        code = """
import os
import sys
import json
import unused_module

def main():
    print(os.path.join(sys.path[0], "file.json"))
    data = json.loads("{}")
"""
        unused = find_unused_imports(code)
        assert "unused_module" in unused
        assert "os" not in unused
        assert "sys" not in unused
        assert "json" not in unused

    def test_find_unused_imports_multiple_unused(self):
        """Test finding multiple unused imports"""
        code = """
import os
import sys
import json
import requests
import datetime
import pandas

def main():
    print("Hello")
    data = json.loads("{}")
"""
        unused = find_unused_imports(code)
        assert "os" in unused
        assert "sys" in unused
        assert "requests" in unused
        assert "datetime" in unused
        assert "pandas" in unused
        assert "json" not in unused

    def test_find_unused_imports_from_imports(self):
        """Test finding unused from imports"""
        code = """
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

def main():
    path = Path("/tmp")
    now = datetime.now()
"""
        unused = find_unused_imports(code)
        # timedelta should be unused
        assert "timedelta" in unused
        # Dict, List, Optional might be unused depending on code analysis
        assert "Path" not in unused
        assert "datetime" not in unused

    def test_find_unused_imports_alias(self):
        """Test finding unused aliased imports"""
        code = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    df = pd.DataFrame()
    # np and plt are not used
"""
        unused = find_unused_imports(code)
        assert "np" in unused  # numpy alias is unused
        assert "plt" in unused  # matplotlib alias is unused
        assert "pd" not in unused  # pandas alias is used

    def test_find_unused_imports_no_unused(self):
        """Test when all imports are used"""
        code = """
import os
import sys
from pathlib import Path

def main():
    path = Path(os.path.join(sys.path[0], "file"))
"""
        unused = find_unused_imports(code)
        assert len(unused) == 0

    def test_fix_unused_imports_removes_unused(self):
        """Test that fix_unused_imports removes unused imports"""
        code = """
import os
import sys
import json
import unused_module

def main():
    print(os.path.join(sys.path[0], "file.json"))
    data = json.loads("{}")
"""
        with patch("builtins.open", mock_open(read_data=code)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = fix_unused_imports("test.py")

        handle = mock_file.return_value.__enter__.return_value
        written_data = ''.join(call[0][0] for call in handle.write.call_args_list)

        # Check that unused_module was removed
        assert "unused_module" not in written_data
        # Check that used imports remain
        assert "import os" in written_data
        assert "import sys" in written_data
        assert "import json" in written_data

    def test_fix_unused_imports_no_changes(self):
        """Test that fix_unused_imports makes no changes when all imports are used"""
        code = """
import os
import sys
from pathlib import Path

def main():
    path = Path(os.path.join(sys.path[0], "file"))
"""

        with patch("builtins.open", mock_open(read_data=code)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = fix_unused_imports("test.py")

        # Should return False if no changes made
        handle = mock_file.return_value.__enter__.return_value
        assert not handle.write.called

    def test_fix_unused_imports_handles_from_imports(self):
        """Test fixing unused from imports"""
        code = """
from pathlib import Path
from datetime import datetime, timedelta, date
from typing import Dict, List

def main():
    path = Path("/tmp")
    now = datetime.now()
    today = date.today()
"""

        with patch("builtins.open", mock_open(read_data=code)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = fix_unused_imports("test.py")

        handle = mock_file.return_value.__enter__.return_value
        written_data = ''.join(call[0][0] for call in handle.write.call_args_list)

        # Check that timedelta was removed but others remain
        assert "timedelta" not in written_data
        assert "from datetime import datetime, date" in written_data or "from datetime import date, datetime" in written_data

    def test_fix_unused_imports_syntax_error_handling(self):
        """Test handling of files with syntax errors"""
        code = """
import os
import sys
def broken_syntax(
    # Missing closing parenthesis
"""

        with patch("builtins.open", mock_open(read_data=code)) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                # Should not crash on syntax error
                result = fix_unused_imports("test.py")
                # Should return False due to syntax error
                assert result is False

    def test_fix_unused_imports_file_error(self):
        """Test error handling when file can't be accessed"""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            result = fix_unused_imports("nonexistent.py")
            assert result is False

    @patch('lib.fix_unused_imports.Path')
    @patch('lib.fix_unused_imports.find_unused_imports')
    @patch('lib.fix_unused_imports.fix_unused_imports')
    def test_main_function(self, mock_fix, mock_find, mock_path):
        """Test main function behavior"""
        # Setup mocks
        mock_find.return_value = ["unused1", "unused2"]
        mock_fix.return_value = True
        mock_path.return_value.exists.return_value = True

        from fix_unused_imports import main
        main()

        # Should process files
        assert mock_fix.called

    def test_import_used_in_comprehension(self):
        """Test that imports used in comprehensions are detected"""
        code = """
import itertools
import math
import unused_module

def main():
    squares = [math.sqrt(x) for x in range(10)]
    pairs = itertools.product([1, 2], [3, 4])
"""
        unused = find_unused_imports(code)
        assert "unused_module" in unused
        assert "math" not in unused
        assert "itertools" not in unused

    def test_import_used_in_class_definition(self):
        """Test that imports used in class definitions are detected"""
        code = """
from dataclasses import dataclass
from typing import List
import unused_module

@dataclass
class Person:
    names: List[str]
"""
        unused = find_unused_imports(code)
        assert "unused_module" in unused
        assert "dataclass" not in unused
        assert "List" not in unused