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
    """Represents a semantic version with parsing and comparison capabilities"""

    def __init__(self, version_string: str):
        self.version_string = version_string
        self.major, self.minor, self.patch = self._parse_version(version_string)

    def _parse_version(self, version_string: str) -> Tuple[int, int, int]:
        """Parse version string into major, minor, patch components"""
        match = re.match(r'v?(\d+)\.(\d+)\.(\d+)', version_string)
        if not match:
            raise ValueError(f"Invalid version format: {version_string}")
        return int(match.group(1)), int(match.group(2)), int(match.group(3))

    def bump_major(self) -> 'SemanticVersion':
        """Return a new version with bumped major version"""
        return SemanticVersion(f"{self.major + 1}.0.0")

    def bump_minor(self) -> 'SemanticVersion':
        """Return a new version with bumped minor version"""
        return SemanticVersion(f"{self.major}.{self.minor + 1}.0")

    def bump_patch(self) -> 'SemanticVersion':
        """Return a new version with bumped patch version"""
        return SemanticVersion(f"{self.major}.{self.minor}.{self.patch + 1}")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other: 'SemanticVersion') -> bool:
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)


def run_git_command(command: List[str], cwd: Optional[str] = None) -> str:
    """Run a git command and return the output"""
    try:
        result = subprocess.run(
            ['git'] + command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise GitError(f"Git command failed: {' '.join(command)}\nError: {e.stderr}")


def get_current_version(cwd: Optional[str] = None) -> SemanticVersion:
    """Get the current version from git tags"""
    try:
        # Get the latest tag
        tag = run_git_command(['describe', '--tags', '--abbrev=0'], cwd)
        return SemanticVersion(tag)
    except GitError:
        # No tags found, return default version
        return SemanticVersion("1.0.0")


def generate_release_notes(
    from_version: Optional[SemanticVersion] = None,
    to_version: Optional[SemanticVersion] = None,
    cwd: Optional[str] = None
) -> str:
    """Generate release notes from git commit history"""
    try:
        # Get commit history
        if from_version and to_version:
            commits = run_git_command([
                'log', f'{from_version}..{to_version}', '--oneline'
            ], cwd)
        else:
            commits = run_git_command(['log', '--oneline', '-10'], cwd)

        # Parse commits and categorize
        features = []
        fixes = []
        other = []

        for line in commits.split('\n'):
            if line.strip():
                commit_hash, *message_parts = line.split(' ', 1)
                message = ' '.join(message_parts) if message_parts else ''

                if any(keyword in message.lower() for keyword in ['feat', 'feature']):
                    features.append(f"- {message}")
                elif any(keyword in message.lower() for keyword in ['fix', 'bugfix']):
                    fixes.append(f"- {message}")
                else:
                    other.append(f"- {message}")

        # Generate release notes
        notes = []
        if features:
            notes.append("### Features\n" + '\n'.join(features))
        if fixes:
            notes.append("### Bug Fixes\n" + '\n'.join(fixes))
        if other:
            notes.append("### Other Changes\n" + '\n'.join(other))

        return '\n\n'.join(notes) if notes else "No changes found."

    except GitError as e:
        return f"Error generating release notes: {e}"


def create_conventional_commit(
    message: str,
    type_: str = "feat",
    scope: Optional[str] = None,
    breaking: bool = False
) -> str:
    """Create a conventional commit message"""
    commit_type = type_
    commit_scope = f"({scope})" if scope else ""
    breaking_marker = "!" if breaking else ""
    commit_header = f"{commit_type}{commit_scope}{breaking_marker}: {message}"

    return commit_header


def is_repository_clean(cwd: Optional[str] = None) -> bool:
    """Check if the git repository is clean (no uncommitted changes)"""
    try:
        output = run_git_command(['status', '--porcelain'], cwd)
        return len(output.strip()) == 0
    except GitError:
        return False


def get_git_branch(cwd: Optional[str] = None) -> str:
    """Get the current git branch name"""
    try:
        return run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'], cwd)
    except GitError:
        return "unknown"


def get_git_remote_url(cwd: Optional[str] = None) -> str:
    """Get the git remote URL"""
    try:
        return run_git_command(['config', '--get', 'remote.origin.url'], cwd)
    except GitError:
        return "unknown"


def validate_repository_state(cwd: Optional[str] = None) -> Dict[str, any]:
    """Validate the repository state and return information"""
    return {
        "is_clean": is_repository_clean(cwd),
        "current_branch": get_git_branch(cwd),
        "remote_url": get_git_remote_url(cwd),
        "current_version": str(get_current_version(cwd)),
        "has_commits": bool(run_git_command(['log', '--oneline', '-1'], cwd) if not GitError else None)
    }


def main():
    """Example usage of git operations"""
    print("Git Operations Utility")
    print("=" * 30)

    try:
        # Show repository state
        state = validate_repository_state()
        print(f"Current branch: {state['current_branch']}")
        print(f"Current version: {state['current_version']}")
        print(f"Repository clean: {state['is_clean']}")

        # Generate release notes
        print("\nRecent changes:")
        print(generate_release_notes())

    except GitError as e:
        print(f"Git operation failed: {e}")


if __name__ == "__main__":
    main()