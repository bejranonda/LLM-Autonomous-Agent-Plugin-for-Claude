#!/usr/bin/env python3
"""
Agent Error Helper

Provides intelligent agent name suggestions and helpful error messages
when users attempt to use incorrect agent names in the Task tool.

This addresses the naming confusion between plugin name "autonomous-agent"
and actual agent names which use simple names without prefixes.
"""

import json
from difflib import get_close_matches

# Complete agent database
AVAILABLE_AGENTS = {
    "orchestrator": {
        "description": "Main autonomous decision maker that delegates to specialized agents",
        "category": "core",
        "usage": "General tasks, project coordination, multi-agent workflows"
    },
    "code-analyzer": {
        "description": "Code structure and pattern analysis specialist",
        "category": "analysis",
        "usage": "Code review, architecture analysis, pattern detection"
    },
    "quality-controller": {
        "description": "Quality assurance and auto-fix specialist",
        "category": "quality",
        "usage": "Code quality issues, standards compliance, auto-fix"
    },
    "validation-controller": {
        "description": "Proactive validation and error prevention specialist",
        "category": "validation",
        "usage": "Error prevention, consistency checks, pre-flight validation"
    },
    "learning-engine": {
        "description": "Pattern learning and continuous improvement specialist",
        "category": "learning",
        "usage": "Pattern learning, performance optimization, continuous improvement"
    },
    "test-engineer": {
        "description": "Test generation and database management specialist",
        "category": "testing",
        "usage": "Test generation, database isolation, test coverage"
    },
    "security-auditor": {
        "description": "Security vulnerability scanning and prevention specialist",
        "category": "security",
        "usage": "Security scanning, vulnerability assessment, OWASP compliance"
    },
    "documentation-generator": {
        "description": "Documentation maintenance and generation specialist",
        "category": "documentation",
        "usage": "Documentation generation, API docs, technical guides"
    },
    "frontend-analyzer": {
        "description": "Frontend-specific validation and analysis specialist",
        "category": "frontend",
        "usage": "TypeScript validation, React issues, build validation"
    },
    "performance-analytics": {
        "description": "Performance analysis and insights specialist",
        "category": "analytics",
        "usage": "Performance analysis, metrics tracking, optimization"
    },
    "gui-validator": {
        "description": "Comprehensive GUI validation and debugging specialist",
        "category": "validation",
        "usage": "GUI testing, interface validation, user experience analysis"
    },
    "background-task-manager": {
        "description": "Parallel background task execution specialist",
        "category": "coordination",
        "usage": "Parallel processing, non-blocking tasks, result coordination"
    },
    "git-repository-manager": {
        "description": "Advanced Git workflow automation specialist",
        "category": "git",
        "usage": "Git operations, branching strategies, release automation"
    },
    "version-release-manager": {
        "description": "Release automation and management specialist",
        "category": "release",
        "usage": "Semantic versioning, release notes, version management"
    },
    "workspace-organizer": {
        "description": "Workspace and report management specialist",
        "category": "organization",
        "usage": "File organization, report consolidation, cleanup automation"
    },
    "report-management-organizer": {
        "description": "Report generation and organization specialist",
        "category": "organization",
        "usage": "Report creation, categorization, search optimization"
    },
    "smart-recommender": {
        "description": "Intelligent workflow recommendations specialist",
        "category": "analytics",
        "usage": "Task-agent optimization, pattern-based suggestions"
    },
    "pr-reviewer": {
        "description": "Pull request review automation specialist",
        "category": "review",
        "usage": "Automated code review, change summarization, security scanning"
    },
    "dev-orchestrator": {
        "description": "Development workflow automation specialist",
        "category": "development",
        "usage": "Milestone planning, incremental implementation, auto-debugging"
    },
    "claude-plugin-validator": {
        "description": "Plugin compliance validation specialist",
        "category": "validation",
        "usage": "Plugin guideline validation, structure verification"
    },
    "build-validator": {
        "description": "Build tool configuration validation specialist",
        "category": "build",
        "usage": "Build validation, environment variable tracking, module conflicts"
    },
    "api-contract-validator": {
        "description": "API synchronization and type generation specialist",
        "category": "api",
        "usage": "API schema extraction, frontend-backend synchronization"
    },
    "integrity-validation": {
        "description": "Pre/post-operation validation specialist",
        "category": "validation",
        "usage": "Tool usage validation, consistency checks, compliance"
    }
}

# Common mistakes and their corrections
COMMON_MISTAKES = {
    "autonomous-agent": "orchestrator",
    "debug-evaluator": "validation-controller",
    "code-analyzer": "code-analyzer",
    "quality": "quality-controller",
    "test": "test-engineer",
    "security": "security-auditor",
    "docs": "documentation-generator",
    "documentation": "documentation-generator",
    "performance": "performance-analytics",
    "frontend": "frontend-analyzer",
    "validation": "validation-controller",
    "learning": "learning-engine",
    "orchestration": "orchestrator",
    "analysis": "code-analyzer",
    "testing": "test-engineer",
    "gui": "gui-validator",
    "git": "git-repository-manager",
    "release": "version-release-manager",
    "workspace": "workspace-organizer",
    "report": "report-management-organizer"
}

def find_closest_agents(user_input, limit=5):
    """Find the closest matching agent names using fuzzy matching."""
    all_agents = list(AVAILABLE_AGENTS.keys())

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
        if part in all_agents and part not in close_matches:
            close_matches.insert(0, part)

    return close_matches

