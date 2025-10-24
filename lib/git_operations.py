#!/usr/bin/env python3
"""
Git Operations Utility Library

Provides helper functions for Git operations including:
- Version bumping with semantic versioning
- Conventional commit message generation
- Release notes creation from commits
- Repository state validation
- Version format detection and parsing
- Multi-platform compatibility (Windows, Linux, Mac)

Version: 1.0.0
Author: Autonomous Agent Plugin
"""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class GitError(Exception):
    """Base exception for Git-related errors"""
    pass


class SemanticVersion:
    """Semantic version handler supporting multiple formats"""

    def __init__(self, version_string: str):
        """
        Parse version string into components.

        Supports formats:
        - Semantic: 1.2.3, v1.2.3
        - Pre-release: 1.2.3-alpha.1, 1.2.3-beta.2
        - Build metadata: 1.2.3+build.123
        - Calendar: 2025.01.24
        """
        self.original = version_string
        self.prefix = ''
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.prerelease = ''
        self.build = ''

        self._parse(version_string)

    def _parse(self, version_string: str):
        """Parse version string into components"""
        # Remove 'v' prefix if present
        if version_string.startswith('v'):
            self.prefix = 'v'
            version_string = version_string[1:]

        # Split build metadata
        if '+' in version_string:
            version_string, self.build = version_string.split('+', 1)

        # Split pre-release
        if '-' in version_string:
            version_string, self.prerelease = version_string.split('-', 1)

        # Parse version numbers
        parts = version_string.split('.')
        if len(parts) >= 1:
            self.major = int(parts[0])
        if len(parts) >= 2:
            self.minor = int(parts[1])
        if len(parts) >= 3:
            self.patch = int(parts[2])

    def bump_major(self) -> 'SemanticVersion':
        """Bump major version (X.0.0)"""
        return SemanticVersion(f"{self.prefix}{self.major + 1}.0.0")

    def bump_minor(self) -> 'SemanticVersion':
        """Bump minor version (x.Y.0)"""
        return SemanticVersion(f"{self.prefix}{self.major}.{self.minor + 1}.0")

    def bump_patch(self) -> 'SemanticVersion':
        """Bump patch version (x.y.Z)"""
        return SemanticVersion(f"{self.prefix}{self.major}.{self.minor}.{self.patch + 1}")

    def __str__(self) -> str:
        """String representation of version"""
        version = f"{self.prefix}{self.major}.{self.minor}.{self.patch}"

        if self.prerelease:
            version += f"-{self.prerelease}"

        if self.build:
            version += f"+{self.build}"

        return version

    def __repr__(self) -> str:
        return f"SemanticVersion('{str(self)}')"


