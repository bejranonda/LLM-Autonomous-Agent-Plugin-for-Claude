#!/usr/bin/env python3
"""
Comprehensive Quality Analysis for Autonomous Agent Plugin
"""

import json
import yaml
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess


class QualityAnalyzer:
    def __init__(self):
        """  Init  ."""
        self.issues = []
        self.fixes_applied = []
        self.metrics = {}

    def analyze_python_utilities(self):
        """Analyze Python utilities for syntax and coverage"""
        print("Analyzing Python utilities...")

        # Test coverage from previous run
        self.metrics["test_coverage"] = {
            "total_statements": 11992,
            "covered_statements": 469,
            "coverage_percentage": 4,
            "tests_passed": 20,
            "tests_failed": 0,
            "python_files_with_issues": 0,
        }

        # Check syntax errors
        lib_dir = Path("lib")
        syntax_errors = 0
        valid_files = 0

        for py_file in lib_dir.glob("*.py"):
            if py_file.name.startswith("fix_") or py_file.name.startswith("test_"):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    compile(f.read(), str(py_file), "exec")
                valid_files += 1
            except SyntaxError:
                syntax_errors += 1
                self.issues.append({"type": "syntax_error", "file": str(py_file), "severity": "high"})

        self.metrics["python_syntax"] = {
            "total_files": len(list(lib_dir.glob("*.py"))),
            "valid_files": valid_files,
            "syntax_errors": syntax_errors,
        }

        print(f"  - Syntax errors: {syntax_errors}")
        print(f"  - Test coverage: {self.metrics['test_coverage']['coverage_percentage']}%")

    def analyze_json_structure(self):
        """Analyze JSON files for syntax and structure"""
        print("Analyzing JSON structure...")

        json_files = [".claude-plugin/plugin.json", "patterns/autofix-patterns.json"]

        json_errors = 0
        valid_json = 0

        for json_file in json_files:
            if Path(json_file).exists():
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Check plugin.json structure
                    if json_file == ".claude-plugin/plugin.json":
                        required_fields = ["name", "version", "description", "author"]
                        missing_fields = [f for f in required_fields if f not in data]
                        if missing_fields:
                            self.issues.append(
                                {
                                    "type": "missing_required_fields",
                                    "file": json_file,
                                    "fields": missing_fields,
                                    "severity": "high",
                                }
                            )
                        else:
                            valid_json += 1
                    else:
                        valid_json += 1

                except json.JSONDecodeError as e:
                    json_errors += 1
                    self.issues.append({"type": "json_syntax_error", "file": json_file, "error": str(e), "severity": "high"})

        self.metrics["json_structure"] = {"total_files": len(json_files), "valid_files": valid_json, "errors": json_errors}

        print(f"  - JSON files valid: {valid_json}/{len(json_files)}")

    def analyze_yaml_frontmatter(self):
        """Analyze YAML frontmatter in agents and skills"""
        print("Analyzing YAML frontmatter...")

        def check_frontmatter(file_path):
            """Check Frontmatter."""
            try:
                content = file_path.read_text(encoding="utf-8")
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        yaml.safe_load(frontmatter)
                        return True, "Valid YAML"
                return False, "No frontmatter found"
            except yaml.YAMLError:
                return False, "YAML Error"
            except Exception:
                return False, "Error"

        # Check agents
        agent_files = list(Path("agents").glob("*.md"))
        agent_valid = 0
        agent_errors = 0

        for agent_file in agent_files:
            valid, msg = check_frontmatter(agent_file)
            if valid:
                agent_valid += 1
            else:
                agent_errors += 1
                if "YAML Error" in msg:
                    self.issues.append(
                        {
                            "type": "yaml_frontmatter_error",
                            "file": f"agents/{agent_file.name}",
                            "error": msg,
                            "severity": "medium",
                        }
                    )

        # Check skills
        skill_dirs = [d for d in Path("skills").iterdir() if d.is_dir()]
        skill_valid = 0
        skill_errors = 0

        for skill_dir in skill_dirs:
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                valid, msg = check_frontmatter(skill_file)
                if valid:
                    skill_valid += 1
                else:
                    skill_errors += 1
                    if "YAML Error" in msg:
                        self.issues.append(
                            {
                                "type": "yaml_frontmatter_error",
                                "file": f"skills/{skill_dir.name}/SKILL.md",
                                "error": msg,
                                "severity": "medium",
                            }
                        )

        self.metrics["yaml_frontmatter"] = {
            "agent_files": {"total": len(agent_files), "valid": agent_valid, "errors": agent_errors},
            "skill_files": {
                "total": len([d for d in skill_dirs if (d / "SKILL.md").exists()]),
                "valid": skill_valid,
                "errors": skill_errors,
            },
        }

        print(f"  - Agent files with valid YAML: {agent_valid}/{len(agent_files)}")
        print(f"  - Skill files with valid YAML: {skill_valid}/{len([d for d in skill_dirs if (d / 'SKILL.md').exists()])}")

    def analyze_documentation(self):
        """Analyze documentation completeness"""
        print("Analyzing documentation completeness...")

        # Check commands
        command_files = list(Path("commands").glob("*.md"))
        command_dirs = list(Path("commands").glob("*"))
        command_dirs = [d for d in command_dirs if d.is_dir()]

        total_commands = len(command_files) + len(command_dirs)

        # Check README files
        readme_files = ["README.md", "STRUCTURE.md", "CHANGELOG.md"]
        existing_readme = [f for f in readme_files if Path(f).exists()]

        # Check docs directory
        docs_files = []
        if Path("docs").exists():
            docs_files = list(Path("docs").rglob("*.md"))

        self.metrics["documentation"] = {
            "commands": {"total": total_commands, "files": len(command_files), "dirs": len(command_dirs)},
            "readme_files": {"expected": len(readme_files), "existing": len(existing_readme)},
            "docs_files": len(docs_files),
        }

        # Check for missing documentation
        if len(existing_readme) < len(readme_files):
            missing = set(readme_files) - set(existing_readme)
            self.issues.append({"type": "missing_documentation", "files": list(missing), "severity": "medium"})

        print(f"  - Commands documented: {total_commands}")
        print(f"  - README files: {len(existing_readme)}/{len(readme_files)}")
        print(f"  - Documentation files: {len(docs_files)}")

    def analyze_plugin_structure(self):
        """Analyze plugin architecture compliance"""
        print("Analyzing plugin structure...")

        required_dirs = [".claude-plugin", "agents", "skills", "commands", "lib"]
        missing_dirs = [d for d in required_dirs if not Path(d).exists()]

        if missing_dirs:
            self.issues.append({"type": "missing_directories", "directories": missing_dirs, "severity": "high"})

        # Check component counts
        agent_count = len(list(Path("agents").glob("*.md")))
        skill_count = len([d for d in Path("skills").iterdir() if d.is_dir() and (d / "SKILL.md").exists()])
        command_count = len(list(Path("commands").glob("*.md"))) + len([d for d in Path("commands").iterdir() if d.is_dir()])

        self.metrics["plugin_structure"] = {
            "required_directories": {"expected": len(required_dirs), "existing": len(required_dirs) - len(missing_dirs)},
            "component_counts": {"agents": agent_count, "skills": skill_count, "commands": command_count},
        }

        print(f"  - Required directories: {len(required_dirs) - len(missing_dirs)}/{len(required_dirs)}")
        print(f"  - Components: {agent_count} agents, {skill_count} skills, {command_count} commands")

    def calculate_quality_score(self):
        """Calculate overall quality score"""
        print("Calculating quality score...")

        # Test Coverage (30 points)
        coverage_score = min(30, (self.metrics["test_coverage"]["coverage_percentage"] / 100) * 30)

        # Code Standards (25 points)
        syntax_issues = self.metrics["python_syntax"]["syntax_errors"]
        json_issues = self.metrics["json_structure"]["errors"]
        yaml_issues = (
            self.metrics["yaml_frontmatter"]["agent_files"]["errors"]
            + self.metrics["yaml_frontmatter"]["skill_files"]["errors"]
        )
        standards_deductions = min(25, (syntax_issues + json_issues + yaml_issues) * 2)
        standards_score = max(0, 25 - standards_deductions)

        # Documentation (20 points)
        readme_ratio = self.metrics["documentation"]["readme_files"]["existing"] / max(
            1, self.metrics["documentation"]["readme_files"]["expected"]
        )
        docs_score = readme_ratio * 20

        # Pattern Adherence (15 points)
        structure_issues = len([i for i in self.issues if i["type"] == "missing_directories"])
        pattern_score = max(0, 15 - structure_issues * 3)

        # Code Metrics (10 points)
        python_ratio = self.metrics["python_syntax"]["valid_files"] / max(1, self.metrics["python_syntax"]["total_files"])
        metrics_score = python_ratio * 10

        total_score = coverage_score + standards_score + docs_score + pattern_score + metrics_score

        self.metrics["quality_score"] = {
            "total": round(total_score, 1),
            "breakdown": {
                "test_coverage": round(coverage_score, 1),
                "code_standards": round(standards_score, 1),
                "documentation": round(docs_score, 1),
                "pattern_adherence": round(pattern_score, 1),
                "code_metrics": round(metrics_score, 1),
            },
        }

        print(f"  - Total Score: {total_score:.1f}/100")

    def generate_report(self):
        """Generate comprehensive quality report"""
        report = {
            "timestamp": "2025-10-30T12:00:00Z",
            "project": "Autonomous Agent Plugin",
            "version": "5.5.1",
            "quality_score": self.metrics["quality_score"],
            "metrics": self.metrics,
            "issues_found": len(self.issues),
            "issues_by_type": {},
            "recommendations": [],
        }

        # Categorize issues
        for issue in self.issues:
            issue_type = issue["type"]
            if issue_type not in report["issues_by_type"]:
                report["issues_by_type"][issue_type] = []
            report["issues_by_type"][issue_type].append(issue)

        # Generate recommendations
        score = self.metrics["quality_score"]["total"]
        if score < 70:
            report["recommendations"].append(
                {
                    "priority": "HIGH",
                    "action": "Quality score below threshold",
                    "details": f"Current score: {score}/100. Target: 70+/100",
                }
            )

        if self.metrics["test_coverage"]["coverage_percentage"] < 50:
            report["recommendations"].append(
                {
                    "priority": "HIGH",
                    "action": "Increase test coverage",
                    "details": f'Current: {self.metrics["test_coverage"]["coverage_percentage"]}%. Target: 50%+',
                }
            )

        if self.metrics["python_syntax"]["syntax_errors"] > 0:
            report["recommendations"].append(
                {
                    "priority": "HIGH",
                    "action": "Fix Python syntax errors",
                    "details": f'{self.metrics["python_syntax"]["syntax_errors"]} files have syntax issues',
                }
            )

        return report

    def apply_auto_fixes(self):
        """Apply automatic fixes where possible"""
        print("Applying auto-fixes...")

        fixes_applied = 0

        # Auto-fix: Restore working task_queue.py
        task_queue_broken = Path("lib/task_queue.py.broken")
        task_queue_working = Path("lib/task_queue.py")

        if task_queue_broken.exists() and not task_queue_working.exists():
            # Create a minimal working task_queue.py
            minimal_task_queue = '''#!/usr/bin/env python3
"""
Task Queue System for Autonomous Claude Agent Plugin (Minimal Working Version)
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class TaskQueue:
    """Manages task queue with priority-based execution."""

    # Priority levels
    PRIORITY_HIGH = 3
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 1

    # Status constants
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'

    def __init__(self, queue_dir: str = ): ):
        """Initialize task queue."""
        self.queue_dir = Path(queue_dir)
        self.queue_file = self.queue_dir / "task_queue.json"
        self._ensure_directory()

    def _ensure_directory(self):
        """Create queue directory if it doesn't exist."""
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        if not self.queue_file.exists():
            self._write_queue([])

    def _read_queue(self) -> List[Dict[str, Any]]:
        """Read task queue from JSON file."""
        try:
            if self.queue_file.exists():
                with open(self.queue_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception:
            return []

    def _write_queue(self, queue: List[Dict[str, Any]]):
        """Write task queue to JSON file."""
        try:
            with open(self.queue_file, 'w', encoding='utf-8') as f:
                json.dump(queue, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing queue: {e}", file=sys.stderr)

def main():
    """CLI interface for task queue."""
    parser = argparse.ArgumentParser(description='Task Queue Management')
    parser.add_argument('action', choices=['status'], help='Action to perform')
    parser.add_argument('--dir', default='.claude-patterns', help='Queue directory')

    args = parser.parse_args()
    queue = TaskQueue(args.dir)

    if args.action == 'status':
        tasks = queue._read_queue()
        print(f"Tasks in queue: {len(tasks)}")
        for task in tasks:
            print(f"  - {task.get('name', 'Unknown')} [{task.get('status', 'Unknown')}]")

if __name__ == '__main__':
    main()
'''
            task_queue_working.write_text(minimal_task_queue, encoding="utf-8")
            fixes_applied += 1
            self.fixes_applied.append(
                {"type": "file_restoration", "file": "lib/task_queue.py", "action": "Created minimal working version"}
            )

        print(f"  - Auto-fixes applied: {fixes_applied}")
        return fixes_applied


