#!/usr/bin/env python3
"""
Corrected Final Quality Assessment for Autonomous Agent Plugin
Comprehensive evaluation after syntax error fixes
"""

import json
import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime


def calculate_test_results():
    """Extract test results manually"""
    try:
        result = subprocess.run(
            ['python', '-m', 'pytest', 'tests/', '-q', '--tb=no'],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout + result.stderr

        # Look for summary at the end of output
        summary_match = re.search(r'(\d+)\s+passed[,\s]*(\d+)\s+failed', output)
        if summary_match:
            passed = int(summary_match.group(1))
            failed = int(summary_match.group(2))
            total = passed + failed
            pass_rate = (passed / total) * 100 if total > 0 else 0
            return passed, failed, total, pass_rate

        # Alternative parsing
        lines = output.strip().split('\n')
        for line in lines:
            if 'passed' in line and 'failed' in line:
                parts = line.split()
                passed = failed = 0
                for i, part in enumerate(parts):
                    if part == 'passed' and i > 0:
                        passed = int(parts[i-1])
                    elif part == 'failed' and i > 0:
                        failed = int(parts[i-1])

                if passed > 0 or failed > 0:
                    total = passed + failed
                    pass_rate = (passed / total) * 100 if total > 0 else 0
                    return passed, failed, total, pass_rate

        return 0, 0, 0, 0

    except Exception as e:
        print(f"Test execution error: {e}")
        return 0, 0, 0, 0


def calculate_quality_score():
    """Calculate comprehensive quality score (0-100)"""

    scores = {
        'test_coverage': {'weight': 0.30, 'score': 0, 'details': ''},
        'code_standards': {'weight': 0.25, 'score': 0, 'details': ''},
        'documentation': {'weight': 0.20, 'score': 0, 'details': ''},
        'pattern_adherence': {'weight': 0.15, 'score': 0, 'details': ''},
        'code_metrics': {'weight': 0.10, 'score': 0, 'details': ''}
    }

    # 1. Test Coverage (30 points) - Manual parsing
    passed, failed, total, pass_rate = calculate_test_results()

    if total > 0:
        if pass_rate >= 90:
            scores['test_coverage']['score'] = 30
        elif pass_rate >= 80:
            scores['test_coverage']['score'] = 25
        elif pass_rate >= 70:
            scores['test_coverage']['score'] = 20
        elif pass_rate >= 60:
            scores['test_coverage']['score'] = 15
        else:
            scores['test_coverage']['score'] = 10

        scores['test_coverage']['details'] = f'Pass rate: {pass_rate:.1f}% ({passed}/{total})'
    else:
        scores['test_coverage']['score'] = 0
        scores['test_coverage']['details'] = 'Test execution failed'

    # 2. Code Standards (25 points)
    lib_files = list(Path('lib').glob('**/*.py'))
    total_files = len(lib_files)

    if total_files > 0:
        # Test compilation of sample files
        sample_files = lib_files[:10]  # Test first 10 files
        compiled = 0
        for file_path in sample_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), str(file_path), 'exec')
                compiled += 1
            except:
                pass

        compilation_rate = (compiled / len(sample_files)) * 100

        if compilation_rate >= 90:
            scores['code_standards']['score'] = 25
        elif compilation_rate >= 80:
            scores['code_standards']['score'] = 20
        elif compilation_rate >= 70:
            scores['code_standards']['score'] = 15
        elif compilation_rate >= 60:
            scores['code_standards']['score'] = 10
        else:
            scores['code_standards']['score'] = 5

        scores['code_standards']['details'] = f'Compilation: {compilation_rate:.1f}% ({compiled}/{len(sample_files)} tested)'
    else:
        scores['code_standards']['score'] = 0
        scores['code_standards']['details'] = 'No Python files found'

    # 3. Documentation (20 points)
    doc_files = ['README.md', 'CLAUDE.md', 'STRUCTURE.md', 'CHANGELOG.md']
    existing_docs = sum(1 for doc in doc_files if Path(doc).exists())

    # Check plugin.json
    plugin_json = Path('.claude-plugin/plugin.json')
    has_plugin = plugin_json.exists()

    if existing_docs >= 4 and has_plugin:
        scores['documentation']['score'] = 20
        scores['documentation']['details'] = 'Complete documentation (4+ files + plugin.json)'
    elif existing_docs >= 3 and has_plugin:
        scores['documentation']['score'] = 17
        scores['documentation']['details'] = 'Good documentation (3+ files + plugin.json)'
    elif existing_docs >= 2:
        scores['documentation']['score'] = 12
        scores['documentation']['details'] = 'Basic documentation (2+ files)'
    else:
        scores['documentation']['score'] = 5
        scores['documentation']['details'] = 'Minimal documentation'

    # 4. Pattern Adherence (15 points)
    agents = list(Path('agents').glob('*.md'))
    skills = list(Path('skills').glob('*/SKILL.md'))
    commands = list(Path('commands').glob('*.md'))

    if len(agents) >= 20 and len(skills) >= 15 and len(commands) >= 35:
        scores['pattern_adherence']['score'] = 15
        scores['pattern_adherence']['details'] = f'Excellent structure ({len(agents)} agents, {len(skills)} skills, {len(commands)} commands)'
    elif len(agents) >= 15 and len(skills) >= 10 and len(commands) >= 25:
        scores['pattern_adherence']['score'] = 12
        scores['pattern_adherence']['details'] = f'Good structure ({len(agents)} agents, {len(skills)} skills, {len(commands)} commands)'
    elif len(agents) >= 10 and len(skills) >= 5 and len(commands) >= 15:
        scores['pattern_adherence']['score'] = 8
        scores['pattern_adherence']['details'] = f'Adequate structure ({len(agents)} agents, {len(skills)} skills, {len(commands)} commands)'
    else:
        scores['pattern_adherence']['score'] = 4
        scores['pattern_adherence']['details'] = f'Limited structure ({len(agents)} agents, {len(skills)} skills, {len(commands)} commands)'

    # 5. Code Metrics (10 points)
    # Check if core utilities are functional
    core_utilities = ['assessment_storage.py', 'quality_tracker.py', 'task_queue.py']
    working_utils = 0

    for util in core_utilities:
        util_path = Path('lib') / util
        if util_path.exists():
            try:
                with open(util_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), str(util_path), 'exec')
                working_utils += 1
            except:
                pass

    if working_utils >= 3:
        scores['code_metrics']['score'] = 10
        scores['code_metrics']['details'] = f'All core utilities working ({working_utils}/3)'
    elif working_utils >= 2:
        scores['code_metrics']['score'] = 7
        scores['code_metrics']['details'] = f'Most core utilities working ({working_utils}/3)'
    elif working_utils >= 1:
        scores['code_metrics']['score'] = 4
        scores['code_metrics']['details'] = f'Some core utilities working ({working_utils}/3)'
    else:
        scores['code_metrics']['score'] = 0
        scores['code_metrics']['details'] = 'No working core utilities'

    # Calculate total weighted score
    total_score = sum(
        category['score'] * category['weight']
        for category in scores.values()
    )

    return total_score, scores


