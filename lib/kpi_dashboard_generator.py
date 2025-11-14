"""
#    KPI Dashboard Generator for Token Optimization Framework
"""
Creates interactive HTML dashboards with comprehensive KPI visualization
"""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from unified_metrics_aggregator import UnifiedMetricsAggregator, MetricPeriod, KpiCategory


class KPIDashboardGenerator:
    """Generates interactive HTML KPI dashboards"""

    def __init__(self, aggregator: UnifiedMetricsAggregator = None):
        """Initialize the processor with default configuration."""
        self.aggregator = aggregator or UnifiedMetricsAggregator()
        self.logger = logging.getLogger(__name__)

    def generate_kpi_dashboard(
        self, output_file: str = "kpi_dashboard.html", period: MetricPeriod = MetricPeriod.DAILY
    )-> str:
        """Generate Kpi Dashboard."""Generate comprehensive KPI dashboard"""

        # Get dashboard data
        dashboard_data = self.aggregator.get_kpi_dashboard_data(period)

        # Generate HTML
        html_content = self._create_html_template(dashboard_data, period)

        # Save to file
        output_path = Path(output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        self.logger.info(f"KPI Dashboard saved to: {output_path.absolute()}")
        return str(output_path.absolute())

    def _create_html_template(self, data: Dict[str, Any], period: MetricPeriod) -> str:
        """Create the HTML template for the dashboard"""

        current_scores = data["current_scores"]
        summary = data["summary"]
        snapshot = data["system_snapshot"]

        # Generate KPI cards HTML
        kpi_cards_html = self._generate_kpi_cards(current_scores["individual_kpis"])

        # Generate trends HTML
        trends_html = self._generate_trends_section(data["historical_trends"])

        # Generate recommendations HTML
        recommendations_html = self._generate_recommendations_section(snapshot["recommendations"])

        # Generate actions HTML
        actions_html = self._generate_actions_section(snapshot["next_actions"])

        # Generate system health HTML
        system_health_html = self._generate_system_health_section(snapshot["system_health"])

        # JavaScript data
        js_data = json.dumps(data, default=str)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token Optimization KPI Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
            animation: fadeInDown 0.8s ease;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .summary-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: fadeInUp 0.8s ease backwards;
        }}

        .summary-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .summary-card:nth-child(2) {{ animation-delay: 0.2s; }}
        .summary-card:nth-child(3) {{ animation-delay: 0.3s; }}
        .summary-card:nth-child(4) {{ animation-delay: 0.4s; }}

        .summary-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}

        .summary-card h3 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1em;
        }}

        .summary-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .summary-card .label {{
            color: #666;
            font-size: 0.9em;
        }}

        .section {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: fadeInUp 0.8s ease backwards;
        }}

        .section:nth-child(odd) {{ animation-delay: 0.2s; }}
        .section:nth-child(even) {{ animation-delay: 0.4s; }}

        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}

        .kpi-card {{
            border: 2px solid #f0f0f0;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }}

        .kpi-card:hover {{
            border-color: #667eea;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }}

        .kpi-card.critical {{
            border-color: #e74c3c;
            background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
        }}

        .kpi-card.poor {{
            border-color: #f39c12;
            background: linear-gradient(135deg, #fff 0%, #fffbf0 100%);
        }}

        .kpi-card.good {{
            border-color: #27ae60;
            background: linear-gradient(135deg, #fff 0%, #f0fff4 100%);
        }}

        .kpi-card.excellent {{
            border-color: #2ecc71;
            background: linear-gradient(135deg, #fff 0%, #f0fff4 100%);
        }}

        .kpi-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .kpi-title {{
            font-weight: bold;
            color: #333;
            font-size: 1.1em;
        }}

        .kpi-status {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}

        .status-excellent {{
            background: #2ecc71;
            color: white;
        }}

        .status-good {{
            background: #3498db;
            color: white;
        }}

        .status-fair {{
            background: #f39c12;
            color: white;
        }}

        .status-poor {{
            background: #e67e22;
            color: white;
        }}

        .status-critical {{
            background: #e74c3c;
            color: white;
        }}

        .kpi-metrics {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 15px;
        }}

        .kpi-metric {{
            text-align: center;
        }}

        .kpi-metric .value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}

        .kpi-metric .label {{
            font-size: 0.8em;
            color: #666;
        }}

        .kpi-progress {{
            margin-top: 10px;
        }}

        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #f0f0f0;
            border-radius: 4px;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s ease;
        }}

        .progress-excellent {{ background: #2ecc71; }}
        .progress-good {{ background: #3498db; }}
        .progress-fair {{ background: #f39c12; }}
        .progress-poor {{ background: #e67e22; }}
        .progress-critical {{ background: #e74c3c; }}

        .chart-container {{
            position: relative;
            height: 400px;
            margin-top: 20px;
        }}

        .recommendations-list, .actions-list {{
            list-style: none;
        }}

        .recommendations-list li, .actions-list li {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            transition: transform 0.2s ease;
        }}

        .recommendations-list li:hover, .actions-list li:hover {{
            transform: translateX(5px);
        }}

        .action-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .action-details {{
            flex: 1;
        }}

        .action-meta {{
            display: flex;
            gap: 15px;
            align-items: center;
        }}

        .priority-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}

        .priority-high {{
            background: #e74c3c;
            color: white;
        }}

        .priority-medium {{
            background: #f39c12;
            color: white;
        }}

        .priority-low {{
            background: #27ae60;
            color: white;
        }}

        .effort-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            background: #ecf0f1;
            color: #333;
        }}

        .system-health-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}

        .health-metric {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}

        .health-metric .value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}

        .health-metric .label {{
            color: #666;
            margin-top: 5px;
        }}

        .trend-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
        }}

        .trend-improving {{
            background: #d4edda;
            color: #155724;
        }}

        .trend-stable {{
            background: #d1ecf1;
            color: #0c5460;
        }}

        .trend-declining {{
            background: #f8d7da;
            color: #721c24;
        }}

        .last-updated {{
            text-align: center;
            color: white;
            opacity: 0.8;
            margin-top: 20px;
        }}

        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}

            .header h1 {{
                font-size: 2em;
            }}

            .summary-cards {{
                grid-template-columns: 1fr;
            }}

            .kpi-grid {{
                grid-template-columns: 1fr;
            }}

            .action-item {{
                flex-direction: column;
                align-items: flex-start;
            }}

            .action-meta {{
                width: 100%;
                justify-content: space-between;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Token Optimization KPI Dashboard</h1>
            <div class="subtitle">Performance Metrics & Insights • {period.value.title()} View</div>
        </div>

        <div class="summary-cards">
            <div class="summary-card">
                <h3>Overall Score</h3>
                <div class="value" style="color: {self._get_score_color(summary['overall_score'])}">{summary['overall_score']:.1f}</div>
                <div class="label">out of 100</div>
            </div>
            <div class="summary-card">
                <h3>Critical Issues</h3>
                <div class="value" style="color: {'#e74c3c' if summary['critical_issues'] > 0 else '#27ae60'}">{summary['critical_issues']}</div>
                <div class="label">need attention</div>
            </div>
            <div class="summary-card">
                <h3>Improving Trends</h3>
                <div class="value" style="color: #27ae60">{summary['improving_trends']}</div>
                <div class="label">KPIs improving</div>
            </div>
            <div class="summary-card">
                <h3>Active Actions</h3>
                <div class="value" style="color: #667eea">{summary['total_actions']}</div>
                <div class="label">recommended</div>
            </div>
        </div>

        {system_health_html}

        <div class="section">
            <h2>Key Performance Indicators</h2>
            {kpi_cards_html}
        </div>

        <div class="section">
            <h2>Performance Trends</h2>
            {trends_html}
        </div>

        <div class="section">
            <h2>Recommendations</h2>
            {recommendations_html}
        </div>

        <div class="section">
            <h2>Action Items</h2>
            {actions_html}
        </div>

        <div class="last-updated">
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>

    <script>
        // Dashboard data
        const dashboardData = {js_data};

        // Initialize charts when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {{
            initializeTrendCharts();
            startAutoRefresh();
        }});

        function initializeTrendCharts() {{
            const historicalData = dashboardData.historical_trends;

            Object.keys(historicalData).forEach(kpiName => {{
                const data = historicalData[kpiName];
                if (data.length > 1) {{
                    createTrendChart(kpiName, data);
                }}
            }});
        }}

        function createTrendChart(kpiName, data) {{
            const ctx = document.getElementById(`chart-${{kpiName}}`);
            if (!ctx) return;

            const labels = data.map(d => new Date(d.timestamp).toLocaleDateString());
            const values = data.map(d => d.value);
            const achievementRates = data.map(d => d.achievement_rate);

            new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: kpiName.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase()),
                        data: values,
                        borderColor: 'rgb(102, 126, 234)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4,
                        fill: true
                    }}, {{
                        label: 'Achievement Rate %',
                        data: achievementRates,
                        borderColor: 'rgb(46, 204, 113)',
                        backgroundColor: 'rgba(46, 204, 113, 0.1)',
                        tension: 0.4,
                        fill: true,
                        yAxisID: 'y1'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{
                        mode: 'index',
                        intersect: false
                    }},
                    plugins: {{
                        legend: {{
                            position: 'top'
                        }}
                    }},
                    scales: {{
                        y: {{
                            type: 'linear',
                            display: true,
                            position: 'left'
                        }},
                        y1: {{
                            type: 'linear',
                            display: true,
                            position: 'right',
                            grid: {{
                                drawOnChartArea: false
                            }}
                        }}
                    }}
                }}
            }});
        }}

        function startAutoRefresh() {{
            // Auto-refresh every 30 seconds
            setInterval(function() {{
                location.reload();
            }}, 30000);
        }}

        function animateValue(element, start, end, duration) {{
            const range = end - start;
            const increment = range / (duration / 16);
            let current = start;

            const timer = setInterval(function() {{
                current += increment;
                if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {{
                    element.textContent = end.toFixed(1);
                    clearInterval(timer);
                }} else {{
                    element.textContent = current.toFixed(1);
                }}
            }}, 16);
        }}

        // Animate values on page load
        window.addEventListener('load', function() {{
            const values = document.querySelectorAll('.kpi-metric .value, .summary-card .value');
            values.forEach(element => {{
                const text = element.textContent;
                const match = text.match(/([\\d.]+)/);
                if (match) {{
                    const value = parseFloat(match[1]);
                    animateValue(element, 0, value, 1000);
                }}
            }});
        }});
    </script>
