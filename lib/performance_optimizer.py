#!/usr/bin/env python3
#     Performance optimizer for dashboard concurrent operations
import time
import json
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import hashlib


class PerformanceOptimizer:
    """Optimizes concurrent operations performance for dashboard"""

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
        self.metrics = {
            "api_calls": 0,
            "cache_hits": 0,
            "avg_response_time": 0.0,
            "concurrent_requests": 0,
            "last_optimization": time.time(),
        }

        # Lock for thread safety
        self.cache_lock = threading.Lock()

    def _load_cache(self) -> Dict[str, Any]:
        """Load performance cache with thread safety"""
        try:
            with self.cache_lock:
                if self.cache_file.exists():
                    with open(self.cache_file, "r") as f:
                        return json.load(f)
        except:
            pass
        return {}

    def _save_cache(self):
        """Save performance cache with thread safety"""
        try:
            with self.cache_lock:
                with open(self.cache_file, "w") as f:
                    json.dump(self.cache_data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def get_cache_key(self, endpoint: str, params: str = "") -> str:
        """Generate cache key for API endpoint"""
        content = f"{endpoint}:{params}"
        return hashlib.md5(content.encode()).hexdigest()

    def get_cached_data(self, endpoint: str, params: str = "") -> Optional[Any]:
        """Get cached data for API endpoint"""
        cache_key = self.get_cache_key(endpoint, params)

        with self.cache_lock:
            if cache_key in self.cache_data:
                cache_entry = self.cache_data[cache_key]
                # Check if cache is still valid (5 minutes for dynamic data, 30 minutes for static data)
                validity_period = 300 if "timeline" in endpoint or "recent" in endpoint else 1800
                if time.time() - cache_entry["timestamp"] < validity_period:
                    self.metrics["cache_hits"] += 1
                    return cache_entry["data"]

        return None

    def set_cached_data(self, endpoint: str, data: Any, params: str = ""):
        """Cache data for API endpoint"""
        cache_key = self.get_cache_key(endpoint, params)

        with self.cache_lock:
            self.cache_data[cache_key] = {"data": data, "timestamp": time.time()}

            # Limit cache size to prevent memory issues
            if len(self.cache_data) > 200:
                oldest_key = min(self.cache_data.keys(), key=lambda k: self.cache_data[k]["timestamp"])
                del self.cache_data[oldest_key]

        # Save cache asynchronously
        threading.Thread(target=self._save_cache, daemon=True).start()

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        with self.cache_lock:
            cache_hit_rate = self.metrics["cache_hits"] / max(self.metrics["api_calls"], 1) * 100

        return {
            **self.metrics,
            "cache_size": len(self.cache_data),
            "cache_hit_rate": round(cache_hit_rate, 1),
            "concurrent_capacity": "4 workers",
            "performance_grade": self._calculate_performance_grade(),
        }

    def _calculate_performance_grade(self) -> str:
        """Calculate current performance grade"""
        avg_time = self.metrics["avg_response_time"]

        if avg_time <= 0.1:
            return "A+ (Excellent)"
        elif avg_time <= 0.5:
            return "A (Very Good)"
        elif avg_time <= 1.0:
            return "B (Good)"
        elif avg_time <= 2.0:
            return "C (Fair)"
        elif avg_time <= 5.0:
            return "D (Poor)"
        else:
            return "F (Very Poor)"

    def clear_cache(self):
        """Clear performance cache"""
        with self.cache_lock:
            self.cache_data.clear()
            self._save_cache()


# Global performance optimizer instance
_performance_optimizer = None


def get_performance_optimizer(patterns_dir: str = ".claude-patterns") -> PerformanceOptimizer:
    """Get global performance optimizer instance"""
    global _performance_optimizer
    if _performance_optimizer is None:
        _performance_optimizer = PerformanceOptimizer(patterns_dir)
    return _performance_optimizer


def cache_api_response(endpoint: str, data: Any, params: str = ""):
    """Cache API response data"""
    optimizer = get_performance_optimizer()
    optimizer.set_cached_data(endpoint, data, params)


def get_cached_api_response(endpoint: str, params: str = "") -> Optional[Any]:
    """Get cached API response data"""
    optimizer = get_performance_optimizer()
    return optimizer.get_cached_data(endpoint, params)


def record_api_call(response_time: float):
    """Record API call for performance tracking"""
    optimizer = get_performance_optimizer()
    optimizer.metrics["api_calls"] += 1
    # Update rolling average
    total_calls = optimizer.metrics["api_calls"]
    current_avg = optimizer.metrics["avg_response_time"]
    optimizer.metrics["avg_response_time"] = (current_avg * (total_calls - 1) + response_time) / total_calls
