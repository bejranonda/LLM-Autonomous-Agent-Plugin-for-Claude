#!/usr/bin/python3
# Emergency Fix for Command Response Generation

# CRITICAL: Prevents cache_control errors in command responses
# Integration: Replace all command response formatting functions

# Status: EMERGENCY DEPLOYMENT REQUIRED
# Version: 1.0.0
# Import emergency fix
try:
    from lib.orchestrator_emergency_fix import emergency_sanitize_messages
except ImportError:
    # Fallback implementation if not available
    def emergency_sanitize_messages(messages):
        """Fallback emergency sanitizer."""
        if not isinstance(messages, list):
            return messages

        sanitized = []
        for msg in messages:
            if isinstance(msg, dict) and "content" in msg and isinstance(msg["content"], list):
                clean_content = []
                for block in msg["content"]:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = str(block.get("text", "")).strip()
                        if text:
                            clean_content.append({"type": "text", "text": text})
                    else:
                        clean_content.append(block)

                if not clean_content:
                    clean_content = [{"type": "text", "text": "Processing..."}]
                msg["content"] = clean_content
            sanitized.append(msg)
        return sanitized


def safe_command_response(title, sections=None, sections_dict=None):
"""
    Generate safe command response that prevents Claude API failure.

    Args:
        title: Response title string
        sections: Dictionary mapping section titles to content (alternative to sections_dict)
        sections_dict: Dictionary mapping section titles to content (alternative to sections)

    Returns:
        Sanitized Claude message dictionary

    Example:
        >>> response = safe_command_response("Title", {"Section": "Content"})
        >>> 'content' in response
        True
        >>> len(response['content']) == 1
        >>> 'text' in response['content'][0]
        True
"""
    # Handle both parameter formats
    if sections_dict is not None:
        sections = sections_dict

    content_blocks = []

    # Add title if provided
    if title and str(title).strip():
        content_blocks.append({"type": "text", "text": str(title).strip()})

    # Add sections
    if sections and isinstance(sections, dict):
        for section_title, section_content in sections.items():
            content = str(section_content).strip()
            if content:  # Only add non-empty sections
                content_blocks.append({"type": "text", "text": f"\n## {str(section_title).strip()}\n\n{content}"})

    # Ensure content exists
    if not content_blocks:
        content_blocks = [{"type": "text", "text": title or "Processing request..."}]

    # Create message
    message = {"role": "assistant", "content": content_blocks}

    # Emergency sanitize before returning
    try:
        sanitized_messages = emergency_sanitize_messages([message])
        return sanitized_messages[0]
    except Exception as e:
        print(f"[EMERGENCY] Command response sanitization failed: {e}")
        return {"role": "assistant", "content": [{"type": "text", "text": str(title) or "Processing..."}]}


"""
def safe_multi_section_response(titles, content_list):
"""
    Generate safe multi-section response with multiple titles and content.

    Args:
        titles: List of section titles
        content_list: List of section content

    Returns:
        Sanitized Claude message dictionary

    Example:
        >>> response = safe_multi_section_response(["A", "B"], ["Content A", "Content B"])
        >>> len(response['content']) == 2
