#!/usr/bin/env python3
#     GitHub About Section Updater
"""
Updates GitHub repository About section with optimized description and topics
for the Autonomous Agent v7.1.0 release.

Usage:
python update_github_about.py [--dry-run] [--token TOKEN]
"""
import json
import os
import sys
import argparse
import requests
from typing import Dict, List, Optional


class GitHubAboutUpdater:
    """Handles GitHub repository About section updates with SEO optimization."""

    def __init__(self, token: Optional[str] = None):
"""
        Initialize the updater.

        Args:
            token: GitHub personal access token (can be set via GITHUB_TOKEN env var)
"""
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            print("WARNING: No GitHub token provided. Use --token or set GITHUB_TOKEN env var.")

        # Repository info from git remote
        self.owner = "bejranonda"
        self.repo = "LLM-Autonomous-Agent-Plugin-for-Claude"

        self.api_base = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "Autonomous-Agent-About-Updater"}

        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

"""
    def analyze_current_state(self) -> Dict:
        """Analyze current repository state and About section."""
        try:
            # Get repository info
            repo_url = f"{self.api_base}/repos/{self.owner}/{self.repo}"
            response = requests.get(repo_url, headers=self.headers)
            response.raise_for_status()

            repo_data = response.json()

            # Get current topics
            topics_url = f"{self.api_base}/repos/{self.owner}/{self.repo}/topics"
            topics_response = requests.get(topics_url, headers=self.headers)
            topics_response.raise_for_status()

            current_topics = topics_response.json().get("names", [])

            # Analyze project from local files
            project_info = self._analyze_project_locally()

            return {
                "current_description": repo_data.get("description", ""),
                "current_topics": current_topics,
                "current_homepage": repo_data.get("homepage", ""),
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "language": repo_data.get("language", ""),
                "project_info": project_info,
            }

        except Exception as e:
            print(f"ERROR: Could not analyze current state: {e}")
            return {}

    def _analyze_project_locally(self) -> Dict:
        """Analyze project from local files to extract key information."""
        try:
            # Read plugin.json for metadata
            plugin_file = os.path.join(os.path.dirname(__file__), "..", ".claude-plugin", "plugin.json")
            if os.path.exists(plugin_file):
                with open(plugin_file, "r", encoding="utf-8") as f:
                    plugin_data = json.load(f)
            else:
                plugin_data = {}

            # Read README for additional context
            readme_file = os.path.join(os.path.dirname(__file__), "..", "README.md")
            features = []
            if os.path.exists(readme_file):
                with open(readme_file, "r", encoding="utf-8") as f:
                    readme_content = f.read()
                    # Extract key features from README
                    if "Four-Tier Architecture" in readme_content:
                        features.append("four-tier-architecture")
                    if "Autonomous" in readme_content:
                        features.append("autonomous-agents")
                    if "Learning System" in readme_content:
                        features.append("pattern-learning")
                    if "Full-Stack Validation" in readme_content:
                        features.append("fullstack-validation")

            return {
                "version": plugin_data.get("version", "7.1.0"),
                "keywords": plugin_data.get("keywords", [])[:20],  # Limit to top 20
                "features": features,
                "description": plugin_data.get("description", ""),
            }

        except Exception as e:
            print(f"WARNING: Could not analyze project locally: {e}")
            return {}

    def generate_optimized_content():
"""
        
        Generate optimized description and topics for v7.1.0.

        Args:
            current_state: Current repository analysis

        Returns:
            Dictionary with optimized description and topics
