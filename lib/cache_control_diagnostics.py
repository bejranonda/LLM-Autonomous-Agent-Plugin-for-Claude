#!/usr/bin/env python3
"""
Cache Control Error Diagnostic Tool

This script helps identify the source of "cache_control cannot be set for empty text blocks" errors
by analyzing all JavaScript code blocks in the plugin and simulating their execution.

Usage:
    python lib/cache_control_diagnostics.py [--directory PATH] [--verbose]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

def extract_javascript_blocks(file_path: str) -> List[Tuple[int, str]]:
    """Extract JavaScript code blocks from markdown file with line numbers."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

    # Pattern to match ```javascript``` code blocks
    pattern = r'```javascript\s*\n(.*?)\n```'
    blocks = []

    for match in re.finditer(pattern, content, re.DOTALL):
        # Calculate line number
        line_before_match = content[:match.start()].count('\n')
        start_line = line_before_match + 1
        js_code = match.group(1).strip()
        blocks.append((start_line, js_code))

    return blocks

def analyze_cache_control_patterns(js_code: str) -> Dict[str, Any]:
    """Analyze JavaScript code for potential cache_control issues."""
    issues = []
    safety_measures = []

    # Check for cache_control usage
    if 'cache_control' in js_code:
        issues.append("Uses cache_control directive")

        # Check for validation before cache_control
        if not any(pattern in js_code for pattern in [
            'validateContentForCaching',
            'safeExecuteOperation',
            'validateCacheContent',
            'content && content.trim().length > 0',
            'String(content).trim().length > 0',
            'content && typeof content === "string" && content.trim().length > 0'
        ]):
            issues.append("Uses cache_control without proper validation")

    # Check for safe patterns
    if any(pattern in js_code for pattern in [
        'validateContentForCaching',
        'safeExecuteOperation',
        'fallback',
        'else.*text.*:',
        'return.*fallback'
    ]):
        safety_measures.append("Has fallback content mechanisms")

    # Check for dangerous patterns that could create empty content
    dangerous_patterns = [
        (r'content:\s*["\']\s*["\']', "Empty string literal"),
        (r'content:\s*""', "Empty string literal"),
        (r'content:\s*undefined', "undefined content"),
        (r'content:\s*null', "null content"),
        (r'text:\s*["\']\s*["\']', "Empty text property"),
        (r'text:\s*""', "Empty text property"),
        (r'text:\s*undefined', "undefined text"),
        (r'text:\s*null', "null text"),
        (r'messages\.push\(\s*\{\s*type:\s*["\']text["\'],?\s*\}', "Empty message object"),
        (r'cache_control:\s*\{\s*type:\s*["\']ephemeral["\']\s*\}', "cache_control without content")
    ]

    for pattern, description in dangerous_patterns:
        if re.search(pattern, js_code):
            issues.append(f"Potentially dangerous pattern: {description}")

    # Check for message construction patterns
    message_constructions = re.findall(r'messages\.push\(\s*\{[^}]*\}\s*\)', js_code, re.DOTALL)
    if message_constructions:
        for construction in message_constructions:
            if 'cache_control' in construction and ('text:' not in construction or 'content:' not in construction):
                issues.append("cache_control without proper text/content field")

    return {
        'issues': issues,
        'safety_measures': safety_measures,
        'message_constructions': len(message_constructions),
        'has_cache_control': 'cache_control' in js_code
    }

def simulate_content_validation(js_code: str) -> Dict[str, Any]:
    """Simulate content validation scenarios that could fail."""
    simulations = []

    # Test common scenarios that could create empty content
    test_scenarios = [
        ("undefined", None),
        ("null", None),
        ("empty string", ""),
        ("whitespace only", "   "),
        ("very short", "abc"),
        ("empty object", {}),
        ("empty array", []),
        ("string 'null'", "null"),
        ("string 'undefined'", "undefined"),
        ("string '[]'", "[]"),
    ]

    for scenario_name, value in test_scenarios:
        try:
            # Simulate the validation logic from our fixes
            if value is None:
                is_valid = False
            else:
                content_str = str(value)
                is_valid = (
                    len(content_str) > 0 and
                    len(content_str.strip()) > 0 and
                    len(content_str.strip()) >= 5 and
                    content_str.strip().lower() not in ['null', 'undefined', '[]', '{}', 'none', 'empty']
                )

            simulations.append({
                'scenario': scenario_name,
                'value': str(value),
                'is_valid': is_valid,
                'would_cause_error': not is_valid and 'cache_control' in js_code
            })
        except Exception as e:
            simulations.append({
                'scenario': scenario_name,
                'value': str(value),
                'is_valid': False,
                'error': str(e),
                'would_cause_error': True
            })

    return {
        'simulations': simulations,
        'risky_scenarios': len([s for s in simulations if s.get('would_cause_error', False)])
    }

