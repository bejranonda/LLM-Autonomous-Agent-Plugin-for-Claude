#!/usr/bin/env python3
#     ORCHESTRATOR AGENT EMERGENCY FIX PACKAGE
    """

CRITICAL: This package fixes the specific unsafe string operations in
agents/orchestrator.md that are causing system-wide Claude failure.

Integration Instructions:
1. Apply the safe_string_operations.py fixes to agents/orchestrator.md
2. Replace all unsafe parse_* functions with safe versions
3. Test with validate_orchestrator_fix.py

Status: EMERGENCY DEPLOYMENT REQUIRED
Version: 1.0.0
import re
from typing import Dict, Any, List, Optional

# ============================================================================
# SAFE STRING OPERATION LIBRARY - Replace all unsafe operations in orchestrator
# ============================================================================


def safe_split():
        """
        
        Safe string splitting that prevents empty parts and handles None values.

    Replaces: text.split(delimiter, maxsplit)

    Args:
        text: Text to split (can be None or empty)
        delimiter: Delimiter to split on
        maxsplit: Maximum number of splits

    Returns:
        List of non-empty split parts

    Example:
        >>> safe_split("a|b||c", "|")
        ['a', 'b', 'c']
        >>> safe_split("", "|")
        []
    """
    if not text:
        return []

    try:
        parts = text.split(delimiter, maxsplit)
        return [part.strip() for part in parts if part.strip()]
    except (ValueError, TypeError, AttributeError):
        return []


def safe_join():
        """
        
        Safe string joining that handles None values and empty lists.

    Replaces: separator.join(parts)

    Args:
        parts: List of parts to join (can contain None/empty values)
        separator: Separator string

    Returns:
        Safe joined string or default value

    Example:
        >>> safe_join(["a", "b", "", "c"])
        'a b c'
        >>> safe_join([])
        ''
    """
    if not parts:
        return ""

    try:
        # Filter out None and empty values, strip whitespace
        clean_parts = [str(part).strip() for part in parts if part and str(part).strip()]
        return separator.join(clean_parts)
    except (ValueError, TypeError):
        return ""


def safe_get_part():
        """
        
        Safe extraction of split operation parts with automatic fallback.

    Replaces: text.split(delimiter)[index]

    Args:
        text: Text to split
        delimiter: Delimiter to split on
        index: Index of part to extract
        default: Default value if part doesn't exist

    Returns:
        Requested part or default value

    Example:
        >>> safe_get_part("a|b|c", "|", 1)
        'b'
        >>> safe_get_part("a|", "|", 1, "default")
        'default'
    """
    parts = safe_split(text, delimiter)
    if 0 <= index < len(parts):
        return parts[index]
    return default


def safe_extract_after():
        """
        
        Safe extraction of content after a marker.

    Replaces: text.split(marker)[1].strip()

    Args:
        text: Text to extract from
        marker: Marker to split on

    Returns:
        Content after marker or empty string

    Example:
        >>> safe_extract_after("command --arg value", "--arg")
        'value'
        >>> safe_extract_after("command --arg", "--arg")
        ''
    """
    if not text or marker not in text:
        return ""

    try:
        # Use regular split to preserve empty parts that we need
        parts = text.split(marker, 1)
        if len(parts) > 1:
            return parts[1].strip()
        return ""
    except (ValueError, TypeError, AttributeError):
        return ""


def safe_extract_between():
        """
        
        Safe extraction of content between two markers.

    Replaces: text.split(start_marker)[1].split(end_marker)[0].strip()

    Args:
        text: Text to extract from
        start_marker: Starting marker
        end_marker: Ending marker

    Returns:
        Content between markers or empty string

    Example:
        >>> safe_extract_between("a --start content --end b", "--start", "--end")
        'content'
    """
    if not text or start_marker not in text or end_marker not in text:
        return ""

    after_start = safe_extract_after(text, start_marker)
    if end_marker in after_start:
        parts = safe_split(after_start, end_marker, 1)
        if parts:
            return parts[0].strip()
    return after_start


# ============================================================================
# SAFE COMMAND PARSING FUNCTIONS - Replace unsafe versions in orchestrator
# ============================================================================


def safe_parse_dashboard_args(user_input: str) -> Dict[str, Any]:
    """Safe version of parse_dashboard_args - prevents empty text blocks."""
    args = {"host": "localhost", "port": 5000, "patterns_dir": ".claude-patterns", "auto_open_browser": True}

    if not user_input:
        return args

    cmd = str(user_input).strip()
    if not cmd:
        return args

    # Safe extraction with fallbacks - use proper extraction logic
    if "--host" in cmd:
        host_value = safe_extract_after(cmd, "--host")
        # Extract just the first word after --host
        host_parts = safe_split(host_value, " ", 1)
        args["host"] = host_parts[0] if host_parts else "localhost"

    if "--port" in cmd:
        port_value = safe_extract_after(cmd, "--port")
        port_parts = safe_split(port_value, " ", 1)
        port_str = port_parts[0] if port_parts else "5000"
        try:
            args["port"] = int(port_str) if port_str.isdigit() else 5000
        except (ValueError, TypeError):
            args["port"] = 5000

    if "--patterns-dir" in cmd:
        patterns_value = safe_extract_after(cmd, "--patterns-dir")
        patterns_parts = safe_split(patterns_value, " ", 1)
        args["patterns_dir"] = patterns_parts[0] if patterns_parts else ".claude-patterns"

    if "--no-browser" in cmd:
        args["auto_open_browser"] = False

    return args


def safe_parse_queue_add_args(user_input: str) -> Dict[str, Any]:
    """Safe version of queue add argument parsing."""
    args = {"name": "", "description": "", "command": "", "priority": "medium"}

    if not user_input:
        return args

    cmd = str(user_input).strip()
    if not cmd:
        return args

    # Safe argument extraction with non-empty defaults
    if "--name" in cmd:
        name = safe_extract_between(cmd, "--name", "--description")
        if not name and "--description" not in cmd:
            name = safe_extract_after(cmd, "--name")
        args["name"] = name or "Untitled Task"

    if "--description" in cmd:
        desc = safe_extract_between(cmd, "--description", "--command")
        if not desc and "--command" not in cmd:
            desc = safe_extract_after(cmd, "--description")
        args["description"] = desc or "No description provided"

    if "--command" in cmd:
        cmd_part = safe_extract_between(cmd, "--command", "--priority")
        if not cmd_part and "--priority" not in cmd:
            cmd_part = safe_extract_after(cmd, "--command")
        args["command"] = cmd_part or "No command specified"

    if "--priority" in cmd:
        priority = safe_get_part(cmd, "--priority", 1, "medium")
        args["priority"] = priority if priority in ["low", "medium", "high"] else "medium"

    return args


def safe_parse_preference_args(user_input: str) -> Dict[str, Any]:
    """Safe version of preference argument parsing."""
    args = {"key": "", "value": "", "export": False, "list": False}

    if not user_input:
        return args

    cmd = str(user_input).strip()
    if not cmd:
        return args

    # Safe extraction with defaults
    if "--key" in cmd:
        key = safe_extract_between(cmd, "--key", "--value")
        if not key and "--value" not in cmd:
            key = safe_extract_after(cmd, "--key")
        args["key"] = key or "unknown_preference"

    if "--value" in cmd:
        args["value"] = safe_extract_after(cmd, "--value") or "default_value"

    if "--export" in cmd:
        args["export"] = True

    if "--list" in cmd:
        args["list"] = True

    return args


def safe_extract_remaining_args():
        """
        
        Safe extraction of remaining arguments after a specific index.

    Replaces: ' '.join(cmd.split()[idx + 1:])

    Args:
        text: Command text
        start_index: Index to start from

    Returns:
        Remaining arguments or default value

    Example:
        >>> safe_extract_remaining_args("cmd arg1 arg2 arg3", 1)
        'arg1 arg2 arg3'
        >>> safe_extract_remaining_args("cmd", 1)
        ''
    """
    if not text:
        return ""

    try:
        parts = safe_split(text, " ")
        if start_index < len(parts):
            remaining_parts = parts[start_index:]
            return safe_join(remaining_parts, " ")
        return ""
    except (ValueError, TypeError, IndexError):
        return ""


# ============================================================================
# CONTENT GENERATION SAFETY FUNCTIONS
# ============================================================================


def safe_content_section():
        """
        
        Generate safe content section that won't create empty text blocks.

    Args:
        title: Section title
        content: Section content

    Returns:
        Safe content block or None if content is empty

    Example:
        >>> block = safe_content_section("Title", "Content")
        >>> block['text']
        '## Title\\n\\nContent'
        >>> safe_content_section("Empty", "")
        None
    """
    if not title:
        return None

    # Convert and clean content
    content_str = str(content).strip() if content is not None else ""
    if not content_str:
        return None

    return {"type": "text", "text": f"## {title.strip()}\n\n{content_str}"}


def safe_multi_section_content():
        """
        
        Generate safe multi-section content with no empty blocks.

    Args:
        sections: List of (title, content) tuples

    Returns:
        List of safe content blocks

    Example:
        >>> sections = [("Title", "Content"), ("Empty", "")]
        >>> blocks = safe_multi_section_content(sections)
        >>> len(blocks)
        1
    """
    content_blocks = []

    for title, content in sections:
        block = safe_content_section(title, content)
        if block:
            content_blocks.append(block)

    # Ensure we never return empty content
    if not content_blocks:
        content_blocks = [{"type": "text", "text": "Processing request..."}]

    return content_blocks


# ============================================================================
# ORCHESTRATOR INTEGRATION UTILITIES
# ============================================================================


def validate_orchestrator_response():
        """
        
        Validate orchestrator response to prevent system-wide failure.

    Args:
        response: Response dictionary to validate

    Returns:
        List of validation issues (empty if valid)

    Example:
        >>> response = {"role": "assistant", "content": [{"type": "text", "text": ""}]}
        >>> issues = validate_orchestrator_response(response)
        >>> len(issues) > 0
        True
    """
    issues = []

    if not isinstance(response, dict):
        issues.append("Response is not a dictionary")
        return issues

    if "content" not in response:
        issues.append("Missing content field in response")
        return issues

    if not isinstance(response["content"], list):
        issues.append("Content is not a list")
        return issues

    if not response["content"]:
        issues.append("Content array is empty")
        return issues

    for i, block in enumerate(response["content"]):
        if not isinstance(block, dict):
            issues.append(f"Content block {i} is not a dictionary")
            continue

        if block.get("type") == "text":
            text = block.get("text", "")
            if not text or not str(text).strip():
                issues.append(f"Content block {i} has empty or whitespace-only text")

    return issues


def sanitize_orchestrator_response():
        """
        
        Sanitize orchestrator response to prevent empty text blocks.

    Args:
        response: Response dictionary to sanitize

    Returns:
        Sanitized response safe for Claude API

    Example:
        >>> response = {"role": "assistant", "content": [{"type": "text", "text": ""}]}
        >>> sanitized = sanitize_orchestrator_response(response)
        >>> len(sanitized['content'])
        1
        >>> sanitized['content'][0]['text']
        'Processing request...'
    """
    if not isinstance(response, dict):
        return response

    if "content" not in response or not isinstance(response["content"], list):
        return response

    # Filter out empty text blocks
    clean_content = []
    for block in response["content"]:
        if isinstance(block, dict) and block.get("type") == "text":
            text = str(block.get("text", "")).strip()
            if text:
                clean_content.append({"type": "text", "text": text})
        else:
            # Keep non-text blocks
            clean_content.append(block)

    # Never return empty content
    if not clean_content:
        clean_content = [{"type": "text", "text": "Processing request..."}]

    response["content"] = clean_content
    return response


# ============================================================================
# INTEGRATION HELPERS
# ============================================================================


def get_orchestrator_replacement_patterns():
    """
    Get the specific patterns that need to be replaced in agents/orchestrator.md

    Returns:
        Dictionary of unsafe patterns and their safe replacements
    """
    return {
        # Unsafe split operations that need replacement
        "parts = user_input.split('--host')[1].strip().split()": "parts = safe_split(user_input, '--host', 1)",
        "remaining = ' '.join(cmd.split()[idx + 1:])": "remaining = safe_extract_remaining_args(cmd, idx + 1)",
        # Unsafe argument assignments that need defaults
        "args['host'] = parts[0]": "args['host'] = safe_get_part(user_input, '--host', 1, 'localhost')",
        "args['name'] = remaining": "args['name'] = remaining or 'Unknown'",
        # Unsafe content generation
        "content_blocks.append({'type': 'text', 'text': f\"## {title}\\n\\n{content}\"})": "block = safe_content_section(title, content); if block: content_blocks.append(block)",
    }


def create_orchestrator_integration_instructions():
    """
    Create step-by-step instructions for integrating fixes into agents/orchestrator.md

    Returns:
        String containing integration instructions
    """
    return """
