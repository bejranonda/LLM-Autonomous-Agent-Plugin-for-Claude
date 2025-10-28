#!/usr/bin/env python3
"""
Smart Agent Suggestion System

Provides intelligent agent name suggestions and helpful error messages
when users attempt to use incorrect agent names in the Task tool.

This addresses the naming confusion between plugin name "autonomous-agent"
and actual agent names which use simple names without prefixes.
"""

import json
import os
import sys
from pathlib import Path
from difflib import get_close_matches
import argparse

# Agent database with descriptions and usage patterns
AGENTS_DATABASE = {
    "orchestrator": {
        "description": "Main autonomous decision maker that delegates to specialized agents",
        "category": "core",
        "usage_frequency": "high",
        "common_for": ["general-tasks", "project-analysis", "coordination", "multi-agent-workflows"],
        "examples": [
            "Analyze project structure",
            "Fix code quality issues",
            "Generate documentation",
            "Coordinate complex development tasks"
        ]
    },
    "code-analyzer": {
        "description": "Code structure and pattern analysis specialist",
        "category": "analysis",
        "usage_frequency": "high",
        "common_for": ["code-review", "architecture-analysis", "pattern-detection", "refactoring-decisions"],
        "examples": [
            "Analyze code architecture",
            "Review code structure",
            "Detect code patterns",
            "Assess refactoring opportunities"
        ]
    },
    "quality-controller": {
        "description": "Quality assurance and auto-fix specialist",
        "category": "quality",
        "usage_frequency": "high",
        "common_for": ["code-quality", "standards-compliance", "auto-fix", "quality-gates"],
        "examples": [
            "Fix code quality issues",
            "Enforce coding standards",
            "Auto-fix syntax errors",
            "Run quality checks"
        ]
    },
    "validation-controller": {
        "description": "Proactive validation and error prevention specialist",
        "category": "validation",
        "usage_frequency": "medium",
        "common_for": ["error-prevention", "consistency-checks", "pre-flight-validation", "documentation-validation"],
        "examples": [
            "Validate tool usage", " validation-controller,
            "Prevent errors before execution", " validation-controller,
            "Check documentation consistency", " validation-controller,
            "Run pre-flight checks", " validation-controller
        ]
    },
    "learning-engine": {
        "description": "Pattern learning and continuous improvement specialist",
        "category": "learning",
        "usage_frequency": "automatic",
        "common_for": ["pattern-learning", "performance-optimization", "continuous-improvement"],
        "examples": [
            "Learn from task patterns", " learning-engine,
            "Optimize performance based on history", " learning-engine,
            "Store successful approaches", " learning-engine
        ]
    },
    "test-engineer": {
        "description": "Test generation and database management specialist",
        "category": "testing",
        "usage_frequency": "medium",
        "common_for": ["test-generation", "database-isolation", "test-coverage", "sqlalchemy-fixes"],
        "examples": [
            "Generate comprehensive tests", " test-engineer,
            "Fix database test isolation", " test-engineer,
            "Improve test coverage", " test-engineer,
            "Handle SQLAlchemy compatibility", " test-engineer
        ]
    },
    "security-auditor": {
        "description": "Security vulnerability scanning and prevention specialist",
        "category": "security",
        "usage_frequency": "medium",
        "common_for": ["security-scan", "vulnerability-assessment", "owasp-compliance", "security-patterns"],
        "examples": [
            "Scan for security vulnerabilities", " security-auditor,
            "Check OWASP Top 10 compliance", " security-auditor,
            "Audit code for security issues", " security-auditor,
            "Implement security patterns", " security-auditor
        ]
    },
    "documentation-generator": {
        "description": "Documentation maintenance and generation specialist",
        "category": "documentation",
        "usage_frequency": "medium",
        "common_for": ["doc-generation", "api-documentation", "readme-maintenance", "technical-guides"],
        "examples": [
            "Generate API documentation", " documentation-generator,
            "Update README files", " documentation-generator,
            "Create technical guides", " documentation-generator,
            "Maintain documentation", " documentation-generator
        ]
    },
    "frontend-analyzer": {
        "description": "Frontend-specific validation and analysis specialist",
        "category": "frontend",
        "usage_frequency": "medium",
        "common_for": ["typescript-validation", "react-issues", "build-validation", "frontend-optimization"],
        "examples": [
            "Fix TypeScript errors", " frontend-analyzer,
            "Validate React components", " frontend-analyzer,
            "Optimize frontend build", " frontend-analyzer,
            "Analyze frontend performance", " frontend-analyzer
        ]
    },
    "performance-analytics": {
        "description": "Performance analysis and insights specialist",
        "category": "analytics",
        "usage_frequency": "medium",
        "common_for": ["performance-analysis", "metrics-tracking", "optimization-recommendations", "trend-analysis"],
        "examples": [
            "Analyze application performance", " performance-analytics,
            "Track performance metrics", " performance-analytics,
            "Generate optimization recommendations", " performance-analytics,
            "Monitor performance trends", " performance-analytics
        ]
    },
    "gui-validator": {
        "description": "Comprehensive GUI validation and debugging specialist",
        "category": "validation",
        "usage_frequency": "low",
        "common_for": ["gui-testing", "interface-validation", "user-experience-analysis", "dashboard-debugging"],
        "examples": [
            "Validate GUI functionality", " gui-validator,
            "Debug user interface issues", " gui-validator,
            "Test dashboard components", " gui-validator,
            "Analyze user experience", " gui-validator
        ]
    }
}

