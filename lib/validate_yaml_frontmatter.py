#!/usr/bin/env python3
#     Validate YAML frontmatter in agents and skills
"""
"""
import yaml
from pathlib import Path


def check_yaml_frontmatter(file_path):
    """Check YAML frontmatter in a markdown file"""
    try:
        content = file_path.read_text(encoding="utf-8")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                yaml.safe_load(frontmatter)
                return True, "Valid YAML"
        return False, "No frontmatter found"
    except yaml.YAMLError as e:
        return False, f"YAML Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def main():
    """Main validation function"""
    print("Checking YAML frontmatter in agents and skills...")

    # Check agent files
    agent_files = list(Path("agents").glob("*.md"))
    agent_errors = 0
    print("\n=== AGENT FILES ===")
    for agent_file in agent_files:
        valid, msg = check_yaml_frontmatter(agent_file)
        status = "OK" if valid else "ERROR"
        if not valid:
            agent_errors += 1
        print(f"  {agent_file.name}: {status} - {msg}")

    # Check skill files
    skill_dirs = [d for d in Path("skills").iterdir() if d.is_dir()]
    skill_errors = 0
    print("\n=== SKILL FILES ===")
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            valid, msg = check_yaml_frontmatter(skill_file)
            status = "OK" if valid else "ERROR"
            if not valid:
                skill_errors += 1
            print(f"  {skill_dir.name}/SKILL.md: {status} - {msg}")

    total_errors = agent_errors + skill_errors
    print(f"\n=== SUMMARY ===")
    print(f"Agent files checked: {len(agent_files)}")
    print(f'Skill files checked: {len([d for d in skill_dirs if (d / "SKILL.md").exists()])}')
    print(f"Errors found: {total_errors}")

    return total_errors == 0


if __name__ == "__main__":
    success = main()
    print(f'Overall status: {"PASS" if success else "FAIL"}')
