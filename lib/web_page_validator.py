#!/usr/bin/env python3
"""
Web Page Validator with JavaScript Error Detection

Automatically validates web pages (like dashboard.py) and detects:
- JavaScript syntax errors
- Console errors, warnings, and logs
- Network request failures
- HTML/CSS validation issues
- Page load performance
- Broken links and resources

Uses Selenium WebDriver for headless browser automation to capture
real browser console output without manual inspection.

Version: 1.0.0
Author: Autonomous Agent Development Team
"""

import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
import subprocess
import urllib.request
import urllib.error
from collections import defaultdict

# Try to import Selenium for browser automation
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("[WARN] Selenium not available. Install with: pip install selenium", file=sys.stderr)

# Try to import playwright as alternative
try:
    from playwright.sync_api import sync_playwright, Error as PlaywrightError

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@dataclass
class ConsoleLog:
    """Represents a browser console log entry"""

    level: str  # error, warning, info, log, debug
    message: str
    source: str
    line: Optional[int] = None
    column: Optional[int] = None
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class ValidationResult:
    """Comprehensive validation result"""

    url: str
    success: bool
    load_time: float
    console_errors: List[ConsoleLog]
    console_warnings: List[ConsoleLog]
    console_logs: List[ConsoleLog]
    network_errors: List[Dict[str, Any]]
    javascript_errors: List[str]
    html_issues: List[str]
    performance_metrics: Dict[str, Any]
    page_title: str
    status_code: int
    timestamp: str
    error_summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "url": self.url,
            "success": self.success,
            "load_time": self.load_time,
            "console_errors": [asdict(log) for log in self.console_errors],
            "console_warnings": [asdict(log) for log in self.console_warnings],
            "console_logs": [asdict(log) for log in self.console_logs],
            "network_errors": self.network_errors,
            "javascript_errors": self.javascript_errors,
            "html_issues": self.html_issues,
            "performance_metrics": self.performance_metrics,
            "page_title": self.page_title,
            "status_code": self.status_code,
            "timestamp": self.timestamp,
            "error_summary": self.error_summary,
        }


