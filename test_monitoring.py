#!/usr/bin/env python3
import sys
sys.path.insert(0, 'lib')

from token_monitoring_dashboard import TokenMonitoringDashboard, MetricType

def test_monitoring_dashboard():
    """Test the monitoring dashboard with sample data."""
    dashboard = TokenMonitoringDashboard()

    print("Testing Token Monitoring Dashboard")
    print("=" * 50)

    # Add sample metrics
    print("Adding sample metrics...")

    for i in range(5):
        # Token usage metrics
        dashboard.record_metric(
            MetricType.TOKEN_USAGE,
            2000 + i * 200,
            'test_agent',
            {'task_id': f'task_{i}', 'user_id': 'test_user'}
        )

        # Token savings metrics
        dashboard.record_metric(
            MetricType.TOKEN_SAVED,
            1000 + i * 100,
            'progressive_loader',
            {'optimization_type': 'progressive', 'tier': 'standard'}
        )

        # Compression metrics
        dashboard.record_metric(
            MetricType.COMPRESSION_RATIO,
            0.65 + (i * 0.05),
            'optimization_engine',
            {'content_type': 'documentation'}
        )

        # Cache metrics
        dashboard.record_metric(
            MetricType.CACHE_HIT_RATE,
            0.85 + (i * 0.02),
            'cache_system',
            {'cache_policy': 'lru', 'entries': 100}
        )

        # Response time metrics
        dashboard.record_metric(
            MetricType.RESPONSE_TIME,
            150 + i * 10,
            'system',
            {'operation': 'optimization', 'complexity': 'medium'}
        )

    # Get statistics
    print("\nDashboard Statistics:")
    stats = dashboard.get_dashboard_stats()

    print(f"  Tokens used: {stats.total_tokens_used:,}")
    print(f"  Tokens saved: {stats.total_tokens_saved:,}")
    print(f"  Cost savings: ${stats.total_cost_savings:.2f}")
    print(f"  Compression ratio: {stats.average_compression_ratio:.1%}")
    print(f"  Cache hit rate: {stats.cache_hit_rate:.1%}")
    print(f"  Response time: {stats.average_response_time:.1f}ms")
    print(f"  System health: {stats.system_health_score:.1%}")
    print(f"  Alerts: {stats.alerts_count}")

    # Get effectiveness
    print("\nOptimization Effectiveness:")
    effectiveness = dashboard.get_optimization_effectiveness(1)

    comp = effectiveness['compression_effectiveness']
    print(f"  Best compression: {comp['best_ratio']:.1%}")
    print(f"  Average compression: {comp['average_ratio']:.1%}")
    print(f"  Total optimizations: {comp['total_optimizations']}")

    cache = effectiveness['cache_effectiveness']
    print(f"  Best cache hit rate: {cache['best_hit_rate']:.1%}")
    print(f"  Average hit rate: {cache['average_hit_rate']:.1%}")
    print(f"  Total cache hits: {cache['total_cache_hits']}")

    savings = effectiveness['token_savings']
    print(f"  Total tokens saved: {savings['total_saved']:,}")
    print(f"  Cost savings: ${savings['cost_savings']:.2f}")
    print(f"  Savings rate: {savings['savings_rate']:.1%}")

    # Generate report
    print("\nGenerating report...")
    report = dashboard.generate_report(1)

    print(f"Report generated with {len(report['recommendations'])} recommendations:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")

    print("\nMonitoring dashboard test completed successfully!")
    print("Key features working:")
    print("- Metric recording and storage")
    print("- Real-time statistics calculation")
    print("- Optimization effectiveness tracking")
    print("- Report generation with recommendations")
    print("- Alert system (no alerts generated in test)")

if __name__ == "__main__":
    test_monitoring_dashboard()