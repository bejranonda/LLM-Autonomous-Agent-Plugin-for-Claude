#!/usr/bin/env python3
#     Predictive Quality Analytics for Autonomous Agent System
    """
Analyzes historical pattern data to predict quality outcomes and
provide proactive intervention triggers for optimal autonomous operations.
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import statistics


class PredictiveQualityAnalyzer:
    """Advanced predictive analytics for quality optimization"""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """Initialize the processor with default configuration."""
        self.patterns_dir = patterns_dir
        self.patterns_file = os.path.join(patterns_dir, "patterns.json")
        self.predictions_file = os.path.join(patterns_dir, "quality_predictions.json")

    def load_patterns(self) -> Dict:
        """Load and validate pattern data"""
        try:
            with open(self.patterns_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"patterns": [], "skill_effectiveness": {}, "agent_effectiveness": {}}

    def extract_quality_features(self, patterns: List[Dict]) -> List[Dict]:
        """Extract predictive features from pattern data"""
        features = []

        for pattern in patterns:
            # Handle both old and new pattern formats
            if "task_type" not in pattern and "pattern_id" in pattern:
                # New format pattern
                feature = {
                    "task_type": pattern.get("task_type", "unknown"),
                    "quality_score": pattern.get("outcome", {}).get("quality_score", 0),
                    "duration": pattern.get("execution", {}).get("duration_seconds", 0),
                    "success": pattern.get("outcome", {}).get("success", False),
                    "complexity": pattern.get("task_complexity", "medium"),
                    "skills_count": len(pattern.get("execution", {}).get("skills_used", [])),
                    "agents_count": len(pattern.get("execution", {}).get("agents_delegated", [])),
                    "timestamp": pattern.get("timestamp", ""),
                    "issues_found": pattern.get("outcome", {}).get("issues_found", 0),
                    "pattern_id": pattern.get("pattern_id", ""),
                }
            else:
                # Old format pattern
                feature = {
                    "task_type": pattern.get("task_type", "unknown"),
                    "quality_score": pattern.get("outcome", {}).get("quality_score", 0),
                    "duration": pattern.get("execution", {}).get("duration_seconds", 0),
                    "success": pattern.get("outcome", {}).get("success", False),
                    "complexity": pattern.get("task_complexity", "medium"),
                    "skills_count": len(pattern.get("execution", {}).get("skills_used", [])),
                    "agents_count": len(pattern.get("execution", {}).get("agents_delegated", [])),
                    "timestamp": pattern.get("timestamp", ""),
                    "issues_found": pattern.get("outcome", {}).get("issues_found", 0),
                    "pattern_id": pattern.get("pattern_id", ""),
                }

            features.append(feature)

        return features

    def calculate_task_type_baselines(self, features: List[Dict]) -> Dict[str, Dict]:
        """Calculate baseline metrics by task type"""
        baselines = defaultdict(list)

        for feature in features:
            task_type = feature["task_type"]
            baselines[task_type].append(feature)

        results = {}
        for task_type, type_features in baselines.items():
            if len(type_features) >= 2:  # Need at least 2 samples for meaningful stats
                quality_scores = [f["quality_score"] for f in type_features if f["quality_score"] > 0]
                durations = [f["duration"] for f in type_features if f["duration"] > 0]

                results[task_type] = {
                    "count": len(type_features),
                    "avg_quality": statistics.mean(quality_scores) if quality_scores else 0,
                    "quality_std": statistics.stdev(quality_scores) if len(quality_scores) > 1 else 0,
                    "avg_duration": statistics.mean(durations) if durations else 0,
                    "success_rate": sum(1 for f in type_features if f["success"]) / len(type_features),
                    "avg_issues": statistics.mean([f["issues_found"] for f in type_features]),
                    "confidence": min(len(type_features) / 5.0, 1.0),  # Confidence increases with more data
                }

        return results

    def identify_quality_patterns(self, features: List[Dict]) -> Dict:
        """Identify patterns that affect quality outcomes"""
        high_quality = [f for f in features if f["quality_score"] >= 90]
        low_quality = [f for f in features if f["quality_score"] < 80 and f["quality_score"] > 0]

        patterns = {"high_quality_indicators": {}, "low_quality_indicators": {}, "optimal_combinations": []}

        # Analyze skill combinations for high quality outcomes
        if high_quality:
            skill_combinations = defaultdict(int)
            for feature in high_quality:
                # Create skill combination signature
                skills = tuple(sorted(feature.get("skills_used", [])))
                if skills:
                    skill_combinations[skills] += 1

            # Top skill combinations for high quality
            patterns["optimal_combinations"] = [
                {"skills": list(comb), "frequency": count, "avg_quality": 95}
                for comb, count in sorted(skill_combinations.items(), key=lambda x: x[1], reverse=True)[:5]
            ]

        # Duration patterns
        if high_quality and low_quality:
            high_durations = [f["duration"] for f in high_quality if f["duration"] > 0]
            low_durations = [f["duration"] for f in low_quality if f["duration"] > 0]

            if high_durations:
                patterns["high_quality_indicators"]["optimal_duration"] = {
                    "min": min(high_durations),
                    "max": max(high_durations),
                    "avg": statistics.mean(high_durations),
                }

            if low_durations:
                patterns["low_quality_indicators"]["problematic_duration"] = {
                    "too_fast": min(low_durations) if len(low_durations) > 1 else None,
                    "too_slow": max(low_durations) if len(low_durations) > 1 else None,
                }

        return patterns

    def predict_quality_outcome(
        self, task_type: str, complexity: str = "medium", skills: List[str] = None, estimated_duration: int = None
    )-> Dict:
        """Predict Quality Outcome."""Predict quality outcome for a given task"""
        patterns_data = self.load_patterns()
        features = self.extract_quality_features(patterns_data.get("patterns", []))
        baselines = self.calculate_task_type_baselines(features)

        # Get baseline for task type
        baseline = baselines.get(task_type, {})
        if not baseline:
            return {
                "predicted_quality": 85,  # Default baseline
                "confidence": 0.3,
                "recommendations": ["Insufficient data for this task type"],
                "risk_factors": ["No historical patterns available"],
            }

        # Base prediction from historical average
        predicted_quality = baseline["avg_quality"]
        confidence = baseline["confidence"]

        # Adjustments based on complexity
        complexity_adjustments = {
            "simple": {"multiplier": 1.05, "confidence_boost": 0.1},
            "medium": {"multiplier": 1.0, "confidence_boost": 0.0},
            "complex": {"multiplier": 0.95, "confidence_boost": -0.1},
            "expert": {"multiplier": 0.9, "confidence_boost": -0.2},
        }

        if complexity in complexity_adjustments:
            adj = complexity_adjustments[complexity]
            predicted_quality *= adj["multiplier"]
            confidence += adj["confidence_boost"]

        # Adjustments based on skill selection
        if skills:
            skill_bonus = min(len(skills) * 2, 10)  # Up to 10 point bonus for comprehensive skills
            predicted_quality += skill_bonus

        # Adjustments based on duration
        if estimated_duration and baseline["avg_duration"] > 0:
            duration_ratio = estimated_duration / baseline["avg_duration"]
            if 0.8 <= duration_ratio <= 1.2:  # Within 20% of optimal
                confidence += 0.1
            elif duration_ratio > 2.0:  # Much longer than expected
                predicted_quality -= 5
            elif duration_ratio < 0.5:  # Much faster than expected
                predicted_quality -= 3

        # Ensure bounds and calculate risk factors
        predicted_quality = max(0, min(100, predicted_quality))
        confidence = max(0.1, min(1.0, confidence))

        risk_factors = []
        recommendations = []

        if predicted_quality < 85:
            risk_factors.append("Below optimal quality threshold")
            recommendations.append("Consider additional quality validation steps")

        if confidence < 0.5:
            risk_factors.append("Low confidence in prediction")
            recommendations.append("Gather more patterns for this task type")

        if complexity in ["complex", "expert"] and (not skills or len(skills) < 3):
            risk_factors.append("Insufficient skills for complex task")
            recommendations.append("Include comprehensive skill coverage")

        return {
            "predicted_quality": round(predicted_quality, 1),
            "confidence": round(confidence, 2),
            "baseline_quality": round(baseline["avg_quality"], 1),
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "historical_success_rate": round(baseline["success_rate"] * 100, 1),
            "estimated_duration": baseline["avg_duration"],
        }

    def generate_intervention_triggers(self) -> Dict[str, List[Dict]]:
        """Generate proactive intervention triggers based on patterns"""
        patterns_data = self.load_patterns()
        features = self.extract_quality_features(patterns_data.get("patterns", []))
        baselines = self.calculate_task_type_baselines(features)

        triggers = {"quality_gates": [], "resource_recommendations": [], "timing_alerts": []}

        # Quality gates for different task types
        for task_type, baseline in baselines.items():
            if baseline["confidence"] > 0.5:  # Only for confident baselines
                quality_threshold = max(85, baseline["avg_quality"] - 5)

                triggers["quality_gates"].append(
                    {
                        "task_type": task_type,
                        "min_quality_score": quality_threshold,
                        "confidence_required": 0.7,
                        "action_if_failed": "Enhanced validation and additional review",
                    }
                )

        # Resource recommendations based on historical success
        quality_patterns = self.identify_quality_patterns(features)

        for combo in quality_patterns.get("optimal_combinations", []):
            if combo["frequency"] >= 2:  # Repeated success patterns
                triggers["resource_recommendations"].append(
                    {
                        "skills_combination": combo["skills"],
                        "expected_quality": combo["avg_quality"],
                        "success_frequency": combo["frequency"],
                        "recommendation": "Use this skill combination for similar tasks",
                    }
                )

        # Timing alerts for unusual durations
        for task_type, baseline in baselines.items():
            if baseline["avg_duration"] > 0:
                triggers["timing_alerts"].append(
                    {
                        "task_type": task_type,
                        "expected_duration": baseline["avg_duration"],
                        "alert_if_longer": baseline["avg_duration"] * 2.0,
                        "alert_if_shorter": baseline["avg_duration"] * 0.5,
                        "recommendation": "Investigate unusual execution times",
                    }
                )

        return triggers

    def save_predictions(self, predictions: Dict):
        """Save predictions for dashboard integration"""
        os.makedirs(self.patterns_dir, exist_ok=True)

        # Add metadata
        predictions["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "model_version": "1.0.0",
            "patterns_analyzed": len(self.load_patterns().get("patterns", [])),
            "prediction_confidence": "improving with more data",
        }

        with open(self.predictions_file, "w", encoding="utf-8") as f:
            json.dump(predictions, f, indent=2, ensure_ascii=False)

    def run_comprehensive_analysis(self) -> Dict:
        """Run complete predictive analytics analysis"""
        print("Running Predictive Quality Analytics...")

        patterns_data = self.load_patterns()
        features = self.extract_quality_features(patterns_data.get("patterns", []))

        if not features:
            print("No pattern data available for analysis")
            return {"status": "no_data", "message": "No patterns found"}

        print(f"Analyzing {len(features)} historical patterns...")

        # Core analyses
        baselines = self.calculate_task_type_baselines(features)
        quality_patterns = self.identify_quality_patterns(features)
        intervention_triggers = self.generate_intervention_triggers()

        # Generate predictions for common task types
        common_task_types = list(baselines.keys())[:10]  # Top 10 task types
        predictions = {}

        for task_type in common_task_types:
            predictions[task_type] = self.predict_quality_outcome(task_type)

        # Compile comprehensive results
        results = {
            "status": "success",
            "analysis_summary": {
                "patterns_analyzed": len(features),
                "task_types_covered": len(baselines),
                "high_confidence_predictions": len([b for b in baselines.values() if b["confidence"] > 0.7]),
                "quality_patterns_found": len(quality_patterns.get("optimal_combinations", [])),
            },
            "baselines": baselines,
            "quality_patterns": quality_patterns,
            "intervention_triggers": intervention_triggers,
            "predictions": predictions,
            "recommendations": self._generate_strategic_recommendations(baselines, quality_patterns),
        }

        # Save results
        self.save_predictions(results)

        print(f"Predictive analytics complete")
        print(f"   {len(baselines)} task type baselines established")
        print(f"   {len(intervention_triggers['quality_gates'])} quality gates created")
        print(f"   Predictions saved to {self.predictions_file}")

        return results

    def _generate_strategic_recommendations(self, baselines: Dict, patterns: Dict) -> List[Dict]:
        """Generate strategic recommendations based on analysis"""
        recommendations = []

        # Identify task types needing improvement
        low_quality_tasks = [
            task_type
            for task_type, baseline in baselines.items()
            if baseline["avg_quality"] < 85 and baseline["confidence"] > 0.5
        ]

        if low_quality_tasks:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "quality_improvement",
                    "title": "Focus on Quality Improvement",
                    "description": f"Task types with suboptimal quality: {', '.join(low_quality_tasks)}",
                    "action": "Implement enhanced validation for these task types",
                    "expected_impact": "+10-15 quality points",
                }
            )

        # Identify successful patterns to leverage
        if patterns.get("optimal_combinations"):
            top_combination = patterns["optimal_combinations"][0]
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "pattern_leverage",
                    "title": "Leverage Successful Skill Combinations",
                    "description": f"Top combination: {', '.join(top_combination['skills'])}",
                    "action": "Apply this skill combination to similar tasks",
                    "expected_impact": "+5-8 quality points",
                }
            )

        # Data collection recommendations
        low_confidence_tasks = [task_type for task_type, baseline in baselines.items() if baseline["confidence"] < 0.5]

        if low_confidence_tasks:
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "data_collection",
                    "title": "Expand Pattern Coverage",
                    "description": f"Task types needing more data: {', '.join(low_confidence_tasks)}",
                    "action": "Execute more tasks of these types to improve predictions",
                    "expected_impact": "+20-30% prediction accuracy",
                }
            )

        return recommendations


