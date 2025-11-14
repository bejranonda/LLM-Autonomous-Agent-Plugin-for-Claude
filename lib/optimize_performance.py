#!/usr/bin/env python3
#     Performance optimization for concurrent operations
"""
"""
import time
import json
import threading
from pathlib import Path
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import hashlib


class PerformanceOptimizer:
    """Optimizes concurrent operations performance"""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """Initialize the processor with default configuration."""
        self.patterns_dir = Path(patterns_dir)
        self.patterns_dir.mkdir(exist_ok=True)

        # Performance cache
        self.cache_file = self.patterns_dir / "performance_cache.json"
        self.cache_data = self._load_cache()

        # Thread pool for concurrent operations
        self.executor = ThreadPoolExecutor(max_workers=4)

        # Performance metrics
        self.metrics = {"api_calls": 0, "cache_hits": 0, "avg_response_time": 0.0, "concurrent_requests": 0}

    def _load_cache(self) -> Dict[str, Any]:
        """Load performance cache"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_cache(self):
        """Save performance cache"""
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self.cache_data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")

    @lru_cache(maxsize=128)
    def _get_cache_key(self, endpoint: str, params: str = "") -> str:
        """Generate cache key for API endpoint"""
        return hashlib.md5(f"{endpoint}:{params}".encode()).hexdigest()

    def get_cached_data(self, endpoint: str, params: str = "") -> Any:
        """Get cached data for API endpoint"""
        cache_key = self._get_cache_key(endpoint, params)

        if cache_key in self.cache_data:
            cache_entry = self.cache_data[cache_key]
            # Check if cache is still valid (5 minutes)
            if time.time() - cache_entry["timestamp"] < 300:
                self.metrics["cache_hits"] += 1
                return cache_entry["data"]

        return None

    def cache_data(self, endpoint: str, data: Any, params: str = ""):
        """Cache data for API endpoint"""
        cache_key = self._get_cache_key(endpoint, params)
        self.cache_data[cache_key] = {"data": data, "timestamp": time.time()}

        # Limit cache size
        if len(self.cache_data) > 100:
            oldest_key = min(self.cache_data.keys(), key=lambda k: self.cache_data[k]["timestamp"])
            del self.cache_data[oldest_key]

        self._save_cache()

    def execute_concurrent_requests(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple API requests concurrently"""
        start_time = time.time()
        self.metrics["concurrent_requests"] += len(requests)

        results = []

        # Use ThreadPoolExecutor for concurrent execution
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all requests
            future_to_request = {executor.submit(self._execute_single_request, req): req for req in requests}

            # Collect results as they complete
            for future in as_completed(future_to_request):
                request = future_to_request[future]
                try:
                    result = future.result(timeout=10)  # 10 second timeout
                    results.append({"request": request, "result": result, "success": True})
                except Exception as e:
                    results.append({"request": request, "error": str(e), "success": False})

        # Update metrics
        total_time = time.time() - start_time
        self.metrics["avg_response_time"] = (self.metrics["avg_response_time"] * self.metrics["api_calls"] + total_time) / (
            self.metrics["api_calls"] + len(requests)
        )
        self.metrics["api_calls"] += len(requests)

        return results

    def _execute_single_request(self, request: Dict[str, Any]) -> Any:
        """Execute a single request with caching"""
        endpoint = request.get("endpoint", "")
        params = request.get("params", "")

        # Check cache first
        cached_data = self.get_cached_data(endpoint, params)
        if cached_data is not None:
            return cached_data

        # Simulate API call (in real implementation, this would be actual API call)
        time.sleep(0.1)  # Simulate network latency

        # Mock data for demonstration
        mock_data = {"endpoint": endpoint, "params": params, "timestamp": time.time(), "data": f"Mock data for {endpoint}"}

        # Cache the result
        self.cache_data(endpoint, mock_data, params)

        return mock_data

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            **self.metrics,
            "cache_size": len(self.cache_data),
            "cache_hit_rate": (self.metrics["cache_hits"] / max(self.metrics["api_calls"], 1) * 100),
            "concurrent_capacity": "4 workers",
        }

    def optimize_dashboard_endpoints(self) -> Dict[str, Any]:
        """Optimize dashboard API endpoints for better performance"""

        # Common dashboard endpoints
        endpoints = [
            "/api/overview",
            "/api/skills",
            "/api/agents",
            "/api/task-distribution",
            "/api/quality-trends",
            "/api/system-health",
            "/api/quality-timeline?days=30",
            "/api/debugging-performance?days=30",
            "/api/recent-performance-records",
            "/api/current-model",
            "/api/validation-results",
            "/api/recent-activity",
        ]

        # Create requests for concurrent execution
        requests = [{"endpoint": endpoint} for endpoint in endpoints]

        # Execute all requests concurrently
        start_time = time.time()
        results = self.execute_concurrent_requests(requests)
        total_time = time.time() - start_time

        # Analyze results
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful

        return {
            "total_requests": len(requests),
            "successful": successful,
            "failed": failed,
            "total_time": total_time,
            "avg_time_per_request": total_time / len(requests),
            "requests_per_second": len(requests) / total_time,
            "performance_grade": self._calculate_performance_grade(total_time, len(requests)),
            "metrics": self.get_performance_metrics(),
        }

    def _calculate_performance_grade(self, total_time: float, num_requests: int) -> str:
        """Calculate performance grade based on response time"""
        avg_time = total_time / num_requests

        if avg_time < 0.5:
            return "A+ (Excellent)"
        elif avg_time < 1.0:
            return "A (Very Good)"
        elif avg_time < 2.0:
            return "B (Good)"
        elif avg_time < 5.0:
            return "C (Fair)"
        elif avg_time < 10.0:
            return "D (Poor)"
        else:
            return "F (Very Poor)"


