"""
Comprehensive Test Suite for Token Optimization Framework

Tests all components of the token optimization system to ensure
proper integration, functionality, and performance.

Test Categories:
- Unit tests for individual components
- Integration tests for component interaction
- Performance tests for optimization effectiveness
- Load tests for system scalability
- End-to-end workflow tests
"""

import os
import json
import unittest
import asyncio
import tempfile
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import time
import statistics
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from token_optimization_engine import TokenOptimizer, ContentType, ContentItem
    from progressive_content_loader import ProgressiveContentLoader, LoadingTier, ContentSection
    from autonomous_token_optimizer import AutonomousTokenOptimizer, TaskComplexity, OptimizationStrategy
    from smart_caching_system import SmartCache, CachePolicy, PredictionModel
    from agent_communication_optimizer import AgentCommunicationOptimizer, MessagePriority, CompressionType
    from token_monitoring_system import TokenMonitoringSystem, MetricType, AlertLevel
    from token_budget_manager import TokenBudgetManager, BudgetLevel, BudgetScope
    from advanced_token_optimizer import AdvancedTokenOptimizer, OptimizationObjective, AlgorithmType
    from token_optimization_integration import TokenOptimizationIntegration, IntegrationMode, OptimizationLevel, IntegrationConfig
except ImportError as e:
    print(f"Import error: {e}")
    print("Running in mock mode - tests will validate structure only")

    # Mock classes for testing when imports fail
    class TokenOptimizer:
        def __init__(self): self.enabled = False
        def enable_progressive_loading(self): return 100
        def enable_compression(self): return 150
        def enable_adaptive_optimization(self): return 200
        def get_current_usage_patterns(self): return {"patterns": []}

    class ProgressiveContentLoader:
        def __init__(self, data_dir): self.data_dir = data_dir
        def load_content(self, task_type, tier, context): return {"content": "test content", "tokens_saved": 50}

    class AutonomousTokenOptimizer:
        def __init__(self, data_dir): self.data_dir = data_dir
        def optimize_workflow(self, workflow): return {"tokens_saved": 75, "optimization_success": True}

    class SmartCache:
        def __init__(self, data_dir): self.data_dir = data_dir
        def get(self, key): return None
        def set(self, key, value): pass
        def get_cache_stats(self): return {"hit_rate": 0.85}
        def optimize_cache_strategy(self): return 100
        def enable_predictive_caching(self): return 120

    class AgentCommunicationOptimizer:
        def __init__(self, data_dir): self.data_dir = data_dir
        def compress_message(self, content, priority, compression_type): return {"compressed_content": content, "tokens_saved": 80}
        def get_communication_patterns(self): return {"patterns": []}
        def enable_compression(self): return 90
        def optimize_message_routing(self): return 60
        def enable_adaptive_protocols(self): return 110
        def get_compression_stats(self): return {"avg_compression": 0.7}

    class TokenMonitoringSystem:
        def __init__(self, db_path, data_dir): self.db_path = db_path
        def record_metric(self, metric_type, value, source, tags, context): pass
        def get_recent_metrics(self, hours, metric_type): return []
        def create_alert(self, level, message, source, tags): pass
        def get_status_report(self): return {"status": "active"}

    class TokenBudgetManager:
        def __init__(self, db_path, data_dir): self.db_path = db_path
        def create_budget_constraint(self, level, scope, limit, tags): return "test_constraint"
        def allocate_tokens(self, constraint_id, requested, task_type, agent_name, context): return True, requested
        def get_budget_status(self, constraint_id): return {"usage_percentage": 0.6}
        def get_optimization_recommendations(self, constraint_id): return []
        def apply_optimization_strategy(self, constraint_id, strategy): return {"tokens_saved": 130}

    class AdvancedTokenOptimizer:
        def __init__(self, data_dir): self.data_dir = data_dir
        def auto_optimize(self, task_type, context, max_duration_seconds):
            return type('Result', (), {"tokens_saved": 95, "efficiency_improvement": 0.8, "success": True})()

    class TokenOptimizationIntegration:
        def __init__(self, config): self.config = config; self.active = False
        def start(self): self.active = True; return True
        def stop(self): self.active = False
        def process_task_request(self, task_type, content, context): return content, 100
        def get_integration_status(self): return {"active": self.active}
        def get_optimization_report(self, hours): return {"summary": {"total_tokens_saved": 1000}}

