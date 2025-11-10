#!/usr/bin/env python3
"""
Distribution Validator for Autonomous Agent Plugin

Validates that the plugin is ready for public distribution by checking:
- Path resolution works correctly
- User-specific data is excluded
- Scripts can be found and executed
- Plugin structure is correct

Usage:
    python validate_distribution.py [--verbose]
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from plugin_path_resolver import get_plugin_path, get_script_path, validate_plugin_installation
except ImportError as e:
    print(f"[ERROR] Error: Could not import plugin_path_resolver: {e}")
    sys.exit(1)


class DistributionValidator:
    """Validates plugin readiness for distribution."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.passed = []

    def log(self, message: str, level: str = "info"):
        """Log a message if verbose mode is enabled."""
        if self.verbose or level in ["error", "warning", "success"]:
            prefix = {
                "error": "[ERROR]",
                "warning": "[WARN]",
                "success": "[PASS]",
                "info": "[INFO]"
            }.get(level, "[INFO]")
            print(f"{prefix} {message}")

    def validate_plugin_json(self) -> bool:
        """Validate plugin.json exists and has required fields."""
        self.log("Validating plugin.json...")

        plugin_path = get_plugin_path()
        if not plugin_path:
            self.log("Plugin path not found", "error")
            self.errors.append("Plugin installation not detected")
            return False

        plugin_json_path = plugin_path / ".claude-plugin" / "plugin.json"
        if not plugin_json_path.exists():
            self.log("plugin.json not found", "error")
            self.errors.append("plugin.json missing")
            return False

        try:
            with open(plugin_json_path, 'r', encoding='utf-8') as f:
                plugin_data = json.load(f)

            required_fields = ["name", "version", "description", "author", "repository"]
            missing_fields = [field for field in required_fields if field not in plugin_data]

            if missing_fields:
                self.log(f"Missing required fields in plugin.json: {missing_fields}", "error")
                self.errors.append(f"plugin.json missing fields: {missing_fields}")
                return False

            self.log("plugin.json is valid", "success")
            self.passed.append("plugin.json validation")
            return True

        except json.JSONDecodeError as e:
            self.log(f"plugin.json is not valid JSON: {e}", "error")
            self.errors.append(f"plugin.json invalid: {e}")
            return False

    def validate_directory_structure(self) -> bool:
        """Validate required directories exist."""
        self.log("Validating directory structure...")

        plugin_path = get_plugin_path()
        if not plugin_path:
            return False

        required_dirs = [
            "agents",
            "commands",
            "skills",
            "lib"
        ]

        all_exist = True
        for dir_name in required_dirs:
            dir_path = plugin_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.log(f"Directory '{dir_name}/' exists", "success")
            else:
                self.log(f"Required directory '{dir_name}/' missing", "error")
                self.errors.append(f"Missing directory: {dir_name}")
                all_exist = False

        if all_exist:
            self.passed.append("Directory structure validation")

        return all_exist

    def validate_python_scripts(self) -> bool:
        """Validate Python scripts exist and are executable."""
        self.log("Validating Python scripts...")

        critical_scripts = [
            "dashboard.py",
            "plugin_path_resolver.py",
            "run_script.py",
            "pattern_storage.py",
            "learning_analytics.py"
        ]

        all_found = True
        for script in critical_scripts:
            script_path = get_script_path(script)
            if script_path and script_path.exists():
                self.log(f"Script '{script}' found", "success")
                # Check if it's readable
                try:
                    with open(script_path, 'r') as f:
                        f.read(10)  # Try to read first 10 bytes
                except Exception as e:
                    self.log(f"Script '{script}' is not readable: {e}", "error")
                    self.errors.append(f"Script not readable: {script}")
                    all_found = False
            else:
                self.log(f"Critical script '{script}' not found", "error")
                self.errors.append(f"Missing script: {script}")
                all_found = False

        if all_found:
            self.passed.append("Python scripts validation")

        return all_found

    def validate_gitignore(self) -> bool:
        """Validate .gitignore excludes user-specific data."""
        self.log("Validating .gitignore...")

        plugin_path = get_plugin_path()
        if not plugin_path:
            return False

        gitignore_path = plugin_path / ".gitignore"
        if not gitignore_path.exists():
            self.log(".gitignore not found", "warning")
            self.warnings.append(".gitignore missing")
            return False

        try:
            with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                gitignore_content = f.read()

            required_exclusions = [
                ".claude/",
                ".claude-patterns/",
                ".claude-unified/",
                "docs/reports/generated/",
                "*.tmp",
                "*.log"
            ]

            missing_exclusions = []
            for exclusion in required_exclusions:
                if exclusion not in gitignore_content:
                    missing_exclusions.append(exclusion)

            if missing_exclusions:
                self.log(f".gitignore missing exclusions: {missing_exclusions}", "warning")
                self.warnings.append(f".gitignore incomplete: {missing_exclusions}")
                return False

            self.log(".gitignore has required exclusions", "success")
            self.passed.append(".gitignore validation")
            return True

        except Exception as e:
            self.log(f"Error reading .gitignore: {e}", "error")
            self.errors.append(f".gitignore error: {e}")
            return False

    def validate_no_hardcoded_paths(self) -> bool:
        """Validate that slash commands don't have hardcoded local paths."""
        self.log("Validating slash commands for hardcoded paths...")

        plugin_path = get_plugin_path()
        if not plugin_path:
            return False

        commands_dir = plugin_path / "commands"
        if not commands_dir.exists():
            self.log("Commands directory not found", "error")
            self.errors.append("Commands directory missing")
            return False

        # Find all markdown files in commands directory
        command_files = list(commands_dir.rglob("*.md"))

        hardcoded_count = 0
        for cmd_file in command_files:
            try:
                with open(cmd_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Check for hardcoded lib paths
                if "python lib/" in content:
                    # Count occurrences
                    occurrences = content.count("python lib/")
                    if occurrences > 0:
                        self.log(f"Found {occurrences} hardcoded path(s) in {cmd_file.relative_to(plugin_path)}", "warning")
                        hardcoded_count += occurrences

            except Exception as e:
                self.log(f"Error reading {cmd_file}: {e}", "error")
                self.errors.append(f"Error reading {cmd_file}")

        if hardcoded_count == 0:
            self.log("No hardcoded paths found in slash commands", "success")
            self.passed.append("Hardcoded paths validation")
            return True
        else:
            self.warnings.append(f"Found {hardcoded_count} hardcoded paths in commands")
            return False

    def validate_agent_files(self) -> bool:
        """Validate that agent files have proper YAML frontmatter."""
        self.log("Validating agent files...")

        plugin_path = get_plugin_path()
        if not plugin_path:
            return False

        agents_dir = plugin_path / "agents"
        if not agents_dir.exists():
            self.log("Agents directory not found", "error")
            self.errors.append("Agents directory missing")
            return False

        agent_files = list(agents_dir.glob("*.md"))
        if not agent_files:
            self.log("No agent files found", "error")
            self.errors.append("No agent files found")
            return False

        valid_agents = 0
        for agent_file in agent_files:
            try:
                with open(agent_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Check for YAML frontmatter
                if content.startswith("---"):
                    self.log(f"Agent {agent_file.name} has YAML frontmatter", "success")
                    valid_agents += 1
                else:
                    self.log(f"Agent {agent_file.name} missing YAML frontmatter", "warning")
                    self.warnings.append(f"Agent missing YAML: {agent_file.name}")

            except Exception as e:
                self.log(f"Error reading agent {agent_file}: {e}", "error")
                self.errors.append(f"Error reading agent: {agent_file}")

        if valid_agents > 0:
            self.log(f"Found {valid_agents} valid agent files", "success")
            self.passed.append("Agent files validation")
            return True
        else:
            self.errors.append("No valid agent files found")
            return False

    def run_all_validations(self) -> Tuple[bool, List[str], List[str], List[str]]:
        """Run all validation checks."""
        self.log("Starting distribution validation...", "info")
        print("=" * 50)

        validations = [
            self.validate_plugin_json,
            self.validate_directory_structure,
            self.validate_python_scripts,
            self.validate_gitignore,
            self.validate_no_hardcoded_paths,
            self.validate_agent_files
        ]

        all_passed = True
        for validation in validations:
            try:
                result = validation()
                if not result:
                    all_passed = False
            except Exception as e:
                self.log(f"Validation failed with error: {e}", "error")
                self.errors.append(f"Validation error: {e}")
                all_passed = False

        return all_passed, self.passed, self.warnings, self.errors

    def print_summary(self, all_passed: bool):
        """Print validation summary."""
        print("\n" + "=" * 50)
        print("DISTRIBUTION VALIDATION SUMMARY")
        print("=" * 50)

        if all_passed:
            print("[SUCCESS] Plugin is READY for public distribution!")
        else:
            print("[FAIL] Plugin is NOT ready for distribution")

        print(f"\n[PASS] Passed: {len(self.passed)}")
        for item in self.passed:
            print(f"  - {item}")

        if self.warnings:
            print(f"\n[WARN] Warnings: {len(self.warnings)}")
            for item in self.warnings:
                print(f"  - {item}")

        if self.errors:
            print(f"\n[ERROR] Errors: {len(self.errors)}")
            for item in self.errors:
                print(f"  - {item}")

        # Recommendations
        print("\n[INFO] Recommendations:")
        if self.errors:
            print("  - Fix all errors before releasing")
        if self.warnings:
            print("  - Review warnings for potential improvements")
        if all_passed:
            print("  - Plugin is ready for marketplace submission")
            print("  - Consider testing installation in a clean environment")


def main():
    parser = argparse.ArgumentParser(description="Validate plugin for distribution")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    validator = DistributionValidator(verbose=args.verbose)
    all_passed, passed, warnings, errors = validator.run_all_validations()
    validator.print_summary(all_passed)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()