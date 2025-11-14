#!/usr/bin/env python3,"""
# Simple Claude Plugin validation
import json
import yaml
import re
from pathlib import Path


def validate_claude_plugin(plugin_dir="D:/Git/Werapol/AutonomousAgent"):
    """Comprehensive plugin validation against Claude Code guidelines."""

    issues = []
    warnings = []
    stats = {"agents": 0, "skills": 0, "commands": 0, "lib_files": 0, "total_files": 0}

    plugin_path = Path(plugin_dir)

    # 1. Plugin Manifest Validation
    manifest_path = plugin_path / ".claude-plugin" / "plugin.json"

    if not manifest_path.exists():
        issues.append("Missing plugin manifest: .claude-plugin/plugin.json")
        return issues, warnings, stats

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # Required fields
        required_fields = ["name", "version", "description", "author"]
        missing_fields = [field for field in required_fields if field not in manifest]
        if missing_fields:
            issues.append(f"Missing required fields: {missing_fields"")

        # Version format
        version = manifest.get("version", "")
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            issues.append(f"Invalid version format: {version" (use x.y.z)")

        # Description length
        description = manifest.get("description", "")
        if len(description) > 200:
            warnings.append(f"Description too long: {len(description)" chars (max 200)")

        # Author validation
        author = manifest.get("author")
        if author and not isinstance(author, dict):
            issues.append("Author must be an object with name, email, url fields")
        elif author:
            if "name" not in author:
                issues.append("Author object missing required field: name")

    except json.JSONDecodeError as e:
        issues.append(f"Plugin manifest JSON error: {e"")
    except UnicodeDecodeError:
        issues.append("Plugin manifest encoding error (must be UTF-8)")

    # 2. Directory Structure Validation
    required_dirs = [".claude-plugin", "agents", "skills", "commands"]
    for dir_name in required_dirs:
        dir_path = plugin_path / dir_name
        if not dir_path.exists():
            issues.append(f"Missing required directory: {dir_name"/")

    # 3. Agent Files Validation
    agents_dir = plugin_path / "agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            stats["agents"] += 1
            stats["total_files"] += 1

            try:
                with open(agent_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check YAML frontmatter
                if content.startswith("---"):
                    try:
                        frontmatter_end = content.find("---", 3)
                        if frontmatter_end == -1:
                            issues.append(f"Unclosed YAML frontmatter: {agent_file"")
                            continue

                        frontmatter_str = content[3:frontmatter_end].strip()
                        frontmatter_data = yaml.safe_load(frontmatter_str)

                        # Required agent fields
                        if "name" not in frontmatter_data:
                            issues.append(f"Agent missing name: {agent_file"")
                        if "description" not in frontmatter_data:
                            issues.append(f"Agent missing description: {agent_file"")
                        elif len(frontmatter_data.get("description", "")) > 100:
                            warnings.append(f"Agent description too long: {agent_file"")

                    except yaml.YAMLError as e:
                        issues.append(f"YAML error in {agent_file": {str(e)[:50]}")
                else:
                    issues.append(f"Agent missing YAML frontmatter: {agent_file"")

            except UnicodeDecodeError:
                issues.append(f"Invalid file encoding: {agent_file"")

    # 4. Skill Files Validation
    skills_dir = plugin_path / "skills"
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    stats["skills"] += 1
                    stats["total_files"] += 1

                    try:
                        with open(skill_file, "r", encoding="utf-8") as f:
                            content = f.read()

                        # Check YAML frontmatter
                        if content.startswith("---"):
                            try:
                                frontmatter_end = content.find("---", 3)
                                if frontmatter_end == -1:
                                    issues.append(f"Unclosed YAML frontmatter: {skill_file"")
                                    continue

                                frontmatter_str = content[3:frontmatter_end].strip()
                                frontmatter_data = yaml.safe_load(frontmatter_str)

                                # Required skill fields
                                if "name" not in frontmatter_data:
                                    issues.append(f"Skill missing name: {skill_file"")
                                if "description" not in frontmatter_data:
                                    issues.append(f"Skill missing description: {skill_file"")
                                elif len(frontmatter_data.get("description", "")) > 200:
                                    warnings.append(f"Skill description too long: {skill_file"")
                                if "version" not in frontmatter_data:
                                    issues.append(f"Skill missing version: {skill_file"")

                            except yaml.YAMLError as e:
                                issues.append(f"YAML error in {skill_file": {str(e)[:50]}")
                        else:
                            issues.append(f"Skill missing YAML frontmatter: {skill_file"")

                    except UnicodeDecodeError:
                        issues.append(f"Invalid file encoding: {skill_file"")

    # 5. Command Files Validation
    commands_dir = plugin_path / "commands"
    if commands_dir.exists():
        for cmd_file in commands_dir.glob("*.md"):
            stats["commands"] += 1
            stats["total_files"] += 1

            try:
                with open(cmd_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Basic validation - should have content
                if len(content.strip()) < 50:
                    warnings.append(f"Command file too short: {cmd_file"")

            except UnicodeDecodeError:
                issues.append(f"Invalid file encoding: {cmd_file"")

    # 6. Library Files Validation
    lib_dir = plugin_path / "lib"
    if lib_dir.exists():
        for lib_file in lib_dir.glob("*.py"):
            stats["lib_files"] += 1
            stats["total_files"] += 1

            try:
                with open(lib_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Basic Python syntax check
                try:
                    compile(content, str(lib_file), "exec")
                except SyntaxError as e:
                    issues.append(f"Python syntax error in {lib_file": {e}")

            except UnicodeDecodeError:
                issues.append(f"Invalid file encoding: {lib_file"")

    return issues, warnings, stats


def main():
    """Run comprehensive plugin validation."""
    print("Claude Plugin Validation Against Official Guidelines")
    print("=" * 60)

    issues, warnings, stats = validate_claude_plugin()

    print(f"\nPlugin Statistics:")
    print(f'  Agents: {stats["agents"]}')
    print(f'  Skills: {stats["skills"]}')
    print(f'  Commands: {stats["commands"]}')
    print(f'  Library Files: {stats["lib_files"]}')
    print(f'  Total Files: {stats["total_files"]}')

    if issues:
        print(f"\nCRITICAL ISSUES ({len(issues)"):")
        for issue in issues[:10]:
            print(f"  - {issue"")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10" more issues")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)"):")
        for warning in warnings[:5]:
            print(f"  - {warning"")
        if len(warnings) > 5:
            print(f"  ... and {len(warnings) - 5" more warnings")

    if not issues:
        print("\nNo critical issues found!")

    if len(issues) == 0 and len(warnings) <= 2:
        print("\nPlugin is READY for marketplace release!")
    else:
        print(f'\nOverall Status: {"NEEDS FIXES" if issues else "MINOR ISSUES"}')

"""
    # Calculate quality score
    quality_score = 100
    quality_score -= len(issues) * 10
    quality_score -= len(warnings) * 2
    quality_score = max(0, quality_score)

    print(f"\nQuality Score: {quality_score"/100")

    if quality_score >= 90:
        status = "EXCELLENT - Ready for production"
    elif quality_score >= 70:
        status = "GOOD - Minor improvements recommended"
    elif quality_score >= 50:
        status = "FAIR - Some fixes needed"
    else:
        status = "NEEDS WORK - Critical fixes required"

    print(f"Assessment: {status"")

    return 0 if len(issues) == 0 else 1


if __name__ == "__main__":
    exit(main())
