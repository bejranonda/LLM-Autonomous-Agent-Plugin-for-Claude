#!/usr/bin/env python3
"""
Token Usage Monitoring and Analytics System

Comprehensive monitoring and analytics system for tracking token consumption
across all autonomous agent operations with real-time insights and optimization recommendations.

Version: 1.0.0
Author: Autonomous Agent Plugin
"""

import json
import os
import time
import pathlib
from typing import Callable
import statistics
import threading
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import sqlite3

from token_optimization_engine import get_token_optimizer
from smart_caching_system import get_smart_cache
from agent_communication_optimizer import get_communication_optimizer


class MetricType(Enum):
    """Types of metrics that can be tracked."""
    CONSUMPTION = "consumption"
    EFFICIENCY = "efficiency"
    PERFORMANCE = "performance"
    PREDICTION = "prediction"
    COMMUNICATION = "communication"
    CACHE = "cache"


class AlertLevel(Enum):
    """Alert levels for monitoring."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class TokenMetric:
    """Single token measurement."""
    timestamp: float
    metric_type: MetricType
    value: float
    tags: Dict[str, str]
    source: str
    context: Dict[str, Any]

    @property
    def formatted_timestamp(self) -> str:
        """Get formatted timestamp."""
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timestamp))


@dataclass
class Alert:
    """System alert for token usage monitoring."""
    level: AlertLevel
    message: str
    metric_type: MetricType
    threshold: float
    current_value: float
    timestamp: float
    recommendations: List[str]
    resolved: bool = False


@dataclass
class TokenBudget:
    """Token budget tracking."""
    budget_id: str
    total_budget: int
    used_tokens: int
    remaining_tokens: int
    start_time: float
    end_time: Optional[float]
    alerts_triggered: List[str]
    efficiency_score: float


class TokenMonitoringSystem:
    """
    Comprehensive token usage monitoring and analytics system.
    """

    def __init__(self, db_path: str = None, cache_dir: str = ".claude-patterns"):
        self.cache_dir = pathlib.Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Database setup
        if db_path is None:
            db_path = self.cache_dir / "token_monitoring.db"
        self.db_path = pathlib.Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_database()

        # Monitoring configuration
        self.alert_thresholds = {
            MetricType.CONSUMPTION: {
                'warning': 50000,      # 50K tokens
                'error': 80000,        # 80K tokens
                'critical': 100000     # 100K tokens
            },
            MetricType.EFFICIENCY: {
                'warning': 0.3,         # 30% efficiency
                'error': 0.2,           # 20% efficiency
                'critical': 0.1         # 10% efficiency
            },
            MetricType.PERFORMANCE: {
                'warning': 5.0,         # 5 seconds
                'error': 10.0,          # 10 seconds
                'critical': 15.0        # 15 seconds
            }
        }

        # Active monitoring
        self.active_budgets: Dict[str, TokenBudget] = {}
        self.real_time_monitoring = False
        self.monitoring_thread = None

        # Statistics cache
        self.stats_cache = {}
        self.stats_cache_ttl = 300  # 5 minutes

        # Core components
        self.token_optimizer = get_token_optimizer()
        self.cache = get_smart_cache()
        self.comm_optimizer = get_communication_optimizer()

        # Monitoring data
        self.metrics_buffer = deque(maxlen=10000)
        self.alerts: List[Alert] = []
        self.reports: Dict[str, Any] = {}

        # Alert handlers
        self.alert_handlers: Dict[MetricType, List[Callable]] = defaultdict(list)

        # Files
        self.reports_dir = self.cache_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)

        # Load existing data
        self._load_alerts()

    def _init_database(self) -> None:
        """Initialize SQLite database for metrics storage."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS token_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                metric_type TEXT NOT NULL,
                value REAL NOT NULL,
                tags TEXT,
                source TEXT NOT NULL,
                context TEXT,
                created_at REAL DEFAULT (strftime('%s', 'now'))
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS token_budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                budget_id TEXT UNIQUE NOT NULL,
                total_budget INTEGER NOT NULL,
                used_tokens INTEGER DEFAULT 0,
                remaining_tokens INTEGER NOT NULL,
                start_time REAL NOT NULL,
                end_time REAL,
                alerts_triggered TEXT,
                efficiency_score REAL DEFAULT 0.0,
                created_at REAL DEFAULT (strftime('%s', 'now'))
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                threshold REAL NOT NULL,
                current_value REAL NOT NULL,
                timestamp REAL NOT NULL,
                recommendations TEXT,
                resolved BOOLEAN DEFAULT 0,
                created_at REAL DEFAULT (strftime('%s', 'now'))
            )
        """)

        # Create indexes for better performance
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON token_metrics(timestamp)")
        self.start_time = time.time()
        self.conn.commit()

    def record_metric(self, metric_type: MetricType, value: float,
                      source: str = "unknown", tags: Dict[str, str] = None,
                      context: Dict[str, Any] = None) -> None:
        """Record a token metric."""
        if tags is None:
            tags = {}

        if context is None:
            context = {}

        metric = TokenMetric(
            timestamp=time.time(),
            metric_type=metric_type,
            value=value,
            tags=tags,
            source=source,
            context=context
        )

        # Store in database
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO token_metrics (timestamp, metric_type, value, tags, source, context)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            metric.timestamp,
            metric.metric_type.value,
            metric.value,
            json.dumps(metric.tags),
            metric.source,
            json.dumps(metric.context)
        ))
        self.conn.commit()

        # Add to buffer
        self.metrics_buffer.append(metric)

        # Check for alerts
        self._check_alerts(metric)

        # Update stats cache
        self._update_stats_cache(metric_type)

    def create_budget(self, budget_id: str, total_budget: int,
                     user_id: str = None, duration: int = None) -> str:
        """Create a new token budget."""
        budget = TokenBudget(
            budget_id=budget_id,
            total_budget=total_budget,
            used_tokens=0,
            remaining_tokens=total_budget,
            start_time=time.time(),
            end_time=time.time() + duration if duration else None,
            alerts_triggered=[],
            efficiency_score=0.0
        )

        self.active_budgets[budget_id] = budget

        # Store in database
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO token_budgets (budget_id, total_budget, used_tokens, remaining_tokens, start_time, end_time, alerts_triggered, efficiency_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            budget.budget_id,
            budget.total_budget,
            budget.used_tokens,
            budget.remaining_tokens,
            budget.start_time,
            budget.end_time,
            json.dumps(budget.alerts_triggered),
            budget.efficiency_score
        ))
        self.conn.commit()

        return budget_id

    def use_budget(self, budget_id: str, tokens: int,
                   context: Dict[str, Any] = None) -> bool:
        """Use tokens from a budget."""
        if budget_id not in self.active_budgets:
            return False

        budget = self.active_budgets[budget_id]

        # Check if budget is expired
        if budget.end_time and time.time() > budget.end_time:
            return False

        # Check if enough tokens available
        if budget.remaining_tokens < tokens:
            self._trigger_budget_alert(budget, tokens)
            return False

        # Update budget
        budget.used_tokens += tokens
        budget.remaining_tokens -= tokens

        # Update efficiency score
        budget.efficiency_score = budget.used_tokens / budget.total_budget

        # Store in database
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE token_budgets
            SET used_tokens = ?, remaining_tokens = ?, efficiency_score = ?
            WHERE budget_id = ?
        """, (budget.used_tokens, budget.remaining_tokens, budget.efficiency_score, budget.budget_id))
        self.conn.commit()

        # Record metric
        self.record_metric(
            MetricType.CONSUMPTION,
            tokens,
            f"budget_{budget_id}",
            {"budget_id": budget_id, "user_id": user_id or "default"},
            context
        )

        return True

    def get_budget_status(self, budget_id: str) -> Dict[str, Any]:
        """Get status of a token budget."""
        if budget_id not in self.active_budgets:
            return {"error": "Budget not found"}

        budget = self.active_budgets[budget_id]
        elapsed_time = time.time() - budget.start_time
        time_remaining = None

        if budget.end_time:
            time_remaining = max(0, budget.end_time - time.time())

        return {
            "budget_id": budget_id,
            "total_budget": budget.total_budget,
            "used_tokens": budget.used_tokens,
            "remaining_tokens": budget.remaining_tokens,
            "usage_percentage": budget.efficiency_score * 100,
            "elapsed_time": elapsed_time,
            "time_remaining": time_remaining,
            "alerts_triggered": len(budget.alerts_triggered),
            "efficiency_score": budget.efficiency_score,
            "status": "active"
        }

    def get_analytics(self, metric_type: MetricType = None,
                     time_range: int = 3600, limit: int = 1000) -> Dict[str, Any]:
        """Get analytics for token usage."""
        if metric_type is None:
            return self._get_overall_analytics(time_range, limit)

        # Get recent metrics from database
        cursor = self.conn.cursor()
        since_time = time.time() - time_range

        cursor.execute("""
            SELECT timestamp, value, tags, source, context
            FROM token_metrics
            WHERE metric_type = ? AND timestamp > ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (metric_type.value, since_time, limit))

        rows = cursor.fetchall()
        metrics = []
        for row in rows:
            metrics.append({
                'timestamp': row[0],
                'value': row[1],
                'tags': json.loads(row[2]),
                'source': row[3],
                'context': json.loads(row[4])
            })

        if not metrics:
            return {"message": "No data available"}

        # Calculate statistics
        values = [m['value'] for m in metrics]
        return {
            'metric_type': metric_type.value,
            'count': len(metrics),
            'time_range_hours': time_range / 3600,
            'min_value': min(values),
            'max_value': max(values),
            'avg_value': statistics.mean(values),
            'median_value': statistics.median(values),
            'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
            'trend': self._calculate_trend(values),
            'recent_values': values[:10],
            'top_sources': self._get_top_sources(metrics)
        }

    def _get_overall_analytics(self, time_range: int, limit: int) -> Dict[str, Any]:
        """Get overall analytics across all metric types."""
        analytics = {
            'overview': {},
            'metrics_by_type': {},
            'alerts_summary': {},
            'budget_summary': {},
            'recommendations': []
        }

        # Overview statistics
        cursor = self.conn.cursor()
        since_time = time.time() - time_range

        for metric_type in MetricType:
            cursor.execute("""
                SELECT COUNT(*), AVG(value), MIN(value), MAX(value), SUM(value)
                FROM token_metrics
                WHERE metric_type = ? AND timestamp > ?
            """, (metric_type.value, since_time))

            row = cursor.fetchone()
            if row and row[0] > 0:
                analytics['metrics_by_type'][metric_type.value] = {
                    'count': row[0],
                    'avg_value': row[1],
                    'min_value': row[2],
                    'max_value': row[3],
                    'total_value': row[4]
                }

        # Alerts summary
        active_alerts = [alert for alert in self.alerts if not alert.resolved]
        analytics['alerts_summary'] = {
            'total_alerts': len(self.alerts),
            'active_alerts': len(active_alerts),
            'by_level': {
                level: len([a for a in self.alerts if a.level == level and not a.resolved])
                for level in AlertLevel
            }
        }

        # Budget summary
        analytics['budget_summary'] = {
            'active_budgets': len(self.active_budgets),
            'total_budget': sum(b.total_budget for b in self.active_budgets.values()),
            'total_used': sum(b.used_tokens for b in self.active_budgets.values()),
            'total_remaining': sum(b.remaining_tokens for b in self.active_budgets.values()),
            'average_efficiency': statistics.mean([
                b.efficiency_score for b in self.active_budgets.values()
            ]) if self.active_budgets else 0
        }

        # Generate recommendations
        analytics['recommendations'] = self._generate_recommendations()

        return analytics

    def create_report(self, report_type: str = "daily",
                      time_range: int = 86400) -> str:
        """Create monitoring report."""
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        report_id = f"token_report_{report_type}_{timestamp}"
        report_path = self.reports_dir / f"{report_id}.md"

        analytics = self._get_overall_analytics(time_range)

        # Create markdown report
        report_content = f"""# Token Usage Monitoring Report

**Report Type**: {report_type.title()}
**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}
**Time Range**: {time_range / 3600:.1f} hours

