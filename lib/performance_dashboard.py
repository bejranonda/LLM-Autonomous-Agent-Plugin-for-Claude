#!/usr/bin/env python3
"""
Performance Dashboard for Autonomous Agent Plugin
Real-time performance monitoring and visualization
"""

import json
import time
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List
import statistics

class PerformanceDashboard:
    """Real-time performance dashboard"""

    def __init__(self, data_dir: str = ".claude-patterns"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Dashboard state
        self.refresh_interval = 5  # seconds
        self.max_display_lines = 40

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def create_progress_bar(self, value: float, max_value: float, width: int = 20) -> str:
        """Create ASCII progress bar"""
        if max_value <= 0:
            return "[" + "=" * width + "]"

        filled = int((value / max_value) * width)
        filled = max(0, min(width, filled))
        empty = width - filled

        return "[" + "=" * filled + " " * empty + "]"

    def format_bytes(self, bytes_value: int) -> str:
        """Format bytes in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024
        return f"{bytes_value:.1f} TB"

    def get_latest_data(self) -> Dict[str, Any]:
        """Get latest performance data"""
        data = {
            "test_results": None,
            "certification": None,
            "monitoring_active": False,
            "monitoring_data": None
        }

        # Load comprehensive test results
        test_files = list(self.data_dir.glob("performance_test_results_*.json"))
        if test_files:
            latest_file = max(test_files, key=lambda p: p.stat().st_mtime)
            try:
                with open(latest_file, 'r') as f:
                    data["test_results"] = json.load(f)
            except:
                pass

        # Load certification
        cert_file = self.data_dir / "performance_certification.json"
        if cert_file.exists():
            try:
                with open(cert_file, 'r') as f:
                    data["certification"] = json.load(f)
            except:
                pass

        # Load monitoring data
        monitor_file = self.data_dir / "performance_history.json"
        if monitor_file.exists():
            try:
                with open(monitor_file, 'r') as f:
                    monitor_data = json.load(f)
                    if monitor_data.get("metrics"):
                        data["monitoring_active"] = True
                        data["monitoring_data"] = monitor_data["metrics"][-1]  # Latest
            except:
                pass

        return data

    def display_header(self, data: Dict[str, Any]):
        """Display dashboard header"""
        print("=" * 80)
        print("AUTONOMOUS AGENT PLUGIN - PERFORMANCE DASHBOARD")
        print("=" * 80)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        plugin_version = data.get("certification", {}).get("plugin_version", "Unknown")

        print(f"Timestamp: {timestamp} | Plugin Version: {plugin_version}")
        print(f"Platform: {sys.platform} | Python: {sys.version.split()[0]}")
        print()

    def display_performance_summary(self, data: Dict[str, Any]):
        """Display performance summary section"""
        print("PERFORMANCE SUMMARY")
        print("-" * 30)

        cert = data.get("certification", {})
        if cert:
            score = cert.get("performance_score", 0)
            grade = cert.get("overall_grade", "Unknown")
            ready = cert.get("production_ready", False)

            print(f"Overall Score: {score}/100")
            print(f"Performance Grade: {grade}")
            print(f"Production Ready: {'YES' if ready else 'NO'}")
        else:
            print("No certification data available")

        print()

    def display_command_performance(self, data: Dict[str, Any]):
        """Display command performance section"""
        print("COMMAND EXECUTION PERFORMANCE")
        print("-" * 35)

        test_results = data.get("test_results")
        if not test_results:
            print("No test data available")
            print()
            return

        cmd_perf = test_results.get("command_performance", {})
        categories = cmd_perf.get("category_summaries", {})

        for category, stats in categories.items():
            if stats.get("total_runs", 0) > 0:
                avg_time = stats.get("avg_execution_time", 0)
                success_rate = stats.get("success_rate", 0)
                memory_delta = stats.get("avg_memory_delta", 0)

                print(f"{category.upper()} Commands:")
                print(f"  Avg Time: {avg_time:.3f}s")
                print(f"  Success Rate: {success_rate:.1f}%")
                print(f"  Memory Delta: {self.format_bytes(memory_delta)}")
                print(f"  Runs: {stats.get('total_runs', 0)}")
                print()

    def display_resource_utilization(self, data: Dict[str, Any]):
        """Display resource utilization section"""
        print("RESOURCE UTILIZATION")
        print("-" * 25)

        test_results = data.get("test_results")
        if not test_results:
            print("No resource data available")
            print()
            return

        resource_perf = test_results.get("resource_utilization", {})
        if not resource_perf:
            print("No resource data available")
            print()
            return

        # Memory stats
        memory_stats = resource_perf.get("memory_stats", {})
        if memory_stats:
            print("Memory Usage:")
            print(f"  Initial: {self.format_bytes(memory_stats.get('initial', 0))}")
            print(f"  Peak: {self.format_bytes(memory_stats.get('peak', 0))}")
            print(f"  Growth: {self.format_bytes(memory_stats.get('growth', 0))}")

            # Memory growth bar
            growth_mb = memory_stats.get('growth', 0) / 1024 / 1024
            growth_bar = self.create_progress_bar(min(growth_mb, 50), 50)
            print(f"  Growth: {growth_bar} {growth_mb:.1f}/50 MB")

        # CPU stats
        cpu_stats = resource_perf.get("cpu_stats", {})
        if cpu_stats:
            print("\nCPU Usage:")
            print(f"  Peak: {cpu_stats.get('peak', 0):.1f}%")
            print(f"  Average: {cpu_stats.get('avg', 0):.1f}%")

            # CPU usage bar
            avg_cpu = cpu_stats.get('avg', 0)
            cpu_bar = self.create_progress_bar(avg_cpu, 100)
            print(f"  Usage: {cpu_bar} {avg_cpu:.1f}%")

        print()

    def display_scalability_metrics(self, data: Dict[str, Any]):
        """Display scalability metrics section"""
        print("SCALABILITY METRICS")
        print("-" * 22)

        test_results = data.get("test_results")
        if not test_results:
            print("No scalability data available")
            print()
            return

        scalability = test_results.get("scalability_tests", {})
        if not scalability:
            print("No scalability data available")
            print()
            return

        print("Concurrent Execution Performance:")
        for worker_config, perf in scalability.items():
            workers = perf.get("workers", 0)
            throughput = perf.get("commands_per_second", 0)
            success_rate = perf.get("success_rate", 0)
            memory_growth = perf.get("memory_growth", 0)

            print(f"  {workers} Workers:")
            print(f"    Throughput: {throughput:.2f} cmd/sec")
            print(f"    Success Rate: {success_rate:.1f}%")
            print(f"    Memory Growth: {self.format_bytes(memory_growth)}")

            # Throughput bar
            throughput_bar = self.create_progress_bar(throughput, 10)
            print(f"    Throughput: {throughput_bar} {throughput:.1f}/10 cmd/sec")

        print()

    def display_memory_analysis(self, data: Dict[str, Any]):
        """Display memory analysis section"""
        print("MEMORY ANALYSIS")
        print("-" * 18)

        test_results = data.get("test_results")
        if not test_results:
            print("No memory analysis data available")
            print()
            return

        memory_tests = test_results.get("memory_leak_tests", {})
        if not memory_tests:
            print("No memory analysis data available")
            print()
            return

        print("Extended Execution Test:")
        print(f"  Iterations: {memory_tests.get('iterations', 0)}")
        print(f"  Initial Memory: {memory_tests.get('initial_memory_mb', 0):.1f} MB")
        print(f"  Final Memory: {memory_tests.get('final_memory_mb', 0):.1f} MB")
        print(f"  Memory Growth: {memory_tests.get('memory_growth_mb', 0):.3f} MB")
        print(f"  Memory Trend: {memory_tests.get('memory_trend', 'unknown').upper()}")
        print(f"  Leak Detected: {'YES' if memory_tests.get('leak_detected', False) else 'NO'}")

        # Memory stability bar
        growth = memory_tests.get('memory_growth_mb', 0)
        stability_bar = self.create_progress_bar(max(0, 50 - growth), 50)
        print(f"  Stability: {stability_bar} {max(0, 50 - growth):.1f}/50 MB stable")

        print()

    def display_real_time_monitoring(self, data: Dict[str, Any]):
        """Display real-time monitoring section"""
        print("REAL-TIME MONITORING")
        print("-" * 24)

        if not data.get("monitoring_active"):
            print("Status: INACTIVE")
            print("Start monitoring with: python lib/performance_monitor.py --monitor")
            print()
            return

        monitoring_data = data.get("monitoring_data")
        if not monitoring_data:
            print("No monitoring data available")
            print()
            return

        print("Status: ACTIVE")
        print(f"Last Update: {datetime.fromtimestamp(monitoring_data.get('timestamp', 0)).strftime('%H:%M:%S')}")
        print(f"Memory Usage: {self.format_bytes(monitoring_data.get('memory_rss', 0))}")
        print(f"CPU Usage: {monitoring_data.get('cpu_percent', 0):.1f}%")
        print(f"Threads: {monitoring_data.get('num_threads', 0)}")
        print(f"Open Files: {monitoring_data.get('open_files', 0)}")

        print()

    def display_recommendations(self, data: Dict[str, Any]):
        """Display recommendations section"""
        print("PERFORMANCE RECOMMENDATIONS")
        print("-" * 32)

        cert = data.get("certification", {})
        recommendations = cert.get("recommendations", [])

        if not recommendations:
            print("No specific recommendations - performance is optimal")
        else:
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")

        print()

    def display_footer(self):
        """Display dashboard footer"""
        print("=" * 80)
        print("Controls: [R]efresh | [Q]uit")
        print("Monitoring: python lib/performance_monitor.py --monitor")
        print("Reports: python lib/performance_final_validation.py")
        print("=" * 80)

    def refresh_dashboard(self):
        """Refresh the dashboard display"""
        self.clear_screen()

        # Get latest data
        data = self.get_latest_data()

        # Display all sections
        self.display_header(data)
        self.display_performance_summary(data)
        self.display_command_performance(data)
        self.display_resource_utilization(data)
        self.display_scalability_metrics(data)
        self.display_memory_analysis(data)
        self.display_real_time_monitoring(data)
        self.display_recommendations(data)
        self.display_footer()

    def run_interactive_dashboard(self):
        """Run interactive dashboard"""
        print("Starting Performance Dashboard...")
        print("Press 'Q' to quit, 'R' to refresh")
        print()

        try:
            while True:
                self.refresh_dashboard()

                # Wait for user input or auto-refresh
                print(f"\nAuto-refresh in {self.refresh_interval} seconds... (Press R to refresh now, Q to quit)")

                # Simple input handling with timeout
                start_time = time.time()
                user_input = ""

                while time.time() - start_time < self.refresh_interval:
                    try:
                        # Non-blocking check for input (simplified)
                        import msvcrt
                        if msvcrt.kbhit():
                            char = msvcrt.getch().decode('utf-8').upper()
                            if char == 'Q':
                                print("\nExiting dashboard...")
                                return
                            elif char == 'R':
                                user_input = 'R'
                                break
                    except:
                        pass

                    time.sleep(0.1)

                if user_input == 'R':
                    continue
                else:
                    # Auto-refresh
                    continue

        except KeyboardInterrupt:
            print("\nDashboard stopped by user")

    def generate_report(self) -> str:
        """Generate text-based performance report"""
        data = self.get_latest_data()

        report_lines = []
        report_lines.append("AUTONOMOUS AGENT PLUGIN PERFORMANCE REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated: {datetime.now().isoformat()}")
        report_lines.append()

        # Performance Summary
        cert = data.get("certification", {})
        if cert:
            report_lines.append("PERFORMANCE SUMMARY")
            report_lines.append("-" * 20)
            report_lines.append(f"Overall Score: {cert.get('performance_score', 0)}/100")
            report_lines.append(f"Performance Grade: {cert.get('overall_grade', 'Unknown')}")
            report_lines.append(f"Production Ready: {'YES' if cert.get('production_ready', False) else 'NO'}")
            report_lines.append()

        # Detailed metrics from test results
        test_results = data.get("test_results")
        if test_results:
            report_lines.append("DETAILED PERFORMANCE METRICS")
            report_lines.append("-" * 30)

            # Command performance
            cmd_perf = test_results.get("command_performance", {})
            if cmd_perf.get("category_summaries"):
                report_lines.append("Command Execution:")
                for category, stats in cmd_perf["category_summaries"].items():
                    if stats.get("total_runs", 0) > 0:
                        report_lines.append(f"  {category}: {stats.get('avg_execution_time', 0):.3f}s avg, {stats.get('success_rate', 0):.1f}% success")

            # Resource utilization
            resource_perf = test_results.get("resource_utilization", {})
            if resource_perf.get("memory_stats"):
                memory_stats = resource_perf["memory_stats"]
                growth_mb = memory_stats.get("growth", 0) / 1024 / 1024
                report_lines.append(f"\nResource Utilization:")
                report_lines.append(f"  Memory Growth: {growth_mb:.2f} MB")
                report_lines.append(f"  Peak CPU: {resource_perf.get('cpu_stats', {}).get('peak', 0):.1f}%")

            # Scalability
            scalability = test_results.get("scalability_tests", {})
            if scalability:
                report_lines.append(f"\nScalability:")
                for config, perf in scalability.items():
                    report_lines.append(f"  {config}: {perf.get('commands_per_second', 0):.2f} cmd/sec")

            # Memory analysis
            memory_tests = test_results.get("memory_leak_tests", {})
            if memory_tests:
                leak_status = "DETECTED" if memory_tests.get("leak_detected", False) else "CLEAN"
                report_lines.append(f"\nMemory Analysis:")
                report_lines.append(f"  Memory Leaks: {leak_status}")
                report_lines.append(f"  Memory Growth: {memory_tests.get('memory_growth_mb', 0):.3f} MB")
                report_lines.append(f"  Memory Trend: {memory_tests.get('memory_trend', 'unknown').upper()}")

        # Recommendations
        if cert and cert.get("recommendations"):
            report_lines.append(f"\nRecommendations:")
            for i, rec in enumerate(cert["recommendations"], 1):
                report_lines.append(f"  {i}. {rec}")

        report_lines.append("\n" + "=" * 60)

        return "\n".join(report_lines)

def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description="Performance Dashboard")
    parser.add_argument("--data-dir", default=".claude-patterns", help="Data directory")
    parser.add_argument("--report", action="store_true", help="Generate text report and exit")
    parser.add_argument("--interactive", action="store_true", help="Run interactive dashboard")

    args = parser.parse_args()

    dashboard = PerformanceDashboard(args.data_dir)

    if args.report:
        # Generate and save report
        report = dashboard.generate_report()

        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = Path(args.data_dir) / f"performance_report_{timestamp}.txt"

        with open(report_file, 'w') as f:
            f.write(report)

        print("PERFORMANCE REPORT GENERATED")
        print("=" * 30)
        print(report)
        print(f"\nReport saved to: {report_file}")

    elif args.interactive:
        # Run interactive dashboard
        dashboard.run_interactive_dashboard()

    else:
        # Single refresh and exit
        dashboard.refresh_dashboard()

if __name__ == "__main__":
    main()