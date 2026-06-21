#!/usr/bin/env python3
# Claude Plugin Validator - Quick validation against official guidelines
import json
import yaml
import re
import sys
from pathlib import Path


def validate_plugin_manifest(manifest_path):
    """Validate plugin manifest specifically."""
    issues = []
    warnings = []

    print("Validating Plugin Manifest...")

    if not manifest_path.exists():
        issues.append("Missing plugin manifest: .claude-plugin/plugin.json")
        return issues, warnings

    # Check encoding
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        issues.append("Plugin manifest encoding error (must be UTF-8)")
        return issues, warnings

    # JSON syntax
    try:
        manifest = json.loads(content)
        print("  [OK] JSON syntax: Valid")
    except json.JSONDecodeError as e:
        issues.append(f"Plugin manifest JSON error: {e}")
        return issues, warnings

    # Required fields
    required_fields = ["name", "version", "description", "author"]
    missing_fields = [field for field in required_fields if field not in manifest]
    if missing_fields:
        issues.append(f"Missing required fields: {missing_fields}")
    else:
        print("  [OK] Required fields: Present")

    # Version format
    if "version" in manifest:
        version = str(manifest["version"])
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            issues.append(f"Invalid version format: {version} (use x.y.z)")
        else:
            print(f"  [OK] Version: {version}")

    # Name validation
    if "name" in manifest:
        name = str(manifest["name"])
        if not name or len(name.strip()) == 0:
            issues.append("Plugin name cannot be empty")
        elif re.search(r'[<>:"/\\|?*]', name):
            issues.append("Plugin name contains invalid characters")
        else:
            print(f"  [OK] Name: {name}")

    # Description
    if "description" in manifest:
        desc = str(manifest["description"])
        if len(desc) < 10:
            warnings.append("Plugin description too short (< 10 chars)")
        elif len(desc) > 2000:
            warnings.append("Plugin description too long (> 2000 chars)")
        else:
            print(f"  [OK] Description: {len(desc)} chars")

    print(f"  [OK] File size: {manifest_path.stat().st_size} bytes")

    return issues, warnings


def validate_directory_structure(plugin_dir):
    """Validate directory structure."""
    print("\nValidating Directory Structure...")

    issues = []
    warnings = []

    # Required directories
    required_dirs = [".claude-plugin"]

    for dir_name in required_dirs:
        dir_path = plugin_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"  [OK] {dir_name}/: Present")
        else:
            issues.append(f"Missing required directory: {dir_name}/")

    # Check plugin manifest specifically
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if manifest_path.exists():
        print("  [OK] plugin.json: Found")
    else:
        issues.append("Missing plugin.json in .claude-plugin/")

    # Optional directories. Glob patterns are recursive where components live in
    # subdirectories (commands/<category>/*.md, skills/<name>/SKILL.md) so the
    # count reflects actual files, not just top-level directory entries.
    optional_dirs = {
        "agents": "*.md",
        "skills": "**/SKILL.md",
        "commands": "**/*.md",
        "lib": "*.py",
        "patterns": "*",
    }
    for dir_name, pattern in optional_dirs.items():
        dir_path = plugin_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            file_count = len(list(dir_path.glob(pattern)))
            print(f"  [OK] {dir_name}/: {file_count} files (optional)")
        else:
            print(f"  [INFO] {dir_name}/: Not present (optional)")

    return issues, warnings


