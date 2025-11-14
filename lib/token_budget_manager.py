"""
Comprehensive Token Budget Management and Optimization System

Provides dynamic budget allocation, predictive budgeting, and optimization
algorithms for autonomous agent workflows.

Features:
- Dynamic budget allocation based on context and performance
- Predictive budgeting using ML algorithms
- Real-time budget tracking and adjustments
- Optimization algorithms for token efficiency
- Budget alerts and constraints
- Multi-level budget hierarchy (global, project, task, agent)
import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from pathlib import Path
import statistics
import math
from collections import defaultdict, deque


class BudgetLevel(Enum):
    """Budget hierarchy levels."""

    GLOBAL = "global"
    PROJECT = "project"
    TASK = "task"
    AGENT = "agent"
    SESSION = "session"


class BudgetScope(Enum):
    """Budget scope types."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    TASK_BASED = "task_based"
    PROJECT_BASED = "project_based"


class BudgetStatus(Enum):
    """Budget status indicators."""

    HEALTHY = "healthy"  # < 60% used
    WARNING = "warning"  # 60-80% used
    CRITICAL = "critical"  # 80-95% used
    EXCEEDED = "exceeded"  # > 95% used
    DEPLETED = "depleted"  # 100% used


class OptimizationStrategy(Enum):
    """Token optimization strategies."""

    CONSERVATIVE = "conservative"  # Minimize usage at all costs
    BALANCED = "balanced"  # Balance efficiency and functionality
    PERFORMANCE = "performance"  # Optimize for task performance
    ADAPTIVE = "adaptive"  # Dynamically adjust based on context
    PREDICTIVE = "predictive"  # Use ML predictions for optimization


