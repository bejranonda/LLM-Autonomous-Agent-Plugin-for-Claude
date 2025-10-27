#!/usr/bin/env python3
"""
Learning Analytics Dashboard for Autonomous Claude Agent Plugin

Real-time visualization and analysis of learning progress, skill effectiveness,
agent performance, and pattern quality trends.
"""

import json
import argparse
import sys
import platform
from datetime import datetime, timedelta
from pathlib import Path
# Handle Windows compatibility
if platform.system() == 'Windows':
    import msvcrt
    def lock_file(f, exclusive=False):
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)
    def unlock_file(f):
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl
    def lock_file(f, exclusive=False):
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
    def unlock_file(f):
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class LearningAnalyticsDashboard:
    """Generate comprehensive learning analytics reports and visualizations."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """Initialize learning analytics dashboard."""
        self.patterns_dir = Path(patterns_dir)
        self.enhanced_patterns_file = self.patterns_dir / "enhanced_patterns.json"
        self.skill_metrics_file = self.patterns_dir / "skill_metrics.json"
        self.agent_metrics_file = self.patterns_dir / "agent_metrics.json"
        self.cross_project_file = self.patterns_dir / "cross_project_patterns.json"
        self.predictions_file = self.patterns_dir / "skill_predictions.json"

    def _read_json(self, file_path: Path) -> Dict[str, Any]:
        """Read JSON file with error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def generate_ascii_chart(self, data: List[float], width: int = 50, height: int = 10, title: str = "") -> str:
        """Generate ASCII chart for terminal display."""
        if not data:
            return "No data available"

        lines = []
        if title:
            lines.append(title)
            lines.append("=" * len(title))

        # Normalize data to chart height
        min_val, max_val = min(data), max(data)
        value_range = max_val - min_val if max_val != min_val else 1

        # Create chart
        chart_lines = []
        for y in range(height, 0, -1):
            line = ""
            threshold = min_val + (value_range * y / height)

            for i, value in enumerate(data[-width:]):  # Show last 'width' data points
                if value >= threshold:
                    line += "█"
                else:
                    line += " "

            # Add y-axis label
            if y == height:
                chart_lines.append(f"{max_val:6.1f} │{line}│")
            elif y == 1:
                chart_lines.append(f"{min_val:6.1f} │{line}│")
            elif y == height // 2:
                chart_lines.append(f"{(max_val + min_val) / 2:6.1f} │{line}│")
            else:
                chart_lines.append(f"       │{line}│")

        lines.extend(chart_lines)

        # Add x-axis
        lines.append(f"       └{'─' * width}┘")
        lines.append(f"        {len(data) - width:>{width // 2 - 3}} → {len(data):<{width // 2 - 3}}")

        return "\n".join(lines)

    def generate_bar_chart(self, data: Dict[str, float], width: int = 40, title: str = "") -> str:
        """Generate horizontal bar chart for terminal display."""
        if not data:
            return "No data available"

        lines = []
        if title:
            lines.append(title)
            lines.append("=" * len(title))

        # Sort by value
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        max_val = max(v for _, v in sorted_data) if sorted_data else 1

        # Calculate max label length
        max_label_len = max(len(label) for label, _ in sorted_data) if sorted_data else 0

        for label, value in sorted_data:
            bar_length = int((value / max_val) * width)
            bar = "█" * bar_length
            lines.append(f"{label:>{max_label_len}} │ {bar} {value:.2f}")

        return "\n".join(lines)

    def calculate_learning_velocity(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate how fast the system is learning."""
        if len(patterns) < 10:
            return {"status": "insufficient_data", "message": "Need at least 10 patterns"}

        # Group patterns by week
        patterns_by_week = defaultdict(list)
        for pattern in patterns:
            timestamp = datetime.fromisoformat(pattern["timestamp"])
            week_key = timestamp.strftime("%Y-W%U")
            patterns_by_week[week_key].append(pattern)

        # Calculate average quality by week
        weekly_quality = {}
        for week, week_patterns in patterns_by_week.items():
            avg_quality = sum(p["outcome"]["quality_score"] for p in week_patterns) / len(week_patterns)
            weekly_quality[week] = avg_quality

        # Sort by week
        sorted_weeks = sorted(weekly_quality.items())

        if len(sorted_weeks) < 3:
            return {"status": "insufficient_data", "message": "Need at least 3 weeks of data"}

        # Calculate improvement rate
        first_3_weeks = [q for _, q in sorted_weeks[:3]]
        last_3_weeks = [q for _, q in sorted_weeks[-3:]]

        avg_early = sum(first_3_weeks) / len(first_3_weeks)
        avg_recent = sum(last_3_weeks) / len(last_3_weeks)

        improvement_rate = (avg_recent - avg_early) / len(sorted_weeks)

        # Calculate acceleration (is improvement rate increasing?)
        if len(sorted_weeks) >= 6:
            mid_point = len(sorted_weeks) // 2
            first_half_improvement = (sorted_weeks[mid_point][1] - sorted_weeks[0][1]) / mid_point
            second_half_improvement = (sorted_weeks[-1][1] - sorted_weeks[mid_point][1]) / (len(sorted_weeks) - mid_point)
            acceleration = second_half_improvement - first_half_improvement
        else:
            acceleration = 0.0

        return {
            "status": "calculated",
            "weeks_analyzed": len(sorted_weeks),
            "early_average_quality": avg_early,
            "recent_average_quality": avg_recent,
            "total_improvement": avg_recent - avg_early,
            "improvement_per_week": improvement_rate,
            "acceleration": acceleration,
            "trajectory": "accelerating" if acceleration > 0.5 else "linear" if acceleration > -0.5 else "decelerating",
            "weekly_quality": dict(sorted_weeks)
        }

    def analyze_skill_synergies(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze which skill combinations work best together."""
        combo_stats = defaultdict(lambda: {
            "count": 0,
            "total_quality": 0.0,
            "successes": 0,
            "patterns": []
        })

        # Collect combination statistics
        for pattern in patterns:
            skills = pattern.get("execution", {}).get("skills_loaded", [])
            if len(skills) < 2:
                continue

            # Create all pairs
            for i in range(len(skills)):
                for j in range(i + 1, len(skills)):
                    pair = tuple(sorted([skills[i], skills[j]]))

                    outcome = pattern.get("outcome", {})
                    quality = outcome.get("quality_score", 0)
                    success = outcome.get("success", False)

                    combo_stats[pair]["count"] += 1
                    combo_stats[pair]["total_quality"] += quality
                    if success:
                        combo_stats[pair]["successes"] += 1
                    combo_stats[pair]["patterns"].append(pattern["pattern_id"])

        # Calculate synergy scores
        synergies = []
        for pair, stats in combo_stats.items():
            if stats["count"] < 3:  # Need at least 3 occurrences
                continue

            avg_quality = stats["total_quality"] / stats["count"]
            success_rate = stats["successes"] / stats["count"]

            # Synergy score combines quality and success rate
            synergy_score = (avg_quality / 100) * success_rate * stats["count"]

            synergies.append({
                "skill_pair": list(pair),
                "usage_count": stats["count"],
                "average_quality": avg_quality,
                "success_rate": success_rate,
                "synergy_score": synergy_score,
                "recommendation": "highly_recommended" if synergy_score > 5 else "recommended" if synergy_score > 2 else "use_with_caution"
            })

        # Sort by synergy score
        synergies.sort(key=lambda x: x["synergy_score"], reverse=True)
        return synergies

    def analyze_learning_patterns(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in how the system learns."""
        if not patterns:
            return {"status": "no_data"}

        # Patterns by task type
        by_task_type = defaultdict(list)
        for pattern in patterns:
            task_type = pattern.get("task_classification", {}).get("type", "unknown")
            by_task_type[task_type].append(pattern)

        # Calculate learning curves for each task type
        learning_curves = {}
        for task_type, type_patterns in by_task_type.items():
            if len(type_patterns) < 3:
                continue

            # Sort by timestamp
            sorted_patterns = sorted(type_patterns, key=lambda p: p["timestamp"])

            # Calculate quality progression
            qualities = [p["outcome"]["quality_score"] for p in sorted_patterns]

            # Calculate improvement rate
            if len(qualities) >= 2:
                first_quality = qualities[0]
                last_quality = qualities[-1]
                improvement = last_quality - first_quality
                improvement_rate = improvement / len(qualities)
            else:
                improvement = 0
                improvement_rate = 0

            learning_curves[task_type] = {
                "pattern_count": len(qualities),
                "initial_quality": qualities[0],
                "current_quality": qualities[-1],
                "total_improvement": improvement,
                "improvement_per_task": improvement_rate,
                "quality_progression": qualities
            }

        # Identify fastest learning areas
        fastest_learning = sorted(
            [(task, curve["improvement_per_task"]) for task, curve in learning_curves.items()],
            key=lambda x: x[1],
            reverse=True
        )

        # Identify slowest learning areas
        slowest_learning = sorted(
            [(task, curve["improvement_per_task"]) for task, curve in learning_curves.items()],
            key=lambda x: x[1]
        )

        return {
            "learning_curves": learning_curves,
            "fastest_learning_areas": fastest_learning[:3],
            "slowest_learning_areas": slowest_learning[:3],
            "insights": self._generate_learning_insights(learning_curves)
        }

    def _generate_learning_insights(self, learning_curves: Dict[str, Any]) -> List[str]:
        """Generate insights from learning curves."""
        insights = []

        # Find plateaus (areas where learning has stalled)
        for task_type, curve in learning_curves.items():
            if curve["improvement_per_task"] < 0.5 and curve["pattern_count"] >= 5:
                insights.append(f"Learning plateau detected in {task_type} - may need new approaches or skills")

        # Find rapid learners
        for task_type, curve in learning_curves.items():
            if curve["improvement_per_task"] > 2.0:
                insights.append(f"Rapid learning in {task_type} - effective skill combinations identified")

        # Find areas needing attention
        for task_type, curve in learning_curves.items():
            if curve["current_quality"] < 75 and curve["pattern_count"] >= 5:
                insights.append(f"Low quality in {task_type} despite multiple attempts - review approach")

        return insights

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive learning analytics report."""
        # Load all data
        patterns_db = self._read_json(self.enhanced_patterns_file)
        skill_metrics = self._read_json(self.skill_metrics_file)
        agent_metrics = self._read_json(self.agent_metrics_file)
        cross_project = self._read_json(self.cross_project_file)
        predictions = self._read_json(self.predictions_file)

        patterns = patterns_db.get("patterns", [])

        if not patterns:
            return {
                "status": "no_data",
                "message": "No patterns found. System needs to execute tasks to generate learning data."
            }

        # Calculate all analytics
        learning_velocity = self.calculate_learning_velocity(patterns)
        skill_synergies = self.analyze_skill_synergies(patterns)
        learning_patterns = self.analyze_learning_patterns(patterns)

        # Overall statistics
        total_patterns = len(patterns)
        avg_quality = sum(p["outcome"]["quality_score"] for p in patterns) / total_patterns
        success_rate = sum(1 for p in patterns if p["outcome"]["success"]) / total_patterns

        # Recent vs historical performance
        recent_patterns = sorted(patterns, key=lambda p: p["timestamp"], reverse=True)[:20]
        recent_avg_quality = sum(p["outcome"]["quality_score"] for p in recent_patterns) / len(recent_patterns)
        recent_success_rate = sum(1 for p in recent_patterns if p["outcome"]["success"]) / len(recent_patterns)

        # Skill performance
        top_skills = sorted(
            [(name, metrics.get("success_rate", 0), metrics.get("avg_quality_contribution", 0))
             for name, metrics in skill_metrics.items()],
            key=lambda x: x[1] * x[2],  # Combined score
            reverse=True
        )[:10]

        # Agent performance
        top_agents = sorted(
            [(name, metrics.get("reliability_score", 0), metrics.get("efficiency_rating", 0))
             for name, metrics in agent_metrics.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # Prediction performance
        prediction_accuracy = predictions.get("prediction_accuracy", 0.0)
        models_trained = len(predictions.get("performance_models", {}).get("models", {}))

        # Cross-project learning
        universal_patterns_count = len(cross_project.get("universal_patterns", []))

        if universal_patterns_count > 0:
            avg_transferability = sum(
                p.get("effectiveness_metrics", {}).get("context_transferability", 0)
                for p in cross_project.get("universal_patterns", [])
            ) / universal_patterns_count
        else:
            avg_transferability = 0.0

        # Time-based trends
        patterns_last_7_days = [
            p for p in patterns
            if datetime.fromisoformat(p["timestamp"]) > datetime.now() - timedelta(days=7)
        ]
        patterns_last_30_days = [
            p for p in patterns
            if datetime.fromisoformat(p["timestamp"]) > datetime.now() - timedelta(days=30)
        ]

        # Generate quality trend chart data
        quality_over_time = [p["outcome"]["quality_score"] for p in sorted(patterns, key=lambda p: p["timestamp"])]

        return {
            "status": "success",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_patterns": total_patterns,
                "overall_quality": avg_quality,
                "overall_success_rate": success_rate,
                "recent_quality": recent_avg_quality,
                "recent_success_rate": recent_success_rate,
                "quality_improvement": recent_avg_quality - avg_quality,
                "patterns_last_7_days": len(patterns_last_7_days),
                "patterns_last_30_days": len(patterns_last_30_days)
            },
            "learning_velocity": learning_velocity,
            "skill_performance": {
                "total_skills": len(skill_metrics),
                "top_skills": [
                    {
                        "name": name,
                        "success_rate": rate,
                        "avg_quality": quality,
                        "composite_score": rate * quality
                    }
                    for name, rate, quality in top_skills
                ],
                "skill_metrics_available": len(skill_metrics) > 0
            },
            "agent_performance": {
                "total_agents": len(agent_metrics),
                "top_agents": [
                    {
                        "name": name,
                        "reliability": reliability,
                        "efficiency": efficiency
                    }
                    for name, reliability, efficiency in top_agents
                ],
                "agent_metrics_available": len(agent_metrics) > 0
            },
            "skill_synergies": {
                "total_synergies_found": len(skill_synergies),
                "top_synergies": skill_synergies[:5],
                "highly_recommended_count": sum(1 for s in skill_synergies if s["recommendation"] == "highly_recommended")
            },
            "prediction_system": {
                "prediction_accuracy": prediction_accuracy,
                "models_trained": models_trained,
                "status": "active" if models_trained > 0 else "inactive"
            },
            "cross_project_learning": {
                "universal_patterns": universal_patterns_count,
                "avg_transferability": avg_transferability,
                "status": "active" if universal_patterns_count > 0 else "inactive"
            },
            "learning_patterns": learning_patterns,
            "quality_trend": {
                "data": quality_over_time,
                "trend": "improving" if recent_avg_quality > avg_quality else "declining" if recent_avg_quality < avg_quality - 2 else "stable"
            },
            "insights": self._generate_comprehensive_insights(
                learning_velocity,
                skill_synergies,
                learning_patterns,
                avg_quality,
                recent_avg_quality,
                prediction_accuracy
            )
        }

    def _generate_comprehensive_insights(
        self,
        velocity: Dict,
        synergies: List[Dict],
        patterns: Dict,
        avg_quality: float,
        recent_quality: float,
        prediction_accuracy: float
    ) -> List[str]:
        """Generate comprehensive insights from all analytics."""
        insights = []

        # Learning velocity insights
        if velocity.get("status") == "calculated":
            if velocity["trajectory"] == "accelerating":
                insights.append(f"✓ Learning is accelerating! Quality improving at {velocity['improvement_per_week']:.2f} points/week and speeding up")
            elif velocity["improvement_per_week"] > 1.0:
                insights.append(f"✓ Steady improvement of {velocity['improvement_per_week']:.2f} quality points per week")
            elif velocity["improvement_per_week"] < 0:
                insights.append(f"⚠ Quality declining by {abs(velocity['improvement_per_week']):.2f} points/week - system may need recalibration")

        # Quality insights
        if recent_quality > avg_quality + 3:
            insights.append(f"✓ Recent performance ({recent_quality:.1f}) significantly better than historical average ({avg_quality:.1f})")
        elif recent_quality > 90:
            insights.append(f"✓ Excellent recent quality scores ({recent_quality:.1f}/100) - system is performing optimally")

        # Synergy insights
        if synergies:
            highly_recommended = [s for s in synergies if s["recommendation"] == "highly_recommended"]
            if highly_recommended:
                top_synergy = highly_recommended[0]
                insights.append(f"✓ Highly effective skill pair discovered: {' + '.join(top_synergy['skill_pair'])} ({top_synergy['synergy_score']:.1f} synergy score)")

        # Prediction system insights
        if prediction_accuracy > 0.85:
            insights.append(f"✓ Prediction system highly accurate ({prediction_accuracy:.1%}) - trust automated skill recommendations")
        elif prediction_accuracy > 0:
            insights.append(f"⚠ Prediction accuracy moderate ({prediction_accuracy:.1%}) - system still learning optimal patterns")

        # Learning patterns insights
        if patterns.get("learning_curves"):
            fastest = patterns.get("fastest_learning_areas", [])
            if fastest:
                insights.append(f"✓ Fastest learning in: {', '.join([area[0] for area in fastest[:2]])}")

        # Add custom insights from learning patterns
        if patterns.get("insights"):
            insights.extend(patterns["insights"])

        return insights

    def format_terminal_report(self, report: Dict[str, Any]) -> str:
        """Format report for terminal display with colors and charts."""
        if report.get("status") == "no_data":
            return "❌ No learning data available yet. Execute tasks to start learning."

        lines = []

        # Header
        lines.append("╔═══════════════════════════════════════════════════════════════════════════╗")
        lines.append("║           LEARNING ANALYTICS DASHBOARD - ENHANCED SYSTEM v3.0           ║")
        lines.append("╚═══════════════════════════════════════════════════════════════════════════╝")
        lines.append("")

        # Summary Section
        summary = report["summary"]
        lines.append("📊 OVERVIEW")
        lines.append("─" * 79)
        lines.append(f"  Total Patterns Captured: {summary['total_patterns']}")
        lines.append(f"  Overall Quality Score:   {summary['overall_quality']:.1f}/100")
        lines.append(f"  Success Rate:            {summary['overall_success_rate']:.1%}")
        lines.append(f"  Recent Quality:          {summary['recent_quality']:.1f}/100 ({'+' if summary['quality_improvement'] >= 0 else ''}{summary['quality_improvement']:.1f})")
        lines.append(f"  Activity (Last 7 days):  {summary['patterns_last_7_days']} patterns")
        lines.append(f"  Activity (Last 30 days): {summary['patterns_last_30_days']} patterns")
        lines.append("")

        # Quality Trend Chart
        if report["quality_trend"]["data"]:
            lines.append("📈 QUALITY TREND OVER TIME")
            lines.append("─" * 79)
            chart = self.generate_ascii_chart(
                report["quality_trend"]["data"],
                width=70,
                height=10,
                title=""
            )
            lines.append(chart)
            lines.append(f"  Trend: {report['quality_trend']['trend'].upper()}")
            lines.append("")

        # Learning Velocity
        velocity = report["learning_velocity"]
        if velocity.get("status") == "calculated":
            lines.append("🚀 LEARNING VELOCITY")
            lines.append("─" * 79)
            lines.append(f"  Weeks Analyzed:          {velocity['weeks_analyzed']}")
            lines.append(f"  Early Average Quality:   {velocity['early_average_quality']:.1f}/100")
            lines.append(f"  Recent Average Quality:  {velocity['recent_average_quality']:.1f}/100")
            lines.append(f"  Total Improvement:       {'+' if velocity['total_improvement'] >= 0 else ''}{velocity['total_improvement']:.1f} points")
            lines.append(f"  Improvement Rate:        {velocity['improvement_per_week']:.2f} points/week")
            lines.append(f"  Trajectory:              {velocity['trajectory'].upper()}")
            if velocity['trajectory'] == "accelerating":
                lines.append(f"  Acceleration:            +{velocity['acceleration']:.2f} (speeding up!)")
            lines.append("")

        # Top Skills
        skill_perf = report["skill_performance"]
        if skill_perf["top_skills"]:
            lines.append("⭐ TOP PERFORMING SKILLS")
            lines.append("─" * 79)
            for i, skill in enumerate(skill_perf["top_skills"][:5], 1):
                lines.append(f"  {i}. {skill['name']:<30} Success: {skill['success_rate']:.1%}  Quality: {skill['avg_quality']:.1f}")
            lines.append("")

        # Top Agents
        agent_perf = report["agent_performance"]
        if agent_perf["top_agents"]:
            lines.append("🤖 TOP PERFORMING AGENTS")
            lines.append("─" * 79)
            for i, agent in enumerate(agent_perf["top_agents"], 1):
                lines.append(f"  {i}. {agent['name']:<30} Reliability: {agent['reliability']:.1%}  Efficiency: {agent['efficiency']:.2f}")
            lines.append("")

        # Skill Synergies
        synergies = report["skill_synergies"]
        if synergies["top_synergies"]:
            lines.append("🔗 SKILL SYNERGIES (Top Combinations)")
            lines.append("─" * 79)
            for i, synergy in enumerate(synergies["top_synergies"], 1):
                pair = " + ".join(synergy["skill_pair"])
                lines.append(f"  {i}. {pair:<40} Score: {synergy['synergy_score']:.1f}  Uses: {synergy['usage_count']}")
                lines.append(f"     Quality: {synergy['average_quality']:.1f}  Success: {synergy['success_rate']:.1%}  [{synergy['recommendation'].upper()}]")
            lines.append("")

        # Prediction System
        pred = report["prediction_system"]
        lines.append("🎯 PREDICTION SYSTEM STATUS")
        lines.append("─" * 79)
        lines.append(f"  Status:                  {pred['status'].upper()}")
        lines.append(f"  Models Trained:          {pred['models_trained']} skills")
        lines.append(f"  Prediction Accuracy:     {pred['prediction_accuracy']:.1%}")
        if pred["prediction_accuracy"] > 0.85:
            lines.append("  ✓ High accuracy - automated recommendations highly reliable")
        elif pred["prediction_accuracy"] > 0.7:
            lines.append("  ⚠ Moderate accuracy - system still learning")
        lines.append("")

        # Cross-Project Learning
        cross = report["cross_project_learning"]
        lines.append("🌐 CROSS-PROJECT LEARNING")
        lines.append("─" * 79)
        lines.append(f"  Status:                  {cross['status'].upper()}")
        lines.append(f"  Universal Patterns:      {cross['universal_patterns']}")
        lines.append(f"  Avg Transferability:     {cross['avg_transferability']:.1%}")
        if cross["universal_patterns"] > 0:
            lines.append("  ✓ Knowledge transfer active - benefiting from other projects")
        lines.append("")

        # Learning Patterns
        learn = report["learning_patterns"]
        if learn.get("fastest_learning_areas"):
            lines.append("📚 LEARNING PATTERNS")
            lines.append("─" * 79)
            lines.append("  Fastest Learning Areas:")
            for task, rate in learn["fastest_learning_areas"]:
                lines.append(f"    • {task:<30} +{rate:.2f} quality/task")
            lines.append("")

        # Key Insights
        insights = report["insights"]
        if insights:
            lines.append("💡 KEY INSIGHTS")
            lines.append("─" * 79)
            for insight in insights[:10]:  # Show top 10 insights
                lines.append(f"  {insight}")
            lines.append("")

        # Footer
        lines.append("╔═══════════════════════════════════════════════════════════════════════════╗")
        lines.append(f"║  Generated: {report['generated_at']:<62} ║")
        lines.append("╚═══════════════════════════════════════════════════════════════════════════╝")

        return "\n".join(lines)

    def export_json_report(self, output_file: str):
        """Export full analytics report as JSON."""
        report = self.generate_comprehensive_report()

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return output_path

    def export_markdown_report(self, output_file: str):
        """Export analytics report as Markdown."""
        report = self.generate_comprehensive_report()

        if report.get("status") == "no_data":
            content = "# Learning Analytics Report\n\nNo data available yet."
        else:
            content = self._format_markdown_report(report)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return output_path

    def _format_markdown_report(self, report: Dict[str, Any]) -> str:
        """Format report as Markdown."""
        lines = []

        lines.append("# Learning Analytics Report")
        lines.append(f"\n**Generated**: {report['generated_at']}")
        lines.append("\n---\n")

        # Summary
        summary = report["summary"]
        lines.append("## 📊 Overview\n")
        lines.append(f"- **Total Patterns**: {summary['total_patterns']}")
        lines.append(f"- **Overall Quality**: {summary['overall_quality']:.1f}/100")
        lines.append(f"- **Success Rate**: {summary['overall_success_rate']:.1%}")
        lines.append(f"- **Recent Quality**: {summary['recent_quality']:.1f}/100 ({'+' if summary['quality_improvement'] >= 0 else ''}{summary['quality_improvement']:.1f})")
        lines.append(f"- **Activity (7 days)**: {summary['patterns_last_7_days']} patterns")
        lines.append(f"- **Activity (30 days)**: {summary['patterns_last_30_days']} patterns")
        lines.append("")

        # Learning Velocity
        velocity = report["learning_velocity"]
        if velocity.get("status") == "calculated":
            lines.append("## 🚀 Learning Velocity\n")
            lines.append(f"- **Improvement Rate**: {velocity['improvement_per_week']:.2f} points/week")
            lines.append(f"- **Trajectory**: {velocity['trajectory'].capitalize()}")
            lines.append(f"- **Total Improvement**: {'+' if velocity['total_improvement'] >= 0 else ''}{velocity['total_improvement']:.1f} points")
            lines.append("")

        # Top Skills
        skill_perf = report["skill_performance"]
        if skill_perf["top_skills"]:
            lines.append("## ⭐ Top Performing Skills\n")
            lines.append("| Rank | Skill | Success Rate | Avg Quality |")
            lines.append("|------|-------|--------------|-------------|")
            for i, skill in enumerate(skill_perf["top_skills"][:5], 1):
                lines.append(f"| {i} | {skill['name']} | {skill['success_rate']:.1%} | {skill['avg_quality']:.1f} |")
            lines.append("")

        # Skill Synergies
        synergies = report["skill_synergies"]
        if synergies["top_synergies"]:
            lines.append("## 🔗 Skill Synergies\n")
            lines.append("| Rank | Skill Combination | Synergy Score | Uses | Quality | Success Rate |")
            lines.append("|------|-------------------|---------------|------|---------|--------------|")
            for i, synergy in enumerate(synergies["top_synergies"][:5], 1):
                pair = " + ".join(synergy["skill_pair"])
                lines.append(f"| {i} | {pair} | {synergy['synergy_score']:.1f} | {synergy['usage_count']} | {synergy['average_quality']:.1f} | {synergy['success_rate']:.1%} |")
            lines.append("")

        # Insights
        insights = report["insights"]
        if insights:
            lines.append("## 💡 Key Insights\n")
            for insight in insights:
                lines.append(f"- {insight}")
            lines.append("")

        return "\n".join(lines)


def main():
    """Command-line interface for learning analytics."""
    parser = argparse.ArgumentParser(description='Learning Analytics Dashboard')
    parser.add_argument('--dir', default='.claude-patterns', help='Patterns directory path')

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Terminal report
    subparsers.add_parser('show', help='Show analytics in terminal')

    # Export JSON
    json_parser = subparsers.add_parser('export-json', help='Export analytics as JSON')
    json_parser.add_argument('--output', default='learning_analytics.json', help='Output file path')

    # Export Markdown
    md_parser = subparsers.add_parser('export-md', help='Export analytics as Markdown')
    md_parser.add_argument('--output', default='learning_analytics.md', help='Output file path')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    dashboard = LearningAnalyticsDashboard(args.dir)

    try:
        if args.action == 'show':
            report = dashboard.generate_comprehensive_report()
            formatted = dashboard.format_terminal_report(report)
            print(formatted)

        elif args.action == 'export-json':
            output_path = dashboard.export_json_report(args.output)
            print(f"✓ JSON report exported to: {output_path}")

        elif args.action == 'export-md':
            output_path = dashboard.export_markdown_report(args.output)
            print(f"✓ Markdown report exported to: {output_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
