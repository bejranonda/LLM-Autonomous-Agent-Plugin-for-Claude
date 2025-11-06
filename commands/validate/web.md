---
description: Validate web pages and detect JavaScript errors automatically using headless browser automation
category: validation
---

# Web Page Validation Command

Automatically validate web pages (like dashboard.py) and detect JavaScript errors, console issues, and performance problems without manual browser inspection.

## Usage

```bash
/validate:web <URL> [options]
```

## Examples

```bash
# Validate local dashboard
/validate:web http://127.0.0.1:5000

# Validate with detailed output
/validate:web http://127.0.0.1:5000 --verbose

# Validate and auto-fix issues
/validate:web http://127.0.0.1:5000 --auto-fix

# Save validation report
/validate:web http://127.0.0.1:5000 --report
```

## Implementation

```python
#!/usr/bin/env python3
import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Add plugin lib directory to path
plugin_lib = Path(__file__).parent.parent.parent / 'lib'
sys.path.insert(0, str(plugin_lib))

try:
    from web_page_validator import WebPageValidator, format_validation_report
    VALIDATOR_AVAILABLE = True
except ImportError:
    VALIDATOR_AVAILABLE = False


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description='Validate web pages automatically')
    parser.add_argument('url', nargs='?', default='http://127.0.0.1:5000',
                       help='URL to validate (default: http://127.0.0.1:5000)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output including warnings')
    parser.add_argument('--auto-fix', action='store_true',
                       help='Attempt to automatically fix detected issues')
    parser.add_argument('--report', action='store_true',
                       help='Save detailed report to .claude/reports/')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Page load timeout in seconds')
    parser.add_argument('--wait', type=int, default=3,
                       help='Wait time after page load in seconds')

    args = parser.parse_args()

    print("[INFO] Web Page Validation")
    print(f"[INFO] Target URL: {args.url}")
    print()

    if not VALIDATOR_AVAILABLE:
        print("[ERROR] Web page validator not available")
        print("[INFO] Install dependencies: pip install selenium")
        print("[INFO] Install ChromeDriver: https://chromedriver.chromium.org/")
        return 1

    # Run validation
    print("[INFO] Starting headless browser validation...")
    print("[INFO] This may take a few seconds...")
    print()

    try:
        with WebPageValidator(headless=True, timeout=args.timeout) as validator:
            result = validator.validate_url(args.url, wait_for_load=args.wait)

        # Display results
        if result.success:
            print("=" * 80)
            print("[OK] VALIDATION PASSED")
            print("=" * 80)
            print(f"URL: {result.url}")
            print(f"Page Title: {result.page_title}")
            print(f"Load Time: {result.load_time:.2f}s")
            print(f"Console Errors: 0")
            print(f"Console Warnings: {len(result.console_warnings)}")
            print(f"JavaScript Errors: 0")
            print()
            print("[OK] No errors detected - page is functioning correctly")
            print()

            if result.console_warnings and args.verbose:
                print("WARNINGS:")
                for i, warning in enumerate(result.console_warnings[:5], 1):
                    print(f"  {i}. {warning.message}")
                if len(result.console_warnings) > 5:
                    print(f"  ... and {len(result.console_warnings) - 5} more warnings")
                print()

        else:
            print("=" * 80)
            print("[ERROR] VALIDATION FAILED")
            print("=" * 80)
            print(f"URL: {result.url}")
            print(f"Page Title: {result.page_title}")
            print(f"Load Time: {result.load_time:.2f}s")
            print()
            print("ERROR SUMMARY:")
            print(f"  Console Errors: {len(result.console_errors)}")
            print(f"  Console Warnings: {len(result.console_warnings)}")
            print(f"  JavaScript Errors: {len(result.javascript_errors)}")
            print(f"  Network Errors: {len(result.network_errors)}")
            print()

            # Show top errors
            if result.console_errors:
                print("TOP CONSOLE ERRORS:")
                for i, error in enumerate(result.console_errors[:3], 1):
                    print(f"  {i}. [{error.level.upper()}] {error.message[:80]}")
                    if error.source and error.source != 'unknown':
                        print(f"     Source: {error.source}")
                if len(result.console_errors) > 3:
                    print(f"  ... and {len(result.console_errors) - 3} more errors")
                print()

            # Show JavaScript errors
            if result.javascript_errors:
                print("JAVASCRIPT ERRORS:")
                for i, js_error in enumerate(result.javascript_errors[:3], 1):
                    print(f"  {i}. {js_error[:80]}")
                if len(result.javascript_errors) > 3:
                    print(f"  ... and {len(result.javascript_errors) - 3} more errors")
                print()

            # Auto-fix suggestions
            if args.auto_fix:
                print("AUTO-FIX ANALYSIS:")
                print("  Analyzing errors for automatic fixes...")
                print()

                # Check for string escaping issues
                has_escape_issues = any(
                    'SyntaxError' in str(e) or 'unexpected token' in str(e).lower()
                    for e in result.javascript_errors
                )

                if has_escape_issues:
                    print("  [DETECTED] String escaping issues in JavaScript")
                    print("  [FIX] Use Python raw strings (r'...') for JavaScript escape sequences")
                    print("  [EXAMPLE] Change 'Value\\n' to r'Value\\n' in Python source")
                    print()
                    print("  [ACTION] Would you like to apply automatic fixes? (y/n)")
                else:
                    print("  [INFO] No auto-fixable issues detected")
                    print("  [INFO] Manual review required for detected errors")
                print()

        # Save detailed report
        if args.report or not result.success:
            report_dir = Path('.claude/reports')
            report_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
            report_file = report_dir / f'web-validation-{timestamp}.md'

            report_content = format_validation_report(result, verbose=True)
            report_file.write_text(report_content, encoding='utf-8')

            print(f"[OK] Detailed report saved to: {report_file}")
            print()

        # Performance metrics
        if args.verbose and result.performance_metrics:
            print("PERFORMANCE METRICS:")
            for key, value in result.performance_metrics.items():
                if isinstance(value, (int, float)):
                    print(f"  {key}: {value:.2f}ms")
                else:
                    print(f"  {key}: {value}")
            print()

        print("=" * 80)

        return 0 if result.success else 1

    except KeyboardInterrupt:
        print("\n[WARN] Validation interrupted by user")
        return 130
    except Exception as e:
        print(f"[ERROR] Validation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
```

