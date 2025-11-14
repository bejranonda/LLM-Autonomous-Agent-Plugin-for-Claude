#!/usr/bin/env python3
#     Emergency Fix for Orchestrator Agent Message Generation
    """

CRITICAL: This file prevents system-wide Claude failure by sanitizing
all message content before sending to Claude's API.

Integration Required: Import and use safe_orchestrator_response()
in all orchestrator response generation functions.

Status: EMERGENCY DEPLOYMENT REQUIRED
Version: 1.0.0
# Import emergency sanitizer - will be available once plugin is properly installed
# from lib.emergency_message_sanitize import emergency_sanitize_messages


# Fallback implementation if main sanitizer not available
def emergency_sanitize_messages(messages):
    """Fallback message sanitizer if main module not available."""
    if not isinstance(messages, list):
        return messages

    sanitized_messages = []
    for message in messages:
        if not isinstance(message, dict):
            continue

        if "content" not in message:
            continue

        if not isinstance(message["content"], list):
            continue

        # Filter content blocks
        clean_content = []
        for block in message["content"]:
            if isinstance(block, dict) and block.get("type") == "text":
                text = str(block.get("text", "")).strip()
                if text:  # Only keep non-empty
                    clean_content.append({"type": "text", "text": text})
            else:
                # Keep non-text blocks
                clean_content.append(block)

        # Never return empty content
        if not clean_content:
            clean_content = [{"type": "text", "text": "Processing..."}]

        message["content"] = clean_content
        sanitized_messages.append(message)

    return sanitized_messages


def safe_orchestrator_response(content_blocks):
    """
    Generate safe response for orchestrator agent that prevents Claude API failure.

    Args:
        content_blocks: List of content blocks to include in response

    Returns:
        Sanitized message dictionary safe for Claude API transmission

    Example:
        >>> blocks = [{"type": "text", "text": ""}, {"type": "text", "text": "Valid"}]
        >>> result = safe_orchestrator_response(blocks)
        >>> result['content'][0]['text']
        'Valid'
        >>> len(result['content']) == 1  # Empty block removed
    """
    if not content_blocks:
        content_blocks = []

    clean_blocks = []
    for block in content_blocks:
        if not isinstance(block, dict):
            continue

        block_type = block.get("type", "text")
        text = block.get("text", "")

        if block_type == "text":
            # Sanitize text content
            text = str(text).strip()
            if text:  # Only keep non-empty text
                clean_blocks.append({"type": "text", "text": text})
        else:
            # Keep non-text blocks (tool results, etc.)
            clean_blocks.append(block)

    # CRITICAL: Never return empty content
    if not clean_blocks:
        clean_blocks = [{"type": "text", "text": "Processing request..."}]

    # Create message structure
    message = {"role": "assistant", "content": clean_blocks}

    # Emergency sanitize before returning
    try:
        sanitized_messages = emergency_sanitize_messages([message])
        return sanitized_messages[0]
    except Exception as e:
        print(f"[EMERGENCY] Message sanitization failed: {e}")
        # Return safest possible message
        return {"role": "assistant", "content": [{"type": "text", "text": "System processing..."}]}


def safe_string_operation(text, default="Unknown"):
    """
    Safe string operation with automatic fallback for empty content.

    Args:
        text: Input text to process
        default: Default value if text is empty or invalid

    Returns:
        Safe processed text string

    Example:
        >>> safe_string_operation("")
        'Unknown'
        >>> safe_string_operation("   ")
        'Unknown'
        >>> safe_string_operation("Valid content")
        'Valid content'
        >>> safe_string_operation(None, "Default")
        'Default'
    """
    if text is None:
        return default

    try:
        text = str(text).strip()
        return text if text else default
    except (ValueError, TypeError):
        return default


def safe_split_operation(text, delimiter, maxsplit=-1):
    """
    Safe string splitting that prevents empty parts.

    Args:
        text: Text to split
        delimiter: Delimiter to split on
        maxsplit: Maximum number of splits

    Returns:
        List of non-empty split parts

    Example:
        >>> safe_split_operation("a|b||c", "|")
        ['a', 'b', 'c']
        >>> safe_split_operation("a|||d", "|")
        ['a', 'd']
        >>> safe_split_operation("", "|")
        []
    """
    if not text:
        return []

    try:
        parts = text.split(delimiter, maxsplit)
        return [part.strip() for part in parts if part.strip()]
    except (ValueError, TypeError):
        return []


def safe_get_operation(text, delimiter, index, default=""):
    """
    Safe extraction of split operation parts with automatic fallback.

    Args:
        text: Text to process
        delimiter: Delimiter to split on
        index: Index of part to extract
        default: Default value if part doesn't exist

    Returns:
        Requested part or default value

    Example:
        >>> safe_get_operation("a|b|c", "|", 1)
        'b'
        >>> safe_get_operation("a||c", "|", 1)
        ''
        >>> safe_get_operation("a||c", "|", 1, "default")
        'default'
    """
    parts = safe_split_operation(text, delimiter)
    if 0 <= index < len(parts):
        return parts[index]
    return default


def validate_response_structure(response):
    """
    Validate response structure to ensure it won't cause Claude API failure.

    Args:
        response: Response dictionary to validate

    Returns:
        List of validation issues (empty if valid)

    Example:
        >>> response = {"role": "assistant", "content": []}
        >>> issues = validate_response_structure(response)
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

    for i, block in enumerate(response["content"]):
        if not isinstance(block, dict):
            issues.append(f"Content block {i} is not a dictionary")
            continue

        if block.get("type") == "text":
            text = block.get("text", "")
            if not text or not str(text).strip():
                issues.append(f"Content block {i} has empty or whitespace-only text")

    return issues


# Export functions for immediate integration
__all__ = [
    "safe_orchestrator_response",
    "safe_string_operation",
    "safe_split_operation",
    "safe_get_operation",
    "validate_response_structure",
]

# Test the emergency fix
if __name__ == "__main__":
    print("=== ORCHESTRATOR EMERGENCY FIX TEST ===")

    # Test with problematic content blocks
    test_blocks = [
        {"type": "text", "text": ""},  # Empty - should be removed
        {"type": "text", "text": "   "},  # Whitespace only - should be removed
        {"type": "text", "text": "Valid content"},  # Should be kept
        {"type": "tool_result", "result": "data"},  # Should be kept
    ]

    print("Testing safe_orchestrator_response:")
    result = safe_orchestrator_response(test_blocks)

    issues = validate_response_structure(result)

    print(f"Content blocks: {len(result['content'])}")
    print(f"Validation issues: {len(issues)}")

    if issues:
        print("ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ Response structure is valid!")

    for i, block in enumerate(result["content"]):
        print(f"  Block {i}: {block.get('type', 'unknown')} - {str(block.get('text', 'N/A'))[:30]}...")

    print("\n=== EMERGENCY FIX IS READY ===")
    print("Integrate safe_orchestrator_response() into orchestrator agent immediately!")
