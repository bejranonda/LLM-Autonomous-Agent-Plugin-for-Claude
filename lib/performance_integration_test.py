#!/usr/bin/env python3
#     Performance Integration Test
    """
Tests real-time monitoring capabilities during plugin operations
import time
import json
import threading
from datetime import datetime
from pathlib import Path
from performance_monitor import PerformanceMonitor


def test_monitoring_integration():
    """Test performance monitoring integration with plugin operations"""
    print("Performance Integration Test")
    print("=" * 50)

    # Initialize monitor
    data_dir = Path(".claude-patterns")
    monitor = PerformanceMonitor(str(data_dir))

    print("Starting performance monitoring...")
    monitor.start_monitoring(sample_interval=0.5)

    # Test various operations with monitoring
    operations = [("validate_plugin", 3), ("simple_test", 3), ("plugin_validator", 2), ("command_validator_help", 2)]

    print("\nExecuting monitored operations...")
    for op_name, iterations in operations:
        for i in range(iterations):
            start_time = time.time()

            try:
                if op_name == "validate_plugin":
                    result = __import__("validate_plugin").main()
                    success = True
                elif op_name == "simple_test":
                    result = __import__("simple_test_script").main()
                    success = True
                elif op_name == "plugin_validator":
                    result = __import__("plugin_validator").main()
                    success = True
                elif op_name == "command_validator_help":
                    result = __import__("command_validator").main()
                    success = True
                else:
                    success = False
                    result = None

                execution_time = time.time() - start_time
                monitor.record_command_execution(op_name, execution_time, success)
                print(f"  {op_name} #{i+1}: {execution_time:.3f}s - {'SUCCESS' if success else 'FAILED'}")

            except Exception as e:
                execution_time = time.time() - start_time
                monitor.record_command_execution(op_name, execution_time, False, str(e))
                print(f"  {op_name} #{i+1}: {execution_time:.3f}s - ERROR: {str(e)[:50]}")

            time.sleep(0.2)  # Small delay between operations

    # Let monitoring run a bit more to collect data
    print("\nCollecting monitoring data...")
    time.sleep(3)

    # Stop monitoring
    monitor.stop_monitoring()

    # Generate and display reports
    print("\nPerformance Analysis Results")
    print("=" * 30)

    # 5-minute summary (all data)
    summary = monitor.get_performance_summary(5)
    print(f"Monitoring Status: {summary.get('status', 'unknown')}")

    if summary.get("status") == "active":
        print(f"Sample Count: {summary.get('sample_count', 0)}")

        # Memory stats
        mem_stats = summary.get("memory_stats", {})
        print(f"Memory Usage:")
        print(f"  Current: {mem_stats.get('current_mb', 0):.1f} MB")
        print(f"  Average: {mem_stats.get('average_mb', 0):.1f} MB")
        print(f"  Peak: {mem_stats.get('peak_mb', 0):.1f} MB")
        print(f"  Growth: {mem_stats.get('growth_mb', 0):.1f} MB")

        # CPU stats
        cpu_stats = summary.get("cpu_stats", {})
        print(f"CPU Usage:")
        print(f"  Average: {cpu_stats.get('average_percent', 0):.1f}%")
        print(f"  Peak: {cpu_stats.get('peak_percent', 0):.1f}%")

        # Command stats
        cmd_stats = summary.get("command_stats", {})
        print(f"Commands:")
        print(f"  Total: {cmd_stats.get('total_commands', 0)}")
        print(f"  Successful: {cmd_stats.get('successful_commands', 0)}")
        print(f"  Success Rate: {cmd_stats.get('success_rate', 0):.1f}%")
        print(f"  Avg Execution Time: {cmd_stats.get('avg_execution_time', 0):.3f}s")

        # Health score
        print(f"System Health Score: {summary.get('health_score', 0)}/100 ({summary.get('health_grade', 'Unknown')})")

    # Save full report
    report = monitor.generate_performance_report()
    report_file = data_dir / f"performance_integration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(report_file, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\nDetailed report saved to: {report_file}")

    # Show metrics count
    print(f"Total metrics collected: {len(monitor.metrics_history)}")

    return report


def test_performance_alerts():
    """Test performance alert system"""
    print("\nPerformance Alert System Test")
    print("=" * 40)

    monitor = PerformanceMonitor(Path(".claude-patterns"))

    alert_count = 0

    def test_alert_callback(alert_type, alert_data):
        """Test Alert Callback."""
        nonlocal alert_count
        alert_count += 1
        print(f"ALERT #{alert_count}: {alert_type} - {alert_data['message']}")

    # Add alert callback
    monitor.add_alert_callback(test_alert_callback)

    # Temporarily lower thresholds to trigger alerts
    original_thresholds = monitor.thresholds.copy()
    monitor.thresholds["memory_usage_percent"] = 1  # Very low threshold
    monitor.thresholds["cpu_usage_percent"] = 1
    monitor.thresholds["execution_time_slow"] = 0.1  # Very low threshold

    # Start monitoring
    monitor.start_monitoring(sample_interval=0.5)

    # Simulate some operations that should trigger alerts
    monitor.record_command_execution("test_slow_command", 0.2, True)  # Should trigger slow command alert

    # Let monitoring run for a few seconds to collect system metrics
    time.sleep(3)

    # Stop monitoring
    monitor.stop_monitoring()

    # Restore original thresholds
    monitor.thresholds = original_thresholds

    print(f"Alert system test completed. {alert_count} alerts triggered.")
    return alert_count > 0


def main():
    """Main execution function"""
    try:
        # Test monitoring integration
        integration_results = test_monitoring_integration()

        # Test alert system
        alert_success = test_performance_alerts()

        # Final summary
        print("\n" + "=" * 60)
        print("PERFORMANCE INTEGRATION TEST SUMMARY")
        print("=" * 60)

        if integration_results:
            monitoring_status = integration_results.get("monitoring_status", "unknown")
            total_samples = integration_results.get("total_samples", 0)

            print(f" Performance Monitoring: {'Active' if monitoring_status == 'active' else 'Inactive'}")
            print(f" Data Collection: {total_samples} samples collected")
            print(f" Alert System: {'Working' if alert_success else 'Needs attention'}")

            if integration_results.get("summaries", {}).get("30_minutes", {}).get("status") == "active":
                summary = integration_results["summaries"]["30_minutes"]
                health_score = summary.get("health_score", 0)
                print(f" System Health: {health_score}/100 ({summary.get('health_grade', 'Unknown')})")

                if health_score >= 90:
                    print(" Overall Status: EXCELLENT")
                elif health_score >= 80:
                    print(" Overall Status: GOOD")
                elif health_score >= 70:
                    print("  Overall Status: ACCEPTABLE")
                else:
                    print(" Overall Status: NEEDS IMPROVEMENT")

        print("\nIntegration test completed successfully!")
        return True

    except Exception as e:
        print(f"Integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
