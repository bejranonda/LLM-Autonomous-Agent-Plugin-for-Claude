#!/usr/bin/env python3
"""
Comprehensive Assessment Storage System
Stores assessment results from ALL commands in the pattern database
for dashboard real-time monitoring and learning system improvement.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List


class AssessmentStorage:
    """Manages storage of assessment results from all commands"""

    def __init__(self, pattern_dir: str = ".claude-patterns"):
        self.pattern_dir = Path(pattern_dir)
        self.pattern_dir.mkdir(exist_ok=True)

        # Pattern files
        self.patterns_file = self.pattern_dir / "patterns.json"
        self.quality_history_file = self.pattern_dir / "quality_history.json"
        self.agent_metrics_file = self.pattern_dir / "agent_metrics.json"
        self.skill_metrics_file = self.pattern_dir / "skill_metrics.json"
        self.assessments_file = self.pattern_dir / "assessments.json"  # New comprehensive storage

        self._ensure_files()

    def _ensure_files(self):
        """Ensure all pattern files exist with proper structure"""
        for file_path, default_structure in [
            (self.patterns_file, {"project_context": {}, "patterns": []}),
            (
                self.quality_history_file,
                {
                    "quality_assessments": [],
                    "statistics": {},
                    "baselines": {},
                    "metadata": {},
                },
            ),
            (
                self.agent_metrics_file,
                {
                    "quality_assessment_tasks": [],
                    "agent_performance": {},
                    "last_updated": "",
                    "total_quality_assessments": 0,
                    "overall_success_rate": 1.0,
                },
            ),
            (
                self.skill_metrics_file,
                {
                    "skill_usage_history": [],
                    "skill_effectiveness": {},
                    "last_updated": "",
                    "total_skill_usage_events": 0,
                    "overall_success_rate": 1.0,
                },
            ),
            (
                self.assessments_file,
                {
                    "assessments": [],
                    "command_performance": {},
                    "last_updated": "",
                    "total_assessments": 0,
                },
            ),
        ]:
            if not file_path.exists():
                with open(file_path, 'w') as f: json.dump(default_structure, f, indent=2)

    def store_assessment(self, assessment_data: Dict[str, Any]) -> bool:
        """
        Store assessment result from any command

        Args:
            assessment_data: Dict containing: - command_name: str (e.g., 'validate-claude-plugin', 'gui-debug')
                - assessment_type: str (
    e.g.,
    'validation',
    'quality-control',
    'gui-analysis',
)
                - overall_score: int (0-100)
                - "breakdown": Dict[str, int] (score breakdown)
                - "details": Dict[str, Any] (detailed findings)
                - "issues_found": List[str]
                - "recommendations": List[str]
                - "agents_used": List[str] (optional)
                - "skills_used": List[str] (optional)
                - execution_time: float (optional, in minutes)
                - pass_threshold_met: bool (optional)
                - "additional_metrics": Dict[str, Any] (optional)

        Returns:
            bool: Success status
        """
        try:
            # Generate assessment ID
            timestamp = datetime.now(timezone.utc)
            assessment_id = f"{assessment_data['command_name']}-{timestamp.strftime('%Y%m%d-%H%M%S')}"

            # Create comprehensive assessment record
            assessment_record = {
                "assessment_id": assessment_id,
                "timestamp": timestamp.isoformat(),
                "command_name": assessment_data["command_name"],
                "assessment_type": assessment_data.get("assessment_type", "general"),
                "task_type": assessment_data.get(
                    "task_type",
                    assessment_data["command_name"]
                ),
                "overall_score": assessment_data["overall_score"],
                "breakdown": assessment_data.get("breakdown", {}),
                "details": assessment_data.get("details", {}),
                "issues_found": assessment_data.get("issues_found", []),
                "recommendations": assessment_data.get("recommendations", []),
                "agents_used": assessment_data.get("agents_used", []),
                "skills_used": assessment_data.get("skills_used", []),
                "execution_time_minutes": assessment_data.get("execution_time"),
                "pass_threshold_met": assessment_data.get(
                    "pass_threshold_met",
                    assessment_data["overall_score"] >= 70
                ),
                "additional_metrics": assessment_data.get("additional_metrics", {}),
                "success": assessment_data["overall_score"] >= 70
            }

            # Store in comprehensive assessments file
            self._store_in_assessments_file(assessment_record)

            # Store in quality history (for backward compatibility)
            self._store_in_quality_history(assessment_record)

            # Update agent metrics if agents were used
            if assessment_data.get("agents_used"):
                self._update_agent_metrics(assessment_record)

            # Update skill metrics if skills were used
            if assessment_data.get("skills_used"):
                self._update_skill_metrics(assessment_record)

            # Store in patterns file (for learning system)
            self._store_in_patterns_file(assessment_record)

            print(f"[+] Assessment stored: {assessment_id} (Score: {assessment_data['overall_score']}/100)")
            return True

        except Exception as e:
            print(f"Failed to store assessment: {e}")
            return False

    def _store_in_assessments_file(self, assessment_record: Dict[str, Any]):
        """Store in comprehensive assessments file"""
        with open(self.assessments_file, 'r') as f:
            data = json.load(f)

        data["assessments"].append(assessment_record)
        data["last_updated"] = assessment_record["timestamp"]
        data["total_assessments"] = len(data["assessments"])

        # Update command performance metrics
        command_name = assessment_record["command_name"]
        if command_name not in data["command_performance"]:
            data["command_performance"][command_name] = {
                "total_executions": 0,
                "successful_executions": 0,
                "avg_score": 0,
                "avg_execution_time": 0,
                "last_execution": None
            }

        cmd_metrics = data["command_performance"][command_name]
        cmd_metrics["total_executions"] += 1
        if assessment_record["success"]:
            cmd_metrics["successful_executions"] += 1

        # Update averages
        total_exec = cmd_metrics["total_executions"]
        current_avg = cmd_metrics["avg_score"]
        new_score = assessment_record["overall_score"]
        cmd_metrics["avg_score"] = ((current_avg * (total_exec - 1)) + new_score) / total_exec

        if assessment_record.get("execution_time_minutes"):
            current_time_avg = cmd_metrics["avg_execution_time"] or 0
            new_time = assessment_record["execution_time_minutes"]
            cmd_metrics["avg_execution_time"] = ((current_time_avg * (total_exec - 1)) + new_time) / total_exec

        cmd_metrics["last_execution"] = assessment_record["timestamp"]

        with open(self.assessments_file, 'w') as f: json.dump(data, f, indent=2)
    def _store_in_quality_history(self, assessment_record: Dict[str, Any]):
        """Store in quality history file (for dashboard compatibility)"""
        with open(self.quality_history_file, 'r') as f:
            data = json.load(f)

        # Convert to quality assessment format
        quality_assessment = {
            "assessment_id": assessment_record["assessment_id"],
            "timestamp": assessment_record["timestamp"],
            "task_type": assessment_record["task_type"],
            "overall_score": assessment_record["overall_score"],
            "breakdown": assessment_record["breakdown"],
            "details": assessment_record["details"],
            "issues_found": assessment_record["issues_found"],
            "recommendations": assessment_record["recommendations"],
            "pass": assessment_record["success"],
            "command_name": assessment_record["command_name"],
            "assessment_type": assessment_record["assessment_type"]
        }

        data["quality_assessments"].append(quality_assessment)

        # Update statistics
        total_assessments = len(data["quality_assessments"])
        scores = [a["overall_score"] for a in data["quality_assessments"]]
        data["statistics"] = {
            "avg_quality_score": sum(scores) / len(scores) if scores else 0,
            "total_assessments": total_assessments,
            "passing_rate": sum(1 for s in scores if s >= 70) / len(scores) if scores else 1.0,
            "trend": "improving"  # Could be calculated more sophisticatedly
        }

        data["metadata"]["last_assessment"] = assessment_record["timestamp"]

        with open(self.quality_history_file, 'w') as f: json.dump(data, f, indent=2)
    def _update_agent_metrics(self, assessment_record: Dict[str, Any]):
        """Update agent performance metrics"""
        with open(self.agent_metrics_file, 'r') as f:
            data = json.load(f)

        task_record = {
            "task_id": assessment_record["assessment_id"],
            "timestamp": assessment_record["timestamp"],
            "task_type": assessment_record["task_type"],
            "agents_involved": assessment_record["agents_used"],
            "execution_details": {},
            "collaboration_effectiveness": "excellent" if
                assessment_record["success"] else "needs_improvement",
            "integration_success": assessment_record["success"]
        }

        # Add execution details for each agent
        for agent in assessment_record["agents_used"]:
            task_record["execution_details"][agent] = {
                "role": "assessment_execution",
                "duration_seconds": int(
                    (assessment_record.get("execution_time_minutes", 0) or 0) * 60
                ),
                "success": assessment_record["success"],
                "quality_score": assessment_record["overall_score"]
            }

        data["quality_assessment_tasks"].append(task_record)

        # Update agent performance
        for agent in assessment_record["agents_used"]:
            if agent not in data["agent_performance"]:
                data["agent_performance"][agent] = {
                    "total_tasks": 0,
                    "successful_tasks": 0,
                    "avg_quality_score": 0,
                    "total_duration": 0
                }

            perf = data["agent_performance"][agent]
            perf["total_tasks"] += 1
            if assessment_record["success"]:
                perf["successful_tasks"] += 1

            # Update average quality score
            total_tasks = perf["total_tasks"]
            current_avg = perf["avg_quality_score"]
            new_score = assessment_record["overall_score"]
            perf["avg_quality_score"] = ((current_avg * (total_tasks - 1)) + new_score) / total_tasks

            # Update total duration
            duration = int((assessment_record.get("execution_time_minutes", 0) or 0) * 60)
            perf["total_duration"] += duration

        data["last_updated"] = assessment_record["timestamp"]
        data["total_quality_assessments"] = len(data["quality_assessment_tasks"])
        data["overall_success_rate"] = sum(1 for t in data["quality_assessment_tasks"] if 
            t["integration_success"]) / len(data["quality_assessment_tasks"])

        with open(self.agent_metrics_file, 'w') as f: json.dump(data, f, indent=2)
    def _update_skill_metrics(self, assessment_record: Dict[str, Any]):
        """Update skill effectiveness metrics"""
        with open(self.skill_metrics_file, 'r') as f:
            data = json.load(f)

        task_record = {
            "task_id": assessment_record["assessment_id"],
            "timestamp": assessment_record["timestamp"],
            "task_type": assessment_record["task_type"],
            "skills_used": assessment_record["skills_used"],
            "overall_success": assessment_record["success"],
            "quality_score": assessment_record["overall_score"]
        }

        data["skill_usage_history"].append(task_record)

        # Update skill effectiveness
        for skill in assessment_record["skills_used"]:
            if skill not in data["skill_effectiveness"]:
                data["skill_effectiveness"][skill] = {
                    "total_uses": 0,
                    "successful_uses": 0,
                    "success_rate": 1.0,
                    "avg_contribution_score": 0.9
                }

            eff = data["skill_effectiveness"][skill]
            eff["total_uses"] += 1
            if assessment_record["success"]:
                eff["successful_uses"] += 1
            eff["success_rate"] = eff["successful_uses"] / eff["total_uses"]

            # Update average contribution score based on quality
            total_uses = eff["total_uses"]
            current_avg = eff["avg_contribution_score"]
            # Normalize quality score to 0-1 range for contribution score
            new_contribution = assessment_record["overall_score"] / 100
            eff["avg_contribution_score"] = ((current_avg * (total_uses - 1)) + new_contribution) / total_uses

        data["last_updated"] = assessment_record["timestamp"]
        data["total_skill_usage_events"] = len(data["skill_usage_history"])
        data["overall_success_rate"] = sum(1 for t in data["skill_usage_history"] if 
            t["overall_success"]) / len(data["skill_usage_history"])

        with open(self.skill_metrics_file, 'w') as f: json.dump(data, f, indent=2)
    def _store_in_patterns_file(self, assessment_record: Dict[str, Any]):
        """Store assessment pattern for learning system"""
        with open(self.patterns_file, 'r') as f:
            data = json.load(f)

        pattern = {
            "pattern_id": assessment_record["assessment_id"],
            "timestamp": assessment_record["timestamp"],
            "task_type": assessment_record["task_type"],
            "task_description": f"{assessment_record['command_name']} command execution",
            "context": {
                "command_name": assessment_record["command_name"],
                "assessment_type": assessment_record["assessment_type"],
                "score": assessment_record["overall_score"],
                "success": assessment_record["success"]
            },
            "execution": {
                "skills_used": assessment_record.get("skills_used", []),
                "agents_delegated": assessment_record.get("agents_used", []),
                "approach": assessment_record["command_name"],
                "duration_seconds": int((assessment_record.get("execution_time_minutes", 0) or 0) * 60),
                "score_achieved": assessment_record["overall_score"]
            },
            "findings": {
                "issues_count": len(assessment_record.get("issues_found", [])),
                "recommendations_count": len(assessment_record.get("recommendations", [])),
                "key_issues": assessment_record.get("issues_found", [])[:3]  # Top 3 issues
            },
            "success_factors": self._extract_success_factors(assessment_record),
            "outcome": {
                "success": assessment_record["success"],
                "quality_score": assessment_record["overall_score"],
                "threshold_met": assessment_record.get(
    "pass_threshold_met",
    assessment_record["overall_score"] >= 70,
)
            },
            "reuse_count": 0,
            "confidence_boost": 0.1 if assessment_record["success"] else 0.0
        }

        data["patterns"].append(pattern)

        with open(self.patterns_file, 'w') as f: json.dump(data, f, indent=2)
    def _extract_success_factors(self, assessment_record: Dict[str, Any]) -> List[str]:
        """Extract success factors from assessment"""
        factors = []
        if assessment_record["overall_score"] >= 90:
            factors.append("high_quality_execution")
        if assessment_record.get("execution_time_minutes", 0) < 5:
            factors.append("efficient_execution")
        if len(assessment_record.get("issues_found", [])) == 0:
            factors.append("no_issues_detected")
        if assessment_record.get("agents_used"):
            factors.append("effective_agent_coordination")
        if assessment_record.get("skills_used"):
            factors.append("optimal_skill_application")
        return factors

    def get_command_summary(self) -> Dict[str, Any]:
        """Get summary of all command assessments"""
        with open(self.assessments_file, 'r') as f:
            data = json.load(f)

        return {
            "total_assessments": data["total_assessments"],
            "command_performance": data["command_performance"],
            "last_updated": data["last_updated"],
            "recent_assessments": data["assessments"][-10:]  # Last 10 assessments
        }

def main():
    """CLI interface for assessment storage"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Store assessment results from any command")
    parser.add_argument(
    "--command",
    required=True,
    help="Command name (e.g., validate-claude-plugin)",
)
    parser.add_argument(
    "--score",
    type=int,
    required=True,
    help="Overall score (0-100)",
)
    parser.add_argument("--type", default="general", help="Assessment type")
    parser.add_argument("--time", type=float, help="Execution time in minutes")
    parser.add_argument("--agents", nargs="*", default=[], help="Agents used")
    parser.add_argument("--skills", nargs="*", default=[], help="Skills used")
    parser.add_argument("--dir", default=".claude-patterns", help="Pattern directory")

    args = parser.parse_args()

    storage = AssessmentStorage(args.dir)

    assessment_data = {
        "command_name": args.command,
        "assessment_type": args.type,
        "overall_score": args.score,
        "execution_time": args.time,
        "agents_used": args.agents,
        "skills_used": args.skills,
        "details": {"cli_stored": True},
        "issues_found": [],
        "recommendations": []
    }

    success = storage.store_assessment(assessment_data)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
