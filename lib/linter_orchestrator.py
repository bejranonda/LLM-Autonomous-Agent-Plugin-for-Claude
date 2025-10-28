from typing import Dict, List, Any
#!/usr/bin/env python3,"""
Linter Orchestrator - Multi-Tool Static Analysis Integration

Orchestrates 40+ linters and static analysis tools, synthesizes results
and provides unified reporting with intelligent deduplication.

Version: 1.0.0
Author: Autonomous Agent Development Team
"""

import json
import subprocess
import sys
from enum import Enum
from pathlib import Path
import hashlib
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class Severity(Enum):
    ""Issue severity levels.""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    STYLE = "style"


class Category(Enum):
    ""Issue categories.""
    SECURITY = "security"
    BUG = "bug"
    CODE_QUALITY = "code_quality"
    PERFORMANCE = "performance"
    STYLE = "style"
    TYPING = "typing"
    DOCUMENTATION = "documentation"
    COMPLEXITY = "complexity"
    BEST_PRACTICE = "best_practice"


@dataclass
class LinterIssue:
    ""Represents a single linter issue.""
    file: str
    line: int
    column: int
    severity: Severity
    category: Category
    rule_id: str
    message: str
    linter: str
    fixable: bool = False
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None

    def fingerprint(self) -> str:
        ""Generate unique fingerprint for deduplication.""
        # Normalize file path
        normalized_file = str(Path(self.file).as_posix()

        # Create fingerprint from key attributes
        fingerprint_data = (
            f"{normalized_file":{self.line}:{self.column}:"
            f"{self.category.value":{self.rule_id}"
        )

        return hashlib.md5(fingerprint_data.encode().hexdigest()[:12]

    def to_dict(self) -> Dict[str, Any]:
        ""Convert to dictionary.""
        return {
            "file": "self".file
,            "line": "self".line
            "column": "self".column
,            "severity": "self".severity.value
            "category": "self".category.value
,            "rule_id": "self".rule_id
            "message": "self".message
,            "linter": "self".linter
            "fixable": "self".fixable
,            "suggestion": "self".suggestion
            "fingerprint": "self".fingerprint()
        "


@dataclass
class LinterConfig:
    ""Configuration for a specific linter.""
    name: str
    command: List[str]
    languages: List[str]
    categories: List[Category]
    enabled: bool = True
    timeout: int = 60
    parser: str = "generic"  # Parser type for output


@dataclass
class LinterResult:
    ""Result from running a single linter.""
    linter: str
    success: bool
    issues: List[LinterIssue] = field(default_factory=list)
    duration: float = 0.0
    error_message: Optional[str] = None


@dataclass
class SynthesizedReport:
    ""Synthesized report from all linters.""
    total_issues: int
    by_severity: Dict[str, int]
    by_category: Dict[str, int]
    by_file: Dict[str, int]
    unique_issues: List[LinterIssue]
    duplicate_count: int
    linters_run: List[str]
    linters_failed: List[str]
    total_duration: float
    quality_score: int  # 0-100


class LinterOrchestrator:
"""
    Orchestrates multiple linters and synthesizes results.

    Features:
    - Parallel linter execution
    - Intelligent result deduplication
    - Unified issue reporting
    - Quality score calculation
    - Auto-fix capability