def generate_helpful_error(user_input):
    """Generate a helpful error message with suggestions."""

    # Find closest matches
    suggestions = find_closest_agents(user_input)

    # Build error message
    error_msg = f"[ERROR] Agent '{user_input}' not found.\n\n"

    if suggestions:
        error_msg += "[SUGGESTION] Did you mean one of these agents?\n"
        for i, agent in enumerate(suggestions[:3], 1):
            agent_info = AVAILABLE_AGENTS.get(agent, {})
            description = agent_info.get("description", "No description available")
            usage = agent_info.get("usage", "General purpose")
            error_msg += f"   {i}. **{agent}** - {description}\n"
            error_msg += f"      Best for: {usage}\n"

        if len(suggestions) > 3:
            error_msg += f"   ... and {len(suggestions) - 3} more\n"
    else:
        error_msg += "[SUGGESTION] No similar agents found. Here are the most used agents:\n"
        top_agents = ["orchestrator", "code-analyzer", "quality-controller", "validation-controller", "test-engineer"]
        for i, agent in enumerate(top_agents, 1):
            agent_info = AVAILABLE_AGENTS.get(agent, {})
            description = agent_info.get("description", "No description available")
            error_msg += f"   {i}. **{agent}** - {description}\n"

    error_msg += f"\n[INFO] **Naming Convention**:\n"
    error_msg += f"   • Use simple agent names WITHOUT 'autonomous-agent:' prefix\n"
    error_msg += f"   • Examples: Task('description', 'orchestrator') or Task('description', 'code-analyzer')\n"
    error_msg += f"   • For most tasks, use 'orchestrator' - it will select the right specialized agents\n"

    error_msg += f"\n[RECOMMENDATION] **Quick Start Guide**:\n"
    error_msg += f"   • General tasks & coordination -> **orchestrator**\n"
    error_msg += f"   • Code quality & fixes -> **quality-controller**\n"
    error_msg += f"   • Code analysis & architecture -> **code-analyzer**\n"
    error_msg += f"   • Testing & coverage -> **test-engineer**\n"
    error_msg += f"   • Documentation -> **documentation-generator**\n"
    error_msg += f"   • Security scanning -> **security-auditor**\n"
    error_msg += f"   • Validation & error prevention -> **validation-controller**\n"

    error_msg += f"\n[HELP] **Need more help?**\n"
    error_msg += f"   • See AGENT_USAGE_GUIDE.md for complete documentation\n"
    error_msg += f"   • Use Task('your description', 'orchestrator') for automatic agent selection\n"

    return error_msg

def suggest_agents_for_task(task_description):
    """Suggest the best agents for a given task description."""
    task_lower = task_description.lower()

    # Keyword-based agent suggestion
    agent_scores = {}

    for agent, info in AVAILABLE_AGENTS.items():
        score = 0

        # Check category and usage patterns
        category = info.get("category", "").lower()
        usage = info.get("usage", "").lower()
        description = info.get("description", "").lower()

        # Category matching
        if category in task_lower:
            score += 3

        # Usage matching
        usage_words = usage.split()
        for word in usage_words:
            if word in task_lower and len(word) > 3:
                score += 2

        # Description matching
        desc_words = description.split()
        for word in desc_words:
            if word in task_lower and len(word) > 4:
                score += 1

        # Bonus for core agents
        if category in ["core", "quality", "validation"]:
            score += 1

        if score > 0:
            agent_scores[agent] = score

    # Sort by score and return top suggestions
    sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)

    if not sorted_agents:
        # Default to orchestrator for unknown tasks
        return [("orchestrator", "General purpose autonomous decision maker")]

    return sorted_agents[:3]

def list_all_agents():
    """List all available agents with their information."""
    result = f"[INFO] Available Agents ({len(AVAILABLE_AGENTS)} total):\n\n"

    # Group by category
    by_category = {}
    for name, info in AVAILABLE_AGENTS.items():
        category = info.get("category", "general")
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((name, info))

    # Sort categories and display
    for category in sorted(by_category.keys()):
        agents = by_category[category]
        result += f"**{category.title()} Category** ({len(agents)} agents):\n"

        for name, info in sorted(agents):
            description = info.get("description", "No description")
            usage = info.get("usage", "General purpose")
            result += f"   • **{name}** - {description}\n"
            result += f"     Best for: {usage}\n\n"

    result += f"[RECOMMENDATION] **Recommendation**: For most tasks, use 'orchestrator' - it automatically selects the best specialized agents.\n"

    return result

def main():
    """Main CLI interface."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python agent_error_helper.py <agent-name-or-task>")
        print("       python agent_error_helper.py --list")
        print("       python agent_error_helper.py --suggest <task-description>")
        return

    command = sys.argv[1]

    if command == "--list":
        print(list_all_agents())
    elif command == "--suggest" and len(sys.argv) > 2:
        task_desc = " ".join(sys.argv[2:])
        suggestions = suggest_agents_for_task(task_desc)
        result = f"[RECOMMENDATION] Agent suggestions for: '{task_desc}'\n\n"
        for agent, reason in suggestions:
            info = AVAILABLE_AGENTS.get(agent, {})
            description = info.get("description", "No description")
            usage = info.get("usage", "General purpose")
            result += f"**{agent}** - {description}\n"
            result += f"   Best for: {usage}\n\n"
        print(result)
    else:
        # Check if it's an agent name or task description
        if command in AVAILABLE_AGENTS:
            info = AVAILABLE_AGENTS[command]
            print(f"[SUCCESS] Agent '{command}' found!")
            print(f"   Description: {info.get('description', 'N/A')}")
            print(f"   Category: {info.get('category', 'N/A')}")
            print(f"   Best for: {info.get('usage', 'N/A')}")
        else:
            print(generate_helpful_error(command))

if __name__ == "__main__":
    main()