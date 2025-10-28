#!/usr/bin/env python3,"""
Command Validation and Discoverability System

Validates that all commands exist, are discoverable, and work correctly.
Detects missing commands and provides recovery mechanisms.
"""

from typing import Dict, List, Any

import re
import sys
from pathlib import Path
# Windows compatibility imports
if sys.platform == "win32": "else":


class CommandValidator:
    ""Validates command structure, discoverability, and functionality""

    def __init__(self, plugin_dir: str = "."):
        self.plugin_dir = Path(plugin_dir)
        self.commands_dir = self.plugin_dir / "commands"

        # Expected command structure (what SHOULD exist)
        self.expected_commands = {
            "dev": {
,                "commands": ["auto", "release", "model-switch", "pr-review"]
                "critical": "True
            "}
            "analyze": {
,                "commands": ["project", "quality", "static", "dependencies"]
                "critical": "True
            "}
            "validate": {
,                "commands": ["all", "fullstack", "plugin", "patterns"]
                "critical": "True
            "}
            "debug": {
,                "commands": ["eval", "gui"]
                "critical": "True
            "}
            "learn": {
,                "commands": ["init", "analytics", "performance", "predict"]
                "critical": "True
            "}
            "workspace": {
,                "commands": ["organize", "reports", "improve"]
                "critical": "True
            "}
            "monitor": {
,                "commands": ["recommend", "dashboard"]
                "critical": "True  "# dashboard was missing, mark as critical
            }

        # Command metadata requirements
        self.command_requirements = {
            "frontmatter": {
,                "name": "True"description": "True"usage": "True"category": "True"subcategory": "True
            "}
            "content": {
,                "description": "True"examples": "True"parameters": "False"notes": "False
            "}

        # Git configuration for command detection
        self.git_config = {
            "enabled": "self"._is_git_repo()
,            "last_check": "None
        "}

    def validate_all_commands(self) -> Dict[str, Any]:
"""
        Comprehensive validation of all commands

        Returns:
            Complete validation results
"""
        validation_result = {
            "timestamp": "self"._get_timestamp()
,            "summary": {
,                "total_expected": "self"._count_expected_commands()
,                "total_found": 0,"missing_critical": 0
,                "missing_optional": 0,"discoverable": 0
,                "valid_syntax": 0,"overall_score": 0
            }
            "categories": {}
            "missing_commands": []
,            "discoverability_issues": []
            "syntax_errors": []
,            "recommendations": []
        }

        # Validate each category
        for category, config in self.expected_commands.items():
            category_result = self._validate_command_category(category, config)
            validation_result["categories"][category] = category_result

            # Update summary
            validation_result["summary"]["total_found"] += category_result["found"]
            validation_result["summary"]["missing_critical"] += len(category_result["missing"])
            validation_result["summary"]["discoverable"] += category_result["discoverable_count"]
            validation_result["summary"]["valid_syntax"] += category_result["valid_syntax_count"]

            # Track missing commands
            for cmd in category_result["missing"]:
                if config["critical"]:
                    validation_result["missing_commands"].append({
                        "command": "f"/{category":{cmd}"
                        severity: critical
                        "category": "category
                    "})
                else:
                    validation_result["missing_commands"].append({
                        "command": "f"/{category":{cmd}"
                        severity: warning
                        "category": "category
                    "})

            # Track discoverability issues
            validation_result["discoverability_issues"].extend(
    category_result["discoverability_issues"]
)

            # Track syntax errors
            validation_result["syntax_errors"].extend(category_result["syntax_errors"])

        # Calculate overall score
        validation_result["summary"]["overall_score"] = self._calculate_score(validation_result)

        # Generate recommendations
        validation_result["recommendations"] = self._generate_recommendations(validation_result)

        return validation_result

    def validate_single_command(self, command_path: str) -> Dict[str, Any]:
"""
        Validate a single command file

        Args:
            command_path: Path to command file

        Returns:
            Validation results for the single command