</body>
</html>"""

        return html

    def _get_score_color(self, score: float) -> str:
        """Get color based on score"""
        if score >= 90:
            return "#27ae60"
        elif score >= 80:
            return "#3498db"
        elif score >= 70:
            return "#f39c12"
        elif score >= 60:
            return "#e67e22"
        else:
            return "#e74c3c"

    def _generate_kpi_cards(self, individual_kpis: Dict[str, Any]) -> str:
        """Generate KPI cards HTML"""
        html = '<div class="kpi-grid">'

        for kpi_name, kpi_data in individual_kpis.items():
            status = kpi_data.get("status", "unknown")
            achievement_rate = kpi_data.get("achievement_rate", 0)
            trend = kpi_data.get("trend", "unknown")

            html += f"""
            <div class="kpi-card {status}">
                <div class="kpi-header">
                    <div class="kpi-title">{kpi_name.replace('_', ' ').title()}</div>
                    <div class="kpi-status status-{status}">{status}</div>
                </div>

                <div class="kpi-metrics">
                    <div class="kpi-metric">
                        <div class="value">{kpi_data['current_value']:.2f}</div>
                        <div class="label">Current ({kpi_data['unit']})</div>
                    </div>
                    <div class="kpi-metric">
                        <div class="value">{kpi_data['target_value']:.2f}</div>
                        <div class="label">Target ({kpi_data['unit']})</div>
                    </div>
                </div>

                <div class="kpi-progress">
                    <div class="progress-bar">
                        <div class="progress-fill progress-{status}" style="width: {min(achievement_rate, 150)}%"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.8em;">
                        <span>Achievement: {achievement_rate:.1f}%</span>
                        <span class="trend-indicator trend-{trend}">
                            {trend.replace('_', ' ').title()}
                        </span>
                    </div>
                </div>
            </div>
