#!/usr/bin/env python3
"""
Smart Recommendation Engine for Autonomous Agent Plugin

Provides intelligent workflow and optimization recommendations based on learned patterns.
Lightweight alternative to complex agent delegation system.

Features:
- Pattern-based skill recommendations
- Success rate calculations
- Quality predictions
- Risk assessment
- Confidence scoring

Version: 1.0.0
Compatible with: v7.6.9+ architecture
"""

import json
import argparse
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter

# Import pattern storage
try:
    from pattern_storage import PatternStorage
except ImportError:
    print("Error: Could not import pattern_storage.py", file=sys.stderr)
    sys.exit(1)


class RecommendationEngine:
    """Lightweight recommendation engine using existing pattern data."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """Initialize recommendation engine."""
        self.storage = PatternStorage(patterns_dir)

    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        Analyze task description to extract key information.

        Args:
            task_description: User's task description

        Returns:
            Task analysis dictionary
        """
        # Extract keywords and classify task
        keywords = re.findall(r'\b\w+\b', task_description.lower()) if task_description else []

        # Task type classification
        task_type = "general"
        complexity = "medium"

        # Simple keyword-based classification
        if any(word in keywords for word in ["refactor", "restructure", "reorganize"]):
            task_type = "refactoring"
            complexity = "medium-high"
        elif any(word in keywords for word in ["test", "testing", "spec"]):
            task_type = "testing"
            complexity = "medium"
        elif any(word in keywords for word in ["bug", "fix", "error", "issue"]):
            task_type = "bugfix"
            complexity = "low-medium"
        elif any(word in keywords for word in ["feature", "add", "implement", "create"]):
            task_type = "feature-implementation"
            complexity = "high"
        elif any(word in keywords for word in ["document", "docs", "readme"]):
            task_type = "documentation"
            complexity = "low"
        elif any(word in keywords for word in ["analyze", "analysis", "review"]):
            task_type = "analysis"
            complexity = "medium"

        return {
            "type": task_type,
            "complexity": complexity,
            "keywords": keywords,
            "original": task_description
        }

    def get_pattern_recommendations(self, task_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get recommendations based on similar patterns.

        Args:
            task_analysis: Task analysis dictionary

        Returns:
            List of pattern-based recommendations
        """
        # Search for similar patterns
        patterns = self.storage.get_similar_patterns(
            task_type=task_analysis["type"],
            context={"keywords": task_analysis["keywords"]},
            limit=5
        )

        recommendations = []
        for pattern in patterns:
            # Calculate recommendation score
            score = self._calculate_recommendation_score(pattern, task_analysis)

            recommendations.append({
                "pattern_id": pattern.get("id", "unknown"),
                "quality_score": pattern.get("quality_score", 0),
                "success_rate": pattern.get("success_rate", 0),
                "skills_used": pattern.get("skills_used", []),
                "agents_delegated": pattern.get("agents_delegated", []),
                "execution_time": pattern.get("execution_time", 0),
                "recommendation_score": score,
                "reuse_count": pattern.get("reuse_count", 0)
            })

        # Sort by recommendation score
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return recommendations

    def _calculate_recommendation_score(self, pattern: Dict[str, Any], task_analysis: Dict[str, Any]) -> float:
        """Calculate recommendation score for a pattern."""
        score = 0.0

        # Quality score contribution (30%)
        quality = pattern.get("quality_score", 0)
        score += (quality / 100) * 0.3

        # Success rate contribution (25%)
        success_rate = pattern.get("success_rate", 0)
        score += (success_rate / 100) * 0.25

        # Reuse count contribution (20%)
        reuse_count = pattern.get("reuse_count", 0)
        score += min(reuse_count / 10, 1.0) * 0.2

        # Execution time (15%) - faster is better
        exec_time = pattern.get("execution_time", 60)
        if exec_time > 0:
            time_score = max(0, 1 - (exec_time / 3600))  # 1 hour = 0 score
            score += time_score * 0.15

        # Skill diversity (10%)
        skills = pattern.get("skills_used", [])
        if skills:
            diversity_score = min(len(skills) / 5, 1.0)
            score += diversity_score * 0.1

        return score

    def generate_skill_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate skill recommendations from pattern data."""
        skill_scores = defaultdict(list)

        # Collect skill effectiveness data
        for rec in recommendations:
            for skill in rec["skills_used"]:
                effectiveness = self.storage.get_skill_effectiveness(skill)
                skill_scores[skill].append(effectiveness.get("success_rate", 0))

        # Calculate average success rates
        final_recommendations = []
        for skill, scores in skill_scores.items():
            avg_success = sum(scores) / len(scores) if scores else 0
            usage_count = len(scores)

            final_recommendations.append({
                "skill": skill,
                "success_rate": avg_success,
                "usage_count": usage_count,
                "recommendation": "PASS" if avg_success >= 80 else "WARN"
            })

        # Sort by success rate
        final_recommendations.sort(key=lambda x: x["success_rate"], reverse=True)
        return final_recommendations

    def assess_risks(self, task_analysis: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess risks for the task."""
        risks = []
        risk_level = "LOW"
        risk_score = 0

        # Task complexity risks
        if task_analysis["complexity"] in ["high", "medium-high"]:
            risks.append({
                "type": "HIGH" if task_analysis["complexity"] == "high" else "MEDIUM",
                "description": "High Task Complexity",
                "mitigation": "Break into smaller sub-tasks",
                "time_impact": "+5-10 minutes"
            })
            risk_score += 30 if task_analysis["complexity"] == "high" else 20

        # Low pattern count risks
        if len(recommendations) == 0:
            risks.append({
                "type": "HIGH",
                "description": "No Similar Patterns Found",
                "mitigation": "Use general approach with extra validation",
                "time_impact": "+8-12 minutes"
            })
            risk_score += 40
        elif len(recommendations) < 2:
            risks.append({
                "type": "MEDIUM",
                "description": "Limited Pattern Data",
                "mitigation": "Proceed with caution, validate frequently",
                "time_impact": "+3-5 minutes"
            })
            risk_score += 20

        # Quality risks
        if recommendations and recommendations[0]["quality_score"] < 85:
            risks.append({
                "type": "MEDIUM",
                "description": "Historical Quality Below Threshold",
                "mitigation": "Add quality-standards skill",
                "quality_impact": "+5-8 points"
            })
            risk_score += 15

        # Determine overall risk level
        if risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "level": risk_level,
            "score": risk_score,
            "risks": risks,
            "mitigations": [risk["mitigation"] for risk in risks]
        }

    def generate_recommendations(self, task_description: str = "") -> Dict[str, Any]:
        """
        Generate comprehensive recommendations.

        Args:
            task_description: User's task description

        Returns:
            Complete recommendation report
        """
        # Analyze task
        task_analysis = self.analyze_task(task_description)

        # Get pattern recommendations
        pattern_recommendations = self.get_pattern_recommendations(task_analysis)

        # Generate skill recommendations
        skill_recommendations = self.generate_skill_recommendations(pattern_recommendations)

        # Assess risks
        risk_assessment = self.assess_risks(task_analysis, pattern_recommendations)

        # Generate predictions
        predictions = self._generate_predictions(pattern_recommendations, risk_assessment)

        return {
            "task": task_analysis,
            "recommendations": pattern_recommendations[:3],  # Top 3
            "skills": skill_recommendations[:5],  # Top 5
            "risks": risk_assessment,
            "predictions": predictions,
            "generated_at": datetime.now().isoformat()
        }

    def _generate_predictions(self, recommendations: List[Dict[str, Any]], risks: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quality and time predictions."""
        if not recommendations:
            return {
                "quality_score": 75,
                "confidence": 50,
                "estimated_time": "15-20 minutes",
                "success_probability": 70
            }

        # Use top recommendation as baseline
        top_rec = recommendations[0]
        base_quality = top_rec["quality_score"]
        base_time = top_rec["execution_time"]

        # Adjust for risks
        risk_penalty = risks["score"] * 0.1  # 10% penalty per risk point
        adjusted_quality = max(70, base_quality - risk_penalty)

        # Adjust time for complexity
        time_multiplier = 1.0
        if risks["level"] == "HIGH":
            time_multiplier = 1.3
        elif risks["level"] == "MEDIUM":
            time_multiplier = 1.15

        adjusted_time = int(base_time * time_multiplier)

        # Calculate confidence based on pattern data
        confidence = min(95, len(recommendations) * 15 + top_rec["success_rate"] * 0.5)

        return {
            "quality_score": round(adjusted_quality, 1),
            "confidence": round(confidence, 1),
            "estimated_time": f"{adjusted_time}-{int(adjusted_time * 1.2)} minutes",
            "success_probability": round(adjusted_quality * 0.9, 1)
        }


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Generate smart recommendations")
    parser.add_argument("--task", type=str, help="Task description", default="")
    parser.add_argument("--dir", type=str, help="Patterns directory", default=".claude-patterns")
    parser.add_argument("--format", type=str, choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    # Initialize engine
    engine = RecommendationEngine(args.dir)

    # Generate recommendations
    recommendations = engine.generate_recommendations(args.task)

    # Output results
    if args.format == "json":
        print(json.dumps(recommendations, indent=2))
    else:
        print(format_recommendations_text(recommendations))


def format_recommendations_text(recs: Dict[str, Any]) -> str:
    """Format recommendations as text (similar to original design)."""
    task = recs["task"]
    predictions = recs["predictions"]
    risks = recs["risks"]

    output = []
    output.append("=" * 56)
    output.append("  SMART RECOMMENDATIONS")
    output.append("=" * 56)
    output.append("")

    if task["original"]:
        output.append(f"Task: \"{task['original']}\"")
        output.append(f"Analyzed as: {task['type']}, {task['complexity']} complexity")
    else:
        output.append("Task: General analysis")
        output.append(f"Analyzed as: {task['type']}, {task['complexity']} complexity")

    output.append("")

    # Top recommendation
    if recs["recommendations"]:
        top = recs["recommendations"][0]
        output.append("+- [RECOMMENDED] APPROACH ({}% confidence) -------------+".format(int(predictions["confidence"])))
        output.append("|                                                         |")
        output.append(f"| Expected Quality: {int(predictions['quality_score'])}/100 (+{int(predictions['quality_score'] - 75)} from baseline)          |")
        output.append(f"| Estimated Time:   {predictions['estimated_time']}                        |")
        output.append("|                                                         |")
        output.append("| Recommended Skills:                                     |")

        for skill in recs["skills"][:3]:
            status = skill["recommendation"]
            output.append(f"| {status}. [{status}] {skill['skill']} ({int(skill['success_rate'])}% success rate)".ljust(57) + " |")

        output.append("|                                                         |")
        output.append("| Based on: {} similar successful patterns                |".format(len(recs["recommendations"])))
        output.append("|                                                         |")
        output.append("+---------------------------------------------------------+")
    else:
        output.append("+- [RECOMMENDED] APPROACH (50% confidence) -------------+")
        output.append("|                                                         |")
        output.append("| Expected Quality: 75/100 (baseline)                   |")
        output.append("| Estimated Time:   15-20 minutes                       |")
        output.append("|                                                         |")
        output.append("| Recommended Skills:                                     |")
        output.append("| 1. [PASS] code-analysis (baseline skill)               |")
        output.append("| 2. [PASS] quality-standards (recommended)              |")
        output.append("|                                                         |")
        output.append("| Based on: General best practices                       |")
        output.append("|                                                         |")
        output.append("+---------------------------------------------------------+")

    output.append("")

    # Alternative approaches
    output.append("+- [ALTERNATIVE] APPROACHES ------------------------------+")
    output.append("|                                                         |")

    if len(recs["recommendations"]) > 1:
        for i, rec in enumerate(recs["recommendations"][1:3], 2):
            quality = rec["quality_score"]
            time_est = f"{rec['execution_time']}-{int(rec['execution_time'] * 1.2)} min"
            output.append(f"| {i}. Pattern-Based Approach ({int(rec['recommendation_score'] * 100)}% confidence)".ljust(57) + " |")
            output.append(f"|    Quality: {int(quality)}/100 | Time: {time_est}".ljust(57) + " |")
            output.append(f"|    Skills: {', '.join(rec['skills_used'][:2])}".ljust(57) + " |")
            output.append("|                                                         |")
    else:
        output.append("| 2. Minimal Approach (60% confidence)                   |")
        output.append("|    Quality: 70/100 | Time: 10-12 min                 |")
        output.append("|    Skills: code-analysis only                          |")
        output.append("|    [WARN] Lower quality but faster                     |")
        output.append("|                                                         |")

    output.append("+---------------------------------------------------------+")
    output.append("")

    # Risk assessment
    output.append("+- [{}] RISK ASSESSMENT ------------------------------------+".format(risks["level"]))
    output.append("|                                                         |")
    output.append(f"| Overall Risk: {risks['level']} ({risks['score']}/100)".ljust(57) + " |")
    output.append("|                                                         |")

    if risks["risks"]:
        for i, risk in enumerate(risks["risks"], 1):
            output.append(f"| {i}. [{risk['type']}] {risk['description']}".ljust(57) + " |")
            output.append(f"|    -> Mitigation: {risk['mitigation']}".ljust(57) + " |")
            if "time_impact" in risk:
                output.append(f"|    -> {risk['time_impact']}".ljust(57) + " |")
            output.append("|                                                         |")
    else:
        output.append("| [PASS] No significant risks identified                 |")
        output.append("|                                                         |")

    output.append("+---------------------------------------------------------+")
    output.append("")

    # Key insights
    output.append("+- [KEY] INSIGHTS ----------------------------------------+")
    output.append("|                                                         |")

    if recs["recommendations"]:
        output.append("| [PASS] Pattern-based approach available                     |")
        output.append(f"| [PASS] Expected success rate: {int(predictions['success_probability'])}%              |")
        output.append(f"| [PASS] Quality improvement: +{int(predictions['quality_score'] - 75)} points         |")
        if len(recs["skills"]) >= 3:
            output.append("| [PASS] Multi-skill approach recommended                |")
    else:
        output.append("| [WARN] No similar patterns found                         |")
        output.append("| [PASS] Using general best practices                      |")
        output.append("| [WARN] Consider breaking task into smaller steps         |")

    output.append("|                                                         |")
    output.append("+---------------------------------------------------------+")
    output.append("")

    # Final recommendation
    output.append("=" * 56)
    output.append("  RECOMMENDATION: Proceed with recommended approach")
    if predictions["confidence"] >= 80:
        output.append("  High confidence - expected excellent results")
    elif predictions["confidence"] >= 60:
        output.append("  Good confidence - recommended approach")
    else:
        output.append("  Moderate confidence - validate frequently")
    output.append("=" * 56)

    return "\n".join(output)


if __name__ == "__main__":
    main()