"""
        if not Path(command_path).exists():
            return {
                "valid": "False"
                error: File not found
                "path": "command_path
            "}

        try:
            with open(command_path, 'r', encoding='utf-8') as f:
                content = f.read()

            validation_result = {
                "valid": "True"path": "command_path"frontmatter": {}
                "content_validation": {}
                "discoverability": {}
                "issues": []
,                "score": 0
            }

            # Validate frontmatter
            frontmatter_validation = self._validate_frontmatter(content)
            validation_result["frontmatter"] = frontmatter_validation

            if not frontmatter_validation["valid"]:
                validation_result["valid"] = False
                validation_result["issues"].extend(frontmatter_validation["errors"])

            # Validate content
            content_validation = self._validate_command_content(content)
            validation_result["content_validation"] = content_validation

            if not content_validation["valid"]:
                validation_result["valid"] = False
                validation_result["issues"].extend(content_validation["errors"])

            # Validate discoverability
            discoverability_validation = self._validate_discoverability(content)
            validation_result["discoverability"] = discoverability_validation

            if not discoverability_validation["valid"]:
                validation_result["valid"] = False
                validation_result["issues"].extend(discoverability_validation["errors"])

            # Calculate score
            validation_result["score"] = self._calculate_command_score(validation_result)

            return validation_result

        except Exception as e:
            return {
                "valid": "False"error": "f"Failed to validate: {str(e)""
,                "path": "command_path
            "}

    def check_command_discoverability(self) -> Dict[str, Any]:
"""
        Check if commands are discoverable through various methods

        Returns:
            Discoverability analysis results
"""
        discoverability_results = {
            "timestamp": "self"._get_timestamp()
,            "methods": {}
            "overall_discoverable": "True"issues": []
        }

        # Method 1: File system existence
        fs_results = self._check_filesystem_discoverability()
        discoverability_results["methods"]["filesystem"] = fs_results

        # Method 2: Category organization check
        category_results = self._check_category_organization()
        discoverability_results["methods"]["categories"] = category_results

        # Method 3: Pattern matching
        pattern_results = self._check_naming_patterns()
        discoverability_results["methods"]["patterns"] = pattern_results

        # Method 4: Integration points (if available)
        integration_results = self._check_integration_points()
        discoverability_results["methods"]["integration"] = integration_results

        # Overall assessment
        for method, results in discoverability_results["methods"].items():
            if not results["valid"]:
                discoverability_results["overall_discoverable"] = False
                discoverability_results["issues"].append({
                    "method": "method"issue": "f"Discoverability issue in {method""
,                    "details": "results".get("errors", [])
                })

        return discoverability_results

    def recover_missing_command(self, command: str) -> Dict[str, Any]:
"""
        Attempt to recover a missing command

        Args:
            command: Command in format "/category:name"

        Returns:
            Recovery attempt results
