#!/usr/bin/env python3
Auto-fix script for autonomous-agent plugin critical issues
"""

import re
from pathlib import Path


def fix_validate_claude_plugin():
    """Fix the broken delegation in validate-claude-plugin.md"""
    file_path = Path("commands/validate-claude-plugin.md")

    if not file_path.exists():
        print(f"ERROR: {file_path" not found")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix the broken YAML frontmatter
    if content.startswith("---\n\n"):
        # Replace incomplete frontmatter with proper one
        new_frontmatter = """---
name: validate-claude-plugin
description: Validate Claude Code plugin against official guidelines
delegates-to: autonomous-agent:orchestrator
---

"""
        content = new_frontmatter + content[5:]  # Remove the broken ---\n\n

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"FIXED: {file_path" - Added proper YAML frontmatter")
    return True


def add_delegation_to_commands():
    """Add delegates-to fields to commands missing them"""
    commands_dir = Path("commands")

    # Commands that should delegate to orchestrator
    orchestrator_commands = [
        "auto-analyze.md",
        "dev-auto.md",
        "dashboard.md",
        "improve-plugin.md",
        "release-dev.md",
        "learn-patterns.md",
        "organize-workspace.md",
        "performance-report.md",
        "recommend.md",
        "validate-patterns.md",
        "validate-fullstack.md",
        "static-analysis.md",
        "scan-dependencies.md",
        "learning-analytics.md",
        "organize-reports.md",
        "predictive-analytics.md",
        "gui-debug.md",
        "eval-debug.md",
    ]

    # Commands that should delegate to specialized agents
    specialized_delegation = {
        "pr-review.md": "autonomous-agent:pr-reviewer",
        "git-release-workflow.md": "autonomous-agent:git-repository-manager",
    }

    fixed_count = 0

    for cmd_file in commands_dir.glob("*.md"):
        # Skip already fixed files
        if cmd_file.name in ["quality-check.md", "validate.md", "validate-claude-plugin.md"]:
            continue

        with open(cmd_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if already has delegates-to
        if "delegates-to:" in content.lower():
            continue

        # Determine delegation target
        if cmd_file.name in orchestrator_commands:
            delegates_to = "autonomous-agent:orchestrator"
        elif cmd_file.name in specialized_delegation:
            delegates_to = specialized_delegation[cmd_file.name]
        else:
            delegates_to = "autonomous-agent:orchestrator"  # Default

        # Add or create YAML frontmatter
        if content.startswith("---"):
            # Add to existing frontmatter
            frontmatter_end = content.find("---", 3)
            if frontmatter_end != -1:
                before = content[:frontmatter_end]
                after = content[frontmatter_end:]

                # Add delegates-to field
                if "\n---" in before:
                    before = before.replace("\n---", f"\ndelegates-to: {delegates_to"\n---")
                else:
                    before = f"{before"\ndelegates-to: {delegates_to}"

                content = before + after
        else:
            # Create new frontmatter
            cmd_name = cmd_file.stem
            new_frontmatter = f"""---
name: {cmd_name}
description: Command for {cmd_name.replace('-', ' ')}
delegates-to: {delegates_to}
---

"""
            content = new_frontmatter + content

        with open(cmd_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"FIXED: {cmd_file.name" - Added delegation to {delegates_to}")
        fixed_count += 1

    return fixed_count


def generate_delegation_report():
    """Generate a report of all command delegations"""
    commands_dir = Path("commands")
    report = []

    report.append("# Command Delegation Report\n")
    report.append("Generated after auto-fix application\n")

    for cmd_file in sorted(commands_dir.glob("*.md")):
        with open(cmd_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract delegation
        delegates_match = re.search(r"delegates-to:\s*(.+)", content, re.IGNORECASE)
        if delegates_match:
            delegates_to = delegates_match.group(1).strip()
            status = "[OK]"
        else:
            delegates_to = "MISSING"
            status = "[ERROR]"

        report.append(f"{status" `{cmd_file.name}` → `{delegates_to}`")

    report_text = "\n".join(report)

    with open("command_delegation_report.md", "w", encoding="utf-8") as f:
        f.write(report_text)

    print("Generated: command_delegation_report.md")


def main():
    """Main."""
    print("AUTONOMOUS AGENT PLUGIN AUTO-FIX")
    print("=" * 50)

    # Fix critical issues
    print("\n1. Fixing critical delegation issues...")
    fix_validate_claude_plugin()

    print("\n2. Adding delegation to missing commands...")
    fixed_count = add_delegation_to_commands()
    print(f"Fixed {fixed_count" command files")

    print("\n3. Generating delegation report...")
    generate_delegation_report()

    print("\n" + "=" * 50)
    print("AUTO-FIX COMPLETE")
    print("\nNext steps:")
    print("1. Run validation again: python validate_plugin.py")
    print("2. Test command execution manually")
    print("3. Commit and release as v3.6.2")


if __name__ == "__main__":
    main()

"""