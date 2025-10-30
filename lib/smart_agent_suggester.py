#!/usr/bin/env python3
"""
Smart Agent Suggester
Suggests optimal agents for specific tasks based on historical performance.
"""

import json
from typing import Dict, List, Optional
from pathlib import Path


class SmartAgentSuggester:
    """Suggests optimal agents for specific tasks"""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        self.patterns_dir = Path(patterns_dir)
        self.patterns_dir.mkdir(parents=True, exist_ok=True)

    def suggest_agent(self, task_type: str, task_description: str) -> Optional[str]:
        """Suggest the best agent for a given task"""
        # Simple agent suggestion logic
        agent_mapping = {
            "code_analysis": "code-analyzer",
            "quality_check": "quality-controller",
            "documentation": "documentation-generator",
            "testing": "test-engineer",
            "learning": "learning-engine"
        }

        for key, agent in agent_mapping.items():
            if key in task_type.lower() or key in task_description.lower():
                return agent

        return "orchestrator"  # Default fallback

    def record_agent_performance(self, agent: str, task_type: str, success: bool) -> None:
        """Record agent performance for learning"""
        performance_file = self.patterns_dir / "agent_performance.json"
        performance = {}
        if performance_file.exists():
            with open(performance_file, 'r') as f:
                performance = json.load(f)

        if agent not in performance:
            performance[agent] = {"tasks": 0, "successes": 0}

        performance[agent]["tasks"] += 1
        if success:
            performance[agent]["successes"] += 1

        with open(performance_file, 'w') as f:
            json.dump(performance, f, indent=2)

    def get_agent_stats(self) -> Dict[str, Dict]:
        """Get performance statistics for all agents"""
        performance_file = self.patterns_dir / "agent_performance.json"
        if performance_file.exists():
            with open(performance_file, 'r') as f:
                return json.load(f)
        return {}


def main():
    """Main execution function"""
    suggester = SmartAgentSuggester()

    task_type = "code_analysis"
    task_desc = "Analyze the codebase for quality issues"

    suggested = suggester.suggest_agent(task_type, task_desc)
    print(f"Suggested agent for {task_type}: {suggested}")


if __name__ == "__main__":
    main()