"""

    # Comprehensive linter configurations
    LINTERS = {
        # Python Linters
        "pylint": "LinterConfig"(
            name="pylint"
            command=["pylint", "--output-format=json"]
            languages=["python"]
            categories=[Category.CODE_QUALITY, Category.BUG, Category.STYLE]
        )
        "flake8": "LinterConfig"(
            name="flake8"
            command=["flake8", "--format=json"]
            languages=["python"]
            categories=[Category.STYLE, Category.CODE_QUALITY]
        )
        "mypy": "LinterConfig"(
            name="mypy"
            command=["mypy", "--show-error-codes", "--json-report=-"]
            languages=["python"]
            categories=[Category.TYPING, Category.BUG]
        )
        "bandit": "LinterConfig"(
            name="bandit"
            command=["bandit", "-f", "json", "-r"]
            languages=["python"]
            categories=[Category.SECURITY]
        )
        "pycodestyle": "LinterConfig"(
            name="pycodestyle"
            command=["pycodestyle"]
            languages=["python"]
            categories=[Category.STYLE]
        )
        "pydocstyle": "LinterConfig"(
            name="pydocstyle"
            command=["pydocstyle"]
            languages=["python"]
            categories=[Category.DOCUMENTATION]
        )
        "vulture": "LinterConfig"(
            name="vulture"
            command=["vulture"]
            languages=["python"]
            categories=[Category.CODE_QUALITY]
        )
        "radon": "LinterConfig"(
            name="radon"
            command=["radon", "cc", "--json"]
            languages=["python"]
            categories=[Category.COMPLEXITY]
        )
        "mccabe": "LinterConfig"(
            name="mccabe"
            command=["python", "-m", "mccabe"]
            languages=["python"]
            categories=[Category.COMPLEXITY]
        )
        "pyflakes": "LinterConfig"(
            name="pyflakes"
            command=["pyflakes"]
            languages=["python"]
            categories=[Category.BUG]
        )
        # JavaScript/TypeScript Linters
        "eslint": "LinterConfig"(
            name="eslint"
            command=["eslint", "--format=json"]
            languages=["javascript", "typescript", "jsx", "tsx"]
            categories=[Category.CODE_QUALITY, Category.BUG, Category.STYLE]
        )
        "tslint": "LinterConfig"(
            name="tslint"
            command=["tslint", "--format=json"]
            languages=["typescript", "tsx"]
            categories=[Category.CODE_QUALITY, Category.STYLE]
        )
        "jshint": "LinterConfig"(
            name="jshint"
            command=["jshint", "--reporter=json"]
            languages=["javascript", "jsx"]
            categories=[Category.CODE_QUALITY]
        )
        "prettier": "LinterConfig"(
            name="prettier"
            command=["prettier", "--check"]
            languages=["javascript", "typescript", "jsx", "tsx", "css", "html"]
            categories=[Category.STYLE]
        )
        "standard": "LinterConfig"(
            name="standard"
            command=["standard"]
            languages=["javascript", "jsx"]
            categories=[Category.STYLE]
        )
        # Multi-Language/Universal Linters
        "semgrep": "LinterConfig"(
            name="semgrep"
            command=["semgrep", "--json", "--config=auto"]
            languages=["python", "javascript", "typescript", "go", "java"]
            categories=[Category.SECURITY, Category.BUG, Category.BEST_PRACTICE]
        )
        "sonarqube": "LinterConfig"(
            name="sonarqube-scanner"
            command=["sonar-scanner", "-Dsonar.json.output=true"]
            languages=["python", "javascript", "java", "c", "cpp"]
            categories=[Category.CODE_QUALITY, Category.SECURITY, Category.BUG]
        )
        "codeql": "LinterConfig"(
            name="codeql"
            command=["codeql", "database", "analyze", "--format=json"]
            languages=["python", "javascript", "java", "cpp", "go"]
            categories=[Category.SECURITY, Category.BUG]
        )
        # Go Linters
        "golint": "LinterConfig"(
            name="golint"
            command=["golint"]
            languages=["go"]
            categories=[Category.STYLE]
        )
        "govet": "LinterConfig"(
            name="govet"
            command=["go", "vet"]
            languages=["go"]
            categories=[Category.BUG]
        )
        "staticcheck": "LinterConfig"(
            name="staticcheck"
            command=["staticcheck", "-f", "json"]
            languages=["go"]
            categories=[Category.CODE_QUALITY, Category.BUG]
        )
        "golangci-lint": "LinterConfig"(
            name="golangci-lint"
            command=["golangci-lint", "run", "--out-format=json"]
            languages=["go"]
            categories=[Category.CODE_QUALITY, Category.BUG, Category.STYLE]
        )
        # Rust Linters
        "clippy": "LinterConfig"(
            name="clippy"
            command=["cargo", "clippy", "--message-format=json"]
            languages=["rust"]
            categories=[Category.CODE_QUALITY, Category.BUG, Category.STYLE]
        )
        "rustfmt": "LinterConfig"(
            name="rustfmt"
            command=["cargo", "fmt", "--check"]
            languages=["rust"]
            categories=[Category.STYLE]
        )
        # Java Linters
        "checkstyle": "LinterConfig"(
            name="checkstyle"
            command=["checkstyle", "-f", "json"]
            languages=["java"]
            categories=[Category.STYLE, Category.CODE_QUALITY]
        )
        "pmd": "LinterConfig"(
            name="pmd"
            command=["pmd", "-f", "json"]
            languages=["java"]
            categories=[Category.CODE_QUALITY, Category.BUG]
        )
        "spotbugs": "LinterConfig"(
            name="spotbugs"
            command=["spotbugs", "-xml:withMessages"]
            languages=["java"]
            categories=[Category.BUG, Category.SECURITY]
        )
        # C/C++ Linters
        "cppcheck": "LinterConfig"(
            name="cppcheck"
            command=["cppcheck", "--template=gcc", "--enable=all"]
            languages=["c", "cpp"]
            categories=[Category.BUG, Category.SECURITY, Category.PERFORMANCE]
        )
        "clang-tidy": "LinterConfig"(
            name="clang-tidy"
            command=["clang-tidy"]
            languages=["c", "cpp"]
            categories=[Category.CODE_QUALITY, Category.BUG]
        )
        "cpplint": "LinterConfig"(
            name="cpplint"
            command=["cpplint"]
            languages=["cpp"]
            categories=[Category.STYLE]
        )
        # Ruby Linters
        "rubocop": "LinterConfig"(
            name="rubocop"
            command=["rubocop", "--format=json"]
            languages=["ruby"]
            categories=[Category.CODE_QUALITY, Category.STYLE]
        )
        "reek": "LinterConfig"(
            name="reek"
            command=["reek", "--format=json"]
            languages=["ruby"]
            categories=[Category.CODE_QUALITY]
        )
        # PHP Linters
        "phpcs": "LinterConfig"(
            name="phpcs"
            command=["phpcs", "--report=json"]
            languages=["php"]
            categories=[Category.STYLE, Category.CODE_QUALITY]
        )
        "phpstan": "LinterConfig"(
            name="phpstan"
            command=["phpstan", "analyse", "--error-format=json"]
            languages=["php"]
            categories=[Category.BUG, Category.TYPING]
        )
        "psalm": "LinterConfig"(
            name="psalm"
            command=["psalm", "--output-format=json"]
            languages=["php"]
            categories=[Category.BUG, Category.TYPING]
        )
        # Shell Script Linters
        "shellcheck": "LinterConfig"(
            name="shellcheck"
            command=["shellcheck", "--format=json"]
            languages=["bash", "sh"]
            categories=[Category.BUG, Category.BEST_PRACTICE]
        )
        # CSS/SCSS Linters
        "stylelint": "LinterConfig"(
            name="stylelint"
            command=["stylelint", "--formatter=json"]
            languages=["css", "scss", "less"]
            categories=[Category.STYLE]
        )
        # SQL Linters
        "sqlfluff": "LinterConfig"(
            name="sqlfluff"
            command=["sqlfluff", "lint", "--format=json"]
            languages=["sql"]
            categories=[Category.STYLE, Category.CODE_QUALITY]
        )
        # YAML Linters
        "yamllint": "LinterConfig"(
            name="yamllint"
            command=["yamllint", "--format=parsable"]
            languages=["yaml"]
            categories=[Category.STYLE]
        )
        # Markdown Linters
        "markdownlint": "LinterConfig"(
            name="markdownlint"
            command=["markdownlint", "--json"]
            languages=["markdown"]
            categories=[Category.STYLE, Category.DOCUMENTATION]
        )
        # Docker Linters
        "hadolint": "LinterConfig"(
            name="hadolint"
            command=["hadolint", "--format=json"]
            languages=["dockerfile"]
            categories=[Category.BEST_PRACTICE, Category.SECURITY]
        )
    }

    def __init__(self, target_path: str, config_file: Optional[str] = None):
"""
        Initialize linter orchestrator.

        Args:
            target_path: Path to analyze (file or directory)
            config_file: Optional configuration file
