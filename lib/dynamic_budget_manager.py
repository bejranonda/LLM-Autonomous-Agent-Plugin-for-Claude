#!/usr/bin/env python3
#     Dynamic Budget Management System
"""
Intelligently manages token budgets across optimization components with
real-time allocation adjustments based on performance metrics and needs.

Target: 15-20% additional cost reduction through intelligent budget allocation
"""
import json
import time
import threading
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import statistics
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class BudgetStrategy(Enum):
    """Budget allocation strategies."""

    EQUAL = "equal"  # Equal distribution
    PERFORMANCE_BASED = "performance"  # Based on performance metrics
    NEEDS_BASED = "needs"  # Based on current needs
    EFFICIENCY_BASED = "efficiency"  # Based on efficiency scores
    PREDICTIVE = "predictive"  # ML-based prediction


class PriorityLevel(Enum):
    """Component priority levels."""

    CRITICAL = 1  # Essential components
    HIGH = 2  # Important components
    MEDIUM = 3  # Useful components
    LOW = 4  # Optional components


@dataclass
class ComponentBudget:
    """Budget allocation for a component."""

    component_id: str
    name: str
    priority: PriorityLevel
    allocated_tokens: int
    used_tokens: int
    performance_score: float  # 0-100
    efficiency_score: float  # 0-100
    last_adjustment: datetime
    adjustment_history: List[Dict[str, Any]]

    @property
    def remaining_tokens(self) -> int:
        """Remaining Tokens."""
        return max(0, self.allocated_tokens - self.used_tokens)

    @property
    def utilization_rate(self) -> float:
        """Utilization Rate."""
        if self.allocated_tokens == 0:
            return 0.0
        return (self.used_tokens / self.allocated_tokens) * 100


@dataclass
class BudgetMetrics:
    """Overall budget management metrics."""

    total_budget: int
    allocated_tokens: int
    used_tokens: int
    waste_percentage: float
    efficiency_score: float
    reallocation_count: int
    savings_achieved: int
    last_rebalancing: datetime

    @property
    def remaining_tokens(self) -> int:
        """Remaining Tokens."""
        return max(0, self.allocated_tokens - self.used_tokens)

    @property
    def utilization_rate(self) -> float:
        """Utilization Rate."""
        if self.allocated_tokens == 0:
            return 0.0
        return (self.used_tokens / self.allocated_tokens) * 100


class DynamicBudgetManager:
    """Intelligent budget management system."""

    def __init__(self, total_budget: int = 100000, db_path: str = "data/databases/budget_metrics.db"):
        """Initialize the processor with default configuration."""
        self.total_budget = total_budget
        self.db_path = db_path
        self.components: Dict[str, ComponentBudget] = {}
        self.strategy = BudgetStrategy.PERFORMANCE_BASED
        self.rebalancing_interval = 300  # 5 minutes
        self.min_budget_allocation = 1000  # Minimum tokens per component

        # Performance tracking
        self.performance_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.efficiency_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))

        # Reallocation tracking
        self.reallocation_log: List[Dict[str, Any]] = []
        self.savings_tracker = 0

        # Threading
        self._lock = threading.RLock()
        self._running = False
        self._rebalancing_thread = None

        # Initialize database
        self._init_database()

        # Register default components
        self._register_default_components()

    def _init_database(self) -> None:
        """Initialize SQLite database for metrics storage."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
"""
                CREATE TABLE IF NOT EXISTS budget_allocations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    component_id TEXT NOT NULL,
                    allocated_tokens INTEGER NOT NULL,
                    used_tokens INTEGER NOT NULL,
                    performance_score REAL NOT NULL,
                    efficiency_score REAL NOT NULL,
                    strategy TEXT NOT NULL
                )
"""
            )

            conn.execute(
"""
                CREATE TABLE IF NOT EXISTS rebalancing_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    trigger_reason TEXT NOT NULL,
                    components_affected INTEGER NOT NULL,
                    tokens_reallocated INTEGER NOT NULL,
                    efficiency_gain REAL NOT NULL
                )
"""
            )

            conn.execute(
"""
                CREATE TABLE IF NOT EXISTS budget_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    total_budget INTEGER NOT NULL,
                    allocated_tokens INTEGER NOT NULL,
                    used_tokens INTEGER NOT NULL,
                    waste_percentage REAL NOT NULL,
                    efficiency_score REAL NOT NULL,
                    savings_achieved INTEGER NOT NULL
                )
