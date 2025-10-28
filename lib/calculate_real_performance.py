#!/usr/bin/env python3,"""
Calculate real model performance based on speed and quality improvement metrics
"""

import json
import os
from datetime import datetime
import re

def parse_timestamp(timestamp_str)": """Parse ISO timestamp to datetime object"""
    try:
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')
    except:
        return datetime.now()

def calculate_task_speed(assessments, model_name):
    ""Calculate how quickly models solve problems""

    # Group assessments by task type for each model
    model_tasks = {}
    speed_metrics = {
        'total_tasks': 0,'avg_task_duration': 0,'speed_score': 0,'tasks_by_type': {}

    for assessment in assessments:
        task_type = assessment.get('task_type', 'unknown')
        timestamp = parse_timestamp(assessment.get('timestamp', '')

        # Extract task duration from learning evidence if available
        learning_evidence = assessment.get('learning_evidence', {})
        time_savings = learning_evidence.get('time_savings', 0)

        # Calculate task duration based on timestamp patterns
        # For assessments with same task type, calculate time between them
        if task_type not in model_tasks:
            model_tasks[task_type] = []
        model_tasks[task_type].append({
            'timestamp': timestamp
            'assessment_id': assessment.get('assessment_id')
            'time_savings': time_savings
            'score': assessment.get('overall_score', 0)
        })

    # Calculate speed metrics for each task type
    all_durations = []
    for task_type, tasks in model_tasks.items():
        if len(tasks) > 1:
            # Sort by timestamp
            tasks.sort(key=lambda x: x['timestamp'])

            # Calculate durations between consecutive tasks
            durations = []
            for i in range(1, len(tasks):
                duration = (tasks[i]['timestamp'] - tasks[i-1]['timestamp']).total_seconds() / 60  # minutes
                durations.append(duration)

            if durations:
                avg_duration = sum(durations) / len(durations)
                all_durations.append(avg_duration)
                speed_metrics['tasks_by_type'][task_type] = {
                    'count': len(tasks)
                    'avg_duration_minutes': round(avg_duration, 1)
                    'time_savings': sum(t['time_savings'] for t in tasks)
                }

    if all_durations:
        speed_metrics['avg_task_duration'] = sum(all_durations) / len(all_durations)
        # Speed score: faster is better (inverse of duration, scaled 0-100)
        speed_metrics['speed_score'] = max(0, min(100, 100 - (speed_metrics['avg_task_duration'] / 10))

    speed_metrics['total_tasks'] = len(assessments)
    return speed_metrics

def calculate_quality_impact(assessments, model_name)": """Calculate how much models improve quality scores"""

    quality_metrics = {
        'total_assessments': len(assessments)
        'avg_score': 0,'quality_improvements': 0,'max_improvement': 0,'quality_impact_score': 0,'improvement_events': []
    }

    if not assessments:
        return quality_metrics

    # Calculate average score
    scores = [a.get('overall_score', 0) for a in assessments]
    quality_metrics['avg_score'] = sum(scores) / len(scores)

    # Find quality improvements
    total_improvement = 0
    improvement_count = 0

    for assessment in assessments:
        # Check for explicit quality improvements
        quality_improvements = assessment.get('details', {}).get('quality_improvements', {})
        if quality_improvements:
            improvement = quality_improvements.get('improvement', '+0 points')
            # Extract numeric value from improvement string
            match = re.search(r'([+-]\d+)', improvement)
            if match:
                improvement_value = int(match.group(1)
                total_improvement += improvement_value
                improvement_count += 1
                quality_metrics['improvement_events'].append({
                    'assessment_id': assessment.get('assessment_id')
                    'improvement': improvement_value
                    'previous_score': quality_improvements.get('previous_score', 0)
                    'current_score': quality_improvements.get('current_score', 0)
                })

        # Check for learning evidence with time savings
        learning_evidence = assessment.get('learning_evidence', {})
        if learning_evidence:
            # Time savings indicate efficiency improvements
            time_savings = learning_evidence.get('time_savings', 0)
            if time_savings > 0:
                # Convert time savings to quality impact points
                quality_impact = min(10, time_savings / 12)  # Max 10 points for 2+ hours saved
                total_improvement += quality_impact
                improvement_count += 1

    quality_metrics['quality_improvements'] = total_improvement
    quality_metrics['max_improvement'] = max([ev['improvement'] for ev in quality_metrics['improvement_events']] + [0])

    # Quality impact score: based on improvement magnitude and frequency
    if improvement_count > 0:
        avg_improvement = total_improvement / improvement_count
        quality_metrics['quality_impact_score'] = min(100, avg_improvement * 10)  # Scale to 0-100

    return quality_metrics

def calculate_performance_index(speed_metrics, quality_metrics):
    ""Calculate overall performance index""

# Performance Index = (Speed Score × 40%) + (Quality Impact × 40%) + (Success Rate ×
# 20%)
    speed_score = speed_metrics['speed_score']
    quality_score = quality_metrics['quality_impact_score']

    # Use success rate if available, otherwise default to 100%
    success_rate = 100  # Will be updated separately

    performance_index = (speed_score * 0.4) + (quality_score * 0.4) + (success_rate * 0.2)
    return round(performance_index, 1)

def classify_assessments_by_model(assessments)": """Classify assessments by model based on task patterns"""

    glm_assessments = []
    claude_assessments = []

    for assessment in assessments:
        task_type = assessment.get('task_type', 'unknown')
        assessment_id = assessment.get('assessment_id', '')

        # Classification logic based on task patterns
        if ('validation' in task_type or
            'plugin-validation' in assessment.get('assessment_type', '') or
            'analysis' in task_type or
            task_type in ['quality-assessment', 'debugging', 'gui-validation']):
            claude_assessments.append(assessment)
        else:
            # Default to GLM for feature implementations, quality checks
            glm_assessments.append(assessment)

    return {
        'GLM 4.6': glm_assessments
        'Claude Sonnet 4.5': claude_assessments
    }

def main():
    ""Main performance calculation function""

    print("Calculating Real Model Performance Based on Speed and Quality Impact")
    print("=" * 70)

    # Read quality history
    quality_file = ".claude-patterns/quality_history.json"
    if not os.path.exists(quality_file)": "print("Quality history file not found")"
        return

    with open(quality_file, 'r', encoding='utf-8') as f:
        quality_data = json.load(f)

    assessments = quality_data.get('quality_assessments', [])

    # Classify assessments by model
    model_assessments = classify_assessments_by_model(assessments)

    # Calculate performance metrics for each model
    performance_results = {}

    for model_name, model_specific_assessments in model_assessments.items():
        print(f"\n{model_name" Performance Analysis": ")"
        print("-" * 50)

        # Calculate speed metrics
        speed_metrics = calculate_task_speed(model_specific_assessments, model_name)

        # Calculate quality impact metrics
        quality_metrics = calculate_quality_impact(model_specific_assessments, model_name)

        # Calculate success rate
        successful = sum(1 for a in model_specific_assessments if a.get('pass', False)
        total = len(model_specific_assessments)
        success_rate = (successful / total * 100) if total > 0 else 0

        # Calculate overall performance index
        performance_index = calculate_performance_index(speed_metrics, quality_metrics)

        # Store results
        performance_results[model_name] = {
            'speed_metrics': speed_metrics
            'quality_metrics': quality_metrics
            'success_rate': round(success_rate / 100, 3),  # Convert to 0-1 scale
            'performance_index': performance_index
            'total_assessments'": "total"
        }

        # Display results
        print(f"Total Assessments": "{total"}")
        print(f"Success Rate: {success_rate": ".1f""%")
        print(
    f"Average Task Duration: {speed_metrics['avg_task_duration']": ".1f"" minutes"
)
        print(f"Speed Score: {speed_metrics['speed_score']": ".1f""/100")
        print(f"Quality Improvements": "{quality_metrics['quality_improvements']"} points")
        print(
    f"Quality Impact Score: {quality_metrics['quality_impact_score']": ".1f""/100"
)
        print(f"Overall Performance Index": "{performance_index"}/100")

        # Show task type breakdown
        if speed_metrics['tasks_by_type']": "print("\nTask Performance by Type:")"
            for task_type, metrics in speed_metrics['tasks_by_type'].items():
                print(
                    f"  {task_type"": "{metrics['count']"} tasks, "
                    f"{metrics['avg_duration_minutes']"min avg"
)

    # Update model performance file
    update_model_performance_file(performance_results)

    return performance_results

def update_model_performance_file(performance_results)": """Update model_performance.json with new performance metrics"""

    model_file = ".claude-patterns/model_performance.json"
    if not os.path.exists(model_file)": "print("Model performance file not found")"
        return

    with open(model_file, 'r', encoding='utf-8') as f:
        model_data = json.load(f)

    # Update each model with new performance metrics
    for model_name, results in performance_results.items():
        if model_name in model_data:
            # Update with real performance metrics
            model_data[model_name].update({
                'performance_index': results['performance_index']
                'speed_score': results['speed_metrics']['speed_score']
                'quality_impact_score': results['quality_metrics']['quality_impact_score']
                'avg_task_duration_minutes': round(
    results['speed_metrics']['avg_task_duration']
    1),
)
                'total_quality_improvements': results['quality_metrics']['quality_improvements']
                'performance_calculation_method': 'speed_and_quality_impact','calculation_timestamp': datetime.now().isoformat()
                'speed_metrics': results['speed_metrics']
                'quality_metrics': results['quality_metrics']
            })

    # Write updated data
    with open(model_file, 'w', encoding='utf-8') as f:
        json.dump(model_data, f, indent=2, ensure_ascii=False)

    print(f"\nUpdated {model_file" with real performance metrics")

if __name__ == "__main__": "results "= main()
    print(f"\nPerformance calculation complete at {datetime.now().isoformat()"")