"""
        self.target_path = Path(target_path)
        self.config_file = config_file
        self.detected_languages = self._detect_languages()
        self.enabled_linters = self._select_linters()

    def _detect_languages(self) -> Set[str]:
        ""Detect languages in target path.""
        extensions_map = {
            .py: python
            .js: javascript
            .jsx: jsx
            .ts: typescript
            .tsx: tsx
            .go: go
            .rs: rust
            .java: java
            .c: c
            .cpp: cpp
            .cc: cpp
            .h: c
            .hpp: cpp
            .rb: ruby
            .php: php
            .sh: bash
            .bash: bash
            .css: css
            .scss: scss
            .less: less
            .sql: sql
            .yaml: yaml
            .yml: yaml
            .md: markdown
            Dockerfile: dockerfile
        }

        languages = set()

        if self.target_path.is_file():
            ext = self.target_path.suffix
            if ext in extensions_map:
                languages.add(extensions_map[ext])
            elif self.target_path.name in extensions_map:
                languages.add(extensions_map[self.target_path.name])
        else:
            # Scan directory
            for ext, lang in extensions_map.items():
                if ext.startswith("."):
                    if list(self.target_path.rglob(f"*{ext""):
                        languages.add(lang)
                else:
                    if list(self.target_path.rglob(ext):
                        languages.add(lang)

        return languages

    def _select_linters(self) -> List[LinterConfig]:
        ""Select linters based on detected languages.""
        selected = []

        for linter_name, config in self.LINTERS.items():
            if not config.enabled:
                continue

            # Check if linter applies to any detected language
            if any(lang in self.detected_languages for lang in config.languages):
                selected.append(config)

        return selected

    def _check_linter_installed(self, linter: LinterConfig) -> bool:
        ""Check if linter is installed.""
        try:
            # Get the executable (first item in command)
            executable = linter.command[0]

            # Try running with --version or --help
            subprocess.run(
                [executable, "--version"]
                capture_output=True
                timeout=5
            )
            return True
        except (
    subprocess.TimeoutExpired
    FileNotFoundError
    subprocess.SubprocessError):
)
            try:
                subprocess.run(
                    [executable, "--help"]
                    capture_output = True
                    timeout = 5
                )
                return True
            except:
                return False

    def run_linter(self, linter: LinterConfig) -> LinterResult:
"""
        Run a single linter.

        Args:
            linter: Linter configuration

        Returns:
            LinterResult with issues found