## Features

- **Automated Error Detection**: Captures JavaScript errors without manual browser inspection
- **Console Log Monitoring**: Captures errors, warnings, and info logs from browser console
- **Network Monitoring**: Detects failed HTTP requests and resource loading issues
- **Performance Metrics**: Measures page load time and resource usage
- **Auto-Fix Suggestions**: Provides guidance on fixing detected issues
- **Detailed Reports**: Saves comprehensive validation reports to `.claude/reports/`

## Requirements

**Recommended** (for full functionality):
```bash
pip install selenium
```

**ChromeDriver** (for Selenium):
- Download from: https://chromedriver.chromium.org/
- Or install automatically: `pip install webdriver-manager`

**Alternative** (if Selenium unavailable):
```bash
pip install playwright
playwright install chromium
```

## Integration with Dashboard

This command is automatically invoked when starting dashboards via `/monitor:dashboard` to ensure no JavaScript errors exist before displaying to the user.

## Output Format

**Terminal Output** (concise summary):
```
[OK] VALIDATION PASSED
URL: http://127.0.0.1:5000
Page Title: Autonomous Agent Dashboard
Load Time: 1.23s
Console Errors: 0
JavaScript Errors: 0
```

**Report File** (detailed analysis):
```markdown
# WEB PAGE VALIDATION REPORT

## Summary
- URL: http://127.0.0.1:5000
- Status: PASSED
- Load Time: 1.23s
- Console Errors: 0
- JavaScript Errors: 0

## Console Errors
(none detected)

## Performance Metrics
- Load Time: 1234ms
- DOM Ready: 456ms
- Resources: 15 loaded successfully
```

## Error Categories

1. **JavaScript Syntax Errors**: Invalid JavaScript code
2. **Runtime Errors**: Uncaught exceptions during execution
3. **Reference Errors**: Undefined variables or functions
4. **Type Errors**: Invalid type operations
5. **Network Errors**: Failed HTTP requests
6. **Resource Errors**: Missing CSS, JS, or image files

## Best Practices

- Run validation after making changes to web components
- Always validate before committing dashboard changes
- Use `--auto-fix` for common issues like string escaping
- Save reports for debugging with `--report` flag
- Increase `--timeout` for slow-loading pages
- Use `--verbose` for detailed troubleshooting

## See Also

- `/monitor:dashboard` - Start dashboard with automatic validation
- `/analyze:quality` - Comprehensive quality control including web validation
- Skill: web-validation - Detailed methodology and best practices
