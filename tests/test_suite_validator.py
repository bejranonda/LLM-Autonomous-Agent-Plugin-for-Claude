"""
Test Suite Validator for Autonomous Agent Plugin v6.0.0

This module validates the structure and completeness of the test suite
for the 8 Phase 1 learning systems.
"""

import os
import ast
import json
from pathlib import Path


class TestSuiteValidator:
    """Validates the test suite structure and completeness"""

    def __init__(self, tests_dir="tests"):
        self.tests_dir = Path(tests_dir)
        self.expected_systems = [
            "agent_feedback_system",
            "agent_performance_tracker",
            "user_preference_learner",
            "adaptive_quality_thresholds",
            "predictive_skill_loader",
            "context_aware_skill_recommendations",
            "intelligent_agent_router",
            "learning_visualizer"
        ]

    def validate_test_structure(self):
        """Validate that all test files exist and have proper structure"""
        results = {
            "total_systems": len(self.expected_systems),
            "test_files_found": 0,
            "missing_files": [],
            "test_methods": {},
            "coverage_analysis": {}
        }

        for system in self.expected_systems:
            test_file = self.tests_dir / f"test_{system}.py"

            if test_file.exists():
                results["test_files_found"] += 1
                test_methods = self._extract_test_methods(test_file)
                results["test_methods"][system] = len(test_methods)
                results["coverage_analysis"][system] = self._analyze_test_coverage(test_file, test_methods)
            else:
                results["missing_files"].append(system)

        return results

    def _extract_test_methods(self, test_file):
        """Extract test methods from a test file"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)
            test_methods = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    test_methods.append(node.name)

            return test_methods
        except Exception as e:
            return [f"Error parsing file: {e}"]

    def _analyze_test_coverage(self, test_file, test_methods):
        """Analyze test coverage areas"""
        coverage_areas = {
            "initialization_tests": 0,
            "basic_functionality_tests": 0,
            "error_handling_tests": 0,
            "persistence_tests": 0,
            "performance_tests": 0,
            "integration_tests": 0
        }

        for method in test_methods:
            if isinstance(method, str):  # Valid method name
                if "initialization" in method.lower():
                    coverage_areas["initialization_tests"] += 1
                elif any(keyword in method.lower() for keyword in ["basic", "success", "valid"]):
                    coverage_areas["basic_functionality_tests"] += 1
                elif "error" in method.lower() or "invalid" in method.lower():
                    coverage_areas["error_handling_tests"] += 1
                elif "persistence" in method.lower() or "file" in method.lower():
                    coverage_areas["persistence_tests"] += 1
                elif "performance" in method.lower() or "speed" in method.lower():
                    coverage_areas["performance_tests"] += 1
                elif "integration" in method.lower() or "context" in method.lower():
                    coverage_areas["integration_tests"] += 1

        return coverage_areas

    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        validation_results = self.validate_test_structure()

        report = {
            "validation_summary": {
                "total_systems_expected": validation_results["total_systems"],
                "test_files_found": validation_results["test_files_found"],
                "completion_percentage": (validation_results["test_files_found"] / validation_results["total_systems"]) * 100
            },
            "detailed_results": validation_results,
            "quality_assessment": self._assess_test_quality(validation_results),
            "recommendations": self._generate_recommendations(validation_results)
        }

        return report

    def _assess_test_quality(self, results):
        """Assess overall test quality"""
        quality_score = 0
        max_score = results["total_systems"] * 6  # 6 quality criteria per system

        for system in self.expected_systems:
            if system in results["coverage_analysis"]:
                coverage = results["coverage_analysis"][system]

                # Score based on coverage areas
                if coverage["initialization_tests"] > 0:
                    quality_score += 1
                if coverage["basic_functionality_tests"] > 0:
                    quality_score += 1
                if coverage["error_handling_tests"] > 0:
                    quality_score += 1
                if coverage["persistence_tests"] > 0:
                    quality_score += 1
                if coverage["performance_tests"] > 0:
                    quality_score += 1
                if coverage["integration_tests"] > 0:
                    quality_score += 1

        quality_percentage = (quality_score / max_score) * 100 if max_score > 0 else 0

        return {
            "quality_score": quality_score,
            "max_possible_score": max_score,
            "quality_percentage": quality_percentage,
            "grade": self._get_quality_grade(quality_percentage)
        }

    def _get_quality_grade(self, percentage):
        """Get quality grade based on percentage"""
        if percentage >= 90:
            return "Excellent"
        elif percentage >= 80:
            return "Good"
        elif percentage >= 70:
            return "Satisfactory"
        elif percentage >= 60:
            return "Needs Improvement"
        else:
            return "Poor"

    def _generate_recommendations(self, results):
        """Generate improvement recommendations"""
        recommendations = []

        # Check for missing test files
        if results["missing_files"]:
            recommendations.append({
                "priority": "HIGH",
                "category": "Missing Tests",
                "description": f"Create test files for missing systems: {', '.join(results['missing_files'])}"
            })

        # Check for insufficient test methods
        for system, method_count in results["test_methods"].items():
            if method_count < 10:
                recommendations.append({
                    "priority": "MEDIUM",
                    "category": "Insufficient Coverage",
                    "description": f"Add more test methods for {system} (current: {method_count}, recommended: 15+)"
                })

        # Check for missing coverage areas
        for system, coverage in results["coverage_analysis"].items():
            missing_areas = [area for area, count in coverage.items() if count == 0]
            if missing_areas:
                recommendations.append({
                    "priority": "MEDIUM",
                    "category": "Coverage Gaps",
                    "description": f"Add {system} tests for: {', '.join(missing_areas)}"
                })

        if not recommendations:
            recommendations.append({
                "priority": "INFO",
                "category": "Excellent Coverage",
                "description": "Test suite has comprehensive coverage across all systems"
            })

        return recommendations


def main():
    """Main validation function"""
    validator = TestSuiteValidator()
    report = validator.generate_validation_report()

    print("AUTONOMOUS AGENT PLUGIN v6.0.0 - TEST SUITE VALIDATION")
    print("=" * 60)

    # Summary
    summary = report["validation_summary"]
    print(f"SUMMARY:")
    print(f"   Total Systems Expected: {summary['total_systems_expected']}")
    print(f"   Test Files Found: {summary['test_files_found']}")
    print(f"   Completion: {summary['completion_percentage']:.1f}%")

    # Quality Assessment
    quality = report["quality_assessment"]
    print(f"\nQUALITY ASSESSMENT:")
    print(f"   Quality Score: {quality['quality_score']}/{quality['max_possible_score']}")
    print(f"   Quality Percentage: {quality['quality_percentage']:.1f}%")
    print(f"   Grade: {quality['grade']}")

    # Detailed Results
    print(f"\nDETAILED RESULTS:")
    for system in validator.expected_systems:
        if system in report["detailed_results"]["test_methods"]:
            method_count = report["detailed_results"]["test_methods"][system]
            coverage = report["detailed_results"]["coverage_analysis"][system]
            print(f"   [OK] {system}: {method_count} test methods")

            # Show coverage areas
            areas = [f"{area}({count})" for area, count in coverage.items() if count > 0]
            if areas:
                print(f"      Coverage: {', '.join(areas)}")
        else:
            print(f"   [MISSING] {system}: Missing test file")

    # Recommendations
    print(f"\nRECOMMENDATIONS:")
    for i, rec in enumerate(report["recommendations"], 1):
        priority_marker = {"HIGH": "[HIGH]", "MEDIUM": "[MED]", "INFO": "[INFO]"}.get(rec["priority"], "[???]")
        print(f"   {i}. {priority_marker} {rec['description']}")

    # Final Assessment
    if summary["completion_percentage"] == 100:
        print(f"\nEXCELLENT: All {summary['total_systems_expected']} learning systems have comprehensive test suites!")
        if quality["quality_percentage"] >= 80:
            print(f"READY FOR PRODUCTION: High-quality test coverage achieved.")
        else:
            print(f"ALMOST READY: Consider addressing quality recommendations.")
    else:
        missing = summary['total_systems_expected'] - summary['test_files_found']
        print(f"\nWORK IN PROGRESS: {missing} test file(s) still needed.")

    return report


if __name__ == "__main__":
    main()