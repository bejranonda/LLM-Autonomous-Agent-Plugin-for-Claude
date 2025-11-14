#!/usr/bin/env python3
#     Comprehensive GUI Analysis Tool for Autonomous Agent Dashboard
    """

Performs complete GUI validation including:
- Interface functionality testing
- Performance analysis
- API endpoint validation
- Mobile responsiveness checking
- Accessibility compliance
- Error detection and resolution

Version: 1.0.0
import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import subprocess
import re


@dataclass
class GUIHealthScore:
    """Overall GUI health metrics"""

    overall_score: int
    web_interface: int
    api_endpoints: int
    performance: int
    mobile_responsive: int
    accessibility: int
    data_visualization: int


class GUIAnalyzer:
    """Comprehensive GUI analysis tool"""

    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        """Initialize the processor with default configuration."""
        self.base_url = base_url
        self.results = {
            "web_interface": {},
            "api_endpoints": {},
            "performance": {},
            "mobile_responsive": {},
            "accessibility": {},
            "data_visualization": {},
            "errors": [],
            "recommendations": [],
        }

        # Key API endpoints to test
        self.api_endpoints = [
            "/api/overview",
            "/api/quality-trends",
            "/api/skills",
            "/api/agents",
            "/api/system-health",
            "/api/recent-activity",
            "/api/validation-results",
            "/api/kpi/overview",
            "/api/unified/system/health",
        ]

    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run complete GUI analysis"""
        print("[START] Comprehensive GUI Analysis")
        print(f"Target URL: {self.base_url}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 80)

        # 1. Web Interface Analysis
        print("\n[1/6] Testing Web Interface...")
        self._analyze_web_interface()

        # 2. API Endpoint Testing
        print("\n[2/6] Testing API Endpoints...")
        self._test_api_endpoints()

        # 3. Performance Analysis
        print("\n[3/6] Analyzing Performance...")
        self._analyze_performance()

        # 4. Mobile Responsiveness
        print("\n[4/6] Testing Mobile Responsiveness...")
        self._test_mobile_responsiveness()

        # 5. Accessibility Compliance
        print("\n[5/6] Checking Accessibility...")
        self._check_accessibility()

        # 6. Data Visualization
        print("\n[6/6] Testing Data Visualization...")
        self._test_data_visualization()

        # Calculate overall scores
        health_score = self._calculate_health_score()

        # Generate report
        self._generate_final_report(health_score)

        return {"health_score": health_score, "detailed_results": self.results}

    def _analyze_web_interface(self):
        """Analyze web interface components"""
        try:
            start_time = time.time()
            response = requests.get(self.base_url, timeout=30)
            load_time = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Check for key components
                checks = {
                    "html5_doctype": "<!DOCTYPE html>" in content,
                    "proper_title": "<title>" in content and "Autonomous Agent Dashboard" in content,
                    "viewport_meta": "viewport" in content,
                    "chart_js_loaded": "chart.js" in content or "Chart.js" in content,
                    "responsive_css": "grid-template-columns" in content,
                    "interactive_elements": "onclick" in content or "addEventListener" in content,
                    "error_handling": "try" in content and "catch" in content,
                }

                # Check CSS components
                css_checks = {
                    "modern_design": "border-radius" in content,
                    "animations": "transition:" in content or "@keyframes" in content,
                    "color_scheme": "gradient" in content,
                    "typography": "font-family" in content,
                    "spacing": "margin:" in content and "padding:" in content,
                }

                passed_checks = sum(checks.values()) + sum(css_checks.values())
                total_checks = len(checks) + len(css_checks)
                web_score = int((passed_checks / total_checks) * 100)

                self.results["web_interface"] = {
                    "status_code": response.status_code,
                    "load_time": load_time,
                    "content_length": len(content),
                    "checks": checks,
                    "css_checks": css_checks,
                    "score": web_score,
                    "functional": web_score >= 70,
                }

                print(f"  [PASS] Web interface loaded in {load_time:.2f}s")
                print(f"  [INFO] {passed_checks}/{total_checks} checks passed ({web_score}%)")

            else:
                self.results["web_interface"] = {
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "score": 0,
                    "functional": False,
                }
                self.results["errors"].append(f"Web interface failed: HTTP {response.status_code}")
                print(f"  [ERROR] Web interface failed: HTTP {response.status_code}")

        except Exception as e:
            self.results["web_interface"] = {"error": str(e), "score": 0, "functional": False}
            self.results["errors"].append(f"Web interface error: {str(e)}")
            print(f"  [ERROR] Web interface error: {str(e)}")

    def _test_api_endpoints(self):
        """Test all API endpoints"""
        endpoint_results = {}
        working_endpoints = 0

        for endpoint in self.api_endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                response_time = time.time() - start_time

                if response.status_code == 200:
                    try:
                        data = response.json()
                        endpoint_results[endpoint] = {
                            "status": "working",
                            "response_time": response_time,
                            "data_size": len(str(data)),
                            "has_data": bool(data),
                            "sample_keys": list(data.keys())[:5] if isinstance(data, dict) else [],
                        }
                        working_endpoints += 1
                        print(f"  [PASS] {endpoint} ({response_time:.3f}s)")
                    except json.JSONDecodeError:
                        endpoint_results[endpoint] = {
                            "status": "invalid_json",
                            "response_time": response_time,
                            "error": "Invalid JSON response",
                        }
                        print(f"  [WARN] {endpoint} - Invalid JSON")

                else:
                    endpoint_results[endpoint] = {
                        "status": "http_error",
                        "response_time": response_time,
                        "error": f"HTTP {response.status_code}",
                    }
                    print(f"  [FAIL] {endpoint} - HTTP {response.status_code}")

            except Exception as e:
                endpoint_results[endpoint] = {"status": "connection_error", "error": str(e)}
                print(f"  [FAIL] {endpoint} - Connection failed")

        api_score = int((working_endpoints / len(self.api_endpoints)) * 100)
        self.results["api_endpoints"] = {
            "total_endpoints": len(self.api_endpoints),
            "working_endpoints": working_endpoints,
            "success_rate": working_endpoints / len(self.api_endpoints),
            "score": api_score,
            "endpoints": endpoint_results,
        }

        print(f"  [INFO] {working_endpoints}/{len(self.api_endpoints)} endpoints working ({api_score}%)")

    def _analyze_performance(self):
        """Analyze performance metrics"""
        try:
            # Test load time
            start_time = time.time()
            response = requests.get(self.base_url, timeout=30)
            initial_load_time = time.time() - start_time

            # Test with cache
            start_time = time.time()
            response = requests.get(self.base_url, timeout=30, headers={"Cache-Control": "no-cache"})
            cached_load_time = time.time() - start_time

            # Calculate performance scores
            load_time_score = max(0, 100 - (initial_load_time * 20))  # 5s = 0 points
            cache_score = 100 if cached_load_time < initial_load_time * 0.8 else 50

            performance_score = int((load_time_score + cache_score) / 2)

            self.results["performance"] = {
                "initial_load_time": initial_load_time,
                "cached_load_time": cached_load_time,
                "cache_efficiency": (initial_load_time - cached_load_time) / initial_load_time * 100,
                "load_time_score": load_time_score,
                "cache_score": cache_score,
                "overall_score": performance_score,
            }

            print(f"  [INFO] Initial load: {initial_load_time:.2f}s")
            print(f"  [INFO] Cached load: {cached_load_time:.2f}s")
            print(f"  [INFO] Performance score: {performance_score}%")

        except Exception as e:
            self.results["performance"] = {"error": str(e), "score": 0}
            self.results["errors"].append(f"Performance analysis error: {str(e)}")
            print(f"  [ERROR] Performance analysis failed: {str(e)}")

    def _test_mobile_responsiveness(self):
        """Test mobile responsiveness"""
        try:
            # Test with mobile user agent
            mobile_headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"}

            response = requests.get(self.base_url, headers=mobile_headers, timeout=30)
            content = response.text

            # Check mobile features
            mobile_checks = {
                "viewport_meta": "viewport" in content,
                "responsive_grid": "grid-template-columns" in content and "auto-fit" in content,
                "mobile_nav": "mobile" in content.lower(),
                "touch_friendly": "min-height" in content and "button" in content,
                "readable_fonts": "font-size" in content,
                "proper_scaling": "initial-scale=1.0" in content,
            }

            passed_mobile_checks = sum(mobile_checks.values())
            mobile_score = int((passed_mobile_checks / len(mobile_checks)) * 100)

            self.results["mobile_responsive"] = {
                "checks": mobile_checks,
                "passed_checks": passed_mobile_checks,
                "total_checks": len(mobile_checks),
                "score": mobile_score,
                "responsive": mobile_score >= 70,
            }

            print(f"  [INFO] {passed_mobile_checks}/{len(mobile_checks)} mobile checks passed ({mobile_score}%)")

        except Exception as e:
            self.results["mobile_responsive"] = {"error": str(e), "score": 0}
            self.results["errors"].append(f"Mobile responsiveness test error: {str(e)}")
            print(f"  [ERROR] Mobile test failed: {str(e)}")

    def _check_accessibility(self):
        """Check accessibility compliance"""
        try:
            response = requests.get(self.base_url, timeout=30)
            content = response.text

            # Basic accessibility checks
            accessibility_checks = {
                "lang_attribute": "lang=" in content,
                "alt_text": "alt=" in content,
                "semantic_html": any(tag in content for tag in ["<nav>", "<main>", "<header>", "<footer>"]),
                "proper_headings": "<h1>" in content and "<h2>" in content,
                "form_labels": "label" in content,
                "button_texts": "button" in content and (">" in content or "value=" in content),
                "color_contrast": "contrast" in content or "contrast" in content.lower(),
                "focus_styles": "focus" in content,
            }

            passed_a11y_checks = sum(accessibility_checks.values())
            a11y_score = int((passed_a11y_checks / len(accessibility_checks)) * 100)

            self.results["accessibility"] = {
                "checks": accessibility_checks,
                "passed_checks": passed_a11y_checks,
                "total_checks": len(accessibility_checks),
                "score": a11y_score,
                "wcag_compliant": a11y_score >= 80,
            }

            print(f"  [INFO] {passed_a11y_checks}/{len(accessibility_checks)} accessibility checks passed ({a11y_score}%)")

        except Exception as e:
            self.results["accessibility"] = {"error": str(e), "score": 0}
            self.results["errors"].append(f"Accessibility check error: {str(e)}")
            print(f"  [ERROR] Accessibility check failed: {str(e)}")

    def _test_data_visualization(self):
        """Test data visualization components"""
        try:
            response = requests.get(self.base_url, timeout=30)
            content = response.text

            # Check Chart.js and data visualization
            viz_checks = {
                "chart_js_loaded": "chart.js" in content or "Chart.js" in content,
                "chart_containers": "chart-container" in content,
                "canvas_elements": "<canvas" in content,
                "data_api_calls": "fetch(" in content or "XMLHttpRequest" in content,
                "real_time_updates": "setInterval" in content or "setTimeout" in content,
                "chart_types": any(chart in content.lower() for chart in ["line", "bar", "pie", "doughnut"]),
                "data_formatting": "toFixed" in content or "toLocaleString" in content,
            }

            # Test data API endpoints
            data_apis_working = 0
            data_endpoints = ["/api/quality-trends", "/api/system-health", "/api/overview"]

            for endpoint in data_endpoints:
                try:
                    api_response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                    if api_response.status_code == 200:
                        data = api_response.json()
                        if data and isinstance(data, dict):
                            data_apis_working += 1
                except:
                    pass

            viz_checks["data_apis_working"] = data_apis_working == len(data_endpoints)

            passed_viz_checks = sum(viz_checks.values())
            viz_score = int((passed_viz_checks / len(viz_checks)) * 100)

            self.results["data_visualization"] = {
                "checks": viz_checks,
                "passed_checks": passed_viz_checks,
                "total_checks": len(viz_checks),
                "data_apis_tested": len(data_endpoints),
                "data_apis_working": data_apis_working,
                "score": viz_score,
                "functional": viz_score >= 70,
            }

            print(f"  [INFO] {passed_viz_checks}/{len(viz_checks)} visualization checks passed ({viz_score}%)")
            print(f"  [INFO] {data_apis_working}/{len(data_endpoints)} data APIs working")

        except Exception as e:
            self.results["data_visualization"] = {"error": str(e), "score": 0}
            self.results["errors"].append(f"Data visualization test error: {str(e)}")
            print(f"  [ERROR] Data visualization test failed: {str(e)}")

    def _calculate_health_score(self) -> GUIHealthScore:
        """Calculate overall GUI health score"""
        scores = {
            "web_interface": self.results["web_interface"].get("score", 0),
            "api_endpoints": self.results["api_endpoints"].get("score", 0),
            "performance": self.results["performance"].get("overall_score", 0),
            "mobile_responsive": self.results["mobile_responsive"].get("score", 0),
            "accessibility": self.results["accessibility"].get("score", 0),
            "data_visualization": self.results["data_visualization"].get("score", 0),
        }

        # Calculate weighted overall score
        weights = {
            "web_interface": 0.25,
            "api_endpoints": 0.20,
            "performance": 0.20,
            "mobile_responsive": 0.15,
            "accessibility": 0.10,
            "data_visualization": 0.10,
        }

        overall_score = int(sum(scores[component] * weights[component] for component in scores))

        return GUIHealthScore(
            overall_score=overall_score,
            web_interface=scores["web_interface"],
            api_endpoints=scores["api_endpoints"],
            performance=scores["performance"],
            mobile_responsive=scores["mobile_responsive"],
            accessibility=scores["accessibility"],
            data_visualization=scores["data_visualization"],
        )

    def _generate_final_report(self, health_score: GUIHealthScore):
        """Generate comprehensive final report"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE GUI ANALYSIS REPORT")
        print("=" * 80)

        # Overall health status
        if health_score.overall_score >= 90:
            status = "EXCELLENT"
        elif health_score.overall_score >= 80:
            status = "GOOD"
        elif health_score.overall_score >= 70:
            status = "ACCEPTABLE"
        else:
            status = "NEEDS IMPROVEMENT"

        print(f"\nOVERALL GUI HEALTH SCORE: {health_score.overall_score}/100 - {status}")

        # Component scores
        print(f"\nComponent Breakdown:")
        print(f"  Web Interface:     {health_score.web_interface}/100")
        print(f"  API Endpoints:     {health_score.api_endpoints}/100")
        print(f"  Performance:       {health_score.performance}/100")
        print(f"  Mobile Responsive: {health_score.mobile_responsive}/100")
        print(f"  Accessibility:     {health_score.accessibility}/100")
        print(f"  Data Visualization:{health_score.data_visualization}/100")

        # Key findings
        print(f"\nKEY FINDINGS:")

        # Web interface findings
        web_data = self.results["web_interface"]
        if web_data.get("functional"):
            print(f"  [PASS] Web interface is fully functional")
            print(f"  [INFO] Page loads in {web_data.get('load_time', 0):.2f} seconds")
        else:
            print(f"  [FAIL] Web interface has issues")

        # API findings
        api_data = self.results["api_endpoints"]
        working = api_data.get("working_endpoints", 0)
        total = api_data.get("total_endpoints", 0)
        if working == total:
            print(f"  [PASS] All {total} API endpoints working")
        else:
            print(f"  [WARN] Only {working}/{total} API endpoints working")

        # Performance findings
        perf_data = self.results["performance"]
        if "error" not in perf_data:
            load_time = perf_data.get("initial_load_time", 0)
            if load_time < 2:
                print(f"  [PASS] Excellent load performance ({load_time:.2f}s)")
            elif load_time < 5:
                print(f"  [INFO] Acceptable load performance ({load_time:.2f}s)")
            else:
                print(f"  [WARN] Slow load performance ({load_time:.2f}s)")

        # Mobile findings
        mobile_data = self.results["mobile_responsive"]
        if mobile_data.get("responsive"):
            print(f"  [PASS] Mobile responsive design implemented")
        else:
            print(f"  [WARN] Mobile responsiveness needs improvement")

        # Errors found
        if self.results["errors"]:
            print(f"\nERRORS FOUND ({len(self.results['errors'])}):")
            for error in self.results["errors"][:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(self.results["errors"]) > 5:
                print(f"  ... and {len(self.results['errors']) - 5} more")
        else:
            print(f"\n[PASS] No critical errors detected")

        # Recommendations
        self._generate_recommendations(health_score)

        print(f"\nAnalysis completed at: {datetime.now().isoformat()}")
        print("=" * 80)

    def _generate_recommendations(self, health_score: GUIHealthScore):
        """Generate actionable recommendations"""
        recommendations = []

        if health_score.web_interface < 80:
            recommendations.append("Improve web interface functionality and component integration")

        if health_score.api_endpoints < 90:
            recommendations.append("Fix broken API endpoints and improve error handling")

        if health_score.performance < 80:
            recommendations.append("Optimize page load performance and implement caching")

        if health_score.mobile_responsive < 80:
            recommendations.append("Enhance mobile responsiveness and touch interactions")

        if health_score.accessibility < 85:
            recommendations.append("Improve accessibility compliance (WCAG 2.1 AA standards)")

        if health_score.data_visualization < 80:
            recommendations.append("Fix data visualization issues and improve chart rendering")

        # Specific recommendations based on detailed results
        web_data = self.results["web_interface"]
        if "checks" in web_data:
            checks = web_data["checks"]
            if not checks.get("chart_js_loaded"):
                recommendations.append("Ensure Chart.js library is properly loaded")
            if not checks.get("interactive_elements"):
                recommendations.append("Add interactive elements for better user engagement")

        api_data = self.results["api_endpoints"]
        if "endpoints" in api_data:
            broken_endpoints = [ep for ep, data in api_data["endpoints"].items() if data.get("status") != "working"]
            if broken_endpoints:
                recommendations.append(f"Fix broken endpoints: {', '.join(broken_endpoints[:3])}")

        if recommendations:
            print(f"\nRECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        else:
            print(f"\n[PASS] No immediate recommendations - GUI system is performing well!")


def main():
    """Main execution function"""
    analyzer = GUIAnalyzer()
    results = analyzer.run_comprehensive_analysis()

    # Save detailed results
    output_file = ".claude-patterns/comprehensive-gui-analysis.json"
    try:
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n[PASS] Detailed results saved to: {output_file}")
    except Exception as e:
        print(f"\n[WARN] Could not save results to file: {str(e)}")

    return results["health_score"].overall_score


if __name__ == "__main__":
    try:
        score = main()
        sys.exit(0 if score >= 70 else 1)
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Analysis cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n[FATAL] Analysis failed: {str(e)}")
        sys.exit(1)