# Common mistakes and their corrections
COMMON_MISTAKES = {
    "autonomous-agent": "orchestrator",
    "debug-evaluator": "validation-controller",
    "code-analyzer": "code-analyzer",  # This one is correct
    "quality": "quality-controller",
    "test": "test-engineer",
    "security": "security-auditor",
    "docs": "documentation-generator",
    "performance": "performance-analytics",
    "frontend": "frontend-analyzer",
    "validation": "validation-controller",
    "learning": "learning-engine",
    "orchestration": "orchestrator",
    "analysis": "code-analyzer",
    "testing": "test-engineer",
    "documentation": "documentation-generator"
}

def find_closest_agents(user_input, limit=5):
    """Find the closest matching agent names using fuzzy matching."""
    all_agents = list(AGENTS_DATABASE.keys())

    # Check for exact matches first
    if user_input in all_agents:
        return [user_input]

    # Check common mistakes
    if user_input.lower() in COMMON_MISTAKES:
        suggested = COMMON_MISTAKES[user_input.lower()]
        if suggested in all_agents:
            return [suggested]

    # Use fuzzy matching for close matches
    close_matches = get_close_matches(user_input, all_agents, n=limit, cutoff=0.6)

    # Also try matching parts of the input
    user_parts = user_input.split('-')
    for part in user_parts:
        if part in all_agents:
            if part not in close_matches:
                close_matches.insert(0, part)

    return close_matches

def generate_helpful_error(user_input, available_agents=None):
    """Generate a helpful error message with suggestions."""
    if available_agents is None:
        available_agents = list(AGENTS_DATABASE.keys())

    # Find closest matches
    suggestions = find_closest_agents(user_input)

    # Build error message
    error_msg = f"❌ Agent '{user_input}' not found.\n\n"

    if suggestions:
        error_msg += "💡 Did you mean one of these agents?\n"
        for i, agent in enumerate(suggestions[:3], 1):
            agent_info = AGENTS_DATABASE.get(agent, {})
            description = agent_info.get("description", "No description available")
            error_msg += f"   {i}. **{agent}** - {description}\n"

        if len(suggestions) > 3:
            error_msg += f"   ... and {len(suggestions) - 3} more\n"
    else:
        error_msg += "💡 No similar agents found. Here are the most used agents:\n"
        top_agents = ["orchestrator", "code-analyzer", "quality-controller", "validation-controller", "test-engineer"]
        for i, agent in enumerate(top_agents, 1):
            agent_info = AGENTS_DATABASE.get(agent, {})
            description = agent_info.get("description", "No description available")
            error_msg += f"   {i}. **{agent}** - {description}\n"

    error_msg += f"\n📋 **Naming Convention**:\n"
    error_msg += f"   • Use simple agent names without 'autonomous-agent:' prefix\n"
    error_msg += f"   • Examples: Task('description', 'orchestrator') or Task('description', 'code-analyzer')\n"
    error_msg += f"   • For most tasks, use 'orchestrator' - it will select the right specialized agents\n"

    error_msg += f"\n🎯 **Quick Start**:\n"
    error_msg += f"   • General tasks, " Task('description', 'orchestrator')\n"
    error_msg += f"   • Code quality, " Task('description', 'quality-controller')\n"
    error_msg += f"   • Code analysis, " Task('description', 'code-analyzer')\n"
    error_msg += f"   • Testing, " Task('description', 'test-engineer')\n"
    error_msg += f"   • Documentation, " Task('description', 'documentation-generator')\n"

    return error_msg

