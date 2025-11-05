#!/usr/bin/env python3
"""
Group Specialization Learning System
Automatically identifies what each group excels at and optimizes task delegation
based on learned specializations.

This system tracks group performance across different task types and contexts to
build specialization profiles that inform intelligent task routing.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

# Platform-specific imports for file locking
try:
    import msvcrt  # Windows
    PLATFORM = 'windows'
except ImportError:
    import fcntl  # Unix/Linux/Mac
    PLATFORM = 'unix'


class GroupSpecializationLearner:
    """
    Learns and tracks group specializations for optimal task delegation.
    """

    # Group definitions
    GROUPS = {
        1: "Strategic Analysis & Intelligence",
        2: "Decision Making & Planning",
        3: "Execution & Implementation",
        4: "Validation & Optimization"
    }

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the specialization learning system.

        Args:
            storage_dir: Directory for storing specialization data
        """
        self.storage_dir = Path(storage_dir)
        self.spec_file = self.storage_dir / "group_specializations.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize file if it doesn't exist
        if not self.spec_file.exists():
            self._initialize_storage()

    def _initialize_storage(self):
        """Initialize the storage with default structure."""
        initial_data = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "metadata": {
                "total_observations": 0,
                "learning_confidence": 0,
                "tracking_start_date": datetime.now().isoformat()
            },
            "group_specializations": {
                "1": self._create_empty_specialization_profile(),
                "2": self._create_empty_specialization_profile(),
                "3": self._create_empty_specialization_profile(),
                "4": self._create_empty_specialization_profile()
            },
            "task_routing_recommendations": {},
            "learning_insights": []
        }

        self._write_data(initial_data)

    def _create_empty_specialization_profile(self) -> Dict[str, Any]:
        """Create empty specialization profile for a group."""
        return {
            "task_type_performance": {},
            "context_performance": {},
            "complexity_performance": {},
            "domain_expertise": {},
            "top_specializations": [],
            "weaknesses": [],
            "optimal_conditions": [],
            "performance_factors": {}
        }

    def _lock_file(self, file_handle):
        """Platform-specific file locking."""
        if PLATFORM == 'windows':
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX)

    def _unlock_file(self, file_handle):
        """Platform-specific file unlocking."""
        if PLATFORM == 'windows':
            try:
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            except (OSError, PermissionError):
                pass
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)

    def _read_data(self) -> Dict[str, Any]:
        """Read specialization data with file locking."""
        try:
            with open(self.spec_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    data = json.load(f)
                finally:
                    self._unlock_file(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_storage()
            return self._read_data()

    def _write_data(self, data: Dict[str, Any]):
        """Write specialization data with file locking."""
        with open(self.spec_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def record_observation(
        self,
        group_num: int,
        task_type: str,
        complexity: str,
        domain: str,
        context: Optional[Dict[str, Any]],
        quality_score: float,
        execution_time: float,
        success: bool
    ):
        """
        Record an observation of group performance.

        Args:
            group_num: Group number (1-4)
            task_type: Type of task (refactoring, bug-fix, etc.)
            complexity: Complexity level (low, medium, high)
            domain: Domain (backend, frontend, database, etc.)
            context: Additional context
            quality_score: Quality score achieved (0-100)
            execution_time: Time taken in seconds
            success: Whether task was successful
        """
        if group_num not in self.GROUPS:
            raise ValueError(f"Invalid group number: {group_num}")

        spec_data = self._read_data()
        group_key = str(group_num)
        group_profile = spec_data["group_specializations"][group_key]

        # Update task type performance
        if task_type not in group_profile["task_type_performance"]:
            group_profile["task_type_performance"][task_type] = {
                "total_attempts": 0,
                "successful_attempts": 0,
                "total_quality_score": 0,
                "total_execution_time": 0,
                "avg_quality_score": 0,
                "avg_execution_time": 0,
                "success_rate": 0
            }

        task_perf = group_profile["task_type_performance"][task_type]
        task_perf["total_attempts"] += 1
        if success:
            task_perf["successful_attempts"] += 1
        task_perf["total_quality_score"] += quality_score
        task_perf["total_execution_time"] += execution_time

        # Calculate averages
        task_perf["avg_quality_score"] = task_perf["total_quality_score"] / task_perf["total_attempts"]
        task_perf["avg_execution_time"] = task_perf["total_execution_time"] / task_perf["total_attempts"]
        task_perf["success_rate"] = task_perf["successful_attempts"] / task_perf["total_attempts"]

        # Update complexity performance
        if complexity not in group_profile["complexity_performance"]:
            group_profile["complexity_performance"][complexity] = {
                "total_attempts": 0,
                "avg_quality": 0,
                "success_rate": 0
            }

        complexity_perf = group_profile["complexity_performance"][complexity]
        total = complexity_perf["total_attempts"]
        complexity_perf["avg_quality"] = (
            (complexity_perf["avg_quality"] * total + quality_score) / (total + 1)
        )
        complexity_perf["total_attempts"] += 1

        # Update domain expertise
        if domain not in group_profile["domain_expertise"]:
            group_profile["domain_expertise"][domain] = {
                "total_attempts": 0,
                "avg_quality": 0,
                "expertise_level": "novice"
            }

        domain_exp = group_profile["domain_expertise"][domain]
        total = domain_exp["total_attempts"]
        domain_exp["avg_quality"] = (
            (domain_exp["avg_quality"] * total + quality_score) / (total + 1)
        )
        domain_exp["total_attempts"] += 1

        # Determine expertise level
        if domain_exp["total_attempts"] >= 20 and domain_exp["avg_quality"] >= 90:
            domain_exp["expertise_level"] = "expert"
        elif domain_exp["total_attempts"] >= 10 and domain_exp["avg_quality"] >= 85:
            domain_exp["expertise_level"] = "advanced"
        elif domain_exp["total_attempts"] >= 5 and domain_exp["avg_quality"] >= 75:
            domain_exp["expertise_level"] = "intermediate"
        else:
            domain_exp["expertise_level"] = "novice"

        # Update metadata
        spec_data["metadata"]["total_observations"] += 1
        spec_data["metadata"]["last_updated"] = datetime.now().isoformat()

        # Calculate learning confidence (0-1)
        total_obs = spec_data["metadata"]["total_observations"]
        spec_data["metadata"]["learning_confidence"] = min(0.95, 0.5 + (total_obs / 200))

        self._write_data(spec_data)

        # Update specializations after each observation
        self._update_specializations(group_num)

    def _update_specializations(self, group_num: int):
        """Update specialization analysis for a group."""
        spec_data = self._read_data()
        group_key = str(group_num)
        group_profile = spec_data["group_specializations"][group_key]

        # Identify top specializations (task types with high performance)
        specializations = []
        for task_type, perf in group_profile["task_type_performance"].items():
            if perf["total_attempts"] >= 3:  # Minimum attempts for consideration
                # Specialization score: weighted combination of quality and success rate
                spec_score = (perf["avg_quality"] * 0.6) + (perf["success_rate"] * 100 * 0.4)

                if spec_score >= 80:  # High performance threshold
                    specializations.append({
                        "task_type": task_type,
                        "specialization_score": spec_score,
                        "avg_quality": perf["avg_quality"],
                        "success_rate": perf["success_rate"],
                        "attempts": perf["total_attempts"],
                        "expertise_level": self._determine_expertise_level(spec_score, perf["total_attempts"])
                    })

        # Sort by specialization score
        specializations.sort(key=lambda x: x["specialization_score"], reverse=True)
        group_profile["top_specializations"] = specializations[:5]

        # Identify weaknesses (task types with low performance)
        weaknesses = []
        for task_type, perf in group_profile["task_type_performance"].items():
            if perf["total_attempts"] >= 3:
                weakness_score = (perf["avg_quality"] * 0.6) + (perf["success_rate"] * 100 * 0.4)

                if weakness_score < 70:  # Low performance threshold
                    weaknesses.append({
                        "task_type": task_type,
                        "weakness_score": weakness_score,
                        "avg_quality": perf["avg_quality"],
                        "success_rate": perf["success_rate"],
                        "attempts": perf["total_attempts"]
                    })

        weaknesses.sort(key=lambda x: x["weakness_score"])
        group_profile["weaknesses"] = weaknesses[:3]

        # Identify optimal conditions
        optimal_conditions = []

        # Check complexity performance
        for complexity, perf in group_profile["complexity_performance"].items():
            if perf["total_attempts"] >= 3 and perf["avg_quality"] >= 85:
                optimal_conditions.append({
                    "condition_type": "complexity",
                    "value": complexity,
                    "avg_quality": perf["avg_quality"]
                })

        # Check domain expertise
        for domain, exp in group_profile["domain_expertise"].items():
            if exp["expertise_level"] in ["advanced", "expert"]:
                optimal_conditions.append({
                    "condition_type": "domain",
                    "value": domain,
                    "expertise_level": exp["expertise_level"],
                    "avg_quality": exp["avg_quality"]
                })

        group_profile["optimal_conditions"] = optimal_conditions

        self._write_data(spec_data)

        # Generate routing recommendations
        self._generate_routing_recommendations()

    def _determine_expertise_level(self, spec_score: float, attempts: int) -> str:
        """Determine expertise level based on score and experience."""
        if attempts >= 20 and spec_score >= 90:
            return "expert"
        elif attempts >= 10 and spec_score >= 85:
            return "advanced"
        elif attempts >= 5 and spec_score >= 80:
            return "intermediate"
        else:
            return "developing"

    def _generate_routing_recommendations(self):
        """Generate task routing recommendations based on specializations."""
        spec_data = self._read_data()

        # Collect all task types across all groups
        all_task_types = set()
        for group_profile in spec_data["group_specializations"].values():
            all_task_types.update(group_profile["task_type_performance"].keys())

        # For each task type, find the best group
        routing_recommendations = {}
        for task_type in all_task_types:
            group_scores = []

            for group_num in [1, 2, 3, 4]:
                group_key = str(group_num)
                group_profile = spec_data["group_specializations"][group_key]

                if task_type in group_profile["task_type_performance"]:
                    perf = group_profile["task_type_performance"][task_type]
                    if perf["total_attempts"] >= 2:
                        score = (perf["avg_quality"] * 0.6) + (perf["success_rate"] * 100 * 0.4)
                        group_scores.append({
                            "group": group_num,
                            "score": score,
                            "quality": perf["avg_quality"],
                            "success_rate": perf["success_rate"]
                        })

            if group_scores:
                # Sort by score
                group_scores.sort(key=lambda x: x["score"], reverse=True)

                routing_recommendations[task_type] = {
                    "primary_group": group_scores[0]["group"],
                    "primary_score": group_scores[0]["score"],
                    "alternatives": [
                        {"group": g["group"], "score": g["score"]}
                        for g in group_scores[1:3]
                    ] if len(group_scores) > 1 else []
                }

        spec_data["task_routing_recommendations"] = routing_recommendations
        self._write_data(spec_data)

    def get_specialization_profile(self, group_num: int) -> Dict[str, Any]:
        """Get complete specialization profile for a group."""
        if group_num not in self.GROUPS:
            raise ValueError(f"Invalid group number: {group_num}")

        spec_data = self._read_data()
        group_key = str(group_num)

        return {
            "group": group_num,
            "group_name": self.GROUPS[group_num],
            **spec_data["group_specializations"][group_key],
            "learning_confidence": spec_data["metadata"]["learning_confidence"]
        }

    def get_recommended_group_for_task(
        self,
        task_type: str,
        complexity: Optional[str] = None,
        domain: Optional[str] = None
    ) -> Tuple[int, float, str]:
        """
        Get recommended group for a task.

        Args:
            task_type: Type of task
            complexity: Optional complexity level
            domain: Optional domain

        Returns:
            Tuple of (group_number, confidence, rationale)
        """
        spec_data = self._read_data()

        # Check routing recommendations
        if task_type in spec_data["task_routing_recommendations"]:
            recommendation = spec_data["task_routing_recommendations"][task_type]
            primary_group = recommendation["primary_group"]
            confidence = min(0.95, recommendation["primary_score"] / 100)

            rationale = f"Group {primary_group} excels at {task_type} (score: {recommendation['primary_score']:.1f})"

            # Adjust confidence based on additional factors
            if complexity or domain:
                group_profile = spec_data["group_specializations"][str(primary_group)]

                if complexity and complexity in group_profile["complexity_performance"]:
                    complexity_quality = group_profile["complexity_performance"][complexity]["avg_quality"]
                    if complexity_quality >= 85:
                        confidence *= 1.1  # Boost confidence
                        rationale += f", strong with {complexity} complexity"

                if domain and domain in group_profile["domain_expertise"]:
                    expertise = group_profile["domain_expertise"][domain]
                    if expertise["expertise_level"] in ["advanced", "expert"]:
                        confidence *= 1.1
                        rationale += f", {expertise['expertise_level']} in {domain}"

            confidence = min(0.95, confidence)

            return (primary_group, confidence, rationale)

        # No specific recommendation - use heuristic based on task type
        # This is fallback for new task types
        if "analysis" in task_type.lower():
            return (1, 0.6, "Task appears to be analysis-related (heuristic)")
        elif "decision" in task_type.lower() or "plan" in task_type.lower():
            return (2, 0.6, "Task appears to be decision/planning-related (heuristic)")
        elif "implement" in task_type.lower() or "execute" in task_type.lower():
            return (3, 0.6, "Task appears to be implementation-related (heuristic)")
        elif "validate" in task_type.lower() or "optimize" in task_type.lower():
            return (4, 0.6, "Task appears to be validation-related (heuristic)")
        else:
            # Default to standard four-tier workflow
            return (1, 0.5, "No specific specialization data - use standard workflow")

    def get_learning_insights(self) -> List[Dict[str, Any]]:
        """Get insights about what the system has learned."""
        spec_data = self._read_data()

        insights = []

        # Identify clear specializations
        for group_num in [1, 2, 3, 4]:
            group_key = str(group_num)
            group_profile = spec_data["group_specializations"][group_key]

            if group_profile["top_specializations"]:
                top_spec = group_profile["top_specializations"][0]
                insights.append({
                    "type": "specialization",
                    "group": group_num,
                    "group_name": self.GROUPS[group_num],
                    "insight": f"Group {group_num} excels at {top_spec['task_type']}",
                    "confidence": top_spec["specialization_score"] / 100,
                    "evidence": f"Quality: {top_spec['avg_quality']:.1f}, Success: {top_spec['success_rate']*100:.1f}%"
                })

            # Identify domain expertise
            expert_domains = [
                (domain, exp) for domain, exp in group_profile["domain_expertise"].items()
                if exp["expertise_level"] == "expert"
            ]

            for domain, exp in expert_domains:
                insights.append({
                    "type": "domain_expertise",
                    "group": group_num,
                    "group_name": self.GROUPS[group_num],
                    "insight": f"Group {group_num} is an expert in {domain}",
                    "confidence": 0.9,
                    "evidence": f"Quality: {exp['avg_quality']:.1f} over {exp['total_attempts']} attempts"
                })

        # Identify complementary groups (groups that work well together)
        # This would require cross-group analysis - placeholder for future enhancement

        return insights


def main():
    """Command-line interface for testing the specialization learner."""
    import argparse

    parser = argparse.ArgumentParser(description='Group Specialization Learner')
    parser.add_argument('--storage-dir', default='.claude-patterns', help='Storage directory')
    parser.add_argument('--action', choices=['record', 'profile', 'recommend', 'insights'],
                       help='Action to perform')
    parser.add_argument('--group', type=int, help='Group number (1-4)')
    parser.add_argument('--task-type', help='Task type')
    parser.add_argument('--complexity', help='Complexity (low/medium/high)')
    parser.add_argument('--domain', help='Domain')
    parser.add_argument('--quality', type=float, help='Quality score')
    parser.add_argument('--time', type=float, default=60, help='Execution time')
    parser.add_argument('--success', action='store_true', help='Task successful')

    args = parser.parse_args()

    learner = GroupSpecializationLearner(args.storage_dir)

    if args.action == 'record':
        if not all([args.group, args.task_type, args.complexity, args.domain, args.quality is not None]):
            print("Error: --group, --task-type, --complexity, --domain, and --quality required")
            sys.exit(1)

        learner.record_observation(
            group_num=args.group,
            task_type=args.task_type,
            complexity=args.complexity,
            domain=args.domain,
            context={},
            quality_score=args.quality,
            execution_time=args.time,
            success=args.success
        )
        print(f"Observation recorded for Group {args.group}")

    elif args.action == 'profile':
        if not args.group:
            print("Error: --group required for profile")
            sys.exit(1)

        profile = learner.get_specialization_profile(args.group)
        print(f"Group {profile['group']}: {profile['group_name']}")
        print(f"  Learning Confidence: {profile['learning_confidence']*100:.1f}%")
        print("\nTop Specializations:")
        for spec in profile['top_specializations'][:3]:
            print(f"  {spec['task_type']}: {spec['specialization_score']:.1f} ({spec['expertise_level']})")

    elif args.action == 'recommend':
        if not args.task_type:
            print("Error: --task-type required for recommend")
            sys.exit(1)

        group, confidence, rationale = learner.get_recommended_group_for_task(
            task_type=args.task_type,
            complexity=args.complexity,
            domain=args.domain
        )
        print(f"Recommended Group: {group}")
        print(f"Confidence: {confidence*100:.1f}%")
        print(f"Rationale: {rationale}")

    elif args.action == 'insights':
        insights = learner.get_learning_insights()
        print(f"Learning Insights ({len(insights)} total):")
        for insight in insights[:5]:
            print(f"  [{insight['type']}] {insight['insight']}")
            print(f"    Confidence: {insight['confidence']*100:.1f}% - {insight['evidence']}")

    else:
        # Show summary
        print("Group Specialization Learner Initialized")
        print(f"Storage: {learner.spec_file}")


if __name__ == '__main__':
    main()