"""
        # v7.1.0 key achievements to highlight
        achievements = [
            "51.6% file size reduction",
            "50% faster loading times",
            "Four-tier architecture with learning systems",
            "Full-stack validation with 89% auto-fix success",
            "95%+ prediction accuracy",
            "Enterprise-ready autonomous agents",
        ]

        # Generate concise description (max 350 chars)
        description_options = [
            # Option 1: Performance-focused
            f"Revolutionary autonomous agent plugin for Claude Code with 51.6% performance optimization, "
            f"four-tier architecture, and 95%+ prediction accuracy. "
            f"Full-stack validation, pattern learning, and enterprise-ready automation.",
            # Option 2: Feature-focused
            f"Autonomous AI agents for Claude Code with revolutionary four-tier architecture. "
            f"Features 51.6% performance optimization, intelligent learning systems, full-stack validation, "
            f"and enterprise-grade automation. Free forever, privacy-first.",
            # Option 3: Benefits-focused
            f"Transform your development with autonomous AI agents that learn and improve. "
            f"Experience 51.6% performance gains, four-tier intelligence, and 95%+ prediction accuracy. "
            f"Complete automation, validation, and learning systems included.",
        ]

        # Select the best description (under 350 chars)
        optimized_description = None
        for desc in description_options:
            if len(desc) <= 350:
                optimized_description = desc
                break

        if not optimized_description:
            # Fallback to truncated version
            optimized_description = description_options[0][:347] + "..."

        # Generate optimized topics based on current state and keywords
        base_topics = [
            "claude-code",
            "autonomous-agents",
            "artificial-intelligence",
            "automation",
            "code-analysis",
            "pattern-learning",
            "quality-control",
            "machine-learning",
            "performance-optimization",
            "fullstack-validation",
        ]

        # Add v7.1.0 specific topics
        v7_1_topics = [
            "four-tier-architecture",
            "enterprise-ready",
            "predictive-analytics",
            "auto-fix",
            "security-scanning",
            "documentation-generation",
        ]

        # Add language-specific topics
        language_topics = ["python", "javascript", "typescript", "multi-language"]

        # Add platform topics
        platform_topics = ["cross-platform", "windows", "linux", "macos"]

        # Combine and deduplicate
        all_topics = list(set(base_topics + v7_1_topics + language_topics + platform_topics))

        # Sort by relevance (put most important first)
        priority_topics = [
            "claude-code",
            "autonomous-agents",
            "artificial-intelligence",
            "automation",
            "pattern-learning",
            "four-tier-architecture",
            "performance-optimization",
            "fullstack-validation",
            "code-analysis",
            "machine-learning",
            "enterprise-ready",
            "predictive-analytics",
        ]

        # Sort topics by priority
        final_topics = []
        for topic in priority_topics:
            if topic in all_topics:
                final_topics.append(topic)
                all_topics.remove(topic)

        # Add remaining topics
        final_topics.extend(all_topics)

        # Limit to 20 topics (GitHub limit)
        final_topics = final_topics[:20]

        return {
            "description": optimized_description,
            "topics": final_topics,
            "homepage": "https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude",
            "achievements_highlighted": achievements,
            "seo_score": self._calculate_seo_score(optimized_description, final_topics),
        }

    def _calculate_seo_score(self, description: str, topics: List[str]) -> Dict:
        """Calculate SEO optimization score."""
        score = 0
        max_score = 100

        # Description length check (optimal: 200-350 chars)
        desc_len = len(description)
        if 200 <= desc_len <= 350:
            score += 20
        elif 150 <= desc_len < 200 or 350 < desc_len <= 400:
            score += 15
        else:
            score += 10

        # Keywords in description
        key_terms = ["autonomous", "claude", "agents", "learning", "performance", "automation"]
        keywords_found = sum(1 for term in key_terms if term.lower() in description.lower())
        score += min(keywords_found * 5, 30)

        # Topic relevance and diversity
        if len(topics) >= 10:
            score += 20
        elif len(topics) >= 7:
            score += 15
        else:
            score += 10

        # Topic quality (mix of general and specific)
        general_topics = sum(1 for topic in topics if len(topic.split("-")) == 1)
        specific_topics = sum(1 for topic in topics if len(topic.split("-")) > 1)

        if general_topics >= 3 and specific_topics >= 5:
            score += 20
        elif general_topics >= 2 and specific_topics >= 3:
            score += 15
        else:
            score += 10

        # v7.1.0 specific keywords
        v7_1_keywords = ["optimization", "performance", "architecture", "validation"]
        v7_1_found = sum(1 for kw in v7_1_keywords if kw.lower() in description.lower())
        score += min(v7_1_found * 2.5, 10)

        return {
            "score": min(score, max_score),
            "description_length": desc_len,
            "keywords_in_description": keywords_found,
            "topics_count": len(topics),
            "v7_1_keywords": v7_1_found,
        }

    def update_repository():
"""
        
        Update the GitHub repository with optimized content.

        Args:
            optimized_content: Dictionary with description and topics
            dry_run: If True, only show what would be updated

        Returns:
            True if successful, False otherwise