## Executive Summary

- **Total Metrics Tracked**: {sum(data.get('count', 0) for data in analytics['metrics_by_type'].values())}
- **Active Budgets**: {analytics['budget_summary']['active_budgets']}
- **Total Budget**: {analytics['budget_summary']['total_budget']:,}
- **Tokens Used**: {analytics['budget_summary']['total_used']:,}
- **Tokens Remaining**: {analytics['budget_summary']['total_remaining']:,}
- **Average Efficiency**: {analytics['budget_summary']['average_efficiency']:.2%}

## Metrics by Type

"""

        for metric_type, data in analytics['metrics_by_type'].items():
            report_content += f"""
### {metric_type.title()}
- **Count**: {data['count']:,}
- **Average**: {data['avg_value']:.2f}
- **Range**: {data['min_value']:.2f} - {data['max_value']:.2f}
- **Total**: {data['total_value']:,}

"""

        report_content += f"""
## Budget Summary

- **Active Budgets**: {analytics['budget_summary']['active_budgets']}
- **Total Allocated**: {analytics['budget_summary']['total_budget']:,}
- **Total Consumed**: {analytics['budget_summary']['total_used']:,}
- **Available**: {analytics['budget_summary']['total_remaining']:,}
- **Utilization Rate**: {(analytics['budget_summary']['total_used'] / analytics['budget_summary']['total_budget'] * 100):.1f}%

