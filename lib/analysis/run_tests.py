#!/usr/bin/env python3
#    Test Runner for Autonomous Agent Plugin
"""

Comprehensive test runner with cross-platform support and detailed reporting.
Provides multiple test execution modes and comprehensive output formatting.

Usage:
    python run_tests.py                    # Run all tests with coverage
    python run_tests.py --unit             # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py --fast             # Run tests without coverage (faster)
    python run_tests.py --platform         # Run cross-platform tests
    python run_tests.py --report           # Generate HTML coverage report
    python run_tests.py --performance      # Run performance benchmarks
"""
import argparse
import subprocess
import sys
import os
from pathlib import Path
import json
import time


def run_command(cmd, description, capture_output=True):
    """Run a command and handle the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        if capture_output:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)

            success = result.returncode == 0
        else:
            result = subprocess.run(cmd, check=False)
            success = result.returncode == 0

        execution_time = time.time() - start_time
        print(f"\nExecution time: {execution_time:.2f} seconds")

        if success:
            print(f"✅ {description} - PASSED")
        else:
            print(f"❌ {description} - FAILED (return code: {result.returncode})")

        return success, result, execution_time

    except FileNotFoundError:
        print(f"❌ {description} - FAILED (command not found)")
        return False, None, time.time() - start_time
    except Exception as e:
        print(f"❌ {description} - FAILED ({str(e)})")
        return False, None, time.time() - start_time


def check_dependencies():
    """Check if required testing dependencies are available"""
    print("Checking testing dependencies...")

    dependencies = [
        ('pytest', 'pytest --version'),
        ('pytest-cov', 'python -c "import pytest_cov"'),
        ('pytest-mock', 'python -c "import pytest_mock"')
    ]

    missing = []
    for dep_name, check_cmd in dependencies:
        success, _, _ = run_command(
            check_cmd.split() if 'python' not in check_cmd else check_cmd.split(' ', 2),
            f"Checking {dep_name}",
            capture_output=True
        )
        if not success:
            missing.append(dep_name)

    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install -r requirements-test.txt")
        return False

    print("✅ All dependencies available")
    return True


def run_unit_tests(args):
    """Run unit tests"""
    cmd = ['python', '-m', 'pytest']

    if args.fast:
        cmd.extend(['-v', 'tests/unit/'])
    else:
        cmd.extend([
            '-v',
            '--cov=lib',
            '--cov-report=term-missing',
            'tests/unit/'
        ])

    if args.markers:
        cmd.extend(['-m', args.markers])

    success, _, exec_time = run_command(cmd, "Unit Tests")
    return success, exec_time


def run_integration_tests(args):
    """Run integration tests"""
    cmd = ['python', '-m', 'pytest']

    if args.fast:
        cmd.extend(['-v', 'tests/integration/'])
    else:
        cmd.extend([
            '-v',
            '--cov=lib',
            '--cov-report=term-missing',
            '--cov-append',  # Append to coverage from unit tests
            'tests/integration/'
        ])

    if args.markers:
        cmd.extend(['-m', args.markers])

    success, _, exec_time = run_command(cmd, "Integration Tests")
    return success, exec_time


def run_cross_platform_tests(args):
    """Run cross-platform tests"""
    cmd = [
        'python', '-m', 'pytest',
        '-v',
        '-m', 'cross_platform',
        'tests/'
    ]

    if not args.fast:
        cmd.extend(['--cov=lib', '--cov-report=term-missing'])

    success, _, exec_time = run_command(cmd, "Cross-Platform Tests")
    return success, exec_time


def run_performance_tests(args):
    """Run performance benchmarks"""
    cmd = [
        'python', '-m', 'pytest',
        '-v',
        '-m', 'slow',
        '--benchmark-only',
        'tests/'
    ]

    success, _, exec_time = run_command(cmd, "Performance Tests")
    return success, exec_time


def generate_coverage_report():
    """Generate HTML coverage report"""
    cmd = [
        'python', '-m', 'coverage',
        'html',
        '--directory=htmlcov',
        '--show-contexts'
    ]

    success, _, exec_time = run_command(cmd, "Generating HTML Coverage Report")

    if success:
        print(f"📊 HTML coverage report generated in: htmlcov/index.html")

        # Also generate JSON report for CI integration
        json_cmd = [
            'python', '-m', 'coverage',
            'json',
            '--show-contexts',
            '-o', 'data/data/data/reports/coverage.json'
        ]
        run_command(json_cmd, "Generating JSON Coverage Report")

    return success, exec_time


def check_code_quality():
    """Run code quality checks"""
    quality_checks = [
        ('Black formatting', ['python', '-m', 'black', '--check', '--diff', 'lib/']),
        ('isort imports', ['python', '-m', 'isort', '--check-only', '--diff', 'lib/']),
        ('Flake8 linting', ['python', '-m', 'flake8', 'lib/', '--max-line-length=100', '--ignore=E203,W503']),
        ('MyPy type checking', ['python', '-m', 'mypy', 'lib/', '--ignore-missing-imports'])
    ]

    all_passed = True
    for check_name, cmd in quality_checks:
        success, _, _ = run_command(cmd, check_name)
        if not success:
            all_passed = False

    return all_passed


def generate_test_report(results, total_time):
    """Generate comprehensive test report"""
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'platform': {
            'system': os.name,
            'python_version': sys.version,
            'working_directory': str(Path.cwd())
        },
        'summary': {
            'total_time_seconds': round(total_time, 2),
            'all_tests_passed': all(result['success'] for result in results.values()),
            'test_suites_run': len(results)
        },
        'results': results
    }

    # Add coverage info if available
    coverage_file = Path('data/data/data/reports/coverage.json')
    if coverage_file.exists():
        try:
            with open(coverage_file, 'r') as f:
                coverage_data = json.load(f)
                report['coverage'] = {
                    'percent_covered': coverage_data.get('totals', {}).get('percent_covered', 0),
                    'files_covered': len(coverage_data.get('files', {})),
                    'missing_lines': coverage_data.get('totals', {}).get('missing_lines', 0)
                }
        except:
            pass

    # Save report
    report_file = Path('test_report.json')
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    return report


def main():
    parser = argparse.ArgumentParser(
        description='Test Runner for Autonomous Agent Plugin',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Run all tests with coverage
  %(prog)s --unit                   # Run only unit tests
  %(prog)s --integration            # Run only integration tests
  %(prog)s --fast                   # Run tests without coverage (faster)
  %(prog)s --platform               # Run cross-platform tests only
  %(prog)s --performance            # Run performance benchmarks
  %(prog)s --quality                # Run code quality checks
  %(prog)s --report                 # Generate HTML coverage report
  %(prog)s --markers "not slow"     # Skip slow tests
"""
    )

