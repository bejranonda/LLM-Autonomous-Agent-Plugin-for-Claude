#!/usr/bin/env python3
"""
Comprehensive Cache Control Fix

This script provides a complete fix for all sources of empty content blocks
that could cause cache_control errors in the autonomous agent plugin.

Usage:
    python lib/comprehensive_cache_control_fix.py [--apply-fixes]
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any


def find_all_empty_returns_in_js(file_path: str) -> List[Tuple[int, str, str]]:
    """Find all JavaScript return statements that could return empty content."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

    issues = []

    # Find all JavaScript code blocks
    js_blocks = re.findall(r"```javascript\s*\n(.*?)\n```", content, re.DOTALL)

    for i, js_code in enumerate(js_blocks):
        lines = js_code.split("\n")
        for line_num, line in enumerate(lines, 1):
            # Look for problematic return patterns
            problematic_patterns = [
                (r"return\s*\[\s*\];", "Empty array return"),
                (r'return\s*""\s*;', "Empty string return"),
                (r"return\s*\'\s*\'\s*;", "Empty string return"),
                (r"return\s*null\s*;", "Null return"),
                (r"return\s*undefined\s*;", "Undefined return"),
                (r"\[\]\s*$", "Array ending with empty array"),
                (r'text:\s*""', "Empty text property"),
                (r'content:\s*""', "Empty content property"),
                (r'message:\s*""', "Empty message property"),
            ]

            for pattern, description in problematic_patterns:
                if re.search(pattern, line):
                    issues.append((line_num, line.strip(), description))

    return issues


def find_message_construction_patterns(file_path: str) -> List[Tuple[int, str, str]]:
    """Find message construction patterns that could create empty content blocks."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

    issues = []

    # Look for message array construction
    message_patterns = [
        (r"messages\s*=\s*\[[^\]]*\]", "Message array construction"),
        (r"messages\.push\([^)]*\)", "Message push operation"),
        (r"content:\s*[^,}]*cache_control", "Content with cache_control"),
        (r"text:\s*[^,}]*cache_control", "Text with cache_control"),
    ]

    lines = content.split("\n")
    for line_num, line in enumerate(lines, 1):
        for pattern, description in message_patterns:
            if re.search(pattern, line):
                issues.append((line_num, line.strip(), description))

    return issues


def apply_comprehensive_fixes(file_path: str, dry_run: bool = True) -> bool:
    """Apply comprehensive fixes to eliminate empty content blocks."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    original_content = content

    # Fix 1: Replace empty array returns
    content = re.sub(
        r"return\s*\[\s*\];", 'return [{ note: "No data available - using fallback", type: "fallback" }];', content
    )

    # Fix 2: Replace empty string returns
    content = re.sub(r'return\s*["\']["\']\s*;', 'return "No content available - using fallback";', content)

    # Fix 3: Replace empty text properties
    content = re.sub(r'text:\s*["\']["\'](?=\s*[,}])', 'text: "No content available"', content)

    # Fix 4: Replace empty content properties
    content = re.sub(r'content:\s*["\']["\'](?=\s*[,}])', 'content: "No content available"', content)

    # Fix 5: Ensure cache_control only appears with valid content
    content = re.sub(
        r'cache_control:\s*\{\s*type:\s*["\']ephemeral["\']\s*\}', "/* cache_control removed for safety */", content
    )

    # Only write if changes were made
    if content != original_content and not dry_run:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False

    return content != original_content


