#!/usr/bin/env python3
#     Intelligent Suggestion Engine for Autonomous Agent Plugin
    """

Provides context-aware suggestions based on user preferences, learned patterns,
system environment, and historical behavior. Integrates with the user preference
memory system and task queue to provide intelligent next-step recommendations.

Features:
- Context-aware suggestion generation
- Learning from user behavior and preferences
- Integration with system environment and capabilities
- Priority-based recommendation system
- Multi-factor scoring algorithm
- Automatic suggestion filtering and ranking
- Cross-project pattern application

Version: 1.0.0
Author: Autonomous Agent Development Team
import json
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, Counter
import re
import hashlib

# Import our custom modules
try:
    from user_preference_memory import UserPreferenceMemory
    from unified_parameter_storage import UnifiedParameterStorage
except ImportError:
    print("Warning: Could not import required modules", file=sys.stderr)


class SuggestionContext:
    """Represents the context for generating suggestions."""

    def __init__(self):
        """Initialize the processor with default configuration."""
        self.current_task = None
        self.recent_commands = []
        self.system_environment = {}
        self.project_type = None
        self.active_files = []
        self.quality_score = None
        self.available_time = None
        self.user_goals = []
        self.session_context = {}
        self.workspace_state = {}

    def update_from_orchestrator(self, task_data: Dict[str, Any]):
        """Update context from orchestrator task data."""
        self.current_task = task_data.get("description", "")
        self.quality_score = task_data.get("quality_score")
        self.session_context = {
            "skills_loaded": task_data.get("skills_loaded", []),
            "agents_delegated": task_data.get("agents_delegated", []),
            "execution_time": task_data.get("execution_time", 0),
        }

    def update_from_workspace(self, workspace_data: Dict[str, Any]):
        """Update context from workspace analysis."""
        self.active_files = workspace_data.get("active_files", [])
        self.project_type = workspace_data.get("project_type", "unknown")
        self.workspace_state = workspace_data

    def update_from_preferences(self, preferences: Dict[str, Any]):
        """Update context from user preferences."""
        self.user_goals = preferences.get("goals", [])
        self.available_time = preferences.get("available_time", None)


class SuggestionTemplate:
    """Template for generating suggestions with dynamic parameters."""

    def __init__(
        self,
        template_id: str,
        category: str,
        priority: str,
        description_template: str,
        command_template: str,
        conditions: Dict[str, Any],
        weights: Dict[str, float],
    ):
        """Initialize the processor with default configuration."""
        self.template_id = template_id
        self.category = category
        self.priority = priority
        self.description_template = description_template
        self.command_template = command_template
        self.conditions = conditions
        self.weights = weights
        self.usage_count = 0
        self.success_count = 0

    def generate_suggestion(self, context: SuggestionContext, variables: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Generate a suggestion from this template if conditions are met."""
        if not self._check_conditions(context):
            return None

        variables = variables or {}
        description = self._fill_template(self.description_template, context, variables)
        command = self._fill_template(self.command_template, context, variables)

        return {
            "template_id": self.template_id,
            "category": self.category,
            "priority": self.priority,
            "description": description,
            "command": command,
            "estimated_time": self._estimate_time(context),
            "confidence": self._calculate_confidence(context),
            "impact": self._estimate_impact(context),
            "prerequisites": self._get_prerequisites(context),
            "risks": self._identify_risks(context),
        }

    def _check_conditions(self, context: SuggestionContext) -> bool:
        """Check if all conditions are met for this template."""
        for condition_type, condition_value in self.conditions.items():
            if condition_type == "min_quality_score":
                if context.quality_score and context.quality_score < condition_value:
                    return False
            elif condition_type == "project_types":
                if context.project_type not in condition_value:
                    return False
            elif condition_type == "required_files":
                if not any(pattern in str(context.active_files) for pattern in condition_value):
                    return False
            elif condition_type == "min_time_available":
                if context.available_time and context.available_time < condition_value:
                    return False
            elif condition_type == "exclude_if_recent":
                if any(cmd in str(context.recent_commands) for cmd in condition_value):
                    return False

        return True

    def _fill_template(self, template: str, context: SuggestionContext, variables: Dict[str, Any]) -> str:
        """Fill template with context variables."""
        # Create context variables
        template_vars = {
            "current_task": context.current_task or "",
            "project_type": context.project_type or "unknown",
            "quality_score": str(context.quality_score or 0),
            "primary_language": self._detect_primary_language(context),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Add custom variables
        template_vars.update(variables)

        # Replace template placeholders
        result = template
        for var, value in template_vars.items():
            result = result.replace(f"{{{var}}}", str(value))

        return result

    def _detect_primary_language(self, context: SuggestionContext) -> str:
        """Detect primary programming language from context."""
        if context.active_files:
            file_extensions = [Path(f).suffix.lower() for f in context.active_files]
            extension_counts = Counter(file_extensions)
            if extension_counts:
                most_common = extension_counts.most_common(1)[0][0]
                lang_map = {
                    ".py": "Python",
                    ".js": "JavaScript",
                    ".ts": "TypeScript",
                    ".java": "Java",
                    ".cpp": "C++",
                    ".c": "C",
                    ".go": "Go",
                    ".rs": "Rust",
                    ".php": "PHP",
                    ".rb": "Ruby",
                }
                return lang_map.get(most_common, "Unknown")
        return "Unknown"

    def _estimate_time(self, context: SuggestionContext) -> str:
        """Estimate execution time for this suggestion."""
        base_time = self.conditions.get("base_time", 5)  # minutes

        # Adjust based on project complexity
        if context.project_type in ["large-enterprise", "monolith"]:
            base_time *= 1.5
        elif context.project_type in ["small-project", "prototype"]:
            base_time *= 0.7

        # Adjust based on file count
        if len(context.active_files) > 50:
            base_time *= 1.3
        elif len(context.active_files) < 10:
            base_time *= 0.8

        return f"{int(base_time)}-{int(base_time * 1.5)} minutes"

    def _calculate_confidence(self, context: SuggestionContext) -> float:
        """Calculate confidence score for this suggestion."""
        confidence = 0.5  # Base confidence

        # Increase confidence based on historical success
        if self.usage_count > 0:
            success_rate = self.success_count / self.usage_count
            confidence += success_rate * 0.3

        # Increase confidence based on context match
        if self.category == "quality_improvement" and context.quality_score and context.quality_score < 80:
            confidence += 0.2

        # Increase confidence based on project type match
        project_types = self.conditions.get("project_types", [])
        if context.project_type in project_types:
            confidence += 0.1

        return min(1.0, confidence)

    def _estimate_impact(self, context: SuggestionContext) -> str:
        """Estimate the impact of this suggestion."""
        impact_scores = {
            "critical_fix": "Critical",
            "feature_addition": "High",
            "quality_improvement": "Medium",
            "documentation": "Medium",
            "optimization": "Low",
            "cleanup": "Low",
        }

        return impact_scores.get(self.category, "Medium")

    def _get_prerequisites(self, context: SuggestionContext) -> List[str]:
        """Get prerequisites for this suggestion."""
        prerequisites = self.conditions.get("prerequisites", [])
        if isinstance(prerequisites, str):
            prerequisites = [prerequisites]
        return prerequisites

    def _identify_risks(self, context: SuggestionContext) -> List[str]:
        """Identify potential risks for this suggestion."""
        risks = []

        if self.conditions.get("requires_backup", False):
            risks.append("May require backup before execution")

        if self.conditions.get("destructive", False):
            risks.append("Destructive operation - review carefully")

        if context.quality_score and context.quality_score < 60:
            risks.append("Low quality score may affect results")

        return risks


class IntelligentSuggestionEngine:
    """
    Intelligent suggestion engine that provides context-aware recommendations
    """
    based on user preferences, learned patterns, and system state.
    """

    def __init__(self, storage_dir: str = ".claude-preferences"):
        """
        Initialize suggestion engine.

        Args:
            storage_dir: Directory for storing suggestion data
        """
        self.storage_dir = Path(storage_dir)
        self.suggestions_file = self.storage_dir / "suggestions_database.json"
        self.templates_file = self.storage_dir / "suggestion_templates.json"
        self.analytics_file = self.storage_dir / "suggestion_analytics.json"

        # Thread safety
        self._lock = threading.RLock()

        # Initialize subsystems
        try:
            self.preference_memory = UserPreferenceMemory(storage_dir)
            self.parameter_storage = UnifiedParameterStorage(str(storage_dir).replace("-preferences", "-unified"))
        except Exception as e:
            print(f"Warning: Could not initialize subsystems: {e}", file=sys.stderr)
            self.preference_memory = None
            self.parameter_storage = None

        # Suggestion templates
        self.templates = []
        self._load_templates()

        # Analytics
        self.analytics = {
            "total_suggestions_generated": 0,
            "total_suggestions_accepted": 0,
            "category_effectiveness": {},
            "template_usage": {},
            "user_response_patterns": {},
            "generation_trends": [],
        }

        self._ensure_directories()
        self._load_analytics()

    def _ensure_directories(self):
        """Create necessary directories."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _load_templates(self):
        """Load suggestion templates."""
        if self.templates_file.exists():
            try:
                with open(self.templates_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.templates = [SuggestionTemplate(**t) for t in data.get("templates", [])]
            except Exception as e:
                print(f"Error loading templates: {e}", file=sys.stderr)
                self.templates = []

        # Load default templates if none exist
        if not self.templates:
            self._load_default_templates()
            self._save_templates()

    def _load_default_templates(self):
        """Load default suggestion templates."""
        default_templates = [
            # Quality improvement templates
            {
                "template_id": "quality_check_low_score",
                "category": "quality_improvement",
                "priority": "high",
                "description_template": "Quality score is {quality_score}/100. Run comprehensive quality check to identify and fix issues.",
                "command_template": "/analyze:quality",
                "conditions": {"min_quality_score": 0, "max_quality_score": 75, "exclude_if_recent": ["/analyze:quality"]},
                "weights": {"relevance": 0.8, "urgency": 0.9, "impact": 0.7},
            },
            {
                "template_id": "fix_failing_tests",
                "category": "quality_improvement",
                "priority": "critical",
                "description_template": "Tests are failing. Auto-debug and fix test failures to ensure code reliability.",
                "command_template": '/dev:auto "fix failing tests"',
                "conditions": {
                    "project_types": ["python", "javascript", "typescript", "java"],
                    "exclude_if_recent": ["/dev:auto"],
                },
                "weights": {"relevance": 0.9, "urgency": 1.0, "impact": 0.8},
            },
            # Documentation templates
            {
                "template_id": "update_docs_coverage",
                "category": "documentation",
                "priority": "medium",
                "description_template": "Documentation coverage is low. Generate comprehensive documentation for {primary_language} project.",
                "command_template": '/dev:auto "update documentation for {project_type} project"',
                "conditions": {"project_types": ["unknown", "prototype"], "exclude_if_recent": ["/dev:auto"]},
                "weights": {"relevance": 0.6, "urgency": 0.5, "impact": 0.7},
            },
            # Optimization templates
            {
                "template_id": "performance_optimization",
                "category": "optimization",
                "priority": "low",
                "description_template": "Performance bottlenecks detected. Optimize {primary_language} code for better performance.",
                "command_template": '/dev:auto "optimize performance bottlenecks"',
                "conditions": {"min_quality_score": 70, "base_time": 15, "exclude_if_recent": ["/dev:auto"]},
                "weights": {"relevance": 0.5, "urgency": 0.3, "impact": 0.8},
            },
            # Security templates
            {
                "template_id": "security_scan",
                "category": "security",
                "priority": "high",
                "description_template": "Run security vulnerability scan to identify potential security issues.",
                "command_template": "/analyze:dependencies",
                "conditions": {
                    "project_types": ["python", "javascript", "typescript", "java", "go"],
                    "exclude_if_recent": ["/analyze:dependencies"],
                },
                "weights": {"relevance": 0.7, "urgency": 0.8, "impact": 0.9},
            },
            # Task queue templates
            {
                "template_id": "queue_tasks_batch",
                "category": "workflow",
                "priority": "medium",
                "description_template": "Multiple tasks pending. Add to queue for sequential execution without interruption.",
                "command_template": '/queue:slash --command "/analyze:project" --priority high',
                "conditions": {"min_time_available": 10, "exclude_if_recent": ["/queue:slash"]},
                "weights": {"relevance": 0.6, "urgency": 0.5, "impact": 0.6},
            },
            # Learning templates
            {
                "template_id": "review_analytics",
                "category": "learning",
                "priority": "low",
                "description_template": "Review performance analytics and learned patterns to improve future suggestions.",
                "command_template": "/learn:analytics",
                "conditions": {"exclude_if_recent": ["/learn:analytics"], "base_time": 2},
                "weights": {"relevance": 0.4, "urgency": 0.2, "impact": 0.5},
            },
            # Release templates
            {
                "template_id": "prepare_release",
                "category": "release",
                "priority": "high",
                "description_template": "Project quality is good. Prepare for release with changelog and version bump.",
                "command_template": "/dev:release --minor",
                "conditions": {"min_quality_score": 85, "exclude_if_recent": ["/dev:release"]},
                "weights": {"relevance": 0.8, "urgency": 0.7, "impact": 0.9},
            },
        ]

        self.templates = [SuggestionTemplate(**template) for template in default_templates]

    def _save_templates(self):
        """Save suggestion templates to file."""
        try:
            templates_data = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "templates": [
                    {
                        "template_id": t.template_id,
                        "category": t.category,
                        "priority": t.priority,
                        "description_template": t.description_template,
                        "command_template": t.command_template,
                        "conditions": t.conditions,
                        "weights": t.weights,
                        "usage_count": t.usage_count,
                        "success_count": t.success_count,
                    }
                    for t in self.templates
                ],
            }

            with open(self.templates_file, "w", encoding="utf-8") as f:
                json.dump(templates_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving templates: {e}", file=sys.stderr)

    def _load_analytics(self):
        """Load analytics data."""
        if self.analytics_file.exists():
            try:
                with open(self.analytics_file, "r", encoding="utf-8") as f:
                    self.analytics = json.load(f)
            except Exception as e:
                print(f"Error loading analytics: {e}", file=sys.stderr)

    def _save_analytics(self):
        """Save analytics data."""
        try:
            self.analytics["last_updated"] = datetime.now().isoformat()
            with open(self.analytics_file, "w", encoding="utf-8") as f:
                json.dump(self.analytics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving analytics: {e}", file=sys.stderr)

    def generate_suggestions(
        self, context: SuggestionContext, max_suggestions: int = 5, include_learning: bool = True
    )-> List[Dict[str, Any]]:
        """Generate Suggestions."""
        Generate intelligent suggestions based on context.

        Args:
            context: Current context for suggestion generation
            max_suggestions: Maximum number of suggestions to return
            include_learning: Whether to include learning-based suggestions

        Returns:
            List of ranked suggestions
        """
        with self._lock:
            suggestions = []

            # Generate suggestions from templates
            for template in self.templates:
                suggestion = template.generate_suggestion(context)
                if suggestion:
                    suggestions.append(suggestion)

            # Add learning-based suggestions
            if include_learning and self.preference_memory:
                learned_suggestions = self._generate_learned_suggestions(context)
                suggestions.extend(learned_suggestions)

            # Add environment-based suggestions
            if self.parameter_storage:
                env_suggestions = self._generate_environment_suggestions(context)
                suggestions.extend(env_suggestions)

            # Score and rank suggestions
            scored_suggestions = self._score_and_rank_suggestions(suggestions, context)

            # Filter and return top suggestions
            filtered_suggestions = self._filter_suggestions(scored_suggestions, context)
            final_suggestions = filtered_suggestions[:max_suggestions]

            # Update analytics
            self._update_generation_analytics(final_suggestions, context)

            return final_suggestions

    def _generate_learned_suggestions(self, context: SuggestionContext) -> List[Dict[str, Any]]:
        """Generate suggestions based on learned patterns."""
        suggestions = []

        if not self.preference_memory:
            return suggestions

        # Get user profile and learned patterns
        profile = self.preference_memory.get_user_profile()
        learned_patterns = profile.get("learned_patterns", {})

        # Generate suggestions from command preferences
        command_prefs = learned_patterns.get("command_preferences", {})
        for command, stats in command_prefs.items():
            if stats.get("usage_count", 0) >= 3 and stats.get("success_rate", 0) >= 0.8:
                # Check if command was used recently
                recent_commands = context.recent_commands[-5:]  # Last 5 commands
                if not any(command in cmd for cmd in recent_commands):
                    suggestion = {
                        "template_id": f"learned_{hash(command) % 10000}",
                        "category": "learned_preference",
                        "priority": "medium",
                        "description": f"Previously successful command: {command}",
                        "command": command,
                        "estimated_time": "2-5 minutes",
                        "confidence": stats.get("success_rate", 0.5),
                        "impact": "Medium",
                        "prerequisites": [],
                        "risks": [],
                        "source": "learned_pattern",
                        "usage_count": stats.get("usage_count", 0),
                    }
                    suggestions.append(suggestion)

        return suggestions

    def _generate_environment_suggestions(self, context: SuggestionContext) -> List[Dict[str, Any]]:
        """Generate suggestions based on system environment."""
        suggestions = []

        if not self.parameter_storage:
            return suggestions

        try:
            # Get dashboard data
            dashboard_data = self.parameter_storage.get_dashboard_data()
            quality_score = dashboard_data.get("quality", {}).get("scores", {}).get("current", 0)

            # System-specific suggestions
            if context.system_environment.get("system", {}).get("platform") == "Windows":
                if "Windows" not in str(context.recent_commands):
                    suggestion = {
                        "template_id": "windows_optimization",
                        "category": "environment",
                        "priority": "low",
                        "description": "Optimize development environment for Windows",
                        "command": '/dev:auto "optimize windows development environment"',
                        "estimated_time": "5-10 minutes",
                        "confidence": 0.6,
                        "impact": "Low",
                        "prerequisites": [],
                        "risks": [],
                        "source": "environment",
                    }
                    suggestions.append(suggestion)

            # Resource-based suggestions
            memory_usage = context.system_environment.get("hardware", {}).get("memory", {}).get("usage_percent", 0)
            if memory_usage > 80:
                suggestion = {
                    "template_id": "memory_optimization",
                    "category": "environment",
                    "priority": "medium",
                    "description": f"High memory usage ({memory_usage}%). Consider optimization.",
                    "command": '/dev:auto "optimize memory usage"',
                    "estimated_time": "3-7 minutes",
                    "confidence": 0.7,
                    "impact": "Medium",
                    "prerequisites": [],
                    "risks": [],
                    "source": "environment",
                }
                suggestions.append(suggestion)

        except Exception as e:
            print(f"Error generating environment suggestions: {e}", file=sys.stderr)

        return suggestions

    def _score_and_rank_suggestions(
        self, suggestions: List[Dict[str, Any]], context: SuggestionContext
    )-> List[Tuple[Dict[str, Any], float]]:
        """ Score And Rank Suggestions."""Score and rank suggestions using multi-factor algorithm."""
        scored_suggestions = []

        for suggestion in suggestions:
            score = self._calculate_suggestion_score(suggestion, context)
            scored_suggestions.append((suggestion, score))

        # Sort by score (descending)
        scored_suggestions.sort(key=lambda x: x[1], reverse=True)
        return scored_suggestions

    def _calculate_suggestion_score(self, suggestion: Dict[str, Any], context: SuggestionContext) -> float:
        """Calculate comprehensive score for a suggestion."""
        score = 0.0

        # Base confidence
        score += suggestion.get("confidence", 0.5) * 0.3

        # Priority weighting
        priority_weights = {"critical": 1.0, "high": 0.8, "medium": 0.6, "low": 0.4}
        score += priority_weights.get(suggestion.get("priority", "medium"), 0.5) * 0.2

        # Impact weighting
        impact_weights = {"Critical": 1.0, "High": 0.8, "Medium": 0.6, "Low": 0.4}
        score += impact_weights.get(suggestion.get("impact", "Medium"), 0.5) * 0.2

        # Context relevance
        if suggestion.get("category") == "quality_improvement" and context.quality_score and context.quality_score < 70:
            score += 0.2

        # User preference alignment
        if self.preference_memory:
            pref_quality_threshold = self.preference_memory.get_preference("workflow", "quality_threshold", 70)
            if (
                suggestion.get("category") == "quality_improvement"
                and context.quality_score
                and context.quality_score < pref_quality_threshold
            ):
                score += 0.1

        # Recent usage penalty (avoid suggesting the same thing repeatedly)
        recent_commands = context.recent_commands[-3:]
        if suggestion.get("command") and any(suggestion.get("command") in cmd for cmd in recent_commands):
            score -= 0.3

        return max(0.0, min(1.0, score))

    def _filter_suggestions(
        self, scored_suggestions: List[Tuple[Dict[str, Any], float]], context: SuggestionContext
    )-> List[Dict[str, Any]]:
        """ Filter Suggestions."""Filter suggestions based on various criteria."""
        filtered = []

        for suggestion, score in scored_suggestions:
            # Skip low-confidence suggestions
            if score < 0.3:
                continue

            # Skip if prerequisites aren't met
            prerequisites = suggestion.get("prerequisites", [])
            if prerequisites:
                # Check if prerequisites are satisfied (simplified check)
                if any("not available" in str(context.system_environment) for prereq in prerequisites):
                    continue

            # Skip high-risk suggestions if quality is low
            if suggestion.get("risks") and context.quality_score and context.quality_score < 50:
                high_risk = any(
                    "destructive" in risk.lower() or "critical" in risk.lower() for risk in suggestion.get("risks")
                )
                if high_risk:
                    continue

            # Add score to suggestion
            suggestion["score"] = score
            filtered.append(suggestion)

        return filtered

    def _update_generation_analytics(self, suggestions: List[Dict[str, Any]], context: SuggestionContext):
        """Update analytics with suggestion generation data."""
        self.analytics["total_suggestions_generated"] += len(suggestions)

        # Update category effectiveness
        for suggestion in suggestions:
            category = suggestion.get("category", "unknown")
            if category not in self.analytics["category_effectiveness"]:
                self.analytics["category_effectiveness"][category] = {"generated": 0, "accepted": 0, "success_rate": 0.0}
            self.analytics["category_effectiveness"][category]["generated"] += 1

        # Add to generation trends
        trend_entry = {
            "timestamp": datetime.now().isoformat(),
            "suggestions_count": len(suggestions),
            "average_confidence": sum(s.get("confidence", 0) for s in suggestions) / len(suggestions) if suggestions else 0,
            "context_quality": context.quality_score or 0,
            "project_type": context.project_type or "unknown",
        }
        self.analytics["generation_trends"].append(trend_entry)

        # Keep only last 100 trend entries
        if len(self.analytics["generation_trends"]) > 100:
            self.analytics["generation_trends"] = self.analytics["generation_trends"][-100:]

        self._save_analytics()

    def record_suggestion_response(self, suggestion: Dict[str, Any], accepted: bool, context: SuggestionContext):
        """Record user response to a suggestion."""
        # Update template usage statistics
        template_id = suggestion.get("template_id")
        if template_id:
            for template in self.templates:
                if template.template_id == template_id:
                    template.usage_count += 1
                    if accepted:
                        template.success_count += 1
                    break

        # Update analytics
        self.analytics["total_suggestions_accepted"] += 1 if accepted else 0

        category = suggestion.get("category", "unknown")
        if category in self.analytics["category_effectiveness"]:
            self.analytics["category_effectiveness"][category]["accepted"] += 1 if accepted else 0
            total = self.analytics["category_effectiveness"][category]["generated"]
            accepted = self.analytics["category_effectiveness"][category]["accepted"]
            self.analytics["category_effectiveness"][category]["success_rate"] = accepted / total if total > 0 else 0

        # Record in preference memory if available
        if self.preference_memory:
            self.preference_memory.record_suggestion_response(
                suggestion.get("command", ""),
                accepted,
                {
                    "category": category,
                    "confidence": suggestion.get("confidence", 0),
                    "context_quality": context.quality_score,
                },
            )

        self._save_analytics()
        self._save_templates()

    def get_suggestion_analytics(self) -> Dict[str, Any]:
        """Get comprehensive suggestion analytics."""
        return {
            "analytics": self.analytics,
            "template_performance": [
                {
                    "template_id": t.template_id,
                    "category": t.category,
                    "usage_count": t.usage_count,
                    "success_count": t.success_count,
                    "success_rate": t.success_count / t.usage_count if t.usage_count > 0 else 0,
                }
                for t in self.templates
            ],
            "most_effective_categories": sorted(
                self.analytics["category_effectiveness"].items(), key=lambda x: x[1]["success_rate"], reverse=True
            ),
        }

    def create_custom_template(
        self,
        template_id: str,
        category: str,
        priority: str,
        description_template: str,
        command_template: str,
        conditions: Dict[str, Any],
        weights: Dict[str, Any],
    )-> bool:
        """Create Custom Template."""Create a custom suggestion template."""
        # Check if template already exists
        for template in self.templates:
            if template.template_id == template_id:
                return False

        new_template = SuggestionTemplate(
            template_id, category, priority, description_template, command_template, conditions, weights
        )

        self.templates.append(new_template)
        self._save_templates()
        return True

    def delete_template(self, template_id: str) -> bool:
        """Delete a suggestion template."""
        for i, template in enumerate(self.templates):
            if template.template_id == template_id:
                del self.templates[i]
                self._save_templates()
                return True
        return False

    def update_template_usage(self, template_id: str, success: bool):
        """Update template usage statistics."""
        for template in self.templates:
            if template.template_id == template_id:
                template.usage_count += 1
                if success:
                    template.success_count += 1
                break

        self._save_templates()


def main():
    """Command-line interface for intelligent suggestion engine."""
    import argparse

    parser = argparse.ArgumentParser(description="Intelligent Suggestion Engine")
    parser.add_argument("--dir", default=".claude-preferences", help="Storage directory path")

    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Generate suggestions
    gen_parser = subparsers.add_parser("generate", help="Generate suggestions")
    gen_parser.add_argument("--max", type=int, default=5, help="Maximum suggestions")
    gen_parser.add_argument("--quality", type=float, help="Current quality score")
    gen_parser.add_argument("--project-type", help="Project type")

    # Analytics
    subparsers.add_parser("analytics", help="Show suggestion analytics")

    # Template management
    template_parser = subparsers.add_parser("template", help="Template operations")
    template_subparsers = template_parser.add_subparsers(dest="template_action")

    # List templates
    template_subparsers.add_parser("list", help="List templates")

    # Add template
    add_template_parser = template_subparsers.add_parser("add", help="Add template")
    add_template_parser.add_argument("--id", required=True, help="Template ID")
    add_template_parser.add_argument("--category", required=True, help="Category")
    add_template_parser.add_argument("--priority", required=True, help="Priority")
    add_template_parser.add_argument("--description", required=True, help="Description template")
    add_template_parser.add_argument("--command", required=True, help="Command template")

    # Delete template
    del_template_parser = template_subparsers.add_parser("delete", help="Delete template")
    del_template_parser.add_argument("--id", required=True, help="Template ID")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    engine = IntelligentSuggestionEngine(args.dir)

    try:
        if args.action == "generate":
            context = SuggestionContext()
            context.quality_score = args.quality
            context.project_type = args.project_type
            context.recent_commands = []  # Would be populated from actual session

            suggestions = engine.generate_suggestions(context, args.max)
            print(json.dumps(suggestions, indent=2))

        elif args.action == "analytics":
            analytics = engine.get_suggestion_analytics()
            print(json.dumps(analytics, indent=2))

        elif args.action == "template":
            if args.template_action == "list":
                templates = [
                    {
                        "id": t.template_id,
                        "category": t.category,
                        "priority": t.priority,
                        "usage_count": t.usage_count,
                        "success_rate": t.success_count / t.usage_count if t.usage_count > 0 else 0,
                    }
                    for t in engine.templates
                ]
                print(json.dumps(templates, indent=2))

            elif args.template_action == "add":
                success = engine.create_custom_template(
                    args.id,
                    args.category,
                    args.priority,
                    args.description,
                    args.command,
                    {},
                    {},  # Empty conditions and weights for CLI
                )
                print(f"[OK] Template {'created' if success else 'already exists'}")

            elif args.template_action == "delete":
                success = engine.delete_template(args.id)
                print(f"[OK] Template {'deleted' if success else 'not found'}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
