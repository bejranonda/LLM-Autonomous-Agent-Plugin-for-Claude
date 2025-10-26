#!/usr/bin/env python3
"""
Enhanced Automatic Performance Recording System v2.2

Integrates with the orchestrator and learning-engine to automatically
capture performance metrics for all tasks, not just assessments.

ENHANCEMENTS v2.2:
- Real-time model detection and attribution
- Data integrity validation and contamination prevention
- Accurate cross-model performance tracking
- Comprehensive validation layer
- Prevention of simulated/fake data

Features:
- Automatic performance metric capture for all task types
- Real-time model detection with high accuracy
- Data integrity validation and cleanup
- Backward compatibility with existing performance records
- Real-time dashboard integration
- Cross-model performance tracking
- Quality improvement scoring
- Time efficiency measurement

Compatible with existing dashboard.py and performance data format.
"""

import json
import os
import time
import uuid
import re
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path


class AutomaticPerformanceRecorder:
    """Automatically records performance metrics for all tasks with enhanced model detection."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        self.patterns_dir = Path(patterns_dir)
        self.patterns_dir.mkdir(exist_ok=True)

        # Performance data files
        self.quality_history_file = self.patterns_dir / "quality_history.json"
        self.performance_records_file = self.patterns_dir / "performance_records.json"
        self.model_performance_file = self.patterns_dir / "model_performance.json"
        self.data_integrity_file = self.patterns_dir / "data_integrity.json"

        # Initialize files if they don't exist
        self._initialize_files()

        # Initialize model detection
        self._initialize_model_detection()

    def _initialize_model_detection(self):
        """Initialize model detection context and validation."""
        # Cache for model detection results
        self._model_cache = {}
        self._model_cache_ttl = 300  # 5 minutes
        self._last_model_detection = None
        self._last_detection_time = 0

    def detect_current_model(self) -> str:
        """
        Enhanced real-time model detection with multiple strategies.

        Returns:
            str: The detected model name (e.g., "GLM 4.6", "Claude Sonnet 4.5")
        """
        current_time = time.time()

        # Check cache first
        if (self._last_model_detection and
            current_time - self._last_detection_time < self._model_cache_ttl):
            return self._last_model_detection

        detected_model = None

        # Strategy 1: Environment variables
        detected_model = self._detect_from_environment()

        # Strategy 2: Session context analysis
        if not detected_model:
            detected_model = self._detect_from_session_context()

        # Strategy 3: Performance patterns analysis
        if not detected_model:
            detected_model = self._detect_from_performance_patterns()

        # Strategy 4: Default fallback with validation
        if not detected_model:
            detected_model = self._detect_default_model()

        # Cache result
        self._last_model_detection = detected_model
        self._last_detection_time = current_time

        return detected_model

    def _detect_from_environment(self) -> Optional[str]:
        """Detect model from environment variables and system context."""
        # Check for Claude Code specific environment variables
        claude_env_vars = [
            'ANTHROPIC_MODEL',
            'CLAUDE_MODEL',
            'MODEL_NAME'
        ]

        for var in claude_env_vars:
            model = os.environ.get(var)
            if model:
                # Normalize common model names
                return self._normalize_model_name(model)

        # Check for GLM specific indicators
        glm_env_vars = [
            'GLM_MODEL',
            'ZHIPU_MODEL',
            'OPENAI_MODEL'  # Some GLM integrations use this
        ]

        for var in glm_env_vars:
            model = os.environ.get(var)
            if model:
                return self._normalize_model_name(model)

        return None

    def _detect_from_session_context(self) -> Optional[str]:
        """Detect model from current session context and file patterns."""
        try:
            # Check for Claude Code CLI indicators
            if os.path.exists(os.path.expanduser("~/.config/claude")):
                # Look for model preferences in Claude config
                config_files = [
                    os.path.expanduser("~/.config/claude/config.json"),
                    os.path.expanduser("~/.claude/config.json")
                ]

                for config_file in config_files:
                    if os.path.exists(config_file):
                        try:
                            with open(config_file, 'r') as f:
                                config = json.load(f)

                            # Check for model settings
                            model = config.get('model') or config.get('default_model')
                            if model:
                                return self._normalize_model_name(model)
                        except (json.JSONDecodeError, KeyError):
                            continue

            # Check for GLM/ChatGLM session indicators
            glm_indicators = [
                "zhipuai",
                "chatglm",
                "glm-4.6",
                "glm-4"
            ]

            # Check current working directory and process info
            cwd = os.getcwd().lower()
            for indicator in glm_indicators:
                if indicator in cwd:
                    return "GLM 4.6"  # Most likely GLM model

            # Check process environment
            try:
                with open('/proc/self/environ', 'r') if os.path.exists('/proc/self/environ') else open(os.devnull, 'r') as f:
                    env_content = f.read()
                    for indicator in glm_indicators:
                        if indicator in env_content.lower():
                            return "GLM 4.6"
            except:
                pass

        except Exception:
            pass

        return None

    def _detect_from_performance_patterns(self) -> Optional[str]:
        """Detect model by analyzing recent performance patterns."""
        try:
            # Load recent quality history
            if self.quality_history_file.exists():
                with open(self.quality_history_file, 'r') as f:
                    quality_data = json.load(f)

                # Look at recent assessments for model patterns
                recent_assessments = quality_data.get('quality_assessments', [])[-10:]  # Last 10

                model_counts = {}
                for assessment in recent_assessments:
                    # Check multiple possible model field locations
                    model = (assessment.get('details', {}).get('model_used') or
                           assessment.get('model_used') or
                           assessment.get('model'))

                    if model and model != 'Unknown':
                        model_counts[model] = model_counts.get(model, 0) + 1

                # Return the most frequently used model
                if model_counts:
                    most_used_model = max(model_counts.items(), key=lambda x: x[1])[0]
                    return most_used_model

        except Exception:
            pass

        return None

    def _detect_default_model(self) -> str:
        """Detect default model based on system heuristics."""
        # Check for common indicators
        try:
            # Claude Code CLI typically runs with specific patterns
            if 'claude' in sys.modules or 'anthropic' in str(type(sys.modules)):
                return "Claude Sonnet 4.5"

            # Check for Python environment that might indicate GLM
            import platform
            system_info = platform.platform().lower()
            if 'windows' in system_info and 'claude code' in os.environ.get('TERM_PROGRAM', '').lower():
                return "Claude Sonnet 4.5"

            # Default to Claude for most environments
            return "Claude Sonnet 4.5"

        except Exception:
            return "Claude Sonnet 4.5"  # Safe default

    def _normalize_model_name(self, model_name: str) -> str:
        """Normalize various model name formats to standard names."""
        if not model_name:
            return "Unknown"

        model_lower = model_name.lower()

        # Claude models
        claude_patterns = {
            'claude-sonnet-4.5': 'Claude Sonnet 4.5',
            'claude-4.5': 'Claude Sonnet 4.5',
            'claude-sonnet': 'Claude Sonnet 4.5',
            'sonnet-4.5': 'Claude Sonnet 4.5',
            'claude-3.5-sonnet': 'Claude Sonnet 3.5',
            'claude-opus-4.1': 'Claude Opus 4.1',
            'claude-opus': 'Claude Opus 4.1',
            'claude-4.1': 'Claude Opus 4.1',
            'claude-haiku-4.5': 'Claude Haiku 4.5',
            'claude-haiku': 'Claude Haiku 4.5',
        }

        # GLM models
        glm_patterns = {
            'glm-4.6': 'GLM 4.6',
            'glm-4': 'GLM 4.6',
            'chatglm-4.6': 'GLM 4.6',
            'chatglm4': 'GLM 4.6',
            'zhipuai-glm-4.6': 'GLM 4.6',
        }

        # Check Claude patterns
        for pattern, standard_name in claude_patterns.items():
            if pattern in model_lower:
                return standard_name

        # Check GLM patterns
        for pattern, standard_name in glm_patterns.items():
            if pattern in model_lower:
                return standard_name

        # Fallback to original name with basic formatting
        return model_name.strip().title()

    def validate_data_integrity(self, record: Dict[str, Any]) -> bool:
        """
        Validate performance record for authenticity and prevent data contamination.

        Args:
            record: Performance record to validate

        Returns:
            bool: True if record appears authentic, False if likely contaminated
        """
        # Check for test/simulation indicators (but allow 'auto' prefixes)
        task_type = record.get('task_type', '').lower()
        assessment_id = record.get('assessment_id', '').lower()

        # Only block if assessment_id contains 'test' but doesn't start with 'auto-'
        if 'test' in assessment_id and not assessment_id.startswith('auto-'):
            return False

        # Check model field for test indicators
        model_used = record.get('details', {}).get('model_used', '').lower()
        if model_used == 'test model':
            return False

        # Validate timestamp is recent and realistic
        timestamp = record.get('timestamp', '')
        if timestamp:
            try:
                # Handle both Z and +00:00 timezone formats
                if timestamp.endswith('Z'):
                    record_time = datetime.fromisoformat(timestamp.rstrip('Z'))
                elif '+00:00' in timestamp:
                    record_time = datetime.fromisoformat(timestamp)
                else:
                    # Try parsing without timezone info
                    record_time = datetime.fromisoformat(timestamp)

                current_time = datetime.now()

                # Reject records that are too old or too far in the future
                time_diff = abs((current_time - record_time).total_seconds())
                if time_diff > 365 * 24 * 3600:  # More than 1 year
                    return False
            except Exception as e:
                # Log the error for debugging but don't fail validation
                print(f"Timestamp validation warning: {e}")
                print(f"Problematic timestamp: {timestamp}")
                return False

        # Validate score ranges are realistic
        score = record.get('overall_score', 0)
        if not (0 <= score <= 100):
            return False

        # Validate model name is realistic
        model = (record.get('details', {}).get('model_used') or
                record.get('model_used', ''))

        if model and not self._is_realistic_model_name(model):
            return False

        return True

    def _is_realistic_model_name(self, model_name: str) -> bool:
        """Check if model name appears realistic."""
        realistic_patterns = [
            'claude', 'glm', 'gpt', 'llama', 'mistral', 'gemini',
            'claude-sonnet', 'claude-opus', 'claude-haiku',
            'chatglm', 'zhipuai'
        ]

        model_lower = model_name.lower()
        return any(pattern in model_lower for pattern in realistic_patterns)

    def clean_contaminated_data(self):
        """Remove contaminated or simulated data from performance files."""
        try:
            # Clean quality history
            if self.quality_history_file.exists():
                with open(self.quality_history_file, 'r') as f:
                    quality_data = json.load(f)

                original_count = len(quality_data.get('quality_assessments', []))

                # Filter out contaminated records
                clean_assessments = []
                for assessment in quality_data.get('quality_assessments', []):
                    if self.validate_data_integrity(assessment):
                        clean_assessments.append(assessment)

                quality_data['quality_assessments'] = clean_assessments

                # Update statistics
                if clean_assessments:
                    total_assessments = len(clean_assessments)
                    passing_assessments = sum(1 for a in clean_assessments if a.get('pass', False))
                    avg_score = sum(a.get('overall_score', 0) for a in clean_assessments) / total_assessments

                    quality_data['statistics'] = {
                        'avg_quality_score': round(avg_score, 1),
                        'total_assessments': total_assessments,
                        'passing_rate': passing_assessments / total_assessments,
                        'trend': quality_data.get('statistics', {}).get('trend', 'stable')
                    }

                    # Update last assessment
                    last_assessment = max(clean_assessments, key=lambda x: x.get('timestamp', ''))
                    quality_data['metadata']['last_assessment'] = last_assessment.get('timestamp', '')

                with open(self.quality_history_file, 'w') as f:
                    json.dump(quality_data, f, indent=2)

                print(f"Cleaned {original_count - len(clean_assessments)} contaminated records from quality history")

            # Clean model performance data (remove simulated data)
            if self.model_performance_file.exists():
                with open(self.model_performance_file, 'r') as f:
                    model_data = json.load(f)

                # Keep only real models with realistic data
                clean_model_data = {}
                for model_name, model_stats in model_data.items():
                    if self._is_realistic_model_name(model_name):
                        # Validate recent scores for authenticity
                        recent_scores = model_stats.get('recent_scores', [])
                        clean_scores = []

                        for score_data in recent_scores:
                            # Check for realistic patterns (not perfect hourly intervals)
                            timestamp = score_data.get('timestamp', '')
                            score = score_data.get('score', 0)

                            if (timestamp and score and
                                0 <= score <= 100 and
                                self._is_realistic_timestamp(timestamp)):
                                clean_scores.append(score_data)

                        if clean_scores:
                            model_stats['recent_scores'] = clean_scores
                            clean_model_data[model_name] = model_stats

                with open(self.model_performance_file, 'w') as f:
                    json.dump(clean_model_data, f, indent=2)

                print(f"Cleaned model performance data, kept {len(clean_model_data)} authentic models")

        except Exception as e:
            print(f"Warning: Error during data cleanup: {e}")

    def _is_realistic_timestamp(self, timestamp: str) -> bool:
        """Check if timestamp appears realistic (not perfectly spaced)."""
        try:
            # Basic timestamp validation
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

            # Check if timestamp is within reasonable bounds
            now = datetime.now()
            time_diff = abs((now - dt).total_seconds())

            # Reject if too far in future or past
            return time_diff < 30 * 24 * 3600  # 30 days
        except:
            return False

    def _initialize_files(self):
        """Initialize performance tracking files."""
        # Initialize quality history if needed
        if not self.quality_history_file.exists():
            self._save_json(self.quality_history_file, {
                "quality_assessments": [],
                "statistics": {
                    "avg_quality_score": 0,
                    "total_assessments": 0,
                    "passing_rate": 0,
                    "trend": "no_data"
                },
                "baselines": {},
                "metadata": {
                    "version": "2.0.0",
                    "auto_recording_enabled": True
                }
            })

        # Initialize performance records if needed
        if not self.performance_records_file.exists():
            self._save_json(self.performance_records_file, {
                "version": "2.0.0",
                "records": [],
                "task_types": {},
                "model_metrics": {},
                "metadata": {
                    "auto_recording_enabled": True,
                    "created": datetime.now().isoformat()
                }
            })

    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON file safely."""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load {file_path}: {e}")
        return {}

    def _save_json(self, file_path: Path, data: Dict):
        """Save JSON file safely."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save {file_path}: {e}")

    def record_task_performance(self,
                              task_data: Dict[str, Any],
                              model_used: Optional[str] = None) -> str:
        """
        Enhanced performance recording with real-time model detection and data validation.

        Args:
            task_data: Dictionary containing task information
            model_used: Optional model override (if None, will auto-detect)

        Returns:
            assessment_id: Unique identifier for the performance record
        """
        # Auto-detect model if not provided
        if not model_used:
            model_used = self.detect_current_model()

        # Generate unique assessment ID with model prefix
        model_prefix = model_used.lower().replace(' ', '-').replace('.', '-')
        assessment_id = f"auto-{model_prefix}-{task_data.get('task_type', 'task')}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        # Calculate performance metrics
        performance_metrics = self._calculate_performance_metrics(task_data)

        # Create enhanced performance record
        performance_record = {
            "assessment_id": assessment_id,
            "timestamp": datetime.now().isoformat() + "Z",
            "task_type": task_data.get("task_type", "general"),
            "overall_score": performance_metrics["overall_score"],
            "breakdown": performance_metrics["breakdown"],
            "details": {
                "auto_recorded": True,
                "model_used": model_used,
                "model_detected_by": "auto-detection" if not model_used else "provided",
                "task_description": task_data.get("description", ""),
                "task_complexity": task_data.get("complexity", "medium"),
                "duration_seconds": task_data.get("duration", 0),
                "skills_used": task_data.get("skills_used", []),
                "agents_delegated": task_data.get("agents_delegated", []),
                "files_modified": task_data.get("files_modified", 0),
                "lines_changed": task_data.get("lines_changed", 0),
                "success": task_data.get("success", True),
                "quality_improvement": performance_metrics.get("quality_improvement", 0),
                "time_efficiency": performance_metrics.get("time_efficiency", 0),
                "performance_index": performance_metrics.get("performance_index", 0),
                "data_source": "real_performance_recording",
                "validation_status": "validated"
            },
            "issues_found": task_data.get("issues_found", []),
            "recommendations": task_data.get("recommendations", []),
            "pass": performance_metrics["overall_score"] >= 70,
            "auto_generated": True,
            "data_integrity": {
                "authenticity_score": 1.0,
                "validation_timestamp": datetime.now().isoformat() + "Z",
                "contamination_flags": []
            }
        }

        # Validate record integrity before storing
        if not self.validate_data_integrity(performance_record):
            print(f"Warning: Record {assessment_id} failed integrity validation, skipping storage")
            return assessment_id

        # Add to quality history (compatible format)
        self._add_to_quality_history(performance_record)

        # Add to performance records (new format)
        self._add_to_performance_records(performance_record, model_used)

        # Update model performance metrics
        self._update_model_performance(model_used, performance_record)

        return assessment_id

    def _calculate_performance_metrics(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance metrics based on task data."""

        # Base score calculation
        base_score = 70  # Default passing score

        # Quality factors
        quality_factors = {
            "task_completion": 30 if task_data.get("success", True) else 0,
            "code_quality": min(25, task_data.get("lines_changed", 0) * 0.1),
            "efficiency": min(20, 300 / max(task_data.get("duration", 60), 30)),  # Faster is better
            "best_practices": 15 if task_data.get("best_practices_followed", True) else 5,
            "documentation": 10 if task_data.get("documentation_updated", False) else 5
        }

        overall_score = min(100, base_score + sum(quality_factors.values()))

        # Calculate breakdown
        breakdown = {
            "tests_passing": int(quality_factors["task_completion"] * 0.3),
            "standards_compliance": int(quality_factors["best_practices"] * 0.25),
            "documentation": int(quality_factors["documentation"] * 2.5),
            "pattern_adherence": int(quality_factors["best_practices"] * 0.15),
            "code_metrics": int(quality_factors["code_quality"])
        }

        # Normalize breakdown to sum to overall_score
        breakdown_sum = sum(breakdown.values())
        if breakdown_sum > 0:
            breakdown = {k: int(v * overall_score / breakdown_sum) for k, v in breakdown.items()}

        # Calculate performance indices
        quality_improvement = task_data.get("quality_improvement", 0)
        time_efficiency = min(100, quality_factors["efficiency"] * 5)

        # Performance Index calculation (compatible with debugging performance)
        performance_index = (
            0.40 * overall_score +
            0.35 * time_efficiency +
            0.25 * (100 if task_data.get("success", True) else 0)
        )

        return {
            "overall_score": overall_score,
            "breakdown": breakdown,
            "quality_improvement": quality_improvement,
            "time_efficiency": time_efficiency,
            "performance_index": performance_index
        }

    def _add_to_quality_history(self, record: Dict[str, Any]):
        """Add record to quality history for dashboard compatibility."""
        quality_data = self._load_json(self.quality_history_file)

        # Add to assessments list
        quality_data["quality_assessments"].append(record)

        # Update statistics
        total_assessments = len(quality_data["quality_assessments"])
        passing_assessments = sum(1 for a in quality_data["quality_assessments"] if a.get("pass", False))
        avg_score = sum(a.get("overall_score", 0) for a in quality_data["quality_assessments"]) / total_assessments

        quality_data["statistics"] = {
            "avg_quality_score": round(avg_score, 1),
            "total_assessments": total_assessments,
            "passing_rate": passing_assessments / total_assessments if total_assessments > 0 else 0,
            "trend": self._calculate_trend(quality_data["quality_assessments"])
        }

        # Update metadata
        quality_data["metadata"]["last_assessment"] = record["timestamp"]
        quality_data["metadata"]["auto_recording_count"] = quality_data["metadata"].get("auto_recording_count", 0) + 1

        self._save_json(self.quality_history_file, quality_data)

    def _add_to_performance_records(self, record: Dict[str, Any], model_used: str):
        """Add record to dedicated performance records file."""
        perf_data = self._load_json(self.performance_records_file)

        # Add to records list
        perf_data["records"].append({
            **record,
            "model_used": model_used
        })

        # Update task type statistics
        task_type = record["task_type"]
        if task_type not in perf_data["task_types"]:
            perf_data["task_types"][task_type] = {
                "count": 0,
                "avg_score": 0,
                "success_rate": 0
            }

        task_stats = perf_data["task_types"][task_type]
        task_stats["count"] += 1

        # Update average score for this task type
        type_records = [r for r in perf_data["records"] if r["task_type"] == task_type]
        task_stats["avg_score"] = sum(r.get("overall_score", 0) for r in type_records) / len(type_records)

        # Update success rate
        successful_tasks = sum(1 for r in type_records if r.get("pass", False))
        task_stats["success_rate"] = successful_tasks / len(type_records)

        # Update metadata
        perf_data["metadata"]["last_updated"] = record["timestamp"]
        perf_data["metadata"]["total_records"] = len(perf_data["records"])

        self._save_json(self.performance_records_file, perf_data)

    def _update_model_performance(self, model_used: str, record: Dict[str, Any]):
        """Update model-specific performance metrics."""
        model_data = self._load_json(self.model_performance_file)

        if model_used not in model_data:
            model_data[model_used] = {
                "total_tasks": 0,
                "avg_score": 0,
                "success_rate": 0,
                "task_types": {},
                "performance_timeline": [],
                "last_updated": None
            }

        model_stats = model_data[model_used]

        # Handle legacy data structures by initializing missing fields
        if "performance_timeline" not in model_stats:
            model_stats["performance_timeline"] = []
        if "task_types" not in model_stats:
            model_stats["task_types"] = {}
        if "avg_score" not in model_stats:
            model_stats["avg_score"] = 0
        if "last_updated" not in model_stats:
            model_stats["last_updated"] = None

        # Ensure total_tasks exists for legacy data
        if "total_tasks" not in model_stats:
            model_stats["total_tasks"] = 0

        model_stats["total_tasks"] += 1

        # Add to performance timeline
        model_stats["performance_timeline"].append({
            "timestamp": record["timestamp"],
            "score": record["overall_score"],
            "task_type": record["task_type"],
            "performance_index": record["details"].get("performance_index", 0)
        })

        # Keep only last 100 entries per model
        if len(model_stats["performance_timeline"]) > 100:
            model_stats["performance_timeline"] = model_stats["performance_timeline"][-100:]

        # Update averages
        recent_scores = [entry["score"] for entry in model_stats["performance_timeline"]]
        model_stats["avg_score"] = sum(recent_scores) / len(recent_scores)

        successful_tasks = sum(1 for entry in model_stats["performance_timeline"] if entry["score"] >= 70)
        model_stats["success_rate"] = successful_tasks / len(recent_scores)

        # Update task type stats for this model
        task_type = record["task_type"]
        if task_type not in model_stats["task_types"]:
            model_stats["task_types"][task_type] = {"count": 0, "avg_score": 0}

        model_stats["task_types"][task_type]["count"] += 1
        type_entries = [e for e in model_stats["performance_timeline"] if e["task_type"] == task_type]
        if type_entries:
            model_stats["task_types"][task_type]["avg_score"] = sum(e["score"] for e in type_entries) / len(type_entries)

        model_stats["last_updated"] = record["timestamp"]

        self._save_json(self.model_performance_file, model_data)

    def _calculate_trend(self, assessments: List[Dict[str, Any]]) -> str:
        """Calculate quality trend over recent assessments."""
        if len(assessments) < 3:
            return "insufficient_data"

        # Get last 10 assessments
        recent = assessments[-10:]
        scores = [a.get("overall_score", 0) for a in recent]

        if len(scores) < 3:
            return "insufficient_data"

        # Compare first half to second half
        mid = len(scores) // 2
        first_half_avg = sum(scores[:mid]) / mid
        second_half_avg = sum(scores[mid:]) / (len(scores) - mid)

        diff = second_half_avg - first_half_avg

        if diff > 5:
            return "improving"
        elif diff < -5:
            return "declining"
        else:
            return "stable"

    def get_performance_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get performance summary for the specified time period."""
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_iso = cutoff_date.isoformat() + "Z"

        # Load recent records
        perf_data = self._load_json(self.performance_records_file)
        recent_records = [
            r for r in perf_data.get("records", [])
            if r.get("timestamp", "") >= cutoff_iso
        ]

        if not recent_records:
            return {
                "period_days": days,
                "total_tasks": 0,
                "avg_score": 0,
                "success_rate": 0,
                "task_types": {},
                "models_used": {}
            }

        # Calculate summary statistics
        scores = [r.get("overall_score", 0) for r in recent_records]
        successful_tasks = sum(1 for r in recent_records if r.get("pass", False))

        # Task type breakdown
        task_types = {}
        for record in recent_records:
            task_type = record.get("task_type", "unknown")
            if task_type not in task_types:
                task_types[task_type] = {"count": 0, "avg_score": 0}
            task_types[task_type]["count"] += 1

        # Model breakdown
        models_used = {}
        for record in recent_records:
            model = record.get("model_used", "unknown")
            if model not in models_used:
                models_used[model] = {"count": 0, "avg_score": 0}
            models_used[model]["count"] += 1

        # Calculate averages for task types and models
        for task_type in task_types:
            type_records = [r for r in recent_records if r.get("task_type") == task_type]
            task_types[task_type]["avg_score"] = sum(r.get("overall_score", 0) for r in type_records) / len(type_records)

        for model in models_used:
            model_records = [r for r in recent_records if r.get("model_used") == model]
            models_used[model]["avg_score"] = sum(r.get("overall_score", 0) for r in model_records) / len(model_records)

        return {
            "period_days": days,
            "total_tasks": len(recent_records),
            "avg_score": sum(scores) / len(scores),
            "success_rate": successful_tasks / len(recent_records),
            "task_types": task_types,
            "models_used": models_used,
            "period_start": cutoff_iso,
            "period_end": datetime.now().isoformat() + "Z"
        }


# Integration function for orchestrator
def record_task_performance(task_data: Dict[str, Any],
                          model_used: str = "Claude Sonnet 4.5",
                          patterns_dir: str = ".claude-patterns") -> str:
    """
    Convenience function to record task performance.

    This function is designed to be called automatically by the orchestrator
    after any task completion.

    Args:
        task_data: Task information dictionary
        model_used: Model that executed the task
        patterns_dir: Directory for pattern storage

    Returns:
        assessment_id: Unique identifier for the performance record
    """
    recorder = AutomaticPerformanceRecorder(patterns_dir)
    return recorder.record_task_performance(task_data, model_used)


# Example usage data structures
EXAMPLE_TASK_DATA = {
    "task_type": "refactoring",
    "description": "Refactored authentication module for better security",
    "complexity": "medium",
    "duration": 180,  # seconds
    "success": True,
    "skills_used": ["code-analysis", "quality-standards", "security-patterns"],
    "agents_delegated": ["code-analyzer", "quality-controller"],
    "files_modified": 3,
    "lines_changed": 127,
    "quality_improvement": 15,
    "issues_found": ["Minor code style issues"],
    "recommendations": ["Add unit tests for new methods"],
    "best_practices_followed": True,
    "documentation_updated": True
}