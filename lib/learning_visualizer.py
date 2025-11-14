#!/usr/bin/env python3
# Real-Time Learning Feedback System
#     Shows users what the autonomous system is learning and provides transparency
"""

into AI decision-making processes.

Features:
- Real-time learning event recording and display
- Decision explanation generation
- Learning progress visualization
- Non-intrusive notifications
- Dashboard integration with learning metrics
"""
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading
import random


class LearningEventType:
    """Learning event types."""

    PATTERN_ACQUIRED = "pattern_acquired"
    SKILL_EFFECTIVENESS_UPDATED = "skill_effectiveness_updated"
    AGENT_PERFORMANCE_IMPROVED = "agent_performance_improved"
    QUALITY_IMPROVEMENT_ACHIEVED = "quality_improvement_achieved"
    USER_PREFERENCE_LEARNED = "user_preference_learned"
    COLLABORATION_INSIGHT = "collaboration_insight"
    SPECIALIZATION_IDENTIFIED = "specialization_identified"
    FAILURE_PATTERN_DETECTED = "failure_pattern_detected"


class LearningEventRecorder:
    """Records learning events for visualization and analysis."""

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """Initialize learning event recorder."""
        self.storage_dir = Path(storage_dir)
        self.events_file = self.storage_dir / "learning_events.json"
        self.summary_file = self.storage_dir / "learning_summary.json"

        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._initialize_storage()

        # In-memory event cache for real-time display
        self.recent_events = deque(maxlen=100)
        self.learning_metrics = defaultdict(int)
        self._lock = threading.Lock()

    def _initialize_storage(self):
        """Initialize storage files."""
        if not self.events_file.exists():
            initial_data = {"version": "1.0.0", "events": [], "total_events": 0, "last_updated": datetime.now().isoformat()}
            with open(self.events_file, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

        if not self.summary_file.exists():
            initial_summary = {
                "version": "1.0.0",
                "learning_velocity": 0.0,
                "pattern_reuse_rate": 0.0,
                "quality_trend": "stable",
                "total_patterns": 0,
                "active_skills": 0,
                "agent_improvements": 0,
                "user_confidence": 0.0,
                "last_updated": datetime.now().isoformat(),
            }
            with open(self.summary_file, "w", encoding="utf-8") as f:
                json.dump(initial_summary, f, indent=2)

    def record_learning_event(
        self,
        event_type: str,
        description: str,
        impact: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        confidence: Optional[float] = None,
    )-> str:
        """Record Learning Event."""
        Record a learning event.

        Args:
            event_type: Type of learning event
            description: Human-readable description
            impact: Impact description (e.g., "quality +5 points")
            data: Additional structured data
            confidence: Confidence level (0-1)

        Returns:
            Event ID
"""
        event_id = f"event_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"

        event = {
            "event_id": event_id,
            "event_type": event_type,
            "description": description,
            "impact": impact,
            "data": data or {},
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
        }

        # Add to in-memory cache
        with self._lock:
            self.recent_events.append(event)
            self.learning_metrics[event_type] += 1

        # Save to persistent storage
        self._save_event(event)
        self._update_summary()

        return event_id

"""
    def _save_event(self, event: Dict[str, Any]):
        """Save event to persistent storage."""
        try:
            with open(self.events_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            data["events"].append(event)
            data["total_events"] += 1
            data["last_updated"] = datetime.now().isoformat()

            # Keep last 500 events
            if len(data["events"]) > 500:
                data["events"] = data["events"][-500:]

            with open(self.events_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving learning event: {e}", file=sys.stderr)

    def _update_summary(self):
        """Update learning summary statistics."""
        try:
            # Load pattern data
            patterns_file = self.storage_dir / "patterns.json"
            total_patterns = 0
            pattern_reuse_rate = 0.0

            if patterns_file.exists():
                with open(patterns_file, "r", encoding="utf-8") as f:
                    patterns = json.load(f)

                if isinstance(patterns, list):
                    total_patterns = len(patterns)
                    if patterns:
                        reuse_counts = [p.get("usage_count", 0) for p in patterns]
                        if reuse_counts:
                            pattern_reuse_rate = sum(1 for count in reuse_counts if count > 0) / len(reuse_counts)
                elif isinstance(patterns, dict):
                    pattern_list = patterns.get("patterns", [])
                    total_patterns = len(pattern_list)

            # Load agent performance data
            performance_file = self.storage_dir / "agent_performance.json"
            agent_improvements = 0
            if performance_file.exists():
                with open(performance_file, "r", encoding="utf-8") as f:
                    perf_data = json.load(f)
                    agent_improvements = len(perf_data.get("agent_metrics", {}))

            # Calculate learning velocity (events in last 24h)
            with open(self.events_file, "r", encoding="utf-8") as f:
                events_data = json.load(f)

            yesterday = datetime.now() - timedelta(days=1)
            recent_events = [e for e in events_data["events"] if datetime.fromisoformat(e["timestamp"]) > yesterday]
            learning_velocity = len(recent_events)

            # Determine quality trend
            quality_events = [e for e in recent_events if e["event_type"] == LearningEventType.QUALITY_IMPROVEMENT_ACHIEVED]

            if len(quality_events) >= 5:
                # Check trend from quality improvements
                quality_scores = []
                for event in quality_events[-5:]:
                    if "data" in event and "quality_score" in event["data"]:
                        quality_scores.append(event["data"]["quality_score"])

                if len(quality_scores) >= 3:
                    if quality_scores[-1] > quality_scores[0]:
                        quality_trend = "improving"
                    elif quality_scores[-1] < quality_scores[0]:
                        quality_trend = "declining"
                    else:
                        quality_trend = "stable"
                else:
                    quality_trend = "stable"
            else:
                quality_trend = "insufficient_data"

            # Update summary
            summary = {
                "version": "1.0.0",
                "learning_velocity": learning_velocity,
                "pattern_reuse_rate": pattern_reuse_rate,
                "quality_trend": quality_trend,
                "total_patterns": total_patterns,
                "active_skills": self._count_active_skills(),
                "agent_improvements": agent_improvements,
                "user_confidence": self._calculate_user_confidence(),
                "total_events": self.learning_metrics["total_events"] if self.learning_metrics else 0,
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.summary_file, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)

        except Exception as e:
            print(f"Error updating learning summary: {e}", file=sys.stderr)

    def _count_active_skills(self) -> int:
        """Count active skills from learning data."""
        try:
            skill_events = [e for e in self.recent_events if e["event_type"] == LearningEventType.SKILL_EFFECTIVENESS_UPDATED]

            # Count unique skills mentioned in events
            skills_mentioned = set()
            for event in skill_events[-20:]:  # Last 20 events
                if "data" in event and "skill" in event["data"]:
                    skills_mentioned.add(event["data"]["skill"])

            return len(skills_mentioned)

        except Exception:
            return 0

    def _calculate_user_confidence(self) -> float:
        """Calculate user confidence based on recent positive events."""
        try:
            with self._lock:
                recent_events = list(self.recent_events)[-50:]  # Last 50 events

            # Count positive vs negative events
            positive_types = [
                LearningEventType.PATTERN_ACQUIRED,
                LearningEventType.AGENT_PERFORMANCE_IMPROVED,
                LearningEventType.QUALITY_IMPROVEMENT_ACHIEVED,
                LearningEventType.SPECIALIZATION_IDENTIFIED,
            ]

            negative_types = [LearningEventType.FAILURE_PATTERN_DETECTED]

            positive_count = sum(1 for e in recent_events if e["event_type"] in positive_types)
            negative_count = sum(1 for e in recent_events if e["event_type"] in negative_types)

            total_relevant = positive_count + negative_count
            if total_relevant == 0:
                return 0.5  # Neutral confidence

            confidence = positive_count / total_relevant
            return min(1.0, confidence)

        except Exception:
            return 0.5

    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent learning events."""
        with self._lock:
            return list(self.recent_events)[-limit:]

    def get_learning_summary(self) -> Dict[str, Any]:
        """Get comprehensive learning summary."""
        try:
            with open(self.summary_file, "r", encoding="utf-8") as f:
                summary = json.load(f)

            # Add recent events for context
            summary["recent_events"] = self.get_recent_events(5)
            summary["event_metrics"] = dict(self.learning_metrics)

            return summary

        except Exception as e:
            print(f"Error getting learning summary: {e}", file=sys.stderr)
            return {"error": str(e)}


class DecisionExplainer:
    """Generates human-readable explanations for AI decisions."""

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """Initialize decision explainer."""
        self.storage_dir = Path(storage_dir)
        self.patterns_file = self.storage_dir / "patterns.json"
        self.preferences_file = self.storage_dir / "user_preferences.json"

    def explain_decision():
"""
        
        Generate human-readable explanation of AI decision.

        Args:
            decision_type: Type of decision (skill_selection, agent_routing, etc.)
            context: Decision context data
            confidence: Decision confidence score

        Returns:
            Human-readable explanation
"""
        if decision_type == "skill_selection":
            return self._explain_skill_selection(context, confidence)
        elif decision_type == "agent_routing":
            return self._explain_agent_routing(context, confidence)
        elif decision_type == "quality_threshold":
            return self._explain_quality_threshold(context, confidence)
        else:
            return f"Decision based on learned patterns for {decision_type}"

"""
    def _explain_skill_selection(self, context: Dict[str, Any], confidence: Optional[float]) -> str:
        """Explain skill selection decision."""
        task_type = context.get("task_type", "unknown")
        selected_skills = context.get("selected_skills", [])

        explanation_parts = [f"Selected {len(selected_skills)} skills for {task_type} task"]

        # Check for pattern-based selection
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, "r", encoding="utf-8") as f:
                    patterns = json.load(f)

                if isinstance(patterns, list):
                    similar_patterns = [
                        p for p in patterns if p.get("task_type") == task_type and p.get("success_rate", 0) > 0.8
                    ]

                    if similar_patterns:
                        explanation_parts.append(f"Based on {len(similar_patterns)} successful similar tasks")

                        # Add success rate
                        avg_success = sum(p.get("success_rate", 0) for p in similar_patterns) / len(similar_patterns)
                        explanation_parts.append(f"Similar tasks {avg_success:.1%} successful")

            except Exception:
                pass

        # Add specific skill explanations
        skill_explanations = {
            "code-analysis": "essential for understanding code structure",
            "quality-standards": "ensures code meets quality benchmarks",
            "pattern-learning": "leverages learned patterns from similar tasks",
            "security-patterns": "identifies potential security issues",
            "testing-strategies": "ensures comprehensive test coverage",
        }

        for skill in selected_skills[:3]:  # Explain top 3 skills
            if skill in skill_explanations:
                explanation_parts.append(skill_explanations[skill])

        if confidence:
            explanation_parts.append(f"Confidence: {confidence:.1%}")

        return ". ".join(explanation_parts) + "."

    def _explain_agent_routing(self, context: Dict[str, Any], confidence: Optional[float]) -> str:
        """Explain agent routing decision."""
        agent = context.get("agent", "unknown")
        task_type = context.get("task_type", "unknown")
        reasoning = context.get("reasoning", "")

        explanation_parts = [f"Selected {agent} for {task_type} task"]

        if reasoning:
            explanation_parts.append(reasoning)

        # Add performance data if available
        try:
            performance_file = self.storage_dir / "agent_performance.json"
            if performance_file.exists():
                with open(performance_file, "r", encoding="utf-8") as f:
                    perf_data = json.load(f)

                if agent in perf_data.get("agent_metrics", {}):
                    metrics = perf_data["agent_metrics"][agent]
                    success_rate = metrics.get("success_rate", 0)
                    avg_quality = metrics.get("average_quality_score", 0)
                    total_tasks = metrics.get("total_tasks", 0)

                    explanation_parts.append(f"Agent has {success_rate:.1%} success rate")
                    explanation_parts.append(f"Average quality: {avg_quality:.1f}/100")
                    explanation_parts.append(f"Completed {total_tasks} similar tasks")

        except Exception:
            pass

        if confidence:
            explanation_parts.append(f"Routing confidence: {confidence:.1%}")

        return ". ".join(explanation_parts) + "."

    def _explain_quality_threshold(self, context: Dict[str, Any], confidence: Optional[float]) -> str:
        """Explain quality threshold decision."""
        threshold = context.get("threshold", 70)
        task_type = context.get("task_type", "unknown")
        adjustments = context.get("adjustments", {})

        explanation_parts = [f"Quality threshold set to {threshold}/100 for {task_type} task"]

        # Explain adjustments
        if adjustments.get("phase_adjustment"):
            phase = adjustments["phase_adjustment"]["phase"]
            multiplier = adjustments["phase_adjustment"]["multiplier"]
            explanation_parts.append(f"Phase adjustment ({phase}): ×{multiplier:.2f}")

        if adjustments.get("criticality_adjustment"):
            criticality = adjustments["criticality_adjustment"]["criticality"]
            multiplier = adjustments["criticality_adjustment"]["multiplier"]
            explanation_parts.append(f"Criticality adjustment ({criticality}): ×{multiplier:.2f}")

        if adjustments.get("user_facing"):
            explanation_parts.append("User-facing code: ×1.05 (stricter)")

        # Add rationale
        if threshold >= 90:
            explanation_parts.append("Very high standards required for safety and reliability")
        elif threshold >= 80:
            explanation_parts.append("High quality standards for production readiness")
        elif threshold >= 70:
            explanation_parts.append("Standard quality requirements")
        else:
            explanation_parts.append("Relaxed standards to prioritize speed and exploration")

        return ". ".join(explanation_parts) + "."


class LearningVisualizer:
    """Main learning visualizer that combines recording and explanation."""

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """Initialize learning visualizer."""
        self.storage_dir = Path(storage_dir)
        self.event_recorder = LearningEventRecorder(storage_dir)
        self.decision_explainer = DecisionExplainer(storage_dir)

    def record_learning_event(
        self,
        event_type: str,
        description: str,
        impact: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        confidence: Optional[float] = None,
    )-> str:
        """Record Learning Event."""Record a learning event."""
        return self.event_recorder.record_learning_event(event_type, description, impact, data, confidence)

    def explain_decision(self, decision_type: str, context: Dict[str, Any], confidence: Optional[float] = None) -> str:
        """Generate explanation for AI decision."""
        return self.decision_explainer.explain_decision(decision_type, context, confidence)

    def generate_learning_notification(self, event: Dict[str, Any]) -> str:
        """Generate a non-intrusive learning notification."""
        emoji_map = {
            LearningEventType.PATTERN_ACQUIRED: "[BRAIN]",
            LearningEventType.QUALITY_IMPROVEMENT_ACHIEVED: "[OK]",
            LearningEventType.AGENT_PERFORMANCE_IMPROVED: "[TREND]",
            LearningEventType.USER_PREFERENCE_LEARNED: "👤",
            LearningEventType.SPECIALIZATION_IDENTIFIED: "[TARGET]",
            LearningEventType.COLLABORATION_INSIGHT: "🤝",
        }

        emoji = emoji_map.get(event["event_type"], "[DATA]")
        description = event["description"]
        impact = event.get("impact", "")

        if impact:
            return f"{emoji} {description} ({impact})"
        else:
            return f"{emoji} {description}"

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get learning data for dashboard display."""
        summary = self.event_recorder.get_learning_summary()
        recent_events = self.event_recorder.get_recent_events(10)

        # Format recent events for display
        formatted_events = []
        for event in recent_events:
            notification = self.generate_learning_notification(event)
            formatted_events.append(
                {
                    "id": event["event_id"],
                    "type": event["event_type"],
                    "notification": notification,
                    "timestamp": event["timestamp"],
                    "confidence": event.get("confidence"),
                }
            )

        return {"summary": summary, "recent_events": formatted_events, "event_metrics": summary.get("event_metrics", {})}


def main():
    """Command-line interface for testing learning visualizer."""
"""
    import argparse

    parser = argparse.ArgumentParser(description="Learning Visualizer")
    parser.add_argument("--storage-dir", default=".claude-patterns", help="Storage directory")
    parser.add_argument("--stats", action="store_true", help="Show learning statistics")
    parser.add_argument("--record", help="Record a test event")
    parser.add_argument("--explain", choices=["skill", "agent", "quality"], help="Test explanation")
    parser.add_argument("--dashboard", action="store_true", help="Get dashboard data")

    args = parser.parse_args()

    visualizer = LearningVisualizer(args.storage_dir)

    if args.stats:
        summary = visualizer.event_recorder.get_learning_summary()
        print("Learning Visualizer Statistics:")
        print(f"  Total Events: {summary.get('total_events', 0)}")
        print(f"  Learning Velocity: {summary.get('learning_velocity', 0)} events/day")
        print(f"  Pattern Reuse Rate: {summary.get('pattern_reuse_rate', 0) * 100:.1f}%")
        print(f"  Quality Trend: {summary.get('quality_trend', 'unknown')}")
        print(f"  User Confidence: {summary.get('user_confidence', 0) * 100:.1f}%")

    elif args.record:
        event_id = visualizer.record_learning_event(
            LearningEventType.PATTERN_ACQUIRED,
            args.record,
            "quality +5 points",
            {"pattern_id": "test_123", "confidence": 0.92},
            0.92,
        )
        print(f"Recorded learning event: {event_id}")

    elif args.explain:
        if args.explain == "skill":
            context = {
                "task_type": "refactoring",
                "selected_skills": ["code-analysis", "quality-standards", "pattern-learning"],
            }
        elif args.explain == "agent":
            context = {
                "agent": "code-analyzer",
                "task_type": "refactoring",
                "reasoning": "Highly specialized for refactoring tasks",
            }
        elif args.explain == "quality":
            context = {
                "threshold": 95,
                "task_type": "security",
                "adjustments": {
                    "phase_adjustment": {"phase": "pre-release", "multiplier": 1.10},
                    "criticality_adjustment": {"criticality": "critical", "multiplier": 1.15},
                    "user_facing": True,
                },
            }

        explanation = visualizer.explain_decision(f"{args.explain}_selection", context, 0.92)
        print(f"Explanation: {explanation}")

    elif args.dashboard:
        data = visualizer.get_dashboard_data()
        print("Dashboard Data:")
        print(f"  Learning Summary: {data['summary']}")
        print(f"  Recent Events: {len(data['recent_events'])}")

    else:
        print("Learning Visualizer initialized")
        print("Use --stats, --record, --explain, or --dashboard to interact")


if __name__ == "__main__":
    main()
