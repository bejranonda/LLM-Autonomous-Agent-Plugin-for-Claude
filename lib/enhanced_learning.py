#!/usr/bin/env python3
#     Enhanced Learning Engine for Autonomous Claude Agent Plugin
    """

Advanced pattern learning system with contextual understanding, confidence scoring,
skill effectiveness tracking, and cross-project pattern transfer capabilities.
import json
import argparse
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import platform
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
import statistics
import os

# Handle Windows compatibility for file locking
if platform.system() == "Windows":
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


class EnhancedLearningEngine:
    """Advanced learning engine with contextual pattern recognition and predictive capabilities."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """
        Initialize enhanced learning engine.

        Args:
            patterns_dir: Directory path for storing patterns (default: .claude-patterns)
        """
        self.patterns_dir = Path(patterns_dir)
        self.patterns_file = self.patterns_dir / "patterns.json"
        self.cache = {}
        self.cache_ttl = 300  # Cache for 5 minutes
        self.last_update = {}
        self._ensure_directory()

    def _ensure_directory(self):
        """Create patterns directory if it doesn't exist."""
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        if not self.patterns_file.exists():
            self._write_patterns(
                {
                    "project_context": {"detected_languages": [], "frameworks": [], "project_type": "unknown"},
                    "patterns": [],
                    "skill_effectiveness": {},
                    "agent_effectiveness": {},
                    "learning_statistics": {
                        "total_patterns": 0,
                        "success_rate": 0.0,
                        "last_updated": datetime.now().isoformat(),
                    },
                }
            )

    def _read_patterns():
        """
        
        Read patterns from JSON file with file locking.

        Returns:
            Dictionary containing patterns data
        """
        try:
            with open(self.patterns_file, "r", encoding="utf-8") as f:
                lock_file(f, exclusive=False)
                try:
                    content = f.read()
                    if not content.strip():
                        return {"patterns": [], "skill_effectiveness": {}, "agent_effectiveness": {}}
                    return json.loads(content)
                finally:
                    unlock_file(f)
        except FileNotFoundError:
            return {"patterns": [], "skill_effectiveness": {}, "agent_effectiveness": {}}
        except json.JSONDecodeError as e:
            print(f"Error: Malformed JSON in {self.patterns_file}: {e}", file=sys.stderr)
            return {"patterns": [], "skill_effectiveness": {}, "agent_effectiveness": {}}
        except Exception as e:
            print(f"Error reading patterns: {e}", file=sys.stderr)
            return {"patterns": [], "skill_effectiveness": {}, "agent_effectiveness": {}}

    def _write_patterns(self, patterns_data: Dict[str, Any]):
        """
        Write patterns to JSON file with file locking.

        Args:
            patterns_data: Dictionary containing patterns data to write
        """
        try:
            with open(self.patterns_file, "w", encoding="utf-8") as f:
                lock_file(f, exclusive=True)
                try:
                    json.dump(patterns_data, f, indent=2, ensure_ascii=False)
                    self.last_update["patterns"] = datetime.now().timestamp()
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error writing patterns: {e}", file=sys.stderr)
            raise

    def record_pattern(
        self,
        task_type: str,
        context: Dict[str, Any],
        execution: Dict[str, Any],
        outcome: Dict[str, Any],
        confidence: float = 1.0,
    )-> bool:
        """Record Pattern."""
        Record a new pattern for learning.

        Args:
            task_type: Type of task performed
            context: Context information (languages, frameworks, etc.)
            execution: Execution details (skills used, agents delegated, etc.)
            outcome: Results of the execution (success, quality score, etc.)
            confidence: Confidence score for this pattern (0.0 to 1.0)

        Returns:
            True on success
        """
        # Validate inputs
        if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
            raise ValueError("confidence must be a number between 0 and 1")

        # Create pattern
        pattern = {
            "pattern_id": self._generate_pattern_id(task_type, context),
            "task_type": task_type,
            "context": context,
            "execution": execution,
            "outcome": outcome,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "reuse_count": 0,
            "last_used": None,
        }

        # Add to patterns
        patterns_data = self._read_patterns()
        patterns_data["patterns"].append(pattern)

        # Update statistics
        patterns_data["learning_statistics"]["total_patterns"] += 1
        patterns_data["learning_statistics"]["last_updated"] = datetime.now().isoformat()

        # Calculate success rate
        successful_patterns = sum(1 for p in patterns_data["patterns"] if p.get("outcome", {}).get("success", False))
        total_patterns = len(patterns_data["patterns"])
        patterns_data["learning_statistics"]["success_rate"] = (
            successful_patterns / total_patterns if total_patterns > 0 else 0.0
        )

        self._write_patterns(patterns_data)
        return True

    def _generate_pattern_id(self, task_type: str, context: Dict[str, Any]) -> str:
        """Generate unique pattern ID based on task type and context."""
        content = f"{task_type}_{json.dumps(context, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def find_similar_patterns(
        self, task_type: str, context: Dict[str, Any], limit: int = 5, min_confidence: float = 0.5
    )-> List[Dict[str, Any]]:
        """Find Similar Patterns."""
        Find patterns similar to the given task type and context.

        Args:
            task_type: Type of task to find patterns for
            context: Context information for matching
            limit: Maximum number of patterns to return
            min_confidence: Minimum confidence threshold

        Returns:
            List of similar patterns sorted by relevance
        """
        patterns_data = self._read_patterns()
        all_patterns = patterns_data.get("patterns", [])

        # Filter by task type and confidence
        matching_patterns = [
            p for p in all_patterns if p.get("task_type") == task_type and p.get("confidence", 0) >= min_confidence
        ]

        # Calculate relevance scores
        scored_patterns = []
        for pattern in matching_patterns:
            relevance_score = self._calculate_relevance(pattern, context)
            scored_patterns.append((pattern, relevance_score))

        # Sort by relevance score and return top patterns
        scored_patterns.sort(key=lambda x: x[1], reverse=True)
        return [pattern for pattern, score in scored_patterns[:limit]]

    def _calculate_relevance(self, pattern: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calculate relevance score of a pattern to given context."""
        pattern_context = pattern.get("context", {})

        # Calculate similarity score
        similarity_score = 0.0
        total_factors = 0

        # Compare languages
        pattern_langs = set(pattern_context.get("detected_languages", []))
        context_langs = set(context.get("detected_languages", []))

        if pattern_langs or context_langs:
            intersection = pattern_langs & context_langs
            union = pattern_langs | context_langs
            similarity_score += len(intersection) / len(union) if union else 0.0
            total_factors += 1

        # Compare frameworks
        pattern_frameworks = set(pattern_context.get("frameworks", []))
        context_frameworks = set(context.get("frameworks", []))

        if pattern_frameworks or context_frameworks:
            intersection = pattern_frameworks & context_frameworks
            union = pattern_frameworks | context_frameworks
            similarity_score += len(intersection) / len(union) if union else 0.0
            total_factors += 1

        # Compare project type
        pattern_type = pattern_context.get("project_type", "unknown")
        context_type = context.get("project_type", "unknown")

        if pattern_type == context_type:
            similarity_score += 1.0
            total_factors += 1

        # Calculate average similarity
        return similarity_score / total_factors if total_factors > 0 else 0.0

    def update_pattern_usage(self, pattern_id: str, success: bool = True, quality_score: float = None):
        """
        Update pattern usage statistics.

        Args:
            pattern_id: ID of the pattern to update
            success: Whether the pattern was successfully applied
            quality_score: Quality score achieved (optional)
        """
        patterns_data = self._read_patterns()

        # Find the pattern
        for pattern in patterns_data.get("patterns", []):
            if pattern.get("pattern_id") == pattern_id:
                pattern["reuse_count"] += 1
                pattern["last_used"] = datetime.now().isoformat()

                # Update confidence based on success
                current_confidence = pattern.get("confidence", 0.5)
                if success:
                    # Increase confidence
                    pattern["confidence"] = min(1.0, current_confidence + 0.1)
                else:
                    # Decrease confidence
                    pattern["confidence"] = max(0.1, current_confidence - 0.2)

                break

        self._write_patterns(patterns_data)

    def get_skill_effectiveness():
        """
        
        Calculate effectiveness scores for all skills.

        Returns:
            Dictionary mapping skill names to effectiveness metrics
        """
        patterns_data = self._read_patterns()
        patterns = patterns_data.get("patterns", [])

        skill_stats = defaultdict(lambda: {"success_count": 0, "total_count": 0, "quality_scores": []})

        for pattern in patterns:
            skills = pattern.get("execution", {}).get("skills_used", [])
            success = pattern.get("outcome", {}).get("success", False)
            quality_score = pattern.get("outcome", {}).get("quality_score", 0)

            for skill in skills:
                skill_stats[skill]["total_count"] += 1
                if success:
                    skill_stats[skill]["success_count"] += 1
                if quality_score is not None:
                    skill_stats[skill]["quality_scores"].append(quality_score)

        # Calculate effectiveness metrics
        effectiveness = {}
        for skill, stats in skill_stats.items():
            success_rate = stats["success_count"] / stats["total_count"] if stats["total_count"] > 0 else 0
            avg_quality = statistics.mean(stats["quality_scores"]) if stats["quality_scores"] else 0

            effectiveness[skill] = {
                "success_rate": success_rate,
                "average_quality": avg_quality,
                "usage_count": stats["total_count"],
                "effectiveness_score": (success_rate * 0.6 + avg_quality * 0.4),
            }

        return effectiveness

    def get_agent_effectiveness():
        """
        
        Calculate effectiveness scores for all agents.

        Returns:
            Dictionary mapping agent names to effectiveness metrics
        """
        patterns_data = self._read_patterns()
        patterns = patterns_data.get("patterns", [])

        agent_stats = defaultdict(lambda: {"success_count": 0, "total_count": 0, "quality_scores": []})

        for pattern in patterns:
            agents = pattern.get("execution", {}).get("agents_delegated", [])
            success = pattern.get("outcome", {}).get("success", False)
            quality_score = pattern.get("outcome", {}).get("quality_score", 0)

            for agent in agents:
                agent_stats[agent]["total_count"] += 1
                if success:
                    agent_stats[agent]["success_count"] += 1
                if quality_score is not None:
                    agent_stats[agent]["quality_scores"].append(quality_score)

        # Calculate effectiveness metrics
        effectiveness = {}
        for agent, stats in agent_stats.items():
            success_rate = stats["success_count"] / stats["total_count"] if stats["total_count"] > 0 else 0
            avg_quality = statistics.mean(stats["quality_scores"]) if stats["quality_scores"] else 0

            effectiveness[agent] = {
                "success_rate": success_rate,
                "average_quality": avg_quality,
                "usage_count": stats["total_count"],
                "effectiveness_score": (success_rate * 0.6 + avg_quality * 0.4),
            }

        return effectiveness

    def get_learning_statistics():
        """
        
        Get comprehensive learning statistics.

        Returns:
            Dictionary containing learning statistics
        """
        patterns_data = self._read_patterns()
        patterns = patterns_data.get("patterns", [])

        # Calculate basic statistics
        total_patterns = len(patterns)
        successful_patterns = sum(1 for p in patterns if p.get("outcome", {}).get("success", False))
        success_rate = successful_patterns / total_patterns if total_patterns > 0 else 0

        # Calculate pattern age statistics
        now = datetime.now()
        pattern_ages = []
        for pattern in patterns:
            try:
                created = datetime.fromisoformat(pattern.get("timestamp", "").replace("Z", "+00:00"))
                age_days = (now - created).days
                pattern_ages.append(age_days)
            except:
                continue

        avg_pattern_age = statistics.mean(pattern_ages) if pattern_ages else 0

        # Get most used patterns
        most_used = sorted(patterns, key=lambda x: x.get("reuse_count", 0), reverse=True)[:5]

        # Get highest confidence patterns
        highest_confidence = sorted(patterns, key=lambda x: x.get("confidence", 0), reverse=True)[:5]

        return {
            "total_patterns": total_patterns,
            "success_rate": success_rate,
            "average_pattern_age_days": avg_pattern_age,
            "most_used_patterns": most_used,
            "highest_confidence_patterns": highest_confidence,
            "skill_effectiveness": self.get_skill_effectiveness(),
            "agent_effectiveness": self.get_agent_effectiveness(),
            "last_updated": datetime.now().isoformat(),
        }

    def cleanup_old_patterns(self, days_threshold: int = 90):
        """
        Remove old patterns that haven't been used recently.

        Args:
            days_threshold: Remove patterns older than this many days if not reused
        """
        patterns_data = self._read_patterns()
        patterns = patterns_data.get("patterns", [])

        cutoff_date = datetime.now() - timedelta(days=days_threshold)

        # Filter patterns
        filtered_patterns = []
        for pattern in patterns:
            try:
                created = datetime.fromisoformat(pattern.get("timestamp", "").replace("Z", "+00:00"))
                last_used = pattern.get("last_used")

                # Keep if recent or has been reused
                if (
                    created > cutoff_date
                    or (last_used and datetime.fromisoformat(last_used.replace("Z", "+00:00")) > cutoff_date)
                    or pattern.get("reuse_count", 0) > 0
                ):
                    filtered_patterns.append(pattern)
            except:
                # Keep patterns with invalid dates
                filtered_patterns.append(pattern)

        patterns_data["patterns"] = filtered_patterns
        patterns_data["learning_statistics"]["last_updated"] = datetime.now().isoformat()

        self._write_patterns(patterns_data)


def main():
    """Command-line interface for enhanced learning engine."""
    parser = argparse.ArgumentParser(description="Enhanced Learning Engine")
    parser.add_argument("--dir", default=".claude-patterns", help="Patterns directory path")

    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Record action
    record_parser = subparsers.add_parser("record", help="Record a pattern")
    record_parser.add_argument("--task-type", required=True, help="Task type")
    record_parser.add_argument("--context", required=True, help="Context JSON string")
    record_parser.add_argument("--execution", required=True, help="Execution JSON string")
    record_parser.add_argument("--outcome", required=True, help="Outcome JSON string")
    record_parser.add_argument("--confidence", type=float, default=1.0, help="Confidence score")

    # Find action
    find_parser = subparsers.add_parser("find", help="Find similar patterns")
    find_parser.add_argument("--task-type", required=True, help="Task type")
    find_parser.add_argument("--context", required=True, help="Context JSON string")
    find_parser.add_argument("--limit", type=int, default=5, help="Maximum patterns to return")

    # Stats action
    stats_parser = subparsers.add_parser("stats", help="Show learning statistics")

    # Cleanup action
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up old patterns")
    cleanup_parser.add_argument("--days", type=int, default=90, help="Age threshold in days")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    engine = EnhancedLearningEngine(args.dir)

    try:
        if args.action == "record":
            context = json.loads(args.context)
            execution = json.loads(args.execution)
            outcome = json.loads(args.outcome)

            success = engine.record_pattern(args.task_type, context, execution, outcome, args.confidence)
            print(json.dumps({"success": success}, indent=2))

        elif args.action == "find":
            context = json.loads(args.context)
            patterns = engine.find_similar_patterns(args.task_type, context, args.limit)
            print(json.dumps(patterns, indent=2))

        elif args.action == "stats":
            stats = engine.get_learning_statistics()
            print(json.dumps(stats, indent=2))

        elif args.action == "cleanup":
            engine.cleanup_old_patterns(args.days)
            print(json.dumps({"success": True}, indent=2))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