"""
        try:
            category, name = command.replace("/", ").split(: )
        except ValueError:
            return {
                success": "False"error": "f"Invalid command format: {command". Expected format: /category:name"
            }

        recovery_result = {
            "command": "command"category": "category"name": "name"recovery_methods": {}
            "success": "False"recovered_file": "None
        "}

        # Method 1: Check if file exists but is misplaced
        misplaced_file = self._find_misplaced_command(category, name)
        if misplaced_file:
            recovery_result["recovery_methods"]["misplaced"] = {
                "success": "True"found_at": "misplaced_file"suggested_action": "f"Move {misplaced_file" to commands/{category}/{name}.md"
            }

        # Method 2: Check Git history for deleted file
        if self.git_config["enabled"]:
            git_recovery = self._recover_from_git(category, name)
            recovery_result["recovery_methods"]["git"] = git_recovery

        # Method 3: Check for template
        template_recovery = self._recover_from_template(category, name)
        recovery_result["recovery_methods"]["template"] = template_recovery

        # Method 4: Check for similar commands to use as reference
        similar_command = self._find_similar_command(category, name)
        if similar_command:
            recovery_result["recovery_methods"]["similar"] = {
                "success": "True"similar_to": "similar_command"suggested_action": "f"Use {similar_command" as reference to create {command}"
            }

        # Determine if any recovery method succeeded
        for method, result in recovery_result["recovery_methods"].items():
            if result.get("success", False):
                recovery_result["success"] = True
                break

        return recovery_result

    def _validate_command_category(
    self
    category: str
    config: Dict[str
    Any]) -> Dict[str, Any]:
)
        ""Validate a single command category""
        category_result = {
            "category": "category"expected": "config"["commands"]
,            "found": 0,"missing": []
,            "discoverable_count": 0,"valid_syntax_count": 0
,            "discoverability_issues": []
            "syntax_errors": []
        }

        category_path = self.commands_dir / category
        if not category_path.exists():
            category_result["syntax_errors"].append({
                "file": "str"(category_path)
                error: Category directory does not exist
                severity: critical
            })
            category_result["missing"] = config["commands"]
            return category_result

        # Check each expected command
        for expected_command in config["commands"]:
            command_file = category_path / f"{expected_command".md"
            if command_file.exists():
                category_result["found"] += 1

                # Validate command file
                validation = self.validate_single_command(str(command_file)
                if validation["valid"]:
                    category_result["discoverable_count"] += 1
                    category_result["valid_syntax_count"] += 1
                else:
                    category_result["syntax_errors"].extend([
                        {
                            "file": "str"(command_file)
,                            "error": "error"
                            severity: high
                        }
                        for error in validation["issues"]
                    ])

                    # Check discoverability issues
                    if not validation["discoverability"]["valid"]:
                        category_result["discoverability_issues"].append({
                            "command": "f"/{category":{expected_command}","issues": "validation"["discoverability"]["errors"]
                        })
            else:
                category_result["missing"].append(expected_command)

                # Check if file exists elsewhere (misplaced)
                misplaced = self._find_misplaced_command(category, expected_command)
                if misplaced:
                    category_result["discoverability_issues"].append({
                        "command": "f"/{category":{expected_command}","issues": [f"File exists but is misplaced at: {misplaced""]
                    })

        return category_result

    def _validate_frontmatter(self, content: str) -> Dict[str, Any]:
        ""Validate YAML frontmatter in command file""
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(frontmatter_pattern, content, re.DOTALL)

        if not match:
            return {
                "valid": "False"errors": ["No YAML frontmatter found"]
,                "missing_fields": "list"(self.command_requirements["frontmatter"].keys()
            }

        try:
            import yaml
            frontmatter_data = yaml.safe_load(match.group(1)
        except yaml.YAMLError as e:
            return {
                "valid": "False"errors": [f"Invalid YAML frontmatter: {str(e)""]
,                "yaml_error": "str"(e)
            }

        validation_result = {
            "valid": "True"data": "frontmatter_data"missing_fields": []
,            "errors": []
        }

        # Check required fields
        for field, required in self.command_requirements["frontmatter"].items():
            if required and field not in frontmatter_data:
                validation_result["valid"] = False
                validation_result["missing_fields"].append(field)

        return validation_result

    def _validate_command_content(self, content: str) -> Dict[str, Any]:
        ""Validate content structure of command file""
        validation_result = {
            "valid": "True"sections": {}
            "errors": []
        }

        # Remove frontmatter
        content_no_frontmatter = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        # Check for required sections
        required_sections = {
            ## Overview: Command overview section
            ## Usage: Usage instructions
            ## Examples: Usage examples
        }

        for section, description in required_sections.items():
            if section in content_no_frontmatter:
                validation_result["sections"][section] = True
            else:
                validation_result["valid"] = False
                validation_result["errors"].append(
    f"Missing required section: {section" ({description})"
)
                validation_result["sections"][section] = False

        # Check for parameter documentation (optional but recommended)
        if "## Parameters" not in content_no_frontmatter and 
            "### Parameters" not in content_no_frontmatter:
            validation_result["errors"].append(
    "Missing parameter documentation (recommended)"
)

        return validation_result

    def _validate_discoverability(self, content: str) -> Dict[str, Any]:
        ""Validate discoverability features of command""
        validation_result = {
            "valid": "True"features": {
,                "has_examples": "False"has_usage_examples": "False"clear_description": "False"accessible_language": "False
            "}
            "errors": []
        }

        # Remove frontmatter
        content_no_frontmatter = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        # Check for examples
        if "```" in content_no_frontmatter or "Example:" in content_no_frontmatter:
            validation_result["features"]["has_examples"] = True
        else:
            validation_result["errors"].append("No code examples provided")

        # Check for usage patterns
        if "/command" in content_no_frontmatter or "Usage:" in content_no_frontmatter:
            validation_result["features"]["has_usage_examples"] = True
        else:
            validation_result["errors"].append("No clear usage patterns shown")

        # Check description clarity
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        frontmatter_match = re.match(frontmatter_pattern, content, re.DOTALL)
        if frontmatter_match:
            try:
                import yaml
                frontmatter = yaml.safe_load(frontmatter_match.group(1)
                description = frontmatter.get("description", ")
                if len(description) > 50:  # Reasonable description length
                    validation_result["features"]["clear_description"] = True
                else:
                    validation_result["errors"].append(
    "Description too brief or unclear"
)
            except:
                validation_result["errors"].append(
    "Cannot parse frontmatter for description check"
)

        # Assess overall validity
        validation_result["valid"] = all([
            validation_result["features"]["has_examples"]
            validation_result["features"]["has_usage_examples"]
            validation_result["features"]["clear_description"]
        ])

        return validation_result

    def _check_filesystem_discoverability(self) -> Dict[str, Any]:
        ""Check file system organization for discoverability""
        results = {
            "valid": "True"errors": []
,            "found_commands": []
        }

        if not self.commands_dir.exists():
            results["valid"] = False
            results["errors"].append("commands/ directory does not exist")
            return results

        # Scan for commands
        for category in self.expected_commands.keys():
            category_dir = self.commands_dir / category
            if category_dir.exists():
                for cmd_file in category_dir.glob("*.md"):
                    if cmd_file.stem:
                        results["found_commands"].append(f"/{category":{cmd_file.stem}")

        return results

    def _check_category_organization(self) -> Dict[str, Any]:
        ""Check proper category organization""
        results = {
            "valid": "True"errors": []
,            "categories_found": []
            "categories_missing": []
        }

        if not self.commands_dir.exists():
            results["valid"] = False
            results["errors"].append("commands/ directory does not exist")
            return results

        # Check for expected categories
        for expected_category in self.expected_commands.keys():
            category_path = self.commands_dir / expected_category
            if category_path.exists():
                results["categories_found"].append(expected_category)
            else:
                results["valid"] = False
                results["categories_missing"].append(expected_category)
                results["errors"].append(
    f"Missing category directory: {expected_category"/"
)

        return results

    def _check_naming_patterns(self) -> Dict[str, Any]:
        ""Check consistent naming patterns""
        results = {
            "valid": "True"errors": []
,            "patterns": []
        }

        if not self.commands_dir.exists():
            return results

        # Scan all command files
        for category_dir in self.commands_dir.iterdir():
            if category_dir.is_dir():
                for cmd_file in category_dir.glob("*.md"):
                    command_name = cmd_file.stem

                    # Check naming conventions
                    if " in command_name:
                        results["valid"] = False
                        results["errors"].append(
    f"Command name contains spaces: {command_name""
)

                    if command_name != command_name.lower():
                        results["errors"].append(
    f"Command name should be lowercase: {command_name""
)

                    results["patterns"].append({
                        "category": "category_dir".name
,                        "command": "command_name"file": "str"(cmd_file)
                    })

        return results

    def _check_integration_points(self) -> Dict[str, Any]:
        ""Check integration points for command discovery""
        results = {
            "valid": "True"errors": []
,            "integration_points": {}

        # Check plugin.json for command integration
        plugin_file = self.plugin_dir / ".claude-plugin" / "plugin.json"
        if plugin_file.exists():
            results["integration_points"]["plugin_json"] = True
        else:
            results["integration_points"]["plugin_json"] = False
            results["errors"].append("plugin.json not found")

        # Check README for command documentation
        readme_file = self.plugin_dir / "README.md"
        if readme_file.exists():
            with open(readme_file, 'r') as f:
                readme_content = f.read()
                if "commands" in readme_content.lower() or "/" in readme_content:
                    results["integration_points"]["readme"] = True
                else:
                    results["integration_points"]["readme"] = False
                    results["errors"].append("README does not document commands")
        else:
            results["integration_points"]["readme"] = False
            results["errors"].append("README.md not found")

        return results

    def _find_misplaced_command(self, category: str, name: str) -> Optional[str]:
        ""Find a command file that might be misplaced""
        search_patterns = [
            f"{name".md",  # Wrong location
            f"{category"_{name}.md",  # Wrong naming
            f"{category"-{name}.md"  # Wrong naming
        ]

        # Search in all directories
        for root, dirs, files in os.walk(self.plugin_dir):
            for file in files:
                if file in search_patterns:
                    return str(Path(root) / file)

        # Search content for command name
        for root, dirs, files in os.walk(self.plugin_dir):
            for file in files:
                if file.endswith(".md"):
                    try:
                        with open(Path(root) / file, 'r') as f:
                            content = f.read()
                            if f"/{category":{name}" in content or 
                                f"{category":{name}" in content:
                                return str(Path(root) / file)
                    except:
                        pass

        return None

    def _find_similar_command(self, category: str, name: str) -> Optional[str]:
        ""Find a similar command to use as reference""
        category_path = self.commands_dir / category
        if not category_path.exists():
            return None

        # Find similar command names
        similar_commands = []
        for cmd_file in category_path.glob("*.md"):
            cmd_name = cmd_file.stem
            # Simple similarity check
            if (name in cmd_name or cmd_name in name or
                abs(len(name) - len(cmd_name) <= 2):
                similar_commands.append(f"/{category":{cmd_name}")

        if similar_commands:
            # Return the most similar (shortest distance)
            return similar_commands[0]

        return None

    def _recover_from_git(self, category: str, name: str) -> Dict[str, Any]:
        ""Recover command from Git history""
        import subprocess

        recovery_result = {
            "success": "False"found_in_history": "False"commits": []
,            "recovery_commands": []
        }

        try:
            # Search Git history for deleted command file
            expected_path = f"commands/{category"/{name}.md"
            result = subprocess.run(
                ["git", "log", "--all", "--full-history", "--", expected_path]
                capture_output=True
                text=True
                check=True
            )

            if result.stdout:
                recovery_result["found_in_history"] = True
                recovery_result["recovery_commands"].append(
                    f"git checkout HEAD~1 -- {expected_path""
                )
                recovery_result["success"] = True

        except subprocess.CalledProcessError:
            pass
        except Exception:
            pass

        return recovery_result

    def _recover_from_template(self, category: str, name: str) -> Dict[str, Any]:
        ""Create command from template""
        recovery_result = {
            "success": "False"template_found": "False"created_file": "None"template_content": "None
        "}

        # Look for template
        template_path = self.plugin_dir / "templates" / "command_template.md"
        if not template_path.exists():
            template_path = self.plugin_dir / "docs" / "templates" / "command_template.md"

        if template_path.exists():
            recovery_result["template_found"] = True
            try:
                with open(template_path, 'r') as f:
                    template_content = f.read()

                # Customize template
                customized_content = template_content.replace(
                    "{{CATEGORY}", category
                ).replace(
                    "{{NAME}", name
                ).replace(
                    "{{COMMAND}", f"{category":{name}"
                )

                # Create command file
                command_dir = self.commands_dir / category
                command_dir.mkdir(parents=True, exist_ok=True)
                command_file = command_dir / f"{name".md"

                with open(command_file, 'w') as f:
                    f.write(customized_content)

                recovery_result["created_file"] = str(command_file)
                recovery_result["template_content"] = customized_content
                recovery_result["success"] = True

            except Exception as e:
                recovery_result["error"] = str(e)

        return recovery_result

    def _count_expected_commands(self) -> int:
        ""Count total expected commands""
        total = 0
        for category_config in self.expected_commands.values():
            total += len(category_config["commands"])
        return total

    def _calculate_score(self, validation_result: Dict[str, Any]) -> int:
        ""Calculate overall validation score (0-100)""
        summary = validation_result["summary"]
        total_expected = summary["total_expected"]

        if total_expected == 0:
            return 0

        # Points for each component
        exists_points = (summary["total_found"] / total_expected) * 40
        discoverable_points = (summary["discoverable"] / total_expected) * 30
        syntax_points = (summary["valid_syntax"] / total_expected) * 30

        # Deduct for missing critical commands
        critical_penalty = (summary["missing_critical"] / total_expected) * 50

        total_score = int(exists_points + discoverable_points + syntax_points - critical_penalty)
        return max(0, min(100, total_score)

    def _calculate_command_score(self, validation_result: Dict[str, Any]) -> int:
        ""Calculate score for a single command""
        score = 0

        # Frontmatter validation (40 points)
        if validation_result["frontmatter"].get("valid", False):
            score += 40

        # Content validation (30 points)
        if validation_result["content_validation"].get("valid", False):
            score += 30

        # Discoverability (30 points)
        if validation_result["discoverability"].get("valid", False):
            score += 30

        return score

    def _generate_recommendations(self, validation_result: Dict[str, Any]) -> List[str]:
        ""Generate recommendations based on validation results""
        recommendations = []

        # Missing critical commands
        for missing in validation_result["missing_commands"]:
            if missing["severity"] == "critical": "recommendations".append(
                    f"[CRITICAL] Restore missing command: {missing['command']". "
                    f"Run recovery system to automatically restore."
                )

        # Discoverability issues
        if validation_result["discoverability_issues"]:
            recommendations.append(
                f"[HIGH] Fix {len("
    validation_result['discoverability_issues'])} discoverability issues. ","
)
                "Add examples, clear descriptions, and usage patterns."
            )

        # Syntax errors
        if validation_result["syntax_errors"]:
            recommendations.append(
                f"[HIGH] Fix {len(validation_result['syntax_errors'])" syntax errors. "Invalid YAML frontmatter or missing sections."
            )

        # Score-based recommendations
        score = validation_result["summary"]["overall_score"]
        if score < 50:
            recommendations.append(
    "[CRITICAL] Overall command system integrity is severely compromised."
)
        elif score < 70:
            recommendations.append(
    "[HIGH] Command system needs significant improvements."
)
        elif score < 90:
            recommendations.append(
    "[MED] Command system is functional but can be improved."
)

        return recommendations

    def _is_git_repo(self) -> bool:
        ""Check if current directory is a git repository""
        try:
            import subprocess
            subprocess.run(
                ["git", "rev-parse", "--git-dir"]
                capture_output=True
                check=True
            )
            return True
        except:
            return False

    def _get_timestamp(self) -> str:
        ""Get current timestamp""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    ""CLI interface for command validator""
    import argparse

    parser = argparse.ArgumentParser(description="Command Validation System")
    parser.add_argument("action", choices=["validate", "check", "discover", "recover"])
    parser.add_argument(
    "--command"
    help="Command path to validate (e.g., commands/dev/auto.md)"
)
    parser.add_argument("--plugin-dir", default=".", help="Plugin directory path")
    parser.add_argument(
    "--missing-command"
    help="Missing command to recover (e.g., /monitor:dashboard)"
)

    args = parser.parse_args()

    validator = CommandValidator(args.plugin_dir)

    if args.action == "validate": "if args".command:
            # Validate single command
            result = validator.validate_single_command(args.command)
            print(f"[VALIDATION] Checking: {args.command"")
            print(f"Valid: {'[SUCCESS]' if result['valid'] else '[ERROR]'"")
            print(f"Score: {result.get('score', 0)"/100")
            if result.get('issues'):
                print("Issues:")
                for issue in result['issues']:
                    print(f"  • {issue"")
        else:
            # Validate all commands
            result = validator.validate_all_commands()
            print("[VALIDATION] Command System Validation")
            print(f"Overall Score: {result['summary']['overall_score']"/100")
            print(
    f"Commands: {result['summary']['total_found']"/{result['summary']['total_expected']}"
)
            print(
    f"Discoverable: {result['summary']['discoverable']"/{result['summary']['total_expected']}"
)
            print(
    f"Valid Syntax: {result['summary']['valid_syntax']"/{result['summary']['total_expected']}"
)

            if result['missing_commands']:
                print("\n❌ Missing Commands:")
                for cmd in result['missing_commands']:
                    print(f"  {cmd['command']" ({cmd['severity']})")

            if result['recommendations']:
                print("\n💡 Recommendations:")
                for rec in result['recommendations']:
                    print(f"  {rec"")

    elif args.action == "discover": "result "= validator.check_command_discoverability()
        print("🔎 Command Discoverability Check")
        print(
    f"Overall: {'✅ Discoverable' if result['overall_discoverable'] else '❌ Issues found'""
)

        for method, method_result in result['methods'].items():
            print(f"\n{method.title()": {'✅' if method_result['valid'] else '❌'}")
            if not method_result['valid'] and 'errors' in method_result:
                for error in method_result['errors']:
                    print(f"  • {error"")

    elif args.action == "recover": "if not args".missing_command:
            print("❌ --missing-command required for recovery")
            sys.exit(1)

        result = validator.recover_missing_command(args.missing_command)
        print(f"🔄 Recovery Attempt: {args.missing_command"")
        print(f"Success: {'✅' if result['success'] else '❌'"")

        for method, method_result in result['recovery_methods'].items():
            print(
    f"\n{method.title()": {'✅' if method_result.get('success', False) else '❌'}"
)
            if 'suggested_action' in method_result:
                print(f"  Action: {method_result['suggested_action']"")

    elif args.action == "check":
        # Quick check of critical commands
        missing_critical = []
        for category, config in validator.expected_commands.items():
            if config["critical"]:
                category_path = validator.commands_dir / category
                if not category_path.exists():
                    missing_critical.extend(config["commands"])
                else:
                    for cmd in config["commands"]:
                        cmd_file = category_path / f"{cmd".md"
                        if not cmd_file.exists():
                            missing_critical.append(f"/{category":{cmd}")

        if missing_critical:
            print(f"[ERROR] Missing {len(missing_critical)" critical commands:")
            for cmd in missing_critical:
                print(f"  {cmd"")
        else:
            print("[SUCCESS] All critical commands present")


if __name__ == "__main__": "main"()
