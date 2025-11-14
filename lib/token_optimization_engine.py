#!/usr/bin/env python3
"""
Token Optimization Engine

Advanced token management system for minimizing token consumption while maximizing functionality.
Implements progressive loading, smart caching, and context-aware content delivery.

Version: 1.0.0
Author: Autonomous Agent Plugin
"""

import json
import os
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import pathlib


class ContentType(Enum):
    """Content type categories for optimization strategies."""

    METADATA = "metadata"  # Always loaded, minimal tokens
    CORE = "core"  # Essential functionality
    EXTENDED = "extended"  # Detailed information
    REFERENCE = "reference"  # Additional resources


@dataclass
class ContentItem:
    """Represents a piece of content with optimization metadata."""

    path: str
    content_type: ContentType
    token_count: int
    priority: int  # 1-10, lower = higher priority
    dependencies: List[str]
    last_accessed: float
    access_frequency: float
    compression_ratio: float = 1.0

    @property
    def efficiency_score(self) -> float:
        """Calculate efficiency score based on usage and size."""
        return self.access_frequency / (self.token_count / 1000)


class TokenOptimizer:
    """
    Advanced token optimization engine with progressive loading and smart caching.
    """

    def __init__(self, cache_dir: str = ".claude-patterns"):
        self.cache_dir = pathlib.Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Content registry
        self.content_registry: Dict[str, ContentItem] = {}
        self.loaded_content: Dict[str, str] = {}
        self.access_log: List[Tuple[str, float]] = []

        # Configuration
        self.max_tokens_per_request = {
            ContentType.METADATA: 10000,  # 10K tokens always available
            ContentType.CORE: 50000,  # 50K tokens for core functionality
            ContentType.EXTENDED: 100000,  # 100K tokens for extended content
            ContentType.REFERENCE: 200000,  # 200K tokens for references
        }

        # Cache files
        self.registry_file = self.cache_dir / "content_registry.json"
        self.access_log_file = self.cache_dir / "access_log.json"
        self.analytics_file = self.cache_dir / "token_analytics.json"

        # Load existing data
        self._load_registry()
        self._load_access_log()
        self._update_analytics()

    def register_content(
        self, path: str, content: str, content_type: ContentType, priority: int = 5, dependencies: List[str] = None
    ) -> None:
        """Register content for optimization management."""
        if dependencies is None:
            dependencies = []

        token_count = self._estimate_tokens(content)

        content_item = ContentItem(
            path=path,
            content_type=content_type,
            token_count=token_count,
            priority=priority,
            dependencies=dependencies,
            last_accessed=time.time(),
            access_frequency=0.0,
        )

        self.content_registry[path] = content_item
        self._save_registry()

    def get_content(self, path: str, available_tokens: int = None) -> str:
        """Get content with progressive loading based on available tokens."""
        if available_tokens is None:
            available_tokens = self.max_tokens_per_request[ContentType.EXTENDED]

        # Update access tracking
        self._track_access(path)

        # Check if content is already loaded
        if path in self.loaded_content:
            return self.loaded_content[path]

        # Load content based on token budget
        content_item = self.content_registry.get(path)
        if not content_item:
            return ""

        # Check if we can load this content within token budget
        if content_item.token_count <= available_tokens:
            full_content = self._load_file_content(path)
            self.loaded_content[path] = full_content
            return full_content
        else:
            # Return compressed/summary version
            return self._get_compressed_content(path, available_tokens)

    def get_optimized_content_set(self, content_type: ContentType, max_total_tokens: int = None) -> Dict[str, str]:
        """Get optimized set of content for a specific type within token budget."""
        if max_total_tokens is None:
            max_total_tokens = self.max_tokens_per_request[content_type]

        # Filter content by type and sort by efficiency score
        filtered_content = [(path, item) for path, item in self.content_registry.items() if item.content_type == content_type]

        # Sort by efficiency score (highest first)
        filtered_content.sort(key=lambda x: x[1].efficiency_score, reverse=True)

        result = {}
        used_tokens = 0

        for path, item in filtered_content:
            if used_tokens + item.token_count <= max_total_tokens:
                content = self.get_content(path, max_total_tokens - used_tokens)
                if content:
                    result[path] = content
                    used_tokens += item.token_count
            else:
                # Try to get compressed version
                compressed = self._get_compressed_content(path, max_total_tokens - used_tokens)
                if compressed:
                    result[path] = compressed
                    break

        return result

    def _track_access(self, path: str) -> None:
        """Track content access for analytics."""
        current_time = time.time()
        self.access_log.append((path, current_time))

        # Update content item
        if path in self.content_registry:
            item = self.content_registry[path]
            item.last_accessed = current_time

            # Calculate access frequency (accesses per day)
            recent_accesses = [t for _, t in self.access_log if t > current_time - 86400]
            path_accesses = len([p for p, t in self.access_log if p == path and t > current_time - 86400])
            item.access_frequency = path_accesses

        # Keep access log manageable (last 1000 entries)
        if len(self.access_log) > 1000:
            self.access_log = self.access_log[-1000:]

        self._save_access_log()

    def _estimate_tokens(self, content: str) -> int:
        """Estimate token count for content."""
        # Rough estimation: ~1 token per 3-4 characters for technical content
        return len(content) // 3

    def _load_file_content(self, path: str) -> str:
        """Load content from file."""
        try:
            file_path = pathlib.Path(path)
            if file_path.exists():
                return file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error loading {path}: {e}")
        return ""

    def _get_compressed_content(self, path: str, max_tokens: int) -> str:
        """Get compressed version of content within token limits."""
        content_item = self.content_registry.get(path)
        if not content_item:
            return ""

        full_content = self._load_file_content(path)

        # Simple compression: extract key sections
        lines = full_content.split("\n")

        # Priority content types
        priority_patterns = [
            "---",  # YAML frontmatter
            "# ",  # Headers
            "## ",  # Subheaders
            "### ",  # Sub-subheaders
            "```",  # Code blocks
            "**",  # Bold text
            "```python",  # Python code
            "```json",  # JSON examples
        ]

        compressed_lines = []
        current_tokens = 0
        target_tokens = max_tokens * 0.9  # Leave some buffer

        for line in lines:
            line_tokens = self._estimate_tokens(line)
            if current_tokens + line_tokens <= target_tokens:
                # Include priority lines
                if any(pattern in line for pattern in priority_patterns):
                    compressed_lines.append(line)
                    current_tokens += line_tokens
                # Include short lines
                elif len(line.strip()) < 100:
                    compressed_lines.append(line)
                    current_tokens += line_tokens
            else:
                break

        if compressed_lines:
            return "\n".join(compressed_lines) + f"\n\n[Content compressed to {current_tokens} tokens]"
        else:
            return f"[Content available but exceeds {max_tokens} token limit]"

    def _load_registry(self) -> None:
        """Load content registry from cache."""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r") as f:
                    data = json.load(f)
                    for path, item_data in data.items():
                        self.content_registry[path] = ContentItem(**item_data)
            except Exception as e:
                print(f"Error loading registry: {e}")

    def _save_registry(self) -> None:
        """Save content registry to cache."""
        try:
            with open(self.registry_file, "w") as f:
                data = {path: asdict(item) for path, item in self.content_registry.items()}
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving registry: {e}")

    def _load_access_log(self) -> None:
        """Load access log from cache."""
        if self.access_log_file.exists():
            try:
                with open(self.access_log_file, "r") as f:
                    data = json.load(f)
                    self.access_log = [(item["path"], item["timestamp"]) for item in data]
            except Exception as e:
                print(f"Error loading access log: {e}")

    def _save_access_log(self) -> None:
        """Save access log to cache."""
        try:
            with open(self.access_log_file, "w") as f:
                data = [{"path": path, "timestamp": timestamp} for path, timestamp in self.access_log]
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving access log: {e}")

    def _update_analytics(self) -> None:
        """Update analytics data."""
        analytics = {
            "total_registered_content": len(self.content_registry),
            "total_tokens": sum(item.token_count for item in self.content_registry.values()),
            "content_by_type": {},
            "access_frequency": len(self.access_log),
            "last_updated": time.time(),
        }

        for content_type in ContentType:
            count = len([item for item in self.content_registry.values() if item.content_type == content_type])
            analytics["content_by_type"][content_type.value] = count

        try:
            with open(self.analytics_file, "w") as f:
                json.dump(analytics, f, indent=2)
        except Exception as e:
            print(f"Error saving analytics: {e}")

    def get_optimization_report(self) -> Dict[str, Any]:
        """Generate comprehensive optimization report."""
        total_tokens = sum(item.token_count for item in self.content_registry.values())

        report = {
            "total_content_items": len(self.content_registry),
            "total_tokens": total_tokens,
            "average_tokens_per_item": total_tokens / len(self.content_registry) if self.content_registry else 0,
            "content_distribution": {},
            "efficiency_ranking": [],
            "recommendations": [],
        }

        # Content distribution by type
        for content_type in ContentType:
            items = [item for item in self.content_registry.values() if item.content_type == content_type]
            if items:
                report["content_distribution"][content_type.value] = {
                    "count": len(items),
                    "total_tokens": sum(item.token_count for item in items),
                    "average_tokens": sum(item.token_count for item in items) / len(items),
                }

        # Efficiency ranking
        sorted_items = sorted(self.content_registry.items(), key=lambda x: x[1].efficiency_score, reverse=True)
        report["efficiency_ranking"] = [
            {
                "path": path,
                "efficiency_score": item.efficiency_score,
                "token_count": item.token_count,
                "access_frequency": item.access_frequency,
            }
            for path, item in sorted_items[:10]
        ]

        # Recommendations
        low_efficiency_items = [item for item in self.content_registry.values() if item.efficiency_score < 0.1]
        if low_efficiency_items:
            report["recommendations"].append(
                {
                    "type": "optimization",
                    "message": f"Found {len(low_efficiency_items)} low-efficiency content items. Consider compression or removal.",
                    "items": [item.path for item in low_efficiency_items[:5]],
                }
            )

        high_token_items = [item for item in self.content_registry.values() if item.token_count > 10000]
        if high_token_items:
            report["recommendations"].append(
                {
                    "type": "compression",
                    "message": f"Found {len(high_token_items)} high-token content items. Consider progressive loading.",
                    "items": [item.path for item in high_token_items[:5]],
                }
            )

        return report


