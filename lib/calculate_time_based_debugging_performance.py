#!/usr/bin/env python3
"""
Calculate AI Debugging Performance Index for specific time frames
"""

import json
import os
from datetime import datetime, timedelta

def parse_timestamp(timestamp_str):
    """Parse ISO timestamp to datetime object"""
    try:
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except:
        return datetime.now()

def filter_assessments_by_timeframe(assessments, days):
    """Filter assessments within the specified time frame"""
    if not assessments:
        return []

    # Use UTC datetime for consistent comparison
    cutoff_date = datetime.now().replace(tzinfo=None) - timedelta(days=days)
    filtered_assessments = []

    for assessment in assessments:
        timestamp = parse_timestamp(assessment.get('timestamp', ''))
        # Remove timezone info for comparison
        timestamp_naive = timestamp.replace(tzinfo=None) if timestamp.tzinfo else timestamp
        if timestamp_naive >= cutoff_date:
            filtered_assessments.append(assessment)

    return filtered_assessments

def extract_debugging_assessments(assessments):
    """Extract assessments specifically related to debugging tasks"""

    debugging_assessments = []

    for assessment in assessments:
        task_type = assessment.get('task_type', 'unknown')
        assessment_id = assessment.get('assessment_id', '')
        details = assessment.get('details', {})
        issues_found = assessment.get('issues_found', [])
        recommendations = assessment.get('recommendations', [])

        # Identify debugging-related assessments
        is_debugging = (
            'debug' in task_type.lower() or
            'debugging' in assessment_id.lower() or
            'gui-debug' in assessment_id.lower() or
            'validation' in task_type.lower() or
            'error' in ' '.join(issues_found).lower() or
            'fix' in ' '.join(recommendations).lower() or
            'bug' in ' '.join(issues_found + recommendations).lower() or
            assessment.get('assessment_type', '') in ['validation', 'comprehensive-validation']
        )

        if is_debugging:
            debugging_assessments.append(assessment)

    return debugging_assessments

def classify_debugging_by_model(debugging_assessments):
    """Classify debugging assessments by AI model"""

    glm_debugging = []
    claude_debugging = []

    for assessment in debugging_assessments:
        task_type = assessment.get('task_type', 'unknown')
        assessment_id = assessment.get('assessment_id', '')

        # Classification based on task patterns and timing
        if ('validation' in task_type or
            'plugin-validation' in assessment.get('assessment_type', '') or
            'gui-debug' in assessment_id or
            'analysis' in task_type or
            'quality-assessment' in task_type):
            claude_debugging.append(assessment)
        else:
            glm_debugging.append(assessment)

    return {
        'GLM 4.6': glm_debugging,
        'Claude Sonnet 4.5': claude_debugging
    }

def calculate_quality_improvement(debugging_assessments, model_name):
    """Calculate Quality Improvement Score (QIS) using new comprehensive framework"""

    if not debugging_assessments:
        return {
            'initial_quality': 0,
            'final_quality': 0,
            'quality_gap': 0,
            'gap_closed_pct': 0,
            'regressions_detected': 0,
            'regression_rate': 0,
            'regression_penalty': 0,
            'qis': 0,
            'efficiency_index': 0,
            'relative_improvement': 0
        }

    # Sort assessments by timestamp to track progression
    sorted_assessments = sorted(debugging_assessments, key=lambda x: parse_timestamp(x.get('timestamp', '')))

    # Extract quality scores over time
    quality_scores = [a.get('overall_score', 0) for a in sorted_assessments]

    # Calculate initial and final quality (average if multiple)
    initial_quality = quality_scores[0] if len(quality_scores) == 1 else sum(quality_scores[:3]) / min(3, len(quality_scores))
    final_quality = quality_scores[-1] if len(quality_scores) == 1 else sum(quality_scores[-3:]) / min(3, len(quality_scores))

    # Quality gap analysis
    max_possible_quality = 100
    quality_gap_initial = max_possible_quality - initial_quality
    quality_gap_final = max_possible_quality - final_quality
    gap_closed = quality_gap_initial - quality_gap_final
    gap_closed_pct = (gap_closed / quality_gap_initial * 100) if quality_gap_initial > 0 else 0

    # Regression detection
    regressions_detected = 0
    for i in range(1, len(quality_scores)):
        if quality_scores[i] < quality_scores[i-1] - 2:  # 2-point tolerance
            regressions_detected += 1

    regression_rate = (regressions_detected / (len(quality_scores) - 1)) if len(quality_scores) > 1 else 0
    regression_penalty = regression_rate * 20  # As per framework

    # Calculate QIS using new formula
    qis = (0.6 * final_quality) + (0.4 * (gap_closed_pct * 100 / 100))  # Normalize gap_closed_pct to 0-1 scale

    # Supporting metrics
    total_tasks = len(debugging_assessments)
    successful_tasks = sum(1 for a in debugging_assessments if a.get('pass', False))
    success_rate = successful_tasks / total_tasks if total_tasks > 0 else 0

    # Efficiency Index (QIS × Success Rate)
    efficiency_index = qis * success_rate

    # Relative Improvement (Final Quality / Initial Quality, capped at 2.0)
    relative_improvement = min(2.0, final_quality / initial_quality) if initial_quality > 0 else 0

    return {
        'initial_quality': round(initial_quality, 1),
        'final_quality': round(final_quality, 1),
        'quality_gap': round(quality_gap_initial, 1),
        'gap_closed_pct': round(gap_closed_pct, 1),
        'regressions_detected': regressions_detected,
        'regression_rate': round(regression_rate, 3),
        'regression_penalty': round(regression_penalty, 1),
        'qis': round(qis, 1),
        'efficiency_index': round(efficiency_index, 1),
        'relative_improvement': round(relative_improvement, 2)
    }