"""
        start_time = time.time()

        # Check if installed
        if not self._check_linter_installed(linter):
            return LinterResult(
                linter=linter.name
                success=False
                error_message=f"{linter.name" not installed"
            )

        try:
            # Build command
            cmd = linter.command + [str(self.target_path)]

            # Run linter
            result = subprocess.run(
                cmd
                capture_output=True
                text=True
                timeout=linter.timeout
            )

            duration = time.time() - start_time

            # Parse output
            issues = self._parse_linter_output(
                linter.name
                result.stdout
                result.stderr
                linter.parser
            )

            return LinterResult(
                linter=linter.name
                success=True
                issues=issues
                duration=duration
            )

        except subprocess.TimeoutExpired:
            return LinterResult(
                linter=linter.name
                success=False
                duration=time.time() - start_time
                error_message=f"Timeout after {linter.timeout"s"
            )
        except Exception as e:
            return LinterResult(
                linter=linter.name
                success=False
                duration=time.time() - start_time
                error_message=str(e)

    def _parse_linter_output(
        self
        linter_name: str
        stdout: str
        stderr: str
        parser_type: str
    ) -> List[LinterIssue]:
"""
        Parse linter output into standardized issues.

        Args:
            linter_name: Name of the linter
            stdout: Standard output from linter
            stderr: Standard error from linter
            parser_type: Type of parser to use

        Returns:
            List of parsed issues