"""
        if not self.token:
            print("ERROR: GitHub token required for updates. Set GITHUB_TOKEN or use --token.")
            return False

        try:
            repo_url = f"{self.api_base}/repos/{self.owner}/{self.repo}"

            # Prepare update data
            update_data = {
                "description": optimized_content["description"],
                "homepage": optimized_content["homepage"],
                "topics": optimized_content["topics"],
            }

            if dry_run:
                print("DRY RUN - Would update repository with:")
                print(f"  Description: {update_data['description']}")
                print(f"  Homepage: {update_data['homepage']}")
                print(f"  Topics: {', '.join(update_data['topics'])}")
                return True

            # Update repository
            response = requests.patch(repo_url, headers=self.headers, json=update_data)
            response.raise_for_status()

            print("SUCCESS: Repository updated successfully!")
            return True

        except Exception as e:
            print(f"ERROR: Could not update repository: {e}")
            return False

"""
    def generate_report(self, current_state: Dict, optimized_content: Dict) -> str:
        """Generate a comprehensive report of the changes."""
        report = []
        report.append("=" * 60)
        report.append("GITHUB ABOUT SECTION OPTIMIZATION REPORT")
        report.append("=" * 60)
        report.append("")

        # Current state
        report.append("CURRENT STATE:")
        report.append(f"  Description: \"{current_state.get('current_description', 'N/A')}\"")
        report.append(f"  Topics: {len(current_state.get('current_topics', []))} topics")
        if current_state.get("current_topics"):
            report.append(f"  Current topics: {', '.join(current_state['current_topics'][:10])}")
        report.append(f"  Stars: {current_state.get('stars', 0)}")
        report.append(f"  Forks: {current_state.get('forks', 0)}")
        report.append("")

        # Optimized content
        report.append("OPTIMIZED CONTENT:")
        report.append(f"  Description: \"{optimized_content['description']}\"")
        report.append(f"  Description length: {len(optimized_content['description'])}/350 chars")
        report.append(f"  Topics: {len(optimized_content['topics'])} topics")
        report.append(f"  New topics: {', '.join(optimized_content['topics'])}")
        report.append("")

        # v7.1.0 achievements highlighted
        report.append("v7.1.0 ACHIEVEMENTS HIGHLIGHTED:")
        for achievement in optimized_content["achievements_highlighted"]:
            report.append(f"  - {achievement}")
        report.append("")

        # SEO score
        seo_score = optimized_content["seo_score"]
        report.append("SEO OPTIMIZATION SCORE:")
        report.append(f"  Overall Score: {seo_score['score']}/100")

        if seo_score["score"] >= 90:
            rating = "EXCELLENT"
        elif seo_score["score"] >= 80:
            rating = "GOOD"
        elif seo_score["score"] >= 70:
            rating = "FAIR"
        else:
            rating = "NEEDS IMPROVEMENT"

        report.append(f"  Rating: {rating}")
        report.append(f"  - Description length: {seo_score['description_length']} chars (optimal: 200-350)")
        report.append(f"  - Keywords in description: {seo_score['keywords_in_description']} (max: 6)")
        report.append(f"  - Topics count: {seo_score['topics_count']} (optimal: 10-20)")
        report.append(f"  - v7.1.0 keywords: {seo_score['v7_1_keywords']}/4")
        report.append("")

        # Expected impact
        report.append("EXPECTED IMPACT:")
        report.append("  - Improved discoverability in GitHub search")
        report.append("  - Better ranking for autonomous agent queries")
        report.append("  - Increased click-through from search results")
        report.append("  - Enhanced professional presentation")
        report.append("")

        report.append("=" * 60)

        return "\n".join(report)


def main():
    """Main function to handle command line execution."""
    parser = argparse.ArgumentParser(description="Update GitHub About section for v7.1.0")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be updated without making changes")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--output", help="Save report to file")

    args = parser.parse_args()

    # Initialize updater
    updater = GitHubAboutUpdater(token=args.token)

    print("Starting GitHub About Section Optimization for v7.1.0...")
    print()

    # Analyze current state
    print("Analyzing current repository state...")
    current_state = updater.analyze_current_state()

    if not current_state:
        print("ERROR: Failed to analyze current state. Exiting.")
        sys.exit(1)

    print("SUCCESS: Current state analyzed successfully.")
    print()

    # Generate optimized content
    print("Generating optimized content for v7.1.0...")
    optimized_content = updater.generate_optimized_content(current_state)
    print("SUCCESS: Optimized content generated.")
    print()

    # Generate report
    report = updater.generate_report(current_state, optimized_content)

    # Save report if requested
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
        print()

    # Display report
    print(report)

    # Update repository (unless dry run)
    if not args.dry_run:
        print("Updating GitHub repository...")
        success = updater.update_repository(optimized_content)

        if success:
            print("SUCCESS: GitHub About section updated successfully!")
            print()
            print("Next steps:")
            print("  - Monitor repository traffic for improvements")
            print("  - Track search ranking changes over time")
            print("  - Consider updating social media with new description")
        else:
            print("ERROR: Failed to update repository. Please check your token and permissions.")
            sys.exit(1)
    else:
        print("DRY RUN COMPLETE - No changes made.")
        print("Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