"""
            )

            conn.commit()

"""
    def _register_default_components(self) -> None:
        """Register default optimization components."""
        default_components = [
            ("progressive_loader", "Progressive Content Loader", PriorityLevel.HIGH),
            ("smart_cache", "Smart Cache System", PriorityLevel.HIGH),
            ("token_monitor", "Token Monitoring System", PriorityLevel.CRITICAL),
            ("comm_optimizer", "Communication Optimizer", PriorityLevel.MEDIUM),
            ("metrics_system", "Metrics & KPI System", PriorityLevel.MEDIUM),
        ]

        for component_id, name, priority in default_components:
            self.register_component(component_id, name, priority)

    def register_component(
        self,
        component_id: str,
        name: str,
        priority: PriorityLevel = PriorityLevel.MEDIUM,
        initial_allocation: Optional[int] = None,
    )-> None:
        """Register Component."""Register a new component for budget management."""
        with self._lock:
            if component_id in self.components:
                logger.warning(f"Component {component_id} already registered")
                return

            if initial_allocation is None:
                initial_allocation = self._calculate_initial_allocation(priority)

            self.components[component_id] = ComponentBudget(
                component_id=component_id,
                name=name,
                priority=priority,
                allocated_tokens=initial_allocation,
                used_tokens=0,
                performance_score=50.0,  # Start with neutral score
                efficiency_score=50.0,
                last_adjustment=datetime.now(),
                adjustment_history=[],
            )

            logger.info(f"Registered component: {name} ({component_id}) with {initial_allocation} tokens")

    def _calculate_initial_allocation(self, priority: PriorityLevel) -> int:
        """Calculate initial budget allocation based on priority."""
        base_allocation = self.total_budget * 0.2  # 20% base for medium priority

        multipliers = {PriorityLevel.CRITICAL: 1.5, PriorityLevel.HIGH: 1.2, PriorityLevel.MEDIUM: 1.0, PriorityLevel.LOW: 0.6}

        allocation = int(base_allocation * multipliers[priority])
        return max(allocation, self.min_budget_allocation)

    def use_tokens(self, component_id: str, tokens_used: int) -> bool:
        """Record token usage for a component."""
        with self._lock:
            if component_id not in self.components:
                logger.warning(f"Component {component_id} not registered")
                return False

            component = self.components[component_id]
            if component.used_tokens + tokens_used > component.allocated_tokens:
                logger.warning(f"Component {component_id} exceeding budget allocation")
                # Try to allocate more tokens if available
                if not self._emergency_allocation(component_id, tokens_used):
                    return False

            component.used_tokens += tokens_used
            self._record_usage(component_id, tokens_used)
            return True

    def _emergency_allocation(self, component_id: str, additional_tokens: int) -> bool:
        """Emergency allocation for components exceeding their budget."""
        # Try to borrow from low-priority components
        available_tokens = 0
        donors = []

        for comp_id, comp in self.components.items():
            if comp_id != component_id and comp.priority == PriorityLevel.LOW:
                available = comp.allocated_tokens - comp.used_tokens
                if available > 0:
                    available_tokens += available
                    donors.append(comp_id)

        if available_tokens >= additional_tokens:
            # Redistribute from donors
            needed = additional_tokens
            for donor in donors:
                donor_comp = self.components[donor]
                available = donor_comp.allocated_tokens - donor_comp.used_tokens
                transfer = min(available, needed)

                donor_comp.allocated_tokens -= transfer
                self.components[component_id].allocated_tokens += transfer
                needed -= transfer

                if needed <= 0:
                    break

            return True

        return False

    def update_performance_metrics(self, component_id: str, performance_score: float, efficiency_score: float) -> None:
        """Update performance metrics for a component."""
        with self._lock:
            if component_id not in self.components:
                return

            component = self.components[component_id]
            component.performance_score = performance_score
            component.efficiency_score = efficiency_score

            # Track history
            self.performance_history[component_id].append(performance_score)
            self.efficiency_history[component_id].append(efficiency_score)

            # Trigger rebalancing if significant change
            self._check_rebalancing_need(component_id)

    def _check_rebalancing_need(self, component_id: str) -> None:
        """Check if rebalancing is needed based on performance changes."""
        if len(self.efficiency_history[component_id]) < 5:
            return

        recent_efficiency = list(self.efficiency_history[component_id])[-5:]
        efficiency_trend = statistics.mean(recent_efficiency[-3:]) - statistics.mean(recent_efficiency[:2])

        # If efficiency improved significantly, consider reallocating more budget
        if efficiency_trend > 10:  # 10% improvement
            self._trigger_rebalancing(f"efficiency_improvement_{component_id}")

        # If efficiency declined significantly, consider reducing budget
        elif efficiency_trend < -10:
            self._trigger_rebalancing(f"efficiency_decline_{component_id}")

    def _trigger_rebalancing(self, reason: str) -> None:
        """Trigger budget rebalancing."""
        logger.info(f"Triggering budget rebalancing: {reason}")
        threading.Thread(target=self._rebalance_budgets, args=(reason,), daemon=True).start()

    def _rebalance_budgets(self, trigger_reason: str) -> None:
        """Rebalance budgets across components based on current strategy."""
        with self._lock:
            start_time = time.time()
            old_allocations = {comp_id: comp.allocated_tokens for comp_id, comp in self.components.items()}

            if self.strategy == BudgetStrategy.PERFORMANCE_BASED:
                self._performance_based_rebalancing()
            elif self.strategy == BudgetStrategy.EFFICIENCY_BASED:
                self._efficiency_based_rebalancing()
            elif self.strategy == BudgetStrategy.NEEDS_BASED:
                self._needs_based_rebalancing()
            elif self.strategy == BudgetStrategy.PREDICTIVE:
                self._predictive_rebalancing()
            else:
                self._equal_rebalancing()

            # Track changes
            tokens_reallocated = sum(
                abs(self.components[comp_id].allocated_tokens - old_allocations[comp_id]) for comp_id in self.components
            )

            # Calculate efficiency gain
            old_efficiency = self._calculate_overall_efficiency(old_allocations)
            new_efficiency = self._calculate_overall_efficiency()
            efficiency_gain = new_efficiency - old_efficiency

            # Log rebalancing event
            self._log_rebalancing_event(trigger_reason, tokens_reallocated, efficiency_gain)

            # Save to database
            self._save_rebalancing_event(trigger_reason, tokens_reallocated, efficiency_gain)

            logger.info(
                f"Rebalancing completed: {tokens_reallocated} tokens reallocated, " f"efficiency gain: {efficiency_gain:.2f}"
            )

    def _performance_based_rebalancing(self) -> None:
        """Rebalance budgets based on performance scores."""
        total_performance_score = sum(comp.performance_score for comp in self.components.values())

        if total_performance_score == 0:
            return

        available_budget = sum(
            comp.allocated_tokens - comp.used_tokens
            for comp in self.components.values()
            if comp.priority != PriorityLevel.CRITICAL
        )

        for component in self.components.values():
            if component.priority == PriorityLevel.CRITICAL:
                continue  # Don't reduce critical component budgets

            # Calculate new allocation based on performance
            performance_ratio = component.performance_score / total_performance_score
            target_allocation = int(available_budget * performance_ratio)

            # Ensure minimum allocation
            target_allocation = max(target_allocation, self.min_budget_allocation)

            # Apply changes gradually
            change = target_allocation - component.allocated_tokens
            max_change = int(component.allocated_tokens * 0.3)  # Max 30% change per rebalancing
            actual_change = max(-max_change, min(max_change, change))

            component.allocated_tokens += actual_change
            component.last_adjustment = datetime.now()

            # Track adjustment
            component.adjustment_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "old_allocation": component.allocated_tokens - actual_change,
                    "new_allocation": component.allocated_tokens,
                    "change": actual_change,
                    "reason": "performance_based",
                }
            )

    def _efficiency_based_rebalancing(self) -> None:
        """Rebalance budgets based on efficiency scores."""
        total_efficiency_score = sum(comp.efficiency_score for comp in self.components.values())

        if total_efficiency_score == 0:
            return

        # Prioritize efficient components
        for component in self.components.values():
            efficiency_ratio = component.efficiency_score / total_efficiency_score

            # High efficiency components get potential increases
            if component.efficiency_score > 70 and component.priority != PriorityLevel.LOW:
                # Try to increase allocation
                additional_tokens = int(self.total_budget * 0.05 * efficiency_ratio)
                component.allocated_tokens += additional_tokens
            elif component.efficiency_score < 40 and component.priority != PriorityLevel.CRITICAL:
                # Reduce allocation for inefficient components
                reduction = int(component.allocated_tokens * 0.1)
                component.allocated_tokens = max(component.allocated_tokens - reduction, self.min_budget_allocation)

            component.last_adjustment = datetime.now()

    def _needs_based_rebalancing(self) -> None:
        """Rebalance budgets based on current utilization and needs."""
        for component in self.components.values():
            utilization_rate = component.utilization_rate

            # High utilization (over 80%) - consider increasing budget
            if utilization_rate > 80 and component.priority in [PriorityLevel.CRITICAL, PriorityLevel.HIGH]:
                increase = int(component.allocated_tokens * 0.2)
                component.allocated_tokens += increase

            # Low utilization (under 30%) - consider reducing budget
            elif utilization_rate < 30 and component.priority != PriorityLevel.CRITICAL:
                reduction = int(component.allocated_tokens * 0.15)
                component.allocated_tokens = max(component.allocated_tokens - reduction, self.min_budget_allocation)

            component.last_adjustment = datetime.now()

    def _predictive_rebalancing(self) -> None:
        """Rebalance budgets using predictive analytics."""
        for component_id, component in self.components.items():
            if len(self.efficiency_history[component_id]) < 10:
                continue

            # Predict future efficiency based on trend
            efficiency_values = list(self.efficiency_history[component_id])
            if len(efficiency_values) >= 6:
                recent_avg = statistics.mean(efficiency_values[-3:])
                previous_avg = statistics.mean(efficiency_values[-6:-3])
                recent_trend = recent_avg - previous_avg
            else:
                recent_trend = 0

            predicted_efficiency = component.efficiency_score + (recent_trend * 0.5)

            # Allocate budget based on prediction
            if predicted_efficiency > 80:
                # Invest in improving components
                component.allocated_tokens = int(component.allocated_tokens * 1.15)
            elif predicted_efficiency < 50:
                # Reduce budget for declining components
                component.allocated_tokens = max(int(component.allocated_tokens * 0.85), self.min_budget_allocation)

            component.last_adjustment = datetime.now()

    def _equal_rebalancing(self) -> None:
        """Equal budget distribution across non-critical components."""
        non_critical_components = [comp for comp in self.components.values() if comp.priority != PriorityLevel.CRITICAL]

        if not non_critical_components:
            return

        available_budget = self.total_budget - sum(
            comp.allocated_tokens for comp in self.components.values() if comp.priority == PriorityLevel.CRITICAL
        )

        equal_share = available_budget // len(non_critical_components)

        for component in non_critical_components:
            component.allocated_tokens = max(equal_share, self.min_budget_allocation)
            component.last_adjustment = datetime.now()

    def _calculate_overall_efficiency(self, allocations: Optional[Dict[str, int]] = None) -> float:
        """Calculate overall system efficiency."""
        if allocations is None:
            allocations = {comp_id: comp.allocated_tokens for comp_id, comp in self.components.items()}

        total_weighted_efficiency = 0
        total_budget = 0

        for comp_id, allocation in allocations.items():
            if comp_id in self.components:
                component = self.components[comp_id]
                weighted_efficiency = component.efficiency_score * allocation
                total_weighted_efficiency += weighted_efficiency
                total_budget += allocation

        return total_weighted_efficiency / total_budget if total_budget > 0 else 0

    def _log_rebalancing_event(self, reason: str, tokens_reallocated: int, efficiency_gain: float) -> None:
        """Log rebalancing event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "tokens_reallocated": tokens_reallocated,
            "efficiency_gain": efficiency_gain,
            "components_affected": len(self.components),
            "strategy": self.strategy.value,
        }

        self.reallocation_log.append(event)
        self.savings_tracker += int(tokens_reallocated * efficiency_gain / 100)

    def _save_rebalancing_event(self, reason: str, tokens_reallocated: int, efficiency_gain: float) -> None:
        """Save rebalancing event to database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
"""
                INSERT INTO rebalancing_events
                (timestamp, trigger_reason, components_affected, tokens_reallocated, efficiency_gain)
                VALUES (?, ?, ?, ?, ?)
            """,
                (datetime.now().isoformat(), reason, len(self.components), tokens_reallocated, efficiency_gain),
            )
            conn.commit()

    def _record_usage(self, component_id: str, tokens_used: int) -> None:
        """Record token usage in database."""
        component = self.components[component_id]

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
"""
                INSERT INTO budget_allocations
                (timestamp, component_id, allocated_tokens, used_tokens, performance_score, efficiency_score, strategy)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    datetime.now().isoformat(),
                    component_id,
                    component.allocated_tokens,
                    component.used_tokens,
                    component.performance_score,
                    component.efficiency_score,
                    self.strategy.value,
                ),
            )
            conn.commit()

    def get_metrics(self) -> BudgetMetrics:
        """Get current budget management metrics."""
        with self._lock:
            allocated_tokens = sum(comp.allocated_tokens for comp in self.components.values())
            used_tokens = sum(comp.used_tokens for comp in self.components.values())

            # Calculate waste (unused allocated tokens)
            waste_percentage = ((allocated_tokens - used_tokens) / allocated_tokens * 100) if allocated_tokens > 0 else 0

            # Calculate efficiency score
            efficiency_scores = [comp.efficiency_score for comp in self.components.values()]
            avg_efficiency = statistics.mean(efficiency_scores) if efficiency_scores else 0

            last_rebalancing = max((comp.last_adjustment for comp in self.components.values()), default=datetime.now())

            return BudgetMetrics(
                total_budget=self.total_budget,
                allocated_tokens=allocated_tokens,
                used_tokens=used_tokens,
                waste_percentage=waste_percentage,
                efficiency_score=avg_efficiency,
                reallocation_count=len(self.reallocation_log),
                savings_achieved=self.savings_tracker,
                last_rebalancing=last_rebalancing,
            )

    def get_component_status(self, component_id: str) -> Optional[ComponentBudget]:
        """Get status of a specific component."""
        return self.components.get(component_id)

    def set_strategy(self, strategy: BudgetStrategy) -> None:
        """Change budget allocation strategy."""
        old_strategy = self.strategy
        self.strategy = strategy
        logger.info(f"Changed strategy from {old_strategy.value} to {strategy.value}")

        # Trigger rebalancing with new strategy
        self._trigger_rebalancing(f"strategy_change_{strategy.value}")

    def start_monitoring(self) -> None:
        """Start continuous budget monitoring."""
        if self._running:
            logger.warning("Budget monitoring already running")
            return

        self._running = True
        self._rebalancing_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._rebalancing_thread.start()
        logger.info("Started budget monitoring")

    def stop_monitoring(self) -> None:
        """Stop budget monitoring."""
        self._running = False
        if self._rebalancing_thread:
            self._rebalancing_thread.join()
        logger.info("Stopped budget monitoring")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop for automatic rebalancing."""
        while self._running:
            try:
                # Check if rebalancing is needed
                metrics = self.get_metrics()

                # Trigger rebalancing if waste is high or efficiency is low
                if metrics.waste_percentage > 30 or metrics.efficiency_score < 60:
                    self._rebalance_budgets("automatic_monitoring")

                # Sleep until next check
                time.sleep(self.rebalancing_interval)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait 1 minute on error

    def generate_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate comprehensive budget management report."""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        with sqlite3.connect(self.db_path) as conn:
            # Get recent allocations
            cursor = conn.execute(
"""
                SELECT component_id, COUNT(*) as allocations_count,
                       AVG(allocated_tokens) as avg_allocation,
                       AVG(used_tokens) as avg_usage,
                       AVG(efficiency_score) as avg_efficiency
                FROM budget_allocations
                WHERE timestamp > ?
                GROUP BY component_id
                ORDER BY avg_efficiency DESC
            """,
                (cutoff_time.isoformat(),),
            )

            component_stats = []
            for row in cursor.fetchall():
                component_id, count, avg_alloc, avg_usage, avg_eff = row
                component = self.components.get(component_id)
                if component:
                    component_stats.append(
                        {
                            "component_id": component_id,
                            "name": component.name,
                            "priority": component.priority.name,
                            "allocations_count": count,
                            "avg_allocation": avg_alloc,
                            "avg_usage": avg_usage,
                            "avg_efficiency": avg_eff,
                            "current_allocation": component.allocated_tokens,
                            "current_usage": component.used_tokens,
                            "utilization_rate": component.utilization_rate,
                        }
                    )

            # Get recent rebalancing events
            cursor = conn.execute(
"""
                SELECT COUNT(*) as events_count,
                       SUM(tokens_reallocated) as total_reallocated,
                       AVG(efficiency_gain) as avg_gain
                FROM rebalancing_events
                WHERE timestamp > ?
            """,
                (cutoff_time.isoformat(),),
            )

            rebalancing_stats = cursor.fetchone()
            events_count, total_reallocated, avg_gain = rebalancing_stats or (0, 0, 0)

            # Calculate overall metrics
            metrics = self.get_metrics()

            return {
                "report_period_hours": hours,
                "generated_at": datetime.now().isoformat(),
                "strategy": self.strategy.value,
                "overall_metrics": asdict(metrics),
                "component_statistics": component_stats,
                "rebalancing_summary": {
                    "events_count": events_count,
                    "total_tokens_reallocated": total_reallocated or 0,
                    "average_efficiency_gain": avg_gain or 0.0,
                },
                "savings_achieved": self.savings_tracker,
                "recommendations": self._generate_recommendations(component_stats),
            }

    def _generate_recommendations(self, component_stats: List[Dict[str, Any]]) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []

        # Analyze component performance
        for stats in component_stats:
            if stats["avg_efficiency"] < 40:
                recommendations.append(
                    f"Consider reducing budget for {stats['name']} - low efficiency ({stats['avg_efficiency']:.1f}%)"
                )
            elif stats["utilization_rate"] > 90:
                recommendations.append(
                    f"Consider increasing budget for {stats['name']} - high utilization ({stats['utilization_rate']:.1f}%)"
                )

        # Strategy recommendations
        metrics = self.get_metrics()
        if metrics.waste_percentage > 25:
            recommendations.append("High waste detected - consider switching to needs-based strategy")

        if metrics.efficiency_score < 60:
            recommendations.append("Low overall efficiency - consider performance-based rebalancing")

        if not recommendations:
            recommendations.append("Budget allocation is optimized - current strategy is effective")

        return recommendations


