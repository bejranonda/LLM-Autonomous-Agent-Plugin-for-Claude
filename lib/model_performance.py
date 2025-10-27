#!/usr/bin/env python3
"""
Model Performance Data Manager for Autonomous Agent Dashboard

Manages historical performance data for different AI models.
Provides utilities to add performance data, generate reports, and
    maintain data integrity.

Version: 1.0.0
Author: Autonomous Agent Development Team
"""

import json
import argparse
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
import statistics

# Handle Windows compatibility for file locking
if platform.system() == 'Windows':
    import msvcrt

    def lock_file(f, exclusive=False):
        """Windows file locking using msvcrt."""
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        """Windows file unlocking."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl

    def lock_file(f, exclusive=False):
        """Unix file locking using fcntl."""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)

    def unlock_file(f):
        """Unix file unlocking."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class ModelPerformanceManager:
    """Manages model performance data storage and analysis."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """
        Initialize model performance manager.

        Args:
            patterns_dir: Directory path for storing model performance data
        """
        self.patterns_dir = Path(patterns_dir)
        self.model_file = self.patterns_dir / "model_performance.json"
        self._ensure_directory()

    def _ensure_directory(self):
        """Create patterns directory if it doesn't exist."""
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        if not self.model_file.exists():
            self._initialize_default_data()

    def _initialize_default_data(self):
        """Initialize with default model data structure."""
        default_models = ["Claude", "OpenAI", "GLM", "Gemini"]
        initial_data = {}

        for model in default_models:
            initial_data[model] = {
                "recent_scores": [],
                "total_tasks": 0,
                "success_rate": 0.0,
                "contribution_to_project": 0.0,
                "first_seen": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }

        self._save_data(initial_data)

    def _load_data(self) -> Dict[str, Any]:
        """Load model performance data from file."""
        try:
            with open(self.model_file, 'r', encoding='utf-8') as f:
                lock_file(f, exclusive=False)
                try:
                    content = f.read()
                    if not content.strip():
                        return {}
                    return json.loads(content)
                finally:
                    unlock_file(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: Malformed JSON in {self.model_file}: {e}", file=sys.stderr)
            return {}
        except Exception as e:
            print(f"Error reading model performance data: {e}", file=sys.stderr)
            return {}

    def _save_data(self, data: Dict[str, Any]):
        """Save model performance data to file."""
        try:
            with open(self.model_file, 'w', encoding='utf-8') as f:
                lock_file(f, exclusive=True)
                try:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error writing model performance data: {e}", file=sys.stderr)
            raise

    def add_performance_score(
    self,
    model: str,
    score: float,
    task_type: str = "unknown",
    contribution: float = 0.0):,


)
        """
        Add a new performance score for a model.

        Args:
            model: Model name (Claude, OpenAI, GLM, Gemini)
            score: Performance score (0-100)
            task_type: Type of task performed
            contribution: Contribution to project (0-100)
        """
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")

        data = self._load_data()

        if model not in data:
            data[model] = {
                "recent_scores": [],
                "total_tasks": 0,
                "success_rate": 0.0,
                "contribution_to_project": 0.0,
                "first_seen": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }

        # Add the new score
        data[model]["recent_scores"].append({
            "score": round(score, 1),
            "timestamp": datetime.now().isoformat(),
            "task_type": task_type,
            "contribution": round(contribution, 1)
        })

        # Keep only the last 100 scores to prevent file bloat
        if len(data[model]["recent_scores"]) > 100:
            data[model]["recent_scores"] = data[model]["recent_scores"][-100:]

        # Update metrics
        data[model]["total_tasks"] += 1
        data[model]["last_updated"] = datetime.now().isoformat()

        # Calculate success rate (scores >= 70 are considered successful)
        successful_tasks = sum(1 for s in data[model]["recent_scores"] if
            s["score"] >= 70)
        data[model]["success_rate"] = successful_tasks /
            len(data[model]["recent_scores"])

        # Update contribution (rolling average)
        contributions = [s["contribution"] for s in data[model]["recent_scores"]]
        data[model]["contribution_to_project"] = statistics.mean(contributions) if
            contributions else 0.0

        self._save_data(data)

    def generate_sample_data(self, days: int = 30):
        """
        Generate sample historical data for demonstration purposes.

        Args:
            days: Number of days of historical data to generate
        """
        data = self._load_data()
        models = ["Claude", "OpenAI", "GLM", "Gemini"]
        task_types = ["feature_implementation", "bug_fix", "refactoring", "testing", "documentation"]

        # Performance characteristics for each model
        model_chars = {
            "Claude": {"base": 85, "variance": 8, "trend": 0.1},
            "OpenAI": {"base": 82, "variance": 10, "trend": 0.05},
            "GLM": {"base": 78, "variance": 12, "trend": -0.02},
            "Gemini": {"base": 80, "variance": 11, "trend": 0.08}
        }

        for model in models:
            if model not in data:
                data[model] = {
                    "recent_scores": [],
                    "total_tasks": 0,
                    "success_rate": 0.0,
                    "contribution_to_project": 0.0,
                    "first_seen": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }

            chars = model_chars[model]
            scores = []

            for day in range(days):
                # Generate 2-5 tasks per day
                tasks_per_day = random.randint(2, 5)
                for task in range(tasks_per_day):
                    # Calculate score with trend and variance
                    trend_effect = chars["trend"] * day
                    base_score = chars["base"] + trend_effect
                    score = max(0, min(100, base_score + random.gauss(0, chars["variance"])))

                    contribution = max(0, min(100, score * 0.3 + random.gauss(0, 5)))
                    task_type = random.choice(task_types)

                    timestamp = datetime.now() - timedelta(days=days-day, hours=random.randint(0, 23))

                    scores.append({
                        "score": round(score, 1),
                        "timestamp": timestamp.isoformat(),
                        "task_type": task_type,
                        "contribution": round(contribution, 1)
                    })

            # Sort by timestamp and add to data
            scores.sort(key=lambda x: x["timestamp"])
            data[model]["recent_scores"] = scores[-100:]  # Keep last 100
            data[model]["total_tasks"] = len(scores)
            data[model]["success_rate"] = sum(1 for s in scores if 
                s["score"] >= 70) / len(scores)
            data[model]["contribution_to_project"] = statistics.mean([s["contribution"] for s in 
                scores])

        self._save_data(data)
        print(f"Generated {days} days of sample data for {len(models)} models")

    def get_model_summary(self, model: str) -> Dict[str, Any]:
        """Get performance summary for a specific model."""
        data = self._load_data()

        if model not in data:
            return {"error": f"Model '{model}' not found"}

        model_data = data[model]
        scores = [s["score"] for s in model_data.get("recent_scores", [])]

        if not scores:
            return {"error": f"No performance data for model '{model}'"}

        return {
            "model": model,
            "total_tasks": model_data.get("total_tasks", 0),
            "average_score": round(statistics.mean(scores), 1),
            "min_score": min(scores),
            "max_score": max(scores),
            "success_rate": round(model_data.get("success_rate", 0) * 100, 1),
            "contribution_to_project": round(
    model_data.get("contribution_to_project", 0),
    1),,
)
            "recent_scores": scores[-10:],  # Last 10 scores
            "first_seen": model_data.get("first_seen"),
            "last_updated": model_data.get("last_updated")
        }

    def get_all_models_summary(self) -> Dict[str, Any]:
        """Get performance summary for all models."""
        data = self._load_data()
        summary = {}

        for model in data.keys():
            summary[model] = self.get_model_summary(model)

        return summary

    def clear_data(self):
        """Clear all model performance data."""
        self._initialize_default_data()
        print("Model performance data cleared")