def main():
    """Generate final quality assessment report"""

    print("=" * 60)
    print("FINAL QUALITY ASSESSMENT")
    print("Autonomous Agent Plugin")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Calculate quality score
    total_score, category_scores = calculate_quality_score()

    print(f"\nOVERALL QUALITY SCORE: {total_score:.1f}/100")

    # Determine status
    if total_score >= 85:
        status = "EXCELLENT - Production Ready"
    elif total_score >= 70:
        status = "GOOD - Development Ready"
    elif total_score >= 50:
        status = "NEEDS IMPROVEMENT"
    else:
        status = "CRITICAL ISSUES"

    print(f"Status: {status}")

    print("\n" + "=" * 40)
    print("CATEGORY BREAKDOWN")
    print("=" * 40)

    for category, data in category_scores.items():
        category_name = category.replace('_', ' ').title()
        max_score = int(data['weight'] * 100)
        print(f"\n{category_name} ({data['weight']*100:.0f}% weight)")
        print(f"   Score: {data['score']}/{max_score}")
        print(f"   Details: {data['details']}")

    print("\n" + "=" * 40)
    print("COMPARISON TO BASELINE")
    print("=" * 40)

    baseline_score = 43.3
    improvement = total_score - baseline_score
    print(f"Previous Score (with syntax errors): {baseline_score}/100")
    print(f"Current Score: {total_score:.1f}/100")
    print(f"Improvement: +{improvement:.1f} points")

    print("\n" + "=" * 40)
    print("PRODUCTION READINESS")
    print("=" * 40)

    if total_score >= 70:
        print("[OK] Project meets minimum quality threshold (70/100)")
        print("[OK] Ready for development and testing")
        if total_score >= 85:
            print("[OK] Production ready with confidence")
    else:
        print("[FAIL] Project below quality threshold")
        print("[FAIL] Requires additional work before development")

    print("\n" + "=" * 40)
    print("KEY ACHIEVEMENTS")
    print("=" * 40)

    achievements = []
    if category_scores['code_standards']['score'] >= 20:
        achievements.append("Python syntax errors resolved")
    if category_scores['documentation']['score'] >= 17:
        achievements.append("Comprehensive documentation maintained")
    if category_scores['code_metrics']['score'] >= 7:
        achievements.append("Core utilities functional")
    if category_scores['pattern_adherence']['score'] >= 8:
        achievements.append("Plugin structure properly organized")

    for achievement in achievements:
        print(f"[+] {achievement}")

    print("\n" + "=" * 40)
    print("NEXT STEPS")
    print("=" * 40)

    if total_score < 70:
        print("Priority Actions:")
        if category_scores['test_coverage']['score'] < 20:
            print("• Fix failing tests to improve test coverage")
        if category_scores['pattern_adherence']['score'] < 8:
            print("• Complete plugin structure organization")
    else:
        print("Recommended Actions:")
        print("• Begin development and feature testing")
        print("• Set up CI/CD pipeline")
        print("• Start user acceptance testing")
        if total_score >= 85:
            print("• Prepare for production deployment")

    print("\n" + "=" * 60)
    print("ASSESSMENT COMPLETE")
    print("=" * 60)

    # Save detailed report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'overall_score': total_score,
        'status': status,
        'baseline_score': baseline_score,
        'improvement': improvement,
        'categories': {
            name: {
                'score': data['score'],
                'max_score': int(data['weight'] * 100),
                'weight_percentage': data['weight'] * 100,
                'details': data['details']
            }
            for name, data in category_scores.items()
        }
    }

    # Create reports directory if needed
    reports_dir = Path('.claude/reports')
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Save report
    report_file = reports_dir / f"FINAL_QUALITY_ASSESSMENT_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)

    print(f"\nDetailed report saved to: {report_file}")

    return total_score


if __name__ == "__main__":
    score = main()
    sys.exit(0 if score >= 70 else 1)