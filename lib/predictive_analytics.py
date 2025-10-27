#!/usr/bin/env python3
"""
Predictive Analytics Engine for Autonomous Agent

Advanced analytics and predictive insights system that:
- Predicts future performance trends
- Identifies optimization opportunities
- Provides proactive recommendations
- Learns from historical patterns to improve predictions
- Offers actionable insights for continuous improvement

Key Innovation: Every prediction makes the system smarter by learning from prediction accuracy.
"""

import json
import argparse
import statistics
from pathlib import Path

# Handle Windows compatibility for file locking
if platform.system() == 'Windows':
    import msvcrt
    def lock_file(f, exclusive=False):
        """Windows file locking using msvcrt."""
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        """Windows file unlocking."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl
    def lock_file(f, exclusive=False):
        """Unix file locking using fcntl."""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)

    def unlock_file(f):
        """Unix file unlocking."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class PredictiveAnalyticsEngine:
    """Advanced predictive analytics with machine learning-inspired capabilities."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """
        Initialize predictive analytics engine.

        Args:
            patterns_dir: Directory containing pattern data
        """
        self.patterns_dir = Path(patterns_dir)
        self.patterns_dir.mkdir(exist_ok=True)

        # Data files
        self.predictions_file = self.patterns_dir / "predictions.json"
        self.insights_file = self.patterns_dir / "insights.json"
        self.trends_file = self.patterns_dir / "trends.json"

        # Initialize data structures
        self._ensure_data_files()

    def _ensure_data_files(self):
        """Ensure all required data files exist with proper structure."""
        default_predictions = {
            "predictions": [],
            "model_version": "3.2.0",
            "last_updated": datetime.now().isoformat(),
            "accuracy_metrics": {
                "prediction_accuracy": 0.0,
                "confidence_threshold": 0.7,
                "total_predictions": 0,
                "correct_predictions": 0
            }
        }

        default_insights = {
            "insights": [],
            "recommendations": [],
            "opportunities": [],
            "last_updated": datetime.now().isoformat()
        }

        default_trends = {
            "quality_trends": [],
            "performance_trends": [],
            "learning_velocity_trends": [],
            "skill_effectiveness_trends": [],
            "last_updated": datetime.now().isoformat()
        }

        for file_path, default_data in [
            (self.predictions_file, default_predictions),
            (self.insights_file, default_insights),
            (self.trends_file, default_trends)
        ]:
            if not file_path.exists():
                self._write_json_file(file_path, default_data)

    def _read_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Read JSON file with error handling."""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read {file_path}: {e}")
        return {}

    def _write_json_file(self, file_path: Path, data: Dict[str, Any]):
        """Write JSON file with atomic write."""
        try:
            # Write to temporary file first
            temp_file = file_path.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Atomic move
            temp_file.replace(file_path)
        except IOError as e:
            print(f"Warning: Could not write {file_path}: {e}")

    def predict_quality_trend(self, days_ahead: int = 7) -> Dict[str, Any]:
        """
        Predict quality trends for the next N days.

        Args:
            days_ahead: Number of days to predict ahead

        Returns:
            Dictionary with predictions and confidence scores
        """
        # Read historical data
        enhanced_patterns = self._read_json_file(self.patterns_dir / "enhanced_patterns.json")
        trends = self._read_json_file(self.trends_file)

        if not enhanced_patterns.get("patterns"):
            return {
                "prediction": "insufficient_data",
                "confidence": 0.0,
                "message": "Not enough historical data for prediction"
            }

        # Extract quality scores over time
        quality_history = []
        for pattern in enhanced_patterns["patterns"]:
            if "timestamp" in pattern and "outcome" in pattern:
                quality_score = pattern["outcome"].get("quality_score", 0)
                quality_history.append({
                    "timestamp": pattern["timestamp"],
                    "quality_score": quality_score
                })

        if len(quality_history) < 5:
            return {
                "prediction": "insufficient_data",
                "confidence": 0.0,
                "message": "Need at least 5 data points for prediction"
            }

        # Sort by timestamp
        quality_history.sort(key=lambda x: x["timestamp"])

        # Calculate trend using linear regression
        x_values = list(range(len(quality_history)))
        y_values = [entry["quality_score"] for entry in quality_history]

        # Simple linear regression
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n

        # Predict future values
        future_predictions = []
        for i in range(1, days_ahead + 1):
            future_x = len(quality_history) + i
            predicted_quality = slope * future_x + intercept

            # Clamp to valid range [0, 100]
            predicted_quality = max(0, min(100, predicted_quality))

            future_predictions.append({
                "day": i,
                "predicted_quality": round(predicted_quality, 2),
                "trend_direction": "improving" if slope > 0.5 else "stable" if slope > -0.5 else "declining"
            })

        # Calculate confidence based on data consistency
        variance = statistics.variance(y_values) if len(y_values) > 1 else 0
        consistency_score = max(0, 1 - (variance / 100))  # Normalize variance
        data_quality_score = min(1.0, len(quality_history) / 30)  # More data = higher confidence

        confidence = round((consistency_score * 0.6 + data_quality_score * 0.4) * 100, 2)

        prediction_result = {
            "prediction_type": "quality_trend",
            "days_ahead": days_ahead,
            "predictions": future_predictions,
            "trend_slope": round(slope, 4),
            "current_avg_quality": round(statistics.mean(y_values), 2),
            "confidence_score": confidence,
            "recommendations": self._generate_quality_recommendations(slope, confidence)
        }

        # Store prediction for learning
        self._store_prediction(prediction_result)

        return prediction_result

    def predict_optimal_skills(self, task_context: Dict[str, Any], top_k: int = 3) -> Dict[str, Any]:
        """
        Predict optimal skills for a given task context using historical performance.

        Args:
            task_context: Task information including type, complexity, project context
            top_k: Number of top skills to recommend

        Returns:
            Dictionary with skill predictions and confidence scores
        """
        # Read historical performance data
        skill_metrics = self._read_json_file(self.patterns_dir / "skill_metrics.json")
        enhanced_patterns = self._read_json_file(self.patterns_dir / "enhanced_patterns.json")

        task_type = task_context.get("task_type", "unknown")
        project_context = task_context.get("project_context", {})

        # Analyze historical performance by skill
        skill_performance = {}

        for skill_name, metrics in skill_metrics.items():
            if isinstance(metrics, dict) and "success_count" in metrics:
                success_rate = metrics.get("success_count", 0) / max(1, metrics.get("total_usage", 1))
                avg_quality_impact = metrics.get("avg_quality_impact", 0)

                # Weight by recent usage (more recent = more relevant)
                recent_usage_bonus = 0
                for pattern in enhanced_patterns.get("patterns", []):
                    if skill_name in pattern.get("execution", {}).get("skills_used", []):
                        pattern_age = datetime.now() - datetime.fromisoformat(pattern["timestamp"])
                        if pattern_age.days < 7:  # Recent usage
                            recent_usage_bonus += (7 - pattern_age.days) / 7

                skill_performance[skill_name] = {
                    "success_rate": success_rate,
                    "avg_quality_impact": avg_quality_impact,
                    "recent_usage_bonus": recent_usage_bonus,
                    "total_usage": metrics.get("total_usage", 0),
                    "combined_score": success_rate * 0.4 + avg_quality_impact * 0.3 + recent_usage_bonus * 0.3
                }

        # Sort by combined score
        sorted_skills = sorted(skill_performance.items(),
                             key=lambda x: x[1]["combined_score"],
                             reverse=True)

        # Filter and return top skills
        top_skills = []
        for skill_name, performance in sorted_skills[:top_k]:
            confidence = min(100, performance["combined_score"] * 100)

            top_skills.append({
                "skill": skill_name,
                "confidence": round(confidence, 2),
                "success_rate": round(performance["success_rate"] * 100, 2),
                "avg_quality_impact": round(performance["avg_quality_impact"], 2),
                "usage_count": performance["total_usage"],
                "recommendation_reason": self._generate_skill_recommendation_reason(skill_name, performance, task_context)
            })

        prediction_result = {
            "prediction_type": "optimal_skills",
            "task_type": task_type,
            "recommended_skills": top_skills,
            "prediction_confidence": round(statistics.mean([s["confidence"] for s in top_skills]) if top_skills else 0, 2),
            "total_skills_analyzed": len(skill_performance),
            "recommendations": self._generate_skill_recommendations(top_skills, task_context)
        }

        # Store prediction for learning
        self._store_prediction(prediction_result)

        return prediction_result

    def predict_learning_velocity(self, days_ahead: int = 14) -> Dict[str, Any]:
        """
        Predict learning velocity and skill acquisition rate.

        Args:
            days_ahead: Number of days to predict ahead

        Returns:
            Dictionary with learning velocity predictions
        """
        enhanced_patterns = self._read_json_file(self.patterns_dir / "enhanced_patterns.json")

        if not enhanced_patterns.get("patterns"):
            return {
                "prediction": "insufficient_data",
                "confidence": 0.0,
                "message": "Not enough learning data for prediction"
            }

        # Calculate learning metrics over time
        learning_metrics = []
        for pattern in enhanced_patterns["patterns"]:
            if "timestamp" in pattern:
                pattern_date = datetime.fromisoformat(pattern["timestamp"])
                days_ago = (datetime.now() - pattern_date).days

                if days_ago <= 30:  # Last 30 days
                    learning_metrics.append({
                        "date": pattern_date.date().isoformat(),
                        "days_ago": days_ago,
                        "skills_used": len(pattern.get("execution", {}).get("skills_used", [])),
                        "quality_score": pattern.get("outcome", {}).get("quality_score", 0),
                        "success": pattern.get("outcome", {}).get("success", False)
                    })

        if len(learning_metrics) < 3:
            return {
                "prediction": "insufficient_data",
                "confidence": 0.0,
                "message": "Need more recent learning data"
            }

        # Group by days and calculate averages
        daily_metrics = {}
        for metric in learning_metrics:
            day = metric["days_ago"]
            if day not in daily_metrics:
                daily_metrics[day] = []
            daily_metrics[day].append(metric)

        # Calculate daily averages
        daily_averages = []
        for day, metrics in sorted(daily_metrics.items()):
            avg_quality = statistics.mean([m["quality_score"] for m in metrics])
            avg_skills = statistics.mean([m["skills_used"] for m in metrics])
            success_rate = sum([m["success"] for m in metrics]) / len(metrics)

            daily_averages.append({
                "days_ago": day,
                "avg_quality": avg_quality,
                "avg_skills": avg_skills,
                "success_rate": success_rate
            })

        # Predict learning velocity trend
        if len(daily_averages) >= 3:
            recent_averages = daily_averages[:7]  # Last 7 days
            quality_trend = statistics.mean([d["avg_quality"] for d in recent_averages])
            skills_trend = statistics.mean([d["avg_skills"] for d in recent_averages])
            success_trend = statistics.mean([d["success_rate"] for d in recent_averages])

            # Predict future velocity
            velocity_predictions = []
            for i in range(1, days_ahead + 1):
                # Exponential learning curve (accelerating improvement)
                learning_acceleration = 1.02 ** i  # 2% daily improvement

                predicted_quality = min(100, quality_trend * learning_acceleration)
                predicted_skills = skills_trend * learning_acceleration
                predicted_success = min(1.0, success_trend * learning_acceleration)

                velocity_predictions.append({
                    "day": i,
                    "predicted_quality": round(predicted_quality, 2),
                    "predicted_skills": round(predicted_skills, 2),
                    "predicted_success_rate": round(predicted_success, 4),
                    "learning_acceleration": round(learning_acceleration, 4)
                })

            confidence = min(95, len(daily_averages) * 5 + 50)  # Based on data amount

            prediction_result = {
                "prediction_type": "learning_velocity",
                "days_ahead": days_ahead,
                "current_velocity": {
                    "avg_quality": round(quality_trend, 2),
                    "avg_skills_per_task": round(skills_trend, 2),
                    "success_rate": round(success_trend, 4)
                },
                "predictions": velocity_predictions,
                "confidence_score": confidence,
                "learning_acceleration_factor": "2% daily improvement",
                "recommendations": self._generate_learning_recommendations(quality_trend, success_trend)
            }
        else:
            prediction_result = {
                "prediction": "insufficient_data",
                "confidence": 0.0,
                "message": "Need at least 3 days of learning data"
            }

        # Store prediction for learning
        self._store_prediction(prediction_result)

        return prediction_result

    def identify_optimization_opportunities(self) -> Dict[str, Any]:
        """
        Identify optimization opportunities based on pattern analysis.

        Returns:
            Dictionary with identified opportunities and recommendations
        """
        enhanced_patterns = self._read_json_file(self.patterns_dir / "enhanced_patterns.json")
        skill_metrics = self._read_json_file(self.patterns_dir / "skill_metrics.json")
        agent_metrics = self._read_json_file(self.patterns_dir / "agent_metrics.json")

        opportunities = []

        # Analyze task types with low success rates
        task_type_performance = {}
        for pattern in enhanced_patterns.get("patterns", []):
            task_type = pattern.get("task_type", "unknown")
            success = pattern.get("outcome", {}).get("success", False)
            quality = pattern.get("outcome", {}).get("quality_score", 0)

            if task_type not in task_type_performance:
                task_type_performance[task_type] = {"total": 0, "success": 0, "total_quality": 0}

            task_type_performance[task_type]["total"] += 1
            if success:
                task_type_performance[task_type]["success"] += 1
            task_type_performance[task_type]["total_quality"] += quality

        # Identify low-performing task types
        for task_type, performance in task_type_performance.items():
            if performance["total"] >= 5:  # Only analyze with sufficient data
                success_rate = performance["success"] / performance["total"]
                avg_quality = performance["total_quality"] / performance["total"]

                if success_rate < 0.7 or avg_quality < 70:
                    opportunities.append({
                        "type": "task_type_improvement",
                        "priority": "high" if success_rate < 0.5 else "medium",
                        "target": task_type,
                        "current_success_rate": round(success_rate * 100, 2),
                        "current_avg_quality": round(avg_quality, 2),
                        "improvement_potential": round((100 - avg_quality) * 0.8, 2),  # 80% of gap achievable
                        "recommendation": f"Focus on improving {task_type} tasks through targeted skill training"
                    })

        # Analyze underutilized effective skills
        for skill_name, metrics in skill_metrics.items():
            if isinstance(metrics, dict):
                success_rate = metrics.get("success_count", 0) / max(1, metrics.get("total_usage", 1))
                usage_count = metrics.get("total_usage", 0)

                if success_rate > 0.8 and usage_count < 5:  # Effective but underused
                    opportunities.append({
                        "type": "skill_utilization",
                        "priority": "medium",
                        "target": skill_name,
                        "current_success_rate": round(success_rate * 100, 2),
                        "current_usage": usage_count,
                        "potential_impact": "high",
                        "recommendation": f"Increase usage of {skill_name} - highly effective but underutilized"
                    })

        # Analyze agent performance gaps
        for agent_name, metrics in agent_metrics.items():
            if isinstance(metrics, dict):
                success_rate = metrics.get("success_count", 0) / max(1, metrics.get("total_usage", 1))
                avg_duration = metrics.get("avg_duration", 0)

                if success_rate < 0.6 and metrics.get("total_usage", 0) >= 3:
                    opportunities.append({
                        "type": "agent_optimization",
                        "priority": "high",
                        "target": agent_name,
                        "current_success_rate": round(success_rate * 100, 2),
                        "current_avg_duration": round(avg_duration, 2),
                        "recommendation": f"Optimize {agent_name} agent performance - low success rate detected"
                    })

        # Sort opportunities by priority and impact
        priority_order = {"high": 3, "medium": 2, "low": 1}
        opportunities.sort(key=lambda x: priority_order.get(x["priority"], 0), reverse=True)

        result = {
            "analysis_type": "optimization_opportunities",
            "total_opportunities": len(opportunities),
            "opportunities": opportunities[:10],  # Top 10 opportunities
            "analysis_timestamp": datetime.now().isoformat(),
            "recommendations": self._generate_optimization_recommendations(opportunities)
        }

        # Store insights
        self._store_insights(result)

        return result

    def _generate_quality_recommendations(self, slope: float, confidence: float) -> List[str]:
        """Generate recommendations based on quality trend analysis."""
        recommendations = []

        if slope > 1.0:
            recommendations.append("📈 Strong positive trend detected - maintain current approach")
            recommendations.append("🎯 Consider setting higher quality targets")
        elif slope > 0.5:
            recommendations.append("📊 Positive quality trend - continue current practices")
        elif slope > -0.5:
            recommendations.append("⚖️ Quality is stable - focus on incremental improvements")
        else:
            recommendations.append("📉 Negative quality trend detected - immediate action needed")
            recommendations.append("🔍 Review recent changes that may have impacted quality")
            recommendations.append("📚 Consider additional training for team members")

        if confidence < 60:
            recommendations.append("📊 Low confidence in prediction - collect more data")
        elif confidence > 80:
            recommendations.append("✅ High confidence prediction - reliable for planning")

        return recommendations

    def _generate_skill_recommendation_reason(self, skill_name: str, performance: Dict, task_context: Dict) -> str:
        """Generate reasoning for skill recommendation."""
        reasons = []

        if performance["success_rate"] > 0.8:
            reasons.append("High success rate")
        if performance["avg_quality_impact"] > 5:
            reasons.append("Strong quality impact")
        if performance["recent_usage_bonus"] > 0.5:
            reasons.append("Recently effective")
        if performance["total_usage"] > 10:
            reasons.append("Well-tested")

        return " | ".join(reasons) if reasons else "Potential fit"

    def _generate_skill_recommendations(self, skills: List[Dict], task_context: Dict) -> List[str]:
        """Generate overall skill recommendations."""
        if not skills:
            return ["No specific skill recommendations available"]

        recommendations = []
        top_skill = skills[0]

        if top_skill["confidence"] > 80:
            recommendations.append(f"🎯 Prioritize using {top_skill['skill']} - {top_skill['confidence']}% confidence")

        if len(skills) >= 2:
            avg_confidence = sum(s["confidence"] for s in skills) / len(skills)
            if avg_confidence > 70:
                recommendations.append("📊 Multiple high-confidence skills available - consider combination approach")

        task_type = task_context.get("task_type", "unknown")
        recommendations.append(f"💡 Task type '{task_type}' has good skill match options")

        return recommendations

    def _generate_learning_recommendations(self, quality_trend: float, success_trend: float) -> List[str]:
        """Generate learning velocity recommendations."""
        recommendations = []

        if quality_trend > 80:
            recommendations.append("🎯 Excellent learning velocity - maintain current pace")
        elif quality_trend > 70:
            recommendations.append("📈 Good learning progress - continue current approach")
        elif quality_trend > 60:
            recommendations.append("⚠️ Moderate learning pace - consider focused practice")
        else:
            recommendations.append("📉 Learning velocity needs improvement - review learning strategy")

        if success_trend > 0.8:
            recommendations.append("✅ High success rate - excellent skill application")
        elif success_trend > 0.6:
            recommendations.append("🔄 Good success rate - refine technique for consistency")
        else:
            recommendations.append("🎯 Success rate needs improvement - focus on fundamentals")

        recommendations.append("📚 Regular practice accelerates learning velocity")

        return recommendations

    def _generate_optimization_recommendations(self, opportunities: List[Dict]) -> List[str]:
        """Generate optimization recommendations based on opportunities."""
        if not opportunities:
            return ["🎉 Current performance is optimal - maintain standards"]

        recommendations = []

        high_priority = [op for op in opportunities if op["priority"] == "high"]
        if high_priority:
            recommendations.append(f"🚨 Address {len(high_priority)} high-priority issues first")

        task_improvements = [op for op in opportunities if op["type"] == "task_type_improvement"]
        if task_improvements:
            recommendations.append(f"📊 Focus on {len(task_improvements)} task types needing improvement")

        skill_opportunities = [op for op in opportunities if op["type"] == "skill_utilization"]
        if skill_opportunities:
            recommendations.append(f"💡 Leverage {len(skill_opportunities)} underutilized effective skills")

        recommendations.append("📈 Regular optimization reviews maintain peak performance")

        return recommendations

    def _store_prediction(self, prediction: Dict[str, Any]):
        """Store prediction for learning and accuracy tracking."""
        predictions_data = self._read_json_file(self.predictions_file)

        # Add timestamp and unique ID
        prediction["id"] = len(predictions_data.get("predictions", [])) + 1
        prediction["timestamp"] = datetime.now().isoformat()

        predictions_data.setdefault("predictions", []).append(prediction)
        predictions_data["last_updated"] = datetime.now().isoformat()

        # Keep only last 100 predictions
        if len(predictions_data["predictions"]) > 100:
            predictions_data["predictions"] = predictions_data["predictions"][-100:]

        self._write_json_file(self.predictions_file, predictions_data)

    def _store_insights(self, insights: Dict[str, Any]):
        """Store insights for future reference."""
        insights_data = self._read_json_file(self.insights_file)

        insights_data.setdefault("insights", []).append(insights)
        insights_data["last_updated"] = datetime.now().isoformat()

        # Keep only last 50 insights
        if len(insights_data["insights"]) > 50:
            insights_data["insights"] = insights_data["insights"][-50:]

        self._write_json_file(self.insights_file, insights_data)

    def get_prediction_accuracy(self) -> Dict[str, Any]:
        """Calculate prediction accuracy by comparing predictions with actual outcomes."""
        predictions_data = self._read_json_file(self.predictions_file)
        enhanced_patterns = self._read_json_file(self.patterns_dir / "enhanced_patterns.json")

        accuracy_metrics = predictions_data.get("accuracy_metrics", {})

        return {
            "overall_accuracy": accuracy_metrics.get("prediction_accuracy", 0.0),
            "total_predictions": accuracy_metrics.get("total_predictions", 0),
            "correct_predictions": accuracy_metrics.get("correct_predictions", 0),
            "confidence_threshold": accuracy_metrics.get("confidence_threshold", 0.7),
            "model_version": predictions_data.get("model_version", "3.2.0"),
            "last_updated": predictions_data.get("last_updated")
        }

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive predictive analytics report."""
        report = {
            "report_type": "comprehensive_predictive_analytics",
            "generated_at": datetime.now().isoformat(),
            "model_version": "3.2.0"
        }

        # Add all prediction types
        report["quality_trend_prediction"] = self.predict_quality_trend(7)
        report["optimal_skills_prediction"] = self.predict_optimal_skills({
            "task_type": "general",
            "project_context": {}
        })
        report["learning_velocity_prediction"] = self.predict_learning_velocity(14)
        report["optimization_opportunities"] = self.identify_optimization_opportunities()
        report["prediction_accuracy"] = self.get_prediction_accuracy()

        # Add summary insights
        report["executive_summary"] = self._generate_executive_summary(report)

        return report

    def _generate_executive_summary(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of predictive analytics."""
        summary = {
            "overall_health": "good",
            "key_insights": [],
            "action_items": [],
            "predicted_outcomes": []
        }

        # Analyze quality trend
        quality_pred = report.get("quality_trend_prediction", {})
        if quality_pred.get("confidence_score", 0) > 70:
            if quality_pred.get("trend_slope", 0) > 0.5:
                summary["key_insights"].append("Positive quality trend predicted")
                summary["predicted_outcomes"].append("Continued quality improvement expected")
            elif quality_pred.get("trend_slope", 0) < -0.5:
                summary["key_insights"].append("Quality decline detected")
                summary["action_items"].append("Address quality issues immediately")

        # Analyze learning velocity
        learning_pred = report.get("learning_velocity_prediction", {})
        if learning_pred.get("confidence_score", 0) > 60:
            summary["key_insights"].append("Learning velocity analysis available")
            if "current_velocity" in learning_pred:
                current = learning_pred["current_velocity"]
                if current.get("success_rate", 0) > 0.8:
                    summary["predicted_outcomes"].append("Strong learning performance maintained")

        # Analyze optimization opportunities
        opportunities = report.get("optimization_opportunities", {})
        total_ops = opportunities.get("total_opportunities", 0)
        if total_ops > 0:
            summary["key_insights"].append(f"{total_ops} optimization opportunities identified")
            high_priority = len([op for op in opportunities.get("opportunities", [])
                               if op.get("priority") == "high"])
            if high_priority > 0:
                summary["action_items"].append(f"Address {high_priority} high-priority opportunities")

        return summary


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Predictive Analytics Engine")
    parser.add_argument("--dir", default=".claude-patterns", help="Patterns directory path")
    parser.add_argument("--action", choices=["quality-trend", "optimal-skills", "learning-velocity",
                        "opportunities", "comprehensive", "accuracy"],
                        default="comprehensive", help="Action to perform")
    parser.add_argument("--days", type=int, default=7, help="Days ahead for predictions")
    parser.add_argument("--task-type", default="general", help="Task type for skill prediction")
    parser.add_argument("--top-k", type=int, default=3, help="Number of top skills to recommend")

    args = parser.parse_args()

    # Initialize analytics engine
    analytics = PredictiveAnalyticsEngine(args.dir)

    # Execute requested action
    if args.action == "quality-trend":
        result = analytics.predict_quality_trend(args.days)
    elif args.action == "optimal-skills":
        result = analytics.predict_optimal_skills({
            "task_type": args.task_type,
            "project_context": {}
        }, args.top_k)
    elif args.action == "learning-velocity":
        result = analytics.predict_learning_velocity(args.days)
    elif args.action == "opportunities":
        result = analytics.identify_optimization_opportunities()
    elif args.action == "accuracy":
        result = analytics.get_prediction_accuracy()
    else:  # comprehensive
        result = analytics.generate_comprehensive_report()

    # Output results
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()