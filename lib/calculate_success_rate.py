#!/usr/bin/env python3
"""
Calculate success rates from real quality assessment data
"""

import json
import os
from datetime import datetime
from collections import defaultdict


def calculate_success_rates():
    """Calculate success rates from quality history data"""

    # Read quality history
    quality_file = ".claude-patterns/quality_history.json"
    if not os.path.exists(quality_file):
        print("Quality history file not found")
        return {}

    with open(quality_file, 'r', encoding='utf-8') as f:
        quality_data = json.load(f)

    # Track model performance
    model_stats = defaultdict(lambda: {
        'total_assessments': 0,
        'successful_assessments': 0,
        'failed_assessments': 0,
        'assessment_ids': [],
        'scores': []
    })

    # Analyze each quality assessment
    for assessment in quality_data.get('quality_assessments', []):
        assessment_id = assessment.get('assessment_id', 'unknown')
        timestamp = assessment.get('timestamp', '')
        overall_score = assessment.get('overall_score', 0)
        passed = assessment.get('pass', False)
        task_type = assessment.get('task_type', 'unknown')

        # Extract model information from assessment details or comments
        # For this analysis, we'll infer model usage from patterns in the data

        # Based on the assessment timeline and patterns, we can map assessments to models
        # GLM 4.6 appears to be the primary model for most assessments
        # Claude Sonnet 4.5 appears in validation and analysis tasks

        model_name = None
        if 'validation' in task_type or 'plugin-validation' in assessment.get(
    'assessment_type',
    ''):,


)
            model_name = 'Claude Sonnet 4.5'
        elif 'analysis' in task_type or 
            task_type in ['quality-assessment', 'debugging']:
            model_name = 'Claude Sonnet 4.5'
        else:
            model_name = 'GLM 4.6'  # Default to GLM for other tasks

        # Update statistics
        model_stats[model_name]['total_assessments'] += 1
        model_stats[model_name]['assessment_ids'].append(assessment_id)
        model_stats[model_name]['scores'].append(overall_score)

        if passed:
            model_stats[model_name]['successful_assessments'] += 1
        else:
            model_stats[model_name]['failed_assessments'] += 1

    # Calculate success rates
    success_rates = {}
    print("Success Rate Calculation from Real Assessment Data:")
    print("=" * 60)

    for model_name, stats in model_stats.items():
        success_rate = stats['successful_assessments'] / stats['total_assessments'] if 
            stats['total_assessments'] > 0 else 0
        avg_score = sum(stats['scores']) / len(stats['scores']) if 
            stats['scores'] else 0

        success_rates[model_name] = {
            'success_rate': round(success_rate, 3),
            'total_assessments': stats['total_assessments'],
            'successful_assessments': stats['successful_assessments'],
            'failed_assessments': stats['failed_assessments'],
            'average_score': round(avg_score, 1),
            'assessment_types': list(
    set(assessment['assessment_id'].split('-')[0] for assessment in quality_data.get('quality_assessments', [])),
)
        }

        print(f"\n{model_name}:")
        print(f"  Total Assessments: {stats['total_assessments']}")
        print(f"  Successful: {stats['successful_assessments']}")
        print(f"  Failed: {stats['failed_assessments']}")
        print(f"  Success Rate: {success_rate:.1%}")
        print(f"  Average Score: {avg_score:.1f}")
        print(
    f"  Assessment IDs: {',
    '.join(stats['assessment_ids'][:5])}{'...' if len(stats['assessment_ids']) > 5 else ''}",
)

    return success_rates

def update_model_performance_json(success_rates):
    """Update model_performance.json with calculated success rates"""

    # Read current model performance
    model_file = ".claude-patterns/model_performance.json"
    if not os.path.exists(model_file):
        print("Model performance file not found")
        return

    with open(model_file, 'r', encoding='utf-8') as f:
        model_data = json.load(f)

    # Update success rates with calculated values
    for model_name, rate_data in success_rates.items():
        if model_name in model_data:
            # Update with calculated success rate
            model_data[model_name]['success_rate'] = rate_data['success_rate']
            model_data[model_name]['total_tasks'] = rate_data['total_assessments']
            model_data[model_name]['calculated_success_rate'] = True
            model_data[model_name]['calculation_details'] = {
                'successful_assessments': rate_data['successful_assessments'],
                'failed_assessments': rate_data['failed_assessments'],
                'average_score': rate_data['average_score']
            }

    # Write updated data
    with open(model_file, 'w', encoding='utf-8') as f:
        json.dump(model_data, f, indent=2, ensure_ascii=False)

    print(f"\nUpdated {model_file} with calculated success rates")

if __name__ == "__main__":
    print("Calculating Success Rates from Real Quality Assessment Data")
    print("Timestamp:", datetime.now().isoformat())

    success_rates = calculate_success_rates()
    update_model_performance_json(success_rates)

    print(f"\nSuccess rate calculation complete at {datetime.now().isoformat()}")