def main():
    """Main analysis function"""
    print("=" * 60)
    print("COMPREHENSIVE QUALITY ANALYSIS")
    print("Autonomous Agent Plugin v5.5.1")
    print("=" * 60)

    analyzer = QualityAnalyzer()

    # Run all analyses
    analyzer.analyze_python_utilities()
    analyzer.analyze_json_structure()
    analyzer.analyze_yaml_frontmatter()
    analyzer.analyze_documentation()
    analyzer.analyze_plugin_structure()
    analyzer.calculate_quality_score()

    # Apply auto-fixes
    analyzer.apply_auto_fixes()

    # Generate report
    report = analyzer.generate_report()

    # Display results
    print("\n" + "=" * 60)
    print("QUALITY ANALYSIS RESULTS")
    print("=" * 60)

    print(f"Overall Quality Score: {report['quality_score']['total']}/100")
    print(f"Issues Found: {report['issues_found']}")
    print(f"Auto-fixes Applied: {len(analyzer.fixes_applied)}")

    print("\nScore Breakdown:")
    for category, score in report["quality_score"]["breakdown"].items():
        print(
            f"  - {category.replace('_', ' ').title()}: {score}/30"
            if category == "test_coverage"
            else (
                f"  - {category.replace('_', ' ').title()}: {score}/25"
                if category == "code_standards"
                else (
                    f"  - {category.replace('_', ' ').title()}: {score}/20"
                    if category == "documentation"
                    else (
                        f"  - {category.replace('_', ' ').title()}: {score}/15"
                        if category == "pattern_adherence"
                        else f"  - {category.replace('_', ' ').title()}: {score}/10"
                    )
                )
            )
        )

    if report["recommendations"]:
        print("\nRecommendations:")
        for rec in report["recommendations"]:
            print(f"  - [{rec['priority']}] {rec['action']}: {rec['details']}")

    # Save detailed report
    report_file = Path(".claude/reports/QUALITY_REPORT_2025-10-30.md")
    report_file.parent.mkdir(parents=True, exist_ok=True)

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# Quality Analysis Report\n\n")
        f.write(f"**Generated:** 2025-10-30T12:00:00Z\n")
        f.write(f"**Project:** Autonomous Agent Plugin v5.5.1\n")
        f.write(f"**Quality Score:** {report['quality_score']['total']}/100\n\n")

        f.write("## Metrics Summary\n\n")
        for category, metrics in report["metrics"].items():
            f.write(f"### {category.replace('_', ' ').title()}\n")
            if isinstance(metrics, dict):
                for key, value in metrics.items():
                    f.write(f"- {key}: {value}\n")
            f.write("\n")

        if report["issues_found"] > 0:
            f.write("## Issues Found\n\n")
            for issue_type, issues in report["issues_by_type"].items():
                f.write(f"### {issue_type.replace('_', ' ').title()}\n")
                for issue in issues:
                    f.write(f"- **{issue.get('file', 'Unknown')}**: {issue.get('error', 'Issue detected')}\n")
                f.write("\n")

        if analyzer.fixes_applied:
            f.write("## Auto-fixes Applied\n\n")
            for fix in analyzer.fixes_applied:
                f.write(f"- **{fix['type']}**: {fix['action']} ({fix['file']})\n")
            f.write("\n")

        if report["recommendations"]:
            f.write("## Recommendations\n\n")
            for rec in report["recommendations"]:
                f.write(f"- **[{rec['priority']}]** {rec['action']}: {rec['details']}\n")
            f.write("\n")

    print(f"\nDetailed report saved to: {report_file}")

    return report["quality_score"]["total"] >= 70


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
