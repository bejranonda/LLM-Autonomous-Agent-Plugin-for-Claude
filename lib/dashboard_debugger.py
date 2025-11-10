#!/usr/bin/env python3
"""
Comprehensive Dashboard Debugger
Implements iterative debugging loop that continues until data is shown or no failures
"""

import sys
import os
import time
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Add plugin lib directory to path
plugin_lib = Path(__file__).parent
sys.path.insert(0, str(plugin_lib))

try:
    from web_page_validator import WebPageValidator
    VALIDATOR_AVAILABLE = True
except ImportError:
    VALIDATOR_AVAILABLE = False


class DashboardDebugger:
    """Iterative debugger that continues until issues are resolved"""

    def __init__(self, dashboard_url="http://127.0.0.1:5001"):
        self.dashboard_url = dashboard_url
        self.debug_log = []
        self.fix_attempts = 0
        self.max_attempts = 10

    def log_debug(self, level: str, message: str):
        """Log debug messages with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.debug_log.append(log_entry)
        print(log_entry)

    def check_javascript_errors(self, html_content: str) -> List[str]:
        """Check for JavaScript syntax errors in HTML content"""
        errors = []

        # Look for common JavaScript syntax issues
        lines = html_content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'Uncaught SyntaxError' in line or 'missing ) after argument list' in line:
                errors.append(f"Line {i}: {line.strip()}")

            # Check for template literal issues
            if '`' in line and '${' in line:
                # Check if template literal is properly closed
                backtick_count = line.count('`')
                if backtick_count % 2 != 0:
                    errors.append(f"Line {i}: Unclosed template literal: {line.strip()}")

            # Check for arrow function issues
            if '=>' in line and line.count('(') != line.count(')'):
                errors.append(f"Line {i}: Mismatched parentheses in arrow function: {line.strip()}")

        return errors

    def check_data_display(self, html_content: str) -> Dict[str, bool]:
        """Check if dashboard sections are displaying actual data"""
        checks = {
            'token_savings_shown': False,
            'kpi_scores_shown': False,
            'system_metrics_shown': False,
            'charts_rendered': False,
            'tables_populated': False
        }

        # Check for actual data values (not placeholder zeros)
        if 'token-savings' in html_content:
            # Look for non-zero token values
            token_pattern = r'id="token-savings"[^>]*>([^<]+)'
            match = re.search(token_pattern, html_content)
            if match and match.group(1).strip() not in ['0', '0.0', '$0', '0%']:
                checks['token_savings_shown'] = True

        # Check for KPI scores
        if 'overall-score' in html_content:
            kpi_pattern = r'id="overall-score"[^>]*>([^<]+)'
            match = re.search(kpi_pattern, html_content)
            if match and match.group(1).strip() not in ['0', '0.0']:
                checks['kpi_scores_shown'] = True

        # Check for system metrics
        if 'cpu-value' in html_content or 'memory-value' in html_content:
            sys_pattern = r'id="(cpu|memory)-value"[^>]*>([^<]+)'
            matches = re.findall(sys_pattern, html_content)
            for match in matches:
                if match[1].strip() not in ['0', '0.0', '0%']:
                    checks['system_metrics_shown'] = True
                    break

        # Check for chart elements
        if 'canvas' in html_content or 'chart' in html_content.lower():
            checks['charts_rendered'] = True

        # Check for table data
        if '<table' in html_content and ('<td>' in html_content and len(re.findall(r'<td>([^<]+)</td>', html_content)) > 5):
            checks['tables_populated'] = True

        return checks

    def analyze_apis(self) -> Dict[str, bool]:
        """Test if dashboard APIs are returning data"""
        apis = {
            'tokens_api': f'{self.dashboard_url}/api/sections/tokens',
            'kpi_api': f'{self.dashboard_url}/api/sections/kpi',
            'system_api': f'{self.dashboard_url}/api/sections/system',
            'analytics_api': f'{self.dashboard_url}/api/analytics'
        }

        results = {}

        try:
            import urllib.request
            import json

            for api_name, url in apis.items():
                try:
                    with urllib.request.urlopen(url, timeout=5) as response:
                        if response.getcode() == 200:
                            data = json.loads(response.read().decode('utf-8'))
                            # Check if API returns meaningful data
                            has_data = bool(data and len(str(data)) > 50)
                            results[api_name] = has_data
                            self.log_debug("INFO", f"{api_name}: {'OK' if has_data else 'NO DATA'}")
                        else:
                            results[api_name] = False
                            self.log_debug("ERROR", f"{api_name}: HTTP {response.getcode()}")
                except Exception as e:
                    results[api_name] = False
                    self.log_debug("ERROR", f"{api_name}: {str(e)}")

        except ImportError:
            self.log_debug("WARN", "urllib not available - skipping API checks")
            for api_name in apis:
                results[api_name] = None

        return results

    def apply_auto_fixes(self, errors: List[str]) -> bool:
        """Apply automatic fixes for common JavaScript errors"""
        if not errors:
            return False

        dashboard_path = Path('.claude-patterns/dashboard.py')
        if not dashboard_path.exists():
            self.log_debug("ERROR", "Dashboard file not found")
            return False

        try:
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            fixes_applied = 0

            # Fix 1: Convert remaining template literals to string concatenation
            template_pattern = r'`([^`]*\$\{[^}]*\}[^`]*)`'

            def replace_template(match):
                nonlocal fixes_applied
                fixes_applied += 1
                template_content = match.group(1)

                # Convert template literal to string concatenation
                parts = re.split(r'\$\{([^}]+)\}', template_content)
                result = "'"
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        # Literal string part
                        escaped_part = part.replace("'", "\\'")
                        result += escaped_part
                    else:
                        # Variable/expression part
                        result += "' + (" + part + ") + '"
                result += "'"
                return result

            content = re.sub(template_pattern, replace_template, content)

            # Fix 2: Convert arrow functions to traditional functions
            arrow_pattern = r'(\w+)\s*=\s*\(([^)]*)\)\s*=>\s*\{'
            content = re.sub(arrow_pattern, r'function \1(\2) {', content)

            # Fix 3: Fix setTimeout with arrow functions
            timeout_pattern = r'setTimeout\(\s*\(\)\s*=>\s*\{([^}]+)\},\s*(\d+)\s*\)'
            content = re.sub(timeout_pattern, r'setTimeout(function() {\1}, \2)', content)

            # Fix 4: Handle unclosed template literals
            lines = content.split('\n')
            fixed_lines = []
            for i, line in enumerate(lines):
                if '`' in line and line.count('`') % 2 != 0:
                    # Unclosed template literal - close it
                    if not line.strip().endswith('`'):
                        line += "`"
                    fixes_applied += 1
                fixed_lines.append(line)

            content = '\n'.join(fixed_lines)

            # Write back if changes were made
            if content != original_content:
                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.log_debug("FIX", f"Applied {fixes_applied} automatic fixes")
                return True
            else:
                self.log_debug("INFO", "No auto-fixes applicable")
                return False

        except Exception as e:
            self.log_debug("ERROR", f"Auto-fix failed: {e}")
            return False

    def run_debugging_loop(self) -> bool:
        """Run iterative debugging loop until success or max attempts"""
        self.log_debug("START", "Starting comprehensive dashboard debugging")

        while self.fix_attempts < self.max_attempts:
            self.fix_attempts += 1
            self.log_debug("ATTEMPT", f"Debugging attempt {self.fix_attempts}/{self.max_attempts}")

            # Step 1: Check if dashboard is running
            try:
                import urllib.request
                with urllib.request.urlopen(self.dashboard_url, timeout=5) as response:
                    if response.getcode() != 200:
                        self.log_debug("ERROR", "Dashboard not responding correctly")
                        return False
            except Exception as e:
                self.log_debug("ERROR", f"Dashboard not accessible: {e}")
                return False

            # Step 2: Get page content and analyze
            try:
                import urllib.request
                with urllib.request.urlopen(self.dashboard_url, timeout=10) as response:
                    html_content = response.read().decode('utf-8')
            except Exception as e:
                self.log_debug("ERROR", f"Failed to fetch page content: {e}")
                return False

            # Step 3: Check for JavaScript errors
            js_errors = self.check_javascript_errors(html_content)
            if js_errors:
                self.log_debug("ERROR", f"Found {len(js_errors)} JavaScript errors:")
                for error in js_errors:
                    self.log_debug("JS_ERROR", error)

                # Try to fix automatically
                if self.apply_auto_fixes(js_errors):
                    self.log_debug("INFO", "Auto-fixes applied, waiting for server reload...")
                    time.sleep(3)  # Wait for potential auto-reload
                    continue
                else:
                    self.log_debug("ERROR", "Could not auto-fix JavaScript errors")
                    return False

            # Step 4: Check API responses
            api_results = self.analyze_apis()
            failed_apis = [name for name, status in api_results.items() if status is False]
            if failed_apis:
                self.log_debug("ERROR", f"Failed APIs: {', '.join(failed_apis)}")
                return False

            # Step 5: Check if data is being displayed
            data_checks = self.check_data_display(html_content)
            self.log_debug("INFO", f"Data display checks: {data_checks}")

            # Check if we have meaningful data in dashboard sections
            meaningful_data = any(data_checks.values())
            if not meaningful_data:
                self.log_debug("WARN", "No meaningful data detected in dashboard sections")

                # Check if it's just a timing issue - wait and retry once
                if self.fix_attempts == 1:
                    self.log_debug("INFO", "First attempt - waiting 5 seconds for data to load...")
                    time.sleep(5)
                    continue
                else:
                    self.log_debug("ERROR", "Dashboard sections not showing data after multiple attempts")
                    return False

            # Step 6: Use web validator for comprehensive check if available
            if VALIDATOR_AVAILABLE:
                try:
                    with WebPageValidator(headless=True, timeout=10) as validator:
                        result = validator.validate_url(self.dashboard_url, wait_for_load=5)

                    if not result.success:
                        self.log_debug("ERROR", "Web validator detected issues")
                        if result.console_errors:
                            for error in result.console_errors[:3]:
                                self.log_debug("CONSOLE_ERROR", f"{error.level}: {error.message}")
                        return False
                    else:
                        self.log_debug("SUCCESS", "Web validator passed - no console errors detected")

                except Exception as e:
                    self.log_debug("WARN", f"Web validator failed: {e}")

            # If we reach here, everything looks good
            self.log_debug("SUCCESS", "Dashboard is working correctly - data is being displayed")
            return True

        self.log_debug("ERROR", f"Maximum debugging attempts ({self.max_attempts}) reached")
        return False

    def generate_debug_report(self) -> str:
        """Generate comprehensive debug report"""
        report = f"""