def main():
    """Demo the dynamic budget management system."""
    print("Dynamic Budget Management System Demo")
    print("=" * 50)
    print("Target: 15-20% additional cost reduction through intelligent budget allocation")
    print()

"""
    # Initialize budget manager
    budget_manager = DynamicBudgetManager(total_budget=100000)

    print(f"Initial budget allocation: ${budget_manager.total_budget:,}")
    print(f"Registered components: {len(budget_manager.components)}")
    print()

    # Simulate component operations
    print("=== Simulating Component Operations ===")

    # Simulate different usage patterns
    operations = [
        ("progressive_loader", 5000, 85.0, 90.0),
        ("smart_cache", 8000, 92.0, 88.0),
        ("token_monitor", 3000, 95.0, 95.0),
        ("comm_optimizer", 6000, 78.0, 82.0),
        ("metrics_system", 4000, 88.0, 85.0),
    ]

    for component_id, tokens, performance, efficiency in operations:
        budget_manager.use_tokens(component_id, tokens)
        budget_manager.update_performance_metrics(component_id, performance, efficiency)
        print(f"   {component_id}: Used {tokens:,} tokens, " f"Performance: {performance:.1f}%, Efficiency: {efficiency:.1f}%")

    print()

    # Test different strategies
    strategies = [BudgetStrategy.PERFORMANCE_BASED, BudgetStrategy.EFFICIENCY_BASED, BudgetStrategy.NEEDS_BASED]

    print("=== Testing Different Allocation Strategies ===")

    for strategy in strategies:
        print(f"\n{strategy.value.title()} Strategy:")
        budget_manager.set_strategy(strategy)
        time.sleep(0.5)  # Allow rebalancing to complete

        metrics = budget_manager.get_metrics()
        print(f"   Overall efficiency: {metrics.efficiency_score:.1f}%")
        print(f"   Waste percentage: {metrics.waste_percentage:.1f}%")
        print(f"   Utilization rate: {metrics.utilization_rate:.1f}%")
        print(f"   Savings achieved: {metrics.savings_achieved:,} tokens")

    # Generate comprehensive report
    print(f"\n=== Budget Management Report ===")
    report = budget_manager.generate_report()

    print(f"Report period: {report['report_period_hours']} hours")
    print(f"Current strategy: {report['strategy']}")
    print(f"Overall efficiency: {report['overall_metrics']['efficiency_score']:.1f}%")
    print(f"Waste percentage: {report['overall_metrics']['waste_percentage']:.1f}%")
    print(f"Total savings: {report['savings_achieved']:,} tokens")
    print(f"Rebalancing events: {report['rebalancing_summary']['events_count']}")

    print(f"\nRecommendations:")
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"   {i}. {rec}")

    # Calculate estimated cost reduction
    total_tokens = report["overall_metrics"]["used_tokens"]
    estimated_reduction = (report["savings_achieved"] / total_tokens * 100) if total_tokens > 0 else 0

    print(f"\nEstimated cost reduction: {estimated_reduction:.1f}%")
    print(f"Target achieved: {'YES' if estimated_reduction >= 15 else 'NO'}")

    return True


if __name__ == "__main__":
    main()
