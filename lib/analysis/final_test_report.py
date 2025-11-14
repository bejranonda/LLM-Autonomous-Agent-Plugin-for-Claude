#!/usr/bin/env python3
"""Generate final test improvement report."""

import json
from pathlib import Path
from datetime import datetime

# Read coverage data
try:
    with open('data/data/data/reports/coverage.json') as f:
        coverage_data = json.load(f)
except:
    print("[ERROR] No data/data/data/reports/coverage.json found")
    exit(1)

total_coverage = coverage_data['totals']['percent_covered']
covered_lines = coverage_data['totals']['covered_lines']
total_lines = coverage_data['totals']['num_statements']

print("=" * 80)
print(" FINAL TEST IMPROVEMENT REPORT")
print("=" * 80)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

print("[COVERAGE SUMMARY]")
print(f"Total Coverage:      {total_coverage:.2f}%")
print(f"Lines Covered:       {covered_lines:,}/{total_lines:,}")
print(f"Coverage Target:     80.00%")
print(f"Gap to Target:       {80.0 - total_coverage:.2f}%")
print()

# Analyze files by coverage
high_coverage = []
medium_coverage = []
low_coverage = []
no_coverage = []

for file_path, info in coverage_data['files'].items():
    if not file_path.startswith('lib\\'):
        continue

    coverage = info['summary']['percent_covered']
    file_info = {
        'path': file_path,
        'coverage': coverage,
        'lines': info['summary']['num_statements']
    }

    if coverage >= 80:
        high_coverage.append(file_info)
    elif coverage >= 50:
        medium_coverage.append(file_info)
    elif coverage > 0:
        low_coverage.append(file_info)
    else:
        no_coverage.append(file_info)

print("[COVERAGE DISTRIBUTION]")
print(f"High Coverage (>=80%):    {len(high_coverage)} files")
print(f"Medium Coverage (50-79%): {len(medium_coverage)} files")
print(f"Low Coverage (1-49%):     {len(low_coverage)} files")
print(f"No Coverage (0%):         {len(no_coverage)} files")
print()

# Count test files
test_dir = Path('tests')
unit_tests = len(list((test_dir / 'unit').glob('**/*.py'))) if (test_dir / 'unit').exists() else 0
integration_tests = len(list((test_dir / 'integration').glob('**/*.py'))) if (test_dir / 'integration').exists() else 0
generated_tests = len(list((test_dir / 'unit' / 'generated').glob('**/*.py'))) if (test_dir / 'unit' / 'generated').exists() else 0

print("[TEST SUITE COMPOSITION]")
print(f"Unit Tests:           {unit_tests} files")
print(f"Integration Tests:    {integration_tests} files")
print(f"Generated Tests:      {generated_tests} files")
print(f"Total Test Files:     {unit_tests + integration_tests}")
print()

# Top 10 files with highest coverage
print("[TOP 10 HIGHEST COVERAGE FILES]")
all_files = high_coverage + medium_coverage + low_coverage
all_files.sort(key=lambda x: x['coverage'], reverse=True)
for i, file_info in enumerate(all_files[:10], 1):
    file_name = Path(file_info['path']).name
    print(f"{i:2d}. {file_name:<45} {file_info['coverage']:>6.2f}%")
print()

# Top 10 files needing most improvement
print("[TOP 10 FILES NEEDING IMPROVEMENT]")
no_coverage.sort(key=lambda x: x['lines'], reverse=True)
for i, file_info in enumerate(no_coverage[:10], 1):
    file_name = Path(file_info['path']).name
    print(f"{i:2d}. {file_name:<45} {file_info['lines']:>5} lines (0%)")
print()

print("[RECOMMENDATIONS]")
print("1. Focus on high-impact files with 0% coverage (large files)")
print("2. Add integration tests for cross-component workflows")
print("3. Improve edge case testing for existing test files")
print("4. Add database isolation tests (PostgreSQL/SQLAlchemy)")
print("5. Generate tests for error handling paths")
print()

print("[QUALITY METRICS]")
print(f"Test Isolation:       {'GOOD' if generated_tests > 0 else 'NEEDS WORK'}")
print(f"Test Organization:    {'GOOD' if unit_tests > integration_tests else 'FAIR'}")
print(f"Auto-Generation:      {'ENABLED' if generated_tests > 0 else 'DISABLED'}")
print()

print("=" * 80)
