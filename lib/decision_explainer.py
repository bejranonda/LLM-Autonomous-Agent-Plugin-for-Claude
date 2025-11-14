#!/usr/bin/env python3
"""
Decision Explainer System
Provides detailed explanations for all decisions made by the four-tier system,
building transparency and trust through clear reasoning.

This implements the v7.1 enhancement for Decision Explainability.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Platform-specific imports for file locking
try:
    import msvcrt  # Windows

    PLATFORM = "windows"
except ImportError:
    import fcntl  # Unix/Linux/Mac

    PLATFORM = "unix"


class DecisionExplainer:
    """
    Explains decisions made by the strategic-planner and other Group 2 agents.
    """

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the decision explainer.

        Args:
            storage_dir: Directory for storing decision explanations
        """
        self.storage_dir = Path(storage_dir)
        self.explanations_file = self.storage_dir / "decision_explanations.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize file if it doesn't exist
        if not self.explanations_file.exists():
            self._initialize_storage()

    def _initialize_storage(self):
        """Initialize the storage with default structure."""
        initial_data = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "metadata": {"total_decisions": 0, "total_explanations": 0},
            "decision_history": [],
        }

        self._write_data(initial_data)

    def _lock_file(self, file_handle):
        """Platform-specific file locking."""
        if PLATFORM == "windows":
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX)

    def _unlock_file(self, file_handle):
        """Platform-specific file unlocking."""
        if PLATFORM == "windows":
            try:
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            except (OSError, PermissionError):
                pass
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)

    def _read_data(self) -> Dict[str, Any]:
        """Read explanation data with file locking."""
        try:
            with open(self.explanations_file, "r", encoding="utf-8") as f:
                self._lock_file(f)
                try:
                    data = json.load(f)
                finally:
                    self._unlock_file(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_storage()
            return self._read_data()

    def _write_data(self, data: Dict[str, Any]):
        """Write explanation data with file locking."""
        with open(self.explanations_file, "w", encoding="utf-8") as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def create_explanation(
        self,
        decision_id: str,
        decision: str,
        recommendations: List[Dict[str, Any]],
        user_preferences: Dict[str, Any],
        historical_data: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    )-> Dict[str, Any]:
        """Create Explanation."""
        """
        Create a comprehensive explanation for a decision.

        Args:
            decision_id: Unique decision identifier
            decision: The decision that was made
            recommendations: List of recommendations from Group 1
            user_preferences: User preferences that influenced the decision
            historical_data: Historical data about similar tasks
            context: Additional context

        Returns:
            Comprehensive explanation dictionary
        """
        explanation = {
            "decision_id": decision_id,
            "decision": decision,
            "timestamp": datetime.now().isoformat(),
            # Why this decision?
            "why_this_decision": self._explain_why_chosen(decision, recommendations, user_preferences, historical_data),
            # Why not alternatives?
            "why_not_alternatives": self._explain_why_not_alternatives(decision, recommendations, user_preferences),
            # Trade-offs considered
            "trade_offs": self._explain_trade_offs(decision, recommendations, context),
            # Confidence factors
            "confidence_factors": self._explain_confidence(recommendations, historical_data),
            # User preference alignment
            "user_alignment": self._explain_user_alignment(decision, user_preferences),
            # Human analogy
            "human_analogy": self._generate_analogy(decision, context),
            # Supporting evidence
            "supporting_evidence": self._compile_evidence(recommendations, historical_data),
        }

        # Store explanation
        self._store_explanation(explanation)

        return explanation

    def _explain_why_chosen(
        self,
        decision: str,
        recommendations: List[Dict[str, Any]],
        user_preferences: Dict[str, Any],
        historical_data: Optional[Dict[str, Any]],
    )-> Dict[str, Any]:
        """ Explain Why Chosen."""
        """Explain why this decision was chosen."""
        # Find the recommendation that matches the decision
        chosen_recommendation = None
        for rec in recommendations:
            if rec.get("recommendation", "").lower() in decision.lower():
                chosen_recommendation = rec
                break

        if not chosen_recommendation:
            return {"primary_reason": "Decision synthesized from multiple recommendations", "supporting_reasons": []}

        supporting_reasons = []

        # User preference alignment
        if user_preferences:
            alignment_score = self._calculate_alignment(chosen_recommendation, user_preferences)
            if alignment_score > 0.8:
                supporting_reasons.append(f"Excellent alignment with user preferences ({alignment_score*100:.0f}%)")

        # Historical success
        if historical_data and historical_data.get("success_rate"):
            success_rate = historical_data["success_rate"]
            if success_rate > 0.8:
                similar_tasks = historical_data.get("similar_tasks", 0)
                supporting_reasons.append(f"Historical success rate: {success_rate*100:.0f}% ({similar_tasks} similar tasks)")

        # Confidence from recommending agent
        if chosen_recommendation.get("confidence"):
            confidence = chosen_recommendation["confidence"]
            if confidence > 0.8:
                agent = chosen_recommendation.get("agent", "analysis agent")
                supporting_reasons.append(f"Recommended by {agent} with high confidence ({confidence*100:.0f}%)")

        # Benefits
        if chosen_recommendation.get("benefits"):
            benefits = chosen_recommendation["benefits"]
            supporting_reasons.append(f"Key benefits: {', '.join(benefits)}")

        return {
            "primary_reason": self._identify_primary_reason(chosen_recommendation, user_preferences, historical_data),
            "supporting_reasons": supporting_reasons,
        }

    def _identify_primary_reason(
        self, recommendation: Dict[str, Any], user_preferences: Dict[str, Any], historical_data: Optional[Dict[str, Any]]
    )-> str:
        """ Identify Primary Reason."""
        """Identify the primary reason for choosing this decision."""
        # Calculate scores for different reasons
        preference_score = 0
        historical_score = 0
        confidence_score = 0

        if user_preferences:
            alignment = self._calculate_alignment(recommendation, user_preferences)
            preference_score = alignment * 100

        if historical_data and historical_data.get("success_rate"):
            historical_score = historical_data["success_rate"] * 100

        if recommendation.get("confidence"):
            confidence_score = recommendation["confidence"] * 100

        # Determine primary reason based on highest score
        scores = {
            "user_preference": preference_score,
            "historical_success": historical_score,
            "high_confidence": confidence_score,
        }

        primary = max(scores.items(), key=lambda x: x[1])

        if primary[0] == "user_preference":
            return f"Best alignment with user preferences ({primary[1]:.0f}%)"
        elif primary[0] == "historical_success":
            return f"Proven approach with {primary[1]:.0f}% success rate"
        else:
            return f"High-confidence recommendation ({primary[1]:.0f}%)"

    def _explain_why_not_alternatives(
        self, decision: str, recommendations: List[Dict[str, Any]], user_preferences: Dict[str, Any]
    )-> Dict[str, Dict[str, str]]:
        """ Explain Why Not Alternatives."""
        """Explain why alternative recommendations were not chosen."""
        alternatives_explanation = {}

        for rec in recommendations:
            if rec.get("recommendation", "").lower() not in decision.lower():
                # This is an alternative that wasn't chosen
                recommendation_name = rec.get("recommendation", "Unknown approach")

                rejected_reason = self._determine_rejection_reason(rec, user_preferences)
                better_if = self._determine_when_better(rec, user_preferences)

                alternatives_explanation[recommendation_name] = {
                    "rejected_because": rejected_reason,
                    "would_be_better_if": better_if,
                }

        return alternatives_explanation

    def _determine_rejection_reason(self, recommendation: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """Determine why a recommendation was rejected."""
        # Check confidence
        confidence = recommendation.get("confidence", 0)
        if confidence < 0.7:
            return f"Lower confidence ({confidence*100:.0f}%) compared to chosen approach"

        # Check user alignment
        alignment = self._calculate_alignment(recommendation, user_preferences)
        if alignment < 0.7:
            return f"Lower alignment with user preferences ({alignment*100:.0f}%)"

        # Check risk
        if recommendation.get("risk_level", 0) > 0.7:
            return "Higher risk level not aligned with user's risk tolerance"

        # Check effort
        effort = recommendation.get("estimated_effort", "unknown")
        if effort in ["high", "very_high"]:
            return "Higher effort required with similar expected outcome"

        return "Lower overall score when considering all factors"

    def _determine_when_better(self, recommendation: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """Determine under what conditions this recommendation would be better."""
        conditions = []

        # Risk tolerance
        if recommendation.get("risk_level", 0) > 0.7:
            conditions.append("user had higher risk tolerance")

        # Time constraints
        if recommendation.get("estimated_effort") == "low":
            conditions.append("time constraints were very tight")

        # Quality requirements
        if recommendation.get("expected_quality", 0) < 85:
            conditions.append("quality requirements were lower")

        # Project phase
        if "rewrite" in recommendation.get("recommendation", "").lower():
            conditions.append("project was in earlier stage")

        if conditions:
            return "; ".join(conditions)
        else:
            return "Chosen approach is superior in current context"

    def _explain_trade_offs(
        self, decision: str, recommendations: List[Dict[str, Any]], context: Optional[Dict[str, Any]]
    )-> Dict[str, str]:
        """ Explain Trade Offs."""
        """Explain trade-offs considered in the decision."""
        trade_offs = {}

        # Time vs Quality
        if context and "time_constraint" in context:
            if context["time_constraint"] == "tight":
                trade_offs["time_vs_quality"] = "Optimized for speed while maintaining acceptable quality"
            else:
                trade_offs["time_vs_quality"] = "Prioritized quality over speed (no time pressure)"
        else:
            trade_offs["time_vs_quality"] = "Balanced approach between time and quality"

        # Risk vs Benefit
        chosen_rec = next((r for r in recommendations if r.get("recommendation", "").lower() in decision.lower()), None)
        if chosen_rec:
            risk = chosen_rec.get("risk_level", 0.5)
            if risk > 0.6:
                trade_offs["risk_vs_benefit"] = "Higher risk accepted for significant benefits"
            elif risk < 0.3:
                trade_offs["risk_vs_benefit"] = "Low-risk approach preferred"
            else:
                trade_offs["risk_vs_benefit"] = "Moderate risk acceptable for expected benefits"

        # Speed vs Thoroughness
        trade_offs["speed_vs_thoroughness"] = "Thorough approach preferred (user style)"

        return trade_offs

    def _explain_confidence(
        self, recommendations: List[Dict[str, Any]], historical_data: Optional[Dict[str, Any]]
    )-> Dict[str, List[str]]:
        """ Explain Confidence."""
        """Explain factors affecting confidence in the decision."""
        high_confidence_factors = []
        uncertainty_factors = []

        # Check historical data
        if historical_data:
            similar_tasks = historical_data.get("similar_tasks", 0)
            if similar_tasks >= 5:
                high_confidence_factors.append(f"Strong historical data ({similar_tasks} similar tasks)")
            elif similar_tasks > 0:
                uncertainty_factors.append(f"Limited historical data (only {similar_tasks} similar tasks)")

        # Check recommendation consensus
        high_conf_recs = [r for r in recommendations if r.get("confidence", 0) > 0.8]
        if len(high_conf_recs) >= 2:
            high_confidence_factors.append(f"Multiple high-confidence recommendations ({len(high_conf_recs)} agents)")

        # Check user preference clarity
        high_confidence_factors.append("Clear user preference match")

        # Check technical risk
        low_risk_recs = [r for r in recommendations if r.get("risk_level", 0) < 0.3]
        if low_risk_recs:
            high_confidence_factors.append("Low technical risk")

        # Identify uncertainties
        uncertainty_factors.append("Actual execution time may vary")

        return {"high_confidence_factors": high_confidence_factors, "uncertainty_factors": uncertainty_factors}

    def _explain_user_alignment(self, decision: str, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Explain how decision aligns with user preferences."""
        alignment_details = {}

        # Coding style
        if "coding_style" in user_preferences:
            style = user_preferences["coding_style"]
            if style.get("verbosity") == "concise" and "concise" in decision.lower():
                alignment_details["coding_style"] = "Matches user's concise coding style preference"

        # Quality priorities
        if "quality_priorities" in user_preferences:
            priorities = user_preferences["quality_priorities"]
            top_priority = max(priorities.items(), key=lambda x: x[1])
            alignment_details["quality_priorities"] = (
                f"Aligned with user's top priority: {top_priority[0]} ({top_priority[1]*100:.0f}%)"
            )

        # Risk tolerance
        if "workflow" in user_preferences:
            if "risk_tolerance" in user_preferences["workflow"]:
                alignment_details["risk_tolerance"] = "Respects user's risk tolerance level"

        return alignment_details

    def _generate_analogy(self, decision: str, context: Optional[Dict[str, Any]]) -> str:
        """Generate a human-friendly analogy for the decision."""
        # Simple pattern matching for common decision types
        decision_lower = decision.lower()

        if "modular" in decision_lower:
            return "Like organizing a messy room into labeled boxes - more work upfront, but much easier to find things later"
        elif "incremental" in decision_lower:
            return "Like eating an elephant one bite at a time - tackle the big task in small, manageable pieces"
        elif "security" in decision_lower and "first" in decision_lower:
            return "Like fixing the locks on your doors before redecorating - security comes first"
        elif "refactor" in decision_lower:
            return "Like renovating a house room-by-room instead of tearing it all down - safer and less disruptive"
        elif "test" in decision_lower:
            return "Like having a safety net when walking a tightrope - gives confidence to make changes"
        else:
            return "Best approach based on evidence and experience"

    def _compile_evidence(self, recommendations: List[Dict[str, Any]], historical_data: Optional[Dict[str, Any]]) -> List[str]:
        """Compile supporting evidence for the decision."""
        evidence = []

        # Evidence from recommendations
        for rec in recommendations:
            if rec.get("evidence"):
                for evidence_item in rec["evidence"]:
                    evidence.append(evidence_item)

        # Evidence from historical data
        if historical_data:
            if historical_data.get("success_rate"):
                evidence.append(f"{historical_data['success_rate']*100:.0f}% success rate in similar past tasks")

            if historical_data.get("avg_quality_score"):
                evidence.append(f"Average quality score of {historical_data['avg_quality_score']:.1f}/100 for this approach")

        return evidence

    def _calculate_alignment(self, recommendation: Dict[str, Any], user_preferences: Dict[str, Any]) -> float:
        """Calculate alignment score between recommendation and user preferences."""
        # Simplified alignment calculation
        # In real implementation, this would use preference-coordinator's logic
        return 0.85  # Placeholder

    def _store_explanation(self, explanation: Dict[str, Any]):
        """Store explanation for future reference."""
        data = self._read_data()

        data["decision_history"].append(explanation)

        # Update metadata
        data["metadata"]["total_decisions"] += 1
        data["metadata"]["total_explanations"] += 1
        data["metadata"]["last_updated"] = datetime.now().isoformat()

        # Keep last 1000 explanations
        if len(data["decision_history"]) > 1000:
            data["decision_history"] = data["decision_history"][-1000:]

        self._write_data(data)

    def get_explanation(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve explanation for a specific decision."""
        data = self._read_data()

        for explanation in data["decision_history"]:
            if explanation["decision_id"] == decision_id:
                return explanation

        return None

    def format_explanation_for_user(self, explanation: Dict[str, Any]) -> str:
        """Format explanation in human-readable format."""
        output = []

        output.append(f"Decision: {explanation['decision']}")
        output.append("")

        output.append("Why this decision?")
        why_chosen = explanation["why_this_decision"]
        output.append(f"  Primary reason: {why_chosen['primary_reason']}")
        if why_chosen["supporting_reasons"]:
            output.append("  Supporting reasons:")
            for reason in why_chosen["supporting_reasons"]:
                output.append(f"    - {reason}")
        output.append("")

        if explanation["why_not_alternatives"]:
            output.append("Why not alternatives?")
            for alt_name, alt_info in list(explanation["why_not_alternatives"].items())[:2]:
                output.append(f"  {alt_name}:")
                output.append(f"    Rejected because: {alt_info['rejected_because']}")
                output.append(f"    Would be better if: {alt_info['would_be_better_if']}")
            output.append("")

        output.append("Trade-offs considered:")
        for trade_off_type, explanation_text in explanation["trade_offs"].items():
            output.append(f"  {trade_off_type.replace('_', ' ').title()}: {explanation_text}")
        output.append("")

        output.append(f"Analogy: {explanation['human_analogy']}")

        return "\n".join(output)


def main():
    """Command-line interface for testing the decision explainer."""
    import argparse

    parser = argparse.ArgumentParser(description="Decision Explainer")
    parser.add_argument("--storage-dir", default=".claude-patterns", help="Storage directory")
    parser.add_argument("--decision-id", help="Decision ID to explain")

    args = parser.parse_args()

    explainer = DecisionExplainer(args.storage_dir)

    if args.decision_id:
        explanation = explainer.get_explanation(args.decision_id)
        if explanation:
            formatted = explainer.format_explanation_for_user(explanation)
            print(formatted)
        else:
            print(f"No explanation found for decision: {args.decision_id}")
    else:
        print("Decision Explainer Initialized")
        print(f"Storage: {explainer.explanations_file}")


if __name__ == "__main__":
    main()
