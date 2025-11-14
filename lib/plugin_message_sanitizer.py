#!/usr/bin/env python3
# PLUGIN MESSAGE SANITIZER - Entry Point for Emergency Fixes

#     This module provides the main entry point for integrating emergency fixes
    """

into the plugin system. It applies sanitization to all message generation
to prevent system-wide Claude failure.

Usage:
    from lib.plugin_message_sanitizer import sanitize_plugin_message

    # Apply to any message before sending to Claude API
    safe_message = sanitize_plugin_message(message)

Status: READY FOR DEPLOYMENT
Version: 1.0.0
import sys
import os
from typing import Dict, Any, List, Optional

# Add lib directory to path for imports
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

try:
    from emergency_message_sanitize import emergency_sanitize_messages
    from orchestrator_agent_emergency_fix import sanitize_orchestrator_response
    from slash_commands_emergency_fix import safe_format_command_response

    EMERGENCY_FIXES_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Emergency fixes not available: {e}")
    EMERGENCY_FIXES_AVAILABLE = False


def sanitize_plugin_message():
        """
        
        Main entry point for sanitizing plugin messages.

    This function should be called before ANY message is sent to Claude's API
    to prevent empty text blocks that cause system-wide failure.

    Args:
        message: Message dictionary to sanitize

    Returns:
        Sanitized message dictionary safe for Claude API

    Example:
        >>> message = {"role": "assistant", "content": [{"type": "text", "text": ""}]}
        >>> safe_message = sanitize_plugin_message(message)
        >>> len(safe_message["content"]) == 1
        True
        >>> safe_message["content"][0]["text"] != ""
        True
    """
    if not EMERGENCY_FIXES_AVAILABLE:
        # Fallback - return message unchanged if fixes not available
        return message

    if not isinstance(message, dict):
        return message

    try:
        # Apply emergency message sanitization
        sanitized_messages = emergency_sanitize_messages([message])
        return sanitized_messages[0] if sanitized_messages else message
    except Exception as e:
        print(f"[WARNING] Message sanitization failed: {e}")
        # Return original message if sanitization fails
        return message


def sanitize_plugin_messages():
        """
        
        Sanitize multiple plugin messages.

    Args:
        messages: List of message dictionaries to sanitize

    Returns:
        List of sanitized message dictionaries
    """
    if not EMERGENCY_FIXES_AVAILABLE:
        return messages

    try:
        return emergency_sanitize_messages(messages)
    except Exception as e:
        print(f"[WARNING] Message list sanitization failed: {e}")
        return messages


def create_safe_command_response():
        """
        
        Create safe command response using emergency fixes.

    Args:
        command_name: Name of the command (e.g., '/learn:init')
        results: Command results dictionary

    Returns:
        Safe Claude message dictionary
    """
    if not EMERGENCY_FIXES_AVAILABLE:
        # Fallback response
        return {"role": "assistant", "content": [{"type": "text", "text": f"{command_name} completed"}]}

    try:
        return safe_format_command_response(command_name, results)
    except Exception as e:
        print(f"[WARNING] Safe command response failed: {e}")
        return {"role": "assistant", "content": [{"type": "text", "text": f"{command_name} completed with warnings"}]}


def validate_message_safety():
        """
        
        Validate that a message is safe for Claude API.

    Args:
        message: Message dictionary to validate

    Returns:
        List of safety issues (empty if safe)
    """
    issues = []

    if not isinstance(message, dict):
        issues.append("Message is not a dictionary")
        return issues

    if "content" not in message:
        issues.append("Missing content field")
        return issues

    if not isinstance(message["content"], list):
        issues.append("Content is not a list")
        return issues

    if not message["content"]:
        issues.append("Content array is empty")
        return issues

    for i, block in enumerate(message["content"]):
        if not isinstance(block, dict):
            issues.append(f"Content block {i} is not a dictionary")
            continue

        if block.get("type") == "text":
            text = block.get("text", "")
            if not text or not str(text).strip():
                issues.append(f"Content block {i} has empty or whitespace-only text")

    return issues


# Export main functions
__all__ = [
    "sanitize_plugin_message",
    "sanitize_plugin_messages",
    "create_safe_command_response",
    "validate_message_safety",
    "EMERGENCY_FIXES_AVAILABLE",
]

# Self-test
if __name__ == "__main__":
    print("=== PLUGIN MESSAGE SANITIZER TEST ===")

    # Test 1: Basic message sanitization
    test_message = {
        "role": "assistant",
        "content": [
            {"type": "text", "text": ""},  # Empty block - should be fixed
            {"type": "text", "text": "Valid content"},  # Should be kept
        ],
    }

    safe_message = sanitize_plugin_message(test_message)
    issues = validate_message_safety(safe_message)

    print(f"Original message: {len(test_message['content'])} content blocks")
    print(f"Sanitized message: {len(safe_message['content'])} content blocks")
    print(f"Safety issues: {len(issues)}")

    if len(issues) == 0:
        print("[OK] Message sanitization working correctly")
    else:
        print("[FAIL] Message sanitization failed:")
        for issue in issues:
            print(f"  - {issue}")

    # Test 2: Command response generation
    test_results = {"score": 100, "issues": [], "status": "success"}

    command_response = create_safe_command_response("/learn:init", test_results)
    cmd_issues = validate_message_safety(command_response)

    print(f"\nCommand response: {len(command_response['content'])} content blocks")
    print(f"Command safety issues: {len(cmd_issues)}")

    if len(cmd_issues) == 0:
        print("[OK] Command response generation working correctly")
    else:
        print("[FAIL] Command response generation failed:")
        for issue in cmd_issues:
            print(f"  - {issue}")

    print(f"\nEmergency fixes available: {EMERGENCY_FIXES_AVAILABLE}")
    print("\n=== PLUGIN MESSAGE SANITIZER READY ===")
