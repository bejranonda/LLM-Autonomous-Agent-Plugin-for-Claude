#!/usr/bin/env python3
"""
Calculate performance based on quality score improvement over time
"""

import json
import os
from datetime import datetime
import statistics

def parse_timestamp(timestamp_str):
    """Parse ISO timestamp to datetime object"""
    try:
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except:
        return datetime.now()

def calculate_quality_improvement_trend(assessments, model_name):
    """Calculate how quality scores improve over time for a specific model"""

    if not assessments:
        return {
            'improvement_rate': 0,
            'total_improvement': 0,
            'time_span_days': 0,
            'trend_direction': 'stable',
            'performance_score': 0,
            'data_points': 0
        }

    # Sort assessments by timestamp
    sorted_assessments = sorted(assessments, key=lambda x: parse_timestamp(x.get('timestamp', '')))

    # Extract quality scores over time
    quality_timeline = []
    for assessment in sorted_assessments:
        timestamp = parse_timestamp(assessment.get('timestamp', ''))
        quality_score = assessment.get('overall_score', 0)
        assessment_id = assessment.get('assessment_id', 'unknown')

        quality_timeline.append({
            'timestamp': timestamp,
            'score': quality_score,
            'assessment_id': assessment_id
        })

    if len(quality_timeline) < 2:
        # Not enough data points for trend calculation
        return {
            'improvement_rate': 0,
            'total_improvement': 0,
            'time_span_days': 0,
            'trend_direction': 'insufficient_data',
            'performance_score': quality_timeline[0]['score'] if quality_timeline else 0,
            'data_points': len(quality_timeline)
        }

    # Calculate quality improvement over time
    first_score = quality_timeline[0]['score']
    last_score = quality_timeline[-1]['score']
    total_improvement = last_score - first_score

    # Calculate time span
    first_time = quality_timeline[0]['timestamp']
    last_time = quality_timeline[-1]['timestamp']
    time_span_days = (last_time - first_time).days + 1  # +1 to include both days

    # Calculate improvement rate (points per day)
    improvement_rate = total_improvement / time_span_days if time_span_days > 0 else 0

    # Determine trend direction
    if improvement_rate > 0.5:
        trend_direction = 'improving'
    elif improvement_rate < -0.5:
        trend_direction = 'declining'
    else:
        trend_direction = 'stable'

    # Calculate performance score based on improvement rate and absolute scores
    # Performance = (Current Score × 60%) + (Improvement Rate × 20 points/day × 40%)
    current_score = last_score
    improvement_bonus = min(40, max(-40, improvement_rate * 20))  # Cap at ±40 points
    performance_score = (current_score * 0.6) + improvement_bonus

    # Calculate linear regression for more accurate trend
    if len(quality_timeline) >= 3:
        # Simple linear regression: y = mx + b
        n = len(quality_timeline)
        x_values = list(range(n))  # 0, 1, 2, ...
        y_values = [q['score'] for q in quality_timeline]

        # Calculate slope (m)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)

        # Convert slope to points per day (approximation)
        if time_span_days > 1:
            daily_improvement = slope * (time_span_days / n)
        else:
            daily_improvement = slope

        # Recalculate performance score using regression
        regression_bonus = min(40, max(-40, daily_improvement * 20))
        performance_score = (current_score * 0.6) + regression_bonus

        # Update improvement rate with regression result
        improvement_rate = daily_improvement
    else:
        # Use simple difference for small datasets
        pass

    return {
        'improvement_rate': round(improvement_rate, 2),
        'total_improvement': round(total_improvement, 1),
        'time_span_days': time_span_days,
        'trend_direction': trend_direction,
        'performance_score': round(performance_score, 1),
        'data_points': len(quality_timeline),
        'first_score': first_score,
        'last_score': last_score,
        'quality_timeline': [
                {
                    'timestamp': q['timestamp'].isoformat(),
                    'score': q['score'],
                    'assessment_id': q['assessment_id']
                } for q in quality_timeline
            ]
    }

def classify_assessments_by_model(assessments):
    """Classify assessments by model based on task patterns and timestamps"""

    glm_assessments = []
    claude_assessments = []

    for assessment in assessments:
        task_type = assessment.get('task_type', 'unknown')
        assessment_id = assessment.get('assessment_id', '')
        timestamp = assessment.get('timestamp', '')

        # Classification logic based on task patterns and time
        if ('validation' in task_type or
            'plugin-validation' in assessment.get('assessment_type', '') or
            'analysis' in task_type or
            task_type in ['quality-assessment', 'debugging', 'gui-validation']):
            claude_assessments.append(assessment)
        else:
            # Default to GLM for feature implementations, quality checks
            glm_assessments.append(assessment)

    return {
        'GLM 4.6': glm_assessments,
        'Claude Sonnet 4.5': claude_assessments
    }

