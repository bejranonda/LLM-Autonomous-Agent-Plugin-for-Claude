---
name: validate:web
description: Validate web pages and detect JavaScript errors automatically using headless browser automation
category: validation
---

# Validate Web Command

**Slash command**: `/validate:web`

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

# Crawl and validate all subpages
/validate:web http://127.0.0.1:5000 --crawl

# Crawl with depth limit
/validate:web http://127.0.0.1:5000 --crawl --max-depth 2

# Crawl specific subpages only
/validate:web http://127.0.0.1:5000 --crawl --include "/api/*,/analytics/*"

# Exclude certain paths from crawling
/validate:web http://127.0.0.1:5000 --crawl --exclude "/admin/*,/debug/*"
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

# Import additional modules for crawling
try:
    from urllib.parse import urljoin, urlparse, urlunparse
    from fnmatch import fnmatch
    import re
    import time
    from collections import deque
    CRAWLING_AVAILABLE = True
except ImportError:
    CRAWLING_AVAILABLE = False


def crawl_and_validate(validator, start_url, max_depth=3, max_pages=50,
                       include_patterns=None, exclude_patterns=None,
                       same_domain=True, wait_for_load=3, verbose=False):
    """Crawl and validate all pages discovered from the start URL."""

    if not CRAWLING_AVAILABLE:
        raise ImportError("Required crawling modules not available")

    from urllib.parse import urljoin, urlparse, urlunparse
    from fnmatch import fnmatch
    import time
    from collections import deque

    start_domain = urlparse(start_url).netloc
    visited = set()
    queue = deque([(start_url, 0)])  # (url, depth)
    results = []

    print(f"[INFO] Starting crawl from: {start_url}")
    print(f"[INFO] Domain: {start_domain}")
    print()

    while queue and len(results) < max_pages:
        current_url, depth = queue.popleft()

        # Skip if already visited
        if current_url in visited:
            continue
        visited.add(current_url)

        # Check depth limit
        if depth > max_depth:
            continue

        # Check domain restriction
        if same_domain and urlparse(current_url).netloc != start_domain:
            continue

        # Check include/exclude patterns
        if not should_crawl_url(current_url, include_patterns, exclude_patterns):
            continue

        print(f"[INFO] Validating (depth {depth}): {current_url}")

        try:
            # Validate the current page
            result = validator.validate_url(current_url, wait_for_load=wait_for_load)
            result.depth = depth  # Add depth information

            results.append(result)

            # Show progress
            status = "✅ PASS" if result.success else "❌ FAIL"
            errors = len(result.console_errors) + len(result.javascript_errors)
            print(f"[{status}] {errors} errors, {len(result.console_warnings)} warnings")

            # Extract links for further crawling (only from successful pages)
            if result.success and depth < max_depth:
                links = extract_links_from_page(current_url, result.page_content or "")
                for link in links:
                    if link not in visited and len(visited) + len(queue) < max_pages:
                        queue.append((link, depth + 1))

            # Brief pause to avoid overwhelming the server
            time.sleep(0.5)

        except Exception as e:
            print(f"[ERROR] Failed to validate {current_url}: {e}")
            # Create a failed result object
            from types import SimpleNamespace
            failed_result = SimpleNamespace(
                url=current_url,
                success=False,
                load_time=0,
                page_title="Error",
                console_errors=[f"Validation failed: {e}"],
                console_warnings=[],
                javascript_errors=[],
                network_errors=[],
                depth=depth,
                page_content=""
            )
            results.append(failed_result)

    print()
    print(f"[INFO] Crawling completed: {len(results)} pages validated")
    print(f"[INFO] Pages discovered: {len(visited)}")

    return results


