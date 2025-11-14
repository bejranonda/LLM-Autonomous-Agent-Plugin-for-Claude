#!/usr/bin/env python3
"""
User Preference Learning System
Learns user preferences over time to adapt agent behavior and improve personalization.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Platform-specific imports for file locking
try:
    import msvcrt  # Windows

    PLATFORM = "windows"
except ImportError:
    import fcntl  # Unix/Linux/Mac

    PLATFORM = "unix"


class UserPreferenceLearner:
    """
    Learns and adapts to user preferences including:
    - Coding style preferences
    - Workflow preferences
    - Quality weights and priorities
    - Communication style
    - Auto-fix confidence thresholds
    """

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the user preference learner.

        Args:
            storage_dir: Directory for storing preference data
        """
        self.storage_dir = Path(storage_dir)
        self.preference_file = self.storage_dir / "user_preferences.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize preference file if it doesn't exist
        if not self.preference_file.exists():
            self._initialize_preference_storage()

    def _initialize_preference_storage(self):
        """Initialize the preference storage with default structure."""
        initial_data = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "metadata": {
                "total_interactions": 0,
                "approvals": 0,
                "rejections": 0,
                "modifications": 0,
                "learning_confidence": 0.0,
            },
            "coding_style": {
                "verbosity": "balanced",  # concise, balanced, verbose
                "comments": "moderate",  # minimal, moderate, extensive
                "naming_convention": "auto",  # auto-detect
                "test_coverage_preference": "medium",  # low, medium, high
                "documentation_level": "standard",  # minimal, standard, comprehensive
                "error_handling": "standard",  # minimal, standard, extensive
            },
            "workflow_preferences": {
                "auto_fix_enabled": True,
                "auto_fix_confidence_threshold": 0.90,
                "confirmation_required_for": ["breaking_changes", "security_fixes"],
                "parallel_execution_preferred": True,
                "background_tasks_enabled": True,
                "quality_threshold": 70,
            },
            "quality_weights": {
                "tests": 0.30,
                "documentation": 0.20,
                "code_quality": 0.25,
                "standards": 0.15,
                "patterns": 0.10,
            },
            "communication_style": {
                "detail_level": "balanced",  # brief, balanced, detailed
                "technical_depth": "medium",  # low, medium, high
                "explanation_preference": "when_needed",  # minimal, when_needed, always
                "progress_updates": "summary",  # none, summary, detailed
            },
            "task_preferences": {
                "preferred_task_order": [],  # learned from history
                "task_type_preferences": {},  # task_type -> preference_score
                "agent_preferences": {},  # agent_name -> preference_score
            },
            "interaction_history": [],
            "learned_patterns": [],
        }

        self._write_data(initial_data)

    def _lock_file(self, file_handle):
        """Platform-specific file locking."""
        if PLATFORM == "windows":
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX)

    def _unlock_file(self, file_handle):
        """Platform-specific file unlocking."""
        if PLATFORM == "windows":
            try:
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            except (OSError, PermissionError):
                # File may already be unlocked on Windows
                pass
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)

    def _read_data(self) -> Dict[str, Any]:
        """Read preference data with file locking."""
        try:
            with open(self.preference_file, "r", encoding="utf-8") as f:
                self._lock_file(f)
                try:
                    data = json.load(f)
                finally:
                    self._unlock_file(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_preference_storage()
            return self._read_data()

    def _write_data(self, data: Dict[str, Any]):
        """Write preference data with file locking."""
        with open(self.preference_file, "w", encoding="utf-8") as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def record_interaction(
        self, interaction_type: str, task_id: str, user_feedback: str, context: Optional[Dict[str, Any]] = None
    ):
        """
        Record a user interaction for learning.

        Args:
            interaction_type: Type of interaction (approval, rejection, modification, comment)
            task_id: Associated task ID
            user_feedback: User's feedback or action
            context: Additional context (code style, quality concerns, etc.)
        """
        pref_data = self._read_data()

        interaction = {
            "interaction_id": f"interaction_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": interaction_type,
            "task_id": task_id,
            "feedback": user_feedback,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
        }

        pref_data["interaction_history"].append(interaction)

        # Keep last 500 interactions
        if len(pref_data["interaction_history"]) > 500:
            pref_data["interaction_history"] = pref_data["interaction_history"][-500:]

        # Update metadata
        pref_data["metadata"]["total_interactions"] += 1

        if interaction_type == "approval":
            pref_data["metadata"]["approvals"] += 1
        elif interaction_type == "rejection":
            pref_data["metadata"]["rejections"] += 1
        elif interaction_type == "modification":
            pref_data["metadata"]["modifications"] += 1

        # Update learning confidence
        total = pref_data["metadata"]["total_interactions"]
        approvals = pref_data["metadata"]["approvals"]
        pref_data["metadata"]["learning_confidence"] = min(approvals / total, 1.0) if total > 0 else 0.0

        pref_data["metadata"]["last_updated"] = datetime.now().isoformat()

        self._write_data(pref_data)

        # Analyze and update preferences
        self._analyze_and_update_preferences(interaction, context)

    def _analyze_and_update_preferences(self, interaction: Dict[str, Any], context: Optional[Dict[str, Any]]):
        """Analyze interaction and update preferences accordingly."""
        if not context:
            return

        pref_data = self._read_data()

        # Learn coding style preferences
        if "code_style" in context:
            self._update_coding_style_preferences(pref_data, interaction, context["code_style"])

        # Learn workflow preferences
        if "workflow" in context:
            self._update_workflow_preferences(pref_data, interaction, context["workflow"])

        # Learn quality weights
        if "quality_focus" in context:
            self._update_quality_weights(pref_data, interaction, context["quality_focus"])

        # Learn communication preferences
        if "communication" in context:
            self._update_communication_preferences(pref_data, interaction, context["communication"])

        # Learn task preferences
        if "task_type" in context:
            self._update_task_preferences(pref_data, interaction, context)

        self._write_data(pref_data)

    def _update_coding_style_preferences(
        self, pref_data: Dict[str, Any], interaction: Dict[str, Any], style_context: Dict[str, Any]
    ):
        """Update coding style preferences based on user feedback."""
        if interaction["type"] == "approval":
            # Reinforce current style choices
            if "verbosity" in style_context:
                pref_data["coding_style"]["verbosity"] = style_context["verbosity"]

            if "comments" in style_context:
                pref_data["coding_style"]["comments"] = style_context["comments"]

            if "documentation_level" in style_context:
                pref_data["coding_style"]["documentation_level"] = style_context["documentation_level"]

        elif interaction["type"] == "modification":
            # Learn from user's changes
            feedback = interaction["feedback"].lower()

            if "too verbose" in feedback or "too long" in feedback:
                pref_data["coding_style"]["verbosity"] = "concise"
            elif "more detail" in feedback or "more explanation" in feedback:
                pref_data["coding_style"]["verbosity"] = "verbose"

            if "more comments" in feedback:
                pref_data["coding_style"]["comments"] = "extensive"
            elif "fewer comments" in feedback or "less comments" in feedback:
                pref_data["coding_style"]["comments"] = "minimal"

    def _update_workflow_preferences(
        self, pref_data: Dict[str, Any], interaction: Dict[str, Any], workflow_context: Dict[str, Any]
    ):
        """Update workflow preferences based on user feedback."""
        if "auto_fix_accepted" in workflow_context:
            if workflow_context["auto_fix_accepted"]:
                # Slightly lower threshold (more aggressive auto-fix)
                current = pref_data["workflow_preferences"]["auto_fix_confidence_threshold"]
                pref_data["workflow_preferences"]["auto_fix_confidence_threshold"] = max(0.85, current - 0.02)
            else:
                # Raise threshold (more conservative)
                current = pref_data["workflow_preferences"]["auto_fix_confidence_threshold"]
                pref_data["workflow_preferences"]["auto_fix_confidence_threshold"] = min(0.95, current + 0.02)

        if "parallel_execution" in workflow_context:
            pref_data["workflow_preferences"]["parallel_execution_preferred"] = workflow_context["parallel_execution"]

    def _update_quality_weights(self, pref_data: Dict[str, Any], interaction: Dict[str, Any], quality_focus: Dict[str, Any]):
        """Update quality weight preferences based on user feedback."""
        if interaction["type"] == "approval":
            # Gradually shift weights toward user's focus areas
            for dimension, importance in quality_focus.items():
                if dimension in pref_data["quality_weights"]:
                    current = pref_data["quality_weights"][dimension]
                    # Move 5% toward the target
                    pref_data["quality_weights"][dimension] = current * 0.95 + importance * 0.05

            # Normalize weights to sum to 1.0
            total = sum(pref_data["quality_weights"].values())
            if total > 0:
                for dim in pref_data["quality_weights"]:
                    pref_data["quality_weights"][dim] /= total

    def _update_communication_preferences(
        self, pref_data: Dict[str, Any], interaction: Dict[str, Any], comm_context: Dict[str, Any]
    ):
        """Update communication style preferences based on user feedback."""
        feedback = interaction["feedback"].lower()

        if "too brief" in feedback or "more detail" in feedback:
            pref_data["communication_style"]["detail_level"] = "detailed"
        elif "too detailed" in feedback or "too long" in feedback:
            pref_data["communication_style"]["detail_level"] = "brief"

        if "explain" in feedback:
            pref_data["communication_style"]["explanation_preference"] = "always"
        elif "skip explanation" in feedback:
            pref_data["communication_style"]["explanation_preference"] = "minimal"

    def _update_task_preferences(self, pref_data: Dict[str, Any], interaction: Dict[str, Any], context: Dict[str, Any]):
        """Update task and agent preferences based on user feedback."""
        task_type = context.get("task_type")
        agent_used = context.get("agent_used")

        if not pref_data["task_preferences"]["task_type_preferences"]:
            pref_data["task_preferences"]["task_type_preferences"] = {}

        if not pref_data["task_preferences"]["agent_preferences"]:
            pref_data["task_preferences"]["agent_preferences"] = {}

        # Update task type preferences
        if task_type:
            if task_type not in pref_data["task_preferences"]["task_type_preferences"]:
                pref_data["task_preferences"]["task_type_preferences"][task_type] = 0.5

            if interaction["type"] == "approval":
                pref_data["task_preferences"]["task_type_preferences"][task_type] += 0.05
            elif interaction["type"] == "rejection":
                pref_data["task_preferences"]["task_type_preferences"][task_type] -= 0.05

            # Clamp to [0, 1]
            pref_data["task_preferences"]["task_type_preferences"][task_type] = max(
                0, min(1, pref_data["task_preferences"]["task_type_preferences"][task_type])
            )

        # Update agent preferences
        if agent_used:
            if agent_used not in pref_data["task_preferences"]["agent_preferences"]:
                pref_data["task_preferences"]["agent_preferences"][agent_used] = 0.5

            if interaction["type"] == "approval":
                pref_data["task_preferences"]["agent_preferences"][agent_used] += 0.05
            elif interaction["type"] == "rejection":
                pref_data["task_preferences"]["agent_preferences"][agent_used] -= 0.05

            # Clamp to [0, 1]
            pref_data["task_preferences"]["agent_preferences"][agent_used] = max(
                0, min(1, pref_data["task_preferences"]["agent_preferences"][agent_used])
            )

    def get_preferences(self) -> Dict[str, Any]:
        """Get current user preferences."""
        return self._read_data()

    def get_coding_style_preferences(self) -> Dict[str, Any]:
        """Get coding style preferences."""
        pref_data = self._read_data()
        return pref_data["coding_style"]

    def get_workflow_preferences(self) -> Dict[str, Any]:
        """Get workflow preferences."""
        pref_data = self._read_data()
        return pref_data["workflow_preferences"]

    def get_quality_weights(self) -> Dict[str, float]:
        """Get quality dimension weights."""
        pref_data = self._read_data()
        return pref_data["quality_weights"]

    def get_communication_preferences(self) -> Dict[str, Any]:
        """Get communication style preferences."""
        pref_data = self._read_data()
        return pref_data["communication_style"]

    def should_auto_fix(self, confidence: float, category: str) -> bool:
        """
        Determine if auto-fix should be applied based on preferences.

        Args:
            confidence: Confidence score (0-1)
            category: Fix category (e.g., "breaking_changes", "security_fixes")

        Returns:
            True if auto-fix should be applied
        """
        pref_data = self._read_data()
        workflow = pref_data["workflow_preferences"]

        # Check if auto-fix is enabled
        if not workflow["auto_fix_enabled"]:
            return False

        # Check if confirmation is required for this category
        if category in workflow["confirmation_required_for"]:
            return False

        # Check confidence threshold
        return confidence >= workflow["auto_fix_confidence_threshold"]

    def get_preference_summary(self) -> Dict[str, Any]:
        """Get summary of learned preferences."""
        pref_data = self._read_data()

        summary = {
            "learning_confidence": pref_data["metadata"]["learning_confidence"],
            "total_interactions": pref_data["metadata"]["total_interactions"],
            "approval_rate": (
                pref_data["metadata"]["approvals"] / pref_data["metadata"]["total_interactions"] * 100
                if pref_data["metadata"]["total_interactions"] > 0
                else 0
            ),
            "coding_style": pref_data["coding_style"],
            "workflow_preferences": pref_data["workflow_preferences"],
            "quality_priorities": sorted(pref_data["quality_weights"].items(), key=lambda x: x[1], reverse=True),
            "top_task_preferences": (
                sorted(pref_data["task_preferences"]["task_type_preferences"].items(), key=lambda x: x[1], reverse=True)[:5]
                if pref_data["task_preferences"]["task_type_preferences"]
                else []
            ),
            "top_agent_preferences": (
                sorted(pref_data["task_preferences"]["agent_preferences"].items(), key=lambda x: x[1], reverse=True)[:5]
                if pref_data["task_preferences"]["agent_preferences"]
                else []
            ),
        }

        return summary


def main():
    """Command-line interface for testing the preference learner."""
    import argparse

    parser = argparse.ArgumentParser(description="User Preference Learner")
    parser.add_argument("--storage-dir", default=".claude-patterns", help="Storage directory")
    parser.add_argument("--action", choices=["record", "get", "summary", "should-autofix"], help="Action to perform")
    parser.add_argument("--type", help="Interaction type (approval, rejection, modification)")
    parser.add_argument("--task-id", help="Task ID")
    parser.add_argument("--feedback", help="User feedback")
    parser.add_argument("--confidence", type=float, help="Confidence score for auto-fix")
    parser.add_argument("--category", help="Fix category")

    args = parser.parse_args()

    learner = UserPreferenceLearner(args.storage_dir)

    if args.action == "record":
        if not all([args.type, args.task_id, args.feedback]):
            print("Error: --type, --task-id, and --feedback required for record")
            sys.exit(1)

        learner.record_interaction(args.type, args.task_id, args.feedback)
        print(f"Interaction recorded: {args.type}")

    elif args.action == "get":
        prefs = learner.get_preferences()
        print("User Preferences:")
        print(f"  Coding Style: {prefs['coding_style']['verbosity']}")
        print(f"  Auto-fix Threshold: {prefs['workflow_preferences']['auto_fix_confidence_threshold']:.2f}")
        print(f"  Quality Priority: {max(prefs['quality_weights'].items(), key=lambda x: x[1])[0]}")

    elif args.action == "summary":
        summary = learner.get_preference_summary()
        print("Preference Summary:")
        print(f"  Learning Confidence: {summary['learning_confidence']:.1%}")
        print(f"  Total Interactions: {summary['total_interactions']}")
        print(f"  Approval Rate: {summary['approval_rate']:.1f}%")
        print(f"  Coding Style: {summary['coding_style']['verbosity']}")

    elif args.action == "should-autofix":
        if args.confidence is None or not args.category:
            print("Error: --confidence and --category required for should-autofix")
            sys.exit(1)

        should_fix = learner.should_auto_fix(args.confidence, args.category)
        print(f"Should auto-fix: {should_fix}")

    else:
        # Show summary
        print("User Preference Learner Initialized")
        print(f"Storage: {learner.preference_file}")
        summary = learner.get_preference_summary()
        print(f"Learning Confidence: {summary['learning_confidence']:.1%}")
        print(f"Total Interactions: {summary['total_interactions']}")


if __name__ == "__main__":
    main()
