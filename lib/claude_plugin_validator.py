#!/usr/bin/env python3
"""
Claude Plugin Validator - Official Guidelines Compliance Checker

Comprehensive validation for Claude Code plugins to prevent installation failures
and ensure compliance with official plugin development guidelines.
"""

import json
import yaml
import re
import sys
from pathlib import Path
import argparse


class ClaudePluginValidator:
    """Validates Claude Code plugins against official guidelines."""

    def __init__(self, plugin_dir: str = "."):
        self.plugin_dir = Path(plugin_dir)
        self.issues = []
        self.warnings = []
        self.fixes = []

    def validate_all(self) -> dict:
        """Run comprehensive validation."""
        print("Claude Plugin Validation Against Official Guidelines")
        print("=" * 60)

        # Core validation checks
        self._validate_plugin_manifest()
        self._validate_directory_structure()
        self._validate_file_formats()
        self._validate_encoding()
        self._validate_cross_platform_compatibility()
        self._validate_installation_readiness()

        return self._generate_results()

    def _validate_plugin_manifest(self):
        """Validate .claude-plugin/plugin.json against Claude Code requirements."""
        manifest_path = self.plugin_dir / ".claude-plugin" / "plugin.json"

        print("\nValidating Plugin Manifest...")

        if not manifest_path.exists():
            self.issues.append("Missing plugin manifest: .claude-plugin/plugin.json")
            return

        # Check file encoding first
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            self.issues.append("❌ Plugin manifest encoding error (must be UTF-8)")
            return

        # Validate JSON syntax
        try:
            manifest = json.loads(content)
            print("  ✅ JSON syntax: Valid")
        except json.JSONDecodeError as e:
            self.issues.append(f"❌ Plugin manifest JSON error: {e}")
            return

        # Check required fields
        required_fields = ["name", "version", "description", "author"]
        missing_fields = [field for field in required_fields if field not in manifest]
        if missing_fields:
            self.issues.append(f"❌ Missing required fields: {missing_fields}")
        else:
            print("  ✅ Required fields: Present")

        # Validate field types and content
        if "name" in manifest:
            name = str(manifest["name"])
            if not name or len(name.strip()) == 0:
                self.issues.append("❌ Plugin name cannot be empty")
            elif re.search(r'[<>:"/\\|?*]', name):
                self.issues.append("❌ Plugin name contains invalid characters")
            else:
                print(f"  ✅ Plugin name: {name}")

        # Version format validation
        if "version" in manifest:
            version = str(manifest["version"])
            if not re.match(r"^\d+\.\d+\.\d+$", version):
                self.issues.append(f"❌ Invalid version format: {version} (use x.y.z)")
            else:
                print(f"  ✅ Version format: {version}")

        # Description validation
        if "description" in manifest:
            desc = str(manifest["description"])
            if len(desc) < 10:
                self.warnings.append("⚠️  Plugin description too short (< 10 chars)")
            elif len(desc) > 2000:
                self.warnings.append("⚠️  Plugin description too long (> 2000 chars)")
            else:
                print(f"  ✅ Description: {len(desc)} chars")

        # Author validation
        if "author" in manifest:
            author = manifest["author"]
            if isinstance(author, dict):
                required_author_fields = ["name"]
                missing_author = [f for f in required_author_fields if f not in author]
                if missing_author:
                    self.warnings.append(f"⚠️  Missing author fields: {missing_author}")
                else:
                    print(f"  ✅ Author: {author.get('name', 'Unknown')}")
            elif isinstance(author, str):
                print(f"  ✅ Author: {author}")
            else:
                self.warnings.append("⚠️  Author field has unexpected format")

        # Check file size
        file_size = manifest_path.stat().st_size
        if file_size > 1024 * 1024:  # 1MB
            self.warnings.append(
                f"⚠️  Plugin manifest large: {file_size / 1024:.1f}KB (>1MB)",
            )
        else:
            print(f"  ✅ File size: {file_size} bytes")

        self.fixes.append(
            "manifest_validated",
            "Plugin manifest validated against Claude Code guidelines",
        )

    def _validate_directory_structure(self):
        """Validate required directory structure."""
        print("\n📁 Validating Directory Structure...")

        # Required directories
        required_structure = {
            ".claude-plugin": "Plugin configuration directory",
        }

        optional_structure = {
            "agents": "Agent definitions",
            "skills": "Skill definitions",
            "commands": "Command definitions",
            "lib": "Python utility scripts",
            "patterns": "Auto-fix patterns",
        }

        # Check required structure
        for dir_name, description in required_structure.items():
            dir_path = self.plugin_dir / dir_name
            if dir_path.exists():
                if dir_path.is_dir():
                    print(f"  ✅ {dir_name}/: Present ({description})")
                else:
                    self.issues.append(f"❌ {dir_name} exists but is not a directory")
            else:
                self.issues.append(f"❌ Missing required directory: {dir_name}/")

        # Check optional structure
        for dir_name, description in optional_structure.items():
            dir_path = self.plugin_dir / dir_name
            if dir_path.exists():
                if dir_path.is_dir():
                    file_count = len(list(dir_path.glob("*")))
                    print(
                        f"  ✅ {dir_name}/: Present ({file_count} files - {description})", )
                else:
                    self.warnings.append(
                        f"⚠️  {dir_name} exists but is not a directory",
                    )
            else:
                print(f"  ⚪ {dir_name}/: Optional ({description})")

        # Check for plugin manifest specifically
        manifest_path = self.plugin_dir / ".claude-plugin" / "plugin.json"
        if manifest_path.exists():
            print("  ✅ plugin.json: Found in .claude-plugin/")
        else:
            self.issues.append("❌ plugin.json: Not found in .claude-plugin/")

    def _validate_file_formats(self):
        """Validate file format compliance."""
        print("\n📄 Validating File Formats...")

        # Validate agent files
        agents_dir = self.plugin_dir / "agents"
        if agents_dir.exists():
            agent_files = list(agents_dir.glob("*.md"))
            valid_agents = 0
            for agent_file in agent_files:
                if self._validate_markdown_file(agent_file, "agent"):
                    valid_agents += 1
            print(f"  ✅ Agent files: {valid_agents}/{len(agent_files)} valid")

        # Validate skill files
        skills_dir = self.plugin_dir / "skills"
        if skills_dir.exists():
            skill_files = []
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_file = skill_dir / "SKILL.md"
                    if skill_file.exists():
                        skill_files.append(skill_file)

            valid_skills = 0
            for skill_file in skill_files:
                if self._validate_markdown_file(skill_file, "skill"):
                    valid_skills += 1
            print(f"  ✅ Skill files: {valid_skills}/{len(skill_files)} valid")

        # Validate command files
        commands_dir = self.plugin_dir / "commands"
        if commands_dir.exists():
            command_files = list(commands_dir.glob("*.md"))
            valid_commands = 0
            for cmd_file in command_files:
                if cmd_file.name.startswith("."):
                    self.warnings.append(
                        f"⚠️  Command file starts with dot: {cmd_file.name}",
                    )
                if self._validate_markdown_file(cmd_file, "command"):
                    valid_commands += 1
            print(f"  ✅ Command files: {valid_commands}/{len(command_files)} valid")

    def _validate_markdown_file(self, file_path: Path, file_type: str) -> bool:
        """Validate a single markdown file format."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check YAML frontmatter
            if content.startswith("---"):
                try:
                    frontmatter_end = content.find("---", 3)
                    if frontmatter_end == -1:
                        self.warnings.append(
                            f"⚠️  Unclosed YAML frontmatter: {file_path.name}",
                        )
                        return False

                    frontmatter_str = content[3:frontmatter_end].strip()
                    frontmatter = yaml.safe_load(frontmatter_str)

                    # Check required fields based on file type
                    if file_type in ["agent", "skill"]:
                        if "name" not in frontmatter:
                            self.warnings.append(
                                f"⚠️  Missing name in {file_type}: {file_path.name}",
                            )
                        if "description" not in frontmatter:
                            self.warnings.append(
                                f"⚠️  Missing description in {file_type}: {
                                    file_path.name}", )
                        if file_type == "skill" and "version" not in frontmatter:
                            self.warnings.append(
                                f"⚠️  Missing version in skill: {file_path.name}",
                            )

                except yaml.YAMLError as e:
                    self.warnings.append(
                        f"⚠️  YAML error in {file_path.name}: {str(e)[:50]}",
                    )
                    return False

            # Check content quality
            if len(content.strip()) < 100:
                self.warnings.append(f"⚠️  File seems too short: {file_path.name}")

            return True

        except UnicodeDecodeError:
            self.issues.append(f"❌ Invalid file encoding: {file_path}")
            return False
        except Exception as e:
            self.warnings.append(
                f"⚠️  Error validating {file_path.name}: {str(e)[:50]}",
            )
            return False

    def _validate_encoding(self):
        """Validate file encoding throughout plugin."""
        print("\n🔤 Validating File Encoding...")

        encoding_issues = 0
        files_checked = 0

        # Check common file types for encoding
        for pattern in ["**/*.json", "**/*.md", "**/*.py", "**/*.yml", "**/*.yaml"]:
            for file_path in self.plugin_dir.glob(pattern):
                files_checked += 1
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        f.read()
                except UnicodeDecodeError:
                    encoding_issues += 1
                    self.issues.append(
                        f"❌ Invalid encoding (not UTF-8): {file_path.relative_to(self.plugin_dir)}",
                    )

        if encoding_issues == 0:
            print(f"  ✅ File encoding: UTF-8 ({files_checked} files)")
        else:
            print(
                f"  ❌ File encoding: {encoding_issues} issues out of {files_checked} files", )

    def _validate_cross_platform_compatibility(self):
        """Validate cross-platform compatibility."""
        print("\n🌐 Validating Cross-Platform Compatibility...")

        # Check for path length issues
        long_paths = []
        for file_path in self.plugin_dir.rglob("*"):
            if file_path.is_file():
                path_str = str(file_path)
                if len(path_str) > 200:  # Conservative limit
                    long_paths.append(file_path.relative_to(self.plugin_dir))

        if long_paths:
            self.warnings.append(
                f"⚠️  Long file paths found (Windows limit 260 chars): {
                    len(long_paths)} files", )
        else:
            print("  ✅ Path lengths: All under limits")

        # Check for problematic characters in filenames
        problematic_files = []
        for file_path in self.plugin_dir.rglob("*"):
            if file_path.is_file():
                filename = file_path.name
                if re.search(r'[<>:"|?*]', filename):
                    problematic_files.append(filename)

        if problematic_files:
            self.warnings.append(
                f"⚠️  Filenames with problematic characters: {len(problematic_files)}",
            )
        else:
            print("  ✅ Filename characters: All valid")

        # Check line endings in script files
        for script_file in self.plugin_dir.glob("**/*.py"):
            try:
                with open(script_file, "rb") as f:
                    content = f.read()
                    if b"\r\n" in content:
                        self.warnings.append(
                            f"⚠️  CRLF line endings in {
                                script_file.name} (should be LF)", )
            except BaseException:
                pass

        print("  ✅ Cross-platform compatibility: Checked")

    def _validate_installation_readiness(self):
        """Validate plugin readiness for installation."""
        print("\n🚀 Validating Installation Readiness...")

        # Check for common installation blockers
        installation_blockers = []

        # 1. Manifest syntax and structure
        manifest_path = self.plugin_dir / ".claude-plugin" / "plugin.json"
        if manifest_path.exists():
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)

                # Check for empty required fields
                for field in ["name", "description"]:
                    if field in manifest and not str(manifest[field]).strip():
                        installation_blockers.append(f"Empty {field} field")

            except BaseException:
                installation_blockers.append("Invalid plugin manifest")

        # 2. File permissions
        try:
            # Test read access to critical files
            manifest_path.read_text(encoding="utf-8")
            print("  ✅ File permissions: Readable")
        except Exception as e:
            installation_blockers.append(f"File permission error: {e}")

        # 3. Directory structure integrity
        if not (self.plugin_dir / ".claude-plugin").exists():
            installation_blockers.append("Missing .claude-plugin directory")

        if installation_blockers:
            self.issues.extend(
                [
                    f"❌ Installation blocker: {blocker}"
                    for blocker in installation_blockers
                ],
            )
        else:
            print("  ✅ Installation readiness: No blockers found")

    def _generate_results(self) -> dict:
        """Generate validation results."""
        total_issues = len(self.issues)
        total_warnings = len(self.warnings)
        total_fixes = len(self.fixes)

        # Calculate score
        score = 100
        score -= total_issues * 10  # -10 points per issue
        score -= total_warnings * 2  # -2 points per warning
        score = max(0, score)

        # Determine status
        if total_issues == 0:
            if total_warnings == 0:
                status = "PERFECT"
                status_emoji = "🎉"
            else:
                status = "READY"
                status_emoji = "✅"
        else:
            status = "NEEDS_FIXES"
            status_emoji = "🔧"

        results = {
            "status": status,
            "status_emoji": status_emoji,
            "score": score,
            "issues": self.issues,
            "warnings": self.warnings,
            "fixes": self.fixes,
            "summary": self._generate_summary(),
        }

        return results

    def _generate_summary(self) -> str:
        """Generate validation summary."""
        lines = []
        lines.append(
            f"Status: {self.issues and '❌ NEEDS FIXES' or '✅ READY FOR RELEASE'}",
        )
        lines.append(
            f"Score: {max(0, 100 - (len(self.issues) * 10) - (len(self.warnings) * 2))}/100",
        )
        lines.append(f"Issues: {len(self.issues)} | Warnings: {len(self.warnings)}")

        if self.issues:
            lines.append("\n🚨 CRITICAL ISSUES (Installation Blockers):")
            for issue in self.issues[:5]:
                lines.append(f"  • {issue}")
            if len(self.issues) > 5:
                lines.append(f"  ... and {len(self.issues) - 5} more issues")

        if self.warnings:
            lines.append("\n⚠️  WARNINGS:")
            for warning in self.warnings[:3]:
                lines.append(f"  • {warning}")
            if len(self.warnings) > 3:
                lines.append(f"  ... and {len(self.warnings) - 3} more warnings")

        if not self.issues and not self.warnings:
            lines.append(
                "\n🎉 Perfect! Plugin is fully compliant with Claude Code guidelines",
            )

        return "\n".join(lines)


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(
        description="Validate Claude Code plugin compliance"
    )
    parser.add_argument("--dir", default=".", help="Plugin directory")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors",
    )

    args = parser.parse_args()

    try:
        validator = ClaudePluginValidator(args.dir)
        results = validator.validate_all()

        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(results["summary"])
        print("=" * 60)

        # Exit code based on results
        if args.strict and results["warnings"]:
            print("\n❌ Validation failed (strict mode - warnings treated as errors)")
            sys.exit(1)
        elif results["issues"]:
            print("\n❌ Validation failed (critical issues found)")
            sys.exit(1)
        else:
            print("\n✅ Validation passed - Plugin ready for release!")
            sys.exit(0)

    except Exception as e:
        print(f"\n❌ Validation error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
