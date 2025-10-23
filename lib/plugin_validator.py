#!/usr/bin/env python3
"""
Plugin Validation System for Autonomous Claude Agent Plugin

Comprehensive validation and quality assurance for the autonomous agent plugin.
Validates plugin structure, documentation consistency, JSON manifests, agent/skill
compliance, and generates detailed reports with auto-fix recommendations.
"""

import json
import argparse
import sys
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import platform
import os

# Handle Windows compatibility for file locking
if platform.system() == 'Windows':
    import msvcrt
    def lock_file(f, exclusive=False):
        """Windows file locking using msvcrt."""
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        """Windows file unlocking."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl
    def lock_file(f, exclusive=False):
        """Unix file locking using fcntl."""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)

    def unlock_file(f):
        """Unix file unlocking."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class PluginValidator:
    """Comprehensive plugin validation system."""

    def __init__(self, plugin_dir: str = "."):
        """
        Initialize plugin validator.

        Args:
            plugin_dir: Root directory of the plugin (default: current directory)
        """
        self.plugin_dir = Path(plugin_dir)
        self.issues = []
        self.warnings = []
        self.fixes = []
        self.score = 100  # Start with perfect score, deduct for issues

    def validate_all(self) -> Dict[str, Any]:
        """
        Run comprehensive validation of the plugin.

        Returns:
            Dictionary containing validation results, score, and recommendations
        """
        print("Starting comprehensive plugin validation...")

        # Core structure validation
        self._validate_plugin_manifest()
        self._validate_directory_structure()
        self._validate_agent_files()
        self._validate_skill_files()
        self._validate_command_files()

        # Content validation
        self._validate_documentation()
        self._validate_version_consistency()
        self._validate_yaml_frontmatter()
        self._validate_cross_references()

        # Quality checks
        self._validate_documentation_quality()
        self._check_for_common_issues()

        # Generate results
        return self._generate_results()

    def _validate_plugin_manifest(self):
        """Validate .claude-plugin/plugin.json manifest."""
        manifest_path = self.plugin_dir / ".claude-plugin" / "plugin.json"

        if not manifest_path.exists():
            self.issues.append("Missing .claude-plugin/plugin.json manifest")
            self.score -= 30
            return

        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)

            # Check required fields
            required_fields = ['name', 'version', 'description', 'author', 'repository']
            for field in required_fields:
                if field not in manifest:
                    self.issues.append(f"Missing required field in manifest: {field}")
                    self.score -= 5

            # Validate version format
            version = manifest.get('version', '')
            if not re.match(r'^\d+\.\d+\.\d+$', version):
                self.issues.append(f"Invalid version format: {version} (use x.y.z)")
                self.score -= 5

            # Validate author structure
            if 'author' in manifest and isinstance(manifest['author'], dict):
                author_fields = ['name', 'email', 'url']
                for field in author_fields:
                    if field not in manifest['author']:
                        self.warnings.append(f"Missing author field: {field}")

            self.fixes.append(("manifest_valid", "Plugin manifest is valid and complete"))

        except json.JSONDecodeError as e:
            self.issues.append(f"Invalid JSON in plugin.json: {e}")
            self.score -= 20
        except Exception as e:
            self.issues.append(f"Error reading manifest: {e}")
            self.score -= 10

    def _validate_directory_structure(self):
        """Validate required directory structure."""
        required_dirs = ['agents', 'skills', 'commands', 'lib']

        for dir_name in required_dirs:
            dir_path = self.plugin_dir / dir_name
            if not dir_path.exists():
                self.issues.append(f"Missing required directory: {dir_name}/")
                self.score -= 10
            elif not dir_path.is_dir():
                self.issues.append(f"Path exists but is not directory: {dir_name}/")
                self.score -= 5

        # Check for patterns directory
        patterns_dir = self.plugin_dir / "patterns"
        if patterns_dir.exists():
            patterns_json = patterns_dir / "autofix-patterns.json"
            if patterns_json.exists():
                try:
                    with open(patterns_json, 'r', encoding='utf-8') as f:
                        patterns = json.load(f)

                    if isinstance(patterns, dict) and 'patterns' in patterns:
                        pattern_count = len(patterns['patterns'])
                        if pattern_count > 0:
                            self.fixes.append(("patterns_found", f"Found {pattern_count} auto-fix patterns"))
                    else:
                        self.warnings.append("autofix-patterns.json has unexpected structure")

                except json.JSONDecodeError:
                    self.warnings.append("autofix-patterns.json contains invalid JSON")

    def _validate_agent_files(self):
        """Validate agent files structure and content."""
        agents_dir = self.plugin_dir / "agents"
        if not agents_dir.exists():
            return

        agent_count = 0
        for agent_file in agents_dir.glob("*.md"):
            agent_count += 1

            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for YAML frontmatter
                if not content.startswith('---'):
                    self.issues.append(f"Agent missing YAML frontmatter: {agent_file.name}")
                    self.score -= 3
                    continue

                # Parse YAML frontmatter
                try:
                    frontmatter_end = content.find('---', 3)
                    frontmatter_str = content[3:frontmatter_end].strip()
                    frontmatter = yaml.safe_load(frontmatter_str)

                    # Check required frontmatter fields
                    if 'name' not in frontmatter:
                        self.issues.append(f"Agent missing name in frontmatter: {agent_file.name}")
                        self.score -= 2

                    if 'description' not in frontmatter:
                        self.warnings.append(f"Agent missing description: {agent_file.name}")

                except yaml.YAMLError:
                    self.issues.append(f"Invalid YAML frontmatter: {agent_file.name}")
                    self.score -= 3

                # Check content quality
                if len(content) < 500:
                    self.warnings.append(f"Agent file seems too short: {agent_file.name}")

            except Exception as e:
                self.issues.append(f"Error reading agent file {agent_file.name}: {e}")
                self.score -= 2

        if agent_count == 0:
            self.issues.append("No agent files found in agents/ directory")
            self.score -= 20
        else:
            self.fixes.append(("agents_valid", f"Validated {agent_count} agent files"))

    def _validate_skill_files(self):
        """Validate skill files structure and content."""
        skills_dir = self.plugin_dir / "skills"
        if not skills_dir.exists():
            return

        skill_count = 0
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    skill_count += 1

                    try:
                        with open(skill_file, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Check for YAML frontmatter
                        if not content.startswith('---'):
                            self.issues.append(f"Skill missing YAML frontmatter: {skill_dir.name}")
                            self.score -= 3
                            continue

                        # Parse YAML frontmatter
                        try:
                            frontmatter_end = content.find('---', 3)
                            frontmatter_str = content[3:frontmatter_end].strip()
                            frontmatter = yaml.safe_load(frontmatter_str)

                            # Check required frontmatter fields
                            if 'name' not in frontmatter:
                                self.issues.append(f"Skill missing name in frontmatter: {skill_dir.name}")
                                self.score -= 2

                            if 'description' not in frontmatter:
                                self.warnings.append(f"Skill missing description: {skill_dir.name}")

                            if 'version' not in frontmatter:
                                self.warnings.append(f"Skill missing version: {skill_dir.name}")

                        except yaml.YAMLError:
                            self.issues.append(f"Invalid YAML frontmatter in skill: {skill_dir.name}")
                            self.score -= 3

                        # Check content quality
                        if len(content) < 300:
                            self.warnings.append(f"Skill file seems too short: {skill_dir.name}")

                    except Exception as e:
                        self.issues.append(f"Error reading skill file {skill_dir.name}: {e}")
                        self.score -= 2

        if skill_count == 0:
            self.issues.append("No skill files found in skills/ directories")
            self.score -= 15
        else:
            self.fixes.append(("skills_valid", f"Validated {skill_count} skill files"))

    def _validate_command_files(self):
        """Validate command files structure and content."""
        commands_dir = self.plugin_dir / "commands"
        if not commands_dir.exists():
            return

        command_count = 0
        for command_file in commands_dir.glob("*.md"):
            command_count += 1

            try:
                with open(command_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for command name in filename (slash command format)
                if command_file.name.startswith('.'):
                    self.warnings.append(f"Command filename should not start with dot: {command_file.name}")

                # Check content quality and structure
                if len(content) < 300:
                    self.warnings.append(f"Command file seems too short: {command_file.name}")

                # Look for command documentation patterns
                if '## Usage' not in content:
                    self.warnings.append(f"Command missing usage section: {command_file.name}")

                if '```bash' not in content and '```' not in content:
                    self.warnings.append(f"Command missing usage examples: {command_file.name}")

            except Exception as e:
                self.issues.append(f"Error reading command file {command_file.name}: {e}")
                self.score -= 2

        if command_count == 0:
            self.issues.append("No command files found in commands/ directory")
            self.score -= 10
        else:
            self.fixes.append(("commands_valid", f"Validated {command_count} command files"))

    def _validate_documentation(self):
        """Validate documentation files."""
        doc_files = ['README.md', 'CLAUDE.md', 'LICENSE']

        for doc_file in doc_files:
            file_path = self.plugin_dir / doc_file
            if not file_path.exists():
                if doc_file == 'LICENSE':
                    self.warnings.append(f"Missing license file: {doc_file}")
                else:
                    self.issues.append(f"Missing documentation file: {doc_file}")
                    self.score -= 10
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check content quality
                    if doc_file == 'README.md':
                        if len(content) < 1000:
                            self.warnings.append("README.md seems too short for a comprehensive plugin")

                        # Look for key sections
                        required_sections = ['## Features', '## Usage', '## Installation']
                        for section in required_sections:
                            if section not in content:
                                self.warnings.append(f"README missing {section} section")

                    elif doc_file == 'CLAUDE.md':
                        if len(content) < 500:
                            self.warnings.append("CLAUDE.md should contain detailed project instructions")

                        # Look for key information
                        if '## Project Overview' not in content:
                            self.warnings.append("CLAUDE.md missing Project Overview section")

                except Exception as e:
                    self.issues.append(f"Error reading documentation file {doc_file}: {e}")
                    self.score -= 5

        self.fixes.append(("documentation_checked", "Documentation files validated"))

    def _validate_version_consistency(self):
        """Validate version consistency across files."""
        versions = {}

        # Get version from manifest
        manifest_path = self.plugin_dir / ".claude-plugin" / "plugin.json"
        if manifest_path.exists():
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                    versions['manifest'] = manifest.get('version', '')
            except:
                pass

        # Check version references in documentation
        doc_files = ['README.md']
        for doc_file in doc_files:
            file_path = self.plugin_dir / doc_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Look for version patterns
                    version_patterns = [
                        r'version-(\d+\.\d+\.\d+)',
                        r'tag/v(\d+\.\d+\.\d+)',
                        r'\*\*(\d+\.\d+\.\d+)\*\*',
                        r'version[:\s]+(\d+\.\d+\.\d+)'
                    ]

                    for pattern in version_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            versions[doc_file] = matches[0]
                            break

                except:
                    pass

        # Check for inconsistencies
        if len(set(versions.values())) > 1:
            self.issues.append("Version inconsistency detected across files")
            self.score -= 10
            for file_name, version in versions.items():
                self.warnings.append(f"Version in {file_name}: {version}")
        elif versions:
            self.fixes.append(("versions_consistent", f"Version consistency verified: {list(versions.values())[0]}"))

    def _validate_yaml_frontmatter(self):
        """Validate YAML frontmatter in all markdown files."""
        markdown_files = list(self.plugin_dir.glob("**/*.md"))

        frontmatter_errors = 0
        valid_files = 0

        for md_file in markdown_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                if content.startswith('---'):
                    try:
                        frontmatter_end = content.find('---', 3)
                        if frontmatter_end == -1:
                            self.issues.append(f"Unclosed YAML frontmatter: {md_file.relative_to(self.plugin_dir)}")
                            frontmatter_errors += 1
                            continue

                        frontmatter_str = content[3:frontmatter_end].strip()
                        yaml.safe_load(frontmatter_str)
                        valid_files += 1

                    except yaml.YAMLError as e:
                        self.issues.append(f"Invalid YAML in {md_file.relative_to(self.plugin_dir)}: {str(e)[:50]}")
                        frontmatter_errors += 1

            except Exception:
                self.warnings.append(f"Could not read file: {md_file.relative_to(self.plugin_dir)}")

        if frontmatter_errors > 0:
            self.score -= min(frontmatter_errors * 2, 15)
        else:
            self.fixes.append(("yaml_valid", f"YAML frontmatter valid in {valid_files} files"))

    def _validate_cross_references(self):
        """Validate cross-references between components."""
        # Check for broken references in documentation
        readme_path = self.plugin_dir / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Look for file references
                file_refs = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                for ref_name, ref_path in file_refs:
                    if ref_path.startswith('http'):
                        continue  # Skip external URLs

                    ref_full_path = self.plugin_dir / ref_path
                    if not ref_full_path.exists():
                        self.warnings.append(f"Broken reference in README: {ref_path} (linked as '{ref_name}')")

            except:
                pass

        # Check component count consistency
        agents_count = len(list((self.plugin_dir / "agents").glob("*.md"))) if (self.plugin_dir / "agents").exists() else 0
        skills_count = len([d for d in (self.plugin_dir / "skills").iterdir() if d.is_dir() and (d / "SKILL.md").exists()]) if (self.plugin_dir / "skills").exists() else 0
        commands_count = len(list((self.plugin_dir / "commands").glob("*.md"))) if (self.plugin_dir / "commands").exists() else 0

        if agents_count > 0 and skills_count > 0 and commands_count > 0:
            self.fixes.append(("components_counted", f"Found {agents_count} agents, {skills_count} skills, {commands_count} commands"))

    def _validate_documentation_quality(self):
        """Validate documentation quality and completeness."""
        readme_path = self.plugin_dir / "README.md"
        if not readme_path.exists():
            return

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for comprehensive documentation
            quality_indicators = {
                ' badges and shields': r'\[\!\[.*?\]\(.*?\)\]',
                ' installation instructions': '## Installation',
                ' usage examples': '```',
                ' feature list': '## Features',
                ' contributing guide': '## Contributing',
                ' license information': '## License' or 'LICENSE',
                ' changelog': '## Changelog' or '## Version History'
            }

            found_indicators = 0
            for indicator, pattern in quality_indicators.items():
                if isinstance(pattern, str):
                    if pattern in content:
                        found_indicators += 1
                else:  # regex pattern
                    if re.search(pattern, content):
                        found_indicators += 1

            quality_score = (found_indicators / len(quality_indicators)) * 100

            if quality_score >= 80:
                self.fixes.append(("high_quality_docs", f"Documentation quality: {quality_score:.0f}%"))
            elif quality_score >= 60:
                self.warnings.append(f"Documentation quality could be improved: {quality_score:.0f}%")
            else:
                self.warnings.append(f"Documentation needs improvement: {quality_score:.0f}%")

        except:
            pass

    def _check_for_common_issues(self):
        """Check for common plugin issues."""
        # Check for very large files
        for file_path in self.plugin_dir.rglob("*.md"):
            if file_path.stat().st_size > 1024 * 1024:  # > 1MB
                self.warnings.append(f"Large file may impact performance: {file_path.relative_to(self.plugin_dir)}")

        # Check for potential sensitive information
        sensitive_patterns = [
            r'api[_-]?key[_-]?=\s*["\'][^"\']+["\']',
            r'password[_-]?=\s*["\'][^"\']+["\']',
            r'secret[_-]?=\s*["\'][^"\']+["\']',
            r'token[_-]?=\s*["\'][^"\']+["\']'
        ]

        for file_path in self.plugin_dir.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                for pattern in sensitive_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        self.warnings.append(f"Potential sensitive information in {file_path.relative_to(self.plugin_dir)}")
                        break

            except:
                pass

    def _generate_results(self) -> Dict[str, Any]:
        """Generate final validation results."""
        # Ensure score is within bounds
        self.score = max(0, min(100, self.score))

        # Determine quality level
        if self.score >= 90:
            quality_level = "Excellent"
        elif self.score >= 80:
            quality_level = "Good"
        elif self.score >= 70:
            quality_level = "Acceptable"
        elif self.score >= 60:
            quality_level = "Needs Improvement"
        else:
            quality_level = "Poor"

        results = {
            'timestamp': datetime.now().isoformat(),
            'plugin_dir': str(self.plugin_dir),
            'overall_score': self.score,
            'quality_level': quality_level,
            'issues_count': len(self.issues),
            'warnings_count': len(self.warnings),
            'fixes_count': len(self.fixes),
            'issues': self.issues,
            'warnings': self.warnings,
            'fixes': self.fixes,
            'summary': self._generate_summary()
        }

        return results

    def _generate_summary(self) -> str:
        """Generate validation summary."""
        summary = []

        if self.score >= 90:
            summary.append("Plugin is in excellent condition!")
        elif self.score >= 80:
            summary.append("Plugin is in good condition with minor issues")
        elif self.score >= 70:
            summary.append("Plugin is acceptable but needs some improvements")
        elif self.score >= 60:
            summary.append("Plugin needs significant improvements")
        else:
            summary.append("Plugin has critical issues that must be addressed")

        summary.append(f"Quality Score: {self.score}/100 ({len(self.issues)} issues, {len(self.warnings)} warnings)")

        if self.issues:
            summary.append(f"\nCritical Issues ({len(self.issues)}):")
            for issue in self.issues[:5]:  # Show first 5
                summary.append(f"  • {issue}")
            if len(self.issues) > 5:
                summary.append(f"  ... and {len(self.issues) - 5} more issues")

        if self.warnings:
            summary.append(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings[:3]:  # Show first 3
                summary.append(f"  • {warning}")
            if len(self.warnings) > 3:
                summary.append(f"  ... and {len(self.warnings) - 3} more warnings")

        if self.fixes:
            summary.append(f"\nValidations Passed ({len(self.fixes)}):")
            for fix in self.fixes[:5]:  # Show first 5
                summary.append(f"  • {fix[1]}")
            if len(self.fixes) > 5:
                summary.append(f"  ... and {len(self.fixes) - 5} more validations")

        return "\n".join(summary)

    def save_report(self, results: Dict[str, Any], output_file: str = None):
        """Save validation report to file."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_file = f"plugin-validation-report-{timestamp}.json"

        output_path = self.plugin_dir / output_file

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            print(f"\nDetailed report saved to: {output_path}")
            return output_path

        except Exception as e:
            print(f"\nError saving report: {e}")
            return None


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(description='Validate Autonomous Agent Plugin')
    parser.add_argument('--dir', default='.', help='Plugin directory path (default: current directory)')
    parser.add_argument('--output', help='Output file for detailed report (default: auto-generated)')
    parser.add_argument('--quiet', action='store_true', help='Only show summary')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')

    args = parser.parse_args()

    try:
        validator = PluginValidator(args.dir)
        results = validator.validate_all()

        if args.format == 'json':
            print(json.dumps(results, indent=2))
        else:
            print("\n" + "="*60)
            print("PLUGIN VALIDATION RESULTS")
            print("="*60)
            print(results['summary'])
            print("="*60)

        # Save detailed report
        report_path = validator.save_report(results, args.output)

        # Return appropriate exit code
        if results['overall_score'] >= 70:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Issues found

    except Exception as e:
        print(f"Validation failed: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()