def main():
    """CLI interface for model performance management."""
    parser = argparse.ArgumentParser(description='Model Performance Data Manager')
    parser.add_argument(
    '--dir',
    default='.claude-patterns',
    help='Patterns directory path',
)

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Add score action
    add_parser = subparsers.add_parser('add', help='Add performance score')
    add_parser.add_argument(
    '--model',
    required=True,
    choices=['Claude',
    'OpenAI',
    'GLM',
    'Gemini'],
)
    add_parser.add_argument(
    '--score',
    type=float,
    required=True,
    help='Performance score (0-100)',
)
    add_parser.add_argument('--task-type', default='unknown', help='Type of task')
    add_parser.add_argument(
    '--contribution',
    type=float,
    default=0.0,
    help='Contribution to project (0-100)',
)

    # Generate sample data action
    generate_parser = subparsers.add_parser('generate-sample', help='Generate sample data')
    generate_parser.add_argument(
    '--days',
    type=int,
    default=30,
    help='Days of historical data to generate',
)

    # Summary actions
    subparsers.add_parser('summary', help='Show all models summary')

    model_summary_parser = subparsers.add_parser('model-summary', help='Show specific model summary')
    model_summary_parser.add_argument('--model', required=True, help='Model name')

    # Clear data action
    subparsers.add_parser('clear', help='Clear all data')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    manager = ModelPerformanceManager(args.dir)

    try:
        if args.action == 'add':
            manager.add_performance_score(
    args.model,
    args.score,
    args.task_type,
    args.contribution,
)
            print(f"Added score {args.score} for {args.model}")

        elif args.action == 'generate-sample':
            manager.generate_sample_data(args.days)

        elif args.action == 'summary':
            summary = manager.get_all_models_summary()
            print(json.dumps(summary, indent=2))

        elif args.action == 'model-summary':
            summary = manager.get_model_summary(args.model)
            print(json.dumps(summary, indent=2))

        elif args.action == 'clear':
            manager.clear_data()

    except Exception as e:
        print(
    json.dumps({'success': False, 'error': str(e)}, indent=2),
    file=sys.stderr,
)
        sys.exit(1)


if __name__ == '__main__':
    main()