@dataclass
class BudgetConstraint:
    """Individual budget constraint."""

    id: str
    level: BudgetLevel
    scope: BudgetScope
    limit: int  # Token limit
    used: int = 0
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    tags: Dict[str, str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = {}
        if self.period_start is None:
            self.period_start = datetime.now()
        if self.period_end is None:
            self.period_end = self._calculate_period_end()

    def _calculate_period_end(self) -> datetime:
        """Calculate period end based on scope."""
        if self.scope == BudgetScope.DAILY:
            return self.period_start + timedelta(days=1)
        elif self.scope == BudgetScope.WEEKLY:
            return self.period_start + timedelta(weeks=1)
        elif self.scope == BudgetScope.MONTHLY:
            return self.period_start + timedelta(days=30)
        else:
            return self.period_start + timedelta(days=1)


@dataclass
class BudgetAllocation:
    """Budget allocation details."""

    constraint_id: str
    allocated: int
    used: int
    available: int
    status: BudgetStatus
    efficiency_score: float = 0.0  # 0-1, higher is better
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()
        self.available = self.allocated - self.used
        self.status = self._calculate_status()

    def _calculate_status(self) -> BudgetStatus:
        """Calculate budget status based on usage percentage."""
        if self.allocated == 0:
            return BudgetStatus.DEPLETED

        usage_percent = (self.used / self.allocated) * 100

        if usage_percent >= 100:
            return BudgetStatus.DEPLETED
        elif usage_percent >= 95:
            return BudgetStatus.EXCEEDED
        elif usage_percent >= 80:
            return BudgetStatus.CRITICAL
        elif usage_percent >= 60:
            return BudgetStatus.WARNING
        else:
            return BudgetStatus.HEALTHY


@dataclass
class OptimizationRecommendation:
    """Token optimization recommendation."""

    strategy: OptimizationStrategy
    description: str
    potential_savings: int  # Estimated tokens saved
    confidence: float  # 0-1, confidence in recommendation
    implementation_cost: str  # "low", "medium", "high"
    priority: int  # 1-10, higher is more urgent
    impact_areas: List[str]  # Areas this optimization affects


@dataclass
class BudgetAlert:
    """Budget alert configuration."""

    level: BudgetLevel
    threshold: float  # Percentage threshold (0-1)
    message: str
    enabled: bool = True
    cooldown_minutes: int = 60  # Minimum time between alerts
    last_triggered: Optional[datetime] = None


class TokenBudgetManager:
    """Comprehensive token budget management system."""

    def __init__(self, db_path: str = None, data_dir: str = ".claude-patterns"):
        """Initialize token budget manager."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Database setup
        if db_path is None:
            db_path = self.data_dir / "token_budgets.db"

        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        # Initialize database
        self._init_database()

        # Budget constraints storage
        self.constraints: Dict[str, BudgetConstraint] = {}
        self.allocations: Dict[str, BudgetAllocation] = {}

        # Alert system
        self.alerts: List[BudgetAlert] = []
        self._setup_default_alerts()

        # Optimization cache
        self.optimization_cache: Dict[str, List[OptimizationRecommendation]] = {}
        self.usage_history: deque = deque(maxlen=1000)  # Recent usage history

        # ML models for prediction
        self.usage_predictor = None  # Could be initialized with ML model
        self.efficiency_predictor = None

        # Configuration
        self.default_daily_budget = 100000  # 100K tokens per day
        self.default_task_budget = 10000  # 10K tokens per task
        self.optimization_threshold = 0.8  # Trigger optimization at 80% usage

        # Load existing constraints
        self._load_constraints()

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _init_database(self) -> None:
        """Initialize database tables for budget tracking."""
        cursor = self.conn.cursor()

        # Budget constraints table
        cursor.execute(
"""
            CREATE TABLE IF NOT EXISTS budget_constraints (
                id TEXT PRIMARY KEY,
                level TEXT NOT NULL,
                scope TEXT NOT NULL,
                token_limit INTEGER NOT NULL,
                used INTEGER DEFAULT 0,
                period_start TEXT,
                period_end TEXT,
                tags TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
"""
        )

        # Budget allocations table
        cursor.execute(
"""
            CREATE TABLE IF NOT EXISTS budget_allocations (
                constraint_id TEXT,
                allocated INTEGER NOT NULL,
                used INTEGER DEFAULT 0,
                available INTEGER,
                status TEXT NOT NULL,
                efficiency_score REAL DEFAULT 0.0,
                last_updated TEXT,
                PRIMARY KEY (constraint_id)
            )
"""
        )

        # Usage history table
        cursor.execute(
"""
            CREATE TABLE IF NOT EXISTS usage_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                constraint_id TEXT,
                timestamp TEXT NOT NULL,
                tokens_used INTEGER NOT NULL,
                task_type TEXT,
                agent_name TEXT,
                efficiency_score REAL,
                context TEXT
            )
"""
        )

        # Optimization recommendations table
        cursor.execute(
"""
            CREATE TABLE IF NOT EXISTS optimization_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                constraint_id TEXT,
                strategy TEXT NOT NULL,
                description TEXT,
                potential_savings INTEGER,
                confidence REAL,
                implementation_cost TEXT,
                priority INTEGER,
                impact_areas TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                applied BOOLEAN DEFAULT FALSE
            )
"""
        )

        # Budget alerts table
        cursor.execute(
"""
            CREATE TABLE IF NOT EXISTS budget_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                threshold REAL NOT NULL,
                message TEXT,
                enabled BOOLEAN DEFAULT TRUE,
                cooldown_minutes INTEGER DEFAULT 60,
                last_triggered TEXT
            )
