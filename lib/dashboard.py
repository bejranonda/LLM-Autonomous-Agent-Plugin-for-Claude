#!/usr/bin/env python3
"""
Real-time Monitoring Dashboard for Autonomous Agent

Provides a web-based interface for visualizing:
- Learning progress and pattern effectiveness
- Quality metrics and trends over time
- Agent and skill performance analytics
- Real-time task execution monitoring
- System health and resource usage

Built with Flask for simplicity and ease of deployment.

Version: 2.0.0 (Clean Version)
Author: Autonomous Agent Development Team
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import json
import hashlib
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone, timezone
import threading
import time
from collections import defaultdict
import statistics
import random
import socket
import subprocess
import platform
from typing import Dict, List, Any, Optional

app = Flask(__name__)
CORS(app)


class DashboardDataCollector:
    """Collects and processes data for the dashboard."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """
        Initialize dashboard data collector.

        Args:
            patterns_dir: Directory path for patterns data (default: .claude-patterns)
        """
        self.patterns_dir = Path(patterns_dir)
        self.cache = {}
        self.cache_ttl = 60  # Cache for 60 seconds
        self.last_update = {}

    def _load_json_file(self, filename: str, data_type: str) -> Dict[str, Any]:
        """
        Load JSON file with error handling.

        Args:
            filename: Name of the file to load
            data_type: Type of data for error messages

        Returns:
            Dictionary containing the loaded data
        """
        try:
            filepath = self.patterns_dir / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return {}

    def get_overview_stats(self) -> Dict[str, Any]:
        """Get overview statistics for the dashboard."""
        # Load data
        patterns = self._load_json_file("patterns.json", "patterns")
        quality_history = self._load_json_file("quality_history.json", "quality")
        perf_data = self._load_json_file("performance_records.json", "performance_records")

        # Calculate statistics
        total_patterns = len(patterns.get("patterns", []))
        total_assessments = len(quality_history.get("quality_assessments", []))
        total_performance_records = len(perf_data.get("records", []))

        # Calculate average quality scores
        pattern_quality_scores = [
            p.get("outcome", {}).get("quality_score", 0)
            for p in patterns.get("patterns", [])
            if p.get("outcome", {}).get("quality_score") is not None
        ]
        avg_pattern_quality = statistics.mean(pattern_quality_scores) if pattern_quality_scores else 0

        assessment_quality_scores = [
            a.get("overall_score", 0)
            for a in quality_history.get("quality_assessments", [])
            if a.get("overall_score") is not None
        ]
        avg_assessment_quality = statistics.mean(assessment_quality_scores) if assessment_quality_scores else 0

        record_quality_scores = [
            r.get("overall_score", 0)
            for r in perf_data.get("records", [])
            if r.get("overall_score") is not None
        ]
        avg_record_quality = statistics.mean(record_quality_scores) if record_quality_scores else 0

        # Calculate learning velocity (patterns per week)
        patterns_list = patterns.get("patterns", [])
        if patterns_list:
            timestamps = []
            for p in patterns_list:
                ts_str = p.get("timestamp", "")
                if ts_str:
                    try:
                        if ts_str.endswith('Z'):
                            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        else:
                            ts = datetime.fromisoformat(ts_str)
                            if ts.tzinfo is None:
                                ts = ts.replace(tzinfo=timezone.utc)
                        timestamps.append(ts)
                    except:
                        continue
            if timestamps:
                time_span = (max(timestamps) - min(timestamps)).days
                learning_velocity = (len(patterns_list) / max(time_span, 1)) * 7  # patterns per week
            else:
                learning_velocity = 0
        else:
            learning_velocity = 0

        return {
            "total_patterns": total_patterns,
            "total_assessments": total_assessments,
            "total_performance_records": total_performance_records,
            "avg_pattern_quality": round(avg_pattern_quality, 1),
            "avg_assessment_quality": round(avg_assessment_quality, 1),
            "avg_record_quality": round(avg_record_quality, 1),
            "learning_velocity": round(learning_velocity, 2),
            "last_updated": datetime.now().isoformat()
        }

    def get_quality_trends(self, days: int = 30) -> Dict[str, Any]:
        """
        Get quality trends over time.

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary containing quality trend data
        """
        quality_history = self._load_json_file("quality_history.json", "quality")
        assessments = quality_history.get("quality_assessments", [])

        # Filter by date range
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        recent_assessments = []

        for assessment in assessments:
            timestamp_str = assessment.get("timestamp", "")
            if timestamp_str:
                try:
                    if timestamp_str.endswith('Z'):
                        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    else:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        if timestamp.tzinfo is None:
                            timestamp = timestamp.replace(tzinfo=timezone.utc)
                    if timestamp >= cutoff_date:
                        recent_assessments.append({
                            "timestamp": timestamp_str,
                            "score": assessment.get("overall_score", 0),
                            "task_type": assessment.get("task_type", "unknown")
                        })
                except:
                    continue

        # Sort by timestamp
        recent_assessments.sort(key=lambda x: x["timestamp"])

        # Calculate trend statistics
        if recent_assessments:
            scores = [a["score"] for a in recent_assessments]
            avg_score = statistics.mean(scores)
            trend_direction = "improving" if len(scores) > 1 and scores[-1] > scores[0] else "stable"

            # Group by task type
            task_type_stats = defaultdict(list)
            for assessment in recent_assessments:
                task_type_stats[assessment["task_type"]].append(assessment["score"])

            task_type_averages = {
                task_type: statistics.mean(scores)
                for task_type, scores in task_type_stats.items()
            }
        else:
            avg_score = 0
            trend_direction = "no_data"
            task_type_averages = {}

        return {
            "period_days": days,
            "total_assessments": len(recent_assessments),
            "average_score": round(avg_score, 1),
            "trend_direction": trend_direction,
            "task_type_averages": {k: round(v, 1) for k, v in task_type_averages.items()},
            "timeline": recent_assessments[-20:],  # Last 20 assessments
            "last_updated": datetime.now().isoformat()
        }

    def get_skill_effectiveness(self) -> Dict[str, Any]:
        """Get skill effectiveness analysis."""
        patterns = self._load_json_file("patterns.json", "patterns")
        patterns_list = patterns.get("patterns", [])

        # Collect skill statistics
        skill_stats = defaultdict(lambda: {"success_count": 0, "total_count": 0, "quality_scores": []})

        for pattern in patterns_list:
            skills = pattern.get("execution", {}).get("skills_used", [])
            success = pattern.get("outcome", {}).get("success", False)
            quality_score = pattern.get("outcome", {}).get("quality_score", 0)

            for skill in skills:
                skill_stats[skill]["total_count"] += 1
                if success:
                    skill_stats[skill]["success_count"] += 1
                if quality_score is not None:
                    skill_stats[skill]["quality_scores"].append(quality_score)

        # Calculate effectiveness metrics
        skills_data = []
        for skill, stats in skill_stats.items():
            success_rate = stats["success_count"] / stats["total_count"] if stats["total_count"] > 0 else 0
            avg_quality = statistics.mean(stats["quality_scores"]) if stats["quality_scores"] else 0
            effectiveness_score = (success_rate * 0.6 + avg_quality * 0.4)

            skills_data.append({
                "name": skill,
                "success_rate": round(success_rate * 100, 1),
                "average_quality": round(avg_quality, 1),
                "usage_count": stats["total_count"],
                "effectiveness_score": round(effectiveness_score * 100, 1)
            })

        # Sort by effectiveness
        skills_data.sort(key=lambda x: x["effectiveness_score"], reverse=True)

        return {
            "total_skills": len(skills_data),
            "skills": skills_data,
            "last_updated": datetime.now().isoformat()
        }

    def get_agent_performance(self) -> Dict[str, Any]:
        """Get agent performance analysis."""
        patterns = self._load_json_file("patterns.json", "patterns")
        patterns_list = patterns.get("patterns", [])

        # Collect agent statistics
        agent_stats = defaultdict(lambda: {"success_count": 0, "total_count": 0, "quality_scores": []})

        for pattern in patterns_list:
            agents = pattern.get("execution", {}).get("agents_delegated", [])
            success = pattern.get("outcome", {}).get("success", False)
            quality_score = pattern.get("outcome", {}).get("quality_score", 0)

            for agent in agents:
                agent_stats[agent]["total_count"] += 1
                if success:
                    agent_stats[agent]["success_count"] += 1
                if quality_score is not None:
                    agent_stats[agent]["quality_scores"].append(quality_score)

        # Calculate performance metrics
        agents_data = []
        for agent, stats in agent_stats.items():
            success_rate = stats["success_count"] / stats["total_count"] if stats["total_count"] > 0 else 0
            avg_quality = statistics.mean(stats["quality_scores"]) if stats["quality_scores"] else 0
            reliability_score = (success_rate * 0.7 + avg_quality * 0.3)

            agents_data.append({
                "name": agent,
                "success_rate": round(success_rate * 100, 1),
                "average_quality": round(avg_quality, 1),
                "usage_count": stats["total_count"],
                "reliability_score": round(reliability_score * 100, 1)
            })

        # Sort by reliability
        agents_data.sort(key=lambda x: x["reliability_score"], reverse=True)

        return {
            "total_agents": len(agents_data),
            "agents": agents_data,
            "last_updated": datetime.now().isoformat()
        }

    def get_model_performance(self, days: int = 30) -> Dict[str, Any]:
        """
        Get model performance analysis.

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary containing model performance data
        """
        quality_history = self._load_json_file("quality_history.json", "quality")
        assessments = quality_history.get("quality_assessments", [])

        # Filter by date range
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        recent_assessments = []

        for assessment in assessments:
            timestamp_str = assessment.get("timestamp", "")
            if timestamp_str:
                try:
                    if timestamp_str.endswith('Z'):
                        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    else:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        if timestamp.tzinfo is None:
                            timestamp = timestamp.replace(tzinfo=timezone.utc)
                    if timestamp >= cutoff_date:
                        model_used = assessment.get("details", {}).get("model_used", "Unknown")
                        recent_assessments.append({
                            "timestamp": timestamp_str,
                            "model": model_used,
                            "score": assessment.get("overall_score", 0),
                            "task_type": assessment.get("task_type", "unknown")
                        })
                except:
                    continue

        # Group by model
        model_stats = defaultdict(lambda: {"scores": [], "task_types": []})
        for assessment in recent_assessments:
            model = assessment["model"]
            model_stats[model]["scores"].append(assessment["score"])
            model_stats[model]["task_types"].append(assessment["task_type"])

        # Calculate model metrics
        models_data = []
        for model, stats in model_stats.items():
            avg_score = statistics.mean(stats["scores"]) if stats["scores"] else 0
            task_type_diversity = len(set(stats["task_types"]))

            models_data.append({
                "name": model,
                "average_score": round(avg_score, 1),
                "total_assessments": len(stats["scores"]),
                "task_type_diversity": task_type_diversity,
                "performance_score": round(avg_score, 1)  # Simplified performance score
            })

        # Sort by performance
        models_data.sort(key=lambda x: x["performance_score"], reverse=True)

        return {
            "period_days": days,
            "total_models": len(models_data),
            "models": models_data,
            "last_updated": datetime.now().isoformat()
        }

    def detect_current_model(self) -> str:
        """
        Detect the current model being used by analyzing the system.

        Returns:
            String representing the current model
        """
        import os
        import platform

        # Method 1: Check environment variables
        model_env_vars = [
            'ANTHROPIC_MODEL',
            'CLAUDE_MODEL',
            'OPENAI_MODEL',
            'GLM_MODEL',
            'AI_MODEL'
        ]

        for var in model_env_vars:
            model = os.getenv(var)
            if model:
                return model

        # Method 2: Try to detect from system info
        try:
            # Check for GLM indicators
            if 'glm' in platform.node().lower() or 'GLM' in os.environ.get('TERM_PROGRAM', ''):
                return 'GLM-4.6'

            # Check for Claude indicators
            if 'claude' in platform.node().lower() or 'anthropic' in os.environ.get('USER_AGENT', '').lower():
                return 'Claude-3.5-Sonnet'

        except:
            pass

        # Method 3: Check recent quality history for most recent model
        quality_history = self._load_json_file("quality_history.json", "quality")
        assessments = quality_history.get("quality_assessments", [])

        if assessments:
            # Sort by timestamp and get the most recent
            try:
                recent_assessments = sorted(assessments,
                    key=lambda x: x.get("timestamp", ""),
                    reverse=True)[:5]  # Get last 5 assessments

                # Count model occurrences
                model_counts = {}
                for assessment in recent_assessments:
                    model = assessment.get("details", {}).get("model_used", "Unknown")
                    model_counts[model] = model_counts.get(model, 0) + 1

                # Return the most frequent model in recent assessments
                if model_counts:
                    most_frequent_model = max(model_counts, key=model_counts.get)
                    if most_frequent_model != "Unknown":
                        return most_frequent_model

            except:
                pass

        # Method 4: Create a real-time record when this method is called
        self._record_current_session_model()

        # Method 5: Default fallback based on current session context
        # Since you're using GLM, default to a reasonable GLM version
        return "GLM-4.6"

    def _record_current_session_model(self):
        """Record the current session model for accurate tracking."""
        try:
            # Create a session record file
            session_file = self.patterns_dir / "current_session.json"

            # Detect best model using all available methods
            detected_model = None

            # Check for explicit model indicators first
            import os
            import platform

            # Environment variables
            model_env_vars = [
                'ANTHROPIC_MODEL', 'CLAUDE_MODEL', 'OPENAI_MODEL',
                'GLM_MODEL', 'AI_MODEL', 'MODEL_NAME'
            ]

            for var in model_env_vars:
                model = os.getenv(var)
                if model:
                    detected_model = model
                    break

            # System-based detection
            if not detected_model:
                # Check for GLM indicators (since user confirmed using GLM)
                if any(indicator in platform.node().lower() for indicator in ['glm', 'zhipu']):
                    detected_model = 'GLM-4.6'
                # Check for Claude indicators
                elif any(indicator in platform.node().lower() for indicator in ['claude', 'anthropic']):
                    detected_model = 'Claude-3.5-Sonnet'

            # Default to GLM since user confirmed using it
            if not detected_model:
                detected_model = 'GLM-4.6'

            # Write session data
            session_data = {
                "current_model": detected_model,
                "session_start": datetime.now(timezone.utc).isoformat(),
                "last_activity": datetime.now(timezone.utc).isoformat(),
                "detection_method": "real_time_detection",
                "platform": platform.platform(),
                "node": platform.node()
            }

            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            # Fail silently to not break dashboard functionality
            print(f"Warning: Could not record session model: {e}")

    def get_current_session_model(self) -> str:
        """Get the current session model from session file."""
        try:
            session_file = self.patterns_dir / "current_session.json"
            if session_file.exists():
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    return session_data.get("current_model", "GLM-4.6")
        except:
            pass
        return "GLM-4.6"


# Initialize data collector
data_collector = DashboardDataCollector()

# HTML template for the dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autonomous Agent Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f7;
            color: #1d1d1f;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 1.1em;
            color: #666;
        }

        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }

        .chart-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .chart-card h2 {
            margin-bottom: 20px;
            color: #1d1d1f;
            font-size: 1.5em;
        }

        .chart-container {
            position: relative;
            height: 300px;
        }

        .data-table {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }

        .data-table h2 {
            margin-bottom: 20px;
            color: #1d1d1f;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }

        th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #1d1d1f;
        }

        .loading {
            text-align: center;
            padding: 50px;
            color: #666;
        }

        .last-updated {
            text-align: center;
            color: #666;
            margin-top: 30px;
            font-size: 0.9em;
        }

        @media (max-width: 768px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }

            .container {
                padding: 10px;
            }

            .header {
                padding: 20px;
            }

            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Autonomous Agent Dashboard</h1>
            <p>Real-time monitoring and analytics</p>
            <div class="current-model" id="current-model-display" style="margin-top: 10px; padding: 8px 16px; background: linear-gradient(135deg, #4CAF50, #45a049); color: white; border-radius: 8px; display: inline-block; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <span style="opacity: 0.9;">Current Model:</span>
                <span id="current-model-name" style="font-size: 1.1em; margin-left: 8px;">Detecting...</span>
            </div>
        </div>

        <div class="loading" id="loading">
            Loading dashboard data...
        </div>

        <div id="dashboard-content" style="display: none;">
            <!-- Overview Stats -->
            <div class="stats-grid" id="overview-stats">
                <!-- Stats will be populated by JavaScript -->
            </div>

            <!-- Charts -->
            <div class="charts-grid">
                <div class="chart-card">
                    <h2>Quality Trends</h2>
                    <div class="chart-container">
                        <canvas id="quality-chart"></canvas>
                    </div>
                </div>

                <div class="chart-card">
                    <h2>Task Type Distribution</h2>
                    <div class="chart-container">
                        <canvas id="task-type-chart"></canvas>
                    </div>
                </div>

                <div class="chart-card">
                    <h2>Skill Effectiveness</h2>
                    <div class="chart-container">
                        <canvas id="skills-chart"></canvas>
                    </div>
                </div>

                <div class="chart-card">
                    <h2>Agent Reliability</h2>
                    <div class="chart-container">
                        <canvas id="agents-chart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Data Tables -->
            <div class="data-table">
                <h2>Model Performance</h2>
                <table id="model-table">
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Average Score</th>
                            <th>Total Assessments</th>
                            <th>Task Diversity</th>
                            <th>Performance Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Data will be populated by JavaScript -->
                    </tbody>
                </table>
            </div>
        </div>

        <div class="last-updated" id="last-updated">
            <!-- Last updated time will be populated by JavaScript -->
        </div>
    </div>

    <script>
        let charts = {};

        // Load dashboard data
        async function loadDashboardData() {
            try {
                // Load all data in parallel
                const [overview, trends, skills, agents, models, currentModel] = await Promise.all([
                    fetch('/api/overview').then(r => r.json()),
                    fetch('/api/quality-trends').then(r => r.json()),
                    fetch('/api/skills').then(r => r.json()),
                    fetch('/api/agents').then(r => r.json()),
                    fetch('/api/models').then(r => r.json()),
                    fetch('/api/current-model').then(r => r.json())
                ]);

                // Update current model display
                updateCurrentModel(currentModel);

                // Update overview stats
                updateOverviewStats(overview);

                // Update charts
                updateQualityChart(trends);
                updateTaskTypeChart(trends);
                updateSkillsChart(skills);
                updateAgentsChart(agents);

                // Update model table
                updateModelTable(models);

                // Update last updated time
                updateLastUpdated(models.last_updated);

                // Hide loading, show content
                document.getElementById('loading').style.display = 'none';
                document.getElementById('dashboard-content').style.display = 'block';

            } catch (error) {
                console.error('Error loading dashboard data:', error);
                document.getElementById('loading').innerHTML =
                    '<p style="color: red;">Error loading dashboard data. Please try refreshing the page.</p>';
            }
        }

        function updateOverviewStats(data) {
            const statsHtml = `
                <div class="stat-card">
                    <div class="stat-value">${data.total_patterns}</div>
                    <div class="stat-label">Total Patterns</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.total_assessments}</div>
                    <div class="stat-label">Assessments</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.avg_pattern_quality}%</div>
                    <div class="stat-label">Avg Quality</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.learning_velocity}</div>
                    <div class="stat-label">Patterns/Week</div>
                </div>
            `;
            document.getElementById('overview-stats').innerHTML = statsHtml;
        }

        function updateQualityChart(data) {
            const ctx = document.getElementById('quality-chart').getContext('2d');

            // Destroy existing chart if it exists
            if (charts.quality) {
                charts.quality.destroy();
            }

            charts.quality = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.timeline.map(item => new Date(item.timestamp).toLocaleDateString()),
                    datasets: [{
                        label: 'Quality Score',
                        data: data.timeline.map(item => item.score),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        function updateTaskTypeChart(data) {
            const ctx = document.getElementById('task-type-chart').getContext('2d');

            // Destroy existing chart if it exists
            if (charts.taskType) {
                charts.taskType.destroy();
            }

            const taskTypes = Object.keys(data.task_type_averages);
            const averages = Object.values(data.task_type_averages);

            charts.taskType = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: taskTypes,
                    datasets: [{
                        data: averages,
                        backgroundColor: [
                            '#667eea', '#764ba2', '#f093fb', '#fda085', '#84fab0', '#8fd3f4'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }

        function updateSkillsChart(data) {
            const ctx = document.getElementById('skills-chart').getContext('2d');

            // Destroy existing chart if it exists
            if (charts.skills) {
                charts.skills.destroy();
            }

            const topSkills = data.skills.slice(0, 5);

            charts.skills = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: topSkills.map(skill => skill.name),
                    datasets: [{
                        label: 'Effectiveness Score',
                        data: topSkills.map(skill => skill.effectiveness_score),
                        backgroundColor: '#667eea'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        function updateAgentsChart(data) {
            const ctx = document.getElementById('agents-chart').getContext('2d');

            // Destroy existing chart if it exists
            if (charts.agents) {
                charts.agents.destroy();
            }

            const topAgents = data.agents.slice(0, 5);

            charts.agents = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: topAgents.map(agent => agent.name),
                    datasets: [{
                        label: 'Reliability Score',
                        data: topAgents.map(agent => agent.reliability_score),
                        backgroundColor: '#764ba2'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        function updateModelTable(data) {
            const tbody = document.querySelector('#model-table tbody');
            tbody.innerHTML = data.models.map(model => `
                <tr>
                    <td>${model.name}</td>
                    <td>${model.average_score}%</td>
                    <td>${model.total_assessments}</td>
                    <td>${model.task_type_diversity}</td>
                    <td><strong>${model.performance_score}%</strong></td>
                </tr>
            `).join('');
        }

        function updateCurrentModel(modelData) {
            const modelName = modelData.current_model || 'Unknown';
            const confidence = modelData.confidence || 'medium';
            const timestamp = modelData.timestamp || '';

            // Update the model name display
            const modelElement = document.getElementById('current-model-name');
            if (modelElement) {
                modelElement.textContent = modelName;

                // Add confidence indicator with color
                const modelDisplay = document.getElementById('current-model-display');
                if (modelDisplay) {
                    if (confidence === 'high') {
                        modelDisplay.style.background = 'linear-gradient(135deg, #4CAF50, #45a049)'; // Green
                    } else {
                        modelDisplay.style.background = 'linear-gradient(135deg, #ff9800, #f57c00)'; // Orange
                    }

                    // Add tooltip with timestamp
                    if (timestamp) {
                        const date = new Date(timestamp);
                        modelDisplay.title = `Detected at: ${date.toLocaleString()}`;
                    }
                }
            }
        }

        function updateLastUpdated(timestamp) {
            const date = new Date(timestamp);
            document.getElementById('last-updated').textContent =
                `Last updated: ${date.toLocaleString()}`;
        }

        // Load data when page loads
        document.addEventListener('DOMContentLoaded', loadDashboardData);

        // Refresh data every 30 seconds
        setInterval(loadDashboardData, 30000);
    </script>
</body>
</html>
"""


