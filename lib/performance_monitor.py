#!/usr/bin/env python3
"""
Performance Monitoring Utility for Autonomous Agent Plugin
Provides real-time monitoring, alerting, and analysis of plugin performance
"""

import time
import json
import psutil
import threading
import statistics
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from collections import deque
import logging

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: float
    memory_rss: int
    memory_vms: int
    memory_percent: float
    cpu_percent: float
    num_threads: int
    open_files: int
    command_name: str = "idle"
    execution_time: float = 0.0
    success: bool = True
    error_type: str = ""

class PerformanceMonitor:
    """Real-time performance monitoring system"""

    def __init__(self, data_dir: str = ".claude-patterns", max_history: int = 1000):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Monitoring state
        self.monitoring_active = False
        self.monitor_thread = None
        self.sample_interval = 1.0  # seconds

        # Performance history
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)

        # Alert thresholds
        self.thresholds = {
            "memory_growth_rate": 5 * 1024 * 1024,  # 5MB/min
            "memory_usage_percent": 80,
            "cpu_usage_percent": 80,
            "execution_time_slow": 5.0,  # seconds
            "error_rate_percent": 10,  # per minute
            "thread_count_high": 50,
            "file_handle_count": 1000
        }

        # Alert callbacks
        self.alert_callbacks = []

        # Logging
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Setup performance monitoring logging"""
        logger = logging.getLogger("performance_monitor")
        logger.setLevel(logging.INFO)

        # Create file handler
        log_file = self.data_dir / "performance_monitor.log"
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def add_alert_callback(self, callback: Callable[[str, Dict[str, Any]], None]):
        """Add custom alert callback function"""
        self.alert_callbacks.append(callback)

    def start_monitoring(self, sample_interval: float = 1.0):
        """Start performance monitoring"""
        if self.monitoring_active:
            self.logger.warning("Monitoring already active")
            return

        self.sample_interval = sample_interval
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

        self.logger.info(f"Performance monitoring started with {sample_interval}s interval")

    def stop_monitoring(self):
        """Stop performance monitoring"""
        if not self.monitoring_active:
            return

        self.monitoring_active = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2.0)

        self.logger.info("Performance monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        last_minute_errors = 0
        last_minute_commands = 0
        last_minute_time = time.time()
        last_memory = 0

        while self.monitoring_active:
            try:
                # Get current metrics
                current_time = time.time()
                process = psutil.Process()

                # Sample system metrics
                metrics = PerformanceMetrics(
                    timestamp=current_time,
                    memory_rss=process.memory_info().rss,
                    memory_vms=process.memory_info().vms,
                    memory_percent=process.memory_percent(),
                    cpu_percent=process.cpu_percent(),
                    num_threads=process.num_threads(),
                    open_files=len(process.open_files()),
                    command_name="system_monitor"
                )

                # Add to history
                self.metrics_history.append(metrics)

                # Check for alerts every minute
                if current_time - last_minute_time >= 60:
                    self._check_alerts(metrics, last_memory, last_minute_errors, last_minute_commands)
                    last_minute_time = current_time
                    last_memory = metrics.memory_rss
                    last_minute_errors = 0
                    last_minute_commands = 0

                # Save history periodically
                if len(self.metrics_history) % 100 == 0:
                    self._save_history()

                time.sleep(self.sample_interval)

            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.sample_interval)

    def _check_alerts(self, current_metrics: PerformanceMetrics,
                     last_memory: int, error_count: int, command_count: int):
        """Check for performance alerts"""
        alerts = []

        # Memory usage alert
        if current_metrics.memory_percent > self.thresholds["memory_usage_percent"]:
            alerts.append({
                "type": "high_memory_usage",
                "severity": "warning",
                "message": f"High memory usage: {current_metrics.memory_percent:.1f}%",
                "value": current_metrics.memory_percent,
                "threshold": self.thresholds["memory_usage_percent"]
            })

        # CPU usage alert
        if current_metrics.cpu_percent > self.thresholds["cpu_usage_percent"]:
            alerts.append({
                "type": "high_cpu_usage",
                "severity": "warning",
                "message": f"High CPU usage: {current_metrics.cpu_percent:.1f}%",
                "value": current_metrics.cpu_percent,
                "threshold": self.thresholds["cpu_usage_percent"]
            })

        # Thread count alert
        if current_metrics.num_threads > self.thresholds["thread_count_high"]:
            alerts.append({
                "type": "high_thread_count",
                "severity": "warning",
                "message": f"High thread count: {current_metrics.num_threads}",
                "value": current_metrics.num_threads,
                "threshold": self.thresholds["thread_count_high"]
            })

        # File handle alert
        if current_metrics.open_files > self.thresholds["file_handle_count"]:
            alerts.append({
                "type": "high_file_handle_count",
                "severity": "warning",
                "message": f"High file handle count: {current_metrics.open_files}",
                "value": current_metrics.open_files,
                "threshold": self.thresholds["file_handle_count"]
            })

        # Error rate alert
        if command_count > 0:
            error_rate = (error_count / command_count) * 100
            if error_rate > self.thresholds["error_rate_percent"]:
                alerts.append({
                    "type": "high_error_rate",
                    "severity": "critical",
                    "message": f"High error rate: {error_rate:.1f}%",
                    "value": error_rate,
                    "threshold": self.thresholds["error_rate_percent"]
                })

        # Trigger alert callbacks
        for alert in alerts:
            self._trigger_alert(alert["type"], alert)

    def _trigger_alert(self, alert_type: str, alert_data: Dict[str, Any]):
        """Trigger performance alert"""
        self.logger.warning(f"ALERT: {alert_data['message']}")

        # Call custom alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert_type, alert_data)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")

    def record_command_execution(self, command_name: str, execution_time: float,
                                success: bool = True, error_type: str = ""):
        """Record command execution metrics"""
        try:
            process = psutil.Process()

            metrics = PerformanceMetrics(
                timestamp=time.time(),
                memory_rss=process.memory_info().rss,
                memory_vms=process.memory_info().vms,
                memory_percent=process.memory_percent(),
                cpu_percent=process.cpu_percent(),
                num_threads=process.num_threads(),
                open_files=len(process.open_files()),
                command_name=command_name,
                execution_time=execution_time,
                success=success,
                error_type=error_type
            )

            self.metrics_history.append(metrics)

            # Immediate alerts for slow commands
            if not success:
                self.logger.error(f"Command failed: {command_name} ({error_type})")
            elif execution_time > self.thresholds["execution_time_slow"]:
                self.logger.warning(f"Slow command: {command_name} took {execution_time:.2f}s")

        except Exception as e:
            self.logger.error(f"Error recording command execution: {e}")

    def get_performance_summary(self, minutes: int = 10) -> Dict[str, Any]:
        """Get performance summary for recent time period"""
        if not self.metrics_history:
            return {"status": "no_data"}

        # Filter recent metrics
        cutoff_time = time.time() - (minutes * 60)
        recent_metrics = [m for m in self.metrics_history if m.timestamp > cutoff_time]

        if not recent_metrics:
            return {"status": "no_recent_data"}

        # Calculate statistics
        memory_values = [m.memory_rss for m in recent_metrics]
        cpu_values = [m.cpu_percent for m in recent_metrics]
        command_metrics = [m for m in recent_metrics if m.command_name != "system_monitor"]

        # Memory analysis
        memory_stats = {
            "current_mb": memory_values[-1] / 1024 / 1024 if memory_values else 0,
            "average_mb": statistics.mean(memory_values) / 1024 / 1024 if memory_values else 0,
            "peak_mb": max(memory_values) / 1024 / 1024 if memory_values else 0,
            "min_mb": min(memory_values) / 1024 / 1024 if memory_values else 0,
            "growth_mb": (memory_values[-1] - memory_values[0]) / 1024 / 1024 if len(memory_values) > 1 else 0
        }

        # CPU analysis
        cpu_stats = {
            "average_percent": statistics.mean(cpu_values) if cpu_values else 0,
            "peak_percent": max(cpu_values) if cpu_values else 0,
            "current_percent": cpu_values[-1] if cpu_values else 0
        }

        # Command analysis
        if command_metrics:
            execution_times = [m.execution_time for m in command_metrics]
            successful_commands = [m for m in command_metrics if m.success]

            command_stats = {
                "total_commands": len(command_metrics),
                "successful_commands": len(successful_commands),
                "success_rate": (len(successful_commands) / len(command_metrics)) * 100,
                "avg_execution_time": statistics.mean(execution_times) if execution_times else 0,
                "slow_commands": len([t for t in execution_times if t > self.thresholds["execution_time_slow"]])
            }
        else:
            command_stats = {
                "total_commands": 0,
                "successful_commands": 0,
                "success_rate": 0,
                "avg_execution_time": 0,
                "slow_commands": 0
            }

        # System health score (0-100)
        health_score = 100
        if memory_stats["growth_mb"] > 50:
            health_score -= 20
        if cpu_stats["average_percent"] > 50:
            health_score -= 15
        if command_stats["success_rate"] < 95:
            health_score -= 25
        if command_stats["slow_commands"] > command_stats["total_commands"] * 0.1:
            health_score -= 10

        health_score = max(0, health_score)

        return {
            "status": "active",
            "time_period_minutes": minutes,
            "sample_count": len(recent_metrics),
            "memory_stats": memory_stats,
            "cpu_stats": cpu_stats,
            "command_stats": command_stats,
            "health_score": health_score,
            "health_grade": self._get_health_grade(health_score)
        }

    def _get_health_grade(self, score: float) -> str:
        """Get health grade from score"""
        if score >= 95:
            return "A+ (Excellent)"
        elif score >= 90:
            return "A (Very Good)"
        elif score >= 85:
            return "B+ (Good)"
        elif score >= 80:
            return "B (Above Average)"
        elif score >= 70:
            return "C+ (Average)"
        elif score >= 60:
            return "C (Below Average)"
        else:
            return "D (Poor)"

    def _save_history(self):
        """Save metrics history to file"""
        try:
            history_file = self.data_dir / "performance_history.json"

            # Convert deque to list for JSON serialization
            history_data = [asdict(m) for m in self.metrics_history]

            with open(history_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "total_samples": len(history_data),
                    "metrics": history_data
                }, f, indent=2)

        except Exception as e:
            self.logger.error(f"Error saving history: {e}")

    def load_history(self) -> bool:
        """Load metrics history from file"""
        try:
            history_file = self.data_dir / "performance_history.json"
            if not history_file.exists():
                return False

            with open(history_file, 'r') as f:
                data = json.load(f)

            # Convert back to PerformanceMetrics objects
            self.metrics_history.clear()
            for item in data.get("metrics", []):
                metrics = PerformanceMetrics(**item)
                self.metrics_history.append(metrics)

            self.logger.info(f"Loaded {len(self.metrics_history)} historical metrics")
            return True

        except Exception as e:
            self.logger.error(f"Error loading history: {e}")
            return False

    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        # Get summaries for different time periods
        summary_5min = self.get_performance_summary(5)
        summary_30min = self.get_performance_summary(30)
        summary_1hr = self.get_performance_summary(60)

        # Identify performance trends
        trends = self._analyze_trends()

        # Generate recommendations
        recommendations = self._generate_recommendations(summary_30min)

        return {
            "timestamp": datetime.now().isoformat(),
            "monitoring_status": "active" if self.monitoring_active else "inactive",
            "total_samples": len(self.metrics_history),
            "summaries": {
                "5_minutes": summary_5min,
                "30_minutes": summary_30min,
                "1_hour": summary_1hr
            },
            "trends": trends,
            "recommendations": recommendations,
            "thresholds": self.thresholds
        }

    def _analyze_trends(self) -> Dict[str, str]:
        """Analyze performance trends"""
        if len(self.metrics_history) < 60:  # Need at least 1 minute of data
            return {"status": "insufficient_data"}

        recent_memory = [m.memory_rss for m in list(self.metrics_history)[-60:]]
        older_memory = [m.memory_rss for m in list(self.metrics_history)[-300:-60]] if len(self.metrics_history) > 300 else []

        trends = {}

        # Memory trend
        if older_memory and recent_memory:
            recent_avg = statistics.mean(recent_memory)
            older_avg = statistics.mean(older_memory)
            change_percent = ((recent_avg - older_avg) / older_avg) * 100

            if change_percent > 10:
                trends["memory"] = "increasing_rapidly"
            elif change_percent > 5:
                trends["memory"] = "increasing"
            elif change_percent < -5:
                trends["memory"] = "decreasing"
            else:
                trends["memory"] = "stable"
        else:
            trends["memory"] = "insufficient_data"

        return trends

    def _generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []

        if summary.get("status") != "active":
            return recommendations

        memory_stats = summary.get("memory_stats", {})
        cpu_stats = summary.get("cpu_stats", {})
        command_stats = summary.get("command_stats", {})

        # Memory recommendations
        if memory_stats.get("growth_mb", 0) > 50:
            recommendations.append("Memory usage is growing rapidly - investigate potential memory leaks")

        if memory_stats.get("peak_mb", 0) > 500:
            recommendations.append("Peak memory usage is high - consider optimizing memory-intensive operations")

        # CPU recommendations
        if cpu_stats.get("average_percent", 0) > 50:
            recommendations.append("High average CPU usage - consider optimizing computationally intensive tasks")

        # Command recommendations
        if command_stats.get("success_rate", 100) < 95:
            recommendations.append("Command success rate is below 95% - investigate failure causes")

        if command_stats.get("slow_commands", 0) > 0:
            recommendations.append(f"{command_stats['slow_commands']} slow commands detected - optimize performance bottlenecks")

        return recommendations

# Global monitor instance
_monitor_instance = None

def get_performance_monitor(data_dir: str = ".claude-patterns") -> PerformanceMonitor:
    """Get global performance monitor instance"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = PerformanceMonitor(data_dir)
    return _monitor_instance

