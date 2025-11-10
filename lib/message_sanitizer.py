#!/usr/bin/env python3
"""
Message Sanitizer for Claude API Compatibility

Prevents empty text blocks from being sent to Claude API by sanitizing
message content arrays and ensuring all text blocks contain non-empty content.

This addresses the "cache_control cannot be set for empty text blocks" error.
"""

import re
from typing import List, Dict, Any, Optional

class MessageSanitizer:
    """Sanitizes message content to prevent empty text blocks."""

    @staticmethod
    def sanitize_text(text: str) -> Optional[str]:
        """
        Sanitize text content to ensure it's non-empty and meaningful.

        Args:
            text: The text to sanitize

        Returns:
            Sanitized text or None if text is empty/meaningless
        """
        if not text:
            return None

        # Convert to string and strip whitespace
        if isinstance(text, (list, dict)):
            return str(text)

        text = str(text).strip()

        # Return None if empty or only whitespace
        if not text:
            return None

        # Return None if it's only whitespace characters or empty markers
        if re.match(r'^[\s\-\_\|\.\,]*$', text):
            return None

        return text

    @staticmethod
    def sanitize_content_block(block: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Sanitize a single content block.

        Args:
            block: The content block to sanitize

        Returns:
            Sanitized block or None if block should be removed
        """
        if not isinstance(block, dict):
            return None

        # Handle text blocks
        if block.get('type') == 'text':
            text = MessageSanitizer.sanitize_text(block.get('text', ''))
            if text:
                return {
                    'type': 'text',
                    'text': text
                }
            return None

        # Keep non-text blocks as-is (tool results, etc.)
        return block

    @staticmethod
    def sanitize_message(message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize a single message to ensure no empty text blocks.

        Args:
            message: The message to sanitize

        Returns:
            Sanitized message
        """
        if not isinstance(message, dict):
            return message

        # Handle content array
        if 'content' in message and isinstance(message['content'], list):
            # Sanitize each content block
            sanitized_content = []
            for block in message['content']:
                sanitized_block = MessageSanitizer.sanitize_content_block(block)
                if sanitized_block:
                    sanitized_content.append(sanitized_block)

            # Ensure we have at least one content block
            if not sanitized_content:
                sanitized_content = [{
                    'type': 'text',
                    'text': 'Processing...'
                }]

            message['content'] = sanitized_content

        return message

    @staticmethod
    def sanitize_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sanitize a list of messages to prevent empty text blocks.

        Args:
            messages: List of messages to sanitize

        Returns:
            Sanitized messages
        """
        if not isinstance(messages, list):
            return messages

        sanitized_messages = []
        for message in messages:
            sanitized_message = MessageSanitizer.sanitize_message(message)
            if sanitized_message:
                sanitized_messages.append(sanitized_message)

        return sanitized_messages

    @staticmethod
    def safe_split(text: str, delimiter: str, maxsplit: int = -1) -> List[str]:
        """
        Safely split text and return non-empty parts.

        Args:
            text: Text to split
            delimiter: Delimiter to split on
            maxsplit: Maximum number of splits

        Returns:
            List of non-empty parts
        """
        if not text:
            return []

        parts = text.split(delimiter, maxsplit)
        return [part.strip() for part in parts if part.strip()]

    @staticmethod
    def safe_get_part(text: str, delimiter: str, index: int, default: str = '') -> str:
        """
        Safely get a part of a split text.

        Args:
            text: Text to split
            delimiter: Delimiter to split on
            index: Index of part to get
            default: Default value if part doesn't exist

        Returns:
            The requested part or default
        """
        parts = MessageSanitizer.safe_split(text, delimiter)
        if 0 <= index < len(parts):
            return parts[index]
        return default

    @staticmethod
    def validate_message_structure(messages: List[Dict[str, Any]]) -> List[str]:
        """
        Validate message structure and return list of issues.

        Args:
            messages: Messages to validate

        Returns:
            List of validation issues (empty if no issues)
        """
        issues = []

        for i, message in enumerate(messages):
            if not isinstance(message, dict):
                issues.append(f"Message {i}: Not a dictionary")
                continue

            if 'content' not in message:
                issues.append(f"Message {i}: Missing content field")
                continue

            if not isinstance(message['content'], list):
                issues.append(f"Message {i}: Content is not a list")
                continue

            for j, block in enumerate(message['content']):
                if not isinstance(block, dict):
                    issues.append(f"Message {i}, Block {j}: Not a dictionary")
                    continue

                if block.get('type') == 'text':
                    text = block.get('text', '')
                    if not text or not str(text).strip():
                        issues.append(f"Message {i}, Block {j}: Empty or whitespace-only text")
                    elif len(str(text).strip()) < 1:
                        issues.append(f"Message {i}, Block {j}: Text too short")

        return issues


# Global functions for easy import
def sanitize_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convenience function to sanitize messages."""
    return MessageSanitizer.sanitize_messages(messages)

def validate_messages(messages: List[Dict[str, Any]]) -> List[str]:
    """Convenience function to validate messages."""
    return MessageSanitizer.validate_message_structure(messages)

def safe_split(text: str, delimiter: str, maxsplit: int = -1) -> List[str]:
    """Convenience function for safe text splitting."""
    return MessageSanitizer.safe_split(text, delimiter, maxsplit)

def safe_get_part(text: str, delimiter: str, index: int, default: str = '') -> str:
    """Convenience function for safe part extraction."""
    return MessageSanitizer.safe_get_part(text, delimiter, index, default)


# Development helper for debugging
def debug_message_structure(messages: List[Dict[str, Any]]) -> None:
    """
    Debug message structure by logging details about each content block.

    Args:
        messages: Messages to debug
    """
    print("=== Message Structure Debug ===")
    for i, message in enumerate(messages):
        print(f"Message {i}:")
        if 'content' in message:
            for j, block in enumerate(message['content']):
                print(f"  Block {j}: {block.get('type', 'unknown')}")
                if block.get('type') == 'text':
                    text = block.get('text', '')
                    print(f"    Text length: {len(text)}")
                    print(f"    Text repr: {repr(text)}")
                    print(f"    Is empty: {not text or not text.strip()}")
        else:
            print("  No content field")
    print("=== End Debug ===")


if __name__ == "__main__":
    # Test the sanitizer with problematic inputs
    test_messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": ""},  # Empty text
                {"type": "text", "text": "   "},  # Whitespace only
                {"type": "text", "text": "Valid content"},
            ]
        },
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "Another valid content"},
            ]
        }
    ]

    print("Before sanitization:")
    issues = validate_messages(test_messages)
    if issues:
        for issue in issues:
            print(f"  Issue: {issue}")

    print("\nAfter sanitization:")
    sanitized = sanitize_messages(test_messages)
    issues = validate_messages(sanitized)
    if issues:
        for issue in issues:
            print(f"  Issue: {issue}")
    else:
        print("  No issues found - messages are clean!")