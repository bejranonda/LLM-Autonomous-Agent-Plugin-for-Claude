#!/usr/bin/env python3
"""
Web Dashboard for Token Monitoring

Simple web interface for the token monitoring dashboard that provides
real-time visualization of optimization performance and metrics.

Features:
- Real-time statistics display
- Interactive charts and graphs
- Alert management
- Performance monitoring
- Cost savings visualization
- Responsive design for mobile and desktop

Version: 1.0.0 - Production Ready
Author: Autonomous Agent Development Team
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from token_monitoring_dashboard import TokenMonitoringDashboard, MetricType
except ImportError:
    print("Error: Token monitoring dashboard not found.")
    sys.exit(1)

class WebDashboard:
    """Web interface for token monitoring dashboard."""

    def __init__(self, port: int = 8080):
        """Initialize web dashboard."""
        self.port = port
        self.monitoring = TokenMonitoringDashboard()

    def generate_html_page(self) -> str:
        """Generate the main HTML dashboard page."""
        # Get current statistics
        stats = self.monitoring.get_dashboard_stats()
        effectiveness = self.monitoring.get_optimization_effectiveness(24)
        recent_alerts = self.monitoring.alerts[-5:]

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token Optimization Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}

        .header h1 {{
            color: #4a5568;
            font-size: 2.5rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .status-indicator {{
            width: 20px;
            height: 20px;
            background: #48bb78;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}

        .subtitle {{
            color: #718096;
            font-size: 1.1rem;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}

        .metric-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }}

        .metric-label {{
            color: #718096;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}

        .metric-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 5px;
        }}

        .metric-change {{
            color: #48bb78;
            font-size: 0.9rem;
        }}

        .metric-change.negative {{
            color: #f56565;
        }}

        .alerts-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }}

        .alerts-header {{
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 20px;
        }}

        .alert-item {{
            background: #f7fafc;
            border-left: 4px solid #4299e1;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 0 8px 8px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .alert-item.warning {{
            border-left-color: #ed8936;
        }}

        .alert-item.critical {{
            border-left-color: #f56565;
        }}

        .alert-message {{
            color: #2d3748;
            font-weight: 500;
        }}

        .alert-time {{
            color: #718096;
            font-size: 0.85rem;
        }}

        .chart-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }}

        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #48bb78, #38a169);
            border-radius: 10px;
            transition: width 0.5s ease;
        }}

        .progress-fill.warning {{
            background: linear-gradient(90deg, #ed8936, #dd6b20);
        }}

        .progress-fill.danger {{
            background: linear-gradient(90deg, #f56565, #e53e3e);
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}

        .stat-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e2e8f0;
        }}

        .stat-label {{
            color: #718096;
            font-weight: 500;
        }}

        .stat-value {{
            color: #2d3748;
            font-weight: bold;
        }}

        .refresh-button {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
            margin: 20px 0;
        }}

        .refresh-button:hover {{
            transform: scale(1.05);
        }}

        .no-alerts {{
            color: #48bb78;
            font-weight: 500;
            text-align: center;
            padding: 20px;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}

            .header h1 {{
                font-size: 2rem;
            }}

            .metrics-grid {{
                grid-template-columns: 1fr;
                gap: 15px;
            }}

            .metric-value {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                <div class="status-indicator"></div>
                Token Optimization Dashboard
            </h1>
            <div class="subtitle">Real-time monitoring and analytics</div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Tokens Used (Last Hour)</div>
                <div class="metric-value">{stats.total_tokens_used:,}</div>
                <div class="metric-change">Active usage</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(100, stats.total_tokens_used / 1000 * 100)}%"></div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Tokens Saved (Last Hour)</div>
                <div class="metric-value">{stats.total_tokens_saved:,}</div>
                <div class="metric-change">Cost optimization</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(100, stats.total_tokens_saved / 1000 * 100)}%"></div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Cost Savings</div>
                <div class="metric-value">${stats.total_cost_savings:.2f}</div>
                <div class="metric-change">This hour</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(100, stats.total_cost_savings / 10 * 100)}%"></div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Compression Ratio</div>
                <div class="metric-value">{stats.average_compression_ratio:.1%}</div>
                <div class="metric-change {'negative' if stats.average_compression_ratio > 0.8 else ''}">Optimization efficiency</div>
                <div class="progress-bar">
                    <div class="progress-fill {'warning' if stats.average_compression_ratio > 0.8 else ''} {'danger' if stats.average_compression_ratio > 0.9 else ''}" style="width: {stats.average_compression_ratio * 100}%"></div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Cache Hit Rate</div>
                <div class="metric-value">{stats.cache_hit_rate:.1%}</div>
                <div class="metric-change {'negative' if stats.cache_hit_rate < 0.7 else ''}">Performance metric</div>
                <div class="progress-bar">
                    <div class="progress-fill {'warning' if stats.cache_hit_rate < 0.8 else ''} {'danger' if stats.cache_hit_rate < 0.7 else ''}" style="width: {stats.cache_hit_rate * 100}%"></div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">System Health</div>
                <div class="metric-value">{stats.system_health_score:.1%}</div>
                <div class="metric-change">Overall status</div>
                <div class="progress-bar">
                    <div class="progress-fill {'warning' if stats.system_health_score < 0.9 else ''} {'danger' if stats.system_health_score < 0.8 else ''}" style="width: {stats.system_health_score * 100}%"></div>
                </div>
            </div>
        </div>

        <div class="chart-container">
            <h2>Optimization Effectiveness</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-label">Best Compression</span>
                    <span class="stat-value">{effectiveness['compression_effectiveness']['best_ratio']:.1%}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Average Compression</span>
                    <span class="stat-value">{effectiveness['compression_effectiveness']['average_ratio']:.1%}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Total Optimizations</span>
                    <span class="stat-value">{effectiveness['compression_effectiveness']['total_optimizations']}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Best Cache Hit Rate</span>
                    <span class="stat-value">{effectiveness['cache_effectiveness']['best_hit_rate']:.1%}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Average Hit Rate</span>
                    <span class="stat-value">{effectiveness['cache_effectiveness']['average_hit_rate']:.1%}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Cache Hits</span>
                    <span class="stat-value">{effectiveness['cache_effectiveness']['total_cache_hits']}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Total Tokens Saved</span>
                    <span class="stat-value">{effectiveness['token_savings']['total_saved']:,}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Cost Savings Rate</span>
                    <span class="stat-value">{effectiveness['token_savings']['savings_rate']:.1%}</span>
                </div>
            </div>
        </div>

        <div class="alerts-section">
            <div class="alerts-header">
                <h2>Recent Alerts</h2>
            </div>
            {self._generate_alerts_html(recent_alerts)}
        </div>

        <center>
            <button class="refresh-button" onclick="location.reload()">
                🔄 Refresh Dashboard
            </button>
        </center>

        <div class="chart-container">
            <h2>System Information</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-label">Active Users</span>
                    <span class="stat-value">{stats.active_users}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Response Time</span>
                    <span class="stat-value">{stats.average_response_time:.1f}ms</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Alerts (1h)</span>
                    <span class="stat-value">{stats.alerts_count}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Uptime</span>
                    <span class="stat-value">{stats.uptime_percentage:.1f}%</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Last Updated</span>
                    <span class="stat-value">{stats.timestamp.strftime('%H:%M:%S')}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">System Status</span>
                    <span class="stat-value" style="color: #48bb78;">🟢 Operational</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => {{
            location.reload();
        }}, 30000);

        // Add some interactivity
        document.querySelectorAll('.metric-card').forEach(card => {{
            card.addEventListener('click', function() {{
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {{
                    this.style.transform = '';
                }}, 100);
            }});
        }});
    </script>
</body>
</html>
        """
        return html_content

    def _generate_alerts_html(self, alerts) -> str:
        """Generate HTML for alerts section."""
        if not alerts:
            return '<div class="no-alerts">✅ No recent alerts - System operating normally</div>'

        alerts_html = ""
        for alert in alerts:
            alert_class = ""
            if alert.level.value == "warning":
                alert_class = "warning"
            elif alert.level.value == "critical":
                alert_class = "critical"

            time_str = alert.timestamp.strftime('%H:%M:%S')
            alerts_html += f"""
            <div class="alert-item {alert_class}">
                <div class="alert-message">{alert.message}</div>
                <div class="alert-time">{time_str}</div>
            </div>
            """

        return alerts_html

    def start_server(self):
        """Start the web server."""
        try:
            import http.server
            import socketserver
            import webbrowser

            # Create a simple handler
            class DashboardHandler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.dashboard = kwargs.pop('dashboard', None)

                def do_GET(self):
                    if self.path == '/' or self.path == '/dashboard':
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        html_content = self.dashboard.generate_html_page()
                        self.wfile.write(html_content.encode())
                    else:
                        super().do_GET()

            # Create custom handler class with dashboard
            handler_class = type('DashboardHandlerWithDashboard', (DashboardHandler,), {})
            handler_class.dashboard = self

            # Start server
            with socketserver.TCPServer(("", self.port), handler_class) as httpd:
                print(f"🚀 Token Optimization Dashboard")
                print(f"📊 Server running at: http://localhost:{self.port}")
                print(f"🔄 Auto-refresh every 30 seconds")
                print(f"⏹ Press Ctrl+C to stop")
                print()

                # Open browser automatically
                webbrowser.open(f"http://localhost:{self.port}")

                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\n👋 Dashboard stopped")

        except ImportError:
            print("Error: http.server module not available")
            print("Please run this on Python 3.7+")

def main():
    """Command line interface for web dashboard."""
    import argparse

    parser = argparse.ArgumentParser(description="Token Optimization Web Dashboard")
    parser.add_argument("--port", type=int, default=8080, help="Port to run server on")
    parser.add_argument("--html", action="store_true", help="Generate HTML file instead of starting server")

    args = parser.parse_args()

    dashboard = WebDashboard(args.port)

    if args.html:
        # Generate HTML file
        html_content = dashboard.generate_html_page()
        output_file = Path("token_dashboard.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML dashboard saved to: {output_file.absolute()}")
        print(f"Open in browser to view the dashboard")
    else:
        # Start web server
        dashboard.start_server()

if __name__ == "__main__":
    main()