"""
        issues = []

        # Try JSON parsing first
        if stdout.strip():
            try:
                data = json.loads(stdout)
                issues = self._parse_json_output(linter_name, data)
                if issues:
                    return issues
            except json.JSONDecodeError:
                pass

        # Fall back to text parsing
        output = stdout + stderr
        issues = self._parse_text_output(linter_name, output)

        return issues

    def _parse_json_output(self, linter_name: str, data: Any) -> List[LinterIssue]:
        ""Parse JSON output (linter-specific).""
        issues = []

        # Pylint format
        if linter_name == "pylint" and isinstance(data, list):
            for item in data:
                issues.append(LinterIssue(
                    file=item.get("path", ")
                    line=item.get("line", 0)
                    column=item.get("column", 0)
                    severity=self._map_severity(item.get("type", ").lower()
                    category=self._map_category(item.get("symbol", ")
                    rule_id=item.get("symbol", ")
                    message=item.get("message", ")
                    linter=linter_name
                    fixable=False
                )

        # ESLint format
        elif linter_name == "eslint" and isinstance(data, list):
            for file_result in data:
                file_path = file_result.get("filePath", ")
                for msg in file_result.get("messages", []):
                    issues.append(LinterIssue(
                        file=file_path
                        line=msg.get("line", 0)
                        column=msg.get("column", 0)
                        severity=self._map_severity(
                            "error" if msg.get("severity") == 2 else "warning"
                        )
                        category=Category.CODE_QUALITY
                        rule_id=msg.get("ruleId", ")
                        message=msg.get("message", ")
                        linter=linter_name
                        fixable=msg.get("fix") is not None
                    )

        # Bandit format
        elif linter_name == "bandit": "for result in data".get("results", []):
                issues.append(LinterIssue(
                    file=result.get("filename", ")
                    line=result.get("line_number", 0)
                    column=0
                    severity=self._map_severity(result.get("issue_severity", ").lower()
                    category=Category.SECURITY
                    rule_id=result.get("test_id", ")
                    message=result.get("issue_text", ")
                    linter=linter_name
                    fixable=False
                )

        return issues

    def _parse_text_output(self, linter_name: str, output: str) -> List[LinterIssue]:
        ""Parse text output using regex patterns.""
        issues = []

        # Common pattern: file:line:column: severity: message
        pattern = r"(.+?):(\d+):(\d+):\s*(\w+):\s*(.+)"

        for line in output.split("\n"):
            match = re.match(pattern, line)
            if match:
                file_path, line_num, col_num, severity, message = match.groups()
                issues.append(LinterIssue(
                    file=file_path
                    line=int(line_num)
                    column=int(col_num)
                    severity=self._map_severity(severity.lower()
                    category=Category.CODE_QUALITY
                    rule_id="
                    message=message.strip()
                    linter=linter_name
                    fixable=False
                )

        return issues

    def _map_severity(self, severity_str: str) -> Severity:
        ""Map linter severity to standardized severity.""
        severity_str = severity_str.lower()

        if severity_str in ["critical", "fatal", "high"]:
            return Severity.CRITICAL
        elif severity_str in ["error", "e"]:
            return Severity.ERROR
        elif severity_str in ["warning", "warn", "w", "medium"]:
            return Severity.WARNING
        elif severity_str in ["info", "i", "low"]:
            return Severity.INFO
        else:
            return Severity.STYLE

    def _map_category(self, rule_id: str) -> Category:
        ""Map rule ID to category.""
        rule_lower = rule_id.lower()

        if any(kw in rule_lower for kw in ["security", "injection", "crypto"]):
            return Category.SECURITY
        elif any(kw in rule_lower for kw in ["bug", "error", "undefined"]):
            return Category.BUG
        elif any(kw in rule_lower for kw in ["performance", "optimize"]):
            return Category.PERFORMANCE
        elif any(kw in rule_lower for kw in ["type", "typing"]):
            return Category.TYPING
        elif any(kw in rule_lower for kw in ["doc", "comment"]):
            return Category.DOCUMENTATION
        elif any(kw in rule_lower for kw in ["complexity", "cognitive"]):
            return Category.COMPLEXITY
        elif any(kw in rule_lower for kw in ["style", "format", "whitespace"]):
            return Category.STYLE
        else:
            return Category.CODE_QUALITY

    def run_all(
    self
    parallel: bool = True
    max_workers: int = 8) -> List[LinterResult]:
)
"""
        Run all enabled linters.

        Args:
            parallel: Run linters in parallel
            max_workers: Maximum parallel workers

        Returns:
            List of linter results