"""
    # Test selection
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    parser.add_argument('--platform', action='store_true', help='Run only cross-platform tests')
    parser.add_argument('--performance', action='store_true', help='Run performance benchmarks')
    parser.add_argument('--quality', action='store_true', help='Run code quality checks')

    # Execution options
    parser.add_argument('--fast', action='store_true', help='Run tests without coverage (faster)')
    parser.add_argument('--report', action='store_true', help='Generate HTML coverage report')
    parser.add_argument('--no-deps-check', action='store_true', help='Skip dependency checking')

    # Filtering options
    parser.add_argument('--markers', help='Pytest markers to filter tests (e.g., "not slow")')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    print("🧪 Autonomous Agent Plugin Test Runner")
    print("=" * 50)

    start_time = time.time()

    # Check dependencies
    if not args.no_deps_check:
        if not check_dependencies():
            sys.exit(1)

    results = {}

    # Run selected test suites
    if args.unit or not any([args.unit, args.integration, args.platform, args.performance]):
        success, exec_time = run_unit_tests(args)
        results['unit_tests'] = {'success': success, 'execution_time': exec_time}
        if not success and not args.integration:
            print("❌ Unit tests failed - stopping execution")
            sys.exit(1)

    if args.integration or not any([args.unit, args.integration, args.platform, args.performance]):
        success, exec_time = run_integration_tests(args)
        results['integration_tests'] = {'success': success, 'execution_time': exec_time}

    if args.platform:
        success, exec_time = run_cross_platform_tests(args)
        results['cross_platform_tests'] = {'success': success, 'execution_time': exec_time}

    if args.performance:
        success, exec_time = run_performance_tests(args)
        results['performance_tests'] = {'success': success, 'execution_time': exec_time}

    # Run code quality checks
    if args.quality:
        success, exec_time = run_command(
            ['python', 'run_tests.py', '--quality-only'],
            "Code Quality Checks",
            capture_output=False
        )
        results['code_quality'] = {'success': success, 'execution_time': exec_time}

    # Generate coverage report
    if args.report and not args.fast:
        success, exec_time = generate_coverage_report()
        results['coverage_report'] = {'success': success, 'execution_time': exec_time}

    total_time = time.time() - start_time

    # Generate comprehensive report
    report = generate_test_report(results, total_time)

    # Print summary
    print(f"\n{'='*60}")
    print("🏁 TEST EXECUTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"All tests passed: {'✅ YES' if report['summary']['all_tests_passed'] else '❌ NO'}")
    print(f"Test suites run: {report['summary']['test_suites_run']}")

    for suite_name, result in results.items():
        status = '✅ PASSED' if result['success'] else '❌ FAILED'
        print(f"  {suite_name}: {status} ({result['execution_time']:.2f}s)")

    if 'coverage' in report:
        print(f"Coverage: {report['coverage']['percent_covered']:.1f}%")

    print(f"\n📄 Detailed report saved to: test_report.json")
    if args.report and not args.fast:
        print(f"📊 HTML coverage report: htmlcov/index.html")

    # Exit with appropriate code
    sys.exit(0 if report['summary']['all_tests_passed'] else 1)


if __name__ == '__main__':
    main()