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

Version: 1.0.0
Author: Autonomous Agent Development Team
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import threading
import time
from collections import defaultdict
import statistics


app = Flask(__name__)
CORS(app)  # Enable CORS for API access


class DashboardDataCollector:
    """Collects and aggregates data for dashboard visualization."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """
        Initialize data collector.

        Args:
            patterns_dir: Directory containing pattern data
        """
        self.patterns_dir = Path(patterns_dir)
        self.cache = {}
        self.cache_ttl = 60  # Cache for 60 seconds
        self.last_update = {}

    def _load_json_file(self, filename: str, cache_key: str) -> Dict[str, Any]:
        """Load JSON file with caching."""
        filepath = self.patterns_dir / filename

        # Check cache
        if cache_key in self.cache:
            if time.time() - self.last_update.get(cache_key, 0) < self.cache_ttl:
                return self.cache[cache_key]

        # Load from file
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    self.cache[cache_key] = data
                    self.last_update[cache_key] = time.time()
                    return data
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                return {}

        return {}

    def get_overview_metrics(self) -> Dict[str, Any]:
        """Get high-level overview metrics."""
        patterns = self._load_json_file("patterns.json", "patterns")

        total_patterns = len(patterns.get("patterns", []))
        total_skills = len(patterns.get("skill_effectiveness", {}))
        total_agents = len(patterns.get("agent_effectiveness", {}))

        # Calculate average quality score
        quality_scores = [
            p.get("outcome", {}).get("quality_score", 0)
            for p in patterns.get("patterns", [])
            if p.get("outcome", {}).get("quality_score") is not None
        ]
        avg_quality = statistics.mean(quality_scores) if quality_scores else 0

        # Calculate learning velocity from quality history (preferred)
        quality_history = self._load_json_file("quality_history.json", "quality")
        learning_velocity = self._calculate_learning_velocity_from_quality(quality_history)

        # Fallback to pattern-based calculation if quality history is insufficient
        if learning_velocity == "insufficient_data":
            recent_patterns = patterns.get("patterns", [])[-20:] if patterns.get("patterns") else []
            learning_velocity = self._calculate_learning_velocity(recent_patterns)

        return {
            "total_patterns": total_patterns,
            "total_skills": total_skills,
            "total_agents": total_agents,
            "average_quality_score": round(avg_quality, 1),
            "learning_velocity": learning_velocity,
            "last_updated": datetime.now().isoformat()
        }

    def _calculate_learning_velocity(self, patterns: List[Dict]) -> str:
        """Calculate learning velocity (accelerating/stable/declining)."""
        if len(patterns) < 3:
            return "insufficient_data"

        # Split into halves
        mid = len(patterns) // 2
        first_half = patterns[:mid]
        second_half = patterns[mid:]

        # Calculate average quality scores
        first_avg = statistics.mean([
            p.get("outcome", {}).get("quality_score", 0)
            for p in first_half
            if p.get("outcome", {}).get("quality_score") is not None
        ]) if first_half else 0

        second_avg = statistics.mean([
            p.get("outcome", {}).get("quality_score", 0)
            for p in second_half
            if p.get("outcome", {}).get("quality_score") is not None
        ]) if second_half else 0

        improvement = second_avg - first_avg

        if improvement > 5:
            return "accelerating"
        elif improvement > -5:
            return "stable"
        else:
            return "declining"

    def _calculate_learning_velocity_from_quality(self, quality_history: Dict) -> str:
        """Calculate learning velocity from quality assessments."""
        assessments = quality_history.get("quality_assessments", [])

        if len(assessments) < 3:
            return "insufficient_data"

        # Sort assessments by timestamp
        assessments.sort(key=lambda x: x.get("timestamp", ""))

        # Split into halves
        mid = len(assessments) // 2
        first_half = assessments[:mid]
        second_half = assessments[mid:]

        # Calculate average quality scores
        first_avg = statistics.mean([
            a.get("overall_score", 0)
            for a in first_half
            if a.get("overall_score") is not None
        ]) if first_half else 0

        second_avg = statistics.mean([
            a.get("overall_score", 0)
            for a in second_half
            if a.get("overall_score") is not None
        ]) if second_half else 0

        improvement = second_avg - first_avg

        # Calculate velocity based on improvement rate
        if improvement > 3:
            return "accelerating 🚀"
        elif improvement > 0:
            return "improving 📈"
        elif improvement > -3:
            return "stable 📊"
        else:
            return "declining 📉"

    def get_quality_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get quality score trends over time with exact timestamps."""
        quality_history = self._load_json_file("quality_history.json", "quality")

        # Get individual assessments with exact timestamps
        trend_data = []
        cutoff_date = datetime.now() - timedelta(days=days)

        for assessment in quality_history.get("quality_assessments", []):
            timestamp = assessment.get("timestamp")
            quality_score = assessment.get("overall_score")
            task_type = assessment.get("task_type", "unknown")

            if timestamp and quality_score is not None:
                try:
                    # Parse timestamp and remove timezone for comparison
                    assessment_date = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).replace(tzinfo=None)
                    if assessment_date >= cutoff_date:
                        # Format timestamp for display
                        display_time = assessment_date.strftime("%m/%d %H:%M")
                        trend_data.append({
                            "timestamp": timestamp,
                            "display_time": display_time,
                            "score": quality_score,
                            "task_type": task_type
                        })
                except:
                    continue

        # Sort by timestamp
        trend_data.sort(key=lambda x: x["timestamp"])

        return {
            "trend_data": trend_data,
            "overall_average": round(statistics.mean([
                d["score"] for d in trend_data
            ]), 1) if trend_data else 0,
            "days": days
        }

    def get_skill_performance(self, top_k: int = 10) -> Dict[str, Any]:
        """Get top performing skills."""
        patterns = self._load_json_file("patterns.json", "patterns")

        skills_data = []
        for skill_name, metrics in patterns.get("skill_effectiveness", {}).items():
            success_rate = metrics.get("success_rate", 0) or 0
            usage_count = metrics.get("total_uses", 0) or 0
            avg_quality = metrics.get("avg_quality_impact", 0)

            skills_data.append({
                "name": skill_name,
                "success_rate": round(success_rate * 100, 1),
                "usage_count": usage_count,
                "avg_quality_impact": round(avg_quality, 1),
                "recommended_for": metrics.get("recommended_for", [])
            })

        # Sort by success rate
        skills_data.sort(key=lambda x: x["success_rate"], reverse=True)

        return {
            "top_skills": skills_data[:top_k],
            "total_skills": len(skills_data)
        }

    def get_agent_performance(self, top_k: int = 10) -> Dict[str, Any]:
        """Get top performing agents."""
        patterns = self._load_json_file("patterns.json", "patterns")

        agents_data = []
        for agent_name, metrics in patterns.get("agent_effectiveness", {}).items():
            success_rate = metrics.get("success_rate", 0) or 0
            usage_count = metrics.get("total_uses", 0) or 0
            avg_duration = metrics.get("avg_duration", 0)
            reliability = metrics.get("reliability_score", 0)

            agents_data.append({
                "name": agent_name,
                "success_rate": round(success_rate * 100, 1),
                "usage_count": usage_count,
                "avg_duration": round(avg_duration, 1),
                "reliability": round(reliability * 100, 1)
            })

        # Sort by reliability
        agents_data.sort(key=lambda x: x["reliability"], reverse=True)

        return {
            "top_agents": agents_data[:top_k],
            "total_agents": len(agents_data)
        }

    def get_task_distribution(self) -> Dict[str, Any]:
        """Get distribution of task types."""
        patterns = self._load_json_file("patterns.json", "patterns")

        task_counts = defaultdict(int)
        success_by_task = defaultdict(list)

        for pattern in patterns.get("patterns", []):
            task_type = pattern.get("task_type", "unknown")
            task_counts[task_type] += 1

            success = pattern.get("outcome", {}).get("success", False)
            success_by_task[task_type].append(1 if success else 0)

        distribution = []
        for task_type, count in task_counts.items():
            success_rate = statistics.mean(success_by_task[task_type]) if success_by_task[task_type] else 0

            distribution.append({
                "task_type": task_type,
                "count": count,
                "success_rate": round(success_rate * 100, 1)
            })

        # Sort by count
        distribution.sort(key=lambda x: x["count"], reverse=True)

        return {
            "distribution": distribution,
            "total_tasks": sum(task_counts.values())
        }

    def get_recent_activity(self, limit: int = 20) -> Dict[str, Any]:
        """Get recent task activity."""
        patterns = self._load_json_file("patterns.json", "patterns")

        recent = patterns.get("patterns", [])[-limit:]
        recent.reverse()  # Most recent first

        activity = []
        for pattern in recent:
            activity.append({
                "timestamp": pattern.get("timestamp", ""),
                "task_type": pattern.get("task_type", "unknown"),
                "quality_score": pattern.get("outcome", {}).get("quality_score"),
                "success": pattern.get("outcome", {}).get("success", False),
                "skills_used": pattern.get("execution", {}).get("skills_used", []),
                "duration": pattern.get("execution", {}).get("duration", 0)
            })

        return {
            "recent_activity": activity,
            "count": len(activity)
        }

    def get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics."""
        patterns = self._load_json_file("patterns.json", "patterns")

        # Calculate error rate (last 50 tasks)
        recent_tasks = patterns.get("patterns", [])[-50:]
        error_count = sum(1 for p in recent_tasks if not p.get("outcome", {}).get("success", False))
        error_rate = (error_count / len(recent_tasks) * 100) if recent_tasks else 0

        # Calculate average quality (last 50 tasks)
        quality_scores = [
            p.get("outcome", {}).get("quality_score", 0)
            for p in recent_tasks
            if p.get("outcome", {}).get("quality_score") is not None
        ]
        avg_quality = statistics.mean(quality_scores) if quality_scores else 0

        # Storage size
        patterns_size = os.path.getsize(self.patterns_dir / "patterns.json") if (self.patterns_dir / "patterns.json").exists() else 0

        health_status = "excellent"
        if error_rate > 20 or avg_quality < 60:
            health_status = "degraded"
        elif error_rate > 10 or avg_quality < 70:
            health_status = "warning"

        return {
            "status": health_status,
            "error_rate": round(error_rate, 1),
            "avg_quality": round(avg_quality, 1),
            "patterns_stored": len(patterns.get("patterns", [])),
            "storage_size_kb": round(patterns_size / 1024, 1)
        }


# Initialize data collector
data_collector = DashboardDataCollector()


# HTML Template for Dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autonomous Agent Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }

        .metric-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }

        .metric-trend {
            font-size: 0.8em;
            color: #28a745;
            margin-top: 5px;
        }

        .metric-trend.negative {
            color: #dc3545;
        }

        .chart-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .chart-title {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }

        .table-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 600;
        }

        .badge-success {
            background: #28a745;
            color: white;
        }

        .badge-warning {
            background: #ffc107;
            color: #333;
        }

        .badge-danger {
            background: #dc3545;
            color: white;
        }

        .badge-info {
            background: #17a2b8;
            color: white;
        }

        .health-status {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .health-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        .health-indicator.excellent {
            background: #28a745;
        }

        .health-indicator.warning {
            background: #ffc107;
        }

        .health-indicator.degraded {
            background: #dc3545;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .refresh-info {
            text-align: center;
            color: white;
            margin-top: 20px;
            font-size: 0.9em;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: white;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Autonomous Agent Dashboard</h1>

        <div id="loading" class="loading">Loading dashboard data...</div>

        <div id="dashboard" style="display: none;">
            <!-- Overview Metrics -->
            <div class="metrics-grid" id="overview-metrics"></div>

            <!-- Quality Trends Chart -->
            <div class="chart-container">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <div class="chart-title">Quality Score Trends</div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <label for="quality-period" style="font-size: 14px; color: #666;">Period:</label>
                        <select id="quality-period" style="padding: 5px 10px; border-radius: 5px; border: 1px solid #ddd; background: white; font-size: 14px;">
                            <option value="1">Last 24 Hours</option>
                            <option value="7">Last 7 Days</option>
                            <option value="30" selected>Last 30 Days</option>
                            <option value="90">Last 90 Days</option>
                            <option value="365">Last Year</option>
                            <option value="all">All Time</option>
                        </select>
                    </div>
                </div>
                <div id="quality-debug" style="background: rgba(0,0,0,0.1); padding: 10px; border-radius: 5px; margin-bottom: 10px; font-size: 12px; color: #666;"></div>
                <canvas id="qualityChart"></canvas>
            </div>

            <!-- Two Column Layout -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                <!-- Task Distribution -->
                <div class="chart-container">
                    <div class="chart-title">Task Distribution</div>
                    <canvas id="taskChart"></canvas>
                </div>

                <!-- System Health -->
                <div class="table-container">
                    <div class="chart-title">System Health</div>
                    <div id="system-health"></div>
                </div>
            </div>

            <!-- Top Skills Table -->
            <div class="table-container">
                <div class="chart-title">Top Performing Skills</div>
                <table id="skills-table">
                    <thead>
                        <tr>
                            <th>Skill</th>
                            <th>Success Rate</th>
                            <th>Usage Count</th>
                            <th>Avg Quality Impact</th>
                        </tr>
                    </thead>
                    <tbody id="skills-tbody"></tbody>
                </table>
            </div>

            <!-- Top Agents Table -->
            <div class="table-container">
                <div class="chart-title">Top Performing Agents</div>
                <table id="agents-table">
                    <thead>
                        <tr>
                            <th>Agent</th>
                            <th>Success Rate</th>
                            <th>Usage Count</th>
                            <th>Avg Duration (s)</th>
                            <th>Reliability</th>
                        </tr>
                    </thead>
                    <tbody id="agents-tbody"></tbody>
                </table>
            </div>

            <!-- Recent Activity -->
            <div class="table-container">
                <div class="chart-title">Recent Activity</div>
                <table id="activity-table">
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Task Type</th>
                            <th>Quality Score</th>
                            <th>Status</th>
                            <th>Skills Used</th>
                        </tr>
                    </thead>
                    <tbody id="activity-tbody"></tbody>
                </table>
            </div>

            <div class="refresh-info">
                Dashboard auto-refreshes every 30 seconds • Last updated: <span id="last-update"></span>
            </div>
        </div>
    </div>

    <script>
        let qualityChart = null;
        let taskChart = null;

        async function fetchQualityData(days = 30) {
            try {
                const response = await fetch(`/api/quality-trends?days=${days}`);
                const quality = await response.json();
                updateQualityChart(quality);
            } catch (error) {
                console.error('Error fetching quality data:', error);
            }
        }

        async function fetchDashboardData() {
            try {
                const [overview, quality, skills, agents, tasks, activity, health] = await Promise.all([
                    fetch('/api/overview').then(r => r.json()),
                    fetch('/api/quality-trends').then(r => r.json()),
                    fetch('/api/skills').then(r => r.json()),
                    fetch('/api/agents').then(r => r.json()),
                    fetch('/api/task-distribution').then(r => r.json()),
                    fetch('/api/recent-activity').then(r => r.json()),
                    fetch('/api/system-health').then(r => r.json())
                ]);

                updateOverviewMetrics(overview);
                updateQualityChart(quality);
                updateTaskChart(tasks);
                updateSkillsTable(skills);
                updateAgentsTable(agents);
                updateActivityTable(activity);
                updateSystemHealth(health);

                document.getElementById('loading').style.display = 'none';
                document.getElementById('dashboard').style.display = 'block';
                document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
                document.getElementById('loading').textContent = 'Error loading dashboard data. Retrying...';
            }
        }

        function updateOverviewMetrics(data) {
            const container = document.getElementById('overview-metrics');
            const velocityBadge = {
                'accelerating 🚀': '🚀 Accelerating',
                'improving 📈': '📈 Improving',
                'stable 📊': '📊 Stable',
                'declining 📉': '📉 Declining',
                'accelerating': '📈 Accelerating',
                'stable': '➡️ Stable',
                'declining': '📉 Declining',
                'insufficient_data': '⏳ Learning'
            }[data.learning_velocity];

            container.innerHTML = `
                <div class="metric-card">
                    <div class="metric-label">Total Patterns</div>
                    <div class="metric-value">${data.total_patterns}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Active Skills</div>
                    <div class="metric-value">${data.total_skills}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Active Agents</div>
                    <div class="metric-value">${data.total_agents}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Avg Quality Score</div>
                    <div class="metric-value">${data.average_quality_score}/100</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Learning Velocity</div>
                    <div class="metric-value" style="font-size: 1.5em;">${velocityBadge}</div>
                </div>
            `;
        }

        function updateQualityChart(data) {
            const debugDiv = document.getElementById('quality-debug');

            if (!data || !data.trend_data || data.trend_data.length === 0) {
                debugDiv.innerHTML = '❌ No quality trend data available';
                return;
            }

            const periodText = data.days === 1 ? '24 Hours' :
                        data.days === 7 ? '7 Days' :
                        data.days === 30 ? '30 Days' :
                        data.days === 90 ? '90 Days' :
                        data.days === 365 ? 'Year' :
                        data.days >= 3650 ? 'All Time' : `${data.days} Days`;

            const latestPoint = data.trend_data[data.trend_data.length - 1];
            debugDiv.innerHTML = `✅ Quality data (${periodText}): ${data.trend_data.length} assessments | Overall avg: ${data.overall_average} | Latest: ${latestPoint.score} (${latestPoint.display_time})`;

            const ctx = document.getElementById('qualityChart').getContext('2d');

            if (qualityChart) {
                qualityChart.destroy();
            }

            // Use bar chart for single data point, line chart for multiple
            const chartType = data.trend_data.length === 1 ? 'bar' : 'line';

            qualityChart = new Chart(ctx, {
                type: chartType,
                data: {
                    labels: data.trend_data.map(d => d.display_time),
                    datasets: [{
                        label: 'Quality Score',
                        data: data.trend_data.map(d => d.score),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        function updateTaskChart(data) {
            const ctx = document.getElementById('taskChart').getContext('2d');

            if (taskChart) {
                taskChart.destroy();
            }

            const colors = [
                '#667eea', '#764ba2', '#f093fb', '#4facfe',
                '#43e97b', '#fa709a', '#fee140', '#30cfd0'
            ];

            taskChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.distribution.map(d => d.task_type),
                    datasets: [{
                        data: data.distribution.map(d => d.count),
                        backgroundColor: colors
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right'
                        }
                    }
                }
            });
        }

        function updateSkillsTable(data) {
            const tbody = document.getElementById('skills-tbody');
            tbody.innerHTML = data.top_skills.map(skill => `
                <tr>
                    <td><strong>${skill.name}</strong></td>
                    <td><span class="badge badge-success">${skill.success_rate}%</span></td>
                    <td>${skill.usage_count}</td>
                    <td>${skill.avg_quality_impact}</td>
                </tr>
            `).join('');
        }

        function updateAgentsTable(data) {
            const tbody = document.getElementById('agents-tbody');
            tbody.innerHTML = data.top_agents.map(agent => `
                <tr>
                    <td><strong>${agent.name}</strong></td>
                    <td><span class="badge badge-success">${agent.success_rate}%</span></td>
                    <td>${agent.usage_count}</td>
                    <td>${agent.avg_duration}s</td>
                    <td><span class="badge badge-info">${agent.reliability}%</span></td>
                </tr>
            `).join('');
        }

        function updateActivityTable(data) {
            const tbody = document.getElementById('activity-tbody');
            tbody.innerHTML = data.recent_activity.map(activity => {
                const statusBadge = activity.success
                    ? '<span class="badge badge-success">✓ Success</span>'
                    : '<span class="badge badge-danger">✗ Failed</span>';

                const timestamp = new Date(activity.timestamp).toLocaleString();
                const skills = activity.skills_used.slice(0, 3).join(', ');

                return `
                    <tr>
                        <td>${timestamp}</td>
                        <td>${activity.task_type}</td>
                        <td><strong>${activity.quality_score || 'N/A'}</strong></td>
                        <td>${statusBadge}</td>
                        <td style="font-size: 0.85em;">${skills}</td>
                    </tr>
                `;
            }).join('');
        }

        function updateSystemHealth(data) {
            const container = document.getElementById('system-health');
            const statusClass = data.status;
            const statusLabel = {
                'excellent': 'Excellent',
                'warning': 'Warning',
                'degraded': 'Degraded'
            }[data.status];

            container.innerHTML = `
                <div class="health-status">
                    <div class="health-indicator ${statusClass}"></div>
                    <strong>Status: ${statusLabel}</strong>
                </div>
                <table style="margin-top: 15px;">
                    <tr>
                        <td><strong>Error Rate</strong></td>
                        <td>${data.error_rate}%</td>
                    </tr>
                    <tr>
                        <td><strong>Avg Quality</strong></td>
                        <td>${data.avg_quality}/100</td>
                    </tr>
                    <tr>
                        <td><strong>Patterns Stored</strong></td>
                        <td>${data.patterns_stored}</td>
                    </tr>
                    <tr>
                        <td><strong>Storage Size</strong></td>
                        <td>${data.storage_size_kb} KB</td>
                    </tr>
                </table>
            `;
        }

        // Add event listener for quality period selector
        document.getElementById('quality-period').addEventListener('change', function(e) {
            const period = e.target.value;
            if (period === 'all') {
                // Fetch all data by using a very large number
                fetchQualityData(3650); // 10 years
            } else {
                fetchQualityData(parseInt(period));
            }
        });

        // Initial load
        fetchDashboardData();

        // Auto-refresh every 30 seconds
        setInterval(fetchDashboardData, 30000);
    </script>
</body>
</html>
"""


