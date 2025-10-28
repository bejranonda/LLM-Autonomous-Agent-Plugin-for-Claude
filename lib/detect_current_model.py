#!/usr/bin/env python3
"""
Automatic Model Detection for Claude Code Dashboard

Detects the current model being used by analyzing:
1. Environment variables set by Claude Code
2. Process information and command-line arguments
3. System context and API indicators
4. Fallback to asking the AI directly via a marker file

This ensures the dashboard always shows the correct current model.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


def detect_model_from_env() -> tuple[str, str]:
    """
    Detect model from environment variables.

    Returns:
        Tuple of (model_name, detection_method)
    """
    # Check for Claude Code specific environment variables
    env_vars = {
        'ANTHROPIC_MODEL': 'env_anthropic_model',
        'CLAUDE_MODEL': 'env_claude_model',
        'MODEL_NAME': 'env_model_name',
        'AI_MODEL': 'env_ai_model',
    }

    for var, method in env_vars.items():
        value = os.getenv(var)
        if value:
            return (value, method)

    return (None, None)


def detect_model_from_process() -> tuple[str, str]:
    """
    Detect model from process information.

    Returns:
        Tuple of (model_name, detection_method)
    """
    try:
        import psutil

        # Get current process and parent processes
        current_process = psutil.Process()
        parent = current_process.parent()

        if parent:
            # Check command line arguments
            cmdline = ' '.join(parent.cmdline()).lower()

            # Look for Claude Code indicators
            if 'claude' in cmdline:
                if 'sonnet' in cmdline:
                    if '4.5' in cmdline or '4-5' in cmdline:
                        return ('Claude Sonnet 4.5', 'process_cmdline')
                    return ('Claude Sonnet 3.5', 'process_cmdline')
                if 'opus' in cmdline:
                    return ('Claude Opus 3', 'process_cmdline')
                if 'haiku' in cmdline:
                    return ('Claude Haiku 3', 'process_cmdline')
                return ('Claude', 'process_cmdline')

            # Look for GLM indicators
            if 'glm' in cmdline or 'zhipu' in cmdline:
                if '4.6' in cmdline or '4-6' in cmdline:
                    return ('GLM 4.6', 'process_cmdline')
                return ('GLM', 'process_cmdline')
    except:
        pass

    return (None, None)


def detect_model_from_marker() -> tuple[str, str]:
    """
    Detect model from marker file that can be manually updated.

    Returns:
        Tuple of (model_name, detection_method)
    """
    marker_file = Path('.claude-patterns/model_marker.txt')
    if marker_file.exists():
        try:
            content = marker_file.read_text().strip()
            if content:
                return (content, 'marker_file')
        except:
            pass

    return (None, None)


def get_default_model() -> str:
    """Get default model based on platform indicators."""
    # Check platform node name for indicators
    import platform
    node = platform.node().lower()

    if any(indicator in node for indicator in ['glm', 'zhipu']):
        return 'GLM 4.6'

    # Default to Claude Sonnet 4.5 (most common)
    return 'Claude Sonnet 4.5'


def detect_current_model() -> dict:
    """
    Detect the current model using multiple methods.

    Returns:
        Dict with model information
    """
    # Try detection methods in order of reliability
    detection_methods = [
        detect_model_from_marker,
        detect_model_from_env,
        detect_model_from_process,
    ]

    for method in detection_methods:
        model, detection_method = method()
        if model:
            return {
                'current_model': model,
                'detection_method': detection_method,
                'confidence': 'high',
                'timestamp': datetime.now().isoformat()
            }

    # Fallback to default
    return {
        'current_model': get_default_model(),
        'detection_method': 'default_fallback',
        'confidence': 'low',
        'timestamp': datetime.now().isoformat()
    }


def update_session_file(patterns_dir: str = '.claude-patterns'):
    """
    Update the current session file with detected model.

    Args:
        patterns_dir: Directory containing pattern data
    """
    patterns_path = Path(patterns_dir)
    patterns_path.mkdir(exist_ok=True)

    # Detect current model
    model_info = detect_current_model()

    # Read existing session file if it exists
    session_file = patterns_path / 'current_session.json'
    session_data = {}
    if session_file.exists():
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
        except:
            pass

    # Update with detected model
    session_data.update({
        'current_model': model_info['current_model'],
        'last_activity': datetime.now().isoformat(),
        'detection_method': model_info['detection_method'],
        'confidence': model_info['confidence'],
        'auto_detected': True
    })

    # Ensure required fields exist
    if 'session_start' not in session_data:
        session_data['session_start'] = datetime.now().isoformat()

    # Write updated session file
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, indent=2, ensure_ascii=False)

    return model_info


def create_marker_file(model_name: str, patterns_dir: str = '.claude-patterns'):
    """
    Create a marker file to manually specify the current model.

    Args:
        model_name: Name of the model to set
        patterns_dir: Directory containing pattern data
    """
    patterns_path = Path(patterns_dir)
    patterns_path.mkdir(exist_ok=True)

    marker_file = patterns_path / 'model_marker.txt'
    marker_file.write_text(model_name)

    print(f"[OK] Model marker set to: {model_name}")
    print(f"     Marker file: {marker_file}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Detect and set current AI model')
    parser.add_argument('--set', type=str, help='Manually set the current model')
    parser.add_argument('--dir', type=str, default='.claude-patterns',
                       help='Pattern directory (default: .claude-patterns)')
    parser.add_argument('--detect', action='store_true',
                       help='Detect and display current model')

    args = parser.parse_args()

    if args.set:
        # Manually set model
        create_marker_file(args.set, args.dir)
        update_session_file(args.dir)
    elif args.detect:
        # Detect and display
        model_info = detect_current_model()
        print(f"Current Model: {model_info['current_model']}")
        print(f"Detection Method: {model_info['detection_method']}")
        print(f"Confidence: {model_info['confidence']}")
    else:
        # Update session file automatically
        model_info = update_session_file(args.dir)
        print(f"[OK] Session updated with model: {model_info['current_model']}")
        print(f"     Detection: {model_info['detection_method']} ({model_info['confidence']} confidence)")