# ORCHESTRATOR AGENT EMERGENCY INTEGRATION INSTRUCTIONS

## Step 1: Add Import Statement
Add this to the top of agents/orchestrator.md after the YAML frontmatter:

```python
# Emergency message sanitization - prevents system-wide Claude failure
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.orchestrator_emergency_fix import (
    safe_split, safe_join, safe_get_part, safe_extract_after,
    safe_parse_dashboard_args, safe_parse_queue_add_args,
    safe_content_section, safe_multi_section_content,
    sanitize_orchestrator_response
)
```

## Step 2: Replace Unsafe Functions
Replace these functions in agents/orchestrator.md:

### Replace parse_dashboard_args() (lines ~938-961):
```python
def parse_dashboard_args(user_input):
    """Parse Dashboard Args."""
    \"\"\"Safe dashboard argument parsing - prevents empty text blocks.\"\"\"
    return safe_parse_dashboard_args(user_input or "")
```

### Replace queue argument parsing (lines ~1201-1227):
```python
def parse_queue_add_args(user_input):
    """Parse Queue Add Args."""
    \"\"\"Safe queue add argument parsing - prevents empty text blocks.\"\"\"
    return safe_parse_queue_add_args(user_input or "")
```

## Step 3: Update Response Generation
Add this before any function that returns message content:

```python
# CRITICAL: Sanitize response before returning to prevent system failure
response = sanitize_orchestrator_response(response)
```

## Step 4: Test Integration
Run this to verify fixes work:

```bash
python lib/orchestrator_emergency_fix.py
```

Expected output:
- [EMERGENCY] Sanitizer is ready for deployment!
- All validation tests should pass
# Export key functions for immediate use
__all__ = [
    "safe_split",
    "safe_join",
    "safe_get_part",
    "safe_extract_after",
    "safe_extract_between",
    "safe_parse_dashboard_args",
    "safe_parse_queue_add_args",
    "safe_parse_preference_args",
    "safe_extract_remaining_args",
    "safe_content_section",
    "safe_multi_section_content",
    "validate_orchestrator_response",
    "sanitize_orchestrator_response",
    "get_orchestrator_replacement_patterns",
    "create_orchestrator_integration_instructions",
]

# ============================================================================
# SELF-TEST: Validate emergency fixes work correctly
# ============================================================================

if __name__ == "__main__":
    print("=== ORCHESTRATOR AGENT EMERGENCY FIX TEST ===")

    # Test safe string operations
    print("\n1. Testing safe string operations:")

    # Test safe_split
    result = safe_split("a|b||c", "|")
    assert result == ["a", "b", "c"], f"Expected ['a', 'b', 'c'], got {result}"
    print("   [OK] safe_split works correctly")

    # Test safe_get_part
    result = safe_get_part("a|b|c", "|", 1, "default")
    assert result == "b", f"Expected 'b', got {result}"

    result = safe_get_part("a|", "|", 1, "default")
    assert result == "default", f"Expected 'default', got {result}"
    print("   [OK] safe_get_part works correctly")

    # Test safe_parse_dashboard_args
    print("\n2. Testing safe argument parsing:")

    args = safe_parse_dashboard_args("--host example.com --port 8080")
    assert args["host"] == "example.com", f"Expected 'example.com', got {args['host']}"
    assert args["port"] == 8080, f"Expected 8080, got {args['port']}"
    print("   [OK] safe_parse_dashboard_args works correctly")

    args = safe_parse_dashboard_args("")  # Empty input
    assert args["host"] == "localhost", f"Expected 'localhost', got {args['host']}"
    print("   [OK] safe_parse_dashboard_args handles empty input")

    # Test safe_parse_queue_add_args
    args = safe_parse_queue_add_args("--name Test --description A test task")
    assert args["name"] == "Test", f"Expected 'Test', got {args['name']}"
    assert args["description"] == "A test task", f"Expected 'A test task', got {args['description']}"
    print("   [OK] safe_parse_queue_add_args works correctly")

    # Test content generation
    print("\n3. Testing safe content generation:")

    block = safe_content_section("Title", "Content")
    assert block is not None, "Expected non-None block"
    assert "Title" in block["text"], "Expected title in block text"
    print("   [OK] safe_content_section works correctly")

    block = safe_content_section("Empty", "")
    assert block is None, "Expected None for empty content"
    print("   [OK] safe_content_section handles empty content")

    # Test response validation
    print("\n4. Testing response validation:")

    # Valid response
    valid_response = {"role": "assistant", "content": [{"type": "text", "text": "Valid content"}]}
    issues = validate_orchestrator_response(valid_response)
    assert len(issues) == 0, f"Expected no issues, got {len(issues)}"
    print("   [OK] Response validation works for valid responses")

    # Invalid response (empty text block)
    invalid_response = {"role": "assistant", "content": [{"type": "text", "text": ""}]}
    issues = validate_orchestrator_response(invalid_response)
    assert len(issues) > 0, "Expected issues for empty text block"
    print("   [OK] Response validation detects empty text blocks")

    # Test response sanitization
    print("\n5. Testing response sanitization:")

    sanitized = sanitize_orchestrator_response(invalid_response)
    assert len(sanitized["content"]) == 1, "Expected one content block"
    assert (
        sanitized["content"][0]["text"] == "Processing request..."
    ), f"Expected default text, got {sanitized['content'][0]['text']}"
    print("   [OK] Response sanitization fixes empty text blocks")

    print("\n=== ALL ORCHESTRATOR FIXES VALIDATED ===")
    print("[OK] Emergency fixes are ready for integration")
    print("[OK] Safe operations prevent empty text blocks")
    print("[OK] Response sanitization prevents system-wide failure")

    # Show integration instructions
    print("\n" + "=" * 60)
    print("INTEGRATION INSTRUCTIONS:")
    print("=" * 60)
    print(create_orchestrator_integration_instructions())
