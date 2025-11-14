#!/usr/bin/env python3
"""Analyze coverage and identify files needing tests."""

import json
from pathlib import Path

# Read coverage data
with open('data/data/data/reports/coverage.json') as f:
    data = json.load(f)

print("[COVERAGE ANALYSIS]")
print(f"Total Coverage: {data['totals']['percent_covered']:.2f}%")
print(f"Target: 80.00%")
print(f"Gap: {80.00 - data['totals']['percent_covered']:.2f}%\n")

# Find files with low coverage
low_coverage_files = []
for file_path, info in data['files'].items():
    if not file_path.startswith('lib\\'):
        continue

    coverage = info['summary']['percent_covered']
    if coverage < 80:
        low_coverage_files.append({
            'path': file_path,
            'coverage': coverage,
            'missing_lines': info['summary']['missing_lines'],
            'total_lines': info['summary']['num_statements']
        })

# Sort by coverage (lowest first) - prioritize files with most impact
low_coverage_files.sort(key=lambda x: (x['coverage'], -x['total_lines']))

print("[TOP 30 FILES NEEDING TESTS (sorted by coverage, then size)]")
print(f"{'File':<50} {'Coverage':<12} {'Missing/Total Lines'}")
print("-" * 90)

for item in low_coverage_files[:30]:
    file_name = Path(item['path']).name
    coverage_str = f"{item['coverage']:.1f}%"
    lines_str = f"{item['missing_lines']}/{item['total_lines']}"
    print(f"{file_name:<50} {coverage_str:<12} {lines_str}")

print(f"\nTotal files with <80% coverage: {len(low_coverage_files)}")