def calculate_time_efficiency(debugging_assessments, model_name):
    """Calculate time efficiency for debugging tasks"""

    if not debugging_assessments:
        return {
            'total_tasks': 0,
            'avg_time_minutes': 0,
            'time_efficiency_score': 0,
            'time_span_hours': 0
        }

    # Sort assessments by timestamp
    sorted_assessments = sorted(debugging_assessments, key=lambda x: parse_timestamp(x.get('timestamp', '')))

    # Calculate time metrics
    if len(sorted_assessments) >= 2:
        first_time = parse_timestamp(sorted_assessments[0].get('timestamp', ''))
        last_time = parse_timestamp(sorted_assessments[-1].get('timestamp', ''))
        total_time_span = (last_time - first_time).total_seconds() / 3600  # hours

        # Average time per debugging task
        avg_time_hours = total_time_span / (len(sorted_assessments) - 1) if len(sorted_assessments) > 1 else 0
        avg_time_minutes = avg_time_hours * 60

        # Time efficiency score (faster is better)
        # Ideal debugging time is ~30 minutes per task
        ideal_time_minutes = 30
        efficiency_ratio = ideal_time_minutes / avg_time_minutes if avg_time_minutes > 0 else 1
        time_efficiency_score = min(100, max(0, efficiency_ratio * 50))  # Scale to 0-100

    else:
        total_time_span = 0
        avg_time_minutes = 0
        time_efficiency_score = 50  # Neutral score for insufficient data

    return {
        'total_tasks': len(debugging_assessments),
        'avg_time_minutes': round(avg_time_minutes, 1),
        'time_efficiency_score': round(time_efficiency_score, 1),
        'time_span_hours': round(total_time_span, 2)
    }

def calculate_debugging_performance_index(quality_metrics, time_metrics, success_rate):
    """Calculate overall AI Debugging Performance Index using new framework"""

    # New Performance Index formula with regression penalty:
    # PI = (0.40 × QIS) + (0.35 × TES) + (0.25 × SR) − Penalty

    quality_weight = 0.40
    time_weight = 0.35
    success_weight = 0.25

    # Extract QIS and regression penalty from quality metrics
    qis = quality_metrics.get('qis', 0)
    regression_penalty = quality_metrics.get('regression_penalty', 0)

    performance_index = (
        qis * quality_weight +
        time_metrics['time_efficiency_score'] * time_weight +
        success_rate * 100 * success_weight -
        regression_penalty
    )

    return max(0, round(performance_index, 1))  # Ensure non-negative