def should_crawl_url(url, include_patterns=None, exclude_patterns=None):
    """Check if URL should be crawled based on include/exclude patterns."""
    from urllib.parse import urlparse

    parsed = urlparse(url)
    path = parsed.path

    # Skip non-HTML resources
    if any(path.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf', '.zip']):
        return False

    # Skip hash fragments
    if parsed.fragment:
        return False

    # Check include patterns
    if include_patterns:
        if not any(fnmatch(path, pattern.strip()) for pattern in include_patterns):
            return False

    # Check exclude patterns
    if exclude_patterns:
        if any(fnmatch(path, pattern.strip()) for pattern in exclude_patterns):
            return False

    return True


def extract_links_from_page(base_url, page_content):
    """Extract all valid links from page content."""
    from urllib.parse import urljoin, urlparse
    import re

    if not page_content:
        return []

    # Extract links using regex patterns
    link_patterns = [
        r'href=["\']([^"\']+)["\']',  # href attributes
        r'action=["\']([^"\']+)["\']',  # form actions
        r'src=["\']([^"\']+)["\']',   # src attributes (for some dynamic content)
    ]

    links = set()

    for pattern in link_patterns:
        matches = re.findall(pattern, page_content, re.IGNORECASE)
        for match in matches:
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, match)

            # Validate URL
            parsed = urlparse(absolute_url)
            if parsed.scheme in ['http', 'https'] and parsed.netloc:
                links.add(absolute_url)

    return list(links)


def display_crawling_results(results):
    """Display comprehensive crawling results."""
    if not results:
        print("[ERROR] No pages were validated")
        return

    # Sort results by URL for consistent output
    results.sort(key=lambda r: r.url)

    # Summary statistics
    total_pages = len(results)
    successful_pages = sum(1 for r in results if r.success)
    failed_pages = total_pages - successful_pages

    total_errors = sum(len(r.console_errors) + len(r.javascript_errors) for r in results)
    total_warnings = sum(len(r.console_warnings) for r in results)

    print("=" * 80)
    print(f"🕷️  CRAWLING VALIDATION RESULTS")
    print("=" * 80)
    print(f"Total Pages: {total_pages}")
    print(f"Successful: {successful_pages} ✅")
    print(f"Failed: {failed_pages} ❌")
    print(f"Total Errors: {total_errors}")
    print(f"Total Warnings: {total_warnings}")
    print(f"Success Rate: {(successful_pages/total_pages)*100:.1f}%")
    print()

    # Show failed pages first
    failed_results = [r for r in results if not r.success]
    if failed_results:
        print("❌ FAILED PAGES:")
        for i, result in enumerate(failed_results, 1):
            print(f"  {i}. {result.url}")
            print(f"     Status: FAILED")
            errors = len(result.console_errors) + len(result.javascript_errors)
            if errors > 0:
                print(f"     Errors: {errors}")
            print()

    # Show successful pages with warnings
    successful_with_warnings = [r for r in results if r.success and
                              (len(r.console_warnings) > 0 or
                               len(r.console_errors) > 0 or
                               len(r.javascript_errors) > 0)]

    if successful_with_warnings:
        print("⚠️  SUCCESSFUL PAGES WITH ISSUES:")
        for i, result in enumerate(successful_with_warnings[:10], 1):  # Limit to first 10
            errors = len(result.console_errors) + len(result.javascript_errors)
            warnings = len(result.console_warnings)
            status_parts = []
            if errors > 0:
                status_parts.append(f"{errors} errors")
            if warnings > 0:
                status_parts.append(f"{warnings} warnings")
            print(f"  {i}. {result.url}")
            print(f"     Issues: {', '.join(status_parts)}")
        if len(successful_with_warnings) > 10:
            print(f"  ... and {len(successful_with_warnings) - 10} more pages with issues")
        print()

    # Show top errors across all pages
    all_errors = []
    for result in results:
        for error in result.console_errors:
            all_errors.append(f"[{error.level.upper()}] {error.message[:100]}")
        for error in result.javascript_errors:
            all_errors.append(f"[JS] {str(error)[:100]}")

    if all_errors:
        print("🔍 TOP ERRORS ACROSS ALL PAGES:")
        from collections import Counter
        error_counts = Counter(all_errors)
        for i, (error, count) in enumerate(error_counts.most_common(10), 1):
            print(f"  {i}. ({count}×) {error}")
        print()

    # Overall status
    if successful_pages == total_pages:
        print("🎉 OVERALL STATUS: ALL PAGES PASSED ✅")
    elif successful_pages > total_pages * 0.8:
        print("✅ OVERALL STATUS: MOSTLY HEALTHY ({successful_pages}/{total_pages} pages passed)")
    else:
        print("⚠️  OVERALL STATUS: NEEDS ATTENTION ({successful_pages}/{total_pages} pages passed)")

    print("=" * 80)