"""
    if not titles or not content_list:
        return safe_command_response("Processing...")

    min_length = min(len(titles), len(content_list))
    content_blocks = []

    for i in range(min_length):
        title = str(titles[i]).strip()
        content = str(content_list[i]).strip()

        block_text = f"## {title}"
        if content:
            block_text += f"\n\n{content}"

        if block_text.strip():
            content_blocks.append({"type": "text", "text": block_text})

    # Ensure content exists
    if not content_blocks:
        content_blocks = [{"type": "text", "text": "Processing..."}]

    message = {"role": "assistant", "content": content_blocks}

    try:
        sanitized_messages = emergency_sanitize_messages([message])
        return sanitized_messages[0]
    except Exception as e:
        print(f"[EMERGENCY] Multi-section response sanitization failed: {e}")
        return {"role": "assistant", "content": [{"type": "text", "text": "Processing..."}]}


"""
def safe_table_response(title, headers, rows):
"""
    Generate safe table response that prevents Claude API failure.

    Args:
        title: Table title
        headers: List of column headers
        rows: List of rows (each row is a list of column values)

    Returns:
        Sanitized Claude message dictionary
"""
    content_blocks = []

    # Add title
    if title and str(title).strip():
        content_blocks.append({"type": "text", "text": str(title).strip()})

    # Create table
    if headers and rows:
        table_lines = []

        # Header row
        header_line = " | ".join(str(h) for h in headers)
        separator_line = " | ".join("-" * len(str(h)) for h in headers)

        table_lines.append(header_line)
        table_lines.append(separator_line)

        # Data rows
        for row in rows:
            if row and any(str(cell).strip() for cell in row):
                row_line = " | ".join(str(cell) if cell is not None else "" for cell in row)
                table_lines.append(row_line)

        if table_lines:
            content_blocks.append({"type": "text", "text": "\n" + "\n".join(table_lines)})

    # Ensure content exists
    if not content_blocks:
        content_blocks = [{"type": "text", "text": title or "No data available"}]

    message = {"role": "assistant", "content": content_blocks}

    try:
        sanitized_messages = emergency_sanitize_messages([message])
        return sanitized_messages[0]
    except Exception as e:
        print(f"[EMERGENCY] Table response sanitization failed: {e}")
        return {"role": "assistant", "content": [{"type": "text", "text": title or "Table data unavailable"}]}


"""
def safe_list_response(title, items, item_format="• {item}"):
"""
    Generate safe list/bullet point response.

    Args:
        title: List title
        items: List of items to include
        item_format: Format string for each item (use {item} as placeholder)

    Returns:
        Sanitized Claude message dictionary
"""
    content_blocks = []

    # Add title
    if title and str(title).strip():
        content_blocks.append({"type": "text", "text": str(title).strip()})

    # Add list items
    if items:
        valid_items = [str(item).strip() for item in items if str(item).strip()]
        if valid_items:
            list_content = "\n".join(item_format.format(item=item) for item in valid_items)
            content_blocks.append({"type": "text", "text": f"\n{list_content}"})

    # Ensure content exists
    if not content_blocks:
        content_blocks = [{"type": "text", "text": title or "No items available"}]

    message = {"role": "assistant", "content": content_blocks}

    try:
        sanitized_messages = emergency_sanitize_messages([message])
        return sanitized_messages[0]
    except Exception as e:
        print(f"[EMERGENCY] List response sanitization failed: {e}")
        return {"role": "assistant", "content": [{"type": "text", "text": title or "No items available"}]}


"""
def safe_code_response(title, code_blocks, language="python"):
"""
    Generate safe code block response.

    Args:
        title: Code block title
        code_blocks: List of code snippets
        language: Programming language for syntax highlighting

    Returns:
        Sanitized Claude message dictionary
"""
    content_blocks = []

    # Add title
    if title and str(title).strip():
        content_blocks.append({"type": "text", "text": str(title).strip()})

    # Add code blocks
    if code_blocks:
        for code in code_blocks:
            if code and str(code).strip():
                content_blocks.append({"type": "text", "text": f"\n```{language}\n{str(code)}\n```"})

    # Ensure content exists
    if not content_blocks:
        content_blocks = [{"type": "text", "text": title or "No code available"}]

    message = {"role": "assistant", "content": content_blocks}

    try:
        sanitized_messages = emergency_sanitize_messages([message])
        return sanitized_messages[0]
    except Exception as e:
        print(f"[EMERGENCY] Code response sanitization failed: {e}")
        return {"role": "assistant", "content": [{"type": "text", "text": title or "Code unavailable"}]}


# Export functions for immediate integration
__all__ = [
    "safe_command_response",
    "safe_multi_section_response",
    "safe_table_response",
    "safe_list_response",
    "safe_code_response",
]

# Test the command response fix
if __name__ == "__main__":
    print("=== COMMAND RESPONSE EMERGENCY FIX TEST ===")

    # Test with empty content
    response = safe_command_response("Test Title", {"Empty Section": "", "Valid Section": "Content here"})

    print("Testing safe_command_response:")
    print(f"Content blocks: {len(response['content'])}")
    print(f"Has content: {bool(response['content'])}")

    for i, block in enumerate(response["content"]):
        if block.get("type") == "text":
            text = block.get("text", "")[:50]
            print(f"  Block {i}: {repr(text)}...")

    print("\n=== COMMAND RESPONSE FIX IS READY ===")
    print("Integrate safe_command_response() into all command handlers!")