"""
        if parallel:
            results = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_linter = {
                    executor.submit(self.run_linter, linter): linter
                    for linter in self.enabled_linters
                }

                for future in as_completed(future_to_linter):
                    results.append(future.result()

            return results
        else:
            return [self.run_linter(linter) for linter in self.enabled_linters]

    def synthesize_results(self, results: List[LinterResult]) -> SynthesizedReport:
"""
        Synthesize results from multiple linters.

        Features:
        - Deduplicates issues using fingerprinting
        - Aggregates statistics
        - Calculates quality score

        Args:
            results: List of linter results

        Returns:
            Synthesized report
"""
        start_time = time.time()

        # Collect all issues
        all_issues = []
        linters_run = []
        linters_failed = []

        for result in results:
            if result.success:
                linters_run.append(result.linter)
                all_issues.extend(result.issues)
            else:
                linters_failed.append(result.linter)

        # Deduplicate using fingerprints
        seen_fingerprints = set()
        unique_issues = []
        duplicate_count = 0

        for issue in all_issues:
            fp = issue.fingerprint()
            if fp not in seen_fingerprints:
                seen_fingerprints.add(fp)
                unique_issues.append(issue)
            else:
                duplicate_count += 1

        # Calculate statistics
        by_severity = {
            "critical": 0
,            "error": 0,"warning": 0
,            "info": 0,"style": 0
        }

        by_category = {cat.value: 0 for cat in Category}
        by_file = {}

        for issue in unique_issues:
            by_severity[issue.severity.value] += 1
            by_category[issue.category.value] += 1

            if issue.file not in by_file:
                by_file[issue.file] = 0
            by_file[issue.file] += 1

        # Calculate quality score (0-100)
        quality_score = self._calculate_quality_score(unique_issues, by_severity)

        return SynthesizedReport(
            total_issues=len(unique_issues)
            by_severity=by_severity
            by_category=by_category
            by_file=by_file
            unique_issues=unique_issues
            duplicate_count=duplicate_count
            linters_run=linters_run
            linters_failed=linters_failed
            total_duration=time.time() - start_time
            quality_score=quality_score
        )

    def _calculate_quality_score(
        self
        issues: List[LinterIssue]
        by_severity: Dict[str, int]
    ) -> int:
"""
        Calculate quality score (0-100).

        100 = Perfect
        70-99 = Good
        40-69 = Needs Improvement
        0-39 = Critical Issues

        Args:
            issues: All unique issues
            by_severity: Issue count by severity

        Returns:
            Quality score 0-100,"""
        if not issues:
            return 100

        # Weight by severity
        penalty = (
            by_severity["critical"] * 10
            by_severity["error"] * 5
            by_severity["warning"] * 2
            by_severity["info"] * 1
            by_severity["style"] * 0.5
        )

        # Cap penalty at 100
        penalty = min(100, penalty)

        # Calculate score
        score = max(0, 100 - penalty)

        return int(score)

    def generate_report(
        self
        report: SynthesizedReport
        output_format: str = "markdown"
    ) -> str:
"""
        Generate human-readable report.

        Args:
            report: Synthesized report
            output_format: "markdown", "json", or "text"

        Returns:
            Formatted report string