# Global optimizer instance
_token_optimizer = None


def get_token_optimizer() -> TokenOptimizer:
    """Get or create global token optimizer instance."""
    global _token_optimizer
    if _token_optimizer is None:
        _token_optimizer = TokenOptimizer()
    return _token_optimizer


def register_project_content():
    """Register all project content for token optimization."""
    optimizer = get_token_optimizer()

    # Register main documentation
    claude_content = pathlib.Path("CLAUDE.md").read_text(encoding="utf-8") if pathlib.Path("CLAUDE.md").exists() else ""
    if claude_content:
        optimizer.register_content("CLAUDE.md", claude_content, ContentType.CORE, priority=1)

    # Register agents
    agents_dir = pathlib.Path("agents")
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            content = agent_file.read_text(encoding="utf-8")
            optimizer.register_content(str(agent_file), content, ContentType.EXTENDED, priority=3)

    # Register skills
    skills_dir = pathlib.Path("skills")
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    content = skill_file.read_text(encoding="utf-8")
                    optimizer.register_content(str(skill_file), content, ContentType.EXTENDED, priority=4)

    # Register commands
    commands_dir = pathlib.Path("commands")
    if commands_dir.exists():
        for cmd_file in commands_dir.glob("*.md"):
            content = cmd_file.read_text(encoding="utf-8")
            optimizer.register_content(str(cmd_file), content, ContentType.CORE, priority=2)

    print(f"Registered {len(optimizer.content_registry)} content items for optimization")


if __name__ == "__main__":
    # Initialize content registration
    register_project_content()

    # Generate optimization report
    optimizer = get_token_optimizer()
    report = optimizer.get_optimization_report()

    print("=== Token Optimization Report ===")
    print(f"Total Content Items: {report['total_content_items']}")
    print(f"Total Tokens: {report['total_tokens']:,}")
    print(f"Average Tokens per Item: {report['average_tokens_per_item']:.1f}")

    print("\nContent Distribution:")
    for content_type, stats in report["content_distribution"].items():
        print(f"  {content_type}: {stats['count']} items, {stats['total_tokens']:,} tokens")

    print("\nTop Efficiency Items:")
    for item in report["efficiency_ranking"][:5]:
        print(f"  {item['path']}: {item['efficiency_score']:.3f} score")

    if report["recommendations"]:
        print("\nRecommendations:")
        for rec in report["recommendations"]:
            print(f"  • {rec['message']}")

    print(f"\nDetailed report saved to: {optimizer.analytics_file}")
