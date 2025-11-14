#!/usr/bin/env python3
#     Progressive Content Loader
    """
Intelligent content loading system that provides tiered access to documentation
and commands based on user needs and available token budget.

Version: 1.0.0
Author: Autonomous Agent Plugin
import json
import os
import pathlib
import re
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import time

from token_optimization_engine import get_token_optimizer, ContentType


class LoadingTier(Enum):
    """Content loading tiers for progressive delivery."""

    ESSENTIAL = "essential"  # Critical information only
    STANDARD = "standard"  # Normal level of detail
    COMPREHENSIVE = "comprehensive"  # Full content
    COMPLETE = "complete"  # Everything including references


@dataclass
class ContentSection:
    """Represents a section of content with loading metadata."""

    title: str
    content: str
    tokens: int
    priority: int  # 1-10, lower = higher priority
    dependencies: List[str]
    tags: Set[str]
    loading_tier: LoadingTier
    last_accessed: float = 0
    access_count: int = 0


class ProgressiveContentLoader:
    """
    Progressive content loader that intelligently manages content delivery
    """
    based on user needs and token constraints.
    """

    def __init__(self, cache_dir: str = ".claude-patterns"):
        """Initialize the processor with default configuration."""
        self.cache_dir = pathlib.Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Content sections registry
        self.sections: Dict[str, List[ContentSection]] = {}
        self.content_index: Dict[str, ContentSection] = {}
        self.user_patterns: Dict[str, Any] = {}

        # Loading configuration
        self.tier_token_limits = {
            LoadingTier.ESSENTIAL: 5000,  # 5K tokens
            LoadingTier.STANDARD: 20000,  # 20K tokens
            LoadingTier.COMPREHENSIVE: 50000,  # 50K tokens
            LoadingTier.COMPLETE: 100000,  # 100K tokens
        }

        # Cache files
        self.sections_file = self.cache_dir / "content_sections.json"
        self.patterns_file = self.cache_dir / "user_patterns.json"
        self.loader_cache_file = self.cache_dir / "loader_cache.json"

        # Load existing data
        self._load_sections()
        self._load_user_patterns()

    def analyze_and_register_file(self, file_path: str) -> None:
        """Analyze a file and register its sections for progressive loading."""
        file_path = pathlib.Path(file_path)
        if not file_path.exists():
            return

        content = file_path.read_text(encoding="utf-8")
        sections = self._parse_content_sections(content, str(file_path))

        self.sections[str(file_path)] = sections

        # Update index
        for section in sections:
            self.content_index[f"{file_path}:{section.title}"] = section

        self._save_sections()

    def _parse_content_sections(self, content: str, file_path: str) -> List[ContentSection]:
        """Parse content into sections with metadata."""
        sections = []

        # Split by headers
        header_pattern = r"^(#{1,6})\s+(.+)$"
        lines = content.split("\n")

        current_section = None
        current_content = []
        current_level = 0

        for line in lines:
            header_match = re.match(header_pattern, line)

            if header_match:
                # Save previous section
                if current_section:
                    section_content = "\n".join(current_content).strip()
                    if section_content:
                        current_section.content = section_content
                        current_section.tokens = len(section_content) // 3
                        sections.append(current_section)

                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()

                current_section = ContentSection(
                    title=title,
                    content="",  # Will be filled when section ends
                    tokens=0,
                    priority=self._calculate_priority(title, level),
                    dependencies=self._extract_dependencies(title),
                    tags=self._extract_tags(title, line),
                    loading_tier=self._determine_loading_tier(title, level),
                    last_accessed=0,
                    access_count=0,
                )

                current_content = []
                current_level = level
            else:
                if current_section:
                    current_content.append(line)

        # Handle last section
        if current_section and current_content:
            section_content = "\n".join(current_content).strip()
            if section_content:
                current_section.content = section_content
                current_section.tokens = len(section_content) // 3
                sections.append(current_section)

        return sections

    def _calculate_priority(self, title: str, level: int) -> int:
        """Calculate priority based on title and header level."""
        base_priority = level * 2  # Higher level headers get higher priority

        # Adjust based on title content
        title_lower = title.lower()

        if any(keyword in title_lower for keyword in ["overview", "introduction", "getting started", "quick start"]):
            base_priority -= 2
        elif any(keyword in title_lower for keyword in ["installation", "setup", "configuration"]):
            base_priority -= 1
        elif any(keyword in title_lower for keyword in ["advanced", "details", "reference", "appendix"]):
            base_priority += 2
        elif any(keyword in title_lower for keyword in ["examples", "code", "implementation"]):
            base_priority += 1

        return max(1, min(10, base_priority))

    def _extract_dependencies(self, title: str) -> List[str]:
        """Extract dependencies from section title."""
        dependencies = []
        title_lower = title.lower()

        # Common dependency patterns
        if any(word in title_lower for word in ["prerequisites", "requirements"]):
            dependencies.append("setup")
        if any(word in title_lower for word in ["advanced", "expert"]):
            dependencies.append("basics")

        return dependencies

    def _extract_tags(self, title: str, content_line: str) -> Set[str]:
        """Extract tags from title and content."""
        tags = set()
        title_lower = title.lower()

        # Category tags
        if "installation" in title_lower or "setup" in title_lower:
            tags.add("setup")
        if "configuration" in title_lower or "config" in title_lower:
            tags.add("configuration")
        if "example" in title_lower or "demo" in title_lower:
            tags.add("example")
        if "api" in title_lower:
            tags.add("api")
        if "troubleshooting" in title_lower or "debug" in title_lower:
            tags.add("troubleshooting")

        return tags

    def _determine_loading_tier(self, title: str, level: int) -> LoadingTier:
        """Determine the appropriate loading tier for a section."""
        title_lower = title.lower()

        # Essential tier - critical information
        if level <= 2 or any(
            keyword in title_lower
            for keyword in [
                "overview",
                "introduction",
                "getting started",
                "quick start",
                "installation",
                "basic usage",
                "summary",
            ]
        ):
            return LoadingTier.ESSENTIAL

        # Standard tier - commonly needed information
        if level <= 3 or any(keyword in title_lower for keyword in ["configuration", "examples", "usage", "api", "commands"]):
            return LoadingTier.STANDARD

        # Comprehensive tier - detailed information
        if level <= 4 or any(keyword in title_lower for keyword in ["advanced", "details", "implementation", "architecture"]):
            return LoadingTier.COMPREHENSIVE

        # Complete tier - everything else
        return LoadingTier.COMPLETE

    def load_content(
        self,
        file_path: str,
        user_request: str = "",
        available_tokens: int = 20000,
        preferred_tier: LoadingTier = LoadingTier.STANDARD,
    )-> Dict[str, Any]:
        """Load Content."""Load content progressively based on user needs and token constraints."""
        file_path_str = str(file_path)

        # Track user pattern
        self._track_user_pattern(user_request, file_path_str)

        # Get sections for this file
        sections = self.sections.get(file_path_str, [])
        if not sections:
            return {"content": "", "sections_loaded": [], "tokens_used": 0}

        # Determine optimal loading strategy
        loading_strategy = self._determine_loading_strategy(user_request, available_tokens, preferred_tier, sections)

        # Load sections according to strategy
        loaded_sections = []
        tokens_used = 0
        content_parts = []

        for section in sections:
            if self._should_load_section(section, loading_strategy, tokens_used, available_tokens):
                # Check dependencies
                if self._dependencies_met(section, loaded_sections):
                    # Load section content
                    section_content = self._format_section(section, loading_strategy)
                    content_parts.append(section_content)
                    loaded_sections.append(section.title)
                    tokens_used += section.tokens

                    # Update access tracking
                    section.last_accessed = time.time()
                    section.access_count += 1

        # Assemble final content
        final_content = "\n\n".join(content_parts)

        return {
            "content": final_content,
            "sections_loaded": loaded_sections,
            "tokens_used": tokens_used,
            "loading_strategy": loading_strategy,
            "file_path": file_path_str,
        }

    def _determine_loading_strategy(
        self, user_request: str, available_tokens: int, preferred_tier: LoadingTier, sections: List[ContentSection]
    )-> Dict[str, Any]:
        """ Determine Loading Strategy."""Determine optimal loading strategy based on context."""
        strategy = {
            "tier": preferred_tier,
            "max_tokens": available_tokens,
            "focus_tags": set(),
            "exclude_patterns": set(),
            "adaptive": True,
        }

        # Analyze user request for keywords
        request_lower = user_request.lower()

        # Determine focus areas based on request
        if any(keyword in request_lower for keyword in ["install", "setup", "getting started", "beginner"]):
            strategy["focus_tags"].update(["setup", "basic", "essential"])
            strategy["tier"] = LoadingTier.ESSENTIAL

        elif any(keyword in request_lower for keyword in ["example", "demo", "how to", "tutorial"]):
            strategy["focus_tags"].update(["example", "usage", "tutorial"])

        elif any(keyword in request_lower for keyword in ["advanced", "expert", "detailed", "comprehensive"]):
            strategy["focus_tags"].update(["advanced", "detailed"])
            strategy["tier"] = LoadingTier.COMPREHENSIVE

        # Adjust based on available tokens
        if available_tokens < self.tier_token_limits[LoadingTier.ESSENTIAL]:
            strategy["tier"] = LoadingTier.ESSENTIAL
        elif available_tokens < self.tier_token_limits[preferred_tier]:
            # Downgrade tier if not enough tokens
            for tier in [LoadingTier.STANDARD, LoadingTier.ESSENTIAL]:
                if available_tokens >= self.tier_token_limits[tier]:
                    strategy["tier"] = tier
                    break

        return strategy

    def _should_load_section(
        self, section: ContentSection, strategy: Dict[str, Any], tokens_used: int, max_tokens: int
    )-> bool:
        """ Should Load Section."""Determine if a section should be loaded based on strategy."""
        # Check token budget
        if tokens_used + section.tokens > max_tokens:
            return False

        # Check tier compatibility
        tier_order = [LoadingTier.ESSENTIAL, LoadingTier.STANDARD, LoadingTier.COMPREHENSIVE, LoadingTier.COMPLETE]
        strategy_tier_index = tier_order.index(strategy["tier"])
        section_tier_index = tier_order.index(section.loading_tier)

        if section_tier_index > strategy_tier_index:
            return False

        # Check priority
        if strategy["focus_tags"] and not strategy["focus_tags"] & section.tags:
            # If no matching tags, only load high priority sections
            if section.priority > 5:
                return False

        return True

    def _dependencies_met(self, section: ContentSection, loaded_sections: List[str]) -> bool:
        """Check if section dependencies are met."""
        for dep in section.dependencies:
            if dep not in [s.lower() for s in loaded_sections]:
                return False
        return True

    def _format_section(self, section: ContentSection, strategy: Dict[str, Any]) -> str:
        """Format section content based on loading strategy."""
        content = section.content

        # Apply tier-based formatting
        if strategy["tier"] == LoadingTier.ESSENTIAL:
            # Extract only essential information
            lines = content.split("\n")
            essential_lines = []

            for line in lines:
                # Keep headers
                if line.startswith("#"):
                    essential_lines.append(line)
                # Keep short, important lines
                elif len(line.strip()) < 100 and line.strip():
                    essential_lines.append(line)
                # Keep code blocks (but limit them)
                elif line.startswith("```"):
                    essential_lines.append(line)
                    essential_lines.append("# [Code block truncated for essential loading]")
                    essential_lines.append("```")

            content = "\n".join(essential_lines)

        elif strategy["tier"] == LoadingTier.STANDARD:
            # Remove very long examples and references
            content = self._truncate_long_content(content, max_lines=50)

        # Add section header
        formatted_content = f"## {section.title}\n\n{content}"

        return formatted_content

    def _truncate_long_content(self, content: str, max_lines: int = 50) -> str:
        """Truncate long content while preserving structure."""
        lines = content.split("\n")

        if len(lines) <= max_lines:
            return content

        # Keep headers and important content
        important_lines = []
        code_block = False
        code_lines = 0

        for line in lines[:max_lines]:
            # Always keep headers
            if line.startswith("#"):
                important_lines.append(line)
            # Handle code blocks
            elif line.startswith("```"):
                code_block = not code_block
                important_lines.append(line)
                code_lines = 0
            elif code_block:
                important_lines.append(line)
                code_lines += 1
                if code_lines > 20:  # Limit code block lines
                    important_lines.append("# [Code block truncated]")
                    important_lines.append("```")
                    code_block = False
            # Keep short lines
            elif len(line.strip()) < 150:
                important_lines.append(line)

        important_lines.append(f"\n# [Content truncated to {max_lines} lines for standard loading]")

        return "\n".join(important_lines)

    def _track_user_pattern(self, user_request: str, file_path: str) -> None:
        """Track user patterns for predictive loading."""
        if not user_request:
            return

        timestamp = time.time()

        if file_path not in self.user_patterns:
            self.user_patterns[file_path] = {
                "requests": [],
                "common_keywords": {},
                "preferred_tiers": {},
                "last_accessed": timestamp,
            }

        pattern = self.user_patterns[file_path]
        pattern["requests"].append({"request": user_request, "timestamp": timestamp})
        pattern["last_accessed"] = timestamp

        # Extract keywords
        words = re.findall(r"\b\w+\b", user_request.lower())
        for word in words:
            if len(word) > 3:  # Only track meaningful words
                pattern["common_keywords"][word] = pattern["common_keywords"].get(word, 0) + 1

        # Keep only recent requests
        if len(pattern["requests"]) > 50:
            pattern["requests"] = pattern["requests"][-50:]

        self._save_user_patterns()

    def get_recommendations(self, file_path: str, user_request: str = "") -> List[Dict[str, Any]]:
        """Get content loading recommendations based on patterns."""
        file_path_str = str(file_path)
        recommendations = []

        # Check user patterns
        if file_path_str in self.user_patterns:
            pattern = self.user_patterns[file_path_str]

            # Recommend based on common keywords
            if user_request:
                request_words = set(re.findall(r"\b\w+\b", user_request.lower()))
                common_keywords = {k: v for k, v in pattern["common_keywords"].items() if v > 2 and len(k) > 3}

                matching_keywords = request_words & set(common_keywords.keys())
                if matching_keywords:
                    recommendations.append(
                        {
                            "type": "relevant_sections",
                            "message": f"Based on your interests in {', '.join(matching_keywords)}",
                            "keywords": list(matching_keywords),
                        }
                    )

        # Recommend based on section popularity
        sections = self.sections.get(file_path_str, [])
        popular_sections = [s for s in sections if s.access_count > 0]

        if popular_sections:
            popular_sections.sort(key=lambda x: x.access_count, reverse=True)
            recommendations.append(
                {
                    "type": "popular_sections",
                    "message": "Popular sections based on usage",
                    "sections": [s.title for s in popular_sections[:3]],
                }
            )

        return recommendations

    def _load_sections(self) -> None:
        """Load content sections from cache."""
        if self.sections_file.exists():
            try:
                with open(self.sections_file, "r") as f:
                    data = json.load(f)
                    for file_path, sections_data in data.items():
                        sections = []
                        for section_data in sections_data:
                            section = ContentSection(
                                title=section_data["title"],
                                content=section_data["content"],
                                tokens=section_data["tokens"],
                                priority=section_data["priority"],
                                dependencies=section_data["dependencies"],
                                tags=set(section_data["tags"]),
                                loading_tier=LoadingTier(section_data["loading_tier"]),
                                last_accessed=section_data.get("last_accessed", 0),
                                access_count=section_data.get("access_count", 0),
                            )
                            sections.append(section)
                        self.sections[file_path] = sections
            except Exception as e:
                print(f"Error loading sections: {e}")

    def _save_sections(self) -> None:
        """Save content sections to cache."""
        try:
            data = {}
            for file_path, sections in self.sections.items():
                data[file_path] = []
                for section in sections:
                    section_data = {
                        "title": section.title,
                        "content": section.content,
                        "tokens": section.tokens,
                        "priority": section.priority,
                        "dependencies": section.dependencies,
                        "tags": list(section.tags),
                        "loading_tier": section.loading_tier.value,
                        "last_accessed": section.last_accessed,
                        "access_count": section.access_count,
                    }
                    data[file_path].append(section_data)

            with open(self.sections_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving sections: {e}")

    def _load_user_patterns(self) -> None:
        """Load user patterns from cache."""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, "r") as f:
                    self.user_patterns = json.load(f)
            except Exception as e:
                print(f"Error loading user patterns: {e}")

    def _save_user_patterns(self) -> None:
        """Save user patterns to cache."""
        try:
            with open(self.patterns_file, "w") as f:
                json.dump(self.user_patterns, f, indent=2)
        except Exception as e:
            print(f"Error saving user patterns: {e}")

    def generate_usage_report(self) -> Dict[str, Any]:
        """Generate comprehensive usage report."""
        report = {
            "total_files": len(self.sections),
            "total_sections": sum(len(sections) for sections in self.sections.values()),
            "section_distribution": {},
            "most_accessed_sections": [],
            "user_patterns_summary": {},
            "optimization_recommendations": [],
        }

        # Section distribution by tier
        tier_counts = {tier.value: 0 for tier in LoadingTier}
        for sections in self.sections.values():
            for section in sections:
                tier_counts[section.loading_tier.value] += 1
        report["section_distribution"] = tier_counts

        # Most accessed sections
        all_sections = []
        for sections in self.sections.values():
            all_sections.extend(sections)

        all_sections.sort(key=lambda x: x.access_count, reverse=True)
        report["most_accessed_sections"] = [
            {
                "title": s.title,
                "access_count": s.access_count,
                "tokens": s.tokens,
                "efficiency": s.access_count / max(s.tokens / 1000, 1),
            }
            for s in all_sections[:10]
        ]

        # User patterns summary
        total_requests = sum(len(pattern.get("requests", [])) for pattern in self.user_patterns.values())
        report["user_patterns_summary"] = {
            "total_patterns": len(self.user_patterns),
            "total_requests": total_requests,
            "avg_requests_per_file": total_requests / len(self.user_patterns) if self.user_patterns else 0,
        }

        # Optimization recommendations
        if total_requests > 0:
            report["optimization_recommendations"].append(
                {"type": "caching", "message": "User patterns detected. Consider implementing predictive caching."}
            )

        low_access_sections = [s for s in all_sections if s.access_count == 0]
        if len(low_access_sections) > len(all_sections) * 0.3:
            report["optimization_recommendations"].append(
                {
                    "type": "content_optimization",
                    "message": f"{len(low_access_sections)} sections have never been accessed. Consider removal or consolidation.",
                }
            )

        return report


# Global loader instance
_progressive_loader = None


def get_progressive_loader() -> ProgressiveContentLoader:
    """Get or create global progressive loader instance."""
    global _progressive_loader
    if _progressive_loader is None:
        _progressive_loader = ProgressiveContentLoader()
    return _progressive_loader


def initialize_content_analysis():
    """Initialize content analysis for all project files."""
    loader = get_progressive_loader()

    # Analyze main documentation
    main_files = ["CLAUDE.md", "README.md", "CHANGELOG.md"]

    for file_path in main_files:
        if pathlib.Path(file_path).exists():
            loader.analyze_and_register_file(file_path)
            print(f"Analyzed {file_path}")

    # Analyze commands
    commands_dir = pathlib.Path("commands")
    if commands_dir.exists():
        for cmd_file in commands_dir.glob("*.md"):
            loader.analyze_and_register_file(str(cmd_file))

    # Analyze agents
    agents_dir = pathlib.Path("agents")
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            loader.analyze_and_register_file(str(agent_file))

    # Analyze skills
    skills_dir = pathlib.Path("skills")
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    loader.analyze_and_register_file(str(skill_file))

    # Generate usage report
    report = loader.generate_usage_report()
    print(f"\n=== Content Analysis Complete ===")
    print(f"Total Files: {report['total_files']}")
    print(f"Total Sections: {report['total_sections']}")
    print(f"Total User Requests: {report['user_patterns_summary']['total_requests']}")

    if report["optimization_recommendations"]:
        print("\nRecommendations:")
        for rec in report["optimization_recommendations"]:
            print(f"  • {rec['message']}")


if __name__ == "__main__":
    initialize_content_analysis()