# API Routes
@app.route('/')
def index():
    """Render dashboard homepage."""
    return render_template_string(DASHBOARD_HTML)


@app.route('/api/overview')
def api_overview():
    """Get overview metrics."""
    return jsonify(data_collector.get_overview_metrics())


@app.route('/api/quality-trends')
def api_quality_trends():
    """Get quality trends."""
    days = request.args.get('days', 30, type=int)
    return jsonify(data_collector.get_quality_trends(days))


@app.route('/api/skills')
def api_skills():
    """Get skill performance."""
    top_k = request.args.get('top_k', 10, type=int)
    return jsonify(data_collector.get_skill_performance(top_k))


@app.route('/api/agents')
def api_agents():
    """Get agent performance."""
    top_k = request.args.get('top_k', 10, type=int)
    return jsonify(data_collector.get_agent_performance(top_k))


@app.route('/api/task-distribution')
def api_task_distribution():
    """Get task distribution."""
    return jsonify(data_collector.get_task_distribution())


@app.route('/api/recent-activity')
def api_recent_activity():
    """Get recent activity."""
    limit = request.args.get('limit', 20, type=int)
    return jsonify(data_collector.get_recent_activity(limit))


@app.route('/api/system-health')
def api_system_health():
    """Get system health."""
    return jsonify(data_collector.get_system_health())


def run_dashboard(host: str = '127.0.0.1', port: int = 5000, patterns_dir: str = ".claude-patterns"):
    """
    Run the dashboard server.

    Args:
        host: Host to bind to
        port: Port to bind to
        patterns_dir: Directory containing pattern data
    """
    global data_collector
    data_collector = DashboardDataCollector(patterns_dir)

    print(f"Starting Autonomous Agent Dashboard...")
    print(f"Dashboard URL: http://{host}:{port}")
    print(f"Pattern directory: {patterns_dir}")
    print(f"\nPress Ctrl+C to stop the server")

    app.run(host=host, port=port, debug=False)


def main():
    """CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description="Autonomous Agent Dashboard")
    parser.add_argument('--host', default='127.0.0.1', help="Host to bind to")
    parser.add_argument('--port', type=int, default=5000, help="Port to bind to")
    parser.add_argument('--patterns-dir', default='.claude-patterns', help="Pattern directory")

    args = parser.parse_args()

    run_dashboard(args.host, args.port, args.patterns_dir)


if __name__ == '__main__':
    main()