def validate_marketplace_sync(plugin_dir):
    """Validate that marketplace.json's listed version matches plugin.json.

    marketplace.json is the listing shown when browsing/installing from a
    marketplace, but nothing enforces that its version field tracks
    plugin.json - it has drifted silently in the past (e.g. stuck at 8.0.0
    for nine releases). This check makes that drift visible instead of silent.
    """
    issues = []
    warnings = []

    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    marketplace_path = plugin_dir / ".claude-plugin" / "marketplace.json"

    if not marketplace_path.exists():
        return issues, warnings

    print("\nValidating Marketplace Sync...")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        warnings.append(f"Could not read plugin.json/marketplace.json for sync check: {e}")
        return issues, warnings

    plugin_name = manifest.get("name")
    plugin_version = str(manifest.get("version", ""))

    entry = next((p for p in marketplace.get("plugins", []) if p.get("name") == plugin_name), None)
    if entry is None:
        warnings.append(f"marketplace.json has no listing for plugin '{plugin_name}'")
        return issues, warnings

    listed_version = str(entry.get("version", ""))
    if listed_version != plugin_version:
        warnings.append(
            f"marketplace.json version ({listed_version}) does not match "
            f"plugin.json version ({plugin_version}) - update marketplace.json"
        )
    else:
        print(f"  [OK] marketplace.json version matches plugin.json: {plugin_version}")

    return issues, warnings


def validate_file_formats(plugin_dir):
    """Validate file formats."""
    print("\nValidating File Formats...")

    issues = []
    warnings = []

    total_files = 0
    valid_files = 0

    # Check markdown files with YAML
    for md_file in plugin_dir.glob("**/*.md"):
        total_files += 1

        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Check YAML frontmatter
            if content.startswith("---"):
                try:
                    frontmatter_end = content.find("---", 3)
                    if frontmatter_end == -1:
                        warnings.append(f"Unclosed YAML frontmatter: {md_file.name}")
                        continue

                    frontmatter_str = content[3:frontmatter_end].strip()
                    yaml.safe_load(frontmatter_str)
                    valid_files += 1

                except yaml.YAMLError as e:
                    warnings.append(f"YAML error in {md_file.name}: {str(e)[:50]}")
            else:
                valid_files += 1

        except UnicodeDecodeError:
            issues.append(f"Invalid encoding: {md_file.name}")

    print(f"  [OK] Markdown files: {valid_files}/{total_files} valid")

    return issues, warnings


def main():
    """Main validation function."""
    print("Claude Plugin Validator - Official Guidelines Compliance")
    print("=" * 60)

    plugin_dir = Path(".")
    all_issues = []
    all_warnings = []

    # Run validations
    issues, warnings = validate_plugin_manifest(plugin_dir / ".claude-plugin" / "plugin.json")
    all_issues.extend(issues)
    all_warnings.extend(warnings)

    issues, warnings = validate_directory_structure(plugin_dir)
    all_issues.extend(issues)
    all_warnings.extend(warnings)

    issues, warnings = validate_marketplace_sync(plugin_dir)
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    issues, warnings = validate_file_formats(plugin_dir)
    all_issues.extend(issues)
    all_warnings.extend(warnings)

    # Results
    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)

    if all_issues:
        print("\nCRITICAL ISSUES (Installation Blockers):")
        for issue in all_issues:
            print(f"  [FAIL] {issue}")

    if all_warnings:
        print("\nWARNINGS:")
        for warning in all_warnings[:5]:  # Show first 5
            print(f"  [WARN] {warning}")
        if len(all_warnings) > 5:
            print(f"  [WARN] ... and {len(all_warnings) - 5} more warnings")

    # Final status
    if not all_issues:
        if not all_warnings:
            print("\n[SUCCESS] Plugin validation PASSED - Ready for release!")
            print("Status: PERFECT - No issues found")
        else:
            print("\n[SUCCESS] Plugin validation PASSED - Ready for release!")
            print("Status: READY - Minor warnings only")

        print(f"\nScore: {100 - (len(all_warnings) * 2)}/100")
        return 0
    else:
        print(f"\n[FAIL] Plugin validation FAILED - {len(all_issues)} critical issues")
        print("Status: NEEDS FIXES before release")

        score = max(0, 100 - (len(all_issues) * 10) - (len(all_warnings) * 2))
        print(f"\nScore: {score}/100")
        return 1


if __name__ == "__main__":
    sys.exit(main())
