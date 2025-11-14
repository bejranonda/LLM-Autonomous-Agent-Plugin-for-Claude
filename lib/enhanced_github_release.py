#!/usr/bin/env python3
"""
Enhanced GitHub Release Manager for Autonomous Agent

Fixes common GitHub release publishing issues:
- Authentication failures
- API rate limiting
- Release creation failures
- Asset upload problems
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional


class EnhancedGitHubReleaseManager:
    """Enhanced GitHub release manager with robust error handling."""

    def __init__(self, repo_path: str = "."):
        """Initialize the release manager."""
        self.repo_path = Path(repo_path)
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_url = self._get_repo_url()

    def _get_repo_url(self) -> str:
        """Get GitHub repository URL from git remote."""
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"], cwd=self.repo_path, capture_output=True, text=True, check=True
            )
            url = result.stdout.strip()

            # Convert SSH to HTTPS URL for API
            if url.startswith("git@"):
                url = url.replace("git@github.com:", "https://github.com/").replace(".git", "")
            elif url.startswith("https://github.com"):
                url = url.replace(".git", "")

            return url

        except subprocess.CalledProcessError:
            print("[ERROR] Could not determine repository URL")
            print("[INFO] Make sure you're in a git repository with remote 'origin'")
            return None

    def _check_github_cli_auth(self) -> bool:
        """Check if GitHub CLI is authenticated."""
        try:
            result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, check=True)
            return "Logged in to github.com" in result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _create_release_with_gh_cli(
        self, tag: str, title: str, notes: str, prerelease: bool = False, draft: bool = False
    )-> bool:
        """ Create Release With Gh Cli."""
        """Create release using GitHub CLI (most reliable method)."""
        try:
            cmd = ["gh", "release", "create", tag, "--title", title, "--notes", notes, "--repo", self.repo_url]

            if prerelease:
                cmd.append("--prerelease")
            if draft:
                cmd.append("--draft")

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"[OK] Release created successfully with GitHub CLI")
            return True

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] GitHub CLI release failed: {e.stderr}")
            return False

    def _create_release_with_curl(
        self, tag: str, title: str, notes: str, prerelease: bool = False, draft: bool = False
    )-> bool:
        """ Create Release With Curl."""
        """Create release using curl and GitHub API (fallback method)."""
        if not self.token:
            print("[ERROR] GITHUB_TOKEN environment variable required for API method")
            return False

        # Extract owner/repo from URL
        if "github.com" in self.repo_url:
            parts = self.repo_url.split("github.com/")
            if len(parts) != 2:
                print("[ERROR] Invalid GitHub repository URL")
                return False
            owner_repo = parts[1]
        else:
            print("[ERROR] Not a GitHub repository")
            return False

        api_url = f"https://api.github.com/repos/{owner_repo}/releases"

        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }

        data = {"tag_name": tag, "name": title, "body": notes, "draft": draft, "prerelease": prerelease}

        try:
            response = requests.post(api_url, headers=headers, json=data, timeout=30)

            if response.status_code == 201:
                print(f"[OK] Release created successfully via API")
                return True
            else:
                print(f"[ERROR] API request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False

        except requests.RequestException as e:
            print(f"[ERROR] API request error: {e}")
            return False

    def _verify_release_exists(self, tag: str) -> bool:
        """Verify that the release exists on GitHub."""
        try:
            result = subprocess.run(
                ["gh", "release", "view", tag, "--repo", self.repo_url], capture_output=True, text=True, check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def create_release(
        self, tag: str, title: str, notes: str, prerelease: bool = False, draft: bool = False, verify: bool = True
    )-> bool:
        """Create Release."""
        """
        Create a GitHub release with multiple fallback methods.

        Args:
            tag: Git tag for the release
            tag: Release title
            notes: Release notes/body
            prerelease: Whether this is a prerelease
            draft: Whether to create as draft
            verify: Whether to verify release after creation

        Returns:
            True if successful, False otherwise
        """
        print(f"[START] Creating GitHub release: {tag}")
        print(f"   Repository: {self.repo_url}")
        print(f"   Title: {title}")
        print(f"   Prerelease: {prerelease}")
        print(f"   Draft: {draft}")
        print()

        # Method 1: GitHub CLI (preferred)
        if self._check_github_cli_auth():
            print("[PHONE] Using GitHub CLI...")
            if self._create_release_with_gh_cli(tag, title, notes, prerelease, draft):
                if verify and self._verify_release_exists(tag):
                    print(f"[OK] Release {tag} verified on GitHub")
                    return True
                elif not verify:
                    return True
                else:
                    print("[WARN]  Release created but verification failed")
                    return False
        else:
            print("[ERROR] GitHub CLI not authenticated")
            print("[INFO] Run: gh auth login")

        # Method 2: API fallback
        print("🌐 Trying API fallback...")
        if self._create_release_with_curl(tag, title, notes, prerelease, draft):
            if verify and self._verify_release_exists(tag):
                print(f"[OK] Release {tag} verified on GitHub")
                return True
            elif not verify:
                return True
            else:
                print("[WARN]  Release created but verification failed")
                return False

        print("[ERROR] All release methods failed")
        return False

    def auto_detect_version_and_changes(self) -> Dict[str, str]:
        """Auto-detect version and generate release notes from commits."""
        try:
            # Get current version from git tags
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"], cwd=self.repo_path, capture_output=True, text=True
            )
            last_tag = result.stdout.strip() if result.returncode == 0 else "v0.0.0"

            # Get commits since last tag
            result = subprocess.run(
                ["git", "log", f"{last_tag}..HEAD", "--oneline"], cwd=self.repo_path, capture_output=True, text=True
            )
            commits = result.stdout.strip().split("\n") if result.stdout.strip() else []

            # Simple version bump logic
            version = last_tag.replace("v", "")
            major, minor, patch = map(int, version.split("."))

            # Analyze commits for version bump
            has_features = any("feat" in commit for commit in commits)
            has_breaking = any("break" in commit.lower() or "!" in commit for commit in commits)
            has_fixes = any("fix" in commit for commit in commits)

            if has_breaking:
                major += 1
                minor = 0
                patch = 0
            elif has_features:
                minor += 1
                patch = 0
            elif has_fixes:
                patch += 1

            new_version = f"v{major}.{minor}.{patch}"

            # Generate release notes
            release_notes = f"## Changes since {last_tag}\n\n"

            if commits:
                release_notes += "### Commits\n\n"
                for commit in commits:
                    release_notes += f"- {commit}\n"
            else:
                release_notes += "No changes detected.\n"

            return {"version": new_version, "title": f"Release {new_version}", "notes": release_notes, "last_tag": last_tag}

        except Exception as e:
            print(f"[ERROR] Auto-detection failed: {e}")
            return {"version": "v1.0.0", "title": "Release v1.0.0", "notes": "Initial release.", "last_tag": "v0.0.0"}


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Enhanced GitHub Release Manager")
    parser.add_argument("--tag", help="Release tag (auto-detected if not provided)")
    parser.add_argument(
        "--title",
        help="Release title (auto-generated if not provided)",
    )
    parser.add_argument(
        "--notes",
        help="Release notes (auto-generated if not provided)",
    )
    parser.add_argument("--notes-file", help="Read release notes from file")
    parser.add_argument("--prerelease", action="store_true", help="Mark as prerelease")
    parser.add_argument("--draft", action="store_true", help="Create as draft")
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip release verification",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Auto-detect version and changes",
    )

    args = parser.parse_args()

    # Initialize release manager
    release_manager = EnhancedGitHubReleaseManager()

    if not release_manager.repo_url:
        sys.exit(1)

    # Auto-detect version and changes
    if args.auto:
        detected = release_manager.auto_detect_version_and_changes()
        tag = args.tag or detected["version"]
        title = args.title or detected["title"]
        notes = args.notes or detected["notes"]
    else:
        tag = args.tag
        title = args.title or f"Release {tag}"

        if args.notes_file:
            try:
                with open(args.notes_file, "r") as f:
                    notes = f.read()
            except FileNotFoundError:
                print(f"[ERROR] Notes file not found: {args.notes_file}")
                sys.exit(1)
        else:
            notes = args.notes or "Release update"
            "Release created with Enhanced GitHub Release Manager."

    # Validate inputs
    if not tag:
        print("[ERROR] Release tag is required")
        sys.exit(1)

    # Create the release
    success = release_manager.create_release(
        tag=tag, title=title, notes=notes, prerelease=args.prerelease, draft=args.draft, verify=not args.no_verify
    )

    if success:
        print(f"[PARTY] Release {tag} completed successfully!")
        print(f"🔗 View at: {release_manager.repo_url}/releases/tag/{tag}")
        sys.exit(0)
    else:
        print(f"💥 Release {tag} failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
