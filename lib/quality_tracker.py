#!/usr/bin/env python3
"""
Quality Tracker System for Autonomous Claude Agent Plugin

Tracks quality metrics over time using JSON files. Records quality assessments,
analyzes trends, and provides insights into performance improvements.
"""

import json
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import platform
from collections import defaultdict

# Handle Windows compatibility for file locking
if platform.system() == 'Windows':
    import msvcrt
    def lock_file(f, exclusive=False):
        """Windows file locking using msvcrt."""
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        """Windows file unlocking."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl
    def lock_file(f, exclusive=False):
        """Unix file locking using fcntl."""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)

    def unlock_file(f):
        """Unix file unlocking."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class QualityTracker:
    """Manages quality tracking and trend analysis."""

    def __init__(self, tracker_dir: str = ".claude-patterns"):
        """
        Initialize quality tracker.

        Args:
            tracker_dir: Directory path for storing quality data (
    default: .claude-patterns,
)
        """
        self.tracker_dir = Path(tracker_dir)
        self.quality_file = self.tracker_dir / "quality_history.json"
        self._ensure_directory()

    def _ensure_directory(self):
        """Create tracker directory if it doesn't exist."""
        self.tracker_dir.mkdir(parents=True, exist_ok=True)
        if not self.quality_file.exists():
            self._write_quality_records([])

    def _read_quality_records(self) -> List[Dict[str, Any]]:
        """
        Read quality records from JSON file with file locking.

        Returns:
            List of quality record dictionaries
        """
        try:
            with open(self.quality_file, 'r', encoding='utf-8') as f:
                # Acquire shared lock for reading
                lock_file(f, exclusive=False)
                try:
                    content = f.read()
                    if not content.strip():
                        return []
                    return json.loads(content)
                finally:
                    unlock_file(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Error: Malformed JSON in {self.quality_file}: {e}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"Error reading quality records: {e}", file=sys.stderr)
            return []

    def _write_quality_records(self, records: List[Dict[str, Any]]):
        """
        Write quality records to JSON file with file locking.

        Args:
            records: List of quality record dictionaries to write
        """
        try:
            with open(self.quality_file, 'w', encoding='utf-8') as f:
                # Acquire exclusive lock for writing
                lock_file(f, exclusive=True)
                try:
                    json.dump(records, f, indent=2, ensure_ascii=False)
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error writing quality records: {e}", file=sys.stderr)
            raise

    def record_quality(
        self,
        task_id: str,
        quality_score: float,
        metrics: Dict[str, float]
    ) -> bool:
        """
        Record quality assessment for a task.

        Args:
            task_id: ID of the task assessed
            quality_score: Overall quality score (0.0 to 1.0)
            metrics: Dictionary of metric scores (
    e.g.,
    code_quality,
    test_quality,
    etc.,
)

        Returns:
            True on success
        """
        # Validate quality score
        if not isinstance(quality_score, (int, float)) or not (0 <= quality_score <= 1):
            raise ValueError("quality_score must be a number between 0 and 1")

        # Validate metrics
        for metric_name, metric_value in metrics.items():
            if not isinstance(
    metric_value,
    (int, float)) or not (0 <= metric_value <= 1):,
)
                raise ValueError(
    f"Metric '{metric_name}' must be a number between 0 and 1",
)

        # Create quality record
        record = {
            'task_id': task_id,
            'quality_score': quality_score,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics
        }

        # Add to records
        records = self._read_quality_records()
        records.append(record)

        # Sort by timestamp
        records.sort(key=lambda x: x['timestamp'])

        self._write_quality_records(records)
        return True

    def get_quality_trends(
        self,
        days: int = 30,
        metric: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get quality trends over time.

        Args:
            days: Number of days to analyze (default: 30)
            metric: Specific metric to analyze (
    optional,
    analyzes overall quality if not specified,
)

        Returns:
            Dictionary with trend analysis
        """
        records = self._read_quality_records()

        if not records:
            return {
                'period_days': days,
                'metric': metric or 'quality_score',
                'data_points': 0,
                'trend': 'no_data',
                'current_average': 0.0,
                'previous_average': 0.0,
                'change_percentage': 0.0,
                'timeline': []
            }

        # Filter records within time period
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_records = [
            r for r in records
            if datetime.fromisoformat(r['timestamp']) >= cutoff_date
        ]

        if not recent_records:
            return {
                'period_days': days,
                'metric': metric or 'quality_score',
                'data_points': 0,
                'trend': 'no_data',
                'current_average': 0.0,
                'previous_average': 0.0,
                'change_percentage': 0.0,
                'timeline': []
            }

        # Extract values
        if metric:
            values = [r['metrics'].get(metric, 0) for r in recent_records]
        else:
            values = [r['quality_score'] for r in recent_records]

        # Calculate trend (compare first half vs second half)
        mid_point = len(values) // 2
        if mid_point == 0:
            mid_point = 1

        first_half = values[:mid_point]
        second_half = values[mid_point:]

        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)

        # Calculate change percentage
        if first_avg > 0:
            change_pct = ((second_avg - first_avg) / first_avg) * 100
        else:
            change_pct = 0.0

        # Determine trend direction
        if change_pct > 5:
            trend = 'improving'
        elif change_pct < -5:
            trend = 'declining'
        else:
            trend = 'stable'

        # Create timeline data
        timeline = []
        for record in recent_records:
            value = record['metrics'].get(metric, 0) if 
                metric else record['quality_score']
            timeline.append({
                'timestamp': record['timestamp'],
                'task_id': record['task_id'],
                'value': value
            })

        return {
            'period_days': days,
            'metric': metric or 'quality_score',
            'data_points': len(values),
            'trend': trend,
            'current_average': second_avg,
            'previous_average': first_avg,
            'change_percentage': change_pct,
            'timeline': timeline
        }

    def get_average_quality(self, days: Optional[int] = None) -> float:
        """
        Get average quality score.

        Args:
            days: Number of days to analyze (optional, all-time if not specified)

        Returns:
            Average quality score
        """
        records = self._read_quality_records()

        if not records:
            return 0.0

        # Filter by days if specified
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            records = [
                r for r in records
                if datetime.fromisoformat(r['timestamp']) >= cutoff_date
            ]

        if not records:
            return 0.0

        total = sum(r['quality_score'] for r in records)
        return total / len(records)

    def get_metric_statistics(
    self,
    days: Optional[int] = None) -> Dict[str, Dict[str, float]]:,
)
        """
        Get statistics for all metrics.

        Args:
            days: Number of days to analyze (optional, all-time if not specified)

        Returns:
            Dictionary with statistics for each metric
        """
        records = self._read_quality_records()

        if not records:
            return {}

        # Filter by days if specified
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            records = [
                r for r in records
                if datetime.fromisoformat(r['timestamp']) >= cutoff_date
            ]

        if not records:
            return {}

        # Collect values for each metric
        metric_values = defaultdict(list)

        for record in records:
            for metric_name, metric_value in record.get('metrics', {}).items():
                metric_values[metric_name].append(metric_value)

        # Calculate statistics
        statistics = {}
        for metric_name, values in metric_values.items():
            statistics[metric_name] = {
                'average': sum(values) / len(values),
                'minimum': min(values),
                'maximum': max(values),
                'count': len(values)
            }

        return statistics

    def get_recent_records(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most recent quality records.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of recent quality records
        """
        records = self._read_quality_records()
        return records[-limit:] if records else []

    def get_low_quality_tasks(
        self,
        threshold: float = 0.7,
        days: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get tasks with quality below threshold.

        Args:
            threshold: Quality score threshold (default: 0.7)
            days: Number of days to analyze (optional)

        Returns:
            List of low-quality task records
        """
        records = self._read_quality_records()

        if not records:
            return []

        # Filter by days if specified
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            records = [
                r for r in records
                if datetime.fromisoformat(r['timestamp']) >= cutoff_date
            ]

        # Filter by quality threshold
        low_quality = [r for r in records if r['quality_score'] < threshold]

        # Sort by quality score (lowest first)
        low_quality.sort(key=lambda x: x['quality_score'])

        return low_quality


def main():
    """Command-line interface for quality tracker."""
    parser = argparse.ArgumentParser(description='Quality Tracker System')
    parser.add_argument(
    '--dir',
    default='.claude-patterns',
    help='Tracker directory path',
)

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Record action
    record_parser = subparsers.add_parser('record', help='Record quality assessment')
    record_parser.add_argument('--task-id', required=True, help='Task ID')
    record_parser.add_argument(
    '--score',
    type=float,
    required=True,
    help='Quality score (0-1)',
)
    record_parser.add_argument('--metrics', required=True, help='Metrics JSON string')

    # Trends action
    trends_parser = subparsers.add_parser('trends', help='Show quality trends')
    trends_parser.add_argument('--days', type=int, default=30, help='Days to analyze')
    trends_parser.add_argument('--metric', help='Specific metric to analyze')

    # Average action
    average_parser = subparsers.add_parser('average', help='Show average quality')
    average_parser.add_argument('--days', type=int, help='Days to analyze')

    # Statistics action
    stats_parser = subparsers.add_parser('stats', help='Show metric statistics')
    stats_parser.add_argument('--days', type=int, help='Days to analyze')

    # Recent action
    recent_parser = subparsers.add_parser('recent', help='Show recent records')
    recent_parser.add_argument(
    '--limit',
    type=int,
    default=10,
    help='Number of records',
)

    # Low quality action
    low_parser = subparsers.add_parser('low-quality', help='Show low quality tasks')
    low_parser.add_argument(
    '--threshold',
    type=float,
    default=0.7,
    help='Quality threshold',
)
    low_parser.add_argument('--days', type=int, help='Days to analyze')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    tracker = QualityTracker(args.dir)

    try:
        if args.action == 'record':
            metrics = json.loads(args.metrics)
            success = tracker.record_quality(args.task_id, args.score, metrics)
            print(json.dumps({'success': success}, indent=2))

        elif args.action == 'trends':
            trends = tracker.get_quality_trends(days=args.days, metric=args.metric)
            print(json.dumps(trends, indent=2))

        elif args.action == 'average':
            average = tracker.get_average_quality(days=args.days)
            print(json.dumps({'average_quality': average}, indent=2))

        elif args.action == 'stats':
            stats = tracker.get_metric_statistics(days=args.days)
            print(json.dumps(stats, indent=2))

        elif args.action == 'recent':
            records = tracker.get_recent_records(limit=args.limit)
            print(json.dumps(records, indent=2))

        elif args.action == 'low-quality':
            low_quality = tracker.get_low_quality_tasks(
                threshold=args.threshold,
                days=args.days
            )
            print(json.dumps(low_quality, indent=2))

    except Exception as e:
        print(
    json.dumps({'success': False, 'error': str(e)}, indent=2),
    file=sys.stderr,
)
        sys.exit(1)


if __name__ == '__main__':
    main()