class TestTokenOptimizer(unittest.TestCase):
    """Test cases for TokenOptimizer component."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.optimizer = TokenOptimizer()

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_progressive_loading_enabling(self):
        """Test enabling progressive loading."""
        tokens_saved = self.optimizer.enable_progressive_loading()
        self.assertIsInstance(tokens_saved, int)
        self.assertGreaterEqual(tokens_saved, 0)

    def test_compression_enabling(self):
        """Test enabling compression."""
        tokens_saved = self.optimizer.enable_compression()
        self.assertIsInstance(tokens_saved, int)
        self.assertGreaterEqual(tokens_saved, 0)

    def test_adaptive_optimization_enabling(self):
        """Test enabling adaptive optimization."""
        tokens_saved = self.optimizer.enable_adaptive_optimization()
        self.assertIsInstance(tokens_saved, int)
        self.assertGreaterEqual(tokens_saved, 0)

    def test_usage_patterns_collection(self):
        """Test collection of usage patterns."""
        patterns = self.optimizer.get_current_usage_patterns()
        self.assertIsInstance(patterns, dict)

class TestProgressiveContentLoader(unittest.TestCase):
    """Test cases for ProgressiveContentLoader component."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.loader = ProgressiveContentLoader(self.temp_dir)

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_content_loading_essential_tier(self):
        """Test loading content with essential tier."""
        result = self.loader.load_content("test_task", LoadingTier.ESSENTIAL, {})
        self.assertIsInstance(result, dict)
        self.assertIn('content', result)

    def test_content_loading_standard_tier(self):
        """Test loading content with standard tier."""
        result = self.loader.load_content("test_task", LoadingTier.STANDARD, {})
        self.assertIsInstance(result, dict)
        self.assertIn('content', result)

    def test_content_loading_comprehensive_tier(self):
        """Test loading content with comprehensive tier."""
        result = self.loader.load_content("test_task", LoadingTier.COMPREHENSIVE, {})
        self.assertIsInstance(result, dict)
        self.assertIn('content', result)

class TestSmartCache(unittest.TestCase):
    """Test cases for SmartCache component."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = SmartCache(self.temp_dir)

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cache_set_and_get(self):
        """Test cache set and get operations."""
        test_key = "test_key"
        test_value = {"content": "test content", "timestamp": datetime.now()}

        # Set value
        self.cache.set(test_key, test_value)

        # Get value
        retrieved = self.cache.get(test_key)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['content'], test_value['content'])

    def test_cache_miss(self):
        """Test cache miss scenario."""
        result = self.cache.get("non_existent_key")
        self.assertIsNone(result)

    def test_cache_stats(self):
        """Test cache statistics."""
        stats = self.cache.get_cache_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn('hit_rate', stats)

    def test_cache_optimization(self):
        """Test cache optimization."""
        tokens_saved = self.cache.optimize_cache_strategy()
        self.assertIsInstance(tokens_saved, int)
        self.assertGreaterEqual(tokens_saved, 0)

class TestAgentCommunicationOptimizer(unittest.TestCase):
    """Test cases for AgentCommunicationOptimizer component."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.optimizer = AgentCommunicationOptimizer(self.temp_dir)

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_message_compression(self):
        """Test message compression."""
        test_content = "This is a test message for compression"
        result = self.optimizer.compress_message(
            test_content,
            MessagePriority.NORMAL,
            CompressionType.SEMANTIC
        )

        self.assertIsInstance(result, dict)
        self.assertIn('compressed_content', result)
        self.assertIn('tokens_saved', result)

    def test_communication_patterns(self):
        """Test communication patterns analysis."""
        patterns = self.optimizer.get_communication_patterns()
        self.assertIsInstance(patterns, dict)

    def test_compression_stats(self):
        """Test compression statistics."""
        stats = self.optimizer.get_compression_stats()
        self.assertIsInstance(stats, dict)