def save_crawling_report(results, base_url):
    """Save comprehensive crawling report to file."""
    from datetime import datetime

    report_dir = Path('.claude/reports')
    report_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    report_file = report_dir / f'web-crawling-{timestamp}.md'

    # Generate report content
    content = generate_crawling_report_content(results, base_url)

    report_file.write_text(content, encoding='utf-8')
    print(f"[OK] Comprehensive crawling report saved to: {report_file}")


def generate_crawling_report_content(results, base_url):
    """Generate comprehensive markdown report for crawling results."""
    from datetime import datetime

    total_pages = len(results)
    successful_pages = sum(1 for r in results if r.success)
    failed_pages = total_pages - successful_pages
    total_errors = sum(len(r.console_errors) + len(r.javascript_errors) for r in results)
    total_warnings = sum(len(r.console_warnings) for r in results)

    content = f"""{'='*80}
WEB CRAWLING VALIDATION REPORT
{'='*80}

**Base URL**: {base_url}
**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status**: {'PASSED' if successful_pages == total_pages else 'FAILED'}

## SUMMARY
{'-'*40}
- **Total Pages**: {total_pages}
- **Successful**: {successful_pages} ✅
- **Failed**: {failed_pages} ❌
- **Success Rate**: {(successful_pages/total_pages)*100:.1f}%
- **Total Errors**: {total_errors}
- **Total Warnings**: {total_warnings}

## DETAILED RESULTS
{'-'*40}
"""

    # Sort results by status and URL
    results.sort(key=lambda r: (not r.success, r.url))

    for i, result in enumerate(results, 1):
        status_icon = "✅" if result.success else "❌"
        content += f"""
### {i}. {result.url} {status_icon}

**Status**: {'PASSED' if result.success else 'FAILED'}
**Load Time**: {result.load_time:.2f}s
**Page Title**: {result.page_title}
"""

        if not result.success:
            errors = len(result.console_errors) + len(result.javascript_errors)
            content += f"**Total Errors**: {errors}\n"

            if result.console_errors:
                content += "\n**Console Errors:**\n"
                for j, error in enumerate(result.console_errors[:5], 1):
                    content += f"  {j}. [{error.level.upper()}] {error.message}\n"
                if len(result.console_errors) > 5:
                    content += f"  ... and {len(result.console_errors) - 5} more errors\n"

            if result.javascript_errors:
                content += "\n**JavaScript Errors:**\n"
                for j, error in enumerate(result.javascript_errors[:5], 1):
                    content += f"  {j}. {str(error)}\n"
                if len(result.javascript_errors) > 5:
                    content += f"  ... and {len(result.javascript_errors) - 5} more errors\n"

        if result.console_warnings:
            content += f"**Warnings**: {len(result.console_warnings)}\n"
            if len(result.console_warnings) <= 3:
                for j, warning in enumerate(result.console_warnings, 1):
                    content += f"  {j}. {warning.message}\n"
            else:
                content += f"  Top 3 warnings:\n"
                for j, warning in enumerate(result.console_warnings[:3], 1):
                    content += f"    {j}. {warning.message}\n"
                content += f"  ... and {len(result.console_warnings) - 3} more warnings\n"

        content += "\n---\n"

    # Add recommendations section
    content += f"""
## RECOMMENDATIONS
{'-'*40}

"""

    if failed_pages > 0:
        content += f"""### 🚨 Priority Fixes ({failed_pages} pages failed)
1. **Fix JavaScript Errors**: Review and fix syntax errors in failed pages
2. **Check Server Configuration**: Ensure all resources load correctly
3. **Validate HTML Structure**: Check for malformed HTML causing issues
4. **Test Functionality**: Verify interactive elements work properly

"""

    if total_errors > 0:
        content += f"""### 🔧 Technical Improvements ({total_errors} total errors)
1. **Console Error Resolution**: Fix JavaScript runtime errors
2. **Resource Loading**: Ensure all assets (CSS, JS, images) are accessible
3. **Network Issues**: Check for failed API calls or missing resources
4. **Error Handling**: Implement proper error handling in JavaScript

"""

    if total_warnings > 0:
        content += f"""### ⚠️ Code Quality ({total_warnings} warnings)
1. **Deprecation Warnings**: Update deprecated API usage
2. **Performance Optimization**: Address performance warnings
3. **Best Practices**: Follow modern web development standards
4. **Code Cleanup**: Remove unused code and console logs

"""

    content += f"""
## VALIDATION METRICS
{'-'*40}
- **Validation Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Tool**: Web Page Validator with Crawling
- **Scope**: Full site validation with subpage discovery
- **Coverage**: {total_pages} pages analyzed
- **Effectiveness**: {((successful_pages/total_pages)*100):.1f}% success rate

{'='*80}
"""

    return content


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

    # Crawling options
    parser.add_argument('--crawl', action='store_true',
                       help='Crawl and validate all subpages found on the site')
    parser.add_argument('--max-depth', type=int, default=3,
                       help='Maximum crawl depth (default: 3)')
    parser.add_argument('--max-pages', type=int, default=50,
                       help='Maximum number of pages to crawl (default: 50)')
    parser.add_argument('--include', type=str, default='',
                       help='Comma-separated list of path patterns to include (e.g., "/api/*,/analytics/*")')
    parser.add_argument('--exclude', type=str, default='',
                       help='Comma-separated list of path patterns to exclude (e.g., "/admin/*,/debug/*")')
    parser.add_argument('--same-domain', action='store_true', default=True,
                       help='Only crawl pages on the same domain (default: True)')

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
    if args.crawl:
        print("[INFO] Starting web page crawling and validation...")
        print(f"[INFO] Max depth: {args.max_depth}, Max pages: {args.max_pages}")
        print("[INFO] This may take several minutes depending on site size...")
        print()

        if args.include:
            print(f"[INFO] Including only: {args.include}")
        if args.exclude:
            print(f"[INFO] Excluding: {args.exclude}")
        print()
    else:
        print("[INFO] Starting headless browser validation...")
        print("[INFO] This may take a few seconds...")
        print()

    try:
        with WebPageValidator(headless=True, timeout=args.timeout) as validator:
            if args.crawl:
                # Enhanced crawling functionality
                results = crawl_and_validate(
                    validator, args.url,
                    max_depth=args.max_depth,
                    max_pages=args.max_pages,
                    include_patterns=args.include.split(',') if args.include else [],
                    exclude_patterns=args.exclude.split(',') if args.exclude else [],
                    same_domain=args.same_domain,
                    wait_for_load=args.wait,
                    verbose=args.verbose
                )

                # Display crawling results
                display_crawling_results(results)

                # Save comprehensive report
                if args.report or not all(r.success for r in results):
                    save_crawling_report(results, args.url)

                # Return appropriate exit code
                return 0 if all(r.success for r in results) else 1
            else:
                # Single page validation (existing logic)
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
- **🆕 Subpage Crawling**: Automatically discovers and validates all subpages on a website
- **🆕 Comprehensive Coverage**: Crawl with configurable depth limits (default: 3 levels)
- **🆕 Smart Filtering**: Include/exclude specific paths with pattern matching
- **🆕 Site-wide Analysis**: Aggregates errors and warnings across entire website
- **🆕 Progress Tracking**: Real-time crawling progress with detailed status updates

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
