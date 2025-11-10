#!/usr/bin/env python3
"""
Quick Fix for Claude API Empty Text Blocks Issue

This is a temporary fix that can be applied immediately to resolve
the "cache_control cannot be set for empty text blocks" error.
"""

def sanitize_claude_messages(messages):
    """
    Quick fix function to sanitize Claude API messages.
    This removes empty text blocks that cause API errors.

    Args:
        messages: List of message dictionaries

    Returns:
        Sanitized messages with no empty text blocks
    """
    if not messages:
        return messages

    sanitized = []

    for message in messages:
        if not isinstance(message, dict):
            continue

        if 'content' not in message:
            sanitized.append(message)
            continue

        content = message['content']
        if not isinstance(content, list):
            sanitized.append(message)
            continue

        # Filter out empty text blocks
        clean_content = []
        for block in content:
            if not isinstance(block, dict):
                continue

            # Keep non-text blocks as-is
            if block.get('type') != 'text':
                clean_content.append(block)
                continue

            # For text blocks, only keep if they have actual content
            text = block.get('text', '')
            if text and str(text).strip():
                clean_content.append({
                    'type': 'text',
                    'text': str(text).strip()
                })

        # Ensure we have at least one content block
        if not clean_content:
            clean_content = [{
                'type': 'text',
                'text': 'Processing...'
            }]

        message['content'] = clean_content
        sanitized.append(message)

    return sanitized

def apply_fix_to_all_commands():
    """
    Apply the fix to all commands that might be affected.

    This function can be imported and called in command handlers
    to automatically sanitize their responses.
    """
    # This is a placeholder for where the fix would be applied
    # In the actual plugin, this would be integrated into:
    # 1. Command response generation
    # 2. Agent delegation responses
    # 3. Tool result processing
    pass

# Example usage in command handlers:
"""
def example_command_response():
    # Generate your response content as usual
    content_blocks = [
        {"type": "text", "text": "Header"},
        {"type": "text", "text": ""},  # This would cause error
        {"type": "text", "text": "Content"}
    ]

    # Apply the fix before returning
    message = {"role": "assistant", "content": content_blocks}
    sanitized_message = sanitize_claude_messages([message])[0]

    return sanitized_message
"""

# Safe string operations to prevent empty content
def safe_split(text, delimiter, maxsplit=-1):
    """Safely split text and return non-empty parts."""
    if not text:
        return []
    parts = text.split(delimiter, maxsplit)
    return [part.strip() for part in parts if part.strip()]

def safe_get_part(text, delimiter, index, default=''):
    """Safely get a part of split text."""
    parts = safe_split(text, delimiter)
    if 0 <= index < len(parts):
        return parts[index]
    return default

if __name__ == "__main__":
    # Test the fix
    test_messages = [
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": ""},
                {"type": "text", "text": "   "},
                {"type": "text", "text": "Valid content"},
            ]
        }
    ]

    print("Before fix:")
    print(f"Content blocks: {len(test_messages[0]['content'])}")

    sanitized = sanitize_claude_messages(test_messages)

    print("\nAfter fix:")
    print(f"Content blocks: {len(sanitized[0]['content'])}")
    for i, block in enumerate(sanitized[0]['content']):
        print(f"  Block {i}: {block.get('text', repr(block))[:30]}...")

    print(f"\n[OK] Fix applied successfully!")