## Alerts Summary

- **Total Alerts**: {analytics['alerts_summary']['total_alerts']}
- **Active Alerts**: {analytics['alerts_summary']['active_alerts']}
- **By Level**:
  - Critical: {analytics['alerts_summary']['by_level'].get('critical', 0)}
  - Error: {analytics['alerts_summary']['by_level'].get('error', 0)}
  - Warning: {analytics['alerts_summary']['by_level'].get('warning', 0)}
  - Info: {analytics['alerts_summary']['by_level'].get('info', 0)}

## Recommendations

"""

        for recommendation in analytics['recommendations']:
            report_content += f"- {recommendation}\n"

        report_content += f"""
## Trend Analysis

{self._generate_trend_analysis()}

---

*Report generated by Token Monitoring System*
"""

        # Write report to file
        with open(report_path, 'w') as f:
            f.write(report_content)

        return str(report_path)

    def _check_alerts(self, metric: TokenMetric) -> None:
        """Check if metric triggers any alerts."""
        thresholds = self.alert_thresholds.get(metric.metric_type, {})

        for alert_level, threshold in thresholds.items():
            if self._should_trigger_alert(metric, threshold, alert_level):
                alert = Alert(
                    level=alert_level,
                    message=self._generate_alert_message(metric, alert_level),
                    metric_type=metric.metric_type,
                    threshold=threshold,
                    current_value=metric.value,
                    timestamp=metric.timestamp,
                    recommendations=self._generate_alert_recommendations(metric, alert_level),
                    resolved=False
                )

                self.alerts.append(alert)
                self._save_alerts()

                # Trigger alert handlers
                self._trigger_alert_handlers(alert)

    def _should_trigger_alert(self, metric: TokenMetric, threshold: float,
                              alert_level: AlertLevel) -> bool:
        """Determine if alert should be triggered."""
        if alert_level == AlertLevel.CRITICAL:
            return metric.value >= threshold
        elif alert_level == AlertLevel.ERROR:
            return metric.value >= threshold
        elif alert_level == AlertLevel.WARNING:
            return metric.value >= threshold
        else:
            return metric.value >= threshold * 0.9  # 90% of threshold for info

    def _generate_alert_message(self, metric: TokenMetric, level: AlertLevel) -> str:
        """Generate alert message."""
        return f"{level.title()} Alert: {metric.metric_type.value()} - Current: {metric.value:.2f}"

    def _generate_alert_recommendations(self, metric: TokenMetric,
                                        level: AlertLevel) -> List[str]:
        """Generate recommendations for alert."""
        recommendations = []

        if metric.metric_type == MetricType.CONSUMPTION:
            if level in [AlertLevel.ERROR, AlertLevel.CRITICAL]:
                recommendations.append("Consider using token optimization features")
                recommendations.append("Review and optimize message compression")
                recommendations.append("Enable progressive content loading")
        elif level == AlertLevel.WARNING:
                recommendations.append("Monitor token usage trends")
                recommendations.append("Consider optimizing recent operations")
        elif level == AlertLevel.INFO:
                    recommendations.append("Continue monitoring token efficiency")

        elif metric.metric_type == MetricType.EFFICIENCY:
            if level in [AlertLevel.ERROR, AlertLevel.CRITICAL]:
                recommendations.append("Review optimization strategies")
                recommendations.append("Check compression effectiveness")
                recommendations.append("Consider different optimization approaches")
            elif level == AlertLevel.WARNING:
                recommendations.append("Fine-tune optimization parameters")
                recommendations.append("Monitor efficiency trends")

        return recommendations

    def _trigger_budget_alert(self, budget: TokenBudget, requested_tokens: int) -> None:
        """Trigger budget alert."""
        if budget.remaining_tokens < requested_tokens:
            alert = Alert(
                level=AlertLevel.ERROR,
                message=f"Budget exceeded: Need {requested_tokens}, have {budget.remaining_tokens}",
                metric_type=MetricType.CONSUMPTION,
                threshold=budget.total_budget,
                current_value=budget.used_tokens + requested_tokens,
                timestamp=time.time(),
                recommendations=[
                    "Reduce token usage in current operations",
                    "Increase budget allocation",
                    "Use more efficient communication"
                ],
                resolved=False
            )

            self.alerts.append(alert)
            budget.alerts_triggered.append(f"budget_exceeded_{int(time.time())}")
            self._save_alerts()

    def _trigger_alert_handlers(self, alert: Alert) -> None:
        """Trigger alert handlers for different metric types."""
        handlers = self.alert_handlers.get(alert.metric_type, [])
        for handler in handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"Alert handler error: {e}")

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend from values."""
        if len(values) < 2:
            return "insufficient_data"

        # Simple linear trend calculation
        recent_values = values[-10:]  # Last 10 values
        if len(recent_values) < 2:
            return "insufficient_data"

        x = list(range(len(recent_values)))
        y = recent_values

        try:
            slope, intercept = statistics.linear_regression(x, y)
            if slope > 0.1:
                return "increasing"
            elif slope < -0.1:
                return "decreasing"
            else:
                return "stable"
        except statistics.StatisticsError:
            return "calculating"

    def _generate_trend_analysis(self) -> str:
        """Generate trend analysis summary."""
        # Get recent consumption metrics
        consumption_analytics = self.get_analytics(MetricType.CONSUMUTION, 86400, 100)
        efficiency_analytics = self.get_analytics(MetricType.EFFICIENCY, 86400, 100)

        analysis = "## Trend Analysis\n\n"

        if 'trend' in consumption_analytics:
            analysis += f"**Token Consumption**: {consumption_analytics['trend'].title()}\n"
        else:
            analysis += "**Token Consumption**: No trend data available\n"

        if 'trend' in efficiency_analytics:
            analysis += f"**Efficiency**: {efficiency_analytics['trend'].title()}\n"
        else:
            analysis += "**Efficiency**: No trend data available\n"

        # Add recommendations based on trends
        if consumption_analytics.get('trend') == 'increasing':
            analysis += "\n[WARN] **Recommendation**: Token consumption is increasing. Consider enabling optimization features.\n"
        elif consumption_analytics.get('trend') == 'decreasing':
            analysis += "\n[OK] **Good**: Token consumption is decreasing. Current optimization strategy is effective.\n"

        return analysis

    def _update_stats_cache(self, metric_type: MetricType) -> None:
        """Update statistics cache for a metric type."""
        self.stats_cache[f"{metric_type.value}_last_update"] = time.time()

    def _get_top_sources(self, metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get top sources by metric count."""
        source_counts = defaultdict(int)
        for metric in metrics:
            source = metric['source']
            source_counts[source] += 1

        top_sources = [
            {'source': source, 'count': count}
            for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        return top_sources[:5]

    def _generate_recommendations(self) -> List[str]:
        """Generate system-wide recommendations."""
        recommendations = []

        # Check budget utilization
        total_budget = sum(b.total_budget for b in self.active_budgets.values())
        total_used = sum(b.used_tokens for b in self.active_budgets.values())
        utilization = total_used / total_budget if total_budget > 0 else 0

        if utilization > 0.9:
            recommendations.append("High budget utilization - consider increasing budgets or optimizing usage")
        elif utilization < 0.5:
            recommendations.append("Low budget utilization - budgets may be underutilized")

        # Check alert frequency
        recent_alerts = [a for a in self.alerts if time.time() - a.timestamp < 3600]  # Last hour
        if len(recent_alerts) > 10:
            recommendations.append("High alert frequency - review system configuration and thresholds")

        # Check cache efficiency
        cache_stats = self.cache.get_cache_statistics()
        if cache_stats.get('hit_rate', 0) < 0.5:
            recommendations.append("Low cache hit rate - consider adjusting cache policies")

        return recommendations

    def _load_alerts(self) -> None:
        """Load alerts from database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
        rows = cursor.fetchall()

        for row in rows:
            alert = Alert(
                level=AlertLevel(row[1]),
                message=row[2],
                metric_type=MetricType(row[3]),
                threshold=row[4],
                current_value=row[5],
                timestamp=row[6],
                recommendations=json.loads(row[7]),
                resolved=bool(row[8])
            )
            self.alerts.append(alert)

    def _save_alerts(self) -> None:
        """Save alerts to database."""
        cursor = self.conn.cursor()
        # Clear resolved alerts older than 7 days
        cutoff_time = time.time() - (7 * 24 * 3600)
        cursor.execute("DELETE FROM alerts WHERE resolved = 1 AND timestamp < ?", (cutoff_time,))
        cursor.execute("DELETE FROM alerts WHERE resolved = 0 AND timestamp < ?", (cutoff_time,))

        # Save current alerts
        for alert in self.alerts:
            cursor.execute("""
                INSERT OR REPLACE INTO alerts
                (level, message, metric_type, threshold, current_value, timestamp, recommendations, resolved, id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.level.value,
                alert.message,
                alert.metric_type.value,
                alert.threshold,
                alert.current_value,
                alert.timestamp,
                json.dumps(alert.recommendations),
                int(alert.resolved),
                int(time.time() * 1000)  # Use timestamp as unique ID
            ))

        self.conn.commit()

    def start_real_time_monitoring(self) -> None:
        """Start real-time monitoring."""
        if self.real_time_monitoring:
            return

        self.real_time_monitoring = True

        def monitor_loop():
            while self.real_time_monitoring:
                try:
                    # Collect metrics from all components
                    self._collect_component_metrics()

                    # Process metrics and generate alerts
                    self._process_metrics()

                    # Sleep for monitoring interval
                    time.sleep(30)  # Monitor every 30 seconds
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(60)  # Wait longer on error

        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()

    def stop_real_time_monitoring(self) -> None:
        """Stop real-time monitoring."""
        self.real_time_monitoring = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)

    def _collect_component_metrics(self) -> None:
        """Collect metrics from all components."""
        # Collect from token optimizer
        try:
            optimizer_stats = self.token_optimizer.get_optimization_report()
            self.record_metric(
                MetricType.EFFICIENCY,
                optimizer_stats.get('overall_score', 0),
                "token_optimizer",
                {"component": "token_optimizer"}
            )
        except Exception as e:
            print(f"Error collecting optimizer metrics: {e}")

        # Collect from cache
        try:
            cache_stats = self.cache.get_cache_statistics()
            self.record_metric(
                MetricType.CACHE,
                cache_stats.get('hit_rate', 0),
                "smart_cache",
                {"component": "smart_cache"}
            )
        except Exception as e:
            print(f"Error collecting cache metrics: {e}")

        # Collect from communication optimizer
        try:
            comm_report = self.comm_optimizer.get_optimization_report()
            self.record_metric(
                MetricType.COMMUNICATION,
                comm_report.get('overall_efficiency', 0),
                "comm_optimizer",
                {"component": "communication_optimizer"}
            )
        except Exception as e:
            print(f"Error collecting communication metrics: {e}")

    def _process_metrics(self) -> None:
        """Process buffered metrics and generate alerts."""
        # Process metrics in buffer
        while self.metrics_buffer:
            metric = self.metrics_buffer.popleft()
            self._check_alerts(metric)

        # Clean up old metrics
        self._cleanup_old_data()

    def _cleanup_old_data(self) -> None:
        """Clean up old monitoring data."""
        cutoff_time = time.time() - (7 * 24 * 3600)  # 7 days

        # Clean old alerts
        self.alerts = [a for a in self.alerts if a.timestamp > cutoff_time]
        self._save_alerts()

        # Clean old metrics
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM token_metrics WHERE timestamp < ?", (cutoff_time,))
        self.conn.commit()

    def add_alert_handler(self, metric_type: MetricType, handler: Callable) -> None:
        """Add custom alert handler for specific metric type."""
        self.alert_handlers[metric_type].append(handler)

    def resolve_alert(self, alert_id: int) -> bool:
        """Resolve an alert by ID."""
        for i, alert in enumerate(self.alerts):
            if int(time.time() * 1000) == alert_id:
                alert.resolved = True
                self._save_alerts()
                return True
        return False

    def get_active_alerts(self) -> List[Alert]:
        """Get all active (unresolved) alerts."""
        return [alert for alert in self.alerts if not alert.resolved]

    def clear_old_data(self, days: int = 7) -> None:
        """Clear old monitoring data."""
        cutoff_time = time.time() - (days * 24 * 3600)

        # Clear old metrics
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM token_metrics WHERE timestamp < ?", (cutoff_time,))
        cursor.execute("DELETE FROM alerts WHERE timestamp < ? AND resolved = 1", (cutoff_time,))
        cursor.execute("DELETE FROM token_budgets WHERE end_time < ? AND end_time < ?", (cutoff_time, cutoff_time))

        # Clean up old files
        for file_path in self.reports_dir.glob("*.md"):
            if file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()

        self.conn.commit()

    def export_data(self, format_type: str = "json", time_range: int = 86400) -> str:
        """Export monitoring data."""
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        export_path = self.cache_dir / f"token_monitoring_export_{timestamp}.{format_type}"

        if format_type == "json":
            data = {
                "export_timestamp": timestamp,
                "time_range_hours": time_range / 3600,
                "metrics": list(self.metrics_buffer),
                "alerts": [asdict(alert) for alert in self.alerts],
                "budgets": [asdict(budget) for budget in self.active_budgets.values()],
                "stats": self.stats
            }

            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)

        return str(export_path)

    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status."""
        return {
            "monitoring_active": self.real_time_monitoring,
            "database_connection": self.conn is not None,
            "alerts_active": len(self.get_active_alerts()),
            "metrics_buffer_size": len(self.metrics_buffer),
            "active_budgets": len(self.active_budgets),
            "cache_status": "healthy",
            "last_cleanup": time.time()
        }


# Global monitoring instance
_token_monitor = None

def get_token_monitoring() -> TokenMonitoringSystem:
    """Get or create global token monitoring system instance."""
    global _token_monitor
    if _token_monitor is None:
        _token_monitor = TokenMonitoringSystem()
    return _token_monitor


if __name__ == "__main__":
    monitor = get_token_monitoring()

    # Test basic functionality
    monitor.record_metric(MetricType.CONSUMPTION, 1500, "test", {"test": True})
    monitor.record_metric(MetricType.EFFICIENCY, 0.7, "test", {"test": True})

    print("=== Token Monitoring System Test ===")
    print(f"System Health: {monitor.get_system_health()}")
    print(f"Active Budgets: {len(monitor.active_budgets)}")
    print(f"Alerts: {len(monitor.get_active_alerts())}")