def run_git_command(args: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    """
    Run a Git command and return the result.

    Args:
        args: List of command arguments (e.g., ['status', '--short'])
        cwd: Working directory (defaults to current directory)

    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        cmd = ['git'] + args
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        raise GitError(f"Git command timed out: {' '.join(args)}")
    except FileNotFoundError:
        raise GitError("Git is not installed or not in PATH")
    except Exception as e:
        raise GitError(f"Failed to run git command: {e}")


def get_current_version(version_file: Optional[Path] = None) -> str:
    """
    Get current version from Git tags or version file.

    Args:
        version_file: Path to version file (optional)

    Returns:
        Current version string (e.g., "v1.2.3")
    """
    # Try to get version from Git tags
    returncode, stdout, _ = run_git_command(['describe', '--tags', '--abbrev=0'])

    if returncode == 0 and stdout:
        return stdout

    # Try to read from version file
    if version_file and version_file.exists():
        content = version_file.read_text()

        # Try to find version pattern
        match = re.search(r'version["\s:=]+([0-9]+\.[0-9]+\.[0-9]+)', content)
        if match:
            return match.group(1)

    return "0.0.0"


def detect_version_format(version_string: str) -> str:
    """
    Detect the version format used.

    Returns:
        Format type: 'semantic', 'calendar', or 'custom'
    """
    if re.match(r'^v?[0-9]+\.[0-9]+\.[0-9]+', version_string):
        return 'semantic'
    elif re.match(r'^[0-9]{4}\.[0-9]{2}\.[0-9]{2}', version_string):
        return 'calendar'
    else:
        return 'custom'


def version_bump(current_version: str, bump_type: str) -> str:
    """
    Bump version based on type.

    Args:
        current_version: Current version string
        bump_type: 'major', 'minor', or 'patch'

    Returns:
        New version string
    """
    version = SemanticVersion(current_version)

    if bump_type == 'major':
        return str(version.bump_major())
    elif bump_type == 'minor':
        return str(version.bump_minor())
    elif bump_type == 'patch':
        return str(version.bump_patch())
    else:
        raise ValueError(f"Invalid bump type: {bump_type}. Use 'major', 'minor', or 'patch'")


def detect_version_bump_from_commits(since: Optional[str] = None) -> str:
    """
    Detect appropriate version bump from commit messages.

    Analyzes commit messages using conventional commits format:
    - Breaking changes → major
    - New features → minor
    - Bug fixes, docs, etc. → patch

    Args:
        since: Git ref to analyze from (defaults to last tag)

    Returns:
        Bump type: 'major', 'minor', or 'patch'
    """
    # Get range
    if since is None:
        returncode, since, _ = run_git_command(['describe', '--tags', '--abbrev=0'])
        if returncode != 0:
            since = 'HEAD~10'  # Default to last 10 commits

    # Get commits
    returncode, commits, _ = run_git_command(['log', '--oneline', f'{since}..HEAD'])

    if returncode != 0:
        return 'patch'

    # Check for breaking changes
    breaking_patterns = [
        r'BREAKING[\s:-]',
        r'breaking[\s:-]',
        r'!:',  # Conventional commits breaking change indicator
    ]

    for pattern in breaking_patterns:
        if re.search(pattern, commits, re.IGNORECASE):
            return 'major'

    # Check for features
    feature_patterns = [
        r'^[a-f0-9]+\s+feat[\(:]',
        r'^[a-f0-9]+\s+feature[\(:]',
    ]

    for pattern in feature_patterns:
        if re.search(pattern, commits, re.MULTILINE | re.IGNORECASE):
            return 'minor'

    # Default to patch
    return 'patch'


def conventional_commit_message(
    commit_type: str,
    scope: str,
    description: str,
    body: Optional[str] = None,
    footer: Optional[str] = None
) -> str:
    """
    Generate a conventional commit message.

    Format:
    <type>(<scope>): <description>

    [optional body]

    [optional footer]

    Args:
        commit_type: Type (feat, fix, docs, etc.)
        scope: Scope of change
        description: Short description
        body: Detailed description (optional)
        footer: Footer (breaking changes, issues, etc.)

    Returns:
        Formatted commit message
    """
    message = f"{commit_type}({scope}): {description}"

    if body:
        message += f"\n\n{body}"

    if footer:
        message += f"\n\n{footer}"

    return message


def generate_changelog(since: Optional[str] = None, until: str = 'HEAD') -> str:
    """
    Generate changelog from commits.

    Categorizes commits by type:
    - Added: feat commits
    - Fixed: fix commits
    - Changed: refactor, perf commits
    - Documentation: docs commits

    Args:
        since: Git ref to start from (defaults to last tag)
        until: Git ref to end at (defaults to HEAD)

    Returns:
        Formatted changelog markdown
    """
    # Get range
    if since is None:
        returncode, since, _ = run_git_command(['describe', '--tags', '--abbrev=0'])
        if returncode != 0:
            since = 'HEAD~10'

    # Get commits with full messages
    returncode, log, _ = run_git_command([
        'log',
        '--pretty=format:%s',
        f'{since}..{until}'
    ])

    if returncode != 0:
        return "No changes found."

    # Categorize commits
    categories = {
        'Added': [],
        'Fixed': [],
        'Changed': [],
        'Documentation': [],
        'Other': []
    }

    for line in log.split('\n'):
        if not line:
            continue

        # Parse commit message
        if re.match(r'^feat[\(:]', line, re.IGNORECASE):
            categories['Added'].append(line)
        elif re.match(r'^fix[\(:]', line, re.IGNORECASE):
            categories['Fixed'].append(line)
        elif re.match(r'^(refactor|perf)[\(:]', line, re.IGNORECASE):
            categories['Changed'].append(line)
        elif re.match(r'^docs[\(:]', line, re.IGNORECASE):
            categories['Documentation'].append(line)
        else:
            categories['Other'].append(line)

    # Generate markdown
    changelog = f"## [{until}] - {datetime.now().strftime('%Y-%m-%d')}\n\n"

    for category, commits in categories.items():
        if commits:
            changelog += f"### {category}\n"
            for commit in commits:
                # Clean up commit message
                cleaned = re.sub(r'^[a-z]+(\([^)]+\))?:\s*', '', commit, flags=re.IGNORECASE)
                changelog += f"- {cleaned}\n"
            changelog += "\n"

    return changelog


def create_release_notes(version: str, changelog: str) -> str:
    """
    Create release notes from changelog.

    Args:
        version: Version string
        changelog: Changelog markdown

    Returns:
        Formatted release notes
    """
    release_notes = f"# Release {version}\n\n"
    release_notes += f"Released on {datetime.now().strftime('%Y-%m-%d')}\n\n"
    release_notes += changelog

    return release_notes


def validate_repository_state() -> Dict[str, bool]:
    """
    Validate Git repository state before release.

    Returns:
        Dictionary of validation results
    """
    results = {}

    # Check if working directory is clean
    returncode, status, _ = run_git_command(['status', '--porcelain'])
    results['clean_working_directory'] = (returncode == 0 and not status)

    # Check if on a branch
    returncode, branch, _ = run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'])
    results['on_branch'] = (returncode == 0 and branch != 'HEAD')

    # Check if remote exists
    returncode, remote, _ = run_git_command(['remote', 'get-url', 'origin'])
    results['has_remote'] = (returncode == 0 and bool(remote))

    # Check if ahead of remote
    if results['on_branch'] and results['has_remote']:
        returncode, ahead, _ = run_git_command([
            'rev-list',
            '--count',
            f'origin/{branch}..HEAD'
        ])
        results['ahead_of_remote'] = (returncode == 0 and ahead == '0')
    else:
        results['ahead_of_remote'] = False

    return results


def get_last_release_info() -> Dict[str, str]:
    """
    Get information about the last release.

    Returns:
        Dictionary with tag, date, and commit info
    """
    # Get last tag
    returncode, tag, _ = run_git_command(['describe', '--tags', '--abbrev=0'])

    if returncode != 0:
        return {
            'tag': 'No previous release',
            'date': 'N/A',
            'commit': 'N/A'
        }

    # Get tag date
    returncode, date, _ = run_git_command([
        'log',
        '-1',
        '--format=%ai',
        tag
    ])

    # Get tag commit
    returncode, commit, _ = run_git_command([
        'rev-parse',
        '--short',
        tag
    ])

    return {
        'tag': tag,
        'date': date.split()[0] if date else 'N/A',
        'commit': commit if commit else 'N/A'
    }


def get_commit_count_since(since: str) -> int:
    """
    Get number of commits since a reference.

    Args:
        since: Git ref to count from

    Returns:
        Number of commits
    """
    returncode, count, _ = run_git_command([
        'rev-list',
        '--count',
        f'{since}..HEAD'
    ])

    if returncode == 0 and count:
        return int(count)

    return 0


def main():
    """CLI interface for testing"""
    import argparse

    parser = argparse.ArgumentParser(description='Git operations utility')
    parser.add_argument('--current-version', action='store_true',
                        help='Get current version')
    parser.add_argument('--detect-bump', action='store_true',
                        help='Detect version bump from commits')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'],
                        help='Bump version')
    parser.add_argument('--changelog', action='store_true',
                        help='Generate changelog')
    parser.add_argument('--validate', action='store_true',
                        help='Validate repository state')
    parser.add_argument('--version', default=None,
                        help='Version string for operations')

    args = parser.parse_args()

    try:
        if args.current_version:
            version = get_current_version()
            print(f"Current version: {version}")

        elif args.detect_bump:
            bump = detect_version_bump_from_commits()
            print(f"Recommended bump: {bump}")

        elif args.bump:
            current = args.version or get_current_version()
            new_version = version_bump(current, args.bump)
            print(f"New version: {new_version}")

        elif args.changelog:
            changelog = generate_changelog()
            print(changelog)

        elif args.validate:
            results = validate_repository_state()
            print("Repository validation:")
            for key, value in results.items():
                status = "✅" if value else "❌"
                print(f"  {status} {key.replace('_', ' ').title()}")

        else:
            parser.print_help()

    except GitError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