class TestTokenMonitoringSystem(unittest.TestCase):
    """Test cases for TokenMonitoringSystem component."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(self.temp_dir, "test_monitoring.db")
        self.monitoring = TokenMonitoringSystem(db_path, self.temp_dir)

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_metric_recording(self):
        """Test token metric recording."""
        self.monitoring.record_metric(
            MetricType.TOKEN_USAGE,
            1000,
            "test_source",
            {"test": "tag"},
            {"context": "data"}
        )
        # No exception means success

    def test_alert_creation(self):
        """Test alert creation."""
        self.monitoring.create_alert(
            AlertLevel.WARNING,
            "Test alert message",
            "test_source",
            {"test": "tag"}
        )
        # No exception means success

    def test_recent_metrics_retrieval(self):
        """Test retrieval of recent metrics."""
        # Record some test metrics
        for i in range(5):
            self.monitoring.record_metric(
                MetricType.TOKEN_USAGE,
                100 * i,
                "test_source"
            )

        # Retrieve recent metrics
        metrics = self.monitoring.get_recent_metrics(1, MetricType.TOKEN_USAGE)
        self.assertIsInstance(metrics, list)

class TestTokenBudgetManager(unittest.TestCase):
    """Test cases for TokenBudgetManager component."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(self.temp_dir, "test_budgets.db")
        self.budget_manager = TokenBudgetManager(db_path, self.temp_dir)

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_budget_constraint_creation(self):
        """Test budget constraint creation."""
        constraint_id = self.budget_manager.create_budget_constraint(
            level=BudgetLevel.TASK,
            scope=BudgetScope.TASK_BASED,
            limit=1000,
            tags={"test": "constraint"}
        )

        self.assertIsInstance(constraint_id, str)
        self.assertGreater(len(constraint_id), 0)

    def test_token_allocation(self):
        """Test token allocation."""
        # Create constraint first
        constraint_id = self.budget_manager.create_budget_constraint(
            level=BudgetLevel.TASK,
            scope=BudgetScope.TASK_BASED,
            limit=1000
        )

        # Allocate tokens
        success, allocated = self.budget_manager.allocate_tokens(
            constraint_id,
            500,
            "test_task",
            "test_agent"
        )

        self.assertTrue(success)
        self.assertEqual(allocated, 500)

    def test_budget_status(self):
        """Test budget status retrieval."""
        status = self.budget_manager.get_budget_status()
        self.assertIsInstance(status, dict)

class TestAdvancedTokenOptimizer(unittest.TestCase):
    """Test cases for AdvancedTokenOptimizer component."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.optimizer = AdvancedTokenOptimizer(self.temp_dir)

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_auto_optimization(self):
        """Test automatic optimization."""
        context = {
            "current_efficiency": 0.6,
            "task_complexity": "medium"
        }

        result = self.optimizer.auto_optimize(
            task_type="test_task",
            context=context,
            max_duration_seconds=10
        )

        self.assertTrue(hasattr(result, 'tokens_saved'))
        self.assertTrue(hasattr(result, 'success'))
        self.assertIsInstance(result.tokens_saved, int)

class TestTokenOptimizationIntegration(unittest.TestCase):
    """Test cases for TokenOptimizationIntegration component."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = IntegrationConfig(
            mode=IntegrationMode.FULL_OPTIMIZATION,
            level=OptimizationLevel.STANDARD,
            data_directory=self.temp_dir,
            monitoring_interval=1,
            optimization_interval=2
        )
        self.integration = TokenOptimizationIntegration(self.config)

    def tearDown(self):
        """Clean up test environment."""
        if self.integration.active:
            self.integration.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_integration_start_stop(self):
        """Test integration start and stop."""
        # Start integration
        success = self.integration.start()
        self.assertTrue(success)
        self.assertTrue(self.integration.active)

        # Stop integration
        self.integration.stop()
        self.assertFalse(self.integration.active)

    def test_task_processing(self):
        """Test task processing with optimization."""
        test_content = "This is a test task content for optimization testing."
        test_context = {"task_type": "test", "priority": "normal"}

        optimized_content, tokens_saved = self.integration.process_task_request(
            "test_task",
            test_content,
            test_context
        )

        self.assertIsInstance(optimized_content, str)
        self.assertIsInstance(tokens_saved, int)
        self.assertGreaterEqual(tokens_saved, 0)

    def test_integration_status(self):
        """Test integration status retrieval."""
        status = self.integration.get_integration_status()
        self.assertIsInstance(status, dict)
        self.assertIn('integration', status)
        self.assertIn('config', status)

    def test_optimization_report(self):
        """Test optimization report generation."""
        report = self.integration.get_optimization_report(1)  # 1 hour
        self.assertIsInstance(report, dict)
        self.assertIn('summary', report)
        self.assertIn('current_metrics', report)

