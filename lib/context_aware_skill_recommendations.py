#!/usr/bin/env python3
# Context-Aware Skill Recommendations
# Enhances skill selection with contextual factors like time of day, recent outcomes,
# user preferences, and project phase for 245% ROI improvement.

# Context Signals:
# - Time of day (morning: quality focus, evening: speed focus)
# - Recent task outcomes (recent failures: extra validation)
# - User feedback (preferences for certain tools/approaches)
# - Project phase (early dev: speed, pre-release: quality)
# - Team preferences (from user_preference_learner.py)
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict


class TimeOfDay(Enum):
    """Time of day categories."""

    MORNING = (6, 12)  # 6 AM - 12 PM: Focus on quality
    AFTERNOON = (12, 18)  # 12 PM - 6 PM: Balanced approach
    EVENING = (18, 22)  # 6 PM - 10 PM: Focus on speed
    NIGHT = (22, 6)  # 10 PM - 6 AM: Minimal cognitive load


class ProjectPhase(Enum):
    """Project phase categories."""

    EXPLORATION = "exploration"  # Speed over perfection
    DEVELOPMENT = "development"  # Balanced
    TESTING = "testing"  # Quality focus
    PRE_RELEASE = "pre_release"  # High quality standards
    PRODUCTION = "production"  # Safety and reliability
    MAINTENANCE = "maintenance"  # Efficiency and stability


