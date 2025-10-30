#!/usr/bin/env python3
"""
Learning Engine Script

This script provides the main learning engine functionality that can be called
by various commands and agents. It handles pattern capture, learning analytics,
and the core learning system operations.

Usage:
    python learning_engine.py init         # Initialize learning system
    python learning_engine.py capture      # Capture patterns from current context
    python learning_engine.py analytics    # Show learning analytics
    python learning_engine.py status       # Show learning system status
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class LearningEngine:
    """Main learning engine class"""

    def __init__(self, data_dir: str = ".claude-patterns"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Data files
        self.patterns_file = self.data_dir / "patterns.json"
        self.quality_history_file = self.data_dir / "quality_history.json"
        self.task_queue_file = self.data_dir / "task_queue.json"
        self.config_file = self.data_dir / "config.json"

    def initialize(self) -> Dict[str, Any]:
        """Initialize the learning system"""
        results = {
            "status": "initialized",
            "timestamp": datetime.now().isoformat(),
            "files_created": []
        }

        # Initialize patterns.json
        if not self.patterns_file.exists():
            patterns_data = {
                "project_context": {
                    "detected_languages": [],
                    "frameworks": [],
                    "project_type": "unknown",
                    "initialized_at": datetime.now().isoformat()
                },
                "patterns": [],
                "skill_effectiveness": {},
                "agent_performance": {},
                "learning_metrics": {
                    "total_patterns": 0,
                    "last_updated": datetime.now().isoformat()
                }
            }
            with open(self.patterns_file, 'w') as f:
                json.dump(patterns_data, f, indent=2)
            results["files_created"].append("patterns.json")

        # Initialize quality_history.json
        if not self.quality_history_file.exists():
            quality_data = []
            with open(self.quality_history_file, 'w') as f:
                json.dump(quality_data, f, indent=2)
            results["files_created"].append("quality_history.json")

        # Initialize task_queue.json
        if not self.task_queue_file.exists():
            task_data = {
                "queue": [],
                "completed": [],
                "failed": [],
                "status": "ready"
            }
            with open(self.task_queue_file, 'w') as f:
                json.dump(task_data, f, indent=2)
            results["files_created"].append("task_queue.json")

        # Initialize config.json
        if not self.config_file.exists():
            config_data = {
                "version": "1.0.0",
                "auto_capture": True,
                "learning_enabled": True,
                "retention_days": 30,
                "created_at": datetime.now().isoformat()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            results["files_created"].append("config.json")

        return results

    def capture_pattern(self, pattern_data: Dict[str, Any]) -> Dict[str, Any]:
        """Capture a learning pattern"""
        try:
            # Load existing patterns
            if self.patterns_file.exists():
                with open(self.patterns_file, 'r') as f:
                    patterns_data = json.load(f)
            else:
                patterns_data = {"patterns": [], "project_context": {}, "skill_effectiveness": {}}

            # Add new pattern
            new_pattern = {
                "id": len(patterns_data.get("patterns", [])) + 1,
                "timestamp": datetime.now().isoformat(),
                "pattern": pattern_data,
                "captured_by": "learning_engine"
            }

            patterns_data.setdefault("patterns", []).append(new_pattern)

            # Save updated patterns
            with open(self.patterns_file, 'w') as f:
                json.dump(patterns_data, f, indent=2)

            return {
                "status": "success",
                "pattern_id": new_pattern["id"],
                "message": "Pattern captured successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Failed to capture pattern"
            }

    def get_analytics(self) -> Dict[str, Any]:
        """Get learning analytics"""
        try:
            analytics = {
                "timestamp": datetime.now().isoformat(),
                "learning_status": "active"
            }

            # Load patterns data
            if self.patterns_file.exists():
                with open(self.patterns_file, 'r') as f:
                    patterns_data = json.load(f)
                analytics["total_patterns"] = len(patterns_data.get("patterns", []))
                analytics["project_context"] = patterns_data.get("project_context", {})
                analytics["skill_effectiveness"] = patterns_data.get("skill_effectiveness", {})
            else:
                analytics["total_patterns"] = 0
                analytics["project_context"] = {}
                analytics["skill_effectiveness"] = {}

            # Load quality history
            if self.quality_history_file.exists():
                with open(self.quality_history_file, 'r') as f:
                    quality_data = json.load(f)
                analytics["quality_assessments"] = len(quality_data)
                if quality_data:
                    latest_quality = quality_data[-1]
                    analytics["latest_quality_score"] = latest_quality.get("quality_score", 0)
                else:
                    analytics["latest_quality_score"] = 0
            else:
                analytics["quality_assessments"] = 0
                analytics["latest_quality_score"] = 0

            return analytics
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Failed to get analytics"
            }

    def get_status(self) -> Dict[str, Any]:
        """Get learning system status"""
        try:
            status = {
                "timestamp": datetime.now().isoformat(),
                "data_directory": str(self.data_dir),
                "system_status": "operational"
            }

            # Check file existence
            status["files"] = {
                "patterns.json": self.patterns_file.exists(),
                "quality_history.json": self.quality_history_file.exists(),
                "task_queue.json": self.task_queue_file.exists(),
                "config.json": self.config_file.exists()
            }

            # Get analytics summary
            analytics = self.get_analytics()
            status["analytics"] = {
                "total_patterns": analytics.get("total_patterns", 0),
                "quality_assessments": analytics.get("quality_assessments", 0),
                "latest_quality_score": analytics.get("latest_quality_score", 0)
            }

            return status
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Failed to get status"
            }


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Learning Engine Script')
    parser.add_argument('command', choices=['init', 'capture', 'analytics', 'status'],
                       help='Command to execute')
    parser.add_argument('--data-dir', default='.claude-patterns',
                       help='Data directory path')
    parser.add_argument('--pattern', help='Pattern data (JSON string) for capture command')

    args = parser.parse_args()

    # Initialize learning engine
    engine = LearningEngine(args.data_dir)

    try:
        if args.command == 'init':
            result = engine.initialize()
            print(f"Learning system initialized successfully")
            print(f"Files created: {', '.join(result['files_created'])}")

        elif args.command == 'capture':
            if not args.pattern:
                # Default pattern for current context
                pattern_data = {
                    "type": "manual_capture",
                    "context": "Command line execution",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                pattern_data = json.loads(args.pattern)

            result = engine.capture_pattern(pattern_data)
            if result["status"] == "success":
                print(f"Pattern captured successfully (ID: {result['pattern_id']})")
            else:
                print(f"Error: {result['message']}")
                sys.exit(1)

        elif args.command == 'analytics':
            result = engine.get_analytics()
            if result.get("status") != "error":
                print(f"Learning Analytics Summary:")
                print(f"  Total Patterns: {result.get('total_patterns', 0)}")
                print(f"  Quality Assessments: {result.get('quality_assessments', 0)}")
                print(f"  Latest Quality Score: {result.get('latest_quality_score', 0)}")
                print(f"  Learning Status: {result.get('learning_status', 'unknown')}")
            else:
                print(f"Error getting analytics: {result.get('error')}")
                sys.exit(1)

        elif args.command == 'status':
            result = engine.get_status()
            if result.get("status") != "error":
                print(f"Learning Engine Status: {result['system_status']}")
                print(f"  Data Directory: {result['data_directory']}")
                print(f"  Files Present: {sum(result['files'].values())}/4")
                print(f"  Total Patterns: {result['analytics']['total_patterns']}")
                print(f"  Quality Assessments: {result['analytics']['quality_assessments']}")
            else:
                print(f"Error getting status: {result.get('error')}")
                sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()