def analyze_file(file_path: str, verbose: bool = False) -> Dict[str, Any]:
    """Analyze a single markdown file for cache_control issues."""
    js_blocks = extract_javascript_blocks(file_path)

    file_analysis = {
        'file': file_path,
        'js_blocks_count': len(js_blocks),
        'blocks': [],
        'overall_risk': 'low'
    }

    total_issues = 0
    total_risky_scenarios = 0

    for line_num, js_code in js_blocks:
        cache_analysis = analyze_cache_control_patterns(js_code)
        simulation = simulate_content_validation(js_code)

        block_analysis = {
            'line': line_num,
            'has_cache_control': cache_analysis['has_cache_control'],
            'issues': cache_analysis['issues'],
            'safety_measures': cache_analysis['safety_measures'],
            'risky_scenarios': simulation['risky_scenarios'],
            'code_preview': js_code[:200] + "..." if len(js_code) > 200 else js_code
        }

        if verbose:
            print(f"\n--- Block at line {line_num} ---")
            print(f"Uses cache_control: {cache_analysis['has_cache_control']}")
            if cache_analysis['issues']:
                print(f"Issues: {cache_analysis['issues']}")
            if cache_analysis['safety_measures']:
                print(f"Safety measures: {cache_analysis['safety_measures']}")
            print(f"Risky scenarios: {simulation['risky_scenarios']}")

        file_analysis['blocks'].append(block_analysis)
        total_issues += len(cache_analysis['issues'])
        total_risky_scenarios += simulation['risky_scenarios']

    # Determine overall risk
    if total_issues > 0 or total_risky_scenarios > 0:
        file_analysis['overall_risk'] = 'high'
    elif any(block['has_cache_control'] for block in file_analysis['blocks']):
        file_analysis['overall_risk'] = 'medium'

    return file_analysis

def main():
    parser = argparse.ArgumentParser(description='Cache Control Error Diagnostic Tool')
    parser.add_argument('--directory', '-d', default='.', help='Directory to analyze (default: current)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    args = parser.parse_args()

    # Find all markdown files
    md_files = []
    for root, dirs, files in os.walk(args.directory):
        # Skip hidden directories and common non-plugin directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]

        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))

    if not md_files:
        print("No markdown files found.")
        return

    print(f"Analyzing {len(md_files)} markdown files for cache_control issues...")
    print("=" * 60)

    all_files_analysis = []
    high_risk_files = []
    medium_risk_files = []

    for file_path in md_files:
        analysis = analyze_file(file_path, args.verbose)
        all_files_analysis.append(analysis)

        if analysis['overall_risk'] == 'high':
            high_risk_files.append(analysis)
        elif analysis['overall_risk'] == 'medium':
            medium_risk_files.append(analysis)

        if not args.json:
            risk_indicator = {
                'high': '[HIGH]',
                'medium': '[MEDIUM]',
                'low': '[LOW]'
            }[analysis['overall_risk']]

            print(f"{risk_indicator}: {file_path}")
            print(f"  JS blocks: {analysis['js_blocks_count']}")
            if analysis['overall_risk'] != 'low':
                total_issues = sum(len(block['issues']) for block in analysis['blocks'])
                total_risky = sum(block['risky_scenarios'] for block in analysis['blocks'])
                print(f"  Issues: {total_issues}, Risky scenarios: {total_risky}")

    print("\n" + "=" * 60)

    if high_risk_files:
        print(f"\n[HIGH] RISK FILES ({len(high_risk_files)}):")
        for analysis in high_risk_files:
            print(f"\n  {analysis['file']}:")
            for block in analysis['blocks']:
                if block['issues'] or block['risky_scenarios'] > 0:
                    print(f"    Line {block['line']}: {len(block['issues'])} issues, {block['risky_scenarios']} risky scenarios")
                    for issue in block['issues']:
                        print(f"      - {issue}")

    if medium_risk_files:
        print(f"\n[MEDIUM] RISK FILES ({len(medium_risk_files)}):")
        for analysis in medium_risk_files:
            print(f"  {analysis['file']}")

    # Summary
    total_blocks = sum(analysis['js_blocks_count'] for analysis in all_files_analysis)
    files_with_cache_control = sum(1 for analysis in all_files_analysis
                                 if any(block['has_cache_control'] for block in analysis['blocks']))

    print(f"\n[SUMMARY]:")
    print(f"  Total files analyzed: {len(all_files_analysis)}")
    print(f"  Total JavaScript blocks: {total_blocks}")
    print(f"  Files using cache_control: {files_with_cache_control}")
    print(f"  High risk files: {len(high_risk_files)}")
    print(f"  Medium risk files: {len(medium_risk_files)}")

    if args.json:
        output = {
            'summary': {
                'total_files': len(all_files_analysis),
                'total_js_blocks': total_blocks,
                'files_with_cache_control': files_with_cache_control,
                'high_risk_files': len(high_risk_files),
                'medium_risk_files': len(medium_risk_files)
            },
            'files': all_files_analysis
        }
        print(json.dumps(output, indent=2))

    # Return exit code based on findings
    if high_risk_files:
        sys.exit(2)  # High risk found
    elif medium_risk_files:
        sys.exit(1)  # Medium risk found
    else:
        sys.exit(0)  # All clear

if __name__ == '__main__':
    main()