def main():
    """CLI interface for predictive quality analytics"""
    import argparse

    parser = argparse.ArgumentParser(description="Predictive Quality Analytics")
    parser.add_argument("--dir", default=".claude-patterns", help="Patterns directory")
    parser.add_argument("--predict", nargs=2, metavar=("TASK_TYPE", "COMPLEXITY"), help="Predict quality for specific task")
    parser.add_argument("--analyze", action="store_true", help="Run comprehensive analysis")
    parser.add_argument("--triggers", action="store_true", help="Generate intervention triggers")

    args = parser.parse_args()

    analyzer = PredictiveQualityAnalyzer(args.dir)

    if args.predict:
        task_type, complexity = args.predict
        prediction = analyzer.predict_quality_outcome(task_type, complexity)
        print(f"\nQuality Prediction for {task_type} ({complexity}):")
        print(f"   Predicted Score: {prediction['predicted_quality']}/100")
        print(f"   Confidence: {prediction['confidence']*100:.1f}%")
        print(f"   Historical Success Rate: {prediction['historical_success_rate']}%")
        if prediction["recommendations"]:
            print(f"   Recommendations: {', '.join(prediction['recommendations'])}")

    elif args.analyze:
        results = analyzer.run_comprehensive_analysis()
        if results["status"] == "success":
            summary = results["analysis_summary"]
            print(f"\nAnalysis Summary:")
            print(f"   Patterns Analyzed: {summary['patterns_analyzed']}")
            print(f"   Task Types Covered: {summary['task_types_covered']}")
            print(f"   High Confidence Predictions: {summary['high_confidence_predictions']}")
            print(f"   Quality Gates Created: {len(results['intervention_triggers']['quality_gates'])}")

    elif args.triggers:
        triggers = analyzer.generate_intervention_triggers()
        print(f"\nIntervention Triggers Generated:")
        print(f"   Quality Gates: {len(triggers['quality_gates'])}")
        print(f"   Resource Recommendations: {len(triggers['resource_recommendations'])}")
        print(f"   Timing Alerts: {len(triggers['timing_alerts'])}")

    else:
        # Default: run comprehensive analysis
        analyzer.run_comprehensive_analysis()


if __name__ == "__main__":
    main()