# DASHBOARD DEBUGGING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target URL: {self.dashboard_url}
Debug Attempts: {self.fix_attempts}

## DEBUG LOG
{chr(10).join(self.debug_log)}

## RECOMMENDATIONS
"""

        if self.fix_attempts >= self.max_attempts:
            report += """
### CRITICAL ISSUES FOUND
- Maximum debugging attempts reached without success
- Manual intervention required

### NEXT STEPS
1. Check browser console for JavaScript errors manually
2. Verify API endpoints are returning data
3. Check dashboard logs for server-side errors
4. Review JavaScript code for syntax issues
"""

        return report


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description='Comprehensive dashboard debugging')
    parser.add_argument('--url', default='http://127.0.0.1:5001',
                       help='Dashboard URL to debug')
    parser.add_argument('--max-attempts', type=int, default=10,
                       help='Maximum debugging attempts')
    parser.add_argument('--report', action='store_true',
                       help='Save debug report to file')

    args = parser.parse_args()

    debugger = DashboardDebugger(args.url)
    debugger.max_attempts = args.max_attempts

    success = debugger.run_debugging_loop()

    if args.report or not success:
        report_dir = Path('.claude/reports')
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        report_file = report_dir / f'dashboard-debug-{timestamp}.md'

        report_file.write_text(debugger.generate_debug_report(), encoding='utf-8')
        print(f"[OK] Debug report saved to: {report_file}")

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())