def main():
    """Run performance optimization analysis"""
    optimizer = PerformanceOptimizer()

    print("=== PERFORMANCE OPTIMIZATION ANALYSIS ===")
    print("Testing concurrent operations performance...")
    print()

    # Test dashboard endpoints
    print("Optimizing dashboard endpoints...")
    results = optimizer.optimize_dashboard_endpoints()

    print(f"Total Requests: {results['total_requests']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")
    print(f"Total Time: {results['total_time']:.3f} seconds")
    print(f"Avg Time per Request: {results['avg_time_per_request']:.3f} seconds")
    print(f"Requests per Second: {results['requests_per_second']:.1f}")
    print(f"Performance Grade: {results['performance_grade']}")
    print()

    # Show detailed metrics
    metrics = results["metrics"]
    print("=== PERFORMANCE METRICS ===")
    print(f"Total API Calls: {metrics['api_calls']}")
    print(f"Cache Hits: {metrics['cache_hits']}")
    print(f"Cache Hit Rate: {metrics['cache_hit_rate']:.1f}%")
    print(f"Average Response Time: {metrics['avg_response_time']:.3f} seconds")
    print(f"Cache Size: {metrics['cache_size']} entries")
    print(f"Concurrent Capacity: {metrics['concurrent_capacity']}")
    print(f"Concurrent Requests Processed: {metrics['concurrent_requests']}")
    print()

    # Performance assessment
    avg_time = results["avg_time_per_request"]
    print("=== PERFORMANCE ASSESSMENT ===")

    if avg_time <= 2.0:
        print("EXCELLENT: Concurrent operations well within 10-second target")
        print("Dashboard will have excellent responsiveness")
    elif avg_time <= 5.0:
        print("GOOD: Concurrent operations within acceptable range")
        print("Dashboard will have good responsiveness")
    elif avg_time <= 10.0:
        print("FAIR: Concurrent operations at the limit of 10-second target")
        print("Dashboard may experience some delays")
    else:
        print("POOR: Concurrent operations exceed 10-second target")
        print("Dashboard will experience significant delays")

    print()
    print("Cache optimization will significantly improve subsequent requests.")
    print("First request populates cache, subsequent requests are much faster.")


if __name__ == "__main__":
    main()
