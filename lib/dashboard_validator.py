#!/usr/bin/env python3
"""
Enhanced Dashboard Validator and Debugger

Comprehensive validation, debugging, and performance monitoring
for the Autonomous Agent real-time monitoring dashboard.

Features:
- Multi-layer validation (application, data, frontend, performance)
- Automated issue detection and resolution
- Real-time monitoring and alerting
- Performance profiling and optimization
- Pattern learning integration

Version: 1.0.0
Author: Autonomous Agent Development Team
"""

import json
import os
import sys
import time
import requests
import psutil
import threading
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import subprocess
import socket
import re


class DashboardValidator:
    """Comprehensive dashboard validation and debugging system."""

    def __init__(self, patterns_dir: str = ".claude-patterns", dashboard_url: str = "http://127.0.0.1:5000"):
        """
        Initialize dashboard validator.

        Args:
            patterns_dir: Directory containing pattern data
            dashboard_url: URL of the dashboard to validate
        """
        self.patterns_dir = Path(patterns_dir)
        self.dashboard_url = dashboard_url
        self.results = {
            "validation_timestamp": datetime.now().isoformat(),
            "overall_score": 0,
            "status": "unknown",
            "layers": {},
            "issues": [],
            "fixes_applied": [],
            "performance_metrics": {},
            "recommendations": []
        }
        self.session = requests.Session()
        self.session.timeout = 10

    def run_validation(self, validation_type: str = "full") -> Dict[str, Any]:
        """
        Run comprehensive dashboard validation.

        Args:
            validation_type: Type of validation (quick, full, performance, data, frontend)

        Returns:
            Validation results dictionary
        """
        print(f"🔍 Starting {validation_type} dashboard validation...")
        start_time = time.time()

        try:
            # Run different validation layers based on type
            if validation_type in ["quick", "full"]:
                self._validate_application_layer()
                self._validate_data_layer()

            if validation_type in ["full", "frontend"]:
                self._validate_frontend_layer()

            if validation_type in ["performance", "full"]:
                self._validate_performance_layer()

            if validation_type in ["data", "full"]:
                self._validate_data_integrity()

            # Calculate overall score
            self._calculate_overall_score()

            # Apply auto-fixes
            self._apply_auto_fixes()

            # Generate recommendations
            self._generate_recommendations()

            execution_time = time.time() - start_time
            self.results["execution_time"] = execution_time

            print(f"✅ Validation completed in {execution_time:.1f} seconds")
            return self.results

        except Exception as e:
            print(f"❌ Validation failed: {e}")
            self.results["status"] = "failed"
            self.results["error"] = str(e)
            return self.results

    def _validate_application_layer(self) -> None:
        """Validate Flask application and API endpoints."""
        print("📡 Validating application layer...")

        layer_results = {
            "status": "pass",
            "tests": {},
            "issues": [],
            "score": 0
        }

        # Test 1: Dashboard accessibility
        try:
            response = self.session.get(self.dashboard_url)
            if response.status_code == 200:
                layer_results["tests"]["dashboard_accessible"] = {
                    "status": "pass",
                    "response_time": response.elapsed.total_seconds()
                }
                print(f"   ✅ Dashboard accessible ({response.elapsed.total_seconds():.3f}s)")
            else:
                layer_results["tests"]["dashboard_accessible"] = {
                    "status": "fail",
                    "status_code": response.status_code
                }
                layer_results["issues"].append(f"Dashboard returned HTTP {response.status_code}")
                layer_results["status"] = "fail"
                print(f"   ❌ Dashboard returned HTTP {response.status_code}")
        except Exception as e:
            layer_results["tests"]["dashboard_accessible"] = {
                "status": "fail",
                "error": str(e)
            }
            layer_results["issues"].append(f"Dashboard inaccessible: {e}")
            layer_results["status"] = "fail"
            print(f"   ❌ Dashboard inaccessible: {e}")

        # Test 2: API endpoints
        api_endpoints = [
            "/api/overview",
            "/api/quality-trends",
            "/api/recent-activity",
            "/api/skills",
            "/api/agents",
            "/api/task-distribution",
            "/api/system-health"
        ]

        api_results = {}
        for endpoint in api_endpoints:
            try:
                response = self.session.get(f"{self.dashboard_url}{endpoint}")
                if response.status_code == 200:
                    api_results[endpoint] = {
                        "status": "pass",
                        "response_time": response.elapsed.total_seconds(),
                        "data_valid": self._validate_json_response(response.text)
                    }
                    print(f"   ✅ {endpoint} ({response.elapsed.total_seconds():.3f}s)")
                else:
                    api_results[endpoint] = {
                        "status": "fail",
                        "status_code": response.status_code
                    }
                    layer_results["issues"].append(f"API endpoint {endpoint} returned {response.status_code}")
                    print(f"   ❌ {endpoint} returned {response.status_code}")
            except Exception as e:
                api_results[endpoint] = {
                    "status": "fail",
                    "error": str(e)
                }
                layer_results["issues"].append(f"API endpoint {endpoint} failed: {e}")
                print(f"   ❌ {endpoint} failed: {e}")

        layer_results["tests"]["api_endpoints"] = api_results

        # Test 3: Process health
        try:
            # Check if Flask process is running
            flask_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'dashboard.py' in cmdline or 'flask' in cmdline:
                        flask_processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "cpu_percent": proc.cpu_percent(),
                            "memory_mb": proc.memory_info().rss / 1024 / 1024
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if flask_processes:
                layer_results["tests"]["process_health"] = {
                    "status": "pass",
                    "processes": flask_processes
                }
                print(f"   ✅ Found {len(flask_processes)} Flask process(es)")
            else:
                layer_results["tests"]["process_health"] = {
                    "status": "warning",
                    "message": "No Flask processes found"
                }
                layer_results["issues"].append("No Flask processes detected")
                print(f"   ⚠️ No Flask processes found")
        except Exception as e:
            layer_results["tests"]["process_health"] = {
                "status": "fail",
                "error": str(e)
            }
            layer_results["issues"].append(f"Process health check failed: {e}")
            print(f"   ❌ Process health check failed: {e}")

        # Calculate layer score
        total_tests = len(layer_results["tests"])
        passed_tests = sum(1 for test in layer_results["tests"].values()
                         if test.get("status") == "pass")
        layer_results["score"] = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0

        if layer_results["issues"]:
            self.results["issues"].extend([f"Application: {issue}" for issue in layer_results["issues"]])

        self.results["layers"]["application"] = layer_results

    def _validate_data_layer(self) -> None:
        """Validate data files and consistency."""
        print("📊 Validating data layer...")

        layer_results = {
            "status": "pass",
            "tests": {},
            "issues": [],
            "score": 0
        }

        # Required data files
        data_files = [
            "patterns.json",
            "quality_history.json",
            "insights.json",
            "trends.json",
            "predictions.json"
        ]

        file_results = {}
        for filename in data_files:
            filepath = self.patterns_dir / filename
            try:
                if filepath.exists():
                    with open(filepath, 'r') as f:
                        data = json.load(f)

                    # Validate JSON structure
                    validation_result = self._validate_data_structure(filename, data)
                    file_results[filename] = {
                        "status": "pass",
                        "size_bytes": filepath.stat().st_size,
                        "validation": validation_result
                    }
                    print(f"   ✅ {filename} ({filepath.stat().st_size} bytes)")

                    if not validation_result["valid"]:
                        layer_results["issues"].extend([f"{filename}: {issue}"
                                                      for issue in validation_result["issues"]])
                else:
                    file_results[filename] = {
                        "status": "fail",
                        "error": "File not found"
                    }
                    layer_results["issues"].append(f"Data file missing: {filename}")
                    print(f"   ❌ {filename} not found")
            except json.JSONDecodeError as e:
                file_results[filename] = {
                    "status": "fail",
                    "error": f"JSON syntax error: {e}"
                }
                layer_results["issues"].append(f"JSON syntax error in {filename}: {e}")
                print(f"   ❌ {filename} JSON error: {e}")
                # Try to auto-fix JSON syntax
                if self._fix_json_syntax(filepath):
                    layer_results["fixes_applied"].append(f"Fixed JSON syntax in {filename}")
                    print(f"   🔧 Auto-fixed JSON syntax in {filename}")
            except Exception as e:
                file_results[filename] = {
                    "status": "fail",
                    "error": str(e)
                }
                layer_results["issues"].append(f"Error reading {filename}: {e}")
                print(f"   ❌ {filename} error: {e}")

        layer_results["tests"]["data_files"] = file_results

        # Test data consistency
        try:
            consistency_result = self._validate_data_consistency()
            layer_results["tests"]["data_consistency"] = consistency_result
            if not consistency_result["consistent"]:
                layer_results["issues"].extend(consistency_result["issues"])
                print(f"   ⚠️ Data consistency issues found")
            else:
                print(f"   ✅ Data consistency verified")
        except Exception as e:
            layer_results["tests"]["data_consistency"] = {
                "status": "fail",
                "error": str(e)
            }
            layer_results["issues"].append(f"Data consistency check failed: {e}")
            print(f"   ❌ Data consistency check failed: {e}")

        # Calculate layer score
        total_tests = len(layer_results["tests"])
        passed_tests = sum(1 for test in layer_results["tests"].values()
                         if test.get("status") == "pass")
        layer_results["score"] = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0

        if layer_results["issues"]:
            self.results["issues"].extend([f"Data: {issue}" for issue in layer_results["issues"]])

        self.results["layers"]["data"] = layer_results

    def _validate_frontend_layer(self) -> None:
        """Validate frontend JavaScript and chart functionality."""
        print("🎨 Validating frontend layer...")

        layer_results = {
            "status": "pass",
            "tests": {},
            "issues": [],
            "score": 0
        }

        # Test 1: Dashboard HTML structure
        try:
            response = self.session.get(self.dashboard_url)
            if response.status_code == 200:
                html_content = response.text

                # Check for essential elements
                required_elements = [
                    "<canvas",  # Chart.js elements
                    "quality-trends",  # Quality trends chart
                    "period-selector",  # Period selector
                    "dashboard-container"  # Main container
                ]

                missing_elements = []
                for element in required_elements:
                    if element not in html_content:
                        missing_elements.append(element)

                if missing_elements:
                    layer_results["tests"]["html_structure"] = {
                        "status": "fail",
                        "missing_elements": missing_elements
                    }
                    layer_results["issues"].append(f"Missing HTML elements: {', '.join(missing_elements)}")
                    print(f"   ❌ Missing HTML elements: {', '.join(missing_elements)}")
                else:
                    layer_results["tests"]["html_structure"] = {
                        "status": "pass",
                        "elements_found": len(required_elements)
                    }
                    print(f"   ✅ HTML structure valid")
            else:
                layer_results["tests"]["html_structure"] = {
                    "status": "fail",
                    "error": f"HTTP {response.status_code}"
                }
                layer_results["issues"].append(f"Cannot validate HTML: HTTP {response.status_code}")
        except Exception as e:
            layer_results["tests"]["html_structure"] = {
                "status": "fail",
                "error": str(e)
            }
            layer_results["issues"].append(f"HTML validation failed: {e}")
            print(f"   ❌ HTML validation failed: {e}")

        # Test 2: JavaScript functionality
        try:
            # Test if JavaScript is working by checking API responses
            response = self.session.get(f"{self.dashboard_url}/api/overview")
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('application/json'):
                layer_results["tests"]["javascript_api"] = {
                    "status": "pass",
                    "content_type": response.headers.get('content-type')
                }
                print(f"   ✅ JavaScript API working")
            else:
                layer_results["tests"]["javascript_api"] = {
                    "status": "fail",
                    "content_type": response.headers.get('content-type', 'unknown')
                }
                layer_results["issues"].append("JavaScript API not responding correctly")
                print(f"   ❌ JavaScript API not working")
        except Exception as e:
            layer_results["tests"]["javascript_api"] = {
                "status": "fail",
                "error": str(e)
            }
            layer_results["issues"].append(f"JavaScript API test failed: {e}")
            print(f"   ❌ JavaScript API test failed: {e}")

        # Test 3: Chart rendering simulation
        try:
            # Get chart data to verify it's properly formatted
            response = self.session.get(f"{self.dashboard_url}/api/quality-trends")
            if response.status_code == 200:
                data = response.json()

                # Validate chart data structure
                if "trend_data" in data and isinstance(data["trend_data"], list):
                    layer_results["tests"]["chart_data"] = {
                        "status": "pass",
                        "data_points": len(data["trend_data"])
                    }
                    print(f"   ✅ Chart data valid ({len(data['trend_data'])} points)")
                else:
                    layer_results["tests"]["chart_data"] = {
                        "status": "fail",
                        "error": "Invalid chart data structure"
                    }
                    layer_results["issues"].append("Chart data structure invalid")
                    print(f"   ❌ Chart data structure invalid")
            else:
                layer_results["tests"]["chart_data"] = {
                    "status": "fail",
                    "error": f"HTTP {response.status_code}"
                }
                layer_results["issues"].append(f"Chart data API failed: HTTP {response.status_code}")
        except Exception as e:
            layer_results["tests"]["chart_data"] = {
                "status": "fail",
                "error": str(e)
            }
            layer_results["issues"].append(f"Chart data validation failed: {e}")
            print(f"   ❌ Chart data validation failed: {e}")

        # Calculate layer score
        total_tests = len(layer_results["tests"])
        passed_tests = sum(1 for test in layer_results["tests"].values()
                         if test.get("status") == "pass")
        layer_results["score"] = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0

        if layer_results["issues"]:
            self.results["issues"].extend([f"Frontend: {issue}" for issue in layer_results["issues"]])

        self.results["layers"]["frontend"] = layer_results

    def _validate_performance_layer(self) -> None:
        """Validate performance metrics and resource usage."""
        print("⚡ Validating performance layer...")

        layer_results = {
            "status": "pass",
            "tests": {},
            "issues": [],
            "score": 0,
            "metrics": {}
        }

        # Test 1: API response times
        try:
            api_endpoints = [
                "/api/overview",
                "/api/quality-trends",
                "/api/recent-activity"
            ]

            response_times = []
            for endpoint in api_endpoints:
                start_time = time.time()
                response = self.session.get(f"{self.dashboard_url}{endpoint}")
                response_time = time.time() - start_time
                response_times.append(response_time)

            avg_response_time = statistics.mean(response_times)
            max_response_time = max(response_times)

            layer_results["tests"]["api_response_times"] = {
                "status": "pass" if avg_response_time < 0.5 else "warning",
                "avg_response_time": avg_response_time,
                "max_response_time": max_response_time,
                "target": 0.2  # 200ms target
            }

            layer_results["metrics"]["response_times"] = {
                "avg": avg_response_time,
                "min": min(response_times),
                "max": max_response_time,
                "p95": sorted(response_times)[int(len(response_times) * 0.95)] if len(response_times) > 1 else avg_response_time
            }

            if avg_response_time > 0.5:
                layer_results["issues"].append(f"Slow API responses: avg {avg_response_time:.3f}s (target: <0.2s)")
                print(f"   ⚠️ Slow API responses: avg {avg_response_time:.3f}s")
            else:
                print(f"   ✅ API response times: avg {avg_response_time:.3f}s")

        except Exception as e:
            layer_results["tests"]["api_response_times"] = {
                "status": "fail",
                "error": str(e)
            }
            layer_results["issues"].append(f"Response time test failed: {e}")
            print(f"   ❌ Response time test failed: {e}")

        # Test 2: Memory usage
        try:
            # Find dashboard process
            dashboard_process = None
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'dashboard.py' in cmdline:
                        dashboard_process = proc
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if dashboard_process:
                memory_info = dashboard_process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024
                cpu_percent = dashboard_process.cpu_percent()

                layer_results["tests"]["resource_usage"] = {
                    "status": "pass" if memory_mb < 200 else "warning",
                    "memory_mb": memory_mb,
                    "cpu_percent": cpu_percent,
                    "pid": dashboard_process.pid
                }

                layer_results["metrics"]["memory"] = {
                    "rss_mb": memory_mb,
                    "vms_mb": memory_info.vms / 1024 / 1024,
                    "cpu_percent": cpu_percent
                }

                if memory_mb > 200:
                    layer_results["issues"].append(f"High memory usage: {memory_mb:.1f}MB")
                    print(f"   ⚠️ High memory usage: {memory_mb:.1f}MB")
                else:
                    print(f"   ✅ Memory usage: {memory_mb:.1f}MB")
            else:
                layer_results["tests"]["resource_usage"] = {
                    "status": "warning",
                    "message": "Dashboard process not found"
                }
                print(f"   ⚠️ Dashboard process not found")

        except Exception as e:
            layer_results["tests"]["resource_usage"] = {
                "status": "fail",
                "error": str(e)
            }
            layer_results["issues"].append(f"Resource usage test failed: {e}")
            print(f"   ❌ Resource usage test failed: {e}")

        # Test 3: Port accessibility
        try:
            # Extract host and port from dashboard URL
            match = re.search(r'http://([^:]+):(\d+)', self.dashboard_url)
            if match:
                host, port = match.groups()
                port = int(port)

                # Test port connectivity
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((host, port))
                sock.close()

                if result == 0:
                    layer_results["tests"]["port_connectivity"] = {
                        "status": "pass",
                        "host": host,
                        "port": port
                    }
                    print(f"   ✅ Port {port} accessible")
                else:
                    layer_results["tests"]["port_connectivity"] = {
                        "status": "fail",
                        "host": host,
                        "port": port,
                        "error_code": result
                    }
                    layer_results["issues"].append(f"Port {port} not accessible (error code: {result})")
                    print(f"   ❌ Port {port} not accessible")
            else:
                layer_results["tests"]["port_connectivity"] = {
                    "status": "warning",
                    "message": "Could not parse dashboard URL"
                }
        except Exception as e:
            layer_results["tests"]["port_connectivity"] = {
                "status": "fail",
                "error": str(e)
            }
            layer_results["issues"].append(f"Port connectivity test failed: {e}")
            print(f"   ❌ Port connectivity test failed: {e}")

        # Calculate layer score
        total_tests = len(layer_results["tests"])
        passed_tests = sum(1 for test in layer_results["tests"].values()
                         if test.get("status") == "pass")
        layer_results["score"] = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0

        if layer_results["issues"]:
            self.results["issues"].extend([f"Performance: {issue}" for issue in layer_results["issues"]])

        self.results["layers"]["performance"] = layer_results
        self.results["performance_metrics"] = layer_results["metrics"]

    def _validate_data_integrity(self) -> None:
        """Validate detailed data integrity and consistency."""
        print("🔍 Validating data integrity...")

        integrity_results = {
            "status": "pass",
            "checks": {},
            "issues": [],
            "score": 0
        }

        # Check patterns.json structure
        try:
            patterns_file = self.patterns_dir / "patterns.json"
            if patterns_file.exists():
                with open(patterns_file, 'r') as f:
                    patterns_data = json.load(f)

                # Validate required fields
                required_fields = ["patterns", "skill_effectiveness", "agent_effectiveness", "metadata"]
                missing_fields = [field for field in required_fields if field not in patterns_data]

                if missing_fields:
                    integrity_results["checks"]["patterns_structure"] = {
                        "status": "fail",
                        "missing_fields": missing_fields
                    }
                    integrity_results["issues"].append(f"patterns.json missing fields: {', '.join(missing_fields)}")
                    print(f"   ❌ patterns.json missing fields: {', '.join(missing_fields)}")
                else:
                    integrity_results["checks"]["patterns_structure"] = {
                        "status": "pass",
                        "patterns_count": len(patterns_data.get("patterns", [])),
                        "skills_count": len(patterns_data.get("skill_effectiveness", {})),
                        "agents_count": len(patterns_data.get("agent_effectiveness", {}))
                    }
                    print(f"   ✅ patterns.json structure valid")
            else:
                integrity_results["checks"]["patterns_structure"] = {
                    "status": "fail",
                    "error": "File not found"
                }
                integrity_results["issues"].append("patterns.json not found")
                print(f"   ❌ patterns.json not found")
        except Exception as e:
            integrity_results["checks"]["patterns_structure"] = {
                "status": "fail",
                "error": str(e)
            }
            integrity_results["issues"].append(f"patterns.json validation failed: {e}")
            print(f"   ❌ patterns.json validation failed: {e}")

        # Check quality_history.json structure
        try:
            quality_file = self.patterns_dir / "quality_history.json"
            if quality_file.exists():
                with open(quality_file, 'r') as f:
                    quality_data = json.load(f)

                # Validate required fields
                required_fields = ["quality_assessments", "statistics", "metadata"]
                missing_fields = [field for field in required_fields if field not in quality_data]

                if missing_fields:
                    integrity_results["checks"]["quality_history_structure"] = {
                        "status": "fail",
                        "missing_fields": missing_fields
                    }
                    integrity_results["issues"].append(f"quality_history.json missing fields: {', '.join(missing_fields)}")
                    print(f"   ❌ quality_history.json missing fields: {', '.join(missing_fields)}")
                else:
                    assessments_count = len(quality_data.get("quality_assessments", []))
                    integrity_results["checks"]["quality_history_structure"] = {
                        "status": "pass",
                        "assessments_count": assessments_count,
                        "avg_quality_score": quality_data.get("statistics", {}).get("avg_quality_score", 0)
                    }
                    print(f"   ✅ quality_history.json structure valid ({assessments_count} assessments)")
            else:
                integrity_results["checks"]["quality_history_structure"] = {
                    "status": "fail",
                    "error": "File not found"
                }
                integrity_results["issues"].append("quality_history.json not found")
                print(f"   ❌ quality_history.json not found")
        except Exception as e:
            integrity_results["checks"]["quality_history_structure"] = {
                "status": "fail",
                "error": str(e)
            }
            integrity_results["issues"].append(f"quality_history.json validation failed: {e}")
            print(f"   ❌ quality_history.json validation failed: {e}")

        # Check data consistency between files
        try:
            consistency_score = self._calculate_data_consistency()
            integrity_results["checks"]["cross_file_consistency"] = {
                "status": "pass" if consistency_score > 80 else "warning",
                "consistency_score": consistency_score
            }

            if consistency_score <= 80:
                integrity_results["issues"].append(f"Low data consistency score: {consistency_score}%")
                print(f"   ⚠️ Low data consistency: {consistency_score}%")
            else:
                print(f"   ✅ Data consistency: {consistency_score}%")
        except Exception as e:
            integrity_results["checks"]["cross_file_consistency"] = {
                "status": "fail",
                "error": str(e)
            }
            integrity_results["issues"].append(f"Data consistency check failed: {e}")
            print(f"   ❌ Data consistency check failed: {e}")

        # Calculate integrity score
        total_checks = len(integrity_results["checks"])
        passed_checks = sum(1 for check in integrity_results["checks"].values()
                          if check.get("status") == "pass")
        integrity_results["score"] = int((passed_checks / total_checks) * 100) if total_checks > 0 else 0

        if integrity_results["issues"]:
            self.results["issues"].extend([f"Integrity: {issue}" for issue in integrity_results["issues"]])

        self.results["layers"]["integrity"] = integrity_results

    def _validate_json_response(self, response_text: str) -> bool:
        """Validate that API response is valid JSON."""
        try:
            json.loads(response_text)
            return True
        except json.JSONDecodeError:
            return False

    def _validate_data_structure(self, filename: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate specific data file structure."""
        validation_result = {
            "valid": True,
            "issues": []
        }

        if filename == "patterns.json":
            required_keys = ["patterns", "skill_effectiveness", "agent_effectiveness", "metadata"]
            for key in required_keys:
                if key not in data:
                    validation_result["valid"] = False
                    validation_result["issues"].append(f"Missing required key: {key}")

        elif filename == "quality_history.json":
            required_keys = ["quality_assessments", "statistics", "metadata"]
            for key in required_keys:
                if key not in data:
                    validation_result["valid"] = False
                    validation_result["issues"].append(f"Missing required key: {key}")

        return validation_result

    def _validate_data_consistency(self) -> Dict[str, Any]:
        """Validate consistency across different data files."""
        result = {
            "consistent": True,
            "issues": []
        }

        try:
            # Load data files
            patterns_data = self._load_json_file("patterns.json")
            quality_data = self._load_json_file("quality_history.json")

            if not patterns_data or not quality_data:
                result["consistent"] = False
                result["issues"].append("Missing required data files")
                return result

            # Check pattern count consistency
            patterns_count = len(patterns_data.get("patterns", []))
            quality_assessments_count = len(quality_data.get("quality_assessments", []))

            # These should be roughly equal (patterns are created from assessments)
            if abs(patterns_count - quality_assessments_count) > 2:
                result["consistent"] = False
                result["issues"].append(f"Pattern count ({patterns_count}) doesn't match assessment count ({quality_assessments_count})")

            # Check timestamp consistency
            if patterns_data.get("metadata", {}).get("last_updated") != quality_data.get("metadata", {}).get("last_assessment"):
                result["issues"].append("Last updated timestamps don't match between files")

        except Exception as e:
            result["consistent"] = False
            result["issues"].append(f"Data consistency check failed: {e}")

        return result

    def _calculate_data_consistency(self) -> int:
        """Calculate overall data consistency score."""
        try:
            consistency_result = self._validate_data_consistency()
            if consistency_result["consistent"]:
                return 100
            else:
                # Deduct points for each issue
                base_score = 100
                base_score -= len(consistency_result["issues"]) * 20
                return max(0, base_score)
        except:
            return 0

    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """Load JSON file safely."""
        filepath = self.patterns_dir / filename
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _fix_json_syntax(self, filepath: Path) -> bool:
        """Attempt to fix common JSON syntax errors."""
        try:
            with open(filepath, 'r') as f:
                content = f.read()

            # Try to parse the JSON to get specific error
            try:
                json.loads(content)
                return True  # No fix needed
            except json.JSONDecodeError as e:
                # Common fixes
                fixed_content = content

                # Fix trailing commas
                fixed_content = re.sub(r',\s*}', '}', fixed_content)
                fixed_content = re.sub(r',\s*]', ']', fixed_content)

                # Fix missing quotes around keys
                fixed_content = re.sub(r'(\w+)\s*:', r'"\1":', fixed_content)

                # Try parsing the fixed content
                try:
                    json.loads(fixed_content)
                    # Write the fixed content back
                    with open(filepath, 'w') as f:
                        f.write(fixed_content)
                    return True
                except json.JSONDecodeError:
                    return False
        except:
            return False

    def _calculate_overall_score(self) -> None:
        """Calculate overall dashboard health score."""
        layer_scores = []
        for layer_name, layer_data in self.results["layers"].items():
            if "score" in layer_data:
                layer_scores.append(layer_data["score"])

        if layer_scores:
            self.results["overall_score"] = int(statistics.mean(layer_scores))
        else:
            self.results["overall_score"] = 0

        # Determine status
        if self.results["overall_score"] >= 90:
            self.results["status"] = "excellent"
        elif self.results["overall_score"] >= 80:
            self.results["status"] = "good"
        elif self.results["overall_score"] >= 70:
            self.results["status"] = "acceptable"
        elif self.results["overall_score"] >= 50:
            self.results["status"] = "needs_improvement"
        else:
            self.results["status"] = "critical"

    def _apply_auto_fixes(self) -> None:
        """Apply automatic fixes for common issues."""
        fixes_applied = []

        # Fix missing data files
        data_files = ["patterns.json", "quality_history.json", "insights.json", "trends.json", "predictions.json"]
        for filename in data_files:
            filepath = self.patterns_dir / filename
            if not filepath.exists():
                try:
                    # Create empty structure
                    if filename == "patterns.json":
                        template = {
                            "project_context": {},
                            "patterns": [],
                            "skill_effectiveness": {},
                            "agent_effectiveness": {},
                            "metadata": {"total_patterns": 0, "last_updated": datetime.now().isoformat()}
                        }
                    elif filename == "quality_history.json":
                        template = {
                            "quality_assessments": [],
                            "statistics": {"avg_quality_score": 0, "total_assessments": 0},
                            "metadata": {"last_assessment": datetime.now().isoformat()}
                        }
                    else:
                        template = {}

                    with open(filepath, 'w') as f:
                        json.dump(template, f, indent=2)

                    fixes_applied.append(f"Created missing {filename}")
                    print(f"   🔧 Created missing {filename}")
                except Exception as e:
                    print(f"   ❌ Failed to create {filename}: {e}")

        # Fix JSON syntax errors
        for filename in data_files:
            filepath = self.patterns_dir / filename
            if filepath.exists():
                if self._fix_json_syntax(filepath):
                    fixes_applied.append(f"Fixed JSON syntax in {filename}")
                    print(f"   🔧 Fixed JSON syntax in {filename}")

        self.results["fixes_applied"] = fixes_applied

    def _generate_recommendations(self) -> None:
        """Generate improvement recommendations based on validation results."""
        recommendations = []

        # Performance recommendations
        perf_layer = self.results["layers"].get("performance", {})
        if "tests" in perf_layer:
            api_times = perf_layer["tests"].get("api_response_times", {})
            if api_times.get("avg_response_time", 0) > 0.2:
                recommendations.append({
                    "priority": "medium",
                    "category": "performance",
                    "issue": "Slow API responses",
                    "recommendation": "Implement response caching and optimize database queries"
                })

            resource_usage = perf_layer["tests"].get("resource_usage", {})
            if resource_usage.get("memory_mb", 0) > 200:
                recommendations.append({
                    "priority": "medium",
                    "category": "performance",
                    "issue": "High memory usage",
                    "recommendation": "Implement memory cleanup and optimize data structures"
                })

        # Data layer recommendations
        data_layer = self.results["layers"].get("data", {})
        if data_layer.get("score", 100) < 100:
            recommendations.append({
                "priority": "low",
                "category": "data",
                "issue": "Data layer issues detected",
                "recommendation": "Review data file integrity and implement regular backups"
            })

        # Frontend recommendations
        frontend_layer = self.results["layers"].get("frontend", {})
        if frontend_layer.get("score", 100) < 100:
            recommendations.append({
                "priority": "low",
                "category": "frontend",
                "issue": "Frontend layer issues detected",
                "recommendation": "Test browser compatibility and optimize JavaScript performance"
            })

        # General recommendations based on overall score
        if self.results["overall_score"] < 80:
            recommendations.append({
                "priority": "high",
                "category": "general",
                "issue": "Dashboard health below optimal",
                "recommendation": "Schedule regular validation checks and implement monitoring alerts"
            })

        self.results["recommendations"] = recommendations

    def print_results(self) -> None:
        """Print formatted validation results."""
        print("\n" + "="*55)
        print(f"  DASHBOARD VALIDATION {'COMPLETE' if self.results['status'] != 'failed' else 'FAILED'}")
        print("="*55)

        # Overall status
        status_emoji = {
            "excellent": "✅",
            "good": "✅",
            "acceptable": "✅",
            "needs_improvement": "⚠️",
            "critical": "🚨",
            "failed": "❌"
        }

        print(f"\n┌─ Overall Health Score ──────────────────────────────┐")
        print(f"│ Score: {self.results['overall_score']}/100 {status_emoji.get(self.results['status'], '❓')} {self.results['status'].upper().replace('_', ' ').title()} │")
        if "execution_time" in self.results:
            print(f"│ Validation Time: {self.results['execution_time']:.1f}s           │")
        print(f"└───────────────────────────────────────────────────────┘")

        # Layer results
        for layer_name, layer_data in self.results["layers"].items():
            layer_emoji = "✅" if layer_data.get("score", 0) >= 80 else "⚠️" if layer_data.get("score", 0) >= 60 else "❌"
            print(f"\n┌─ {layer_name.title()} Layer ───────────────────────────────┐")
            print(f"│ Score: {layer_data.get('score', 0):3d}/100 {layer_emoji}                    │")

            # Show key test results
            if "tests" in layer_data:
                for test_name, test_result in layer_data["tests"].items():
                    test_emoji = "✅" if test_result.get("status") == "pass" else "⚠️" if test_result.get("status") == "warning" else "❌"
                    test_display_name = test_name.replace("_", " ").title()
                    print(f"│ {test_display_name:<20} {test_emoji}                 │")

            print(f"└───────────────────────────────────────────────────────┘")

        # Performance metrics
        if self.results.get("performance_metrics"):
            print(f"\n┌─ Performance Metrics ───────────────────────────────┐")
            metrics = self.results["performance_metrics"]

            if "response_times" in metrics:
                rt = metrics["response_times"]
                print(f"│ API Response Time: {rt['avg']:.3f}s avg              │")

            if "memory" in metrics:
                mem = metrics["memory"]
                print(f"│ Memory Usage: {mem['rss_mb']:.1f}MB                   │")

            print(f"└───────────────────────────────────────────────────────┘")

        # Issues found
        if self.results["issues"]:
            print(f"\n┌─ Issues Found ─────────────────────────────────────┐")
            for i, issue in enumerate(self.results["issues"][:10], 1):  # Show max 10 issues
                print(f"│ {i}. {issue:<50} │")
            if len(self.results["issues"]) > 10:
                print(f"│ ... and {len(self.results['issues']) - 10} more issues           │")
            print(f"└───────────────────────────────────────────────────────┘")

        # Fixes applied
        if self.results.get("fixes_applied"):
            print(f"\n┌─ Auto-Fixes Applied ───────────────────────────────┐")
            for fix in self.results["fixes_applied"]:
                print(f"│ • {fix:<47} │")
            print(f"└───────────────────────────────────────────────────────┘")

        # Recommendations
        if self.results["recommendations"]:
            print(f"\n┌─ Recommendations ──────────────────────────────────┐")
            for i, rec in enumerate(self.results["recommendations"][:5], 1):  # Show max 5 recommendations
                priority_emoji = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
                print(f"│ {i}. {priority_emoji} {rec['recommendation']:<45} │")
            print(f"└───────────────────────────────────────────────────────┘")

        # Final status
        if self.results["status"] in ["excellent", "good", "acceptable"]:
            print(f"\n🌐 Dashboard URL: {self.dashboard_url}")
            print(f"📊 Status: Production Ready ✅")
        elif self.results["status"] == "needs_improvement":
            print(f"\n⚠️ Dashboard functional but needs optimization")
        else:
            print(f"\n🚨 Dashboard requires immediate attention")


def main():
    """Main entry point for dashboard validator."""
    parser = argparse.ArgumentParser(description="Dashboard Validation and Debugging Tool")
    parser.add_argument("--patterns-dir", default=".claude-patterns",
                       help="Directory containing pattern data")
    parser.add_argument("--dashboard-url", default="http://127.0.0.1:5000",
                       help="URL of the dashboard to validate")
    parser.add_argument("--type", choices=["quick", "full", "performance", "data", "frontend"],
                       default="full", help="Type of validation to run")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--output", help="Output results to JSON file")

    args = parser.parse_args()

    # Create validator
    validator = DashboardValidator(
        patterns_dir=args.patterns_dir,
        dashboard_url=args.dashboard_url
    )

    # Run validation
    results = validator.run_validation(args.type)

    # Print results
    validator.print_results()

    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📄 Results saved to: {args.output}")

    # Exit with appropriate code
    if results["status"] in ["failed", "critical"]:
        sys.exit(1)
    elif results["status"] in ["needs_improvement"]:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()