class TestPerformanceOptimization(unittest.TestCase):
    """Performance tests for optimization effectiveness."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = IntegrationConfig(
            mode=IntegrationMode.FULL_OPTIMIZATION,
            level=OptimizationLevel.AGGRESSIVE,
            data_directory=self.temp_dir,
            monitoring_interval=1,
            optimization_interval=1
        )
        self.integration = TokenOptimizationIntegration(self.config)

    def tearDown(self):
        """Clean up test environment."""
        if self.integration.active:
            self.integration.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_optimization_effectiveness(self):
        """Test optimization effectiveness over multiple tasks."""
        # Start integration
        self.integration.start()

        # Process multiple tasks
        tasks = [
            ("analysis_task", "Perform code analysis and optimization"),
            ("documentation_task", "Generate comprehensive documentation"),
            ("testing_task", "Run comprehensive test suite"),
            ("optimization_task", "Optimize performance and efficiency"),
            ("reporting_task", "Generate detailed reports and metrics")
        ]

        original_tokens = 0
        saved_tokens = 0

        for task_type, content in tasks:
            content_tokens = len(content.split())
            original_tokens += content_tokens

            optimized_content, tokens_saved = self.integration.process_task_request(
                task_type,
                content,
                {"priority": "high"}
            )

            saved_tokens += tokens_saved

        # Stop integration
        self.integration.stop()

        # Calculate optimization ratio
        if original_tokens > 0:
            optimization_ratio = saved_tokens / original_tokens
            self.assertGreater(optimization_ratio, 0.1, "Optimization should save at least 10% of tokens")

        print(f"Original tokens: {original_tokens}")
        print(f"Tokens saved: {saved_tokens}")
        print(f"Optimization ratio: {optimization_ratio:.2%}")

    def test_load_performance(self):
        """Test system performance under load."""
        self.integration.start()

        # Simulate high load
        start_time = time.time()
        task_count = 50

        for i in range(task_count):
            content = f"Task {i} content for performance testing under load conditions"
            optimized_content, tokens_saved = self.integration.process_task_request(
                f"load_test_task_{i}",
                content,
                {"batch_id": i}
            )

        end_time = time.time()
        total_time = end_time - start_time
        avg_time_per_task = total_time / task_count

        self.integration.stop()

        # Performance assertions
        self.assertLess(avg_time_per_task, 0.1, "Average processing time should be under 100ms")
        self.assertLess(total_time, 10, "Total processing time should be under 10 seconds")

        print(f"Processed {task_count} tasks in {total_time:.2f} seconds")
        print(f"Average time per task: {avg_time_per_task*1000:.2f}ms")

class TestEndToEndWorkflows(unittest.TestCase):
    """End-to-end workflow tests."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = IntegrationConfig(
            mode=IntegrationMode.FULL_OPTIMIZATION,
            level=OptimizationLevel.ADAPTIVE,
            data_directory=self.temp_dir,
            monitoring_interval=1,
            optimization_interval=2
        )
        self.integration = TokenOptimizationIntegration(self.config)

    def tearDown(self):
        """Clean up test environment."""
        if self.integration.active:
            self.integration.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_autonomous_agent_workflow(self):
        """Test complete autonomous agent workflow."""
        self.integration.start()

        # Simulate autonomous agent workflow
        workflow_steps = [
            ("task_analysis", "Analyze task requirements and constraints"),
            ("planning", "Create execution plan and strategy"),
            ("implementation", "Implement solution with optimizations"),
            ("testing", "Run tests and validation"),
            ("documentation", "Generate documentation and reports"),
            ("optimization", "Apply final optimizations and improvements")
        ]

        workflow_tokens_saved = 0
        step_results = []

        for step_name, content in workflow_steps:
            optimized_content, tokens_saved = self.integration.process_task_request(
                step_name,
                content,
                {
                    "workflow": "autonomous_agent",
                    "step": step_name,
                    "priority": "high"
                }
            )

            workflow_tokens_saved += tokens_saved
            step_results.append({
                "step": step_name,
                "original_length": len(content.split()),
                "optimized_length": len(optimized_content.split()),
                "tokens_saved": tokens_saved
            })

        self.integration.stop()

        # Validate workflow results
        self.assertGreater(workflow_tokens_saved, 0, "Workflow should save tokens")

        # Print workflow summary
        print("Autonomous Agent Workflow Results:")
        for result in step_results:
            print(f"  {result['step']}: {result['tokens_saved']} tokens saved")

        print(f"Total workflow tokens saved: {workflow_tokens_saved}")

    def test_multi_agent_coordination(self):
        """Test multi-agent coordination with optimization."""
        self.integration.start()

        # Simulate multiple agents working together
        agents = ["analyzer", "optimizer", "validator", "reporter"]
        coordination_tasks = []

        for agent in agents:
            for other_agent in agents:
                if agent != other_agent:
                    # Agent communication task
                    message = f"Coordination message from {agent} to {other_agent}"
                    optimized_content, tokens_saved = self.integration.process_task_request(
                        f"agent_communication_{agent}_{other_agent}",
                        message,
                        {
                            "sender": agent,
                            "receiver": other_agent,
                            "type": "coordination"
                        }
                    )

                    coordination_tasks.append({
                        "sender": agent,
                        "receiver": other_agent,
                        "tokens_saved": tokens_saved
                    })

        self.integration.stop()

        # Validate coordination results
        total_coordination_savings = sum(task['tokens_saved'] for task in coordination_tasks)
        self.assertGreater(total_coordination_savings, 0, "Agent coordination should save tokens")

        print(f"Multi-agent coordination tokens saved: {total_coordination_savings}")

