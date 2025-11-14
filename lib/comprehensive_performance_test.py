#!/usr/bin/env python3
#     Comprehensive Performance Testing Suite for Autonomous Agent Plugin
"""
Tests command execution, resource utilization, context management, and scalability
"""
import time
import json
import psutil
import threading
import traceback
import gc
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import subprocess
import statistics


class PerformanceTestSuite:
    """Comprehensive performance testing suite"""

    def __init__(self, test_dir: str = ".claude-patterns"):
        """Initialize the processor with default configuration."""
        self.test_dir = Path(test_dir)
        self.test_dir.mkdir(parents=True, exist_ok=True)

        # Performance metrics storage
        self.results = {
            "test_session": {
                "start_time": datetime.now().isoformat(),
                "platform": sys.platform,
                "python_version": sys.version,
                "plugin_version": self._get_plugin_version(),
            },
            "command_performance": {},
            "resource_utilization": {},
            "context_management": {},
            "scalability_tests": {},
            "stress_tests": {},
            "memory_leak_tests": {},
            "summary": {},
        }

        # Performance baselines
        self.baselines = {
            "fast_command": 0.5,  # seconds
            "medium_command": 2.0,
            "slow_command": 5.0,
            "max_memory_growth": 50 * 1024 * 1024,  # 50MB
            "max_cpu_usage": 80,  # percentage
            "acceptable_error_rate": 5,  # percentage
        }

        # Test commands to benchmark
        self.test_commands = [
            # Fast commands
            {"category": "fast", "command": "python lib/validate_plugin.py", "expected_time": 0.5},
            {"category": "fast", "command": "python lib/simple_test_script.py", "expected_time": 0.5},
            # Medium commands
            {"category": "medium", "command": "python lib/comprehensive_quality_analysis.py --dir .", "expected_time": 2.0},
            {"category": "medium", "command": "python lib/plugin_validator.py", "expected_time": 2.0},
            # Slow commands
            {
                "category": "slow",
                "command": "python lib/dashboard_launcher.py --no-browser --validate-only",
                "expected_time": 5.0,
            },
        ]

    def _get_plugin_version(self) -> str:
        """Get plugin version from plugin.json"""
        try:
            plugin_file = Path(".claude-plugin/plugin.json")
            if plugin_file.exists():
                with open(plugin_file, "r") as f:
                    data = json.load(f)
                    return data.get("version", "unknown")
        except:
            pass
        return "unknown"

    def _get_process_metrics(self) -> Dict[str, float]:
        """Get current process resource metrics"""
        process = psutil.Process()
        return {
            "memory_rss": process.memory_info().rss,
            "memory_vms": process.memory_info().vms,
            "cpu_percent": process.cpu_percent(),
            "num_threads": process.num_threads(),
            "open_files": len(process.open_files()),
            "memory_percent": process.memory_percent(),
        }

    def _execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute command and measure performance"""
        start_time = time.time()
        start_metrics = self._get_process_metrics()

        try:
            # Force garbage collection before test
            gc.collect()

            # Execute command with timeout
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout, cwd=os.getcwd())

            end_time = time.time()
            end_metrics = self._get_process_metrics()

            # Calculate deltas
            execution_time = end_time - start_time
            memory_delta = end_metrics["memory_rss"] - start_metrics["memory_rss"]

            return {
                "success": result.returncode == 0,
                "execution_time": execution_time,
                "memory_delta": memory_delta,
                "memory_peak": end_metrics["memory_rss"],
                "cpu_usage": end_metrics["cpu_percent"],
                "return_code": result.returncode,
                "stdout_length": len(result.stdout) if result.stdout else 0,
                "stderr_length": len(result.stderr) if result.stderr else 0,
                "error": None,
                "start_memory": start_metrics["memory_rss"],
                "end_memory": end_metrics["memory_rss"],
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "execution_time": timeout,
                "memory_delta": 0,
                "memory_peak": 0,
                "cpu_usage": 0,
                "return_code": -1,
                "stdout_length": 0,
                "stderr_length": 0,
                "error": f"Command timed out after {timeout} seconds",
                "start_memory": start_metrics["memory_rss"],
                "end_memory": start_metrics["memory_rss"],
            }
        except Exception as e:
            end_time = time.time()
            return {
                "success": False,
                "execution_time": end_time - start_time,
                "memory_delta": 0,
                "memory_peak": 0,
                "cpu_usage": 0,
                "return_code": -2,
                "stdout_length": 0,
                "stderr_length": 0,
                "error": str(e),
                "start_memory": start_metrics["memory_rss"],
                "end_memory": start_metrics["memory_rss"],
            }

    def test_command_performance(self) -> Dict[str, Any]:
        """Test command execution performance"""
        print("Testing command execution performance...")

        category_results = {
            "fast": {"times": [], "memory_usage": [], "success_rate": 0},
            "medium": {"times": [], "memory_usage": [], "success_rate": 0},
            "slow": {"times": [], "memory_usage": [], "success_rate": 0},
        }

        detailed_results = []

        for test_cmd in self.test_commands:
            category = test_cmd["category"]
            command = test_cmd["command"]
            expected_time = test_cmd["expected_time"]

            print(f"  Testing {category} command: {command[:50]}...")

            # Run command multiple times for statistical significance
            runs = []
            for i in range(3):
                result = self._execute_command(command)
                runs.append(result)

                # Small delay between runs
                time.sleep(0.5)

            # Calculate statistics
            execution_times = [r["execution_time"] for r in runs if r["success"]]
            memory_deltas = [r["memory_delta"] for r in runs if r["success"]]
            success_count = sum(1 for r in runs if r["success"])

            if execution_times:
                avg_time = statistics.mean(execution_times)
                min_time = min(execution_times)
                max_time = max(execution_times)
                std_dev = statistics.stdev(execution_times) if len(execution_times) > 1 else 0
                avg_memory = statistics.mean(memory_deltas) if memory_deltas else 0
                success_rate = (success_count / len(runs)) * 100
            else:
                avg_time = min_time = max_time = std_dev = avg_memory = success_rate = 0

            # Store results
            category_results[category]["times"].extend(execution_times)
            category_results[category]["memory_usage"].extend(memory_deltas)
            category_results[category]["success_rate"] = success_rate

            detailed_results.append(
                {
                    "command": command,
                    "category": category,
                    "expected_time": expected_time,
                    "avg_time": avg_time,
                    "min_time": min_time,
                    "max_time": max_time,
                    "std_dev": std_dev,
                    "avg_memory_delta": avg_memory,
                    "success_rate": success_rate,
                    "performance_vs_expected": (expected_time / avg_time * 100) if avg_time > 0 else 0,
                    "runs": runs,
                }
            )

            print(f"    Avg time: {avg_time:.3f}s, Success rate: {success_rate:.1f}%")

        # Calculate category summaries
        category_summaries = {}
        for category, data in category_results.items():
            if data["times"]:
                category_summaries[category] = {
                    "avg_execution_time": statistics.mean(data["times"]),
                    "min_execution_time": min(data["times"]),
                    "max_execution_time": max(data["times"]),
                    "std_deviation": statistics.stdev(data["times"]) if len(data["times"]) > 1 else 0,
                    "avg_memory_delta": statistics.mean(data["memory_usage"]) if data["memory_usage"] else 0,
                    "success_rate": data["success_rate"],
                    "total_runs": len(data["times"]) + (3 - len(data["times"])),  # Include failed runs
                }
            else:
                category_summaries[category] = {
                    "avg_execution_time": 0,
                    "min_execution_time": 0,
                    "max_execution_time": 0,
                    "std_deviation": 0,
                    "avg_memory_delta": 0,
                    "success_rate": 0,
                    "total_runs": 0,
                }

        return {
            "category_summaries": category_summaries,
            "detailed_results": detailed_results,
            "overall_success_rate": sum(len(data["times"]) for data in category_results.values())
            / sum(data["total_runs"] for data in category_summaries.values())
            * 100,
        }

    def test_resource_utilization(self) -> Dict[str, Any]:
        """Test resource utilization during command execution"""
        print("Testing resource utilization...")

        resource_samples = []

        # Select a representative medium command for resource testing
        test_command = "python lib/comprehensive_quality_analysis.py --dir ."

        # Start resource monitoring thread
        monitoring_active = True
        resource_data = []

        def monitor_resources():
            """Monitor Resources."""
            while monitoring_active:
                try:
                    metrics = self._get_process_metrics()
                    resource_data.append(
                        {
                            "timestamp": time.time(),
                            "memory_rss": metrics["memory_rss"],
                            "memory_percent": metrics["memory_percent"],
                            "cpu_percent": metrics["cpu_percent"],
                            "num_threads": metrics["num_threads"],
                        }
                    )
                    time.sleep(0.1)  # Sample every 100ms
                except:
                    break

        # Start monitoring
        monitor_thread = threading.Thread(target=monitor_resources)
        monitor_thread.start()

        # Execute the command
        start_time = time.time()
        result = self._execute_command(test_command, timeout=60)
        end_time = time.time()

        # Stop monitoring
        monitoring_active = False
        monitor_thread.join(timeout=1)

        # Analyze resource data
        if resource_data:
            memory_usage = [d["memory_rss"] for d in resource_data]
            cpu_usage = [d["cpu_percent"] for d in resource_data]
            thread_count = [d["num_threads"] for d in resource_data]

            resource_analysis = {
                "execution_time": end_time - start_time,
                "memory_stats": {
                    "initial": memory_usage[0] if memory_usage else 0,
                    "peak": max(memory_usage) if memory_usage else 0,
                    "final": memory_usage[-1] if memory_usage else 0,
                    "avg": statistics.mean(memory_usage) if memory_usage else 0,
                    "growth": (memory_usage[-1] - memory_usage[0]) if len(memory_usage) > 1 else 0,
                },
                "cpu_stats": {
                    "peak": max(cpu_usage) if cpu_usage else 0,
                    "avg": statistics.mean(cpu_usage) if cpu_usage else 0,
                    "samples_above_50": sum(1 for c in cpu_usage if c > 50),
                    "samples_above_80": sum(1 for c in cpu_usage if c > 80),
                },
                "thread_stats": {
                    "initial": thread_count[0] if thread_count else 0,
                    "peak": max(thread_count) if thread_count else 0,
                    "final": thread_count[-1] if thread_count else 0,
                },
                "sample_count": len(resource_data),
                "command_result": result,
            }
        else:
            resource_analysis = {
                "execution_time": end_time - start_time,
                "memory_stats": {},
                "cpu_stats": {},
                "thread_stats": {},
                "sample_count": 0,
                "command_result": result,
                "error": "No resource data collected",
            }

        return resource_analysis

    def test_scalability(self) -> Dict[str, Any]:
        """Test plugin scalability with concurrent execution"""
        print("Testing scalability with concurrent execution...")

        def run_concurrent_test(num_workers: int) -> Dict[str, Any]:
            """Run concurrent test with specified number of workers"""
            commands = [
                "python lib/validate_plugin.py",
                "python lib/simple_test_script.py",
                "python lib/command_validator.py --help",
            ]

            start_time = time.time()
            start_metrics = self._get_process_metrics()

            results = []

            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                # Submit commands multiple times
                futures = []
                for _ in range(num_workers * 2):  # 2 commands per worker
                    cmd = commands[_ % len(commands)]
                    future = executor.submit(self._execute_command, cmd)
                    futures.append(future)

                # Collect results
                for future in futures:
                    try:
                        result = future.result(timeout=30)
                        results.append(result)
                    except TimeoutError:
                        results.append({"success": False, "execution_time": 30, "error": "Future timeout"})
                    except Exception as e:
                        results.append({"success": False, "execution_time": 0, "error": str(e)})

            end_time = time.time()
            end_metrics = self._get_process_metrics()

            # Calculate statistics
            successful_results = [r for r in results if r["success"]]
            total_time = end_time - start_time

            return {
                "workers": num_workers,
                "total_commands": len(results),
                "successful_commands": len(successful_results),
                "success_rate": (len(successful_results) / len(results)) * 100,
                "total_time": total_time,
                "avg_command_time": (
                    statistics.mean([r["execution_time"] for r in successful_results]) if successful_results else 0
                ),
                "commands_per_second": len(results) / total_time,
                "memory_growth": end_metrics["memory_rss"] - start_metrics["memory_rss"],
                "peak_memory": max(r["memory_peak"] for r in results if r.get("memory_peak")) if results else 0,
                "results": results,
            }

        # Test with different numbers of workers
        scalability_results = {}
        for workers in [1, 2, 4, 8]:
            print(f"  Testing with {workers} concurrent workers...")
            result = run_concurrent_test(workers)
            scalability_results[f"{workers}_workers"] = result
            print(f"    Success rate: {result['success_rate']:.1f}%, Commands/sec: {result['commands_per_second']:.1f}")

        return scalability_results

    def test_memory_leaks(self) -> Dict[str, Any]:
        """Test for memory leaks during repeated command execution"""
        print("Testing for memory leaks...")

        # Command to execute repeatedly
        test_command = "python lib/validate_plugin.py"
        iterations = 20

        memory_samples = []
        execution_times = []

        initial_metrics = self._get_process_metrics()
        initial_memory = initial_metrics["memory_rss"]

        print(f"  Executing command {iterations} times...")

        for i in range(iterations):
            # Execute command
            result = self._execute_command(test_command)
            execution_times.append(result["execution_time"])

            # Force garbage collection
            gc.collect()

            # Measure memory
            current_metrics = self._get_process_metrics()
            memory_samples.append(current_metrics["memory_rss"])

            if (i + 1) % 5 == 0:
                print(f"    Iteration {i + 1}: Memory: {current_metrics['memory_rss'] / 1024 / 1024:.1f} MB")

            # Small delay between iterations
            time.sleep(0.1)

        # Final garbage collection and measurement
        gc.collect()
        final_metrics = self._get_process_metrics()
        final_memory = final_metrics["memory_rss"]

        # Analyze memory growth
        memory_growth = final_memory - initial_memory
        memory_trend = "stable"

        if len(memory_samples) > 1:
            # Simple linear regression to detect trend
            x = list(range(len(memory_samples)))
            n = len(memory_samples)
            sum_x = sum(x)
            sum_y = sum(memory_samples)
            sum_xy = sum(x[i] * memory_samples[i] for i in range(n))
            sum_x2 = sum(xi * xi for xi in x)

            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)

            if slope > 100000:  # Growing by more than 100KB per iteration
                memory_trend = "leaking"
            elif slope > 50000:
                memory_trend = "growing"
            elif slope < -50000:
                memory_trend = "decreasing"

        return {
            "iterations": iterations,
            "initial_memory_mb": initial_memory / 1024 / 1024,
            "final_memory_mb": final_memory / 1024 / 1024,
            "memory_growth_mb": memory_growth / 1024 / 1024,
            "memory_trend": memory_trend,
            "peak_memory_mb": max(memory_samples) / 1024 / 1024 if memory_samples else 0,
            "avg_execution_time": statistics.mean(execution_times) if execution_times else 0,
            "execution_time_std": statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
            "memory_samples_mb": [m / 1024 / 1024 for m in memory_samples],
            "leak_detected": memory_trend == "leaking" or memory_growth > self.baselines["max_memory_growth"],
        }

    def test_context_management(self) -> Dict[str, Any]:
        """Test context management and cleanup"""
        print("Testing context management...")

        # Simulate context by running multiple different commands
        commands_sequence = [
            "python lib/validate_plugin.py",
            "python lib/simple_test_script.py",
            "python lib/command_validator.py --help",
            "python lib/plugin_validator.py",
            "python lib/validate_yaml_frontmatter.py --help",
        ]

        context_samples = []

        for cycle in range(3):  # 3 cycles of all commands
            print(f"  Context cycle {cycle + 1}/3")

            for cmd in commands_sequence:
                # Measure context before command
                before_metrics = self._get_process_metrics()

                # Execute command
                result = self._execute_command(cmd)

                # Force cleanup
                gc.collect()

                # Measure context after command
                after_metrics = self._get_process_metrics()

                context_samples.append(
                    {
                        "cycle": cycle,
                        "command": cmd,
                        "before_memory": before_metrics["memory_rss"],
                        "after_memory": after_metrics["memory_rss"],
                        "memory_delta": after_metrics["memory_rss"] - before_metrics["memory_rss"],
                        "execution_time": result["execution_time"],
                        "success": result["success"],
                    }
                )

        # Analyze context behavior
        memory_deltas = [s["memory_delta"] for s in context_samples]
        successful_samples = [s for s in context_samples if s["success"]]

        return {
            "total_commands": len(context_samples),
            "successful_commands": len(successful_samples),
            "success_rate": (len(successful_samples) / len(context_samples)) * 100,
            "avg_memory_delta": statistics.mean(memory_deltas) if memory_deltas else 0,
            "max_memory_delta": max(memory_deltas) if memory_deltas else 0,
            "min_memory_delta": min(memory_deltas) if memory_deltas else 0,
            "context_stability": len([d for d in memory_deltas if abs(d) < 10 * 1024 * 1024])
            / len(memory_deltas)
            * 100,  # Within 10MB
            "samples": context_samples,
        }

    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        print("\nGenerating comprehensive performance report...")

        # Calculate overall performance metrics
        command_perf = self.results["command_performance"]
        resource_perf = self.results["resource_utilization"]
        scalability_perf = self.results["scalability_tests"]
        memory_perf = self.results["memory_leak_tests"]
        context_perf = self.results["context_management"]

        # Overall performance score (0-100)
        performance_score = 0
        score_factors = []

        # Command execution performance (30%)
        if command_perf.get("overall_success_rate", 0) >= 95:
            performance_score += 30
            score_factors.append("Command execution: Excellent (30/30)")
        elif command_perf.get("overall_success_rate", 0) >= 90:
            performance_score += 25
            score_factors.append("Command execution: Good (25/30)")
        elif command_perf.get("overall_success_rate", 0) >= 80:
            performance_score += 20
            score_factors.append("Command execution: Fair (20/30)")
        else:
            performance_score += 10
            score_factors.append("Command execution: Poor (10/30)")

        # Resource utilization (25%)
        if resource_perf.get("memory_stats", {}).get("growth", 0) < 20 * 1024 * 1024:
            performance_score += 25
            score_factors.append("Resource utilization: Excellent (25/25)")
        elif resource_perf.get("memory_stats", {}).get("growth", 0) < 50 * 1024 * 1024:
            performance_score += 20
            score_factors.append("Resource utilization: Good (20/25)")
        else:
            performance_score += 15
            score_factors.append("Resource utilization: Fair (15/25)")

        # Scalability (20%)
        best_scalability = max(scalability_perf.values(), key=lambda x: x.get("success_rate", 0), default={})
        if best_scalability.get("success_rate", 0) >= 90:
            performance_score += 20
            score_factors.append("Scalability: Excellent (20/20)")
        elif best_scalability.get("success_rate", 0) >= 80:
            performance_score += 15
            score_factors.append("Scalability: Good (15/20)")
        else:
            performance_score += 10
            score_factors.append("Scalability: Fair (10/20)")

        # Memory management (15%)
        if not memory_perf.get("leak_detected", True):
            performance_score += 15
            score_factors.append("Memory management: Excellent (15/15)")
        elif memory_perf.get("memory_growth_mb", 0) < 20:
            performance_score += 10
            score_factors.append("Memory management: Good (10/15)")
        else:
            performance_score += 5
            score_factors.append("Memory management: Poor (5/15)")

        # Context management (10%)
        if context_perf.get("context_stability", 0) >= 90:
            performance_score += 10
            score_factors.append("Context management: Excellent (10/10)")
        elif context_perf.get("context_stability", 0) >= 80:
            performance_score += 8
            score_factors.append("Context management: Good (8/10)")
        else:
            performance_score += 5
            score_factors.append("Context management: Fair (5/10)")

        # Generate recommendations
        recommendations = []

        if command_perf.get("overall_success_rate", 0) < 90:
            recommendations.append("Investigate command failure causes and improve error handling")

        if resource_perf.get("memory_stats", {}).get("growth", 0) > 50 * 1024 * 1024:
            recommendations.append("Optimize memory usage in command execution")

        if memory_perf.get("leak_detected", False):
            recommendations.append("Address memory leaks in long-running operations")

        if context_perf.get("context_stability", 0) < 80:
            recommendations.append("Improve context cleanup between command executions")

        # Performance grade
        if performance_score >= 90:
            grade = "A+ (Excellent)"
        elif performance_score >= 85:
            grade = "A (Very Good)"
        elif performance_score >= 80:
            grade = "B+ (Good)"
        elif performance_score >= 75:
            grade = "B (Above Average)"
        elif performance_score >= 70:
            grade = "C+ (Average)"
        elif performance_score >= 65:
            grade = "C (Below Average)"
        else:
            grade = "D (Poor)"

        self.results["summary"] = {
            "overall_score": performance_score,
            "performance_grade": grade,
            "score_factors": score_factors,
            "recommendations": recommendations,
            "test_duration": time.time() - datetime.fromisoformat(self.results["test_session"]["start_time"]).timestamp(),
            "tests_completed": len([k for k, v in self.results.items() if k != "test_session" and v]),
        }

        return self.results

    def save_results(self) -> str:
        """Save performance test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.test_dir / f"performance_test_results_{timestamp}.json"

        # Update end time
        self.results["test_session"]["end_time"] = datetime.now().isoformat()

        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2, default=str)

        return str(results_file)

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all performance tests"""
        print("Starting comprehensive performance testing...")
        print(f"Platform: {sys.platform}")
        print(f"Python version: {sys.version.split()[0]}")
        print(f"Plugin version: {self._get_plugin_version()}")
        print("=" * 60)

        try:
            # Test 1: Command execution performance
            self.results["command_performance"] = self.test_command_performance()
            print()

            # Test 2: Resource utilization
            self.results["resource_utilization"] = self.test_resource_utilization()
            print()

            # Test 3: Context management
            self.results["context_management"] = self.test_context_management()
            print()

            # Test 4: Scalability
            self.results["scalability_tests"] = self.test_scalability()
            print()

            # Test 5: Memory leak detection
            self.results["memory_leak_tests"] = self.test_memory_leaks()
            print()

            # Generate comprehensive report
            self.generate_performance_report()

            # Save results
            results_file = self.save_results()

            print("=" * 60)
            print("Performance testing completed!")
            print(f"Results saved to: {results_file}")
            print(f"Overall performance score: {self.results['summary']['overall_score']:.1f}/100")
            print(f"Performance grade: {self.results['summary']['performance_grade']}")

            return self.results

        except Exception as e:
            print(f"Error during performance testing: {e}")
            traceback.print_exc()
            self.results["error"] = str(e)
            return self.results


def main():
    """Main execution function"""
    test_suite = PerformanceTestSuite()
    results = test_suite.run_all_tests()

    # Print summary
    if "summary" in results:
        summary = results["summary"]
        print("\n" + "=" * 60)
        print("PERFORMANCE TEST SUMMARY")
        print("=" * 60)
        print(f"Overall Score: {summary['overall_score']:.1f}/100")
        print(f"Performance Grade: {summary['performance_grade']}")
        print(f"Test Duration: {summary['test_duration']:.1f} seconds")

        print("\nScore Factors:")
        for factor in summary.get("score_factors", []):
            print(f"  • {factor}")

        if summary.get("recommendations"):
            print("\nRecommendations:")
            for rec in summary["recommendations"]:
                print(f"  • {rec}")

    return results


if __name__ == "__main__":
    main()
