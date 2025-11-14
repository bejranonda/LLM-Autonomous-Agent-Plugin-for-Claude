"""
    Unified Metrics Aggregator for Token Optimization Framework
    """
Centralizes metrics from all optimization systems and provides KPI tracking
import sqlite3
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from pathlib import Path


class MetricPeriod(Enum):
    """Period types for aggregation"""

    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class KpiCategory(Enum):
    """KPI categories for tracking"""

    PERFORMANCE = "performance"
    COST = "cost"
    QUALITY = "quality"
    USER_EXPERIENCE = "user_experience"
    SYSTEM_HEALTH = "system_health"


@dataclass
class AggregatedMetric:
    """Aggregated metric with multiple dimensions"""

    timestamp: datetime
    metric_name: str
    category: KpiCategory
    period: MetricPeriod
    value: float
    unit: str
    source_system: str
    metadata: Dict[str, Any]


@dataclass
class KpiDefinition:
    """KPI definition with targets and thresholds"""

    name: str
    category: KpiCategory
    description: str
    unit: str
    target_value: float
    minimum_acceptable: float
    optimal_value: float
    weight: float = 1.0


class UnifiedMetricsAggregator:
    """Centralizes metrics aggregation from all optimization systems"""

    def __init__(self, db_path: str = None, cache_dir: str = ".claude-patterns"):
        self.db_path = db_path or f"{cache_dir}/unified_metrics.db"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Thread safety
        self.lock = threading.RLock()

        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize database
        self._init_database()

        # KPI definitions
        self._init_kpi_definitions()

        # Cache for performance
        self._metric_cache = {}
        self._kpi_cache = {}

        self.logger.info("Unified Metrics Aggregator initialized")

    def _init_database(self):
        """Initialize SQLite database for metrics storage"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Aggregated metrics table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS aggregated_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    period TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT NOT NULL,
                    source_system TEXT NOT NULL,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # KPI results table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS kpi_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    kpi_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    value REAL NOT NULL,
                    target_value REAL NOT NULL,
                    achievement_rate REAL NOT NULL,
                    trend TEXT,
                    period TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # System snapshots table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS system_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    total_tokens_saved INTEGER DEFAULT 0,
                    total_cost_savings REAL DEFAULT 0.0,
                    overall_effectiveness REAL DEFAULT 0.0,
                    cache_hit_rate REAL DEFAULT 0.0,
                    compression_ratio REAL DEFAULT 0.0,
                    user_satisfaction REAL DEFAULT 0.0,
                    system_health_score REAL DEFAULT 0.0,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON aggregated_metrics(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_name ON aggregated_metrics(metric_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_kpi_timestamp ON kpi_results(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_snapshot_timestamp ON system_snapshots(timestamp)")

            conn.commit()

    def _init_kpi_definitions(self):
        """Initialize KPI definitions with targets"""
        self.kpi_definitions = {
            # Performance KPIs
            "token_reduction_rate": KpiDefinition(
                name="Token Reduction Rate",
                category=KpiCategory.PERFORMANCE,
                description="Percentage of tokens saved through optimization",
                unit="%",
                target_value=60.0,
                minimum_acceptable=40.0,
                optimal_value=75.0,
                weight=2.0,
            ),
            "cache_hit_rate": KpiDefinition(
                name="Cache Hit Rate",
                category=KpiCategory.PERFORMANCE,
                description="Percentage of requests served from cache",
                unit="%",
                target_value=80.0,
                minimum_acceptable=60.0,
                optimal_value=90.0,
                weight=1.5,
            ),
            "response_time_improvement": KpiDefinition(
                name="Response Time Improvement",
                category=KpiCategory.PERFORMANCE,
                description="Percentage improvement in response time",
                unit="%",
                target_value=30.0,
                minimum_acceptable=15.0,
                optimal_value=50.0,
                weight=1.0,
            ),
            # Cost KPIs
            "daily_cost_savings": KpiDefinition(
                name="Daily Cost Savings",
                category=KpiCategory.COST,
                description="Daily monetary savings from token optimization",
                unit="$",
                target_value=50.0,
                minimum_acceptable=25.0,
                optimal_value=100.0,
                weight=2.0,
            ),
            "roi_percentage": KpiDefinition(
                name="ROI Percentage",
                category=KpiCategory.COST,
                description="Return on investment for optimization systems",
                unit="%",
                target_value=300.0,
                minimum_acceptable=150.0,
                optimal_value=500.0,
                weight=1.5,
            ),
            # Quality KPIs
            "compression_quality_score": KpiDefinition(
                name="Compression Quality Score",
                category=KpiCategory.QUALITY,
                description="Quality of compressed content (1-100)",
                unit="score",
                target_value=85.0,
                minimum_acceptable=70.0,
                optimal_value=95.0,
                weight=1.5,
            ),
            "content_integrity_rate": KpiDefinition(
                name="Content Integrity Rate",
                category=KpiCategory.QUALITY,
                description="Percentage of content maintaining integrity",
                unit="%",
                target_value=95.0,
                minimum_acceptable=85.0,
                optimal_value=99.0,
                weight=2.0,
            ),
            # User Experience KPIs
            "user_satisfaction_score": KpiDefinition(
                name="User Satisfaction Score",
                category=KpiCategory.USER_EXPERIENCE,
                description="User satisfaction with optimized responses",
                unit="score",
                target_value=4.0,
                minimum_acceptable=3.0,
                optimal_value=4.5,
                weight=2.0,
            ),
            "task_completion_rate": KpiDefinition(
                name="Task Completion Rate",
                category=KpiCategory.USER_EXPERIENCE,
                description="Percentage of tasks completed successfully",
                unit="%",
                target_value=95.0,
                minimum_acceptable=85.0,
                optimal_value=99.0,
                weight=1.5,
            ),
            # System Health KPIs
            "system_availability": KpiDefinition(
                name="System Availability",
                category=KpiCategory.SYSTEM_HEALTH,
                description="Percentage of time system is available",
                unit="%",
                target_value=99.5,
                minimum_acceptable=98.0,
                optimal_value=99.9,
                weight=2.0,
            ),
            "error_rate": KpiDefinition(
                name="Error Rate",
                category=KpiCategory.SYSTEM_HEALTH,
                description="Percentage of operations resulting in errors",
                unit="%",
                target_value=1.0,
                minimum_acceptable=3.0,
                optimal_value=0.1,
                weight=1.5,
            ),
            "resource_utilization": KpiDefinition(
                name="Resource Utilization",
                category=KpiCategory.SYSTEM_HEALTH,
                description="Percentage of system resources utilized",
                unit="%",
                target_value=70.0,
                minimum_acceptable=90.0,
                optimal_value=60.0,
                weight=1.0,
            ),
        }

    def collect_metrics_from_all_systems(self) -> Dict[str, Any]:
        """Collect metrics from all optimization systems"""
        with self.lock:
            metrics = {
                "progressive_loader": self._collect_progressive_loader_metrics(),
                "smart_cache": self._collect_smart_cache_metrics(),
                "token_monitoring": self._collect_token_monitoring_metrics(),
                "budget_manager": self._collect_budget_manager_metrics(),
                "timestamp": datetime.now().isoformat(),
            }

            # Calculate aggregated metrics
            metrics["aggregated"] = self._calculate_aggregated_metrics(metrics)

            return metrics

    def _collect_progressive_loader_metrics(self) -> Dict[str, Any]:
        """Collect metrics from progressive loading system"""
        try:
            # Try to import progressive loader
            from enhanced_progressive_loader import EnhancedProgressiveLoader

            loader = EnhancedProgressiveLoader()
            summary = loader.get_performance_summary()

            return {
                "total_requests": summary.get("total_optimizations", 0),
                "avg_compression_ratio": summary.get("avg_compression_ratio", 0.0),
                "token_savings": summary.get("total_tokens_saved", 0),
                "avg_optimization_time": summary.get("avg_optimization_time", 0.0),
                "user_patterns": len(loader.user_patterns),
                "cached_items": len(loader.content_cache),
                "performance_improvement": summary.get("avg_compression_ratio", 0.0) * 100,  # Convert to percentage
            }
        except ImportError:
            return {"error": "Progressive loader not available"}
        except Exception as e:
            self.logger.warning(f"Error collecting progressive loader metrics: {e}")
            return {"error": f"Progressive loader error: {str(e)}"}

    def _collect_smart_cache_metrics(self) -> Dict[str, Any]:
        """Collect metrics from smart cache system"""
        try:
            # Try to import smart cache
            from smart_cache_system_simple import SimpleSmartCache

            cache = SimpleSmartCache(max_size_mb=100)
            stats = cache.get_stats()

            return {
                "hit_rate": stats.get("hit_rate", 0.0),
                "total_hits": stats.get("hit_count", 0),
                "total_misses": stats.get("miss_count", 0),
                "cache_size": len(cache.cache),
                "memory_usage": stats.get("memory_usage", 0),
                "prediction_accuracy": stats.get("prediction_accuracy", 0.0),
                "policy_performance": stats.get("policy_performance", {}),
                "evictions": stats.get("evictions", 0),
            }
        except ImportError:
            return {"error": "Smart cache not available"}
        except Exception as e:
            self.logger.warning(f"Error collecting smart cache metrics: {e}")
            return {"error": f"Smart cache error: {str(e)}"}

    def _collect_token_monitoring_metrics(self) -> Dict[str, Any]:
        """Collect metrics from token monitoring system"""
        try:
            # Try to import token monitoring
            from token_monitoring_dashboard import TokenMonitoringDashboard

            monitor = TokenMonitoringDashboard()
            stats = monitor.get_dashboard_stats()
            effectiveness = monitor.get_optimization_effectiveness(24)  # Last 24 hours

            # Calculate savings rate
            total_tokens = stats.total_tokens_used + stats.total_tokens_saved
            savings_rate = (stats.total_tokens_saved / total_tokens * 100) if total_tokens > 0 else 0.0

            return {
                "total_tokens_used": stats.total_tokens_used,
                "total_tokens_saved": stats.total_tokens_saved,
                "savings_rate": savings_rate,
                "cost_savings": stats.total_cost_savings,
                "avg_compression_ratio": effectiveness.get("avg_compression_ratio", stats.average_compression_ratio),
                "avg_cache_hit_rate": effectiveness.get("avg_cache_hit_rate", stats.cache_hit_rate),
                "active_alerts": stats.alerts_count,
                "system_health": stats.system_health_score,
            }
        except ImportError:
            return {"error": "Token monitoring not available"}
        except Exception as e:
            self.logger.warning(f"Error collecting token monitoring metrics: {e}")
            return {"error": f"Token monitoring error: {str(e)}"}

    def _collect_budget_manager_metrics(self) -> Dict[str, Any]:
        """Collect metrics from budget manager system"""
        try:
            # Try to import budget manager
            from token_budget_manager import TokenBudgetManager

            budget_manager = TokenBudgetManager()
            report = budget_manager.get_budget_report(format="summary")

            return {
                "total_budgets": report.get("total_constraints", 0),
                "active_constraints": report.get("active_constraints", 0),
                "avg_utilization": report.get("overall_utilization", 0.0),
                "budget_overruns": report.get("overrun_count", 0),
                "cost_avoidance": report.get("total_cost_avoidance", 0.0),
                "total_allocated": report.get("total_allocated", 0),
                "total_used": report.get("total_used", 0),
            }
        except ImportError:
            return {"error": "Budget manager not available"}
        except Exception as e:
            self.logger.warning(f"Error collecting budget manager metrics: {e}")
            return {"error": f"Budget manager error: {str(e)}"}

    def _calculate_aggregated_metrics(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate aggregated metrics across all systems"""
        aggregated = {}

        # Token metrics - handle missing systems gracefully
        token_monitoring = system_metrics.get("token_monitoring", {})
        progressive_loader = system_metrics.get("progressive_loader", {})

        if "error" not in token_monitoring and "error" not in progressive_loader:
            tokens_used = token_monitoring.get("total_tokens_used", 0)
            tokens_saved = token_monitoring.get("total_tokens_saved", 0)
            progressive_savings = progressive_loader.get("token_savings", 0)

            total_tokens_saved = tokens_saved + progressive_savings
            total_tokens = tokens_used + total_tokens_saved

            aggregated["total_tokens_processed"] = total_tokens
            aggregated["total_tokens_saved"] = total_tokens_saved
            aggregated["overall_savings_rate"] = (total_tokens_saved / total_tokens * 100) if total_tokens > 0 else 0.0

            # Cost metrics
            cost_per_token = 0.002  # $0.002 per 1K tokens = $0.000002 per token
            aggregated["total_cost_savings"] = total_tokens_saved * cost_per_token / 1000
        else:
            # Default values when systems aren't available
            aggregated["total_tokens_processed"] = 0
            aggregated["total_tokens_saved"] = 0
            aggregated["overall_savings_rate"] = 0.0
            aggregated["total_cost_savings"] = 0.0

        # Performance metrics
        smart_cache = system_metrics.get("smart_cache", {})
        if "error" not in smart_cache:
            cache_hit_rate = smart_cache.get("hit_rate", 0.0)
            aggregated["overall_cache_hit_rate"] = cache_hit_rate
        else:
            aggregated["overall_cache_hit_rate"] = 0.0

        # Compression metrics
        if "error" not in progressive_loader and "error" not in token_monitoring:
            avg_compression = progressive_loader.get("avg_compression_ratio", 0.0)
            monitoring_compression = token_monitoring.get("avg_compression_ratio", 0.0)
            if avg_compression > 0:
                aggregated["overall_compression_ratio"] = (avg_compression + monitoring_compression) / 2
            else:
                aggregated["overall_compression_ratio"] = monitoring_compression
        else:
            aggregated["overall_compression_ratio"] = 0.0

        # System health
        if "error" not in token_monitoring:
            system_health = token_monitoring.get("system_health", 0.0)
            error_rate = max(0, 100 - system_health)  # Simple inversion
            aggregated["system_health_score"] = system_health
            aggregated["error_rate"] = error_rate
        else:
            aggregated["system_health_score"] = 0.0
            aggregated["error_rate"] = 0.0

        return aggregated

    def store_aggregated_metrics(self, metrics: Dict[str, Any], period: MetricPeriod = MetricPeriod.DAILY):
        """Store aggregated metrics in database"""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                timestamp = datetime.now().isoformat()

                # Store each aggregated metric
                for metric_name, value in metrics.items():
                    if isinstance(value, (int, float)) and metric_name != "timestamp":
                        # Determine category
                        category = self._categorize_metric(metric_name)

                        cursor.execute(
                            """
                            INSERT INTO aggregated_metrics
                            (timestamp, metric_name, category, period, value, unit, source_system, metadata)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                            (
                                timestamp,
                                metric_name,
                                category.value,
                                period.value,
                                float(value),
                                self._get_metric_unit(metric_name),
                                "unified_aggregator",
                                json.dumps({"source": "aggregation"}),
                            ),
                        )

                conn.commit()

        self.logger.info(f"Stored {len(metrics)} aggregated metrics for {period.value} period")

    def _categorize_metric(self, metric_name: str) -> KpiCategory:
        """Categorize a metric by name"""
        name_lower = metric_name.lower()

        if any(word in name_lower for word in ["token", "compression", "cache", "performance", "response"]):
            return KpiCategory.PERFORMANCE
        elif any(word in name_lower for word in ["cost", "saving", "roi", "budget"]):
            return KpiCategory.COST
        elif any(word in name_lower for word in ["quality", "integrity", "score"]):
            return KpiCategory.QUALITY
        elif any(word in name_lower for word in ["satisfaction", "completion", "user"]):
            return KpiCategory.USER_EXPERIENCE
        elif any(word in name_lower for word in ["health", "availability", "error", "resource"]):
            return KpiCategory.SYSTEM_HEALTH
        else:
            return KpiCategory.PERFORMANCE  # Default

    def _get_metric_unit(self, metric_name: str) -> str:
        """Get unit for metric by name"""
        name_lower = metric_name.lower()

        if "rate" in name_lower or "percentage" in name_lower:
            return "%"
        elif "cost" in name_lower or "saving" in name_lower:
            return "$"
        elif "time" in name_lower:
            return "ms"
        elif "tokens" in name_lower:
            return "tokens"
        elif "score" in name_lower:
            return "score"
        else:
            return "units"

    def calculate_kpi_scores(self, period: MetricPeriod = MetricPeriod.DAILY) -> Dict[str, Any]:
        """Calculate KPI scores and achievement rates"""
        with self.lock:
            # Get recent metrics
            recent_metrics = self._get_recent_metrics(period)

            kpi_results = {}
            overall_score = 0.0
            total_weight = 0.0

            for kpi_name, kpi_def in self.kpi_definitions.items():
                # Get current value for this KPI
                current_value = self._get_kpi_value(kpi_name, recent_metrics)

                if current_value is not None:
                    # Calculate achievement rate
                    achievement_rate = self._calculate_achievement_rate(
                        current_value, kpi_def.target_value, kpi_def.minimum_acceptable
                    )

                    # Calculate trend
                    trend = self._calculate_kpi_trend(kpi_name, period)

                    kpi_results[kpi_name] = {
                        "current_value": current_value,
                        "target_value": kpi_def.target_value,
                        "minimum_acceptable": kpi_def.minimum_acceptable,
                        "optimal_value": kpi_def.optimal_value,
                        "achievement_rate": achievement_rate,
                        "trend": trend,
                        "category": kpi_def.category.value,
                        "weight": kpi_def.weight,
                        "unit": kpi_def.unit,
                        "status": self._get_kpi_status(achievement_rate),
                    }

                    # Store in database
                    self._store_kpi_result(
                        kpi_name, kpi_def.category, current_value, kpi_def.target_value, achievement_rate, trend, period
                    )

                    # Add to overall score
                    overall_score += achievement_rate * kpi_def.weight
                    total_weight += kpi_def.weight

            # Calculate overall score
            overall_achievement = overall_score / total_weight if total_weight > 0 else 0.0

            return {
                "individual_kpis": kpi_results,
                "overall_score": overall_achievement,
                "overall_achievement_rate": overall_achievement,
                "total_kpis_tracked": len(kpi_results),
                "period": period.value,
                "calculated_at": datetime.now().isoformat(),
            }

    def _get_recent_metrics(self, period: MetricPeriod, limit: int = 100) -> List[AggregatedMetric]:
        """Get recent metrics for the specified period"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Calculate time threshold based on period
            time_threshold = datetime.now()
            if period == MetricPeriod.HOURLY:
                time_threshold -= timedelta(hours=24)
            elif period == MetricPeriod.DAILY:
                time_threshold -= timedelta(days=30)
            elif period == MetricPeriod.WEEKLY:
                time_threshold -= timedelta(weeks=12)
            elif period == MetricPeriod.MONTHLY:
                time_threshold -= timedelta(days=365)

            cursor.execute(
                """
                SELECT * FROM aggregated_metrics
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT ?
            """,
                (time_threshold.isoformat(), limit),
            )

            rows = cursor.fetchall()
            metrics = []

            for row in rows:
                metrics.append(
                    AggregatedMetric(
                        timestamp=datetime.fromisoformat(row[1]),
                        metric_name=row[2],
                        category=KpiCategory(row[3]),
                        period=MetricPeriod(row[4]),
                        value=row[5],
                        unit=row[6],
                        source_system=row[7],
                        metadata=json.loads(row[8]) if row[8] else {},
                    )
                )

            return metrics

    def _get_kpi_value(self, kpi_name: str, metrics: List[AggregatedMetric]) -> Optional[float]:
        """Get current value for a specific KPI from metrics"""
        # Find the most recent metric that matches this KPI
        for metric in metrics:
            if self._metric_matches_kpi(metric.metric_name, kpi_name):
                return metric.value

        return None

    def _metric_matches_kpi(self, metric_name: str, kpi_name: str) -> bool:
        """Check if a metric name matches a KPI"""
        metric_lower = metric_name.lower()
        kpi_lower = kpi_name.lower()

        # Direct match
        if metric_lower == kpi_lower:
            return True

        # Common variations
        metric_mappings = {
            "overall_savings_rate": "token_reduction_rate",
            "total_tokens_saved": "token_reduction_rate",
            "overall_cache_hit_rate": "cache_hit_rate",
            "total_cost_savings": "daily_cost_savings",
            "system_health_score": "system_availability",
            "error_rate": "error_rate",
        }

        return metric_mappings.get(metric_name) == kpi_lower or kpi_lower in metric_lower or metric_lower in kpi_lower

    def _calculate_achievement_rate(self, current_value: float, target_value: float, minimum_acceptable: float) -> float:
        """Calculate achievement rate for a KPI"""
        if current_value >= target_value:
            # Exceeded target - bonus points up to 150%
            excess = current_value - target_value
            max_excess = target_value * 0.5  # 50% bonus max
            bonus = min(excess / max_excess, 1.0) * 50  # Up to 50% bonus
            return min(150.0, 100.0 + bonus)
        elif current_value >= minimum_acceptable:
            # Between minimum and target - linear scaling
            range_size = target_value - minimum_acceptable
            if range_size > 0:
                progress = (current_value - minimum_acceptable) / range_size
                return 50.0 + (progress * 50.0)  # 50-100% range
            else:
                return 75.0
        else:
            # Below minimum - proportional penalty
            if minimum_acceptable > 0:
                return (current_value / minimum_acceptable) * 50.0  # 0-50% range
            else:
                return 0.0

    def _calculate_kpi_trend(self, kpi_name: str, period: MetricPeriod) -> str:
        """Calculate trend for a KPI"""
        # Get historical values for this KPI
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Calculate time threshold based on period
            time_threshold = datetime.now()
            if period == MetricPeriod.DAILY:
                time_threshold -= timedelta(days=7)  # Last 7 days
            elif period == MetricPeriod.WEEKLY:
                time_threshold -= timedelta(weeks=4)  # Last 4 weeks
            elif period == MetricPeriod.MONTHLY:
                time_threshold -= timedelta(days=90)  # Last 3 months

            cursor.execute(
                """
                SELECT value FROM kpi_results
                WHERE kpi_name = ? AND timestamp >= ?
                ORDER BY timestamp ASC
            """,
                (kpi_name, time_threshold.isoformat()),
            )

            rows = cursor.fetchall()

            if len(rows) < 2:
                return "insufficient_data"

            values = [row[0] for row in rows]

            # Simple trend calculation
            recent_avg = sum(values[-3:]) / min(3, len(values[-3:]))
            earlier_avg = sum(values[:3]) / min(3, len(values[:3]))

            if recent_avg > earlier_avg * 1.05:
                return "improving"
            elif recent_avg < earlier_avg * 0.95:
                return "declining"
            else:
                return "stable"

    def _get_kpi_status(self, achievement_rate: float) -> str:
        """Get status based on achievement rate"""
        if achievement_rate >= 100:
            return "excellent"
        elif achievement_rate >= 80:
            return "good"
        elif achievement_rate >= 60:
            return "fair"
        elif achievement_rate >= 40:
            return "poor"
        else:
            return "critical"

    def _store_kpi_result(
        self,
        kpi_name: str,
        category: KpiCategory,
        current_value: float,
        target_value: float,
        achievement_rate: float,
        trend: str,
        period: MetricPeriod,
    ):
        """Store KPI result in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO kpi_results
                (timestamp, kpi_name, category, value, target_value, achievement_rate, trend, period)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    datetime.now().isoformat(),
                    kpi_name,
                    category.value,
                    current_value,
                    target_value,
                    achievement_rate,
                    trend,
                    period.value,
                ),
            )

            conn.commit()

    def create_system_snapshot(self) -> Dict[str, Any]:
        """Create a comprehensive system snapshot"""
        # Collect all current metrics
        metrics = self.collect_metrics_from_all_systems()

        # Calculate KPI scores
        kpi_scores = self.calculate_kpi_scores()

        # Create snapshot
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "kpi_scores": kpi_scores,
            "system_health": {
                "overall_score": kpi_scores.get("overall_score", 0.0),
                "critical_issues": len(
                    [k for k, v in kpi_scores.get("individual_kpis", {}).items() if v.get("status") == "critical"]
                ),
                "improving_trends": len(
                    [k for k, v in kpi_scores.get("individual_kpis", {}).items() if v.get("trend") == "improving"]
                ),
                "declining_trends": len(
                    [k for k, v in kpi_scores.get("individual_kpis", {}).items() if v.get("trend") == "declining"]
                ),
            },
            "recommendations": self._generate_recommendations(kpi_scores),
            "next_actions": self._generate_next_actions(kpi_scores),
        }

        # Store snapshot
        self._store_system_snapshot(snapshot)

        return snapshot

    def _store_system_snapshot(self, snapshot: Dict[str, Any]):
        """Store system snapshot in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            aggregated = snapshot.get("metrics", {}).get("aggregated", {})
            kpi_scores = snapshot.get("kpi_scores", {})

            cursor.execute(
                """
                INSERT INTO system_snapshots
                (timestamp, total_tokens_saved, total_cost_savings, overall_effectiveness,
                 cache_hit_rate, compression_ratio, user_satisfaction, system_health_score, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    snapshot["timestamp"],
                    aggregated.get("total_tokens_saved", 0),
                    aggregated.get("total_cost_savings", 0.0),
                    kpi_scores.get("overall_achievement_rate", 0.0),
                    aggregated.get("overall_cache_hit_rate", 0.0),
                    aggregated.get("overall_compression_ratio", 0.0),
                    0.0,  # User satisfaction - would need integration
                    kpi_scores.get("overall_score", 0.0),
                    json.dumps(snapshot),
                ),
            )

            conn.commit()

    def _generate_recommendations(self, kpi_scores: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on KPI scores"""
        recommendations = []
        individual_kpis = kpi_scores.get("individual_kpis", {})

        # Check critical KPIs
        for kpi_name, kpi_data in individual_kpis.items():
            if kpi_data.get("status") == "critical":
                if "token" in kpi_name.lower():
                    recommendations.append("URGENT: Token reduction is critically low. Review progressive loading settings.")
                elif "cache" in kpi_name.lower():
                    recommendations.append("URGENT: Cache hit rate is too low. Increase cache size or review cache policies.")
                elif "cost" in kpi_name.lower():
                    recommendations.append("URGENT: Cost savings are below target. Check budget constraints.")

        # Check declining trends
        for kpi_name, kpi_data in individual_kpis.items():
            if kpi_data.get("trend") == "declining":
                recommendations.append(f"[WARN] {kpi_name.replace('_', ' ').title()} is declining. Investigate root cause.")

        # Overall recommendations
        overall_score = kpi_scores.get("overall_score", 0)
        if overall_score < 60:
            recommendations.append("CRITICAL: Overall system performance is poor. Immediate attention required.")
        elif overall_score < 80:
            recommendations.append("System performance needs improvement. Focus on underperforming KPIs.")

        if not recommendations:
            recommendations.append("[OK] All systems performing well. Continue monitoring.")

        return recommendations

    def _generate_next_actions(self, kpi_scores: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific next actions based on KPI scores"""
        actions = []
        individual_kpis = kpi_scores.get("individual_kpis", {})

        # Token reduction actions
        token_kpi = individual_kpis.get("token_reduction_rate", {})
        if token_kpi.get("achievement_rate", 0) < 80:
            actions.append(
                {
                    "action": "Optimize progressive loading tiers",
                    "priority": "high",
                    "expected_impact": "15-25% token reduction",
                    "effort": "medium",
                    "timeline": "1-2 days",
                }
            )

        # Cache optimization actions
        cache_kpi = individual_kpis.get("cache_hit_rate", {})
        if cache_kpi.get("achievement_rate", 0) < 80:
            actions.append(
                {
                    "action": "Increase cache size and tune policies",
                    "priority": "high",
                    "expected_impact": "10-20% performance improvement",
                    "effort": "low",
                    "timeline": "2-4 hours",
                }
            )

        # Budget management actions
        if "budget_utilization" in individual_kpis:
            budget_kpi = individual_kpis["budget_utilization"]
            if budget_kpi.get("achievement_rate", 0) < 70:
                actions.append(
                    {
                        "action": "Review and adjust budget constraints",
                        "priority": "medium",
                        "expected_impact": "5-15% cost optimization",
                        "effort": "medium",
                        "timeline": "1 day",
                    }
                )

        return actions

    def get_kpi_dashboard_data(self, period: MetricPeriod = MetricPeriod.DAILY) -> Dict[str, Any]:
        """Get comprehensive KPI dashboard data"""
        # Calculate current KPI scores
        kpi_scores = self.calculate_kpi_scores(period)

        # Get historical trends
        historical_data = self._get_historical_kpi_data(period)

        # Get system snapshot
        snapshot = self.create_system_snapshot()

        return {
            "current_scores": kpi_scores,
            "historical_trends": historical_data,
            "system_snapshot": snapshot,
            "period": period.value,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "overall_score": kpi_scores.get("overall_score", 0),
                "critical_issues": len(
                    [k for k, v in kpi_scores.get("individual_kpis", {}).items() if v.get("status") == "critical"]
                ),
                "improving_trends": len(
                    [k for k, v in kpi_scores.get("individual_kpis", {}).items() if v.get("trend") == "improving"]
                ),
                "total_recommendations": len(snapshot.get("recommendations", [])),
                "total_actions": len(snapshot.get("next_actions", [])),
            },
        }

    def _get_historical_kpi_data(self, period: MetricPeriod, days: int = 30) -> Dict[str, List[Dict[str, Any]]]:
        """Get historical KPI data for trend analysis"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Calculate time threshold
            time_threshold = datetime.now() - timedelta(days=days)

            cursor.execute(
                """
                SELECT kpi_name, timestamp, value, achievement_rate, trend
                FROM kpi_results
                WHERE timestamp >= ? AND period = ?
                ORDER BY timestamp ASC
            """,
                (time_threshold.isoformat(), period.value),
            )

            rows = cursor.fetchall()

            # Organize by KPI name
            historical_data = {}

            for row in rows:
                kpi_name, timestamp, value, achievement_rate, trend = row

                if kpi_name not in historical_data:
                    historical_data[kpi_name] = []

                historical_data[kpi_name].append(
                    {"timestamp": timestamp, "value": value, "achievement_rate": achievement_rate, "trend": trend}
                )

            return historical_data

    def generate_performance_report(self, period: MetricPeriod = MetricPeriod.DAILY) -> str:
        """Generate comprehensive performance report"""
        dashboard_data = self.get_kpi_dashboard_data(period)

        report = f"""
# Token Optimization Performance Report
**Period**: {period.value.title()}
**Generated**: {dashboard_data['generated_at'][:19].replace('T', ' ')}

## Executive Summary

**Overall Performance Score**: {dashboard_data['summary']['overall_score']:.1f}/100

### Key Metrics
- **Critical Issues**: {dashboard_data['summary']['critical_issues']}
- **Improving Trends**: {dashboard_data['summary']['improving_trends']}
- **Active Recommendations**: {dashboard_data['summary']['total_recommendations']}

## KPI Performance Analysis

        individual_kpis = dashboard_data["current_scores"]["individual_kpis"]

        for kpi_name, kpi_data in individual_kpis.items():
            status_emoji = {"excellent": "🟢", "good": "🟡", "fair": "🟠", "poor": "🔴", "critical": "🚨"}.get(
                kpi_data.get("status"), "⚪"
            )

            trend_emoji = {"improving": "[TREND]", "declining": "📉", "stable": "[RIGHT]"}.get(kpi_data.get("trend"), "❓")

            report += f"""
### {kpi_name.replace('_', ' ').title()} {status_emoji} {trend_emoji}
- **Current Value**: {kpi_data['current_value']:.2f} {kpi_data['unit']}
- **Target**: {kpi_data['target_value']:.2f} {kpi_data['unit']}
- **Achievement Rate**: {kpi_data['achievement_rate']:.1f}%
- **Status**: {kpi_data.get('status', 'unknown').title()}
- **Trend**: {kpi_data.get('trend', 'unknown').title()}

        # Add recommendations
        recommendations = dashboard_data["system_snapshot"]["recommendations"]
        if recommendations:
            report += "## Recommendations\n\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"{i}. {rec}\n"

        # Add next actions
        actions = dashboard_data["system_snapshot"]["next_actions"]
        if actions:
            report += "\n## Next Actions\n\n"
            for i, action in enumerate(actions, 1):
                report += f"""
### {action['action']}
- **Priority**: {action['priority'].title()}
- **Expected Impact**: {action['expected_impact']}
- **Effort**: {action['effort'].title()}
- **Timeline**: {action['timeline']}

        return report

    def export_metrics_json(self, period: MetricPeriod = MetricPeriod.DAILY) -> str:
        """Export all metrics as JSON"""
        dashboard_data = self.get_kpi_dashboard_data(period)
        return json.dumps(dashboard_data, indent=2, default=str)

    def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old metrics data"""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()

                # Clean up old aggregated metrics
                cursor.execute("DELETE FROM aggregated_metrics WHERE timestamp < ?", (cutoff_date,))
                metrics_deleted = cursor.rowcount

                # Clean up old KPI results
                cursor.execute("DELETE FROM kpi_results WHERE timestamp < ?", (cutoff_date,))
                kpis_deleted = cursor.rowcount

                # Clean up old system snapshots (keep fewer of these)
                snapshot_cutoff = (datetime.now() - timedelta(days=30)).isoformat()
                cursor.execute("DELETE FROM system_snapshots WHERE timestamp < ?", (snapshot_cutoff,))
                snapshots_deleted = cursor.rowcount

                conn.commit()

                self.logger.info(f"Cleaned up {metrics_deleted} metrics, {kpis_deleted} KPIs, {snapshots_deleted} snapshots")


def main():
    """Demonstrate the unified metrics aggregator"""
    print("🔗 Unified Metrics Aggregator Demo")
    print("=" * 50)

    # Initialize aggregator
    aggregator = UnifiedMetricsAggregator()

    # Collect metrics from all systems
    print("\n[DATA] Collecting metrics from all systems...")
    metrics = aggregator.collect_metrics_from_all_systems()

    print(f"[OK] Collected metrics from {len(metrics)} systems")

    # Store aggregated metrics
    print("\n[SAVE] Storing aggregated metrics...")
    aggregator.store_aggregated_metrics(metrics.get("aggregated", {}))

    # Calculate KPI scores
    print("\n[TARGET] Calculating KPI scores...")
    kpi_scores = aggregator.calculate_kpi_scores()

    print(f"[TREND] Overall Score: {kpi_scores['overall_score']:.1f}/100")
    print(f"[DATA] KPIs Tracked: {kpi_scores['total_kpis_tracked']}")

    # Create system snapshot
    print("\n📸 Creating system snapshot...")
    snapshot = aggregator.create_system_snapshot()

    print(f"[OK] System health score: {snapshot['system_health']['overall_score']:.1f}/100")
    print(f"[WARN] Critical issues: {snapshot['system_health']['critical_issues']}")

    # Generate dashboard data
    print("\n[LIST] Generating dashboard data...")
    dashboard_data = aggregator.get_kpi_dashboard_data()

    print(f"[TREND] Improving trends: {dashboard_data['summary']['improving_trends']}")
    print(f"[INFO] Recommendations: {dashboard_data['summary']['total_recommendations']}")

    # Generate performance report
    print("\n📄 Generating performance report...")
    report = aggregator.generate_performance_report()

    # Save report
    report_file = Path("performance_report.md")
    with open(report_file, "w") as f:
        f.write(report)

    print(f"[OK] Performance report saved to: {report_file.absolute()}")

    # Export metrics as JSON
    print("\n📤 Exporting metrics as JSON...")
    json_data = aggregator.export_metrics_json()

    json_file = Path("metrics_export.json")
    with open(json_file, "w") as f:
        f.write(json_data)

    print(f"[OK] Metrics exported to: {json_file.absolute()}")

    # Show summary
    print("\n[DATA] Summary:")
    print(f"   Overall Score: {kpi_scores['overall_score']:.1f}/100")
    print(f"   Tokens Saved: {metrics.get('aggregated', {}).get('total_tokens_saved', 0):,}")
    print(f"   Cost Savings: ${metrics.get('aggregated', {}).get('total_cost_savings', 0):.2f}")
    print(f"   Cache Hit Rate: {metrics.get('aggregated', {}).get('overall_cache_hit_rate', 0):.1f}%")

    print("\n[PARTY] Unified Metrics Aggregator demo completed!")


if __name__ == "__main__":
    main()