def start_monitoring(data_dir: str = ".claude-patterns", sample_interval: float = 1.0):
    """Start global performance monitoring"""
    monitor = get_performance_monitor(data_dir)
    monitor.start_monitoring(sample_interval)

def stop_monitoring():
    """Stop global performance monitoring"""
    monitor = get_performance_monitor()
    monitor.stop_monitoring()

def record_command(command_name: str, execution_time: float, success: bool = True, error_type: str = ""):
    """Record command execution in global monitor"""
    monitor = get_performance_monitor()
    monitor.record_command_execution(command_name, execution_time, success, error_type)

def get_summary(minutes: int = 10) -> Dict[str, Any]:
    """Get performance summary from global monitor"""
    monitor = get_performance_monitor()
    return monitor.get_performance_summary(minutes)

def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description="Performance Monitor for Autonomous Agent")
    parser.add_argument("--data-dir", default=".claude-patterns", help="Data directory")
    parser.add_argument("--interval", type=float, default=1.0, help="Sample interval in seconds")
    parser.add_argument("--summary", type=int, help="Show N-minute summary and exit")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive report")
    parser.add_argument("--monitor", action="store_true", help="Start monitoring")
    parser.add_argument("--duration", type=int, default=60, help="Monitoring duration in seconds")

    args = parser.parse_args()

    monitor = PerformanceMonitor(args.data_dir)

    if args.summary:
        # Load history and show summary
        monitor.load_history()
        summary = monitor.get_performance_summary(args.summary)
        print(json.dumps(summary, indent=2, default=str))
        return

    if args.report:
        # Generate comprehensive report
        monitor.load_history()
        report = monitor.generate_performance_report()
        print(json.dumps(report, indent=2, default=str))
        return

    if args.monitor:
        print(f"Starting performance monitoring for {args.duration} seconds...")
        monitor.start_monitoring(args.interval)

        try:
            time.sleep(args.duration)
        except KeyboardInterrupt:
            print("\nMonitoring interrupted by user")

        monitor.stop_monitoring()
        print("Monitoring stopped")

        # Show final summary
        summary = monitor.get_performance_summary(args.duration // 60)
        print("\nPerformance Summary:")
        print(json.dumps(summary, indent=2, default=str))
    else:
        print("Use --monitor to start monitoring, --summary for quick stats, or --report for detailed analysis")

if __name__ == "__main__":
    main()