def run_performance_benchmark():
    """Run performance benchmark for the optimization system."""
    print("\n" + "="*60)
    print("PERFORMANCE BENCHMARK")
    print("="*60)

    temp_dir = tempfile.mkdtemp()
    config = IntegrationConfig(
        mode=IntegrationMode.FULL_OPTIMIZATION,
        level=OptimizationLevel.AGGRESSIVE,
        data_directory=temp_dir,
        monitoring_interval=1,
        optimization_interval=1
    )

    integration = TokenOptimizationIntegration(config)

    try:
        integration.start()

        # Benchmark scenarios
        scenarios = [
            ("Small Tasks", ["Small task content"] * 100),
            ("Medium Tasks", ["This is a medium sized task content for testing purposes"] * 50),
            ("Large Tasks", ["This is a large task content with comprehensive details and extensive information for testing the optimization system performance under various conditions and workloads"] * 20),
            ("Mixed Tasks", [
                "Small task",
                "Medium task content with some details",
                "Large task content with comprehensive information and extensive details for performance testing"
            ] * 30)
        ]

        for scenario_name, tasks in scenarios:
            print(f"\n{scenario_name}:")
            start_time = time.time()

            total_saved = 0
            for i, task in enumerate(tasks):
                optimized, saved = integration.process_task_request(
                    f"benchmark_task_{i}",
                    task,
                    {"scenario": scenario_name}
                )
                total_saved += saved

            end_time = time.time()
            duration = end_time - start_time

            print(f"  Tasks processed: {len(tasks)}")
            print(f"  Total time: {duration:.3f}s")
            print(f"  Average time per task: {duration/len(tasks)*1000:.2f}ms")
            print(f"  Total tokens saved: {total_saved}")
            print(f"  Average tokens saved per task: {total_saved/len(tasks):.1f}")

        # Generate final report
        report = integration.get_optimization_report(1)
        print(f"\nFinal Optimization Report:")
        print(f"  Total tokens saved: {report['summary']['total_tokens_saved']}")
        print(f"  Success rate: {report['summary']['optimization_success_rate']:.2%}")
        print(f"  Average efficiency: {report['summary']['average_efficiency_improvement']:.2%}")

    finally:
        integration.stop()
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    """Main test runner."""
    print("Token Optimization Framework Test Suite")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test cases
    test_classes = [
        TestTokenOptimizer,
        TestProgressiveContentLoader,
        TestSmartCache,
        TestAgentCommunicationOptimizer,
        TestTokenMonitoringSystem,
        TestTokenBudgetManager,
        TestAdvancedTokenOptimizer,
        TestTokenOptimizationIntegration,
        TestPerformanceOptimization,
        TestEndToEndWorkflows
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Run performance benchmark
    if result.wasSuccessful():
        run_performance_benchmark()
    else:
        print("\nSkipping performance benchmark due to test failures.")

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")

    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")

    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")

    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    exit(main())