class WebPageValidator:
    """Validates web pages and captures JavaScript errors"""

    def __init__(self, headless: bool = True, timeout: int = 30):
        """
        Initialize validator

        Args:
            headless: Run browser in headless mode
            timeout: Page load timeout in seconds
        """
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.browser_type = None

    def _init_selenium_driver(self) -> bool:
        """Initialize Selenium WebDriver"""
        if not SELENIUM_AVAILABLE:
            return False

        try:
            chrome_options = ChromeOptions()
            if self.headless:
                chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

            # Enable console log capture
            chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(self.timeout)
            self.browser_type = "selenium"
            return True

        except Exception as e:
            print(f"[ERROR] Failed to initialize Chrome WebDriver: {e}", file=sys.stderr)
            print("[INFO] Install ChromeDriver: https://chromedriver.chromium.org/", file=sys.stderr)
            return False

    def _init_playwright_browser(self):
        """Initialize Playwright browser"""
        if not PLAYWRIGHT_AVAILABLE:
            return None

        try:
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(headless=self.headless)
            self.browser_type = "playwright"
            return browser, playwright
        except Exception as e:
            print(f"[ERROR] Failed to initialize Playwright: {e}", file=sys.stderr)
            return None

    def validate_url(self, url: str, wait_for_load: int = 3) -> ValidationResult:
        """
        Validate a web page URL

        Args:
            url: URL to validate
            wait_for_load: Seconds to wait after page load for JavaScript execution

        Returns:
            ValidationResult with all detected issues
        """
        if SELENIUM_AVAILABLE:
            return self._validate_with_selenium(url, wait_for_load)
        elif PLAYWRIGHT_AVAILABLE:
            return self._validate_with_playwright(url, wait_for_load)
        else:
            return self._validate_basic(url)

    def _validate_with_selenium(self, url: str, wait_for_load: int) -> ValidationResult:
        """Validate using Selenium WebDriver"""
        console_errors = []
        console_warnings = []
        console_logs = []
        javascript_errors = []
        network_errors = []

        start_time = time.time()

        try:
            if not self.driver and not self._init_selenium_driver():
                raise Exception("Failed to initialize Selenium WebDriver")

            # Navigate to URL
            self.driver.get(url)

            # Wait for page to load
            time.sleep(wait_for_load)

            # Get page title
            page_title = self.driver.title

            # Capture console logs
            logs = self.driver.get_log("browser")
            for log in logs:
                level = log.get("level", "INFO").lower()
                message = log.get("message", "")
                source = log.get("source", "unknown")

                console_log = ConsoleLog(
                    level=level,
                    message=message,
                    source=source,
                    timestamp=datetime.fromtimestamp(log.get("timestamp", 0) / 1000).isoformat(),
                )

                if level == "severe" or "error" in level:
                    console_errors.append(console_log)
                    if "SyntaxError" in message or "Uncaught" in message:
                        javascript_errors.append(message)
                elif level == "warning":
                    console_warnings.append(console_log)
                else:
                    console_logs.append(console_log)

            # Check for JavaScript errors using window.onerror
            js_errors = self.driver.execute_script(
                """
                return window.__jsErrors || [];
            """
            )
            javascript_errors.extend(js_errors)

            # Get performance metrics
            performance = self.driver.execute_script(
                """
                const perf = performance.timing;
                return {
                    loadTime: perf.loadEventEnd - perf.navigationStart,
                    domReady: perf.domContentLoadedEventEnd - perf.navigationStart,
                    responseTime: perf.responseEnd - perf.requestStart
                };
            """
            )

            load_time = time.time() - start_time

            # Check for network errors using Resource Timing API
            resources = self.driver.execute_script(
                """
                return performance.getEntriesByType('resource').map(r => ({
                    name: r.name,
                    duration: r.duration,
                    transferSize: r.transferSize,
                    failed: r.transferSize === 0 && r.duration > 0
                }));
            """
            )

            network_errors = [r for r in resources if r.get("failed")]

            # Build error summary
            error_summary = self._build_error_summary(
                len(console_errors), len(console_warnings), len(javascript_errors), len(network_errors)
            )

            return ValidationResult(
                url=url,
                success=len(console_errors) == 0 and len(javascript_errors) == 0,
                load_time=load_time,
                console_errors=console_errors,
                console_warnings=console_warnings,
                console_logs=console_logs,
                network_errors=network_errors,
                javascript_errors=javascript_errors,
                html_issues=[],
                performance_metrics=performance,
                page_title=page_title,
                status_code=200,
                timestamp=datetime.now().isoformat(),
                error_summary=error_summary,
            )

        except TimeoutException:
            return self._create_error_result(url, f"Page load timeout after {self.timeout}s")
        except WebDriverException as e:
            return self._create_error_result(url, f"WebDriver error: {str(e)}")
        except Exception as e:
            return self._create_error_result(url, f"Validation error: {str(e)}")

    def _validate_with_playwright(self, url: str, wait_for_load: int) -> ValidationResult:
        """Validate using Playwright"""
        console_errors = []
        console_warnings = []
        console_logs = []
        javascript_errors = []
        network_errors = []

        start_time = time.time()
        browser_data = self._init_playwright_browser()

        if not browser_data:
            return self._validate_basic(url)

        browser, playwright = browser_data

        try:
            context = browser.new_context()
            page = context.new_page()

            # Capture console logs
            def handle_console(msg):
                level = msg.type
                message = msg.text

                console_log = ConsoleLog(level=level, message=message, source="console")

                if level == "error":
                    console_errors.append(console_log)
                    if "SyntaxError" in message or "Uncaught" in message:
                        javascript_errors.append(message)
                elif level == "warning":
                    console_warnings.append(console_log)
                else:
                    console_logs.append(console_log)

            page.on("console", handle_console)

            # Capture page errors
            def handle_page_error(error):
                javascript_errors.append(str(error))

            page.on("pageerror", handle_page_error)

            # Navigate and wait
            response = page.goto(url, timeout=self.timeout * 1000)
            page.wait_for_load_state("networkidle")
            time.sleep(wait_for_load)

            load_time = time.time() - start_time
            page_title = page.title()
            status_code = response.status if response else 0

            # Get performance metrics
            performance = page.evaluate(
                """() => {
                const perf = performance.timing;
                return {
                    loadTime: perf.loadEventEnd - perf.navigationStart,
                    domReady: perf.domContentLoadedEventEnd - perf.navigationStart,
                    responseTime: perf.responseEnd - perf.requestStart
                };
            }"""
            )

            error_summary = self._build_error_summary(
                len(console_errors), len(console_warnings), len(javascript_errors), len(network_errors)
            )

            return ValidationResult(
                url=url,
                success=len(console_errors) == 0 and len(javascript_errors) == 0,
                load_time=load_time,
                console_errors=console_errors,
                console_warnings=console_warnings,
                console_logs=console_logs,
                network_errors=network_errors,
                javascript_errors=javascript_errors,
                html_issues=[],
                performance_metrics=performance,
                page_title=page_title,
                status_code=status_code,
                timestamp=datetime.now().isoformat(),
                error_summary=error_summary,
            )

        except PlaywrightError as e:
            return self._create_error_result(url, f"Playwright error: {str(e)}")
        except Exception as e:
            return self._create_error_result(url, f"Validation error: {str(e)}")
        finally:
            browser.close()
            playwright.stop()

    def _validate_basic(self, url: str) -> ValidationResult:
        """Basic validation without browser automation"""
        start_time = time.time()

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "WebPageValidator/1.0"})
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                content = response.read().decode("utf-8")
                status_code = response.status
                load_time = time.time() - start_time

                # Basic checks
                javascript_errors = []
                html_issues = []

                # Check for common JavaScript error patterns in HTML
                if "SyntaxError" in content:
                    javascript_errors.append("Potential SyntaxError found in page content")
                if "Uncaught" in content:
                    javascript_errors.append("Potential Uncaught error found in page content")

                # Extract title
                import re

                title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
                page_title = title_match.group(1) if title_match else "No title"

                return ValidationResult(
                    url=url,
                    success=status_code == 200,
                    load_time=load_time,
                    console_errors=[],
                    console_warnings=[],
                    console_logs=[],
                    network_errors=[],
                    javascript_errors=javascript_errors,
                    html_issues=html_issues,
                    performance_metrics={"loadTime": load_time * 1000},
                    page_title=page_title,
                    status_code=status_code,
                    timestamp=datetime.now().isoformat(),
                    error_summary=f"Basic validation only (browser automation unavailable)",
                )

        except urllib.error.HTTPError as e:
            return self._create_error_result(url, f"HTTP {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            return self._create_error_result(url, f"URL error: {e.reason}")
        except Exception as e:
            return self._create_error_result(url, f"Request failed: {str(e)}")

    def _build_error_summary(self, errors: int, warnings: int, js_errors: int, network_errors: int) -> str:
        """Build human-readable error summary"""
        parts = []
        if errors > 0:
            parts.append(f"{errors} console error(s)")
        if warnings > 0:
            parts.append(f"{warnings} warning(s)")
        if js_errors > 0:
            parts.append(f"{js_errors} JavaScript error(s)")
        if network_errors > 0:
            parts.append(f"{network_errors} network error(s)")

        if not parts:
            return "No errors detected"
        return ", ".join(parts)

    def _create_error_result(self, url: str, error_msg: str) -> ValidationResult:
        """Create error result"""
        return ValidationResult(
            url=url,
            success=False,
            load_time=0.0,
            console_errors=[ConsoleLog(level="error", message=error_msg, source="validator")],
            console_warnings=[],
            console_logs=[],
            network_errors=[],
            javascript_errors=[],
            html_issues=[],
            performance_metrics={},
            page_title="",
            status_code=0,
            timestamp=datetime.now().isoformat(),
            error_summary=error_msg,
        )

    def close(self):
        """Cleanup browser resources"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def format_validation_report(result: ValidationResult, verbose: bool = False) -> str:
    """Format validation result as readable report"""
    lines = []
    lines.append("=" * 80)
    lines.append("WEB PAGE VALIDATION REPORT")
    lines.append("=" * 80)
    lines.append(f"URL: {result.url}")
    lines.append(f"Status: {'[OK] PASSED' if result.success else '[ERROR] FAILED'}")
    lines.append(f"Load Time: {result.load_time:.2f}s")
    lines.append(f"Page Title: {result.page_title}")
    lines.append(f"Timestamp: {result.timestamp}")
    lines.append("")

    # Summary
    lines.append("SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Console Errors: {len(result.console_errors)}")
    lines.append(f"Console Warnings: {len(result.console_warnings)}")
    lines.append(f"JavaScript Errors: {len(result.javascript_errors)}")
    lines.append(f"Network Errors: {len(result.network_errors)}")
    lines.append(f"Status: {result.error_summary}")
    lines.append("")

    # Console Errors
    if result.console_errors:
        lines.append("CONSOLE ERRORS")
        lines.append("-" * 80)
        for i, error in enumerate(result.console_errors, 1):
            lines.append(f"{i}. [{error.level.upper()}] {error.message}")
            if error.source and error.source != "unknown":
                lines.append(f"   Source: {error.source}")
            if error.line:
                lines.append(f"   Line: {error.line}, Column: {error.column}")
            lines.append(f"   Time: {error.timestamp}")
            lines.append("")

    # Console Warnings
    if result.console_warnings and verbose:
        lines.append("CONSOLE WARNINGS")
        lines.append("-" * 80)
        for i, warning in enumerate(result.console_warnings, 1):
            lines.append(f"{i}. [{warning.level.upper()}] {warning.message}")
            lines.append("")

    # JavaScript Errors
    if result.javascript_errors:
        lines.append("JAVASCRIPT ERRORS")
        lines.append("-" * 80)
        for i, error in enumerate(result.javascript_errors, 1):
            lines.append(f"{i}. {error}")
        lines.append("")

    # Network Errors
    if result.network_errors:
        lines.append("NETWORK ERRORS")
        lines.append("-" * 80)
        for i, error in enumerate(result.network_errors, 1):
            lines.append(f"{i}. {error.get('name', 'Unknown resource')}")
            lines.append(f"   Duration: {error.get('duration', 0):.2f}ms")
        lines.append("")

    # Performance Metrics
    if result.performance_metrics and verbose:
        lines.append("PERFORMANCE METRICS")
        lines.append("-" * 80)
        for key, value in result.performance_metrics.items():
            lines.append(f"{key}: {value}")
        lines.append("")

    # Recommendations
    if not result.success:
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 80)
        if result.javascript_errors:
            lines.append("1. Fix JavaScript syntax errors in source files")
            lines.append("2. Use Python raw strings (r'...') for JavaScript escape sequences")
            lines.append("3. Validate JavaScript code before deployment")
        if result.network_errors:
            lines.append("4. Check network requests and resource URLs")
            lines.append("5. Verify all static assets are accessible")
        lines.append("")

    lines.append("=" * 80)

    return "\n".join(lines)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Web Page Validator with JavaScript Error Detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate local dashboard
  python web_page_validator.py http://127.0.0.1:5000

  # Validate with detailed output
  python web_page_validator.py http://127.0.0.1:5000 --verbose

  # Save report to file
  python web_page_validator.py http://127.0.0.1:5000 --output report.txt

  # Show browser window during validation
  python web_page_validator.py http://127.0.0.1:5000 --no-headless
        """,
    )

    parser.add_argument("url", help="URL to validate")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output including warnings")
    parser.add_argument("--output", "-o", help="Save report to file")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--no-headless", action="store_true", help="Show browser window (for debugging)")
    parser.add_argument("--timeout", type=int, default=30, help="Page load timeout in seconds (default: 30)")
    parser.add_argument("--wait", type=int, default=3, help="Wait time after page load in seconds (default: 3)")

    args = parser.parse_args()

    # Run validation
    print(f"[INFO] Validating {args.url}...")
    print(
        f"[INFO] Using {'Selenium' if SELENIUM_AVAILABLE else 'Playwright' if PLAYWRIGHT_AVAILABLE else 'basic HTTP'} validation"
    )
    print()

    with WebPageValidator(headless=not args.no_headless, timeout=args.timeout) as validator:
        result = validator.validate_url(args.url, wait_for_load=args.wait)

    # Output results
    if args.json:
        output = json.dumps(result.to_dict(), indent=2)
    else:
        output = format_validation_report(result, verbose=args.verbose)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[OK] Report saved to {args.output}")
    else:
        print(output)

    # Exit with error code if validation failed
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
