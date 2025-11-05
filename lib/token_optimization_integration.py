"""
Token Optimization Integration System

Integrates all token optimization components into a unified system for
maximum token efficiency across the autonomous agent platform.

Components Integrated:
- Token Optimization Engine
- Progressive Content Loader
- Autonomous Token Optimizer
- Smart Caching System
- Agent Communication Optimizer
- Token Monitoring System
- Token Budget Manager
- Advanced Token Optimizer
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from pathlib import Path
import threading
import time

# Import all optimization components
try:
    from token_optimization_engine import TokenOptimizer, ContentType, ContentItem
    from progressive_content_loader import ProgressiveContentLoader, LoadingTier, ContentSection
    from autonomous_token_optimizer import AutonomousTokenOptimizer, TaskComplexity, OptimizationStrategy
    from smart_caching_system import SmartCache, CachePolicy, PredictionModel
    from agent_communication_optimizer import AgentCommunicationOptimizer, MessagePriority, CompressionType
    from token_monitoring_system import TokenMonitoringSystem, MetricType, AlertLevel
    from token_budget_manager import TokenBudgetManager, BudgetLevel, BudgetScope, OptimizationStrategy as BudgetOptimizationStrategy
    from advanced_token_optimizer import AdvancedTokenOptimizer, OptimizationObjective, AlgorithmType
except ImportError as e:
    logging.error(f"Failed to import optimization components: {e}")
    # Continue with mock classes for integration structure
    class TokenOptimizer: pass
    class ProgressiveContentLoader: pass
    class AutonomousTokenOptimizer: pass
    class SmartCache: pass
    class AgentCommunicationOptimizer: pass
    class TokenMonitoringSystem: pass
    class TokenBudgetManager: pass
    class AdvancedTokenOptimizer: pass

class IntegrationMode(Enum):
    """Integration operation modes."""
    MONITORING_ONLY = "monitoring_only"
    OPTIMIZATION_ACTIVE = "optimization_active"
    BUDGET_ENFORCED = "budget_enforced"
    FULL_OPTIMIZATION = "full_optimization"

class OptimizationLevel(Enum):
    """Optimization aggressiveness levels."""
    MINIMAL = "minimal"      # Basic optimizations only
    STANDARD = "standard"    # Recommended optimizations
    AGGRESSIVE = "aggressive"  # Maximum optimizations
    ADAPTIVE = "adaptive"    # Dynamically adjusts

@dataclass
class IntegrationConfig:
    """Configuration for token optimization integration."""
    mode: IntegrationMode
    level: OptimizationLevel
    data_directory: str = ".claude-patterns"
    monitoring_interval: int = 60  # seconds
    optimization_interval: int = 300  # seconds
    budget_enforcement: bool = True
    auto_optimization: bool = True
    learning_enabled: bool = True
    alert_thresholds: Dict[str, float] = None

    def __post_init__(self):
        if self.alert_thresholds is None:
            self.alert_thresholds = {
                "token_usage_rate": 0.8,
                "budget_usage": 0.9,
                "efficiency_drop": 0.2,
                "error_rate": 0.05
            }

@dataclass
class OptimizationMetrics:
    """Combined optimization metrics."""
    total_tokens_saved: int
    efficiency_improvement: float
    budget_utilization: float
    cache_hit_rate: float
    compression_ratio: float
    response_time_improvement: float
    cost_savings: float
    optimization_success_rate: float

@dataclass
class IntegrationStatus:
    """Status of integration system."""
    active: bool
    mode: IntegrationMode
    level: OptimizationLevel
    components_status: Dict[str, bool]
    last_optimization: Optional[datetime]
    uptime_seconds: float
    metrics: OptimizationMetrics

class TokenOptimizationIntegration:
    """Main integration system for all token optimization components."""

    def __init__(self, config: IntegrationConfig):
        """Initialize token optimization integration."""
        self.config = config
        self.data_dir = Path(config.data_directory)
        self.data_dir.mkdir(exist_ok=True)

        # Initialize all components
        self.components = {}
        self._initialize_components()

        # Integration state
        self.active = False
        self.start_time = None
        self.optimization_thread = None
        self.monitoring_thread = None
        self.shutdown_event = threading.Event()

        # Metrics and status
        self.metrics = OptimizationMetrics(
            total_tokens_saved=0,
            efficiency_improvement=0.0,
            budget_utilization=0.0,
            cache_hit_rate=0.0,
            compression_ratio=0.0,
            response_time_improvement=0.0,
            cost_savings=0.0,
            optimization_success_rate=0.0
        )

        self.status = IntegrationStatus(
            active=False,
            mode=config.mode,
            level=config.level,
            components_status={},
            last_optimization=None,
            uptime_seconds=0,
            metrics=self.metrics
        )

        # Performance tracking
        self.performance_history = []
        self.optimization_results = []

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _initialize_components(self) -> None:
        """Initialize all optimization components."""
        try:
            # Core optimization engine
            self.components['token_optimizer'] = TokenOptimizer()
            self.logger.info("Token optimizer initialized")

            # Progressive content loader
            self.components['progressive_loader'] = ProgressiveContentLoader(
                data_dir=str(self.data_dir)
            )
            self.logger.info("Progressive content loader initialized")

            # Autonomous token optimizer
            self.components['autonomous_optimizer'] = AutonomousTokenOptimizer(
                data_dir=str(self.data_dir)
            )
            self.logger.info("Autonomous token optimizer initialized")

            # Smart caching system
            self.components['smart_cache'] = SmartCache(
                data_dir=str(self.data_dir)
            )
            self.logger.info("Smart cache initialized")

            # Agent communication optimizer
            self.components['communication_optimizer'] = AgentCommunicationOptimizer(
                data_dir=str(self.data_dir)
            )
            self.logger.info("Communication optimizer initialized")

            # Token monitoring system
            self.components['monitoring_system'] = TokenMonitoringSystem(
                db_path=str(self.data_dir / "token_monitoring.db"),
                data_dir=str(self.data_dir)
            )
            self.logger.info("Monitoring system initialized")

            # Token budget manager
            self.components['budget_manager'] = TokenBudgetManager(
                db_path=str(self.data_dir / "token_budgets.db"),
                data_dir=str(self.data_dir)
            )
            self.logger.info("Budget manager initialized")

            # Advanced token optimizer
            self.components['advanced_optimizer'] = AdvancedTokenOptimizer(
                data_dir=str(self.data_dir)
            )
            self.logger.info("Advanced optimizer initialized")

            # Update component status
            self.status.components_status = {
                name: True for name in self.components.keys()
            }

        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            self.status.components_status = {
                name: False for name in ['token_optimizer', 'progressive_loader',
                                       'autonomous_optimizer', 'smart_cache',
                                       'communication_optimizer', 'monitoring_system',
                                       'budget_manager', 'advanced_optimizer']
            }

    def start(self) -> bool:
        """Start the integration system."""
        if self.active:
            self.logger.warning("Integration system already active")
            return False

        try:
            self.active = True
            self.start_time = datetime.now()
            self.status.active = True

            # Start monitoring thread
            if self.config.mode in [IntegrationMode.MONITORING_ONLY, IntegrationMode.FULL_OPTIMIZATION]:
                self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
                self.monitoring_thread.start()
                self.logger.info("Monitoring thread started")

            # Start optimization thread
            if self.config.mode in [IntegrationMode.OPTIMIZATION_ACTIVE, IntegrationMode.FULL_OPTIMIZATION]:
                self.optimization_thread = threading.Thread(target=self._optimization_loop, daemon=True)
                self.optimization_thread.start()
                self.logger.info("Optimization thread started")

            # Create default budget constraints
            if self.config.budget_enforcement:
                self._create_default_budgets()

            self.logger.info(f"Token optimization integration started in {self.config.mode.value} mode")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start integration system: {e}")
            self.active = False
            self.status.active = False
            return False

    def stop(self) -> None:
        """Stop the integration system."""
        if not self.active:
            return

        self.logger.info("Stopping token optimization integration...")
        self.active = False
        self.shutdown_event.set()

        # Wait for threads to finish
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)

        if self.optimization_thread and self.optimization_thread.is_alive():
            self.optimization_thread.join(timeout=5)

        self.status.active = False
        self.logger.info("Token optimization integration stopped")

    def _create_default_budgets(self) -> None:
        """Create default budget constraints."""
        budget_manager = self.components.get('budget_manager')
        if not budget_manager:
            return

        # Global daily budget
        budget_manager.create_budget_constraint(
            level=BudgetLevel.GLOBAL,
            scope=BudgetScope.DAILY,
            limit=100000,  # 100K tokens per day
            tags={"type": "default", "scope": "global"}
        )

        # Project budget
        budget_manager.create_budget_constraint(
            level=BudgetLevel.PROJECT,
            scope=BudgetScope.PROJECT_BASED,
            limit=50000,  # 50K tokens per project
            tags={"type": "default", "scope": "project"}
        )

        # Task budget
        budget_manager.create_budget_constraint(
            level=BudgetLevel.TASK,
            scope=BudgetScope.TASK_BASED,
            limit=5000,  # 5K tokens per task
            tags={"type": "default", "scope": "task"}
        )

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        monitoring_system = self.components.get('monitoring_system')
        if not monitoring_system:
            return

        while self.active and not self.shutdown_event.is_set():
            try:
                # Collect metrics from all components
                self._collect_metrics()

                # Check for alerts
                self._check_alerts()

                # Update status
                self._update_status()

                # Sleep until next iteration
                self.shutdown_event.wait(self.config.monitoring_interval)

            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)  # Brief pause on error

    def _optimization_loop(self) -> None:
        """Main optimization loop."""
        while self.active and not self.shutdown_event.is_set():
            try:
                # Run optimization cycle
                self._run_optimization_cycle()

                # Sleep until next iteration
                self.shutdown_event.wait(self.config.optimization_interval)

            except Exception as e:
                self.logger.error(f"Error in optimization loop: {e}")
                time.sleep(30)  # Brief pause on error

    def _collect_metrics(self) -> None:
        """Collect metrics from all components."""
        current_time = datetime.now()

        # Collect from monitoring system
        monitoring_system = self.components.get('monitoring_system')
        if monitoring_system:
            try:
                # Get recent metrics
                recent_metrics = monitoring_system.get_recent_metrics(
                    hours=1, metric_type=MetricType.TOKEN_USAGE
                )

                if recent_metrics:
                    total_usage = sum(m.value for m in recent_metrics)
                    self.metrics.budget_utilization = min(1.0, total_usage / 1000)  # Normalize
            except Exception as e:
                self.logger.warning(f"Failed to collect monitoring metrics: {e}")

        # Collect from smart cache
        smart_cache = self.components.get('smart_cache')
        if smart_cache:
            try:
                cache_stats = smart_cache.get_cache_stats()
                self.metrics.cache_hit_rate = cache_stats.get('hit_rate', 0.0)
            except Exception as e:
                self.logger.warning(f"Failed to collect cache metrics: {e}")

        # Collect from communication optimizer
        comm_optimizer = self.components.get('communication_optimizer')
        if comm_optimizer:
            try:
                # Get compression statistics
                compression_stats = comm_optimizer.get_compression_stats()
                self.metrics.compression_ratio = compression_stats.get('avg_compression', 1.0)
            except Exception as e:
                self.logger.warning(f"Failed to collect communication metrics: {e}")

        # Store in performance history
        self.performance_history.append({
            'timestamp': current_time,
            'metrics': asdict(self.metrics)
        })

        # Keep only recent history
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]

    def _check_alerts(self) -> None:
        """Check for alert conditions."""
        monitoring_system = self.components.get('monitoring_system')
        if not monitoring_system:
            return

        # Check budget utilization
        if self.metrics.budget_utilization > self.config.alert_thresholds["budget_usage"]:
            monitoring_system.create_alert(
                level=AlertLevel.WARNING,
                message=f"High budget utilization: {self.metrics.budget_utilization:.1%}",
                source="integration_system",
                tags={"type": "budget_alert"}
            )

        # Check efficiency drop
        if len(self.performance_history) >= 2:
            current_efficiency = self.metrics.efficiency_improvement
            previous_efficiency = self.performance_history[-2]['metrics']['efficiency_improvement']

            if previous_efficiency > 0:
                efficiency_change = (current_efficiency - previous_efficiency) / previous_efficiency
                if efficiency_change < -self.config.alert_thresholds["efficiency_drop"]:
                    monitoring_system.create_alert(
                        level=AlertLevel.WARNING,
                        message=f"Efficiency drop detected: {efficiency_change:.1%}",
                        source="integration_system",
                        tags={"type": "efficiency_alert"}
                    )

    def _update_status(self) -> None:
        """Update integration status."""
        if self.start_time:
            self.status.uptime_seconds = (datetime.now() - self.start_time).total_seconds()

        # Update component status
        for name, component in self.components.items():
            try:
                # Basic health check - try to access a simple attribute or method
                if hasattr(component, 'is_healthy'):
                    self.status.components_status[name] = component.is_healthy()
                else:
                    self.status.components_status[name] = True  # Assume healthy if no check method
            except Exception:
                self.status.components_status[name] = False

    def _run_optimization_cycle(self) -> None:
        """Run a complete optimization cycle."""
        cycle_start = datetime.now()
        tokens_saved_cycle = 0

        try:
            # 1. Optimize token usage
            tokens_saved_cycle += self._optimize_token_usage()

            # 2. Optimize caching
            tokens_saved_cycle += self._optimize_caching()

            # 3. Optimize communications
            tokens_saved_cycle += self._optimize_communications()

            # 4. Optimize budgets if needed
            if self.config.budget_enforcement:
                self._optimize_budgets()

            # 5. Advanced optimization if enabled
            if self.config.level in [OptimizationLevel.AGGRESSIVE, OptimizationLevel.ADAPTIVE]:
                tokens_saved_cycle += self._run_advanced_optimization()

            # Update metrics
            self.metrics.total_tokens_saved += tokens_saved_cycle
            self.status.last_optimization = datetime.now()

            # Record optimization result
            self.optimization_results.append({
                'timestamp': cycle_start,
                'tokens_saved': tokens_saved_cycle,
                'duration': (datetime.now() - cycle_start).total_seconds(),
                'success': True
            })

            self.logger.info(f"Optimization cycle completed: {tokens_saved_cycle} tokens saved")

        except Exception as e:
            self.logger.error(f"Optimization cycle failed: {e}")
            self.optimization_results.append({
                'timestamp': cycle_start,
                'tokens_saved': 0,
                'duration': (datetime.now() - cycle_start).total_seconds(),
                'success': False,
                'error': str(e)
            })

    def _optimize_token_usage(self) -> int:
        """Optimize token usage patterns."""
        token_optimizer = self.components.get('token_optimizer')
        if not token_optimizer:
            return 0

        try:
            # Get current usage patterns
            usage_patterns = token_optimizer.get_current_usage_patterns()

            # Apply optimizations based on level
            tokens_saved = 0

            if self.config.level in [OptimizationLevel.STANDARD, OptimizationLevel.AGGRESSIVE, OptimizationLevel.ADAPTIVE]:
                # Enable progressive loading
                tokens_saved += token_optimizer.enable_progressive_loading()

            if self.config.level in [OptimizationLevel.AGGRESSIVE, OptimizationLevel.ADAPTIVE]:
                # Enable aggressive compression
                tokens_saved += token_optimizer.enable_compression()

            if self.config.level == OptimizationLevel.ADAPTIVE:
                # Enable adaptive optimization
                tokens_saved += token_optimizer.enable_adaptive_optimization()

            return tokens_saved

        except Exception as e:
            self.logger.warning(f"Token usage optimization failed: {e}")
            return 0

    def _optimize_caching(self) -> int:
        """Optimize caching strategies."""
        smart_cache = self.components.get('smart_cache')
        if not smart_cache:
            return 0

        try:
            # Analyze cache performance
            cache_stats = smart_cache.get_cache_stats()

            # Optimize cache based on performance
            tokens_saved = 0

            if cache_stats.get('hit_rate', 0) < 0.7:
                # Low hit rate, optimize cache
                tokens_saved += smart_cache.optimize_cache_strategy()

            if self.config.level in [OptimizationLevel.AGGRESSIVE, OptimizationLevel.ADAPTIVE]:
                # Enable predictive caching
                tokens_saved += smart_cache.enable_predictive_caching()

            return tokens_saved

        except Exception as e:
            self.logger.warning(f"Caching optimization failed: {e}")
            return 0

    def _optimize_communications(self) -> int:
        """Optimize agent communications."""
        comm_optimizer = self.components.get('communication_optimizer')
        if not comm_optimizer:
            return 0

        try:
            # Get communication patterns
            comm_patterns = comm_optimizer.get_communication_patterns()

            # Apply optimizations
            tokens_saved = 0

            if self.config.level in [OptimizationLevel.STANDARD, OptimizationLevel.AGGRESSIVE, OptimizationLevel.ADAPTIVE]:
                # Enable message compression
                tokens_saved += comm_optimizer.enable_compression()

            if self.config.level in [OptimizationLevel.AGGRESSIVE, OptimizationLevel.ADAPTIVE]:
                # Optimize message routing
                tokens_saved += comm_optimizer.optimize_message_routing()

            if self.config.level == OptimizationLevel.ADAPTIVE:
                # Enable adaptive protocols
                tokens_saved += comm_optimizer.enable_adaptive_protocols()

            return tokens_saved

        except Exception as e:
            self.logger.warning(f"Communication optimization failed: {e}")
            return 0

    def _optimize_budgets(self) -> int:
        """Optimize budget allocations."""
        budget_manager = self.components.get('budget_manager')
        if not budget_manager:
            return 0

        try:
            # Get budget status
            budget_status = budget_manager.get_budget_status()

            tokens_saved = 0

            for constraint_id, status in budget_status.items():
                if isinstance(status, dict) and status.get('usage_percentage', 0) > 80:
                    # High usage, apply optimization
                    recommendations = budget_manager.get_optimization_recommendations(constraint_id)

                    if recommendations:
                        # Apply top recommendation
                        top_rec = recommendations[0]
                        result = budget_manager.apply_optimization_strategy(
                            constraint_id,
                            BudgetOptimizationStrategy(top_rec.strategy.value)
                        )
                        tokens_saved += result.get('tokens_saved', 0)

            return tokens_saved

        except Exception as e:
            self.logger.warning(f"Budget optimization failed: {e}")
            return 0

    def _run_advanced_optimization(self) -> int:
        """Run advanced optimization algorithms."""
        advanced_optimizer = self.components.get('advanced_optimizer')
        if not advanced_optimizer:
            return 0

        try:
            # Prepare context for optimization
            context = {
                "current_efficiency": self.metrics.efficiency_improvement,
                "cache_hit_rate": self.metrics.cache_hit_rate,
                "compression_ratio": self.metrics.compression_ratio,
                "budget_utilization": self.metrics.budget_utilization
            }

            # Run auto-optimization
            result = advanced_optimizer.auto_optimize(
                task_type="general_optimization",
                context=context,
                max_duration_seconds=60
            )

            return result.tokens_saved

        except Exception as e:
            self.logger.warning(f"Advanced optimization failed: {e}")
            return 0

    def process_task_request(self,
                           task_type: str,
                           content: str,
                           context: Dict[str, Any] = None) -> Tuple[str, int]:
        """Process a task request with optimization."""
        if not self.active or self.config.mode == IntegrationMode.MONITORING_ONLY:
            return content, len(content.split())  # Return original content

        tokens_saved = 0
        optimized_content = content

        try:
            # 1. Apply progressive loading if content is large
            progressive_loader = self.components.get('progressive_loader')
            if progressive_loader and len(content) > 5000:
                tier = LoadingTier.ESSENTIAL if self.config.level == OptimizationLevel.MINIMAL else LoadingTier.STANDARD
                loaded_content = progressive_loader.load_content(task_type, tier, context or {})
                optimized_content = loaded_content.get('content', content)
                tokens_saved += len(content.split()) - len(optimized_content.split())

            # 2. Apply caching
            smart_cache = self.components.get('smart_cache')
            if smart_cache:
                cache_key = f"{task_type}_{hash(content[:100])}"  # Use first 100 chars as cache key
                cached_result = smart_cache.get(cache_key)

                if cached_result:
                    optimized_content = cached_result.get('content', optimized_content)
                    tokens_saved += cached_result.get('tokens_saved', 0)
                else:
                    # Cache the result
                    smart_cache.set(cache_key, {
                        'content': optimized_content,
                        'tokens_saved': tokens_saved,
                        'timestamp': datetime.now()
                    })

            # 3. Apply compression if enabled
            comm_optimizer = self.components.get('communication_optimizer')
            if comm_optimizer and self.config.level in [OptimizationLevel.AGGRESSIVE, OptimizationLevel.ADAPTIVE]:
                compressed_result = comm_optimizer.compress_message(
                    optimized_content,
                    priority=MessagePriority.NORMAL,
                    compression_type=CompressionType.SEMANTIC
                )
                optimized_content = compressed_result.get('compressed_content', optimized_content)
                tokens_saved += compressed_result.get('tokens_saved', 0)

            # 4. Check budget constraints
            if self.config.budget_enforcement:
                budget_manager = self.components.get('budget_manager')
                if budget_manager:
                    # Try to allocate tokens
                    success, allocated = budget_manager.allocate_tokens(
                        constraint_id="task_default",  # Use default task constraint
                        requested=len(optimized_content.split()),
                        task_type=task_type,
                        context=context
                    )

                    if not success:
                        # Budget exceeded, apply aggressive optimization
                        optimized_content = self._emergency_optimization(optimized_content)
                        tokens_saved += len(content.split()) - len(optimized_content.split())

            return optimized_content, tokens_saved

        except Exception as e:
            self.logger.error(f"Task processing optimization failed: {e}")
            return content, 0

    def _emergency_optimization(self, content: str) -> str:
        """Emergency optimization when budget is exceeded."""
        # Apply aggressive content reduction
        lines = content.split('\n')
        essential_lines = []

        for line in lines:
            # Keep only essential lines (very basic heuristic)
            stripped = line.strip()
            if (stripped and
                not stripped.startswith('#') and
                len(stripped) > 10 and
                not stripped.startswith('<!--')):
                essential_lines.append(line)

            # Limit to top 50 lines
            if len(essential_lines) >= 50:
                break

        return '\n'.join(essential_lines)

    def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status."""
        return {
            "integration": asdict(self.status),
            "config": asdict(self.config),
            "components": {name: type(comp).__name__ for name, comp in self.components.items()},
            "recent_performance": self.performance_history[-10:] if self.performance_history else [],
            "optimization_results": self.optimization_results[-20:] if self.optimization_results else []
        }

    def get_optimization_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate comprehensive optimization report."""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        # Filter recent data
        recent_performance = [
            p for p in self.performance_history
            if p['timestamp'] > cutoff_time
        ]

        recent_optimizations = [
            o for o in self.optimization_results
            if o['timestamp'] > cutoff_time
        ]

        # Calculate statistics
        total_tokens_saved = sum(o['tokens_saved'] for o in recent_optimizations if o['success'])
        success_rate = sum(1 for o in recent_optimizations if o['success']) / len(recent_optimizations) if recent_optimizations else 0

        avg_efficiency = 0
        if recent_performance:
            efficiencies = [p['metrics']['efficiency_improvement'] for p in recent_performance]
            avg_efficiency = statistics.mean(efficiencies)

        # Get component-specific reports
        component_reports = {}
        for name, component in self.components.items():
            try:
                if hasattr(component, 'get_status_report'):
                    component_reports[name] = component.get_status_report()
                elif hasattr(component, 'get_report'):
                    component_reports[name] = component.get_report()
                else:
                    component_reports[name] = {"status": "active", "type": type(component).__name__}
            except Exception as e:
                component_reports[name] = {"status": "error", "error": str(e)}

        return {
            "report_period_hours": hours,
            "generated_at": datetime.now().isoformat(),
            "integration_status": asdict(self.status),
            "summary": {
                "total_tokens_saved": total_tokens_saved,
                "optimization_success_rate": success_rate,
                "average_efficiency_improvement": avg_efficiency,
                "total_optimizations": len(recent_optimizations),
                "uptime_hours": self.status.uptime_seconds / 3600 if self.status.uptime_seconds else 0
            },
            "current_metrics": asdict(self.metrics),
            "component_reports": component_reports,
            "recent_optimizations": recent_optimizations[-10:],  # Last 10 optimizations
            "recommendations": self._generate_recommendations()
        }

    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate optimization recommendations."""
        recommendations = []

        # Analyze current performance
        if self.metrics.cache_hit_rate < 0.7:
            recommendations.append({
                "type": "caching",
                "priority": "high",
                "description": "Cache hit rate is below optimal. Consider increasing cache size or improving cache strategy.",
                "potential_impact": "15-25% token reduction"
            })

        if self.metrics.compression_ratio > 0.8:
            recommendations.append({
                "type": "compression",
                "priority": "medium",
                "description": "Compression effectiveness could be improved. Consider enabling semantic compression.",
                "potential_impact": "10-20% token reduction"
            })

        if self.metrics.budget_utilization > 0.8:
            recommendations.append({
                "type": "budget",
                "priority": "high",
                "description": "Budget utilization is high. Consider enabling aggressive optimization or increasing budget limits.",
                "potential_impact": "Prevents service interruption"
            })

        if self.metrics.efficiency_improvement < 0.3:
            recommendations.append({
                "type": "general",
                "priority": "medium",
                "description": "Overall efficiency improvement is low. Consider upgrading to aggressive optimization mode.",
                "potential_impact": "20-40% improvement in token efficiency"
            })

        # Check component health
        inactive_components = [
            name for name, status in self.status.components_status.items()
            if not status
        ]

        if inactive_components:
            recommendations.append({
                "type": "maintenance",
                "priority": "critical",
                "description": f"Components inactive: {', '.join(inactive_components)}. Restart integration system.",
                "potential_impact": "Restore full optimization capabilities"
            })

        return recommendations

