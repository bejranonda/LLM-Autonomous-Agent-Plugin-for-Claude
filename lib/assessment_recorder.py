#!/usr/bin/env python3
"""
Assessment Recorder - Unified Storage Integration Module

Provides simple interface for commands to record their execution as assessments
in the unified parameter storage system.

Usage:
    from assessment_recorder import record_assessment

    record_assessment(
        task_type="documentation",
        description="Updated README to v5.4.0",
        overall_score=95,
        skills_used=["documentation-best-practices", "pattern-learning"],
        details={"files_modified": ["README.md"]}
    )

Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib
import platform


def get_current_model() -> str:
    """
    Detect the current AI model being used.

    Priority:
    1. Environment variable MODEL_NAME
    2. Session file .claude-patterns/current_session.json
    3. Default to Claude Sonnet 4.5
    """
    import os

    # Check environment variable
    model = os.getenv('MODEL_NAME') or os.getenv('ANTHROPIC_MODEL')
    if model:
        return model

    # Check session file
    try:
        session_file = Path(".claude-patterns/current_session.json")
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
                model = session_data.get("current_model")
                if model:
                    return model
    except:
        pass

    # Default
    return "Claude Sonnet 4.5"


def generate_assessment_id(task_type: str) -> str:
    """Generate unique assessment ID."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{task_type}-{timestamp}"


def record_assessment(
    task_type: str,
    description: str,
    overall_score: int,
    skills_used: List[str],
    details: Optional[Dict[str, Any]] = None,
    breakdown: Optional[Dict[str, int]] = None,
    issues_found: Optional[List[str]] = None,
    recommendations: Optional[List[str]] = None,
    duration_seconds: Optional[int] = None,
    task_complexity: str = "medium",
    files_modified: Optional[List[str]] = None
) -> bool:
    """
    Record an assessment to unified parameter storage.

    Args:
        task_type: Type of task (e.g., "documentation", "development", "analysis")
        description: Human-readable task description
        overall_score: Quality score 0-100
        skills_used: List of skills employed
        details: Additional task-specific details
        breakdown: Score breakdown by category (optional)
        issues_found: List of issues identified (optional)
        recommendations: List of recommendations (optional)
        duration_seconds: Task duration in seconds (optional)
        task_complexity: low/medium/high (default: medium)
        files_modified: List of files modified (optional)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load unified parameters
        unified_file = Path(".claude-unified/unified_parameters.json")

        if not unified_file.exists():
            print(f"Warning: Unified storage not found at {unified_file}", file=sys.stderr)
            return False

        with open(unified_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Build assessment object
        assessment = {
            "assessment_id": generate_assessment_id(task_type),
            "timestamp": datetime.now().isoformat(),
            "overall_score": overall_score,
            "pass": overall_score >= 70,
            "task_type": task_type,
            "breakdown": breakdown or {},
            "details": {
                "duration_seconds": duration_seconds or 0,
                "model_used": get_current_model(),
                "task_complexity": task_complexity,
                "issues_found": len(issues_found) if issues_found else 0,
                "fixes_applied": 0,
                "skills_used": skills_used,
                "task_description": description
            },
            "issues_found": issues_found or [],
            "recommendations": recommendations or [],
            "skills_used": skills_used
        }

        # Add optional fields
        if files_modified:
            assessment["details"]["files_modified"] = files_modified

        # Merge additional details
        if details:
            assessment["details"].update(details)

        # Add to history
        if "quality" not in data:
            data["quality"] = {"assessments": {"history": []}}
        if "assessments" not in data["quality"]:
            data["quality"]["assessments"] = {"history": []}
        if "history" not in data["quality"]["assessments"]:
            data["quality"]["assessments"]["history"] = []

        data["quality"]["assessments"]["history"].append(assessment)

        # Update metadata
        data["metadata"]["last_updated"] = datetime.now().isoformat()

        # Write back
        with open(unified_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[Assessment Recorded] {task_type}: {description} (score: {overall_score})", file=sys.stderr)
        return True

    except Exception as e:
        print(f"Error recording assessment: {e}", file=sys.stderr)
        return False


def record_command_execution(
    command_name: str,
    args: Optional[Dict[str, Any]] = None,
    result: Optional[Dict[str, Any]] = None,
    success: bool = True,
    duration_seconds: Optional[int] = None
) -> bool:
    """
    Simplified wrapper for recording command executions.

    Args:
        command_name: Name of command executed (e.g., "/dev:commit")
        args: Command arguments
        result: Command result/output
        success: Whether command succeeded
        duration_seconds: Execution time

    Returns:
        True if successful
    """
    # Infer task type from command name
    task_type_map = {
        "commit": "development",
        "release": "release",
        "pr-review": "code-review",
        "update-readme": "documentation",
        "update-about": "documentation",
        "auto": "autonomous-development",
        "quality": "quality-control",
        "project": "project-analysis",
        "static": "static-analysis",
        "dependencies": "dependency-scan",
        "fullstack": "fullstack-validation",
        "dashboard": "monitoring"
    }

    # Extract task type
    task_type = "general"
    for key, value in task_type_map.items():
        if key in command_name.lower():
            task_type = value
            break

    # Calculate score based on success
    score = 90 if success else 50

    # Build description
    description = f"Executed {command_name}"
    if args:
        description += f" with args: {args}"

    # Record
    return record_assessment(
        task_type=task_type,
        description=description,
        overall_score=score,
        skills_used=["automation", "command-execution"],
        duration_seconds=duration_seconds,
        details={
            "command": command_name,
            "arguments": args or {},
            "result_summary": result or {},
            "success": success
        }
    )


# Convenience functions for common task types
def record_documentation_task(description: str, files_modified: List[str], score: int = 90):
    """Record documentation update."""
    return record_assessment(
        task_type="documentation",
        description=description,
        overall_score=score,
        skills_used=["documentation-best-practices", "pattern-learning"],
        files_modified=files_modified,
        breakdown={
            "accuracy": 30,
            "completeness": 25,
            "clarity": 20,
            "formatting": 15,
            "updates": 10
        }
    )


def record_development_task(description: str, files_modified: List[str], score: int = 90):
    """Record development work."""
    return record_assessment(
        task_type="development",
        description=description,
        overall_score=score,
        skills_used=["code-analysis", "pattern-learning", "quality-standards"],
        files_modified=files_modified,
        breakdown={
            "functionality": 30,
            "code_quality": 25,
            "testing": 20,
            "documentation": 15,
            "maintainability": 10
        }
    )


def record_git_commit(commit_hash: str, message: str, files: List[str], score: int = 93):
    """Record git commit operation."""
    return record_assessment(
        task_type="development",
        description=f"Git commit: {message[:100]}",
        overall_score=score,
        skills_used=["git-automation", "pattern-learning"],
        files_modified=files,
        details={
            "commit_hash": commit_hash,
            "commit_message": message,
            "files_committed": files,
            "commit_type": "conventional"
        },
        breakdown={
            "commit_quality": 30,
            "message_clarity": 25,
            "file_staging": 20,
            "best_practices": 15,
            "documentation": 8
        }
    )


if __name__ == "__main__":
    # Test recording
    print("Testing assessment recorder...")

    success = record_assessment(
        task_type="test",
        description="Test assessment recording",
        overall_score=95,
        skills_used=["testing", "quality-assurance"],
        details={"test_mode": True}
    )

    if success:
        print("Success! Assessment recorded to unified storage.")
    else:
        print("Failed to record assessment.")