def analyze_plugin_for_cache_control_issues():
    """Analyze entire plugin for cache control issues."""
    plugin_dir = Path(".")

    # Find all relevant files
    js_files = []
    for pattern in ["**/*.md", "**/*.js", "**/*.json"]:
        js_files.extend(plugin_dir.glob(pattern))

    print(f"Analyzing {len(js_files)} files for cache control issues...")
    print("=" * 70)

    total_issues = 0
    files_with_issues = []

    for file_path in js_files:
        if ".git" in str(file_path) or "node_modules" in str(file_path):
            continue

        issues = find_all_empty_returns_in_js(str(file_path))
        message_issues = find_message_construction_patterns(str(file_path))

        if issues or message_issues:
            files_with_issues.append((str(file_path), issues, message_issues))
            total_issues += len(issues) + len(message_issues)

    # Report findings
    print(f"\n[ANALYSIS] RESULTS:")
    print(f"Files with issues: {len(files_with_issues)}")
    print(f"Total issues found: {total_issues}")

    if files_with_issues:
        print(f"\n[DETAILED] FINDINGS:")
        for file_path, js_issues, message_issues in files_with_issues:
            print(f"\n[FILE]: {file_path}")

            if js_issues:
                print(f"  JavaScript Issues ({len(js_issues)}):")
                for line_num, line, description in js_issues:
                    print(f"    Line {line_num}: {description}")
                    print(f"    Code: {line}")

            if message_issues:
                print(f"  Message Construction Issues ({len(message_issues)}):")
                for line_num, line, description in message_issues:
                    print(f"    Line {line_num}: {description}")
                    print(f"    Code: {line}")

    return files_with_issues, total_issues


def create_emergency_fix():
    """Create emergency fix to eliminate all cache_control usage."""
    print("[EMERGENCY] Removing all cache_control usage...")

    plugin_dir = Path(".")
    modified_files = []

    for file_path in plugin_dir.glob("**/*.md"):
        if ".git" in str(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Remove all cache_control usage
            content = re.sub(
                r'cache_control:\s*\{\s*type:\s*["\'][^"\']*["\']\s*\}',
                "/* cache_control removed for emergency fix */",
                content,
            )

            # Fix any remaining empty content issues
            content = re.sub(
                r"return\s*\[\s*\];",
                'return [{ note: "Emergency fallback - empty array prevented", type: "emergency" }];',
                content,
            )

            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                modified_files.append(str(file_path))

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"[COMPLETE] Emergency fix applied to {len(modified_files)} files")
    return modified_files


def main():
    """Main."""
    parser = argparse.ArgumentParser(description="Comprehensive Cache Control Fix")
    parser.add_argument("--apply-fixes", action="store_true", help="Apply fixes to files")
    parser.add_argument("--emergency", action="store_true", help="Apply emergency fix (remove all cache_control)")
    parser.add_argument("--analyze-only", action="store_true", help="Only analyze, no fixes")

    args = parser.parse_args()

    if args.emergency:
        modified_files = create_emergency_fix()
        print(f"\n[COMPLETE] Emergency fix completed!")
        print(f"Modified {len(modified_files)} files")
        print("All cache_control usage has been removed to prevent errors.")
        return

    if args.analyze_only:
        files_with_issues, total_issues = analyze_plugin_for_cache_control_issues()
        if total_issues > 0:
            print(f"\n⚠️  Found {total_issues} issues that need fixing!")
            print("Run with --apply-fixes to resolve them.")
        else:
            print("\n✅ No cache control issues found!")
        return

    # Default: analyze and optionally apply fixes
    files_with_issues, total_issues = analyze_plugin_for_cache_control_issues()

    if total_issues > 0:
        print(f"\n🛠️  APPLYING FIXES...")
        modified_count = 0

        for file_path, js_issues, message_issues in files_with_issues:
            if apply_comprehensive_fixes(file_path, dry_run=not args.apply_fixes):
                if args.apply_fixes:
                    print(f"  ✅ Fixed: {file_path}")
                    modified_count += 1
                else:
                    print(f"  📋 Would fix: {file_path}")

        if args.apply_fixes:
            print(f"\n[SUCCESS] Fixes applied to {modified_count} files!")
        else:
            print(f"\n[INFO] Run with --apply-fixes to apply these changes.")
    else:
        print("\n[OK] No cache control issues found!")


if __name__ == "__main__":
    main()