def main():
    """CLI interface for token optimization integration."""
    import argparse

    parser = argparse.ArgumentParser(description="Token Optimization Integration System")
    parser.add_argument("--data-dir", default=".claude-patterns", help="Data directory")
    parser.add_argument("--mode", choices=["monitoring_only", "optimization_active", "budget_enforced", "full_optimization"],
                       default="full_optimization", help="Integration mode")
    parser.add_argument("--level", choices=["minimal", "standard", "aggressive", "adaptive"],
                       default="standard", help="Optimization level")
    parser.add_argument("--start", action="store_true", help="Start integration system")
    parser.add_argument("--stop", action="store_true", help="Stop integration system")
    parser.add_argument("--status", action="store_true", help="Show integration status")
    parser.add_argument("--report", action="store_true", help="Generate optimization report")
    parser.add_argument("--report-hours", type=int, default=24, help="Report period in hours")
    parser.add_argument("--process-task", help="Process a task with optimization")
    parser.add_argument("--task-file", help="File containing task content")
    parser.add_argument("--monitoring-interval", type=int, default=60, help="Monitoring interval in seconds")
    parser.add_argument("--optimization-interval", type=int, default=300, help="Optimization interval in seconds")

    args = parser.parse_args()

    # Create configuration
    config = IntegrationConfig(
        mode=IntegrationMode(args.mode),
        level=OptimizationLevel(args.level),
        data_directory=args.data_dir,
        monitoring_interval=args.monitoring_interval,
        optimization_interval=args.optimization_interval
    )

    # Initialize integration
    integration = TokenOptimizationIntegration(config)

    if args.start:
        success = integration.start()
        print(f"Integration started: {success}")

        if success:
            print("Integration system is running. Press Ctrl+C to stop.")
            try:
                while integration.active:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping integration...")
                integration.stop()

    elif args.stop:
        integration.stop()
        print("Integration stopped")

    elif args.status:
        status = integration.get_integration_status()
        print(json.dumps(status, indent=2, default=str))

    elif args.report:
        report = integration.get_optimization_report(args.report_hours)
        print(json.dumps(report, indent=2, default=str))

    elif args.process_task:
        if not args.task_file:
            print("Error: --task-file required for task processing")
            return

        try:
            with open(args.task_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Start integration for processing
            integration.start()

            optimized_content, tokens_saved = integration.process_task_request(
                args.process_task,
                content
            )

            print(f"Original tokens: {len(content.split())}")
            print(f"Tokens saved: {tokens_saved}")
            print(f"Optimization ratio: {tokens_saved / len(content.split()):.2%}")
            print(f"\nOptimized content:\n{optimized_content}")

            integration.stop()

        except Exception as e:
            print(f"Error processing task: {e}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()