def suggest_agents_for_task(task_description):
    """Suggest the best agents for a given task description."""
    task_lower = task_description.lower()

    # Keyword-based agent suggestion
    agent_scores = {}

    for agent, info in AGENTS_DATABASE.items():
        score = 0
        common_for = info.get("common_for", [])

        # Check against common_for patterns
        for pattern in common_for:
            if pattern.replace("-", " ") in task_lower:
                score += 3
            elif pattern.replace("-", "") in task_lower.replace(" ", ""):
                score += 2

        # Check against description
        description = info.get("description", "").lower()
        desc_words = description.split()
        for word in desc_words:
            if word in task_lower and len(word) > 3:
                score += 1

        # Bonus for high-frequency agents
        if info.get("usage_frequency") == "high":
            score += 1

        if score > 0:
            agent_scores[agent] = score

    # Sort by score and return top suggestions
    sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)

    if not sorted_agents:
        # Default to orchestrator for unknown tasks
        return [("orchestrator", "General purpose autonomous decision maker")]

    return sorted_agents[:3]

def list_all_agents(category=None):
    """List all available agents, optionally filtered by category."""
    agents = AGENTS_DATABASE.items()

    if category:
        agents = [(name, info) for name, info in agents if info.get("category") == category]

    result = f"📋 Available Agents ({len(agents)} total):\n\n"

    for name, info in sorted(agents):
        description = info.get("description", "No description")
        usage_freq = info.get("usage_frequency", "unknown")
        category_name = info.get("category", "general")

        result += f"**{name}** ({category_name}, {usage_freq} usage)\n"
        result += f"   {description}\n"

        examples = info.get("examples", [])
        if examples:
            result += f"   Examples: {examples[0] if examples else 'N/A'}\n"
        result += "\n"

    return result

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Smart Agent Suggestion System")
    parser.add_argument("input", nargs="?", help="Agent name to check or task description")
    parser.add_argument("--list", "-l", action="store_true", help="List all available agents")
    parser.add_argument("--category", "-c", help="Filter agents by category")
    parser.add_argument("--suggest", "-s", action="store_true", help="Suggest agents for task")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    if args.list:
        result = list_all_agents(args.category)
    elif args.suggest and args.input:
        suggestions = suggest_agents_for_task(args.input)
        if args.json:
            print(json.dumps(suggestions, indent=2))
        else:
            result = f"🎯 Agent suggestions for: '{args.input}'\n\n"
            for agent, reason in suggestions:
                agent_info = AGENTS_DATABASE.get(agent, {})
                description = agent_info.get("description", "No description")
                result += f"**{agent}** - {description}\n"
                result += f"   Reason: {reason}\n\n"
    elif args.input:
        result = generate_helpful_error(args.input)
    else:
        # Interactive mode
        print("🤖 Smart Agent Suggestion System")
        print("=" * 40)
        print("Enter an agent name to check, or a task description to get suggestions.")
        print("Type 'quit' to exit, 'help' for commands.\n")

        while True:
            try:
                user_input = input("❓ ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() in ['help', 'h']:
                    print("Commands:")
                    print("  <agent-name>    - Check if agent exists and get suggestions")
                    print("  <task-desc>     - Get agent suggestions for task")
                    print("  list            - List all agents")
                    print("  help            - Show this help")
                    print("  quit            - Exit")
                    continue
                elif user_input.lower() == 'list':
                    print(list_all_agents())
                elif user_input:
                    # Check if it's an agent name or task description
                    if user_input in AGENTS_DATABASE:
                        info = AGENTS_DATABASE[user_input]
                        print(f"✅ Agent '{user_input}' found!")
                        print(f"   Description: {info.get('description', 'N/A')}")
                        print(f"   Category: {info.get('category', 'N/A')}")
                        print(f"   Usage: {info.get('usage_frequency', 'N/A')}")
                    else:
                        suggestions = find_closest_agents(user_input, limit=3)
                        if suggestions and any(user_input.lower() in s.lower() for s in suggestions):
                            # Likely looking for agent suggestions
                            task_suggestions = suggest_agents_for_task(user_input)
                            print(f"🎯 Agent suggestions for task: '{user_input}'")
                            for agent, _ in task_suggestions:
                                info = AGENTS_DATABASE.get(agent, {})
                                print(f"   • {agent} - {info.get('description', 'N/A')}")
                        else:
                            # Likely checking for a specific agent
                            print(generate_helpful_error(user_input))
                print()

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    if not args.suggest or not args.json:
        print(result)

if __name__ == "__main__":
    main()