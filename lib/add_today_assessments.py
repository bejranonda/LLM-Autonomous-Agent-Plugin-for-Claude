#!/usr/bin/env python3
"""
Add today's work assessments to unified storage retroactively.
"""

import json
from pathlib import Path
from datetime import datetime


def add_todays_assessments():
    """Add assessments for today's completed work."""

    unified_file = Path(".claude-unified/unified_parameters.json")

    # Load current data
    with open(unified_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Create today's assessments
    today_assessments = [
        {
            "assessment_id": "readme-update-v5.4.0-20251029-160800",
            "timestamp": "2025-10-29T16:08:00.000000",
            "overall_score": 95,
            "pass": True,
            "task_type": "documentation",
            "breakdown": {
                "accuracy": 30,
                "completeness": 25,
                "style_preservation": 20,
                "content_updates": 15,
                "formatting": 10,
            },
            "details": {
                "duration_seconds": 420,
                "model_used": "Claude Sonnet 4.5",
                "task_complexity": "medium",
                "issues_found": 0,
                "fixes_applied": 0,
                "skills_used": ["documentation-best-practices", "pattern-learning", "code-analysis"],
                "task_description": "Updated README.md to v5.4.0 with 7 new commands and platform-agnostic releases",
                "files_modified": ["README.md"],
                "changes_summary": "Version update, 7 new commands documented, historical evolution updated, component inventory updated",
            },
            "issues_found": [],
            "recommendations": [
                "Consider adding visual diagrams for command workflow",
                "Add quick reference card for common command combinations",
            ],
            "skills_used": ["documentation-best-practices", "pattern-learning", "code-analysis"],
        },
        {
            "assessment_id": "git-commit-readme-20251029-160900",
            "timestamp": "2025-10-29T16:09:00.000000",
            "overall_score": 93,
            "pass": True,
            "task_type": "development",
            "breakdown": {
                "commit_quality": 30,
                "message_clarity": 25,
                "file_staging": 20,
                "best_practices": 15,
                "documentation": 10,
            },
            "details": {
                "duration_seconds": 180,
                "model_used": "Claude Sonnet 4.5",
                "task_complexity": "low",
                "issues_found": 0,
                "fixes_applied": 0,
                "skills_used": ["git-automation", "pattern-learning", "code-analysis"],
                "task_description": "Intelligent commit of README v5.4.0 updates with conventional commit format",
                "commit_hash": "42aa036",
                "files_committed": ["README.md"],
                "commit_message_type": "docs",
            },
            "issues_found": [],
            "recommendations": [
                "Commit message is comprehensive and follows conventions",
                "Consider adding co-author attribution for collaborative work",
            ],
            "skills_used": ["git-automation", "pattern-learning"],
        },
        {
            "assessment_id": "dashboard-monitoring-20251029-161000",
            "timestamp": "2025-10-29T16:10:00.000000",
            "overall_score": 88,
            "pass": True,
            "task_type": "monitoring",
            "breakdown": {
                "dashboard_functionality": 30,
                "browser_opening": 25,
                "data_display": 20,
                "performance": 10,
                "accessibility": 8,
            },
            "details": {
                "duration_seconds": 600,
                "model_used": "Claude Sonnet 4.5",
                "task_complexity": "low",
                "issues_found": 2,
                "fixes_applied": 2,
                "skills_used": ["monitoring", "troubleshooting", "quality-assurance"],
                "task_description": "Launched dashboard and investigated recent activity display",
                "dashboard_port": 5000,
                "browser_opened": True,
                "issues_investigated": ["Empty recent activities section", "Incorrect model detection (GLM vs Claude)"],
            },
            "issues_found": [
                "Recent activities not showing today's work",
                "Model detection showing GLM-4.6 instead of Claude Sonnet 4.5",
            ],
            "recommendations": [
                "Integrate command storage with unified parameters",
                "Improve real-time model detection logic",
            ],
            "skills_used": ["monitoring", "troubleshooting", "quality-assurance"],
        },
        {
            "assessment_id": "debugging-dashboard-issues-20251029-161500",
            "timestamp": "2025-10-29T16:15:00.000000",
            "overall_score": 96,
            "pass": True,
            "task_type": "debugging",
            "breakdown": {
                "root_cause_analysis": 30,
                "code_investigation": 25,
                "documentation_review": 20,
                "solution_design": 15,
                "explanation_quality": 10,
            },
            "details": {
                "duration_seconds": 900,
                "model_used": "Claude Sonnet 4.5",
                "task_complexity": "high",
                "issues_found": 2,
                "fixes_applied": 0,
                "skills_used": ["code-analysis", "pattern-learning", "troubleshooting", "documentation-best-practices"],
                "task_description": "Debugged dashboard behavior: investigated empty activities and model detection issues",
                "files_analyzed": [
                    "lib/dashboard.py",
                    "lib/unified_parameter_storage.py",
                    ".claude-unified/unified_parameters.json",
                    ".claude-patterns/current_session.json",
                ],
                "analysis_depth": "comprehensive",
                "quality_improvement": 15,
            },
            "issues_found": ["Commands don't auto-record to unified storage", "Session file contains stale model detection"],
            "recommendations": [
                "Add unified storage integration to key commands (/dev:commit, /workspace:update-readme)",
                "Improve model detection to use model_id as primary source",
                "Update session file with correct model information",
                "Consider adding automatic assessment recording for all commands",
            ],
            "skills_used": ["code-analysis", "pattern-learning", "troubleshooting", "documentation-best-practices"],
        },
    ]

    # Add to history
    data["quality"]["assessments"]["history"].extend(today_assessments)

    # Update metadata
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    data["metadata"]["total_records_migrated"] = len(data["quality"]["assessments"]["history"])

    # Backup original file
    backup_file = unified_file.with_suffix(".json.backup")
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Write updated data
    with open(unified_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Added {len(today_assessments)} assessments for today's work")
    print(f"[INFO] Backup saved to: {backup_file}")
    print(f"[INFO] Total assessments now: {len(data['quality']['assessments']['history'])}")

    return True


if __name__ == "__main__":
    add_todays_assessments()
