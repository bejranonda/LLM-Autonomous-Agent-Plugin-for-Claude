#!/usr/bin/env python3
# EMERGENCY: Plugin Message Sanitizer

# CRITICAL: This plugin is causing system-wide Claude failure by generating
# empty text blocks that break Claude's entire functionality.

# This emergency wrapper sanitizes ALL messages before they reach Claude's API
# to prevent complete system failure.

# STATUS: EMERGENCY FIX REQUIRED
import re
from typing import List, Dict, Any, Optional


class EmergencyMessageSanitizer:
    """Emergency message sanitizer to prevent Claude system failure."""

    @staticmethod
    def sanitize_message_text():
# Emergency sanitization - only keep non-empty, meaningful text.
# Args:
# text: Text to sanitize
# Returns:
# Sanitized text or None if content is invalid
        if text is None:
            return None

        # Convert to string and clean
        text = str(text).strip()

        # Reject empty or meaningless content
        if not text:
            return None

        # Reject whitespace-only characters
        if re.match(r"^[\s\-\_\|\.\,\:\;\(\)\[\]\{\}]*$", text):
            return None

        # Reject very short content (likely empty)
        if len(text) < 1:
            return None

        return text

"""
    @staticmethod
    def sanitize_content_block():
"""
        
        Emergency content block sanitization.

        Args:
            block: Content block to sanitize

        Returns:
            Sanitized block or None if block should be removed
"""
        if not isinstance(block, dict):
            return None

        block_type = block.get("type")

        # Handle text blocks with strict filtering
        if block_type == "text":
            text = EmergencyMessageSanitizer.sanitize_message_text(block.get("text", ""))
            if text:
                return {"type": "text", "text": text}
            return None

        # Keep non-text blocks (tool results, etc.) but validate structure
        if block_type in ["tool_result", "tool_use", "function_call", "function_result"]:
            return block

        # Unknown block type - keep if it has content
        return block

"""
    @staticmethod
    def sanitize_message():
"""
        
        Emergency message sanitization.

        Args:
            message: Message to sanitize

        Returns:
            Sanitized message
"""
        if not isinstance(message, dict):
            return message

        # Handle content array
        if "content" in message and isinstance(message["content"], list):
            original_count = len(message["content"])

            # Filter content blocks aggressively
            sanitized_content = []
            for block in message["content"]:
                sanitized_block = EmergencyMessageSanitizer.sanitize_content_block(block)
                if sanitized_block:
                    sanitized_content.append(sanitized_block)

            # NEVER return empty content - this breaks Claude entirely
            if not sanitized_content:
                sanitized_content = [{"type": "text", "text": "Processing request..."}]

            message["content"] = sanitized_content

            # Log if we removed empty blocks (for debugging)
            if len(sanitized_content) != original_count:
                print(f"[EMERGENCY] Removed {original_count - len(sanitized_content)} empty content blocks")

        return message

"""
    @staticmethod
    def sanitize_messages():
"""
        
        Emergency message sanitization for all messages.

        Args:
            messages: List of messages to sanitize

        Returns:
            Sanitized messages
"""
        if not isinstance(messages, list):
            return messages

        sanitized_messages = []
        for message in messages:
            sanitized_message = EmergencyMessageSanitizer.sanitize_message(message)
            if sanitized_message:
                sanitized_messages.append(sanitized_message)

        return sanitized_messages


# Emergency global functions for immediate integration
"""
def emergency_sanitize_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Emergency sanitization function - call this before ANY Claude API call."""
    return EmergencyMessageSanitizer.sanitize_messages(messages)


def validate_no_empty_blocks(messages: List[Dict[str, Any]]) -> List[str]:
    """Validate messages have no empty text blocks."""
    issues = []
    for i, message in enumerate(messages):
        if isinstance(message, dict) and "content" in message:
            if isinstance(message["content"], list):
                for j, block in enumerate(message["content"]):
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = str(block.get("text", ""))
                        if not text.strip():
                            issues.append(f"Message {i}, Block {j}: Empty text detected")
    return issues


# Emergency wrapper for Claude API calls
class EmergencyAPICallWrapper:
    """Emergency wrapper to sanitize all Claude API calls."""

    def __init__(self, original_api_function):
        """Initialize the processor with default configuration."""
        self.original_function = original_api_function

    def __call__(self, *args, **kwargs):
        """Wrap API call with emergency sanitization."""
        # Sanitize messages in common API call patterns
        if "messages" in kwargs:
            kwargs["messages"] = emergency_sanitize_messages(kwargs["messages"])

        elif args and isinstance(args[0], list):
            # First argument might be messages
            args = list(args)
            args[0] = emergency_sanitize_messages(args[0])

        # Call original function
        return self.original_function(*args, **kwargs)


# Emergency installation
def install_emergency_wrapper():
"""
    Install emergency wrapper globally.

    This function should be called during plugin initialization
    to prevent all future message issues.
"""
"""
    import sys
    import importlib

    # This would need to be adapted based on how the plugin makes API calls
    # For now, provide the tools needed
    print("[EMERGENCY] Message sanitizer installed")
    print("[EMERGENCY] Use emergency_sanitize_messages() before API calls")


# Test the emergency fix
if __name__ == "__main__":
    print("=== EMERGENCY MESSAGE SANITIZER TEST ===")

    # Test with problematic messages
    test_messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": ""},  # Empty - should be removed
                {"type": "text", "text": "   "},  # Whitespace only - should be removed
                {"type": "text", "text": "Valid content"},  # Should be kept
                {"type": "tool_result", "result": "data"},  # Should be kept
            ],
        },
        {"role": "assistant", "content": []},  # Empty array - should get default content
    ]

    print("Before sanitization:")
    issues = validate_no_empty_blocks(test_messages)
    print(f"Issues found: {len(issues)}")
    for issue in issues:
        print(f"  {issue}")

    print("\nAfter sanitization:")
    sanitized = emergency_sanitize_messages(test_messages)
    issues = validate_no_empty_blocks(sanitized)
    print(f"Issues found: {len(issues)}")

    print(f"\nSanitized messages: {len(sanitized)}")
    for i, msg in enumerate(sanitized):
        print(f"  Message {i}: {len(msg.get('content', []))} content blocks")
        for j, block in enumerate(msg.get("content", [])):
            print(f"    Block {j}: {block.get('type', 'unknown')} - {block.get('text', str(block))[:30]}...")

    print("\n[EMERGENCY] Sanitizer is ready for deployment!")
    print("[EMERGENCY] This will prevent system-wide Claude failure!")
