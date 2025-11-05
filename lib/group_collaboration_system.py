#!/usr/bin/env python3
"""
Group Collaboration System
Manages communication and feedback between the four agent groups
for continuous improvement and knowledge sharing.

Groups:
- Group 1: Strategic Analysis & Intelligence (The "Brain")
- Group 2: Decision Making & Planning (The "Council")
- Group 3: Execution & Implementation (The "Hand")
- Group 4: Validation & Optimization (The "Guardian")
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


class GroupCollaborationSystem:
    """
    Manages inter-group communication, feedback, and collaboration tracking.
    """

    # Group definitions with agent members
    GROUPS = {
        1: {
            "name": "Strategic Analysis & Intelligence",
            "alias": "The Brain",
            "role": "Analyze and suggest",
            "agents": [
                "code-analyzer",
                "security-auditor",
                "performance-analytics",
                "pr-reviewer",
                "learning-engine"
            ]
        },
        2: {
            "name": "Decision Making & Planning",
            "alias": "The Council",
            "role": "Evaluate and decide",
            "agents": [
                "strategic-planner",
                "preference-coordinator",
                "smart-recommender",
                "orchestrator"
            ]
        },
        3: {
            "name": "Execution & Implementation",
            "alias": "The Hand",
            "role": "Execute and implement",
            "agents": [
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
                "claude-plugin-validator",
                "background-task-manager",
                "report-management-organizer"
            ]
        },
        4: {
            "name": "Validation & Optimization",
            "alias": "The Guardian",
            "role": "Validate and optimize",
            "agents": [
                "validation-controller",
                "post-execution-validator",
                "performance-optimizer",
                "continuous-improvement"
            ]
        }
    }

    # Typical communication flows
    COMMUNICATION_FLOWS = [
        (1, 2),  # Group 1 → Group 2: Analysis to Decision
        (2, 1),  # Group 2 → Group 1: Decision to Analysis (feedback/requests)
        (2, 3),  # Group 2 → Group 3: Decision to Execution (plans)
        (3, 2),  # Group 3 → Group 2: Execution to Decision (results/issues)
        (3, 4),  # Group 3 → Group 4: Execution to Validation
        (4, 2),  # Group 4 → Group 2: Validation to Decision (approval/issues)
        (4, 3),  # Group 4 → Group 3: Validation to Execution (minor fixes)
        (4, 1),  # Group 4 → Group 1: Validation to Analysis (feedback)
    ]

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the group collaboration system.

        Args:
            storage_dir: Directory for storing collaboration data
        """
        self.storage_dir = Path(storage_dir)
        self.collab_file = self.storage_dir / "group_collaboration.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize collaboration file if it doesn't exist
        if not self.collab_file.exists():
            self._initialize_collaboration_storage()

    def _initialize_collaboration_storage(self):
        """Initialize the collaboration storage with default structure."""
        initial_data = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "metadata": {
                "total_communications": 0,
                "successful_collaborations": 0,
                "communication_by_flow": {},
                "tracking_start_date": datetime.now().isoformat()
            },
            "group_definitions": self.GROUPS,
            "communication_history": [],
            "collaboration_patterns": {
                "successful": [],
                "problematic": []
            },
            "group_interaction_matrix": self._initialize_interaction_matrix(),
            "communication_effectiveness": {},
            "knowledge_shared": []
        }

        self._write_data(initial_data)

    def _initialize_interaction_matrix(self) -> Dict[str, Dict[str, int]]:
        """Initialize interaction tracking matrix between groups."""
        matrix = {}
        for from_group in range(1, 5):
            for to_group in range(1, 5):
                if from_group != to_group:
                    key = f"G{from_group}->G{to_group}"
                    matrix[key] = {
                        "total_communications": 0,
                        "successful": 0,
                        "feedback_provided": 0,
                        "issues_raised": 0,
                        "knowledge_transferred": 0
                    }
        return matrix

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
        """Read collaboration data with file locking."""
        try:
            with open(self.collab_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    data = json.load(f)
                finally:
                    self._unlock_file(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_collaboration_storage()
            return self._read_data()

    def _write_data(self, data: Dict[str, Any]):
        """Write collaboration data with file locking."""
        with open(self.collab_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def get_agent_group(self, agent_name: str) -> Optional[int]:
        """
        Get the group number for an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Group number (1-4) or None if not found
        """
        for group_num, group_data in self.GROUPS.items():
            if agent_name in group_data["agents"]:
                return group_num
        return None

    def record_communication(
        self,
        from_agent: str,
        to_agent: str,
        task_id: str,
        communication_type: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        outcome: Optional[str] = None
    ) -> str:
        """
        Record a communication between agents (potentially in different groups).

        Args:
            from_agent: Source agent name
            to_agent: Target agent name
            task_id: Associated task ID
            communication_type: Type (recommendation, feedback, plan, result, etc.)
            message: Communication message
            data: Additional structured data
            outcome: Outcome of the communication (success, pending, issue)

        Returns:
            Communication ID
        """
        collab_data = self._read_data()

        from_group = self.get_agent_group(from_agent)
        to_group = self.get_agent_group(to_agent)

        if from_group is None or to_group is None:
            raise ValueError(f"Unknown agent: {from_agent if from_group is None else to_agent}")

        comm_id = f"comm_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        communication = {
            "comm_id": comm_id,
            "timestamp": datetime.now().isoformat(),
            "from_agent": from_agent,
            "from_group": from_group,
            "to_agent": to_agent,
            "to_group": to_group,
            "task_id": task_id,
            "communication_type": communication_type,
            "message": message,
            "data": data or {},
            "outcome": outcome or "pending",
            "flow": f"G{from_group}->G{to_group}"
        }

        collab_data["communication_history"].append(communication)

        # Update metadata
        collab_data["metadata"]["total_communications"] += 1
        collab_data["metadata"]["last_updated"] = datetime.now().isoformat()

        # Update interaction matrix
        flow_key = f"G{from_group}->G{to_group}"
        if flow_key in collab_data["group_interaction_matrix"]:
            collab_data["group_interaction_matrix"][flow_key]["total_communications"] += 1

            if communication_type == "feedback":
                collab_data["group_interaction_matrix"][flow_key]["feedback_provided"] += 1

            if outcome == "success":
                collab_data["group_interaction_matrix"][flow_key]["successful"] += 1

        # Track communication by flow
        flow_str = f"Group {from_group} → Group {to_group}"
        collab_data["metadata"]["communication_by_flow"][flow_str] = \
            collab_data["metadata"]["communication_by_flow"].get(flow_str, 0) + 1

        # Keep last 5000 communications
        if len(collab_data["communication_history"]) > 5000:
            collab_data["communication_history"] = collab_data["communication_history"][-5000:]

        self._write_data(collab_data)

        return comm_id

    def update_communication_outcome(
        self,
        comm_id: str,
        outcome: str,
        impact: Optional[str] = None
    ):
        """
        Update the outcome of a communication.

        Args:
            comm_id: Communication ID
            outcome: Outcome (success, failure, partial, etc.)
            impact: Impact description
        """
        collab_data = self._read_data()

        for comm in collab_data["communication_history"]:
            if comm["comm_id"] == comm_id:
                comm["outcome"] = outcome
                comm["outcome_timestamp"] = datetime.now().isoformat()

                if impact:
                    comm["impact"] = impact

                # Update success count in interaction matrix
                if outcome == "success":
                    flow_key = comm["flow"]
                    if flow_key in collab_data["group_interaction_matrix"]:
                        collab_data["group_interaction_matrix"][flow_key]["successful"] += 1
                        collab_data["metadata"]["successful_collaborations"] += 1

                break

        self._write_data(collab_data)

    def record_knowledge_transfer(
        self,
        from_group: int,
        to_group: int,
        knowledge_type: str,
        description: str,
        source_task: Optional[str] = None,
        impact: Optional[str] = None
    ) -> str:
        """
        Record knowledge transfer between groups.

        Args:
            from_group: Source group number (1-4)
            to_group: Target group number (1-4)
            knowledge_type: Type of knowledge (pattern, insight, best_practice, etc.)
            description: Description of knowledge transferred
            source_task: Task ID where knowledge originated
            impact: Impact of knowledge transfer

        Returns:
            Knowledge transfer ID
        """
        collab_data = self._read_data()

        kt_id = f"kt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        knowledge_transfer = {
            "kt_id": kt_id,
            "timestamp": datetime.now().isoformat(),
            "from_group": from_group,
            "to_group": to_group,
            "knowledge_type": knowledge_type,
            "description": description,
            "source_task": source_task,
            "impact": impact,
            "flow": f"G{from_group}->G{to_group}"
        }

        collab_data["knowledge_shared"].append(knowledge_transfer)

        # Update interaction matrix
        flow_key = f"G{from_group}->G{to_group}"
        if flow_key in collab_data["group_interaction_matrix"]:
            collab_data["group_interaction_matrix"][flow_key]["knowledge_transferred"] += 1

        # Keep last 1000 knowledge transfers
        if len(collab_data["knowledge_shared"]) > 1000:
            collab_data["knowledge_shared"] = collab_data["knowledge_shared"][-1000:]

        self._write_data(collab_data)

        return kt_id

    def get_group_collaboration_stats(self) -> Dict[str, Any]:
        """Get collaboration statistics for all groups."""
        collab_data = self._read_data()

        # Calculate communication effectiveness by flow
        flow_effectiveness = {}
        for flow_key, stats in collab_data["group_interaction_matrix"].items():
            total = stats["total_communications"]
            if total > 0:
                success_rate = stats["successful"] / total
                flow_effectiveness[flow_key] = {
                    "total_communications": total,
                    "success_rate": success_rate,
                    "feedback_provided": stats["feedback_provided"],
                    "knowledge_transferred": stats["knowledge_transferred"]
                }

        # Find most active flows
        most_active = sorted(
            collab_data["group_interaction_matrix"].items(),
            key=lambda x: x[1]["total_communications"],
            reverse=True
        )[:5]

        # Find most effective flows (high success rate with sufficient volume)
        effective_flows = [
            (flow, stats)
            for flow, stats in collab_data["group_interaction_matrix"].items()
            if stats["total_communications"] >= 5
        ]
        most_effective = sorted(
            effective_flows,
            key=lambda x: x[1]["successful"] / x[1]["total_communications"] if x[1]["total_communications"] > 0 else 0,
            reverse=True
        )[:5]

        return {
            "total_communications": collab_data["metadata"]["total_communications"],
            "successful_collaborations": collab_data["metadata"]["successful_collaborations"],
            "communication_by_flow": collab_data["metadata"]["communication_by_flow"],
            "flow_effectiveness": flow_effectiveness,
            "most_active_flows": [
                {
                    "flow": flow,
                    "total": stats["total_communications"],
                    "successful": stats["successful"]
                }
                for flow, stats in most_active
            ],
            "most_effective_flows": [
                {
                    "flow": flow,
                    "success_rate": stats["successful"] / stats["total_communications"] if stats["total_communications"] > 0 else 0,
                    "total": stats["total_communications"]
                }
                for flow, stats in most_effective
            ],
            "knowledge_transfers": len(collab_data["knowledge_shared"])
        }

    def get_group_performance_summary(self, group_num: int) -> Dict[str, Any]:
        """
        Get performance summary for a specific group.

        Args:
            group_num: Group number (1-4)

        Returns:
            Performance summary
        """
        collab_data = self._read_data()

        if group_num not in self.GROUPS:
            raise ValueError(f"Invalid group number: {group_num}")

        group_info = self.GROUPS[group_num]

        # Count communications from/to this group
        from_count = sum(
            1 for comm in collab_data["communication_history"]
            if comm["from_group"] == group_num
        )

        to_count = sum(
            1 for comm in collab_data["communication_history"]
            if comm["to_group"] == group_num
        )

        # Count successful communications
        successful_from = sum(
            1 for comm in collab_data["communication_history"]
            if comm["from_group"] == group_num and comm["outcome"] == "success"
        )

        successful_to = sum(
            1 for comm in collab_data["communication_history"]
            if comm["to_group"] == group_num and comm["outcome"] == "success"
        )

        # Knowledge transfers
        knowledge_provided = sum(
            1 for kt in collab_data["knowledge_shared"]
            if kt["from_group"] == group_num
        )

        knowledge_received = sum(
            1 for kt in collab_data["knowledge_shared"]
            if kt["to_group"] == group_num
        )

        return {
            "group_number": group_num,
            "group_name": group_info["name"],
            "group_alias": group_info["alias"],
            "role": group_info["role"],
            "agents": group_info["agents"],
            "communications": {
                "sent": from_count,
                "received": to_count,
                "total": from_count + to_count
            },
            "success_rates": {
                "outgoing": successful_from / from_count if from_count > 0 else 0,
                "incoming": successful_to / to_count if to_count > 0 else 0
            },
            "knowledge_transfers": {
                "provided": knowledge_provided,
                "received": knowledge_received,
                "net": knowledge_provided - knowledge_received
            }
        }

    def get_recent_communications(
        self,
        group_num: Optional[int] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get recent communications, optionally filtered by group.

        Args:
            group_num: Optional group number to filter (1-4)
            limit: Maximum number of communications to return

        Returns:
            List of recent communications
        """
        collab_data = self._read_data()

        comms = collab_data["communication_history"]

        if group_num is not None:
            comms = [
                comm for comm in comms
                if comm["from_group"] == group_num or comm["to_group"] == group_num
            ]

        # Sort by timestamp (most recent first)
        comms.sort(key=lambda x: x["timestamp"], reverse=True)

        return comms[:limit]

    def analyze_collaboration_patterns(self) -> Dict[str, Any]:
        """
        Analyze collaboration patterns to identify successful and problematic patterns.

        Returns:
            Analysis of collaboration patterns
        """
        collab_data = self._read_data()

        # Group communications by task
        task_comms = defaultdict(list)
        for comm in collab_data["communication_history"]:
            task_comms[comm["task_id"]].append(comm)

        # Analyze successful collaboration patterns
        successful_patterns = []
        problematic_patterns = []

        for task_id, comms in task_comms.items():
            if not comms:
                continue

            # Calculate success rate for this task
            total = len(comms)
            successful = sum(1 for c in comms if c["outcome"] == "success")
            success_rate = successful / total if total > 0 else 0

            # Extract communication flow pattern
            flow_pattern = " → ".join([f"G{c['from_group']}" for c in comms] + [f"G{comms[-1]['to_group']}"])

            pattern_data = {
                "task_id": task_id,
                "flow_pattern": flow_pattern,
                "total_communications": total,
                "success_rate": success_rate,
                "communication_types": [c["communication_type"] for c in comms]
            }

            if success_rate >= 0.80:
                successful_patterns.append(pattern_data)
            elif success_rate < 0.50:
                problematic_patterns.append(pattern_data)

        # Find common successful patterns
        pattern_frequency = defaultdict(int)
        for pattern in successful_patterns:
            pattern_frequency[pattern["flow_pattern"]] += 1

        common_successful = sorted(
            pattern_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            "successful_patterns": successful_patterns[:10],
            "problematic_patterns": problematic_patterns[:10],
            "common_successful_flows": [
                {"flow": flow, "frequency": freq}
                for flow, freq in common_successful
            ],
            "insights": self._generate_collaboration_insights(
                successful_patterns,
                problematic_patterns
            )
        }

    def _generate_collaboration_insights(
        self,
        successful: List[Dict],
        problematic: List[Dict]
    ) -> List[str]:
        """Generate insights from collaboration patterns."""
        insights = []

        if successful:
            avg_success_rate = sum(p["success_rate"] for p in successful) / len(successful)
            insights.append(
                f"Successful collaborations achieve {avg_success_rate*100:.0f}% success rate on average"
            )

        if problematic:
            avg_problem_rate = sum(p["success_rate"] for p in problematic) / len(problematic)
            insights.append(
                f"Problematic collaborations have {avg_problem_rate*100:.0f}% success rate - require attention"
            )

        # Find most common flow patterns
        if successful:
            flows = [p["flow_pattern"] for p in successful]
            if flows:
                most_common = max(set(flows), key=flows.count)
                insights.append(f"Most successful collaboration flow: {most_common}")

        return insights


def main():
    """Command-line interface for testing the collaboration system."""
    import argparse

    parser = argparse.ArgumentParser(description='Group Collaboration System')
    parser.add_argument('--storage-dir', default='.claude-patterns', help='Storage directory')
    parser.add_argument('--action', choices=['record', 'stats', 'group', 'recent', 'analyze'],
                       help='Action to perform')
    parser.add_argument('--from-agent', help='Source agent')
    parser.add_argument('--to-agent', help='Target agent')
    parser.add_argument('--task-id', help='Task ID')
    parser.add_argument('--message', help='Communication message')
    parser.add_argument('--type', default='feedback', help='Communication type')
    parser.add_argument('--group', type=int, help='Group number (1-4)')

    args = parser.parse_args()

    system = GroupCollaborationSystem(args.storage_dir)

    if args.action == 'record':
        if not all([args.from_agent, args.to_agent, args.message, args.task_id]):
            print("Error: --from-agent, --to-agent, --message, and --task-id required for record")
            sys.exit(1)

        comm_id = system.record_communication(
            args.from_agent,
            args.to_agent,
            args.task_id,
            args.type,
            args.message
        )
        print(f"Communication recorded: {comm_id}")

    elif args.action == 'stats':
        stats = system.get_group_collaboration_stats()
        print("Group Collaboration Statistics:")
        print(f"  Total Communications: {stats['total_communications']}")
        print(f"  Successful: {stats['successful_collaborations']}")
        print(f"  Knowledge Transfers: {stats['knowledge_transfers']}")
        print("\nMost Active Flows:")
        for flow in stats['most_active_flows'][:3]:
            print(f"  {flow['flow']}: {flow['total']} communications")

    elif args.action == 'group':
        if not args.group:
            print("Error: --group required for group action")
            sys.exit(1)

        summary = system.get_group_performance_summary(args.group)
        print(f"Group {summary['group_number']}: {summary['group_name']}")
        print(f"  Alias: {summary['group_alias']}")
        print(f"  Role: {summary['role']}")
        print(f"  Communications: {summary['communications']['total']}")
        print(f"  Success Rate (outgoing): {summary['success_rates']['outgoing']*100:.1f}%")

    elif args.action == 'recent':
        comms = system.get_recent_communications(args.group, limit=10)
        print(f"Recent Communications ({len(comms)}):")
        for comm in comms:
            print(f"  [{comm['communication_type']}] {comm['from_agent']} → {comm['to_agent']}")
            print(f"    {comm['message'][:80]}...")

    elif args.action == 'analyze':
        analysis = system.analyze_collaboration_patterns()
        print("Collaboration Pattern Analysis:")
        print(f"  Successful Patterns: {len(analysis['successful_patterns'])}")
        print(f"  Problematic Patterns: {len(analysis['problematic_patterns'])}")
        print("\nInsights:")
        for insight in analysis['insights']:
            print(f"  - {insight}")

    else:
        # Show summary
        print("Group Collaboration System Initialized")
        print(f"Storage: {system.collab_file}")
        stats = system.get_group_collaboration_stats()
        print(f"Total Communications: {stats['total_communications']}")


if __name__ == '__main__':
    main()