def analyze_debugging_performance_for_timeframe(days):
    """Main function to analyze AI debugging performance for specific timeframe"""

    print(f"AI Debugging Performance Analysis - Last {days} Days")
    print("=" * 60)

    # Read quality history
    quality_file = ".claude-patterns/quality_history.json"
    if not os.path.exists(quality_file):
        print("Quality history file not found")
        return {}

    with open(quality_file, 'r', encoding='utf-8') as f:
        quality_data = json.load(f)

    assessments = quality_data.get('quality_assessments', [])

    # Filter assessments by timeframe
    timeframe_assessments = filter_assessments_by_timeframe(assessments, days)
    print(f"Found {len(timeframe_assessments)} assessments in last {days} days")

    # Extract debugging-related assessments
    debugging_assessments = extract_debugging_assessments(timeframe_assessments)

    print(f"Found {len(debugging_assessments)} debugging-related assessments")

    # Classify by model
    model_debugging = classify_debugging_by_model(debugging_assessments)

    # Calculate performance metrics for each model
    debugging_performance = {}

    for model_name, model_assessments in model_debugging.items():
        print(f"\n{model_name} Debugging Performance (Last {days} days):")
        print("-" * 50)

        if not model_assessments:
            print("No debugging assessments found for this model in this timeframe")
            continue

        # Calculate quality improvement
        quality_metrics = calculate_quality_improvement(model_assessments, model_name)

        # Calculate time efficiency
        time_metrics = calculate_time_efficiency(model_assessments, model_name)

        # Calculate success rate
        successful = sum(1 for a in model_assessments if a.get('pass', False))
        total = len(model_assessments)
        success_rate = (successful / total) if total > 0 else 0

        # Calculate overall performance index
        performance_index = calculate_debugging_performance_index(quality_metrics, time_metrics, success_rate)

        # Store results
        debugging_performance[model_name] = {
            'quality_metrics': quality_metrics,
            'time_metrics': time_metrics,
            'success_rate': success_rate,
            'performance_index': performance_index,
            'total_debugging_tasks': total,
            'debugging_assessments': model_assessments
        }

        # Display results with new metrics
        print(f"Debugging Tasks: {total}")
        print(f"Success Rate: {success_rate:.1%}")
        print(f"Initial Quality: {quality_metrics['initial_quality']}")
        print(f"Final Quality: {quality_metrics['final_quality']}")
        print(f"Quality Gap Closed: {quality_metrics['gap_closed_pct']:.1f}%")
        print(f"Regressions Detected: {quality_metrics['regressions_detected']}")
        print(f"Regression Penalty: -{quality_metrics['regression_penalty']}")
        print(f"QIS (Quality Improvement Score): {quality_metrics['qis']}/100")
        print(f"Efficiency Index: {quality_metrics['efficiency_index']}/100")
        print(f"Relative Improvement: {quality_metrics['relative_improvement']}x")
        print(f"Avg Time per Task: {time_metrics['avg_time_minutes']} minutes")
        print(f"Time Efficiency Score: {time_metrics['time_efficiency_score']}/100")
        print(f"DEBUGGING PERFORMANCE INDEX: {performance_index}/100")

    # Rank models by performance index
    ranked_models = sorted(debugging_performance.items(), key=lambda x: x[1]['performance_index'], reverse=True)

    print(f"\nAI DEBUGGING PERFORMANCE RANKINGS (Last {days} days):")
    print("=" * 70)
    for rank, (model_name, metrics) in enumerate(ranked_models, 1):
        pi = metrics['performance_index']
        qis = metrics['quality_metrics']['qis']
        time_score = metrics['time_metrics']['time_efficiency_score']
        success_rate = metrics['success_rate']
        penalty = metrics['quality_metrics']['regression_penalty']
        efficiency_index = metrics['quality_metrics']['efficiency_index']

        print(f"{rank}. {model_name}")
        print(f"   Performance Index: {pi}/100")
        print(f"   QIS (Quality Improvement): {qis}/100")
        print(f"   Time Efficiency Score: {time_score}/100")
        print(f"   Success Rate: {success_rate:.1%}")
        print(f"   Regression Penalty: -{penalty}")
        print(f"   Efficiency Index: {efficiency_index}/100")
        print()

    # Save results to file with timeframe suffix
    save_debugging_performance_results(debugging_performance, ranked_models, days)

    return debugging_performance, ranked_models

def save_debugging_performance_results(debugging_performance, ranked_models, days):
    """Save debugging performance results to JSON file with timeframe"""

    results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'timeframe_days': days,
        'timeframe_label': get_timeframe_label(days),
        'total_debugging_assessments': sum(len(m['debugging_assessments']) for m in debugging_performance.values()),
        'performance_rankings': [
            {
                'rank': rank + 1,
                'model': model_name,
                'performance_index': metrics['performance_index'],
                'qis': metrics['quality_metrics']['qis'],
                'quality_improvement_score': metrics['quality_metrics']['qis'],  # Keep for compatibility
                'time_efficiency_score': metrics['time_metrics']['time_efficiency_score'],
                'success_rate': metrics['success_rate'],
                'total_debugging_tasks': metrics['total_debugging_tasks'],
                'regression_penalty': metrics['quality_metrics']['regression_penalty'],
                'efficiency_index': metrics['quality_metrics']['efficiency_index'],
                'relative_improvement': metrics['quality_metrics']['relative_improvement'],
                'initial_quality': metrics['quality_metrics']['initial_quality'],
                'final_quality': metrics['quality_metrics']['final_quality'],
                'gap_closed_pct': metrics['quality_metrics']['gap_closed_pct']
            }
            for rank, (model_name, metrics) in enumerate(ranked_models)
        ],
        'detailed_metrics': debugging_performance
    }

    # Save to .claude-patterns directory
    output_file = f".claude-patterns/debugging_performance_{days}days.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Debugging performance results saved to: {output_file}")

def get_timeframe_label(days):
    """Get human-readable label for timeframe."""
    if days == 1:
        return "Today"
    elif days == 3:
        return "Last 3 Days"
    elif days == 7:
        return "Last Week"
    elif days == 30:
        return "Last Month"
    else:
        return f"Last {days} Days"

if __name__ == "__main__":
    import sys

    # Get days from command line argument or default to 30
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 30

    performance_data, rankings = analyze_debugging_performance_for_timeframe(days)
    print(f"\nAI Debugging Performance Index analysis complete for {get_timeframe_label(days)} at {datetime.now().isoformat()}")