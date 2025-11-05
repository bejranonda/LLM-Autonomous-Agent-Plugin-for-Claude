#!/usr/bin/env python3
"""
Proactive Suggester for Four-Tier Agent Architecture
====================================================

Purpose: Proactively suggests improvements without being asked

Key Features:
- Analyzes project patterns and identifies improvement opportunities
- Generates suggestions based on code quality trends, security gaps, technical debt
- Prioritizes by urgency (high/medium/low) with effort/impact estimates
- Tracks suggestion acceptance and effectiveness
- Learns from user preferences and suggestion outcomes
- Integrates with inter-group knowledge transfer system

Suggestion Types:
- Security: Vulnerabilities, outdated dependencies, missing security measures
- Performance: Bottlenecks, optimization opportunities, resource inefficiencies
- Quality: Code smells, standards violations, technical debt
- Documentation: Missing docs, outdated guides, unclear APIs
- Testing: Coverage gaps, flaky tests, missing edge cases
- Technical Debt: Old TODOs, deprecated code, refactoring opportunities

Enhancement: v7.1 - High Impact, Low Complexity
Target: 30+ proactive suggestions per 100 tasks
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import platform

# Platform-specific file locking
if platform.system() == 'Windows':
    import msvcrt

    def lock_file(f):
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)

    def unlock_file(f):
        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
else:
    import fcntl

    def lock_file(f):
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)

    def unlock_file(f):
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class ProactiveSuggester:
    """Proactively suggests improvements based on project patterns and trends"""

    def __init__(self, data_dir: str = ".claude-patterns"):
        self.data_dir = data_dir
        self.suggestions_file = os.path.join(data_dir, "proactive_suggestions.json")
        self._ensure_data_dir()
        self._ensure_suggestions_file()

    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _ensure_suggestions_file(self):
        """Ensure suggestions file exists with initial structure"""
        if not os.path.exists(self.suggestions_file):
            initial_data = {
                "suggestions": [],
                "acceptance_stats": {
                    "total_suggestions": 0,
                    "accepted": 0,
                    "rejected": 0,
                    "ignored": 0,
                    "acceptance_rate": 0.0
                },
                "effectiveness_by_type": {},
                "user_preferences": {
                    "preferred_types": [],
                    "preferred_urgency": "medium",
                    "preferred_effort": "low_to_medium"
                },
                "learning_insights": []
            }
            self._write_data(initial_data)

    def _read_data(self) -> Dict:
        """Thread-safe read of suggestions data"""
        try:
            with open(self.suggestions_file, 'r', encoding='utf-8') as f:
                lock_file(f)
                try:
                    data = json.load(f)
                finally:
                    unlock_file(f)
            return data
        except Exception as e:
            print(f"Error reading suggestions data: {e}")
            return self._get_empty_data()

    def _write_data(self, data: Dict):
        """Thread-safe write of suggestions data"""
        try:
            with open(self.suggestions_file, 'w', encoding='utf-8') as f:
                lock_file(f)
                try:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error writing suggestions data: {e}")

    def _get_empty_data(self) -> Dict:
        """Get empty data structure"""
        return {
            "suggestions": [],
            "acceptance_stats": {
                "total_suggestions": 0,
                "accepted": 0,
                "rejected": 0,
                "ignored": 0,
                "acceptance_rate": 0.0
            },
            "effectiveness_by_type": {},
            "user_preferences": {
                "preferred_types": [],
                "preferred_urgency": "medium",
                "preferred_effort": "low_to_medium"
            },
            "learning_insights": []
        }

    def create_suggestion(
        self,
        suggestion_type: str,
        title: str,
        description: str,
        rationale: str,
        urgency: str,
        estimated_effort_hours: float,
        expected_impact: str,
        context: Optional[Dict] = None,
        related_files: Optional[List[str]] = None,
        related_patterns: Optional[List[str]] = None
    ) -> str:
        """
        Create a new proactive suggestion

        Args:
            suggestion_type: Type of suggestion (security, performance, quality, documentation, testing, technical_debt)
            title: Brief title describing the suggestion
            description: Detailed description of what should be done
            rationale: Why this suggestion is important now
            urgency: Urgency level (high, medium, low)
            estimated_effort_hours: Estimated implementation effort in hours
            expected_impact: Expected impact (high, medium, low)
            context: Additional context (code quality trends, recent events, etc.)
            related_files: List of files related to this suggestion
            related_patterns: List of related patterns from pattern database

        Returns:
            Suggestion ID
        """
        data = self._read_data()

        # Generate suggestion ID
        suggestion_id = f"suggestion_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(data['suggestions']) + 1}"

        # Calculate priority score (0-100)
        urgency_scores = {"high": 40, "medium": 25, "low": 10}
        impact_scores = {"high": 40, "medium": 25, "low": 10}
        effort_scores = {
            (0, 2): 20,      # Quick wins
            (2, 8): 15,      # Moderate effort
            (8, 24): 10,     # Significant effort
            (24, 999): 5     # Major undertaking
        }

        urgency_score = urgency_scores.get(urgency.lower(), 25)
        impact_score = impact_scores.get(expected_impact.lower(), 25)

        # Effort score (inverse - less effort = higher score)
        effort_score = 10
        for (min_hours, max_hours), score in effort_scores.items():
            if min_hours <= estimated_effort_hours < max_hours:
                effort_score = score
                break

        priority_score = urgency_score + impact_score + effort_score

        # Determine category
        if priority_score >= 80:
            category = "critical_quick_win"
        elif priority_score >= 60 and estimated_effort_hours <= 4:
            category = "quick_win"
        elif priority_score >= 60:
            category = "strategic_improvement"
        else:
            category = "nice_to_have"

        suggestion = {
            "suggestion_id": suggestion_id,
            "type": suggestion_type,
            "title": title,
            "description": description,
            "rationale": rationale,
            "urgency": urgency,
            "estimated_effort_hours": estimated_effort_hours,
            "expected_impact": expected_impact,
            "priority_score": priority_score,
            "category": category,
            "status": "pending",
            "context": context or {},
            "related_files": related_files or [],
            "related_patterns": related_patterns or [],
            "created_at": datetime.now().isoformat(),
            "acceptance_status": None,  # None, "accepted", "rejected", "ignored"
            "acceptance_timestamp": None,
            "implementation_outcome": None,  # Track if implemented successfully
            "impact_measured": None  # Actual measured impact
        }

        data["suggestions"].append(suggestion)
        data["acceptance_stats"]["total_suggestions"] += 1

        self._write_data(data)
        return suggestion_id

    def get_suggestions(
        self,
        status: Optional[str] = None,
        suggestion_type: Optional[str] = None,
        urgency: Optional[str] = None,
        category: Optional[str] = None,
        min_priority_score: Optional[float] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get suggestions with optional filtering

        Args:
            status: Filter by status (pending, accepted, rejected, ignored, implemented)
            suggestion_type: Filter by type
            urgency: Filter by urgency level
            category: Filter by category (critical_quick_win, quick_win, strategic_improvement, nice_to_have)
            min_priority_score: Minimum priority score
            limit: Maximum number of suggestions to return

        Returns:
            List of suggestions sorted by priority score (descending)
        """
        data = self._read_data()
        suggestions = data["suggestions"]

        # Apply filters
        if status:
            suggestions = [s for s in suggestions if s["status"] == status]
        if suggestion_type:
            suggestions = [s for s in suggestions if s["type"] == suggestion_type]
        if urgency:
            suggestions = [s for s in suggestions if s["urgency"] == urgency]
        if category:
            suggestions = [s for s in suggestions if s["category"] == category]
        if min_priority_score is not None:
            suggestions = [s for s in suggestions if s["priority_score"] >= min_priority_score]

        # Sort by priority score (descending)
        suggestions.sort(key=lambda x: x["priority_score"], reverse=True)

        return suggestions[:limit]

    def record_acceptance(
        self,
        suggestion_id: str,
        acceptance_status: str,
        feedback: Optional[str] = None
    ):
        """
        Record user's response to a suggestion

        Args:
            suggestion_id: ID of the suggestion
            acceptance_status: User response (accepted, rejected, ignored)
            feedback: Optional user feedback
        """
        data = self._read_data()

        for suggestion in data["suggestions"]:
            if suggestion["suggestion_id"] == suggestion_id:
                suggestion["acceptance_status"] = acceptance_status
                suggestion["acceptance_timestamp"] = datetime.now().isoformat()
                if feedback:
                    suggestion["user_feedback"] = feedback

                # Update stats
                data["acceptance_stats"][acceptance_status] += 1

                # Calculate new acceptance rate
                total = data["acceptance_stats"]["total_suggestions"]
                if total > 0:
                    accepted = data["acceptance_stats"]["accepted"]
                    data["acceptance_stats"]["acceptance_rate"] = accepted / total

                # Update status
                if acceptance_status == "accepted":
                    suggestion["status"] = "accepted"
                elif acceptance_status == "rejected":
                    suggestion["status"] = "rejected"
                else:
                    suggestion["status"] = "ignored"

                break

        self._write_data(data)
        self._update_user_preferences()

    def record_implementation_outcome(
        self,
        suggestion_id: str,
        success: bool,
        impact_measured: str,
        actual_effort_hours: Optional[float] = None,
        quality_improvement: Optional[float] = None,
        notes: Optional[str] = None
    ):
        """
        Record the outcome of implementing a suggestion

        Args:
            suggestion_id: ID of the suggestion
            success: Whether implementation was successful
            impact_measured: Actual measured impact (high, medium, low)
            actual_effort_hours: Actual hours spent (vs estimated)
            quality_improvement: Quality score improvement (if applicable)
            notes: Additional notes about implementation
        """
        data = self._read_data()

        for suggestion in data["suggestions"]:
            if suggestion["suggestion_id"] == suggestion_id:
                suggestion["implementation_outcome"] = "success" if success else "failure"
                suggestion["impact_measured"] = impact_measured
                suggestion["status"] = "implemented"
                suggestion["implementation_timestamp"] = datetime.now().isoformat()

                if actual_effort_hours is not None:
                    suggestion["actual_effort_hours"] = actual_effort_hours
                    suggestion["effort_accuracy"] = 1.0 - abs(
                        actual_effort_hours - suggestion["estimated_effort_hours"]
                    ) / max(suggestion["estimated_effort_hours"], 1)

                if quality_improvement is not None:
                    suggestion["quality_improvement"] = quality_improvement

                if notes:
                    suggestion["implementation_notes"] = notes

                # Update effectiveness by type
                suggestion_type = suggestion["type"]
                if suggestion_type not in data["effectiveness_by_type"]:
                    data["effectiveness_by_type"][suggestion_type] = {
                        "total": 0,
                        "successful": 0,
                        "success_rate": 0.0,
                        "average_impact": 0.0,
                        "average_effort_accuracy": 0.0
                    }

                type_stats = data["effectiveness_by_type"][suggestion_type]
                type_stats["total"] += 1
                if success:
                    type_stats["successful"] += 1
                type_stats["success_rate"] = type_stats["successful"] / type_stats["total"]

                break

        self._write_data(data)

    def _update_user_preferences(self):
        """Update user preferences based on acceptance patterns"""
        data = self._read_data()

        # Analyze accepted suggestions to identify preferences
        accepted_suggestions = [
            s for s in data["suggestions"]
            if s["acceptance_status"] == "accepted"
        ]

        if len(accepted_suggestions) < 3:
            return  # Not enough data yet

        # Find preferred types
        type_counts = {}
        urgency_counts = {}
        effort_ranges = {"low": 0, "medium": 0, "high": 0}

        for suggestion in accepted_suggestions:
            # Count types
            stype = suggestion["type"]
            type_counts[stype] = type_counts.get(stype, 0) + 1

            # Count urgency
            urgency = suggestion["urgency"]
            urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1

            # Count effort ranges
            effort = suggestion["estimated_effort_hours"]
            if effort <= 4:
                effort_ranges["low"] += 1
            elif effort <= 16:
                effort_ranges["medium"] += 1
            else:
                effort_ranges["high"] += 1

        # Update preferences
        preferred_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        data["user_preferences"]["preferred_types"] = [t[0] for t in preferred_types[:3]]

        preferred_urgency = max(urgency_counts.items(), key=lambda x: x[1])[0]
        data["user_preferences"]["preferred_urgency"] = preferred_urgency

        preferred_effort = max(effort_ranges.items(), key=lambda x: x[1])[0]
        data["user_preferences"]["preferred_effort"] = preferred_effort

        self._write_data(data)

    def get_top_suggestions(
        self,
        count: int = 5,
        consider_preferences: bool = True
    ) -> List[Dict]:
        """
        Get top priority suggestions, optionally considering user preferences

        Args:
            count: Number of suggestions to return
            consider_preferences: Whether to boost suggestions matching user preferences

        Returns:
            List of top suggestions
        """
        data = self._read_data()
        suggestions = [s for s in data["suggestions"] if s["status"] == "pending"]

        if consider_preferences and len(data["user_preferences"]["preferred_types"]) > 0:
            # Boost priority scores for preferred types
            for suggestion in suggestions:
                if suggestion["type"] in data["user_preferences"]["preferred_types"]:
                    suggestion["adjusted_priority_score"] = suggestion["priority_score"] * 1.2
                else:
                    suggestion["adjusted_priority_score"] = suggestion["priority_score"]

            # Sort by adjusted score
            suggestions.sort(key=lambda x: x.get("adjusted_priority_score", x["priority_score"]), reverse=True)
        else:
            # Sort by original priority score
            suggestions.sort(key=lambda x: x["priority_score"], reverse=True)

        return suggestions[:count]

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics about suggestions"""
        data = self._read_data()

        total_suggestions = len(data["suggestions"])
        pending = len([s for s in data["suggestions"] if s["status"] == "pending"])
        accepted = len([s for s in data["suggestions"] if s["acceptance_status"] == "accepted"])
        implemented = len([s for s in data["suggestions"] if s["status"] == "implemented"])

        # Success rate of implemented suggestions
        implemented_suggestions = [s for s in data["suggestions"] if s["status"] == "implemented"]
        successful_implementations = len([
            s for s in implemented_suggestions
            if s["implementation_outcome"] == "success"
        ])

        implementation_success_rate = 0.0
        if len(implemented_suggestions) > 0:
            implementation_success_rate = successful_implementations / len(implemented_suggestions)

        # Average priority by category
        categories = ["critical_quick_win", "quick_win", "strategic_improvement", "nice_to_have"]
        category_counts = {cat: 0 for cat in categories}
        for suggestion in data["suggestions"]:
            category_counts[suggestion["category"]] += 1

        return {
            "total_suggestions": total_suggestions,
            "pending": pending,
            "accepted": accepted,
            "implemented": implemented,
            "acceptance_rate": data["acceptance_stats"]["acceptance_rate"],
            "implementation_success_rate": implementation_success_rate,
            "effectiveness_by_type": data["effectiveness_by_type"],
            "user_preferences": data["user_preferences"],
            "category_distribution": category_counts,
            "suggestions_per_category": {
                "critical_quick_wins": category_counts["critical_quick_win"],
                "quick_wins": category_counts["quick_win"],
                "strategic": category_counts["strategic_improvement"],
                "nice_to_have": category_counts["nice_to_have"]
            }
        }

    def analyze_project_and_suggest(
        self,
        project_context: Dict,
        patterns_data: Optional[Dict] = None,
        quality_data: Optional[Dict] = None,
        performance_data: Optional[Dict] = None
    ) -> List[str]:
        """
        Analyze project state and generate suggestions automatically

        Args:
            project_context: Current project context (languages, frameworks, etc.)
            patterns_data: Data from patterns.json
            quality_data: Data from quality tracking
            performance_data: Data from performance tracking

        Returns:
            List of suggestion IDs created
        """
        suggestion_ids = []

        # Analyze code quality trends
        if quality_data:
            suggestion_ids.extend(self._analyze_quality_trends(quality_data, project_context))

        # Analyze performance patterns
        if performance_data:
            suggestion_ids.extend(self._analyze_performance_patterns(performance_data, project_context))

        # Analyze pattern usage
        if patterns_data:
            suggestion_ids.extend(self._analyze_pattern_usage(patterns_data, project_context))

        return suggestion_ids

    def _analyze_quality_trends(self, quality_data: Dict, context: Dict) -> List[str]:
        """Analyze quality trends and generate suggestions"""
        suggestion_ids = []

        # Check if quality is declining
        if quality_data.get("trend") == "declining":
            suggestion_id = self.create_suggestion(
                suggestion_type="quality",
                title="Address Declining Code Quality",
                description="Code quality scores have been declining over recent tasks. Run comprehensive quality analysis and address identified issues.",
                rationale=f"Quality trend is declining. Current score: {quality_data.get('current_score', 'N/A')}",
                urgency="high",
                estimated_effort_hours=4.0,
                expected_impact="high",
                context={"quality_data": quality_data, "project_context": context}
            )
            suggestion_ids.append(suggestion_id)

        return suggestion_ids

    def _analyze_performance_patterns(self, performance_data: Dict, context: Dict) -> List[str]:
        """Analyze performance patterns and generate suggestions"""
        suggestion_ids = []

        # Check for performance regressions
        if performance_data.get("regression_detected"):
            suggestion_id = self.create_suggestion(
                suggestion_type="performance",
                title="Investigate Performance Regression",
                description="Performance metrics show regression in execution time or resource usage. Profile and optimize affected components.",
                rationale="Performance regression detected in recent changes",
                urgency="medium",
                estimated_effort_hours=6.0,
                expected_impact="medium",
                context={"performance_data": performance_data, "project_context": context}
            )
            suggestion_ids.append(suggestion_id)

        return suggestion_ids

    def _analyze_pattern_usage(self, patterns_data: Dict, context: Dict) -> List[str]:
        """Analyze pattern usage and generate suggestions"""
        suggestion_ids = []

        # Check for underutilized successful patterns
        patterns = patterns_data.get("patterns", [])
        successful_patterns = [
            p for p in patterns
            if p.get("outcome", {}).get("success", False)
            and p.get("outcome", {}).get("quality_score", 0) >= 85
            and p.get("reuse_count", 0) < 3
        ]

        if len(successful_patterns) >= 2:
            suggestion_id = self.create_suggestion(
                suggestion_type="technical_debt",
                title="Propagate Successful Patterns",
                description=f"Found {len(successful_patterns)} highly successful patterns that are underutilized. Consider applying these patterns to similar code areas.",
                rationale="Successful patterns with low reuse count detected",
                urgency="low",
                estimated_effort_hours=3.0,
                expected_impact="medium",
                context={"patterns": successful_patterns, "project_context": context},
                related_patterns=[p.get("pattern_id") for p in successful_patterns]
            )
            suggestion_ids.append(suggestion_id)

        return suggestion_ids

    def format_suggestion_for_display(self, suggestion: Dict) -> str:
        """Format a suggestion for user display"""
        urgency_icons = {
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢"
        }

        impact_icons = {
            "high": "⬆️⬆️⬆️",
            "medium": "⬆️⬆️",
            "low": "⬆️"
        }

        category_labels = {
            "critical_quick_win": "🎯 CRITICAL QUICK WIN",
            "quick_win": "⚡ QUICK WIN",
            "strategic_improvement": "📈 STRATEGIC",
            "nice_to_have": "💡 NICE TO HAVE"
        }

        output = []
        output.append(f"\n{category_labels.get(suggestion['category'], '📋 SUGGESTION')}")
        output.append(f"Priority: {suggestion['priority_score']}/100")
        output.append(f"\n{urgency_icons.get(suggestion['urgency'], '⚪')} {suggestion['title']}")
        output.append(f"\nType: {suggestion['type'].replace('_', ' ').title()}")
        output.append(f"Urgency: {suggestion['urgency'].title()}")
        output.append(f"Expected Impact: {impact_icons.get(suggestion['expected_impact'], '')} {suggestion['expected_impact'].title()}")
        output.append(f"Estimated Effort: {suggestion['estimated_effort_hours']} hours")
        output.append(f"\nDescription:")
        output.append(suggestion['description'])
        output.append(f"\nRationale:")
        output.append(suggestion['rationale'])

        if suggestion.get('related_files'):
            output.append(f"\nRelated Files:")
            for file in suggestion['related_files'][:3]:
                output.append(f"  - {file}")

        output.append(f"\nSuggestion ID: {suggestion['suggestion_id']}")
        output.append("─" * 70)

        return "\n".join(output)


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Proactive Suggester for Four-Tier Architecture")
    parser.add_argument("--dir", default=".claude-patterns", help="Data directory")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Create suggestion
    create_parser = subparsers.add_parser("create", help="Create a new suggestion")
    create_parser.add_argument("--type", required=True, help="Suggestion type")
    create_parser.add_argument("--title", required=True, help="Suggestion title")
    create_parser.add_argument("--description", required=True, help="Detailed description")
    create_parser.add_argument("--rationale", required=True, help="Why this is important")
    create_parser.add_argument("--urgency", required=True, choices=["high", "medium", "low"])
    create_parser.add_argument("--effort", type=float, required=True, help="Estimated hours")
    create_parser.add_argument("--impact", required=True, choices=["high", "medium", "low"])

    # List suggestions
    list_parser = subparsers.add_parser("list", help="List suggestions")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--type", help="Filter by type")
    list_parser.add_argument("--urgency", help="Filter by urgency")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--limit", type=int, default=10, help="Max suggestions")

    # Get top suggestions
    top_parser = subparsers.add_parser("top", help="Get top priority suggestions")
    top_parser.add_argument("--count", type=int, default=5, help="Number of suggestions")
    top_parser.add_argument("--no-preferences", action="store_true", help="Ignore user preferences")

    # Record acceptance
    accept_parser = subparsers.add_parser("accept", help="Record suggestion acceptance")
    accept_parser.add_argument("--id", required=True, help="Suggestion ID")
    accept_parser.add_argument("--status", required=True, choices=["accepted", "rejected", "ignored"])
    accept_parser.add_argument("--feedback", help="Optional feedback")

    # Record implementation
    implement_parser = subparsers.add_parser("implement", help="Record implementation outcome")
    implement_parser.add_argument("--id", required=True, help="Suggestion ID")
    implement_parser.add_argument("--success", type=bool, required=True, help="Implementation success")
    implement_parser.add_argument("--impact", required=True, choices=["high", "medium", "low"])
    implement_parser.add_argument("--effort", type=float, help="Actual effort hours")
    implement_parser.add_argument("--notes", help="Implementation notes")

    # Statistics
    stats_parser = subparsers.add_parser("stats", help="Show statistics")

    args = parser.parse_args()

    suggester = ProactiveSuggester(data_dir=args.dir)

    if args.command == "create":
        suggestion_id = suggester.create_suggestion(
            suggestion_type=args.type,
            title=args.title,
            description=args.description,
            rationale=args.rationale,
            urgency=args.urgency,
            estimated_effort_hours=args.effort,
            expected_impact=args.impact
        )
        print(f"Created suggestion: {suggestion_id}")

    elif args.command == "list":
        suggestions = suggester.get_suggestions(
            status=args.status,
            suggestion_type=args.type,
            urgency=args.urgency,
            category=args.category,
            limit=args.limit
        )
        print(f"\nFound {len(suggestions)} suggestions:\n")
        for suggestion in suggestions:
            print(suggester.format_suggestion_for_display(suggestion))

    elif args.command == "top":
        suggestions = suggester.get_top_suggestions(
            count=args.count,
            consider_preferences=not args.no_preferences
        )
        print(f"\n🎯 Top {len(suggestions)} Priority Suggestions:\n")
        for suggestion in suggestions:
            print(suggester.format_suggestion_for_display(suggestion))

    elif args.command == "accept":
        suggester.record_acceptance(
            suggestion_id=args.id,
            acceptance_status=args.status,
            feedback=args.feedback
        )
        print(f"Recorded acceptance: {args.status}")

    elif args.command == "implement":
        suggester.record_implementation_outcome(
            suggestion_id=args.id,
            success=args.success,
            impact_measured=args.impact,
            actual_effort_hours=args.effort,
            notes=args.notes
        )
        print(f"Recorded implementation outcome")

    elif args.command == "stats":
        stats = suggester.get_statistics()
        print("\n📊 Proactive Suggester Statistics\n")
        print(f"Total Suggestions: {stats['total_suggestions']}")
        print(f"Pending: {stats['pending']}")
        print(f"Accepted: {stats['accepted']}")
        print(f"Implemented: {stats['implemented']}")
        print(f"Acceptance Rate: {stats['acceptance_rate']:.1%}")
        print(f"Implementation Success Rate: {stats['implementation_success_rate']:.1%}")
        print(f"\nCategory Distribution:")
        for category, count in stats['suggestions_per_category'].items():
            print(f"  {category}: {count}")
        print(f"\nUser Preferences:")
        prefs = stats['user_preferences']
        print(f"  Preferred Types: {', '.join(prefs['preferred_types']) if prefs['preferred_types'] else 'Not yet determined'}")
        print(f"  Preferred Urgency: {prefs['preferred_urgency']}")
        print(f"  Preferred Effort: {prefs['preferred_effort']}")

    else:
        parser.print_help()
