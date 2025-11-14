#!/usr/bin/env python3
"""
Inter-Group Knowledge Transfer System
Automatically propagates knowledge, patterns, and insights between the four agent groups
for accelerated learning and continuous improvement.

Groups:
- Group 1: Strategic Analysis & Intelligence
- Group 2: Decision Making & Planning
- Group 3: Execution & Implementation
- Group 4: Validation & Optimization
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict

# Platform-specific imports for file locking
try:
    import msvcrt  # Windows

    PLATFORM = "windows"
except ImportError:
    import fcntl  # Unix/Linux/Mac

    PLATFORM = "unix"


class InterGroupKnowledgeTransfer:
    """
    Manages automatic knowledge propagation between agent groups.
    """

    # Group definitions
    GROUPS = {
        1: "Strategic Analysis & Intelligence",
        2: "Decision Making & Planning",
        3: "Execution & Implementation",
        4: "Validation & Optimization",
    }

    # Knowledge types that can be transferred
    KNOWLEDGE_TYPES = [
        "pattern",  # Successful approach pattern
        "anti_pattern",  # Failed approach to avoid
        "best_practice",  # Best practice discovered
        "optimization",  # Optimization technique
        "user_preference",  # User preference insight
        "technical_insight",  # Technical discovery
        "workflow_improvement",  # Workflow optimization
        "quality_indicator",  # Quality indicator discovered
        "risk_pattern",  # Risk pattern identified
        "performance_tip",  # Performance improvement tip
    ]

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the knowledge transfer system.

        Args:
            storage_dir: Directory for storing knowledge data
        """
        self.storage_dir = Path(storage_dir)
        self.knowledge_file = self.storage_dir / "inter_group_knowledge.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize knowledge file if it doesn't exist
        if not self.knowledge_file.exists():
            self._initialize_knowledge_storage()

    def _initialize_knowledge_storage(self):
        """Initialize the knowledge storage with default structure."""
        initial_data = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "metadata": {
                "total_knowledge_items": 0,
                "successful_transfers": 0,
                "transfer_success_rate": 0,
                "tracking_start_date": datetime.now().isoformat(),
            },
            "knowledge_base": [],
            "transfer_history": [],
            "group_expertise": {
                "1": {"specializations": [], "key_insights": []},
                "2": {"specializations": [], "key_insights": []},
                "3": {"specializations": [], "key_insights": []},
                "4": {"specializations": [], "key_insights": []},
            },
            "knowledge_flows": {
                "G1->G2": {"total": 0, "successful": 0},
                "G1->G3": {"total": 0, "successful": 0},
                "G1->G4": {"total": 0, "successful": 0},
                "G2->G1": {"total": 0, "successful": 0},
                "G2->G3": {"total": 0, "successful": 0},
                "G2->G4": {"total": 0, "successful": 0},
                "G3->G1": {"total": 0, "successful": 0},
                "G3->G2": {"total": 0, "successful": 0},
                "G3->G4": {"total": 0, "successful": 0},
                "G4->G1": {"total": 0, "successful": 0},
                "G4->G2": {"total": 0, "successful": 0},
                "G4->G3": {"total": 0, "successful": 0},
            },
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
                pass
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)

    def _read_data(self) -> Dict[str, Any]:
        """Read knowledge data with file locking."""
        try:
            with open(self.knowledge_file, "r", encoding="utf-8") as f:
                self._lock_file(f)
                try:
                    data = json.load(f)
                finally:
                    self._unlock_file(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_knowledge_storage()
            return self._read_data()

    def _write_data(self, data: Dict[str, Any]):
        """Write knowledge data with file locking."""
        with open(self.knowledge_file, "w", encoding="utf-8") as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def add_knowledge(
        self,
        source_group: int,
        knowledge_type: str,
        title: str,
        description: str,
        context: Optional[Dict[str, Any]] = None,
        evidence: Optional[Dict[str, Any]] = None,
        applicable_to_groups: Optional[List[int]] = None,
    )-> str:
        """Add Knowledge."""
        """
        Add new knowledge to the system.

        Args:
            source_group: Group that discovered this knowledge (1-4)
            knowledge_type: Type of knowledge
            title: Short title
            description: Detailed description
            context: Context in which this knowledge was discovered
            evidence: Supporting evidence (metrics, examples)
            applicable_to_groups: Which groups this knowledge applies to

        Returns:
            Knowledge ID
        """
        if knowledge_type not in self.KNOWLEDGE_TYPES:
            raise ValueError(f"Invalid knowledge type: {knowledge_type}")

        knowledge_data = self._read_data()

        knowledge_id = f"knowledge_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        knowledge_item = {
            "knowledge_id": knowledge_id,
            "source_group": source_group,
            "knowledge_type": knowledge_type,
            "title": title,
            "description": description,
            "context": context or {},
            "evidence": evidence or {},
            "applicable_to_groups": applicable_to_groups or [1, 2, 3, 4],
            "created_at": datetime.now().isoformat(),
            "application_count": 0,
            "success_count": 0,
            "confidence_score": 0.5,  # Starts at 50%, improves with applications
            "last_applied": None,
        }

        knowledge_data["knowledge_base"].append(knowledge_item)

        # Update metadata
        knowledge_data["metadata"]["total_knowledge_items"] += 1
        knowledge_data["metadata"]["last_updated"] = datetime.now().isoformat()

        # Keep last 5000 knowledge items
        if len(knowledge_data["knowledge_base"]) > 5000:
            knowledge_data["knowledge_base"] = knowledge_data["knowledge_base"][-5000:]

        self._write_data(knowledge_data)

        # Automatically trigger knowledge transfer to applicable groups
        self._trigger_automatic_transfer(knowledge_id, applicable_to_groups or [1, 2, 3, 4])

        return knowledge_id

    def _trigger_automatic_transfer(self, knowledge_id: str, target_groups: List[int]):
        """Automatically transfer knowledge to target groups."""
        knowledge_data = self._read_data()

        # Find the knowledge item
        knowledge_item = None
        for item in knowledge_data["knowledge_base"]:
            if item["knowledge_id"] == knowledge_id:
                knowledge_item = item
                break

        if not knowledge_item:
            return

        source_group = knowledge_item["source_group"]

        # Transfer to each target group
        for target_group in target_groups:
            if target_group != source_group:
                self._record_transfer(
                    knowledge_id=knowledge_id,
                    from_group=source_group,
                    to_group=target_group,
                    knowledge_type=knowledge_item["knowledge_type"],
                    title=knowledge_item["title"],
                )

    def _record_transfer(self, knowledge_id: str, from_group: int, to_group: int, knowledge_type: str, title: str):
        """Record a knowledge transfer between groups."""
        knowledge_data = self._read_data()

        transfer_record = {
            "transfer_id": f"transfer_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "knowledge_id": knowledge_id,
            "from_group": from_group,
            "to_group": to_group,
            "knowledge_type": knowledge_type,
            "title": title,
            "transferred_at": datetime.now().isoformat(),
            "applied": False,
            "success": None,
        }

        knowledge_data["transfer_history"].append(transfer_record)

        # Update knowledge flows
        flow_key = f"G{from_group}->G{to_group}"
        if flow_key in knowledge_data["knowledge_flows"]:
            knowledge_data["knowledge_flows"][flow_key]["total"] += 1

        # Keep last 10000 transfer records
        if len(knowledge_data["transfer_history"]) > 10000:
            knowledge_data["transfer_history"] = knowledge_data["transfer_history"][-10000:]

        self._write_data(knowledge_data)

    def record_knowledge_application(
        self,
        knowledge_id: str,
        applied_by_group: int,
        success: bool,
        impact: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        """Record Knowledge Application."""
        """
        Record that knowledge was applied by a group.

        Args:
            knowledge_id: ID of knowledge that was applied
            applied_by_group: Group that applied the knowledge
            success: Whether application was successful
            impact: Impact description (e.g., "quality +10 points")
            notes: Additional notes
        """
        knowledge_data = self._read_data()

        # Update knowledge item
        for item in knowledge_data["knowledge_base"]:
            if item["knowledge_id"] == knowledge_id:
                item["application_count"] += 1
                if success:
                    item["success_count"] += 1

                # Update confidence score based on success rate
                success_rate = item["success_count"] / item["application_count"]
                # Confidence increases with successful applications
                item["confidence_score"] = min(0.95, success_rate * 0.8 + 0.15)

                item["last_applied"] = datetime.now().isoformat()
                break

        # Update transfer history
        for transfer in knowledge_data["transfer_history"]:
            if transfer["knowledge_id"] == knowledge_id and transfer["to_group"] == applied_by_group:
                transfer["applied"] = True
                transfer["success"] = success
                transfer["applied_at"] = datetime.now().isoformat()
                transfer["impact"] = impact
                transfer["notes"] = notes

                # Update knowledge flows
                if success:
                    flow_key = f"G{transfer['from_group']}->G{transfer['to_group']}"
                    if flow_key in knowledge_data["knowledge_flows"]:
                        knowledge_data["knowledge_flows"][flow_key]["successful"] += 1

        # Update metadata
        if success:
            knowledge_data["metadata"]["successful_transfers"] += 1

        total_transfers = sum(flow["total"] for flow in knowledge_data["knowledge_flows"].values())
        successful_transfers = sum(flow["successful"] for flow in knowledge_data["knowledge_flows"].values())
        knowledge_data["metadata"]["transfer_success_rate"] = (
            successful_transfers / total_transfers if total_transfers > 0 else 0
        )

        self._write_data(knowledge_data)

    def query_knowledge(
        self, for_group: int, knowledge_type: Optional[str] = None, min_confidence: float = 0.7, limit: int = 10
    )-> List[Dict[str, Any]]:
        """Query Knowledge."""
        """
        Query knowledge relevant to a specific group.

        Args:
            for_group: Group requesting knowledge
            knowledge_type: Optional filter by type
            min_confidence: Minimum confidence score
            limit: Maximum results

        Returns:
            List of relevant knowledge items
        """
        knowledge_data = self._read_data()

        # Filter knowledge
        relevant_knowledge = []
        for item in knowledge_data["knowledge_base"]:
            # Check if applicable to this group
            if for_group not in item["applicable_to_groups"]:
                continue

            # Check confidence threshold
            if item["confidence_score"] < min_confidence:
                continue

            # Check knowledge type filter
            if knowledge_type and item["knowledge_type"] != knowledge_type:
                continue

            relevant_knowledge.append(item)

        # Sort by confidence score (highest first)
        relevant_knowledge.sort(key=lambda x: (x["confidence_score"], x["application_count"]), reverse=True)

        return relevant_knowledge[:limit]

    def get_group_expertise(self, group_num: int) -> Dict[str, Any]:
        """Get expertise profile for a group."""
        knowledge_data = self._read_data()

        if str(group_num) not in knowledge_data["group_expertise"]:
            return {"group": group_num, "specializations": [], "key_insights": []}

        # Find knowledge originated from this group
        group_knowledge = [
            k for k in knowledge_data["knowledge_base"] if k["source_group"] == group_num and k["confidence_score"] >= 0.8
        ]

        # Count by knowledge type
        type_counts = defaultdict(int)
        for k in group_knowledge:
            type_counts[k["knowledge_type"]] += 1

        # Top specializations
        specializations = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        # Top insights (highest confidence)
        key_insights = sorted(group_knowledge, key=lambda x: x["confidence_score"], reverse=True)[:5]

        return {
            "group": group_num,
            "group_name": self.GROUPS[group_num],
            "total_knowledge_created": len(group_knowledge),
            "specializations": [{"type": spec[0], "count": spec[1]} for spec in specializations],
            "key_insights": [
                {
                    "title": k["title"],
                    "type": k["knowledge_type"],
                    "confidence": k["confidence_score"],
                    "applications": k["application_count"],
                }
                for k in key_insights
            ],
        }

    def get_knowledge_flow_analysis(self) -> Dict[str, Any]:
        """Analyze knowledge flow patterns between groups."""
        knowledge_data = self._read_data()

        # Calculate success rates by flow
        flow_analysis = {}
        for flow_key, stats in knowledge_data["knowledge_flows"].items():
            if stats["total"] > 0:
                success_rate = stats["successful"] / stats["total"]
                flow_analysis[flow_key] = {
                    "total_transfers": stats["total"],
                    "successful_transfers": stats["successful"],
                    "success_rate": success_rate,
                    "effectiveness": "High" if success_rate >= 0.8 else "Medium" if success_rate >= 0.6 else "Low",
                }

        # Find most effective flows
        effective_flows = [
            (flow, analysis)
            for flow, analysis in flow_analysis.items()
            if analysis["total_transfers"] >= 3 and analysis["success_rate"] >= 0.75
        ]
        effective_flows.sort(key=lambda x: x[1]["success_rate"], reverse=True)

        # Find knowledge types that transfer well
        type_success = defaultdict(lambda: {"total": 0, "successful": 0})
        for transfer in knowledge_data["transfer_history"]:
            if transfer["applied"]:
                k_type = transfer["knowledge_type"]
                type_success[k_type]["total"] += 1
                if transfer["success"]:
                    type_success[k_type]["successful"] += 1

        knowledge_type_effectiveness = {}
        for k_type, stats in type_success.items():
            if stats["total"] >= 2:
                success_rate = stats["successful"] / stats["total"]
                knowledge_type_effectiveness[k_type] = {"total": stats["total"], "success_rate": success_rate}

        return {
            "overall_transfer_success_rate": knowledge_data["metadata"]["transfer_success_rate"],
            "total_transfers": sum(stats["total"] for stats in knowledge_data["knowledge_flows"].values()),
            "successful_transfers": sum(stats["successful"] for stats in knowledge_data["knowledge_flows"].values()),
            "flow_analysis": flow_analysis,
            "most_effective_flows": [{"flow": flow, **analysis} for flow, analysis in effective_flows[:5]],
            "knowledge_type_effectiveness": knowledge_type_effectiveness,
        }

    def suggest_knowledge_for_task(
        self, for_group: int, task_type: str, task_context: Optional[Dict[str, Any]] = None
    )-> List[Dict[str, Any]]:
        """Suggest Knowledge For Task."""
        """
        Suggest relevant knowledge for a specific task.

        Args:
            for_group: Group performing the task
            task_type: Type of task
            task_context: Additional task context

        Returns:
            List of suggested knowledge items
        """
        # Query high-confidence knowledge
        knowledge = self.query_knowledge(for_group=for_group, min_confidence=0.75, limit=20)

        # Score relevance to task
        scored_knowledge = []
        for item in knowledge:
            relevance_score = 0

            # Direct task type match
            if task_type in item.get("context", {}).get("task_types", []):
                relevance_score += 0.5

            # Context match
            if task_context:
                item_context = item.get("context", {})
                for key, value in task_context.items():
                    if key in item_context and item_context[key] == value:
                        relevance_score += 0.1

            # Confidence bonus
            relevance_score += item["confidence_score"] * 0.3

            # Recent application bonus
            if item["last_applied"]:
                last_applied = datetime.fromisoformat(item["last_applied"])
                days_ago = (datetime.now() - last_applied).days
                if days_ago < 7:
                    relevance_score += 0.1

            scored_knowledge.append({"knowledge_item": item, "relevance_score": relevance_score})

        # Sort by relevance
        scored_knowledge.sort(key=lambda x: x["relevance_score"], reverse=True)

        return [
            {
                "title": item["knowledge_item"]["title"],
                "description": item["knowledge_item"]["description"],
                "type": item["knowledge_item"]["knowledge_type"],
                "confidence": item["knowledge_item"]["confidence_score"],
                "relevance": item["relevance_score"],
                "evidence": item["knowledge_item"]["evidence"],
            }
            for item in scored_knowledge[:5]
        ]


def main():
    """Command-line interface for testing the knowledge transfer system."""
    import argparse

    parser = argparse.ArgumentParser(description="Inter-Group Knowledge Transfer")
    parser.add_argument("--storage-dir", default=".claude-patterns", help="Storage directory")
    parser.add_argument("--action", choices=["add", "query", "apply", "flows", "expertise"], help="Action to perform")
    parser.add_argument("--group", type=int, help="Group number (1-4)")
    parser.add_argument("--type", help="Knowledge type")
    parser.add_argument("--title", help="Knowledge title")
    parser.add_argument("--description", help="Knowledge description")
    parser.add_argument("--knowledge-id", help="Knowledge ID")
    parser.add_argument("--success", action="store_true", help="Application was successful")

    args = parser.parse_args()

    system = InterGroupKnowledgeTransfer(args.storage_dir)

    if args.action == "add":
        if not all([args.group, args.type, args.title, args.description]):
            print("Error: --group, --type, --title, and --description required for add")
            sys.exit(1)

        knowledge_id = system.add_knowledge(
            source_group=args.group, knowledge_type=args.type, title=args.title, description=args.description
        )
        print(f"Knowledge added: {knowledge_id}")

    elif args.action == "query":
        if not args.group:
            print("Error: --group required for query")
            sys.exit(1)

        knowledge = system.query_knowledge(for_group=args.group, knowledge_type=args.type)
        print(f"Relevant knowledge for Group {args.group} ({len(knowledge)} items):")
        for k in knowledge:
            print(f"  [{k['knowledge_type']}] {k['title']} (confidence: {k['confidence_score']:.2f})")

    elif args.action == "apply":
        if not all([args.knowledge_id, args.group]):
            print("Error: --knowledge-id and --group required for apply")
            sys.exit(1)

        system.record_knowledge_application(knowledge_id=args.knowledge_id, applied_by_group=args.group, success=args.success)
        print(f"Knowledge application recorded for Group {args.group}")

    elif args.action == "flows":
        analysis = system.get_knowledge_flow_analysis()
        print("Knowledge Flow Analysis:")
        print(f"  Overall Success Rate: {analysis['overall_transfer_success_rate']*100:.1f}%")
        print(f"  Total Transfers: {analysis['total_transfers']}")
        print("\nMost Effective Flows:")
        for flow in analysis["most_effective_flows"][:3]:
            print(f"  {flow['flow']}: {flow['success_rate']*100:.1f}% ({flow['total_transfers']} transfers)")

    elif args.action == "expertise":
        if not args.group:
            print("Error: --group required for expertise")
            sys.exit(1)

        expertise = system.get_group_expertise(args.group)
        print(f"Group {expertise['group']}: {expertise['group_name']}")
        print(f"  Total Knowledge Created: {expertise['total_knowledge_created']}")
        print("\nSpecializations:")
        for spec in expertise["specializations"]:
            print(f"  {spec['type']}: {spec['count']} items")

    else:
        # Show summary
        print("Inter-Group Knowledge Transfer System Initialized")
        print(f"Storage: {system.knowledge_file}")
        analysis = system.get_knowledge_flow_analysis()
        print(f"Total Transfers: {analysis['total_transfers']}")
        print(f"Success Rate: {analysis['overall_transfer_success_rate']*100:.1f}%")


if __name__ == "__main__":
    main()