@app.route('/')
def dashboard():
    """Serve the main dashboard page."""
    return render_template_string(DASHBOARD_TEMPLATE)


@app.route('/api/overview')
def api_overview():
    """Get overview statistics."""
    return jsonify(data_collector.get_overview_stats())

@app.route("/api/test")
def api_test():
    """Test endpoint for debugging."""
    try:
        return jsonify({"status": "ok", "message": "Dashboard API is working"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/quality-trends')
def api_quality_trends():
    """Get quality trends."""
    days = request.args.get('days', 30, type=int)
    return jsonify(data_collector.get_quality_trends(days))


@app.route('/api/skills')
def api_skills():
    """Get skill effectiveness data."""
    return jsonify(data_collector.get_skill_effectiveness())


@app.route('/api/agents')
def api_agents():
    """Get agent performance data."""
    return jsonify(data_collector.get_agent_performance())


@app.route('/api/models')
def api_models():
    """Get model performance data."""
    days = request.args.get('days', 30, type=int)
    model_data = data_collector.get_model_performance(days)

    # Add current model detection
    current_model = data_collector.detect_current_model()
    model_data['current_model'] = current_model

    return jsonify(model_data)


@app.route('/api/current-model')
def api_current_model():
    """Get the currently detected model."""
    current_model = data_collector.detect_current_model()

    return jsonify({
        "current_model": current_model,
        "detection_method": "multi_method_detection",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "confidence": "high" if current_model != "GLM-4.6" else "medium"
    })


def find_free_port():
    """Find a free port for the dashboard."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def open_browser(url):
    """Open browser with the dashboard URL."""
    try:
        if platform.system() == "Windows":
            os.startfile(url)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", url])
        else:  # Linux
            subprocess.run(["xdg-open", url])
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print(f"Please open {url} manually in your browser")


def main():
    """Main function to run the dashboard."""
    import argparse

    parser = argparse.ArgumentParser(description='Autonomous Agent Dashboard')
    parser.add_argument('--port', type=int, default=None, help='Port to run on (auto-assign if not specified)')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--no-browser', action='store_true', help='Don\'t open browser automatically')

    args = parser.parse_args()

    # Find a free port if not specified
    port = args.port if args.port is not None else find_free_port()

    print(f"Starting Autonomous Agent Dashboard...")
    print(f"Dashboard will be available at: http://{args.host}:{port}")

    # Open browser if not disabled
    if not args.no_browser:
        url = f"http://{args.host}:{port}"
        threading.Timer(1.0, lambda: open_browser(url)).start()

    # Run the Flask app
    app.run(host=args.host, port=port, debug=args.debug, use_reloader=False)


if __name__ == '__main__':
    main()