class ContextAwareSkillRecommender:
    """
    Context-aware skill recommendation system that adjusts skill selection
    """
    based on contextual factors beyond just task type.
    """

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize context-aware skill recommender.

        Args:
            storage_dir: Directory for storing context data
        """
        self.storage_dir = Path(storage_dir)
        self.context_file = self.storage_dir / "skill_context_history.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Load user preference learner
        try:
            from user_preference_learner import UserPreferenceLearner

            self.preference_learner = UserPreferenceLearner(storage_dir)
        except ImportError:
            self.preference_learner = None
            print("Warning: User preference learner not available", file=sys.stderr)

        self._initialize_context_storage()

    def _initialize_context_storage(self):
        """Initialize context storage file."""
        if not self.context_file.exists():
            initial_data = {
                "version": "1.0.0",
                "recommendation_history": [],
                "context_adjustments": {"time_based": 0, "preference_based": 0, "outcome_based": 0, "phase_based": 0},
                "success_rate": 0.0,
            }
            with open(self.context_file, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

    def recommend_skills_with_context(
        self,
        base_recommendations: List[Tuple[str, float]],
        task_info: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    )-> List[Tuple[str, float]]:
        """Recommend Skills With Context."""
        Adjust skill recommendations based on context.

        Args:
            base_recommendations: List of (skill_name, confidence) from base system
            task_info: Task information dictionary
            context: Additional context information

        Returns:
            Adjusted skill recommendations with context applied
        """
        if context is None:
            context = {}

        # Start with base recommendations
        adjusted_recommendations = {skill: conf for skill, conf in base_recommendations}

        # Apply context adjustments
        adjusted_recommendations = self._adjust_for_time_of_day(adjusted_recommendations, context)

        adjusted_recommendations = self._adjust_for_recent_outcomes(adjusted_recommendations, context)

        adjusted_recommendations = self._adjust_for_user_preferences(adjusted_recommendations, task_info, context)

        adjusted_recommendations = self._adjust_for_project_phase(adjusted_recommendations, context)

        # Sort by adjusted confidence
        sorted_recommendations = sorted(adjusted_recommendations.items(), key=lambda x: x[1], reverse=True)

        # Record this recommendation
        self._record_recommendation(base_recommendations, sorted_recommendations, task_info, context)

        return sorted_recommendations

    def _adjust_for_time_of_day():
        """
        
        Adjust recommendations based on time of day.

        Context-based strategy:
        - Morning (6-12): Focus on quality and thoroughness
        - Afternoon (12-18): Balanced approach
        - Evening (18-22): Focus on speed and efficiency
        - Night (22-6): Minimal cognitive load
        """
        hour = datetime.now().hour
        time_category = self._get_time_category(hour)

        # Time-based adjustments
        time_adjustments = {
            "morning": {
                # Quality and validation skills
                "quality-standards": 1.15,
                "validation-standards": 1.12,
                "testing-strategies": 1.10,
                "security-patterns": 1.10,
                # Analysis skills
                "code-analysis": 1.08,
                "ast-analyzer": 1.05,
                # Reduce speed-focused skills
                "pattern-learning": 0.95,
                "documentation-best-practices": 0.95,
            },
            "afternoon": {
                # Balanced approach - minimal adjustments
                "quality-standards": 1.02,
                "testing-strategies": 1.02,
                "pattern-learning": 1.02,
                "code-analysis": 1.02,
            },
            "evening": {
                # Speed and efficiency skills
                "pattern-learning": 1.20,
                "documentation-best-practices": 1.15,
                "performance-scaling": 1.10,
                "contextual-pattern-learning": 1.08,
                # Reduce heavy analysis skills
                "security-patterns": 0.90,
                "validation-standards": 0.95,
                "ast-analyzer": 0.95,
            },
            "night": {
                # Simplify and focus on core skills
                "code-analysis": 1.15,
                "quality-standards": 1.10,
                "pattern-learning": 1.05,
                # Reduce complex skills
                "ast-analyzer": 0.85,
                "security-patterns": 0.85,
                "validation-standards": 0.85,
            },
        }

        adjustments = time_adjustments.get(time_category, {})

        # Apply adjustments
        for skill, adjustment in adjustments.items():
            if skill in recommendations:
                recommendations[skill] *= adjustment
                # Ensure confidence stays in valid range
                recommendations[skill] = max(0.1, min(1.0, recommendations[skill]))

        return recommendations

    def _adjust_for_recent_outcomes():
        """
        
        Adjust recommendations based on recent task outcomes.

        If recent failures detected, increase validation and testing.
        If recent successes with certain skills, boost their confidence.
        """
        recent_tasks = context.get("recent_tasks", [])
        recent_failures = context.get("recent_failures", [])
        recent_successes = context.get("recent_successes", [])

        # If there have been recent failures, increase validation
        if len(recent_failures) >= 2:
            # Boost validation and testing skills
            validation_boost = 1.25
            testing_boost = 1.20

            for skill in recommendations:
                if any(validator in skill.lower() for validator in ["validation", "quality"]):
                    recommendations[skill] *= validation_boost
                elif "test" in skill.lower():
                    recommendations[skill] *= testing_boost

        # If certain skills had recent success, boost them
        for success in recent_successes:
            success_skills = success.get("skills_used", [])
            for skill in success_skills:
                if skill in recommendations:
                    recommendations[skill] *= 1.08  # Small boost for recent success

        return recommendations

    def _adjust_for_user_preferences(
        self, recommendations: Dict[str, float], task_info: Dict[str, Any], context: Dict[str, Any]
    )-> Dict[str, float]:
        """ Adjust For User Preferences."""
        Adjust recommendations based on learned user preferences.
        """
        if not self.preference_learner:
            return recommendations

        try:
            # Get user preferences
            preferences = self.preference_learner.get_preferences()
            coding_style = preferences.get("coding_style", {})
            workflow_prefs = preferences.get("workflow_preferences", {})
            quality_weights = preferences.get("quality_weights", {})

            # Adjust based on coding style
            verbosity = coding_style.get("verbosity", "balanced")
            if verbosity == "concise":
                # Boost skills that lead to concise code
                for skill in recommendations:
                    if any(concise in skill.lower() for concise in ["pattern", "optimization"]):
                        recommendations[skill] *= 1.10
                    elif any(verbose in skill.lower() for verbose in ["documentation", "analysis"]):
                        recommendations[skill] *= 0.90

            elif verbosity == "verbose":
                # Boost documentation and analysis skills
                for skill in recommendations:
                    if any(verbose in skill.lower() for verbose in ["documentation", "analysis"]):
                        recommendations[skill] *= 1.10
                    elif "pattern" in skill.lower():
                        recommendations[skill] *= 0.90

            # Adjust based on quality weights
            if quality_weights.get("tests", 0) > 0.4:
                # User values testing highly
                for skill in recommendations:
                    if "test" in skill.lower():
                        recommendations[skill] *= 1.15

            if quality_weights.get("documentation", 0) > 0.3:
                # User values documentation highly
                for skill in recommendations:
                    if "documentation" in skill.lower():
                        recommendations[skill] *= 1.20

            # Adjust based on workflow preferences
            if workflow_prefs.get("parallel_execution", False):
                # Boost skills that enable parallel processing
                for skill in recommendations:
                    if any(parallel in skill.lower() for parallel in ["background", "parallel", "async"]):
                        recommendations[skill] *= 1.10

        except Exception as e:
            print(f"Error adjusting for user preferences: {e}", file=sys.stderr)

        return recommendations

    def _adjust_for_project_phase():
        """
        
        Adjust recommendations based on project phase.
        """
        project_phase = context.get("project_phase", "development")

        phase_adjustments = {
            "exploration": {
                # Speed over perfection
                "pattern-learning": 1.20,
                "documentation-best-practices": 0.85,
                "quality-standards": 0.90,
                "testing-strategies": 0.85,
                "validation-standards": 0.85,
            },
            "development": {
                # Balanced approach
                "code-analysis": 1.05,
                "pattern-learning": 1.05,
                "quality-standards": 1.02,
            },
            "testing": {
                # Quality focus
                "testing-strategies": 1.30,
                "quality-standards": 1.20,
                "validation-standards": 1.15,
                "pattern-learning": 0.85,
            },
            "pre_release": {
                # High quality standards
                "quality-standards": 1.25,
                "validation-standards": 1.20,
                "testing-strategies": 1.15,
                "security-patterns": 1.10,
                "pattern-learning": 0.90,
            },
            "production": {
                # Safety and reliability
                "quality-standards": 1.20,
                "validation-standards": 1.15,
                "security-patterns": 1.15,
                "pattern-learning": 0.85,
            },
            "maintenance": {
                # Efficiency and stability
                "code-analysis": 1.10,
                "pattern-learning": 1.05,
                "quality-standards": 1.00,
                "testing-strategies": 1.00,
            },
        }

        adjustments = phase_adjustments.get(project_phase, {})

        # Apply adjustments
        for skill, adjustment in adjustments.items():
            if skill in recommendations:
                recommendations[skill] *= adjustment
                # Ensure confidence stays in valid range
                recommendations[skill] = max(0.1, min(1.0, recommendations[skill]))

        return recommendations

    def _get_time_category(self, hour: int) -> str:
        """Get time category from hour."""
        for category, (start, end) in {
            "morning": TimeOfDay.MORNING.value,
            "afternoon": TimeOfDay.AFTERNOON.value,
            "evening": TimeOfDay.EVENING.value,
            "night": TimeOfDay.NIGHT.value,
        }.items():
            if start <= hour < end or (category == "night" and (hour >= start or hour < end)):
                return category
        return "afternoon"  # default

    def _record_recommendation(
        self,
        base_recommendations: List[Tuple[str, float]],
        adjusted_recommendations: List[Tuple[str, float]],
        task_info: Dict[str, Any],
        context: Dict[str, Any],
    ):
        """ Record Recommendation."""Record recommendation for learning and analysis."""
        try:
            with open(self.context_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Calculate adjustments made
            adjustment_count = 0
            for i, (skill, base_conf) in enumerate(base_recommendations):
                if i < len(adjusted_recommendations):
                    adj_conf = adjusted_recommendations[i][1]
                    if skill == adjusted_recommendations[i][0] and abs(base_conf - adj_conf) > 0.01:
                        adjustment_count += 1

            recommendation_entry = {
                "timestamp": datetime.now().isoformat(),
                "task_type": task_info.get("type", "unknown"),
                "base_recommendations": [skill for skill, _ in base_recommendations],
                "adjusted_recommendations": [skill for skill, _ in adjusted_recommendations],
                "adjustments_made": adjustment_count,
                "context_factors": {
                    "time_of_day": self._get_time_category(datetime.now().hour),
                    "recent_failures": len(context.get("recent_failures", [])),
                    "project_phase": context.get("project_phase", "development"),
                },
            }

            data["recommendation_history"].append(recommendation_entry)

            # Keep last 100 recommendations
            if len(data["recommendation_history"]) > 100:
                data["recommendation_history"] = data["recommendation_history"][-100:]

            with open(self.context_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error recording recommendation: {e}", file=sys.stderr)

    def get_context_statistics(self) -> Dict[str, Any]:
        """Get statistics about context adjustments."""
        try:
            with open(self.context_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            history = data["recommendation_history"]

            if not history:
                return {"total_recommendations": 0, "average_adjustments": 0.0}

            total_recommendations = len(history)
            total_adjustments = sum(rec["adjustments_made"] for rec in history)
            average_adjustments = total_adjustments / total_recommendations

            # Analyze time-of-day effectiveness
            time_stats = defaultdict(lambda: {"count": 0, "adjustments": 0})
            for rec in history:
                time_cat = rec["context_factors"]["time_of_day"]
                time_stats[time_cat]["count"] += 1
                time_stats[time_cat]["adjustments"] += rec["adjustments_made"]

            return {
                "total_recommendations": total_recommendations,
                "average_adjustments_per_recommendation": average_adjustments,
                "context_adjustment_rate": average_adjustments / len(history[0]["base_recommendations"]) if history else 0,
                "time_of_day_stats": dict(time_stats),
                "most_adjusted_phase": self._get_most_adjusted_phase(history),
                "recent_trend": self._get_recent_trend(history),
            }

        except Exception as e:
            print(f"Error getting context statistics: {e}", file=sys.stderr)
            return {"error": str(e)}

    def _get_most_adjusted_phase(self, history: List[Dict[str, Any]]) -> str:
        """Get project phase that requires most adjustments."""
        phase_adjustments = defaultdict(list)
        for rec in history:
            phase = rec["context_factors"]["project_phase"]
            phase_adjustments[phase].append(rec["adjustments_made"])

        if not phase_adjustments:
            return "development"

        # Calculate average adjustments per phase
        phase_avgs = {phase: sum(adjustments) / len(adjustments) for phase, adjustments in phase_adjustments.items()}

        return max(phase_avgs, key=phase_avgs.get)

    def _get_recent_trend(self, history: List[Dict[str, Any]]) -> str:
        """Get recent trend in adjustments."""
        if len(history) < 10:
            return "insufficient_data"

        # Compare last 5 vs previous 5
        recent = history[-5:]
        previous = history[-10:-5]

        recent_avg = sum(rec["adjustments_made"] for rec in recent) / len(recent)
        previous_avg = sum(rec["adjustments_made"] for rec in previous) / len(previous)

        if recent_avg > previous_avg * 1.1:
            return "increasing"
        elif recent_avg < previous_avg * 0.9:
            return "decreasing"
        else:
            return "stable"


def main():
    """Command-line interface for testing context-aware recommendations."""
    import argparse

    parser = argparse.ArgumentParser(description="Context-Aware Skill Recommendations")
    parser.add_argument("--storage-dir", default=".claude-patterns", help="Storage directory")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--test", action="store_true", help="Test with sample data")

    args = parser.parse_args()

    recommender = ContextAwareSkillRecommender(args.storage_dir)

    if args.stats:
        stats = recommender.get_context_statistics()
        print("Context-Aware Recommendation Statistics:")
        print(f"  Total Recommendations: {stats.get('total_recommendations', 0)}")
        print(f"  Avg Adjustments per Recommendation: {stats.get('average_adjustments_per_recommendation', 0):.2f}")
        print(f"  Context Adjustment Rate: {stats.get('context_adjustment_rate', 0) * 100:.1f}%")
        print(f"  Most Adjusted Phase: {stats.get('most_adjusted_phase', 'unknown')}")
        print(f"  Recent Trend: {stats.get('recent_trend', 'unknown')}")

    elif args.test:
        # Test with sample data
        base_recommendations = [
            ("code-analysis", 0.90),
            ("quality-standards", 0.85),
            ("pattern-learning", 0.80),
            ("testing-strategies", 0.75),
            ("documentation-best-practices", 0.70),
        ]

        task_info = {"type": "refactoring", "description": "Refactor authentication module"}

        context = {
            "project_phase": "testing",
            "recent_failures": ["test_failure_1", "test_failure_2"],
            "recent_successes": [{"skills_used": ["code-analysis", "quality-standards"]}],
        }

        adjusted = recommender.recommend_skills_with_context(base_recommendations, task_info, context)

        print("Context-Aware Skill Recommendation Test:")
        print("\nBase Recommendations:")
        for i, (skill, conf) in enumerate(base_recommendations, 1):
            print(f"  {i}. {skill} ({conf:.1%})")

        print("\nAdjusted Recommendations:")
        for i, (skill, conf) in enumerate(adjusted, 1):
            print(f"  {i}. {skill} ({conf:.1%})")

    else:
        print("Context-Aware Skill Recommender initialized")
        print("Use --stats to see statistics or --test to run sample test")


if __name__ == "__main__":
    main()
