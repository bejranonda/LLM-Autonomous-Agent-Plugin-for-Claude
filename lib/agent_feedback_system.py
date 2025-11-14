#!/usr/bin/env python3
"""
Agent Feedback System
Enables explicit feedback exchange between analysis and execution agents
for continuous improvement and knowledge sharing.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Platform-specific imports for file locking
try:
    import msvcrt  # Windows

    PLATFORM = "windows"
except ImportError:
    import fcntl  # Unix/Linux/Mac

    PLATFORM = "unix"


class AgentFeedbackSystem:
    """
    Manages feedback exchange between agent groups for continuous improvement.

    Group 1 (Analysis): code-analyzer, smart-recommender, security-auditor,
                       performance-analytics, pr-reviewer
    Group 2 (Execution): quality-controller, test-engineer, frontend-analyzer,
                        documentation-generator, build-validator, git-repository-manager
    """

    # Agent group classifications
    ANALYSIS_AGENTS = {
        "code-analyzer",
        "smart-recommender",
        "security-auditor",
        "performance-analytics",
        "pr-reviewer",
        "learning-engine",
        "validation-controller",
    }

    EXECUTION_AGENTS = {
        "quality-controller",
        "test-engineer",
        "frontend-analyzer",
        "documentation-generator",
        "build-validator",
        "git-repository-manager",
        "api-contract-validator",
        "gui-validator",
        "dev-orchestrator",
        "version-release-manager",
        "workspace-organizer",
        "report-management-organizer",
        "background-task-manager",
        "claude-plugin-validator",
    }

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the agent feedback system.

        Args:
            storage_dir: Directory for storing feedback data
        """
        self.storage_dir = Path(storage_dir)
        self.feedback_file = self.storage_dir / "agent_feedback.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize feedback file if it doesn't exist
        if not self.feedback_file.exists():
            self._initialize_feedback_storage()

    def _initialize_feedback_storage(self):
        """Initialize the feedback storage with default structure."""
        initial_data = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "metadata": {
                "total_feedbacks": 0,
                "analysis_to_execution": 0,
                "execution_to_analysis": 0,
                "cross_agent_learnings": 0,
            },
            "feedback_exchanges": [],
            "learning_insights": {"common_patterns": [], "successful_collaborations": [], "improvement_areas": []},
            "agent_collaboration_matrix": {},
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
        """Read feedback data with file locking."""
        try:
            with open(self.feedback_file, "r", encoding="utf-8") as f:
                self._lock_file(f)
                try:
                    data = json.load(f)
                finally:
                    self._unlock_file(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_feedback_storage()
            return self._read_data()

    def _write_data(self, data: Dict[str, Any]):
        """Write feedback data with file locking."""
        with open(self.feedback_file, "w", encoding="utf-8") as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def add_feedback(
        self,
        from_agent: str,
        to_agent: str,
        task_id: str,
        feedback_type: str,
        message: str,
        impact: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    )-> str:
        """Add Feedback."""
        """
        Add feedback from one agent to another.

        Args:
            from_agent: Source agent name
            to_agent: Target agent name
            task_id: Associated task/pattern ID
            feedback_type: Type of feedback (improvement, success, warning, error)
            message: Feedback message
            impact: Impact description (e.g., "quality_score +8 points")
            data: Additional structured data

        Returns:
            Feedback ID
        """
        feedback_data = self._read_data()

        feedback_id = f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        feedback_entry = {
            "feedback_id": feedback_id,
            "from_agent": from_agent,
            "to_agent": to_agent,
            "task_id": task_id,
            "feedback_type": feedback_type,
            "message": message,
            "impact": impact,
            "data": data or {},
            "timestamp": datetime.now().isoformat(),
            "read": False,
            "applied": False,
        }

        feedback_data["feedback_exchanges"].append(feedback_entry)

        # Update metadata
        feedback_data["metadata"]["total_feedbacks"] += 1
        feedback_data["metadata"]["last_updated"] = datetime.now().isoformat()

        # Track direction
        if from_agent in self.ANALYSIS_AGENTS and to_agent in self.EXECUTION_AGENTS:
            feedback_data["metadata"]["analysis_to_execution"] += 1
        elif from_agent in self.EXECUTION_AGENTS and to_agent in self.ANALYSIS_AGENTS:
            feedback_data["metadata"]["execution_to_analysis"] += 1
        else:
            feedback_data["metadata"]["cross_agent_learnings"] += 1

        # Update collaboration matrix
        collab_key = f"{from_agent}->{to_agent}"
        if collab_key not in feedback_data["agent_collaboration_matrix"]:
            feedback_data["agent_collaboration_matrix"][collab_key] = {
                "total_feedbacks": 0,
                "feedback_types": defaultdict(int),
                "avg_impact_score": 0,
            }

        feedback_data["agent_collaboration_matrix"][collab_key]["total_feedbacks"] += 1

        self._write_data(feedback_data)

        return feedback_id

    def get_feedback_for_agent(self, agent_name: str, unread_only: bool = True, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get feedback addressed to a specific agent.

        Args:
            agent_name: Target agent name
            unread_only: Only return unread feedback
            limit: Maximum number of feedback items

        Returns:
            List of feedback entries
        """
        feedback_data = self._read_data()

        feedbacks = [
            fb
            for fb in feedback_data["feedback_exchanges"]
            if fb["to_agent"] == agent_name and (not unread_only or not fb["read"])
        ]

        # Sort by timestamp (most recent first)
        feedbacks.sort(key=lambda x: x["timestamp"], reverse=True)

        return feedbacks[:limit]

    def mark_feedback_read(self, feedback_id: str):
        """Mark feedback as read."""
        feedback_data = self._read_data()

        for fb in feedback_data["feedback_exchanges"]:
            if fb["feedback_id"] == feedback_id:
                fb["read"] = True
                break

        self._write_data(feedback_data)

    def mark_feedback_applied(self, feedback_id: str):
        """Mark feedback as applied/acted upon."""
        feedback_data = self._read_data()

        for fb in feedback_data["feedback_exchanges"]:
            if fb["feedback_id"] == feedback_id:
                fb["applied"] = True
                fb["applied_at"] = datetime.now().isoformat()
                break

        self._write_data(feedback_data)

    def get_collaboration_stats(self) -> Dict[str, Any]:
        """Get agent collaboration statistics."""
        feedback_data = self._read_data()

        stats = {
            "total_feedbacks": feedback_data["metadata"]["total_feedbacks"],
            "analysis_to_execution": feedback_data["metadata"]["analysis_to_execution"],
            "execution_to_analysis": feedback_data["metadata"]["execution_to_analysis"],
            "cross_agent_learnings": feedback_data["metadata"]["cross_agent_learnings"],
            "collaboration_matrix": feedback_data["agent_collaboration_matrix"],
            "most_active_pairs": self._get_most_active_pairs(feedback_data),
            "feedback_effectiveness": self._calculate_feedback_effectiveness(feedback_data),
        }

        return stats

    def _get_most_active_pairs(self, feedback_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get most active agent collaboration pairs."""
        pairs = []

        for pair, data in feedback_data["agent_collaboration_matrix"].items():
            pairs.append({"pair": pair, "total_feedbacks": data["total_feedbacks"]})

        return sorted(pairs, key=lambda x: x["total_feedbacks"], reverse=True)[:5]

    def _calculate_feedback_effectiveness(self, feedback_data: Dict[str, Any]) -> float:
        """Calculate feedback effectiveness (% applied)."""
        total = len(feedback_data["feedback_exchanges"])
        if total == 0:
            return 0.0

        applied = sum(1 for fb in feedback_data["feedback_exchanges"] if fb.get("applied", False))
        return (applied / total) * 100

    def add_learning_insight(
        self, insight_type: str, description: str, agents_involved: List[str], impact: Optional[str] = None
    ):
        """Add Learning Insight."""
        """
        Add a learning insight from agent collaboration.

        Args:
            insight_type: Type (common_pattern, successful_collaboration, improvement_area)
            description: Insight description
            agents_involved: List of agents involved
            impact: Impact description
        """
        feedback_data = self._read_data()

        insight = {
            "insight_id": f"insight_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": insight_type,
            "description": description,
            "agents_involved": agents_involved,
            "impact": impact,
            "timestamp": datetime.now().isoformat(),
        }

        if insight_type not in feedback_data["learning_insights"]:
            feedback_data["learning_insights"][insight_type] = []

        feedback_data["learning_insights"][insight_type].append(insight)

        self._write_data(feedback_data)

    def get_insights(self, insight_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get learning insights, optionally filtered by type."""
        feedback_data = self._read_data()

        if insight_type:
            return feedback_data["learning_insights"].get(insight_type, [])

        # Return all insights combined
        all_insights = []
        for insights in feedback_data["learning_insights"].values():
            all_insights.extend(insights)

        return sorted(all_insights, key=lambda x: x["timestamp"], reverse=True)


def main():
    """Command-line interface for testing the feedback system."""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Feedback System")
    parser.add_argument("--storage-dir", default=".claude-patterns", help="Storage directory")
    parser.add_argument("--action", choices=["add", "get", "stats", "insights"], help="Action to perform")
    parser.add_argument("--from-agent", help="Source agent")
    parser.add_argument("--to-agent", help="Target agent")
    parser.add_argument("--message", help="Feedback message")
    parser.add_argument("--task-id", help="Task ID")
    parser.add_argument("--type", default="improvement", help="Feedback type")

    args = parser.parse_args()

    system = AgentFeedbackSystem(args.storage_dir)

    if args.action == "add":
        if not all([args.from_agent, args.to_agent, args.message, args.task_id]):
            print("Error: --from-agent, --to-agent, --message, and --task-id required for add")
            sys.exit(1)

        feedback_id = system.add_feedback(args.from_agent, args.to_agent, args.task_id, args.type, args.message)
        print(f"Feedback added: {feedback_id}")

    elif args.action == "get":
        if not args.to_agent:
            print("Error: --to-agent required for get")
            sys.exit(1)

        feedbacks = system.get_feedback_for_agent(args.to_agent)
        print(f"Feedback for {args.to_agent}:")
        for fb in feedbacks:
            print(f"  [{fb['feedback_type']}] From {fb['from_agent']}: {fb['message']}")

    elif args.action == "stats":
        stats = system.get_collaboration_stats()
        print(f"Collaboration Statistics:")
        print(f"  Total Feedbacks: {stats['total_feedbacks']}")
        print(f"  Analysis → Execution: {stats['analysis_to_execution']}")
        print(f"  Execution → Analysis: {stats['execution_to_analysis']}")
        print(f"  Feedback Effectiveness: {stats['feedback_effectiveness']:.1f}%")

    elif args.action == "insights":
        insights = system.get_insights()
        print(f"Learning Insights ({len(insights)} total):")
        for insight in insights[:5]:
            print(f"  [{insight['type']}] {insight['description']}")

    else:
        # Show summary
        print("Agent Feedback System Initialized")
        print(f"Storage: {system.feedback_file}")
        stats = system.get_collaboration_stats()
        print(f"Total Feedbacks: {stats['total_feedbacks']}")


if __name__ == "__main__":
    main()