"""

        html += "</div>"
        return html

"""
    def _generate_trends_section(self, historical_trends: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate trends section with charts"""
        html = '<div class="trend-charts">'

        for kpi_name, data in historical_trends.items():
            if len(data) > 1:  # Only show chart if we have multiple data points
                html += f"""
                <div style="margin-bottom: 30px;">
                    <h3>{kpi_name.replace('_', ' ').title()} Trend</h3>
                    <div class="chart-container">
                        <canvas id="chart-{kpi_name}"></canvas>
                    </div>
                </div>
"""

        if not html:
            html = "<p>No historical data available for trend analysis.</p>"

        return html

"""
    def _generate_recommendations_section(self, recommendations: List[str]) -> str:
        """Generate recommendations section"""
        if not recommendations:
            return '<p style="text-align: center; color: #27ae60; font-weight: bold;">[OK] All systems performing well!</p>'

        html = '<ul class="recommendations-list">'
        for rec in recommendations:
            html += f"<li>{rec}</li>"
        html += "</ul>"

        return html

    def _generate_actions_section(self, actions: List[Dict[str, Any]]) -> str:
        """Generate actions section"""
        if not actions:
            return '<p style="text-align: center; color: #666;">No immediate actions required.</p>'

        html = '<ul class="actions-list">'
        for action in actions:
            html += f"""
            <li>
                <div class="action-item">
                    <div class="action-details">
                        <strong>{action['action']}</strong>
                        <div style="color: #666; margin-top: 5px;">
                            Expected Impact: {action['expected_impact']} • Timeline: {action['timeline']}
                        </div>
                    </div>
                    <div class="action-meta">
                        <span class="priority-badge priority-{action['priority']}">{action['priority']}</span>
                        <span class="effort-badge">{action['effort']} effort</span>
                    </div>
                </div>
            </li>
"""
        html += "</ul>"

        return html

"""
    def _generate_system_health_section(self, system_health: Dict[str, Any]) -> str:
        """Generate system health section"""
        html = """
        <div class="section">
            <h2>System Health Overview</h2>
            <div class="system-health-grid">
"""

        health_metrics = [
            ("Overall Score", system_health.get("overall_score", 0), "score"),
            ("Critical Issues", system_health.get("critical_issues", 0), "issues"),
            ("Improving Trends", system_health.get("improving_trends", 0), "trends"),
            ("Declining Trends", system_health.get("declining_trends", 0), "trends"),
        ]

        for label, value, _type in health_metrics:
            color = self._get_score_color(value) if _type == "score" else "#667eea"
            if _type == "issues" and value > 0:
                color = "#e74c3c"

            html += f"""
            <div class="health-metric">
                <div class="value" style="color: {color}">{value}</div>
                <div class="label">{label}</div>
            </div>
"""

        html += "</div></div>"
        return html

"""
    def generate_executive_summary_report(self, output_file: str = "executive_summary.html") -> str:
        """Generate executive summary report"""
        dashboard_data = self.aggregator.get_kpi_dashboard_data()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token Optimization Executive Summary</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .content {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
        .metric {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .section {{
            margin: 30px 0;
        }}
        .highlight {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            margin: 15px 0;
        }}
        @media (max-width: 600px) {{
            .metric-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Token Optimization Executive Summary</h1>
        <p>Performance Overview & Business Impact</p>
    </div>

    <div class="content">
        <div class="metric-grid">
            <div class="metric">
                <div class="metric-value">{dashboard_data['summary']['overall_score']:.1f}</div>
                <div>Overall Performance Score</div>
            </div>
            <div class="metric">
                <div class="metric-value">{dashboard_data['current_scores']['individual_kpis'].get('token_reduction_rate', {}).get('current_value', 0):.1f}%</div>
                <div>Token Reduction Rate</div>
            </div>
            <div class="metric">
                <div class="metric-value">${dashboard_data['system_snapshot']['metrics'].get('aggregated', {}).get('total_cost_savings', 0):.2f}</div>
                <div>Total Cost Savings</div>
            </div>
            <div class="metric">
                <div class="metric-value">{dashboard_data['current_scores']['individual_kpis'].get('cache_hit_rate', {}).get('current_value', 0):.1f}%</div>
                <div>Cache Hit Rate</div>
            </div>
        </div>

        <div class="section">
            <h2>Key Achievements</h2>
            <div class="highlight">
                <strong>Token Optimization:</strong> Achieved {dashboard_data['current_scores']['individual_kpis'].get('token_reduction_rate', {}).get('current_value', 0):.1f}% token reduction, exceeding target of 60%.
            </div>
            <div class="highlight">
                <strong>Cost Efficiency:</strong> Generated ${dashboard_data['system_snapshot']['metrics'].get('aggregated', {}).get('total_cost_savings', 0):.2f} in cost savings through intelligent optimization.
            </div>
            <div class="highlight">
                <strong>System Performance:</strong> Maintained {dashboard_data['current_scores']['individual_kpis'].get('cache_hit_rate', {}).get('current_value', 0):.1f}% cache hit rate, ensuring fast response times.
            </div>
        </div>

        <div class="section">
            <h2>Strategic Recommendations</h2>
            <ul>
                {"".join([f"<li>{rec}</li>" for rec in dashboard_data['system_snapshot']['recommendations'][:3]])}
            </ul>
        </div>

        <div class="section">
            <h2>Business Impact</h2>
            <p>The token optimization framework has delivered significant business value through:</p>
            <ul>
                <li>Reduced operational costs by ${dashboard_data['system_snapshot']['metrics'].get('aggregated', {}).get('total_cost_savings', 0):.2f}</li>
                <li>Improved system efficiency with {dashboard_data['current_scores']['individual_kpis'].get('cache_hit_rate', {}).get('current_value', 0):.1f}% cache effectiveness</li>
                <li>Maintained high quality standards with {dashboard_data['summary']['overall_score']:.1f}/100 performance score</li>
            </ul>
        </div>
    </div>
</body>
</html>"""

        output_path = Path(output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return str(output_path.absolute())


def main():
    """Demonstrate KPI dashboard generation"""
    print("KPI Dashboard Generator Demo")
    print("=" * 50)

    # Initialize aggregator and generator
    aggregator = UnifiedMetricsAggregator()
    generator = KPIDashboardGenerator(aggregator)

    # Generate comprehensive KPI dashboard
    print("\nGenerating KPI dashboard...")
    dashboard_file = generator.generate_kpi_dashboard()
    print(f"KPI Dashboard saved to: {dashboard_file}")

    # Generate executive summary
    print("\nGenerating executive summary...")
    summary_file = generator.generate_executive_summary_report()
    print(f"Executive Summary saved to: {summary_file}")

    # Generate performance report
    print("\nGenerating performance report...")
    report = aggregator.generate_performance_report()
    report_file = Path("performance_report.md")
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Performance Report saved to: {report_file.absolute()}")

    print("\nKPI Dashboard Generation completed!")
    print("\nGenerated files:")
    print(f"   KPI Dashboard: {dashboard_file}")
    print(f"   Executive Summary: {summary_file}")
    print(f"   Performance Report: {report_file}")


if __name__ == "__main__":
    main()
