#!/usr/bin/env python3
"""
Calculate AI Debugging Performance Index based on quality improvement, time efficiency, and overall performance
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
    """Calculate quality improvement from debugging activities"""

    if not debugging_assessments:
        return {
            'before_score': 0,
            'after_score': 0,
            'improvement': 0,
            'improvement_percentage': 0,
            'improvement_score': 0
        }

    # Sort assessments by timestamp to track progression
    sorted_assessments = sorted(debugging_assessments, key=lambda x: parse_timestamp(x.get('timestamp', '')))

    # Calculate quality improvement
    if len(sorted_assessments) >= 2:
        before_score = sorted_assessments[0].get('overall_score', 0)
        after_score = sorted_assessments[-1].get('overall_score', 0)
        improvement = after_score - before_score

        # Calculate improvement percentage
        improvement_percentage = (improvement / before_score * 100) if before_score > 0 else 0

        # Normalize improvement score (0-100 scale)
        # Max expected improvement is ~30 points, scale accordingly
        improvement_score = min(100, max(0, (improvement + 15) * 2))  # +15 to allow negative improvements, *2 for scaling

    elif len(sorted_assessments) == 1:
        # Single assessment - assume improvement from baseline
        score = sorted_assessments[0].get('overall_score', 0)
        before_score = 70  # Assumed baseline before debugging
        after_score = score
        improvement = after_score - before_score
        improvement_percentage = (improvement / before_score * 100) if before_score > 0 else 0
        improvement_score = min(100, max(0, (improvement + 15) * 2))
    else:
        before_score = after_score = improvement = improvement_percentage = improvement_score = 0

    return {
        'before_score': before_score,
        'after_score': after_score,
        'improvement': improvement,
        'improvement_percentage': improvement_percentage,
        'improvement_score': round(improvement_score, 1)
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
    """Calculate overall AI Debugging Performance Index"""

    # Performance Index formula:
    # PI = (Quality Improvement Score × 40%) + (Time Efficiency Score × 35%) + (Success Rate × 25%)

    quality_weight = 0.40
    time_weight = 0.35
    success_weight = 0.25

    performance_index = (
        quality_metrics['improvement_score'] * quality_weight +
        time_metrics['time_efficiency_score'] * time_weight +
        success_rate * 100 * success_weight
    )

    return round(performance_index, 1)

def analyze_debugging_performance():
    """Main function to analyze AI debugging performance"""

    print("AI Debugging Performance Index Analysis")
    print("=" * 50)

    # Read quality history
    quality_file = ".claude-patterns/quality_history.json"
    if not os.path.exists(quality_file):
        print("Quality history file not found")
        return {}

    with open(quality_file, 'r', encoding='utf-8') as f:
        quality_data = json.load(f)

    assessments = quality_data.get('quality_assessments', [])

    # Extract debugging-related assessments
    debugging_assessments = extract_debugging_assessments(assessments)

    print(f"Found {len(debugging_assessments)} debugging-related assessments out of {len(assessments)} total")

    # Classify by model
    model_debugging = classify_debugging_by_model(debugging_assessments)

    # Calculate performance metrics for each model
    debugging_performance = {}

    for model_name, model_assessments in model_debugging.items():
        print(f"\n{model_name} Debugging Performance:")
        print("-" * 40)

        if not model_assessments:
            print("No debugging assessments found for this model")
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

        # Display results
        print(f"Debugging Tasks: {total}")
        print(f"Success Rate: {success_rate:.1%}")
        print(f"Quality Before: {quality_metrics['before_score']}")
        print(f"Quality After: {quality_metrics['after_score']}")
        print(f"Quality Improvement: {quality_metrics['improvement']:+.1f} points ({quality_metrics['improvement_percentage']:+.1f}%)")
        print(f"Avg Time per Task: {time_metrics['avg_time_minutes']} minutes")
        print(f"Time Efficiency Score: {time_metrics['time_efficiency_score']}/100")
        print(f"Quality Improvement Score: {quality_metrics['improvement_score']}/100")
        print(f"DEBUGGING PERFORMANCE INDEX: {performance_index}/100")

        # Show debugging task details
        print(f"\nDebugging Tasks Timeline:")
        for assessment in model_assessments[:5]:  # Show first 5
            timestamp = parse_timestamp(assessment.get('timestamp', ''))
            date_str = timestamp.strftime('%m-%d %H:%M')
            score = assessment.get('overall_score', 0)
            task_type = assessment.get('task_type', 'unknown')
            passed = "PASS" if assessment.get('pass', False) else "FAIL"
            print(f"  {date_str}: {score} ({task_type}) {passed}")

    # Rank models by performance index
    ranked_models = sorted(debugging_performance.items(), key=lambda x: x[1]['performance_index'], reverse=True)

    print(f"\nAI DEBUGGING PERFORMANCE RANKINGS:")
    print("=" * 50)
    for rank, (model_name, metrics) in enumerate(ranked_models, 1):
        pi = metrics['performance_index']
        quality_score = metrics['quality_metrics']['improvement_score']
        time_score = metrics['time_metrics']['time_efficiency_score']
        success_rate = metrics['success_rate']

        print(f"{rank}. {model_name}")
        print(f"   Performance Index: {pi}/100")
        print(f"   Quality Improvement: {quality_score}/100")
        print(f"   Time Efficiency: {time_score}/100")
        print(f"   Success Rate: {success_rate:.1%}")
        print()

    # Save results to file
    save_debugging_performance_results(debugging_performance, ranked_models)

    return debugging_performance, ranked_models

def save_debugging_performance_results(debugging_performance, ranked_models):
    """Save debugging performance results to JSON file"""

    results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'total_debugging_assessments': sum(len(m['debugging_assessments']) for m in debugging_performance.values()),
        'performance_rankings': [
            {
                'rank': rank + 1,
                'model': model_name,
                'performance_index': metrics['performance_index'],
                'quality_improvement_score': metrics['quality_metrics']['improvement_score'],
                'time_efficiency_score': metrics['time_metrics']['time_efficiency_score'],
                'success_rate': metrics['success_rate'],
                'total_debugging_tasks': metrics['total_debugging_tasks']
            }
            for rank, (model_name, metrics) in enumerate(ranked_models)
        ],
        'detailed_metrics': debugging_performance
    }

    # Save to .claude-patterns directory
    output_file = ".claude-patterns/debugging_performance.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Debugging performance results saved to: {output_file}")

if __name__ == "__main__":
    performance_data, rankings = analyze_debugging_performance()
    print(f"\nAI Debugging Performance Index analysis complete at {datetime.now().isoformat()}")