def main():
    """Main performance calculation based on quality improvement over time"""

    print("Calculating Performance Based on Quality Score Improvement Over Time")
    print("=" * 75)

    # Read quality history
    quality_file = ".claude-patterns/quality_history.json"
    if not os.path.exists(quality_file):
        print("Quality history file not found")
        return

    with open(quality_file, 'r', encoding='utf-8') as f:
        quality_data = json.load(f)

    assessments = quality_data.get('quality_assessments', [])

    # Classify assessments by model
    model_assessments = classify_assessments_by_model(assessments)

    # Calculate time-based performance for each model
    performance_results = {}

    for model_name, model_specific_assessments in model_assessments.items():
        print(f"\n{model_name} - Quality Improvement Analysis:")
        print("-" * 55)

        # Calculate quality improvement trend
        trend_analysis = calculate_quality_improvement_trend(model_specific_assessments, model_name)

        # Calculate success rate
        successful = sum(1 for a in model_specific_assessments if a.get('pass', False))
        total = len(model_specific_assessments)
        success_rate = (successful / total * 100) if total > 0 else 0

        # Store results
        performance_results[model_name] = {
            'quality_trend': trend_analysis,
            'success_rate': round(success_rate / 100, 3),  # Convert to 0-1 scale
            'total_assessments': total,
            'performance_calculation_method': 'quality_improvement_over_time'
        }

        # Display results
        print(f"Total Assessments: {total}")
        print(f"Time Period: {trend_analysis['time_span_days']} days")
        print(f"First Score: {trend_analysis['first_score']}")
        print(f"Current Score: {trend_analysis['last_score']}")
        print(f"Total Improvement: {trend_analysis['total_improvement']:+.1f} points")
        print(f"Improvement Rate: {trend_analysis['improvement_rate']:+.2f} points/day")
        print(f"Trend Direction: {trend_analysis['trend_direction']}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Performance Score: {trend_analysis['performance_score']}/100")

        # Show detailed timeline
        if trend_analysis['quality_timeline']:
            print(f"\nQuality Score Timeline:")
            for i, point in enumerate(trend_analysis['quality_timeline'][-5:]):  # Last 5 points
                timestamp_str = point['timestamp'] if isinstance(point['timestamp'], str) else point['timestamp'].isoformat()
                # Parse the timestamp string to format it
                try:
                    dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    date_str = dt.strftime('%m-%d %H:%M')
                except:
                    date_str = timestamp_str[:16]  # First 16 chars as fallback
                print(f"  {date_str}: {point['score']} ({point['assessment_id']})")

    # Update model performance file
    update_model_performance_file(performance_results)

    return performance_results

def update_model_performance_file(performance_results):
    """Update model_performance.json with time-based performance metrics"""

    model_file = ".claude-patterns/model_performance.json"
    if not os.path.exists(model_file):
        print("Model performance file not found")
        return

    with open(model_file, 'r', encoding='utf-8') as f:
        model_data = json.load(f)

    # Update each model with time-based performance metrics
    for model_name, results in performance_results.items():
        if model_name in model_data:
            trend = results['quality_trend']

            # Update with time-based performance metrics
            model_data[model_name].update({
                'performance_index': trend['performance_score'],
                'improvement_rate': trend['improvement_rate'],
                'total_improvement': trend['total_improvement'],
                'time_span_days': trend['time_span_days'],
                'trend_direction': trend['trend_direction'],
                'first_score': trend['first_score'],
                'last_score': trend['last_score'],
                'performance_calculation_method': 'quality_improvement_over_time',
                'calculation_timestamp': datetime.now().isoformat(),
                'quality_trend_data': trend
            })

    # Write updated data
    with open(model_file, 'w', encoding='utf-8') as f:
        json.dump(model_data, f, indent=2, ensure_ascii=False)

    print(f"\nUpdated {model_file} with time-based performance metrics")

if __name__ == "__main__":
    results = main()
    print(f"\nTime-based performance calculation complete at {datetime.now().isoformat()}")