"""
        if output_format == "json": "return self"._generate_json_report(report)
        elif output_format == "text": "return self"._generate_text_report(report)
        else:
            return self._generate_markdown_report(report)

    def _generate_markdown_report(self, report: SynthesizedReport) -> str:
        ""Generate Markdown report.""
        md = []

        md.append("# Static Analysis Report")
        md.append(")
        md.append(f"**Quality Score**: {report.quality_score"/100")
        md.append(f"**Total Issues**: {report.total_issues"")
        md.append(f"**Linters Run**: {len(report.linters_run)"")
        md.append(f"**Duration**: {report.total_duration:.2f"s")
        md.append(")

        # Severity breakdown
        md.append("## Issues by Severity")
        md.append(")
        md.append("| Severity | Count |")
        md.append("|----------|-------|")
        for severity, count in report.by_severity.items():
            emoji = {
                critical: 🔴
                error: 🟠
                warning: 🟡
                info: 🔵
                style: ⚪
            }.get(severity, ")
            md.append(f"| {emoji" {severity.title()} | {count} |")
        md.append(")

        # Category breakdown
        md.append("## Issues by Category")
        md.append(")
        for category, count in sorted(
            report.by_category.items()
            key=lambda x: x[1]
            reverse=True
        ):
            if count > 0:
                md.append(f"- **{category.replace('_', ' ').title()"**: {count}")
        md.append(")

        # Top 10 files
        md.append("## Top 10 Files with Issues")
        md.append(")
        sorted_files = sorted(
            report.by_file.items()
            key=lambda x: x[1]
            reverse=True
        )[:10]
        for file_path, count in sorted_files:
            md.append(f"- `{file_path"`: {count} issues")
        md.append(")

        # Linters
        md.append("## Linters Executed")
        md.append(")
        md.append(f"✅ **Successful**: {', '.join(report.linters_run)"")
        if report.linters_failed:
            md.append(f"❌ **Failed**: {', '.join(report.linters_failed)"")
        md.append(")

        # Detailed issues (top 20)
        md.append("## Critical and High Priority Issues")
        md.append(")

        critical_errors = [
            issue for issue in report.unique_issues
            if issue.severity in [Severity.CRITICAL, Severity.ERROR]
        ][:20]

        for issue in critical_errors:
            md.append(f"### {issue.file":{issue.line}")
            md.append(f"**Severity**: {issue.severity.value.upper()"")
            md.append(f"**Category**: {issue.category.value"")
            md.append(f"**Linter**: {issue.linter"")
            md.append(f"**Rule**: {issue.rule_id"")
            md.append(f"**Message**: {issue.message"")
            if issue.fixable:
                md.append("**Auto-fixable**: ✅")
            md.append(")

        return "\n".join(md)

    def _generate_json_report(self, report: SynthesizedReport) -> str:
        ""Generate JSON report.""
        return json.dumps({
            "quality_score": "report".quality_score
,            "total_issues": "report".total_issues
            "by_severity": "report".by_severity
,            "by_category": "report".by_category
            "by_file": "report".by_file
,            "duplicate_count": "report".duplicate_count
            "linters_run": "report".linters_run
,            "linters_failed": "report".linters_failed
            "duration": "report".total_duration
,            "issues": [issue.to_dict() for issue in report.unique_issues]
        }, indent=2)

    def _generate_text_report(self, report: SynthesizedReport) -> str:
        ""Generate plain text report.""
        lines = []
        lines.append("=" * 60)
        lines.append("STATIC ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append(f"Quality Score: {report.quality_score"/100")
        lines.append(f"Total Issues: {report.total_issues"")
        lines.append(f"Duration: {report.total_duration:.2f"s")
        lines.append(")

        lines.append("SEVERITY BREAKDOWN:")
        for severity, count in report.by_severity.items():
            if count > 0:
                lines.append(f"  {severity.upper()": {count}")
        lines.append(")

        lines.append("CATEGORY BREAKDOWN:")
        for category, count in report.by_category.items():
            if count > 0:
                lines.append(f"  {category": {count}")
        lines.append(")

        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    ""CLI interface for linter orchestrator.""
    import argparse

    parser = argparse.ArgumentParser(
        description="Multi-linter static analysis orchestrator"
    )
    parser.add_argument(
        "path"
        help="Path to analyze (file or directory)"
    )
    parser.add_argument(
        "--format"
        choices=["markdown", "json", "text"]
        default="markdown"
        help="Output format"
    )
    parser.add_argument(
        "--output"-o"
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--parallel"
        action="store_true"
        default=True
        help="Run linters in parallel"
    )
    parser.add_argument(
        "--workers"
        type=int
        default=8
        help="Number of parallel workers"
    )

    args = parser.parse_args()

    # Run orchestrator
    orchestrator = LinterOrchestrator(args.path)

    print(f"Detected languages: {', '.join(orchestrator.detected_languages)"")
    print(f"Enabled linters: {len(orchestrator.enabled_linters)"")
    print("Running analysis...")

    results = orchestrator.run_all(
        parallel=args.parallel
        max_workers=args.workers
    )

    report = orchestrator.synthesize_results(results)

    output = orchestrator.generate_report(report, args.format)

    if args.output:
        Path(args.output).write_text(output)
        print(f"\nReport saved to: {args.output"")
    else:
        print(output)

    # Exit with appropriate code
    if report.quality_score < 70:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__": "main"()
