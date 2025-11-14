#!
# /*/usr/bin/env python3
# //Learning Engine - Token-Efficient Implementation
# */
# //
# //    This script provides efficient file operations and data management
    """

for the learning-engine agent. The agent handles AI reasoning while
this script handles file I/O, JSON operations, and data management.


# /*
U
*/sage (called by learning-engine agent):
    python learning_engine.py init --project-context '{"type": "python", "frameworks": ["fastapi"]}'
    python learning_engine.py capture --pattern '{"type": "function", "name": "auth"}'
    python learning_engine.py status --dir .claude-patterns
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class LearningEngine:
    """Efficient learning engine for file operations and data management"""

    def __init__(self, data_dir: str = ".claude-patterns"):
"""Initialize learning engine with data directory and create required files."""
self.data_dir = Path(data_dir)
self.data_dir.mkdir(parents=True, exist_ok=True)

# Data files
self.patterns_file = self.data_dir / "patterns.json"
self.quality_history_file = self.data_dir / "quality_history.json"
self.task_queue_file = self.data_dir / "task_queue.json"
self.config_file = self.data_dir / "config.json"

# Initialize files if they don't exist
self._initialize_default_files()

    def _initialize_default_files(self):
"""Initialize default files with basic structure if they don't exist"""
# Initialize patterns.json with basic structure
if not self.patterns_file.exists():
    patterns_data = {
        "project_context": {},
        "patterns": [],
        "skill_effectiveness": {},
        "agent_performance": {},
        "learning_metrics": {
            "total_patterns": 0,
            "last_updated": datetime.now().isoformat(),
            "initialization_timestamp": datetime.now().isoformat(),
        },
    }
    with open(self.patterns_file, "w") as f:
        json.dump(patterns_data, f, indent=2)

# Initialize quality_history.json
if not self.quality_history_file.exists():
    quality_data = []
    with open(self.quality_history_file, "w") as f:
        json.dump(quality_data, f, indent=2)

# Initialize task_queue.json
if not self.task_queue_file.exists():
    task_data = {
        "queue": [],
        "completed": [],
        "failed": [],
        "status": "ready",
        "created_at": datetime.now().isoformat(),
    }
    with open(self.task_queue_file, "w") as f:
        json.dump(task_data, f, indent=2)

# Initialize config.json with defaults
if not self.config_file.exists():
    config_data = {
        "version": "1.0.0",
        "auto_capture": True,
        "learning_enabled": True,
        "retention_days": 30,
        "created_at": datetime.now().isoformat(),
        "project_context": {},
    }
    with open(self.config_file, "w") as f:
        json.dump(config_data, f, indent=2)

    def initialize_learning_system(self, project_context: Dict[str, Any] = None) -> Dict[str, Any]:
"""Initialize learning system with project context"""
# Use default context if not provided
if project_context is None:
    project_context = {
        "type": "unknown",
        "frameworks": [],
        "detected_at": datetime.now().isoformat()
    }

results = {
    "status": "initialized",
    "timestamp": datetime.now().isoformat(),
    "files_created": [],
    "project_context": project_context,
}

# Initialize patterns.json with project context
if not self.patterns_file.exists():
    patterns_data = {
        "project_context": project_context,
        "patterns": [],
        "skill_effectiveness": {},
        "agent_performance": {},
        "learning_metrics": {
            "total_patterns": 0,
            "last_updated": datetime.now().isoformat(),
            "initialization_timestamp": datetime.now().isoformat(),
        },
    }
    with open(self.patterns_file, "w") as f:
        json.dump(patterns_data, f, indent=2)
    results["files_created"].append("patterns.json")
else:
    # Update existing patterns file with new project context
    with open(self.patterns_file, "r+") as f:
        patterns_data = json.load(f)
        patterns_data["project_context"] = project_context
        f.seek(0)
        json.dump(patterns_data, f, indent=2)
        f.truncate()

# Initialize quality_history.json
if not self.quality_history_file.exists():
    quality_data = []
    with open(self.quality_history_file, "w") as f:
        json.dump(quality_data, f, indent=2)
    results["files_created"].append("quality_history.json")

# Initialize task_queue.json
if not self.task_queue_file.exists():
    task_data = {
        "queue": [],
        "completed": [],
        "failed": [],
        "status": "ready",
        "created_at": datetime.now().isoformat(),
    }
    with open(self.task_queue_file, "w") as f:
        json.dump(task_data, f, indent=2)
    results["files_created"].append("task_queue.json")

# Initialize config.json with defaults
if not self.config_file.exists():
    config_data = {
        "version": "1.0.0",
        "auto_capture": True,
        "learning_enabled": True,
        "retention_days": 30,
        "created_at": datetime.now().isoformat(),
        "project_context": project_context,
    }
    with open(self.config_file, "w") as f:
        json.dump(config_data, f, indent=2)
    results["files_created"].append("config.json")

return results

    def capture_pattern(self, pattern_data: Dict[str, Any]) -> Dict[str, Any]:
"""Efficiently capture a learning pattern"""
try:
    # Load existing patterns
    if self.patterns_file.exists():
        try:
            with open(self.patterns_file, "r") as f:
                patterns_data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            # File is corrupted, create new structure
            patterns_data = {
                "patterns": [],
                "project_context": {},
                "skill_effectiveness": {},
                "agent_performance": {},
                "learning_metrics": {
                    "total_patterns": 0,
                    "last_updated": datetime.now().isoformat(),
                }
            }
    else:
        patterns_data = {
            "patterns": [],
            "project_context": {},
            "skill_effectiveness": {},
            "agent_performance": {},
            "learning_metrics": {
                "total_patterns": 0,
                "last_updated": datetime.now().isoformat(),
            }
        }

    # Add new pattern with metadata
    new_pattern = {
        "id": len(patterns_data.get("patterns", [])) + 1,
        "timestamp": datetime.now().isoformat(),
        "pattern": pattern_data,
        "captured_by": "learning_engine",
        "processed": True,
    }

    patterns_data.setdefault("patterns", []).append(new_pattern)
    patterns_data["learning_metrics"]["total_patterns"] = len(patterns_data["patterns"])
    patterns_data["learning_metrics"]["last_updated"] = datetime.now().isoformat()

    # Save efficiently
    with open(self.patterns_file, "w") as f:
        json.dump(patterns_data, f, indent=2)

    return {
        "status": "success",
        "pattern_id": new_pattern["id"],
        "total_patterns": patterns_data["learning_metrics"]["total_patterns"],
        "message": "Pattern captured successfully",
    }
except Exception as e:
    return {"status": "error", "error": str(e), "message": "Failed to capture pattern"}

    def get_status(self) -> Dict[str, Any]:
"""Get comprehensive learning system status"""
try:
    status = {
        "timestamp": datetime.now().isoformat(),
        "data_directory": str(self.data_dir),
        "system_status": "operational",
    }

    # Check files
    status["files"] = {
        "patterns.json": self.patterns_file.exists(),
        "quality_history.json": self.quality_history_file.exists(),
        "task_queue.json": self.task_queue_file.exists(),
        "config.json": self.config_file.exists(),
    }

    # Load analytics efficiently
    if self.patterns_file.exists():
        with open(self.patterns_file, "r") as f:
            patterns_data = json.load(f)
        status["analytics"] = {
            "total_patterns": len(patterns_data.get("patterns", [])),
            "project_context": patterns_data.get("project_context", {}),
            "learning_metrics": patterns_data.get("learning_metrics", {}),
            "last_updated": patterns_data.get("learning_metrics", {}).get("last_updated"),
        }
    else:
        status["analytics"] = {"total_patterns": 0}

    if self.quality_history_file.exists():
        with open(self.quality_history_file, "r") as f:
            quality_data = json.load(f)
        # Only add quality_assessments to analytics if there are actual assessments
        if quality_data:
            status["analytics"]["quality_assessments"] = len(quality_data)
            status["analytics"]["latest_quality_score"] = quality_data[-1].get("quality_score", 0)

    return status
except Exception as e:
    return {"status": "error", "error": str(e), "message": "Failed to get status"}

    def add_quality_assessment(self, quality_data: Dict[str, Any]) -> Dict[str, Any]:
"""Add quality assessment to history"""
try:
    # Load existing quality history
    if self.quality_history_file.exists():
        with open(self.quality_history_file, "r") as f:
            history = json.load(f)
    else:
        history = []

    # Add new assessment with timestamp
    new_assessment = {"timestamp": datetime.now().isoformat(), **quality_data}
    history.append(new_assessment)

    # Save (with optional cleanup for old entries)
    with open(self.quality_history_file, "w") as f:
        json.dump(history, f, indent=2)

    return {
        "status": "success",
        "total_assessments": len(history),
        "latest_score": quality_data.get("quality_score", 0),
    }
except Exception as e:
    return {"status": "error", "error": str(e), "message": "Failed to add quality assessment"}


def main():
    """Main execution function - CLI interface for learning-engine agent"""
    parser = argparse.ArgumentParser(description="Learning Engine - Token-Efficient Operations")
    parser.add_argument("command", choices=["init", "capture", "status", "add-quality"], help="Command to execute")
    parser.add_argument("--data-dir", default=".claude-patterns", help="Data directory path")
    parser.add_argument("--project-context", help="Project context (JSON string)")
    parser.add_argument("--pattern", help="Pattern data (JSON string)")
    parser.add_argument("--quality-data", help="Quality assessment data (JSON string)")

    args = parser.parse_args()

    # Initialize learning engine
    engine = LearningEngine(args.data_dir)

    try:
if args.command == "init":
    if not args.project_context:
        # Default context if not provided
        project_context = {"type": "unknown", "frameworks": [], "detected_at": datetime.now().isoformat()}
    else:
        project_context = json.loads(args.project_context)

    result = engine.initialize_learning_system(project_context)
    print(json.dumps(result, indent=2))

elif args.command == "capture":
    if not args.pattern:
        result = {"status": "error", "message": "Pattern data required"}
    else:
        pattern_data = json.loads(args.pattern)
        result = engine.capture_pattern(pattern_data)
    print(json.dumps(result, indent=2))

elif args.command == "status":
    result = engine.get_status()
    print(json.dumps(result, indent=2))

elif args.command == "add-quality":
    if not args.quality_data:
        result = {"status": "error", "message": "Quality data required"}
    else:
        quality_data = json.loads(args.quality_data)
        result = engine.add_quality_assessment(quality_data)
    print(json.dumps(result, indent=2))

    except Exception as e:
error_result = {"status": "error", "error": str(e), "command": args.command, "timestamp": datetime.now().isoformat()}
print(json.dumps(error_result, indent=2))
import sys
sys.exit(1)


if __name__ == "__main__":
    main()