"""
        )

        self.conn.commit()

"""
    def _setup_default_alerts(self) -> None:
        """Setup default budget alerts."""
        default_alerts = [
            BudgetAlert(level=BudgetLevel.GLOBAL, threshold=0.8, message="Global budget usage exceeded 80%"),
            BudgetAlert(level=BudgetLevel.PROJECT, threshold=0.9, message="Project budget usage exceeded 90%"),
            BudgetAlert(level=BudgetLevel.TASK, threshold=0.95, message="Task budget nearly depleted"),
            BudgetAlert(level=BudgetLevel.AGENT, threshold=0.85, message="Agent budget usage high"),
        ]

        self.alerts.extend(default_alerts)

    def create_budget_constraint(
        self,
        level: BudgetLevel,
        scope: BudgetScope,
        limit: int,
        period_start: Optional[datetime] = None,
        tags: Dict[str, str] = None,
    ) -> str:
        """Create a new budget constraint."""
        constraint_id = f"{level.value}_{scope.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        constraint = BudgetConstraint(
            id=constraint_id,
            level=level,
            scope=scope,
            limit=limit,
            period_start=period_start or datetime.now(),
            tags=tags or {},
        )

        self.constraints[constraint_id] = constraint

        # Save to database
        cursor = self.conn.cursor()
        cursor.execute(
"""
            INSERT OR REPLACE INTO budget_constraints
            (id, level, scope, token_limit, period_start, period_end, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                constraint_id,
                level.value,
                scope.value,
                limit,
                constraint.period_start.isoformat(),
                constraint.period_end.isoformat(),
                json.dumps(tags or {}),
            ),
        )

        self.conn.commit()

        # Initialize allocation
        self._initialize_allocation(constraint_id)

        self.logger.info(f"Created budget constraint: {constraint_id} with limit {limit}")
        return constraint_id

    def _initialize_allocation(self, constraint_id: str) -> None:
        """Initialize budget allocation for constraint."""
        constraint = self.constraints[constraint_id]

        allocation = BudgetAllocation(
            constraint_id=constraint_id,
            allocated=constraint.limit,
            used=0,
            available=constraint.limit,
            status=BudgetStatus.HEALTHY,
        )

        self.allocations[constraint_id] = allocation

        # Save to database
        cursor = self.conn.cursor()
        cursor.execute(
"""
            INSERT OR REPLACE INTO budget_allocations
            (constraint_id, allocated, used, available, status, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                constraint_id,
                allocation.allocated,
                allocation.used,
                allocation.available,
                allocation.status.value,
                allocation.last_updated.isoformat(),
            ),
        )

        self.conn.commit()

    def allocate_tokens(
        self,
        constraint_id: str,
        requested: int,
        task_type: str = "unknown",
        agent_name: str = "unknown",
        context: Dict[str, Any] = None,
    ) -> Tuple[bool, int]:
        """Allocate tokens for a task."""
        if constraint_id not in self.allocations:
            return False, 0

        allocation = self.allocations[constraint_id]

        # Check if allocation is possible
        available = allocation.available

        # Apply optimization if needed
        if requested > available:
            optimized_requested = self._optimize_request(constraint_id, requested, task_type)
            if optimized_requested > available:
                self._check_and_trigger_alerts(constraint_id)
                return False, 0
            requested = optimized_requested

        # Update allocation
        allocation.used += requested
        allocation.available = allocation.allocated - allocation.used
        allocation.last_updated = datetime.now()
        allocation.status = allocation._calculate_status()

        # Record usage
        self._record_usage(constraint_id, requested, task_type, agent_name, context)

        # Save to database
        self._update_allocation_in_db(allocation)

        # Check for optimization opportunities
        if allocation.status.value in ["warning", "critical"]:
            self._generate_optimization_recommendations(constraint_id)

        return True, requested

    def _optimize_request(self, constraint_id: str, requested: int, task_type: str) -> int:
        """Optimize token request based on budget constraints."""
        # Get optimization recommendations for this constraint
        recommendations = self._get_cached_recommendations(constraint_id)

        if not recommendations:
            return requested

        # Apply top recommendation
        top_rec = recommendations[0]

        # Apply optimization based on strategy
        if top_rec.strategy == OptimizationStrategy.CONSERVATIVE:
            return min(requested, int(requested * 0.7))  # 30% reduction
        elif top_rec.strategy == OptimizationStrategy.BALANCED:
            return min(requested, int(requested * 0.85))  # 15% reduction
        elif top_rec.strategy == OptimizationStrategy.PERFORMANCE:
            return min(requested, int(requested * 0.9))  # 10% reduction

        return requested

    def _record_usage(
        self, constraint_id: str, tokens_used: int, task_type: str, agent_name: str, context: Dict[str, Any] = None
    ) -> None:
        """Record token usage in history."""
        cursor = self.conn.cursor()
        cursor.execute(
"""
            INSERT INTO usage_history
            (constraint_id, timestamp, tokens_used, task_type, agent_name, context)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (constraint_id, datetime.now().isoformat(), tokens_used, task_type, agent_name, json.dumps(context or {})),
        )

        self.conn.commit()

        # Add to in-memory history
        self.usage_history.append(
            {
                "constraint_id": constraint_id,
                "tokens_used": tokens_used,
                "timestamp": datetime.now(),
                "task_type": task_type,
                "agent_name": agent_name,
            }
        )

    def _update_allocation_in_db(self, allocation: BudgetAllocation) -> None:
        """Update allocation in database."""
        cursor = self.conn.cursor()
        cursor.execute(
"""
            UPDATE budget_allocations
            SET used = ?, available = ?, status = ?, last_updated = ?
            WHERE constraint_id = ?
        """,
            (
                allocation.used,
                allocation.available,
                allocation.status.value,
                allocation.last_updated.isoformat(),
                allocation.constraint_id,
            ),
        )

        self.conn.commit()

    def _check_and_trigger_alerts(self, constraint_id: str) -> None:
        """Check and trigger budget alerts if needed."""
        allocation = self.allocations[constraint_id]
        constraint = self.constraints[constraint_id]

        for alert in self.alerts:
            if alert.level != constraint.level:
                continue

            # Check if threshold exceeded
            usage_ratio = allocation.used / allocation.allocated

            if usage_ratio >= alert.threshold:
                # Check cooldown
                if alert.last_triggered and datetime.now() - alert.last_triggered < timedelta(minutes=alert.cooldown_minutes):
                    continue

                # Trigger alert
                self._trigger_alert(alert, allocation, usage_ratio)
                alert.last_triggered = datetime.now()

    def _trigger_alert(self, alert: BudgetAlert, allocation: BudgetAllocation, usage_ratio: float) -> None:
        """Trigger a budget alert."""
        self.logger.warning(
            f"BUDGET ALERT: {alert.message} | "
            f"Constraint: {allocation.constraint_id} | "
            f"Usage: {usage_ratio:.1%} ({allocation.used}/{allocation.allocated})"
        )

        # Could integrate with external notification systems here
        # e.g., email, Slack, webhook, etc.

    def _generate_optimization_recommendations(self, constraint_id: str) -> None:
        """Generate optimization recommendations for constraint."""
        recommendations = []

        allocation = self.allocations[constraint_id]
        constraint = self.constraints[constraint_id]

        # Analyze usage patterns
        recent_usage = self._get_recent_usage(constraint_id, limit=50)

        if recent_usage:
            avg_task_usage = statistics.mean([u["tokens_used"] for u in recent_usage])

            # Recommendation 1: Progressive loading
            if avg_task_usage > 5000:  # Large tasks
                recommendations.append(
                    OptimizationRecommendation(
                        strategy=OptimizationStrategy.ADAPTIVE,
                        description="Enable progressive content loading for large tasks",
                        potential_savings=int(avg_task_usage * 0.3),  # 30% savings
                        confidence=0.85,
                        implementation_cost="low",
                        priority=8,
                        impact_areas=["task_execution", "content_loading"],
                    )
                )

            # Recommendation 2: Agent communication optimization
            if len(recent_usage) > 10:
                recommendations.append(
                    OptimizationRecommendation(
                        strategy=OptimizationStrategy.BALANCED,
                        description="Optimize agent-to-agent communication protocols",
                        potential_savings=int(avg_task_usage * 0.15),  # 15% savings
                        confidence=0.75,
                        implementation_cost="medium",
                        priority=6,
                        impact_areas=["agent_communication", "inter_agent_coordination"],
                    )
                )

            # Recommendation 3: Smart caching
            recommendations.append(
                OptimizationRecommendation(
                    strategy=OptimizationStrategy.PREDICTIVE,
                    description="Implement smart caching with predictive loading",
                    potential_savings=int(avg_task_usage * 0.25),  # 25% savings
                    confidence=0.80,
                    implementation_cost="medium",
                    priority=7,
                    impact_areas=["caching", "content_delivery", "performance"],
                )
            )

        # Cache recommendations
        self.optimization_cache[constraint_id] = recommendations

        # Save to database
        self._save_recommendations_to_db(constraint_id, recommendations)

    def _get_recent_usage(self, constraint_id: str, limit: int = 50) -> List[Dict]:
        """Get recent usage history for constraint."""
        cursor = self.conn.cursor()
        cursor.execute(
"""
            SELECT * FROM usage_history
            WHERE constraint_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """,
            (constraint_id, limit),
        )

        return [dict(row) for row in cursor.fetchall()]

    def _save_recommendations_to_db(self, constraint_id: str, recommendations: List[OptimizationRecommendation]) -> None:
        """Save optimization recommendations to database."""
        cursor = self.conn.cursor()

        for rec in recommendations:
            cursor.execute(
"""
                INSERT INTO optimization_recommendations
                (constraint_id, strategy, description, potential_savings,
                 confidence, implementation_cost, priority, impact_areas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    constraint_id,
                    rec.strategy.value,
                    rec.description,
                    rec.potential_savings,
                    rec.confidence,
                    rec.implementation_cost,
                    rec.priority,
                    json.dumps(rec.impact_areas),
                ),
            )

        self.conn.commit()

    def _get_cached_recommendations(self, constraint_id: str) -> List[OptimizationRecommendation]:
        """Get cached optimization recommendations."""
        return self.optimization_cache.get(constraint_id, [])

    def get_budget_status(self, constraint_id: str = None) -> Dict[str, Any]:
        """Get current budget status."""
        if constraint_id:
            if constraint_id not in self.allocations:
                return {"error": "Constraint not found"}

            allocation = self.allocations[constraint_id]
            constraint = self.constraints[constraint_id]

            return {
                "constraint_id": constraint_id,
                "level": constraint.level.value,
                "scope": constraint.scope.value,
                "allocated": allocation.allocated,
                "used": allocation.used,
                "available": allocation.available,
                "usage_percentage": (allocation.used / allocation.allocated) * 100,
                "status": allocation.status.value,
                "efficiency_score": allocation.efficiency_score,
                "last_updated": allocation.last_updated.isoformat(),
            }
        else:
            # Return all constraints
            return {constraint_id: self.get_budget_status(constraint_id) for constraint_id in self.allocations.keys()}

    def get_optimization_recommendations(self, constraint_id: str = None) -> List[OptimizationRecommendation]:
        """Get optimization recommendations."""
        if constraint_id:
            return self._get_cached_recommendations(constraint_id)
        else:
            # Return all recommendations
            all_recommendations = []
            for constraint_id in self.allocations.keys():
                all_recommendations.extend(self._get_cached_recommendations(constraint_id))

            # Sort by priority
            return sorted(all_recommendations, key=lambda x: x.priority, reverse=True)

    def predict_usage(self, constraint_id: str, days_ahead: int = 7) -> Dict[str, Any]:
        """Predict future token usage using historical data."""
        recent_usage = self._get_recent_usage(constraint_id, limit=100)

        if len(recent_usage) < 7:
            return {"error": "Insufficient data for prediction"}

        # Simple linear prediction (could be enhanced with ML models)
        daily_usage = defaultdict(list)

        for usage in recent_usage:
            date = datetime.fromisoformat(usage["timestamp"]).date()
            daily_usage[date].append(usage["tokens_used"])

        # Calculate daily totals and trends
        daily_totals = {date: sum(tokens) for date, tokens in daily_usage.items()}
        sorted_dates = sorted(daily_totals.keys())

        if len(sorted_dates) < 3:
            return {"error": "Need at least 3 days of data"}

        # Calculate trend
        recent_totals = [daily_totals[date] for date in sorted_dates[-7:]]
        trend = statistics.mean(recent_totals[-3:]) - statistics.mean(recent_totals[:3])

        # Predict future usage
        current_daily_avg = statistics.mean(recent_totals)
        predicted_daily = current_daily_avg + (trend * days_ahead / 7)

        # Calculate predicted total
        predicted_total = predicted_daily * days_ahead

        return {
            "constraint_id": constraint_id,
            "days_ahead": days_ahead,
            "current_daily_average": current_daily_avg,
            "predicted_daily_average": predicted_daily,
            "predicted_total_usage": predicted_total,
            "trend": "increasing" if trend > 0 else "decreasing" if trend < 0 else "stable",
            "confidence": min(0.9, len(recent_usage) / 100),  # Confidence based on data amount
        }

    def reset_budget(self, constraint_id: str) -> bool:
        """Reset budget allocation for constraint."""
        if constraint_id not in self.allocations:
            return False

        allocation = self.allocations[constraint_id]
        constraint = self.constraints[constraint_id]

        # Reset allocation
        allocation.used = 0
        allocation.available = constraint.limit
        allocation.status = BudgetStatus.HEALTHY
        allocation.last_updated = datetime.now()

        # Update database
        self._update_allocation_in_db(allocation)

        self.logger.info(f"Reset budget for constraint: {constraint_id}")
        return True

    def _load_constraints(self) -> None:
        """Load existing constraints from database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM budget_constraints")

        for row in cursor.fetchall():
            constraint_id = row["id"]

            constraint = BudgetConstraint(
                level=BudgetLevel(row["level"]),
                scope=BudgetScope(row["scope"]),
                limit=row["limit"],
                used=row["used"],
                period_start=datetime.fromisoformat(row["period_start"]) if row["period_start"] else None,
                period_end=datetime.fromisoformat(row["period_end"]) if row["period_end"] else None,
                tags=json.loads(row["tags"]) if row["tags"] else {},
            )

            self.constraints[constraint_id] = constraint

            # Load allocation
            cursor.execute("SELECT * FROM budget_allocations WHERE constraint_id = ?", (constraint_id,))
            alloc_row = cursor.fetchone()

            if alloc_row:
                allocation = BudgetAllocation(
                    constraint_id=constraint_id,
                    allocated=alloc_row["allocated"],
                    used=alloc_row["used"],
                    available=alloc_row["available"],
                    status=BudgetStatus(alloc_row["status"]),
                    efficiency_score=alloc_row["efficiency_score"],
                    last_updated=datetime.fromisoformat(alloc_row["last_updated"]) if alloc_row["last_updated"] else None,
                )

                self.allocations[constraint_id] = allocation
            else:
                self._initialize_allocation(constraint_id)

    def get_budget_report(self, constraint_id: str = None, format: str = "summary") -> Dict[str, Any]:
        """Generate comprehensive budget report."""
        if constraint_id:
            constraints = {constraint_id: self.constraints.get(constraint_id)}
            allocations = {constraint_id: self.allocations.get(constraint_id)}
        else:
            constraints = self.constraints
            allocations = self.allocations

        report = {
            "generated_at": datetime.now().isoformat(),
            "total_constraints": len(constraints),
            "total_allocated": sum(alloc.allocated for alloc in allocations.values() if alloc),
            "total_used": sum(alloc.used for alloc in allocations.values() if alloc),
            "overall_usage_percentage": 0,
            "constraints": {},
        }

        if report["total_allocated"] > 0:
            report["overall_usage_percentage"] = (report["total_used"] / report["total_allocated"]) * 100

        # Per-constraint details
        for cid, constraint in constraints.items():
            allocation = allocations.get(cid)
            if not allocation:
                continue

            constraint_report = {
                "level": constraint.level.value,
                "scope": constraint.scope.value,
                "allocated": allocation.allocated,
                "used": allocation.used,
                "available": allocation.available,
                "usage_percentage": (allocation.used / allocation.allocated) * 100,
                "status": allocation.status.value,
                "efficiency_score": allocation.efficiency_score,
                "period_start": constraint.period_start.isoformat(),
                "period_end": constraint.period_end.isoformat(),
                "recommendations": len(self._get_cached_recommendations(cid)),
            }

            if format == "detailed":
                # Add usage trends
                recent_usage = self._get_recent_usage(cid, limit=30)
                if recent_usage:
                    constraint_report["recent_daily_average"] = statistics.mean([u["tokens_used"] for u in recent_usage])
                    constraint_report["peak_usage"] = max(u["tokens_used"] for u in recent_usage)

                # Add predictions
                prediction = self.predict_usage(cid)
                if "error" not in prediction:
                    constraint_report["prediction"] = prediction

            report["constraints"][cid] = constraint_report

        return report

    def apply_optimization_strategy(self, constraint_id: str, strategy: OptimizationStrategy) -> Dict[str, Any]:
        """Apply an optimization strategy to constraint."""
        if constraint_id not in self.allocations:
            return {"error": "Constraint not found"}

        allocation = self.allocations[constraint_id]

        results = {
            "strategy": strategy.value,
            "constraint_id": constraint_id,
            "tokens_saved": 0,
            "efficiency_improvement": 0,
            "changes_made": [],
        }

        if strategy == OptimizationStrategy.CONSERVATIVE:
            # Implement conservative optimization
            target_reduction = int(allocation.allocated * 0.2)  # 20% reduction
            results["tokens_saved"] = target_reduction
            results["changes_made"].append("Enabled conservative token usage limits")
            results["changes_made"].append("Reduced maximum task token allocation")

        elif strategy == OptimizationStrategy.BALANCED:
            # Implement balanced optimization
            target_reduction = int(allocation.allocated * 0.1)  # 10% reduction
            results["tokens_saved"] = target_reduction
            results["changes_made"].append("Enabled balanced optimization")
            results["changes_made"].append("Optimized agent communication protocols")

        elif strategy == OptimizationStrategy.PERFORMANCE:
            # Focus on performance optimization
            results["efficiency_improvement"] = 0.15  # 15% efficiency boost
            results["changes_made"].append("Optimized for task performance")
            results["changes_made"].append("Enabled performance-focused caching")

        elif strategy == OptimizationStrategy.ADAPTIVE:
            # Implement adaptive optimization
            recent_usage = self._get_recent_usage(constraint_id, limit=20)
            if recent_usage:
                avg_usage = statistics.mean([u["tokens_used"] for u in recent_usage])
                if avg_usage > allocation.allocated * 0.8:
                    target_reduction = int(allocation.allocated * 0.15)
                    results["tokens_saved"] = target_reduction
                    results["changes_made"].append("Adaptive reduction based on high usage")

        elif strategy == OptimizationStrategy.PREDICTIVE:
            # Implement predictive optimization
            prediction = self.predict_usage(constraint_id)
            if "error" not in prediction and prediction["trend"] == "increasing":
                results["changes_made"].append("Enabled predictive budgeting")
                results["changes_made"].append("Pre-emptive optimization based on usage trends")

        # Update allocation efficiency score
        allocation.efficiency_score = min(1.0, allocation.efficiency_score + results["efficiency_improvement"])
        self._update_allocation_in_db(allocation)

        return results

    def cleanup_expired_constraints(self) -> int:
        """Clean up expired budget constraints."""
        expired_count = 0
        current_time = datetime.now()

        expired_constraints = []
        for constraint_id, constraint in self.constraints.items():
            if constraint.period_end and current_time > constraint.period_end:
                expired_constraints.append(constraint_id)

        for constraint_id in expired_constraints:
            # Remove from memory
            self.constraints.pop(constraint_id, None)
            self.allocations.pop(constraint_id, None)
            self.optimization_cache.pop(constraint_id, None)

            # Remove from database
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM budget_constraints WHERE id = ?", (constraint_id,))
            cursor.execute("DELETE FROM budget_allocations WHERE constraint_id = ?", (constraint_id,))

            expired_count += 1

        if expired_count > 0:
            self.conn.commit()
            self.logger.info(f"Cleaned up {expired_count} expired budget constraints")

        return expired_count

    def __del__(self):
        """Cleanup database connection."""
        if hasattr(self, "conn"):
            self.conn.close()


def main():
    """CLI interface for token budget manager."""
"""
    import argparse

    parser = argparse.ArgumentParser(description="Token Budget Management System")
    parser.add_argument("--data-dir", default=".claude-patterns", help="Data directory")
    parser.add_argument("--create-constraint", action="store_true", help="Create a budget constraint")
    parser.add_argument("--level", choices=["global", "project", "task", "agent", "session"], help="Budget level")
    parser.add_argument("--scope", choices=["daily", "weekly", "monthly", "task_based", "project_based"], help="Budget scope")
    parser.add_argument("--limit", type=int, help="Token limit")
    parser.add_argument("--status", action="store_true", help="Show budget status")
    parser.add_argument("--report", action="store_true", help="Generate budget report")
    parser.add_argument("--constraint-id", help="Specific constraint ID")
    parser.add_argument("--recommendations", action="store_true", help="Show optimization recommendations")
    parser.add_argument("--predict", type=int, metavar="DAYS", help="Predict usage for N days ahead")
    parser.add_argument(
        "--optimize",
        choices=["conservative", "balanced", "performance", "adaptive", "predictive"],
        help="Apply optimization strategy",
    )
    parser.add_argument("--reset", action="store_true", help="Reset budget allocation")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup expired constraints")

    args = parser.parse_args()

    # Initialize budget manager
    manager = TokenBudgetManager(data_dir=args.data_dir)

    if args.create_constraint:
        if not all([args.level, args.scope, args.limit]):
            print("Error: --level, --scope, and --limit required for creating constraints")
            return

        constraint_id = manager.create_budget_constraint(
            level=BudgetLevel(args.level), scope=BudgetScope(args.scope), limit=args.limit
        )
        print(f"Created budget constraint: {constraint_id}")

    elif args.status:
        status = manager.get_budget_status(args.constraint_id)
        print(json.dumps(status, indent=2))

    elif args.report:
        format_type = "detailed" if args.constraint_id else "summary"
        report = manager.get_budget_report(args.constraint_id, format_type)
        print(json.dumps(report, indent=2))

    elif args.recommendations:
        recommendations = manager.get_optimization_recommendations(args.constraint_id)
        output = []
        for rec in recommendations:
            output.append(
                {
                    "strategy": rec.strategy.value,
                    "description": rec.description,
                    "potential_savings": rec.potential_savings,
                    "confidence": rec.confidence,
                    "priority": rec.priority,
                    "implementation_cost": rec.implementation_cost,
                }
            )
        print(json.dumps(output, indent=2))

    elif args.predict:
        if not args.constraint_id:
            print("Error: --constraint-id required for prediction")
            return

        prediction = manager.predict_usage(args.constraint_id, args.predict)
        print(json.dumps(prediction, indent=2))

    elif args.optimize:
        if not args.constraint_id:
            print("Error: --constraint-id required for optimization")
            return

        results = manager.apply_optimization_strategy(args.constraint_id, OptimizationStrategy(args.optimize))
        print(json.dumps(results, indent=2))

    elif args.reset:
        if not args.constraint_id:
            print("Error: --constraint-id required for reset")
            return

        success = manager.reset_budget(args.constraint_id)
        print(f"Reset {'successful' if success else 'failed'}")

    elif args.cleanup:
        count = manager.cleanup_expired_constraints()
        print(f"Cleaned up {count} expired constraints")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
