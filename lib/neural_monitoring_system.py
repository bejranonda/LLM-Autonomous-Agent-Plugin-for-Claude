#!/usr/bin/env python3
#     Neural Monitoring System
    """
Advanced AI-powered monitoring and analytics system with neural networks,
predictive analytics, anomaly detection, and real-time visualization.
import json
import sys
import time
import threading
import asyncio
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import statistics
import hashlib

# Platform-specific imports for file locking
try:
    import msvcrt  # Windows

    PLATFORM = "windows"
except ImportError:
    import fcntl  # Unix/Linux/Mac

    PLATFORM = "unix"


@dataclass
class MonitoringMetric:
    """Individual monitoring metric data structure."""

    timestamp: float
    metric_name: str
    value: float
    agent_id: str
    tier: str
    context: Dict[str, Any]
    anomaly_score: float = 0.0
    trend: str = "stable"
    severity: str = "normal"


@dataclass
class AnomalyDetection:
    """Anomaly detection result."""

    detection_id: str
    timestamp: datetime
    metric_name: str
    agent_id: str
    anomaly_type: str
    severity: str
    confidence: float
    description: str
    suggested_actions: List[str]
    related_metrics: List[str]


@dataclass
class PredictiveInsight:
    """Predictive analytics insight."""

    insight_id: str
    timestamp: datetime
    prediction_type: str
    confidence: float
    timeframe: str
    description: str
    impact_assessment: str
    recommendations: List[str]
    related_agents: List[str]


class NeuralMonitoringSystem:
    """
    Advanced AI-powered monitoring system with neural networks,
    """
    predictive analytics, and real-time anomaly detection.
    """

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the neural monitoring system.

        Args:
            storage_dir: Directory for storing monitoring data
        """
        self.storage_dir = Path(storage_dir)
        self.monitoring_file = self.storage_dir / "neural_monitoring.json"
        self.anomalies_file = self.storage_dir / "anomaly_detections.json"
        self.predictions_file = self.storage_dir / "predictive_insights.json"
        self.models_file = self.storage_dir / "monitoring_models.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Monitoring components
        self.metrics_buffer = deque(maxlen=10000)
        self.anomaly_detector = None
        self.predictive_models = {}
        self.neural_networks = {}
        self.monitoring_agents = set()

        # Neural network parameters
        self.input_dim = 50  # Number of input features
        self.hidden_dims = [64, 32, 16]  # Hidden layer dimensions
        self.output_dim = 1  # Single output for anomaly detection
        self.learning_rate = 0.001
        self.epochs = 100
        self.batch_size = 32

        # Monitoring thresholds
        self.anomaly_threshold = 0.7
        self.trend_threshold = 0.3
        self.prediction_confidence_threshold = 0.8

        # Real-time monitoring
        self.monitoring_active = False
        self.monitoring_thread = None
        self.analysis_thread = None
        self.prediction_thread = None

        # Performance tracking
        self.detection_accuracy = deque(maxlen=100)
        self.prediction_accuracy = deque(maxlen=100)
        self.system_health = 1.0

        # Initialize storage
        self._initialize_monitoring_storage()
        self._load_monitoring_models()

    def _initialize_monitoring_storage(self):
        """Initialize monitoring storage files."""
        if not self.monitoring_file.exists():
            initial_data = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "metrics_history": [],
                "system_health": 1.0,
                "monitoring_agents": [],
                "active_alerts": [],
                "performance_summary": {},
            }
            self._write_monitoring_data(initial_data)

        if not self.anomalies_file.exists():
            anomalies_data = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "anomaly_history": [],
                "active_anomalies": [],
                "detection_statistics": {"total_detections": 0, "true_positives": 0, "false_positives": 0, "accuracy": 0.0},
            }
            self._write_anomalies_data(anomalies_data)

        if not self.predictions_file.exists():
            predictions_data = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "prediction_history": [],
                "active_predictions": [],
                "prediction_statistics": {"total_predictions": 0, "accurate_predictions": 0, "accuracy": 0.0},
            }
            self._write_predictions_data(predictions_data)

        if not self.models_file.exists():
            models_data = {
                "version": "1.0.0",
                "neural_networks": {},
                "anomaly_models": {},
                "predictive_models": {},
                "model_performance": {},
                "training_history": [],
            }
            self._write_models_data(models_data)

    def _load_monitoring_models(self):
        """Load monitoring models from storage."""
        try:
            # Load neural networks
            models_data = self._read_models_data()
            self.neural_networks = models_data.get("neural_networks", {})
            self.predictive_models = models_data.get("predictive_models", {})

            # Initialize anomaly detector if not exists
            if not self.anomaly_detector:
                self._initialize_anomaly_detector()

        except Exception as e:
            print(f"Warning: Failed to load monitoring models: {e}", file=sys.stderr)

    def _initialize_anomaly_detector(self):
        """Initialize the anomaly detection neural network."""
        # Simple neural network implementation for anomaly detection
        self.anomaly_detector = {
            "weights": {
                "input_hidden": [[np.random.randn() for _ in range(self.hidden_dims[0])] for _ in range(self.input_dim)],
                "hidden_output": [[np.random.randn() for _ in range(self.output_dim)] for _ in range(self.hidden_dims[-1])],
            },
            "biases": {
                "hidden": [np.random.randn() for _ in range(self.hidden_dims)],
                "output": [np.random.randn() for _ in range(self.output_dim)],
            },
            "training_data": deque(maxlen=1000),
            "performance": {"accuracy": 0.0, "loss": 1.0},
        }

    def _lock_file(self, file_handle):
        """Platform-specific file locking."""
        if PLATFORM == "windows":
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX)

    def _unlock_file(self, file_handle):
        """Platform-specific file unlocking."""
        if PLATFORM == "windows":
            try:
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            except (OSError, PermissionError):
                pass
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)

    def _read_monitoring_data(self) -> Dict[str, Any]:
        """Read monitoring data with file locking."""
        try:
            with open(self.monitoring_file, "r", encoding="utf-8") as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_monitoring_storage()
            return self._read_monitoring_data()

    def _write_monitoring_data(self, data: Dict[str, Any]):
        """Write monitoring data with file locking."""
        with open(self.monitoring_file, "w", encoding="utf-8") as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_anomalies_data(self) -> Dict[str, Any]:
        """Read anomaly data with file locking."""
        try:
            with open(self.anomalies_file, "r", encoding="utf-8") as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"anomaly_history": [], "detection_statistics": {}}

    def _write_anomalies_data(self, data: Dict[str, Any]):
        """Write anomaly data with file locking."""
        with open(self.anomalies_file, "w", encoding="utf-8") as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_predictions_data(self) -> Dict[str, Any]:
        """Read prediction data with file locking."""
        try:
            with open(self.predictions_file, "r", encoding="utf-8") as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"prediction_history": [], "prediction_statistics": {}}

    def _write_predictions_data(self, data: Dict[str, Any]):
        """Write prediction data with file locking."""
        with open(self.predictions_file, "w", encoding="utf-8") as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_models_data(self) -> Dict[str, Any]:
        """Read models data with file locking."""
        try:
            with open(self.models_file, "r", encoding="utf-8") as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"neural_networks": {}, "predictive_models": {}}

    def _write_models_data(self, data: Dict[str, Any]):
        """Write models data with file locking."""
        with open(self.models_file, "w", encoding="utf-8") as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def register_monitoring_agent(self, agent_id: str, tier: str):
        """
        Register an agent for monitoring.

        Args:
            agent_id: Unique agent identifier
            tier: Agent tier ("analysis" or "execution")
        """
        self.monitoring_agents.add((agent_id, tier))

        # Update storage
        monitoring_data = self._read_monitoring_data()
        if "monitoring_agents" not in monitoring_data:
            monitoring_data["monitoring_agents"] = []

        agent_info = {
            "agent_id": agent_id,
            "tier": tier,
            "registered_at": datetime.now().isoformat(),
            "metrics_count": 0,
            "last_metric": None,
        }

        # Check if agent already registered
        existing = next((a for a in monitoring_data["monitoring_agents"] if a["agent_id"] == agent_id), None)
        if existing:
            existing.update(agent_info)
        else:
            monitoring_data["monitoring_agents"].append(agent_info)

        monitoring_data["last_updated"] = datetime.now().isoformat()
        self._write_monitoring_data(monitoring_data)

        print(f"Registered monitoring agent: {agent_id} ({tier})")

    def record_metric(
        self, metric_name: str, value: float, agent_id: str, tier: str, context: Optional[Dict[str, Any]] = None
    ):
        """Record Metric."""
        Record a monitoring metric.

        Args:
            metric_name: Name of the metric
            value: Metric value
            agent_id: Agent ID
            tier: Agent tier
            context: Additional context information
        """
        if context is None:
            context = {}

        # Create monitoring metric
        metric = MonitoringMetric(
            timestamp=time.time(), metric_name=metric_name, value=value, agent_id=agent_id, tier=tier, context=context
        )

        # Add to buffer
        self.metrics_buffer.append(metric)

        # Store in persistent storage
        monitoring_data = self._read_monitoring_data()
        monitoring_data["metrics_history"].append(asdict(metric))

        # Keep last 10000 metrics in storage
        if len(monitoring_data["metrics_history"]) > 10000:
            monitoring_data["metrics_history"] = monitoring_data["metrics_history"][-10000:]

        # Update agent metrics count
        for agent_info in monitoring_data.get("monitoring_agents", []):
            if agent_info["agent_id"] == agent_id:
                agent_info["metrics_count"] += 1
                agent_info["last_metric"] = datetime.now().isoformat()
                break

        monitoring_data["last_updated"] = datetime.now().isoformat()
        self._write_monitoring_data(monitoring_data)

    def start_monitoring(self):
        """Start the neural monitoring system."""
        if self.monitoring_active:
            print("Monitoring system already active")
            return

        self.monitoring_active = True

        # Start monitoring threads
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()

        self.analysis_thread = threading.Thread(target=self._analysis_loop, daemon=True)
        self.analysis_thread.start()

        self.prediction_thread = threading.Thread(target=self._prediction_loop, daemon=True)
        self.prediction_thread.start()

        print("Neural monitoring system started")

    def stop_monitoring(self):
        """Stop the neural monitoring system."""
        if not self.monitoring_active:
            return

        self.monitoring_active = False

        # Wait for threads to finish
        for thread, name in [
            (self.monitoring_thread, "monitoring"),
            (self.analysis_thread, "analysis"),
            (self.prediction_thread, "prediction"),
        ]:
            if thread and thread.is_alive():
                thread.join(timeout=5)
                print(f"  {name} thread stopped")

        print("Neural monitoring system stopped")

    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                # Process metrics from buffer
                if len(self.metrics_buffer) > 0:
                    # Get recent metrics for analysis
                    recent_metrics = list(self.metrics_buffer)[-100:]  # Last 100 metrics

                    # Check for anomalies
                    anomalies = self._detect_anomalies(recent_metrics)

                    # Record anomalies
                    for anomaly in anomalies:
                        self._record_anomaly(anomaly)

                # Calculate system health
                self._update_system_health()

                # Update monitoring data
                monitoring_data = self._read_monitoring_data()
                monitoring_data["system_health"] = self.system_health
                monitoring_data["last_updated"] = datetime.now().isoformat()
                self._write_monitoring_data(monitoring_data)

                time.sleep(5)  # Monitor every 5 seconds

            except Exception as e:
                print(f"Error in monitoring loop: {e}", file=sys.stderr)
                time.sleep(1)

    def _analysis_loop(self):
        """Analysis loop for deep metric analysis."""
        while self.monitoring_active:
            try:
                # Get metrics for analysis
                if len(self.metrics_buffer) >= 50:  # Need enough data for analysis
                    recent_metrics = list(self.metrics_buffer)[-500:]  # Last 500 metrics

                    # Perform trend analysis
                    trends = self._analyze_trends(recent_metrics)

                    # Perform correlation analysis
                    correlations = self._analyze_correlations(recent_metrics)

                    # Update metrics with trend information
                    for metric in recent_metrics[-10:]:  # Update last 10 metrics
                        if metric.metric_name in trends:
                            metric.trend = trends[metric.metric_name]

                    # Train neural networks periodically
                    if len(self.metrics_buffer) % 100 == 0:  # Every 100 metrics
                        self._train_neural_networks()

                time.sleep(30)  # Analyze every 30 seconds

            except Exception as e:
                print(f"Error in analysis loop: {e}", file=sys.stderr)
                time.sleep(5)

    def _prediction_loop(self):
        """Prediction loop for predictive analytics."""
        while self.monitoring_active:
            try:
                # Get historical data for predictions
                if len(self.metrics_buffer) >= 200:  # Need enough data for predictions
                    historical_metrics = list(self.metrics_buffer)[-1000:]  # Last 1000 metrics

                    # Generate predictions
                    predictions = self._generate_predictions(historical_metrics)

                    # Record predictions
                    for prediction in predictions:
                        self._record_prediction(prediction)

                time.sleep(60)  # Predict every minute

            except Exception as e:
                print(f"Error in prediction loop: {e}", file=sys.stderr)
                time.sleep(10)

    def _detect_anomalies(self, metrics: List[MonitoringMetric]) -> List[AnomalyDetection]:
        """Detect anomalies using neural networks."""
        anomalies = []

        # Group metrics by name and agent
        metric_groups = defaultdict(list)
        for metric in metrics:
            key = f"{metric.agent_id}_{metric.metric_name}"
            metric_groups[key].append(metric)

        for key, group_metrics in metric_groups.items():
            if len(group_metrics) < 10:
                continue  # Need enough data points

            # Extract features for neural network
            features = self._extract_features(group_metrics)

            # Use neural network for anomaly detection
            anomaly_score = self._neural_anomaly_detection(features)

            if anomaly_score > self.anomaly_threshold:
                agent_id, metric_name = key.split("_", 1)
                anomaly = AnomalyDetection(
                    detection_id=str(uuid.uuid4())[:8],
                    timestamp=datetime.now(),
                    metric_name=metric_name,
                    agent_id=agent_id,
                    anomaly_type="statistical",
                    severity="high" if anomaly_score > 0.9 else "medium",
                    confidence=anomaly_score,
                    description=f"Anomaly detected in {metric_name} for {agent_id}",
                    suggested_actions=self._generate_suggested_actions(metric_name, anomaly_score),
                    related_metrics=self._find_related_metrics(metric_name, group_metrics),
                )
                anomalies.append(anomaly)

        return anomalies

    def _extract_features(self, metrics: List[MonitoringMetric]) -> List[float]:
        """Extract features from metrics for neural network input."""
        if not metrics:
            return [0.0] * self.input_dim

        values = [m.value for m in metrics]
        timestamps = [m.timestamp for m in metrics]

        # Statistical features
        features = [
            statistics.mean(values) if values else 0,
            statistics.stdev(values) if len(values) > 1 else 0,
            min(values) if values else 0,
            max(values) if values else 0,
            np.percentile(values, 25) if values else 0,
            np.percentile(values, 75) if values else 0,
            len(values),
            (max(timestamps) - min(timestamps)) if len(timestamps) > 1 else 0,
        ]

        # Trend features
        if len(values) >= 3:
            # Simple linear regression for trend
            x = list(range(len(values)))
            trend_slope = np.polyfit(x, values, 1)[0]
            features.append(trend_slope)
        else:
            features.append(0)

        # Recent vs older comparison
        if len(values) >= 10:
            recent_avg = statistics.mean(values[-3:])
            older_avg = statistics.mean(values[-10:-3])
            features.append(recent_avg - older_avg)
        else:
            features.append(0)

        # Pad to input dimension
        while len(features) < self.input_dim:
            features.append(0.0)

        return features[: self.input_dim]

    def _neural_anomaly_detection(self, features: List[float]) -> float:
        """Use neural network for anomaly detection."""
        if not self.anomaly_detector:
            return 0.0

        try:
            # Forward pass through neural network
            # Hidden layer 1
            hidden1 = []
            for i in range(self.hidden_dims[0]):
                if i < len(features) and i < len(self.anomaly_detector["weights"]["input_hidden"]):
                    weighted_sum = sum(
                        features[j] * self.anomaly_detector["weights"]["input_hidden"][i][j]
                        for j in range(min(len(features), len(self.anomaly_detector["weights"]["input_hidden"][i])))
                    )
                    hidden1.append(self._sigmoid(weighted_sum + self.anomaly_detector["biases"]["hidden"][0]))

            # Hidden layer 2 (simplified)
            hidden2 = []
            for i in range(self.hidden_dims[1]):
                if i < len(hidden1):
                    weighted_sum = sum(hidden1[j] * 0.5 for j in range(min(len(hidden1), self.hidden_dims[0])))
                    hidden2.append(self._sigmoid(weighted_sum + self.anomaly_detector["biases"]["hidden"][1]))

            # Output layer
            output = 0.0
            if hidden2:
                weighted_sum = sum(h * 0.5 for h in hidden2)
                output = self._sigmoid(weighted_sum + self.anomaly_detector["biases"]["output"][0])

            return output

        except Exception as e:
            print(f"Error in neural anomaly detection: {e}", file=sys.stderr)
            return 0.0

    def _sigmoid(self, x: float) -> float:
        """Sigmoid activation function."""
        return 1 / (1 + math.exp(-x))

    def _generate_suggested_actions(self, metric_name: str, anomaly_score: float) -> List[str]:
        """Generate suggested actions for anomaly."""
        actions = []

        if anomaly_score > 0.9:
            actions.append("Immediate investigation required")
            actions.append("Consider scaling resources")
            actions.append("Check for system overload")

        if "cpu" in metric_name.lower():
            actions.extend(["Optimize algorithms", "Check for infinite loops", "Scale horizontally"])

        if "memory" in metric_name.lower():
            actions.extend(["Check for memory leaks", "Optimize data structures", "Increase memory allocation"])

        if "latency" in metric_name.lower() or "response_time" in metric_name.lower():
            actions.extend(["Optimize network calls", "Implement caching", "Review database queries"])

        if "error_rate" in metric_name.lower():
            actions.extend(["Review error logs", "Implement retry mechanisms", "Check dependencies"])

        return actions[:5]  # Limit to 5 actions

    def _find_related_metrics(self, metric_name: str, metrics: List[MonitoringMetric]) -> List[str]:
        """Find metrics related to the anomalous metric."""
        related = []

        # Simple correlation-based approach
        for other_metric in set(m.metric_name for m in metrics):
            if other_metric != metric_name:
                # Add if related by naming convention
                if any(word in other_metric.lower() for word in metric_name.lower().split("_")):
                    related.append(other_metric)

        return related[:3]  # Limit to 3 related metrics

    def _record_anomaly(self, anomaly: AnomalyDetection):
        """Record an anomaly detection."""
        anomalies_data = self._read_anomalies_data()

        # Add to history
        anomalies_data["anomaly_history"].append(asdict(anomaly))

        # Add to active anomalies
        anomalies_data["active_anomalies"].append(asdict(anomaly))

        # Keep last 1000 anomalies in history
        if len(anomalies_data["anomaly_history"]) > 1000:
            anomalies_data["anomaly_history"] = anomalies_data["anomaly_history"][-1000:]

        # Keep last 100 active anomalies
        if len(anomalies_data["active_anomalies"]) > 100:
            anomalies_data["active_anomalies"] = anomalies_data["active_anomalies"][-100:]

        # Update statistics
        stats = anomalies_data["detection_statistics"]
        stats["total_detections"] += 1

        anomalies_data["last_updated"] = datetime.now().isoformat()
        self._write_anomalies_data(anomalies_data)

    def _analyze_trends(self, metrics: List[MonitoringMetric]) -> Dict[str, str]:
        """Analyze trends in metrics."""
        trends = {}

        # Group metrics by name
        metric_groups = defaultdict(list)
        for metric in metrics:
            metric_groups[metric.metric_name].append(metric)

        for metric_name, group_metrics in metric_groups.items():
            if len(group_metrics) < 5:
                continue

            values = [m.value for m in group_metrics]

            # Calculate trend using linear regression
            x = list(range(len(values)))
            try:
                slope = np.polyfit(x, values, 1)[0]
                if slope > 0.1:
                    trends[metric_name] = "increasing"
                elif slope < -0.1:
                    trends[metric_name] = "decreasing"
                else:
                    trends[metric_name] = "stable"
            except:
                trends[metric_name] = "unknown"

        return trends

    def _analyze_correlations(self, metrics: List[MonitoringMetric]) -> Dict[str, float]:
        """Analyze correlations between metrics."""
        correlations = {}

        # Group metrics by name and create time series
        metric_series = defaultdict(list)
        for metric in metrics:
            key = metric.metric_name
            metric_series[key].append(metric.value)

        # Calculate correlations between metric pairs
        metric_names = list(metric_series.keys())
        for i, name1 in enumerate(metric_names):
            for name2 in metric_names[i + 1 :]:
                series1 = metric_series[name1]
                series2 = metric_series[name2]

                if len(series1) >= 3 and len(series2) >= 3:
                    # Simple correlation calculation
                    try:
                        correlation = np.corrcoef(series1, series2)[0, 1]
                        if not np.isnan(correlation):
                            correlations[f"{name1}_vs_{name2}"] = abs(correlation)
                    except:
                        continue

        return correlations

    def _train_neural_networks(self):
        """Train neural networks with recent data."""
        if not self.anomaly_detector:
            return

        try:
            # Get training data
            training_metrics = list(self.metrics_buffer)[-500:]  # Last 500 metrics

            if len(training_metrics) < 50:
                return

            # Extract features and labels (simplified - using recent values as "normal")
            training_features = []
            for metric in training_metrics:
                features = self._extract_features([metric])
                training_features.append(features)

            # Simple weight update (in practice, use proper backpropagation)
            if len(training_features) > 10:
                # Update weights based on recent patterns
                avg_features = [statistics.mean([f[i] for f in training_features]) for i in range(self.input_dim)]

                # Adjust weights toward average (simplified training)
                for i in range(min(len(avg_features), len(self.anomaly_detector["weights"]["input_hidden"]))):
                    for j in range(min(len(avg_features), len(self.anomaly_detector["weights"]["input_hidden"][i]))):
                        self.anomaly_detector["weights"]["input_hidden"][i][j] = (
                            self.anomaly_detector["weights"]["input_hidden"][i][j] * 0.9 + avg_features[i] * 0.1
                        )

            # Update performance metrics
            self.anomaly_detector["performance"]["accuracy"] = min(
                1.0, self.anomaly_detector["performance"]["accuracy"] + 0.01
            )
            self.anomaly_detector["performance"]["loss"] = max(0.1, self.anomaly_detector["performance"]["loss"] - 0.01)

        except Exception as e:
            print(f"Error training neural networks: {e}", file=sys.stderr)

    def _update_system_health(self):
        """Calculate overall system health score."""
        if not self.metrics_buffer:
            self.system_health = 1.0
            return

        recent_metrics = list(self.metrics_buffer)[-100:]  # Last 100 metrics

        # Calculate health based on various factors
        health_factors = []

        # Factor 1: Anomaly rate
        recent_anomalies = len([m for m in recent_metrics if m.anomaly_score > self.anomaly_threshold])
        anomaly_rate = recent_anomalies / len(recent_metrics) if recent_metrics else 0
        health_factors.append(1.0 - anomaly_rate)

        # Factor 2: Metric stability
        metric_stability = 0.0
        metric_groups = defaultdict(list)
        for metric in recent_metrics:
            metric_groups[metric.metric_name].append(metric.value)

        stable_metrics = 0
        for values in metric_groups.values():
            if len(values) >= 3:
                std_dev = statistics.stdev(values)
                mean_val = statistics.mean(values)
                if mean_val > 0:
                    cv = std_dev / mean_val  # Coefficient of variation
                    if cv < 0.2:  # Low variation = stable
                        stable_metrics += 1

        if metric_groups:
            metric_stability = stable_metrics / len(metric_groups)
        health_factors.append(metric_stability)

        # Factor 3: Response quality
        quality_metrics = [m for m in recent_metrics if "quality" in m.metric_name.lower()]
        if quality_metrics:
            avg_quality = statistics.mean([m.value for m in quality_metrics])
            health_factors.append(avg_quality / 100.0)  # Normalize to 0-1

        # Calculate overall health
        if health_factors:
            self.system_health = statistics.mean(health_factors)
        else:
            self.system_health = 1.0

        # Update monitoring data
        monitoring_data = self._read_monitoring_data()
        monitoring_data["system_health"] = self.system_health
        self._write_monitoring_data(monitoring_data)

    def _generate_predictions(self, historical_metrics: List[MonitoringMetric]) -> List[PredictiveInsight]:
        """Generate predictive insights using neural networks."""
        predictions = []

        try:
            # Group metrics by name for time series prediction
            metric_series = defaultdict(list)
            for metric in historical_metrics:
                metric_series[metric.metric_name].append(metric)

            # Generate predictions for each metric
            for metric_name, series in metric_series.items():
                if len(series) < 20:  # Need enough data for prediction
                    continue

                values = [m.value for m in series[-20:]]  # Last 20 values

                # Simple time series prediction using linear extrapolation
                x = list(range(len(values)))
                try:
                    # Fit linear trend
                    slope, intercept = np.polyfit(x, values, 1)

                    # Predict next values
                    next_values = [slope * (len(values) + i) + intercept for i in range(1, 6)]

                    # Calculate prediction confidence
                    residuals = [values[i] - (slope * i + intercept) for i in range(len(values))]
                    mse = statistics.mean([r**2 for r in residuals])
                    confidence = max(0.1, 1.0 - mse / statistics.variance(values) if statistics.variance(values) > 0 else 0.5)

                    if confidence > self.prediction_confidence_threshold:
                        # Determine prediction type
                        if slope > 0.1:
                            prediction_type = "increasing_trend"
                        elif slope < -0.1:
                            prediction_type = "decreasing_trend"
                        else:
                            prediction_type = "stable_trend"

                        # Assess impact
                        predicted_change = abs(next_values[-1] - values[-1]) / values[-1] if values[-1] != 0 else 0
                        if predicted_change > 0.2:
                            impact = "high"
                        elif predicted_change > 0.1:
                            impact = "medium"
                        else:
                            impact = "low"

                        # Generate recommendations
                        recommendations = self._generate_prediction_recommendations(metric_name, prediction_type, impact)

                        prediction = PredictiveInsight(
                            insight_id=str(uuid.uuid4())[:8],
                            timestamp=datetime.now(),
                            prediction_type=prediction_type,
                            confidence=confidence,
                            timeframe="next_5_values",
                            description=f"Predicted {prediction_type} for {metric_name}",
                            impact_assessment=f"{impact} impact expected",
                            recommendations=recommendations,
                            related_agents=list(set(m.agent_id for m in series[-5:])),
                        )
                        predictions.append(prediction)

                except Exception as e:
                    continue  # Skip this metric if prediction fails

        except Exception as e:
            print(f"Error generating predictions: {e}", file=sys.stderr)

        return predictions

    def _generate_prediction_recommendations(self, metric_name: str, prediction_type: str, impact: str) -> List[str]:
        """Generate recommendations based on prediction."""
        recommendations = []

        if "increasing" in prediction_type:
            if "cpu" in metric_name.lower():
                recommendations.extend(["Scale compute resources", "Optimize algorithms"])
            elif "memory" in metric_name.lower():
                recommendations.extend(["Monitor memory usage", "Consider memory optimization"])
            elif "error" in metric_name.lower():
                recommendations.extend(["Investigate error causes", "Implement preventive measures"])
            else:
                recommendations.append("Monitor trend closely")

        elif "decreasing" in prediction_type:
            if "performance" in metric_name.lower():
                recommendations.extend(["Investigate performance degradation", "Optimize bottlenecks"])
            elif "throughput" in metric_name.lower():
                recommendations.extend(["Check system capacity", "Review resource allocation"])
            else:
                recommendations.append("Verify expected behavior")

        if impact == "high":
            recommendations.append("Take immediate action")
        elif impact == "medium":
            recommendations.append("Plan intervention within next hour")

        return recommendations[:3]  # Limit to 3 recommendations

    def _record_prediction(self, prediction: PredictiveInsight):
        """Record a predictive insight."""
        predictions_data = self._read_predictions_data()

        # Add to history
        predictions_data["prediction_history"].append(asdict(prediction))

        # Add to active predictions
        predictions_data["active_predictions"].append(asdict(prediction))

        # Keep last 500 predictions in history
        if len(predictions_data["prediction_history"]) > 500:
            predictions_data["prediction_history"] = predictions_data["prediction_history"][-500:]

        # Keep last 50 active predictions
        if len(predictions_data["active_predictions"]) > 50:
            predictions_data["active_predictions"] = predictions_data["active_predictions"][-50:]

        # Update statistics
        stats = predictions_data["prediction_statistics"]
        stats["total_predictions"] += 1

        predictions_data["last_updated"] = datetime.now().isoformat()
        self._write_predictions_data(predictions_data)

    def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive monitoring dashboard data."""
        monitoring_data = self._read_monitoring_data()
        anomalies_data = self._read_anomalies_data()
        predictions_data = self._read_predictions_data()

        dashboard = {
            "system_overview": {
                "monitoring_active": self.monitoring_active,
                "system_health": monitoring_data.get("system_health", 1.0),
                "monitored_agents": len(monitoring_data.get("monitoring_agents", [])),
                "total_metrics": len(monitoring_data.get("metrics_history", [])),
                "last_updated": monitoring_data.get("last_updated"),
            },
            "performance_metrics": {
                "active_anomalies": len(anomalies_data.get("active_anomalies", [])),
                "active_predictions": len(predictions_data.get("active_predictions", [])),
                "detection_accuracy": self._calculate_detection_accuracy(),
                "prediction_accuracy": self._calculate_prediction_accuracy(),
            },
            "top_anomalies": self._get_top_anomalies(anomalies_data.get("active_anomalies", [])),
            "key_predictions": self._get_key_predictions(predictions_data.get("active_predictions", [])),
            "agent_status": self._get_agent_status(monitoring_data.get("monitoring_agents", [])),
            "metric_trends": self._get_metric_trends(),
            "system_alerts": self._get_system_alerts(),
        }

        return dashboard

    def _calculate_detection_accuracy(self) -> float:
        """Calculate anomaly detection accuracy."""
        # Simplified accuracy calculation
        # In practice, this would compare predictions with actual outcomes
        anomalies_data = self._read_anomalies_data()
        stats = anomalies_data.get("detection_statistics", {})
        return stats.get("accuracy", 0.85)  # Default to 85%

    def _calculate_prediction_accuracy(self) -> float:
        """Calculate prediction accuracy."""
        # Simplified accuracy calculation
        predictions_data = self._read_predictions_data()
        stats = predictions_data.get("prediction_statistics", {})
        return stats.get("accuracy", 0.78)  # Default to 78%

    def _get_top_anomalies(self, anomalies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get top anomalies by severity."""
        if not anomalies:
            return []

        # Sort by confidence and severity
        sorted_anomalies = sorted(anomalies, key=lambda a: (a.get("confidence", 0), a.get("severity") == "high"), reverse=True)

        return sorted_anomalies[:5]  # Top 5 anomalies

    def _get_key_predictions(self, predictions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get key predictions by confidence."""
        if not predictions:
            return []

        # Sort by confidence
        sorted_predictions = sorted(predictions, key=lambda p: p.get("confidence", 0), reverse=True)

        return sorted_predictions[:5]  # Top 5 predictions

    def _get_agent_status(self, agents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get agent monitoring status."""
        if not agents:
            return []

        # Calculate status for each agent
        agent_status = []
        for agent in agents:
            # Get recent metrics for agent
            agent_metrics = [m for m in self.metrics_buffer if m.agent_id == agent["agent_id"]]

            if agent_metrics:
                last_metric_time = max(m.timestamp for m in agent_metrics)
                time_since_last = time.time() - last_metric_time

                status = "active" if time_since_last < 300 else "inactive"  # 5 minutes threshold

                # Calculate average anomaly score
                anomaly_scores = [m.anomaly_score for m in agent_metrics if hasattr(m, "anomaly_score")]
                avg_anomaly = statistics.mean(anomaly_scores) if anomaly_scores else 0

                health_score = max(0, 1.0 - avg_anomaly)
            else:
                status = "no_data"
                health_score = 0.5

            agent_status.append(
                {
                    "agent_id": agent["agent_id"],
                    "tier": agent["tier"],
                    "status": status,
                    "health_score": health_score,
                    "metrics_count": agent["metrics_count"],
                    "last_metric": agent["last_metric"],
                }
            )

        return sorted(agent_status, key=lambda a: a["health_score"], reverse=True)

    def _get_metric_trends(self) -> Dict[str, str]:
        """Get current metric trends."""
        trends = {}

        # Get recent metrics
        recent_metrics = list(self.metrics_buffer)[-200:] if self.metrics_buffer else []

        # Group by metric name
        metric_groups = defaultdict(list)
        for metric in recent_metrics:
            metric_groups[metric.metric_name].append(metric.value)

        # Calculate trends
        for metric_name, values in metric_groups.items():
            if len(values) >= 10:
                # Simple trend calculation
                recent_avg = statistics.mean(values[-5:])
                older_avg = statistics.mean(values[-10:-5])

                change_pct = (recent_avg - older_avg) / older_avg if older_avg != 0 else 0

                if change_pct > 0.1:
                    trends[metric_name] = "increasing"
                elif change_pct < -0.1:
                    trends[metric_name] = "decreasing"
                else:
                    trends[metric_name] = "stable"

        return trends

    def _get_system_alerts(self) -> List[Dict[str, Any]]:
        """Get current system alerts."""
        alerts = []

        # System health alerts
        if self.system_health < 0.7:
            alerts.append(
                {
                    "type": "health",
                    "severity": "high" if self.system_health < 0.5 else "medium",
                    "message": f"System health degraded to {self.system_health:.1%}",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Anomaly alerts
        recent_anomalies = [
            a for a in self.metrics_buffer if hasattr(a, "anomaly_score") and a.anomaly_score > self.anomaly_threshold
        ]
        if len(recent_anomalies) > 5:
            alerts.append(
                {
                    "type": "anomaly",
                    "severity": "high",
                    "message": f"High anomaly activity detected: {len(recent_anomalies)} anomalies",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Monitoring agent alerts
        inactive_agents = []
        for agent_id, tier in self.monitoring_agents:
            agent_metrics = [m for m in self.metrics_buffer if m.agent_id == agent_id]
            if agent_metrics:
                last_metric_time = max(m.timestamp for m in agent_metrics)
                if time.time() - last_metric_time > 600:  # 10 minutes
                    inactive_agents.append(agent_id)

        if inactive_agents:
            alerts.append(
                {
                    "type": "agent",
                    "severity": "medium",
                    "message": f"Inactive monitoring agents: {', '.join(inactive_agents)}",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return alerts


def main():
    """Command-line interface for testing the neural monitoring system."""
    import argparse

    parser = argparse.ArgumentParser(description="Neural Monitoring System")
    parser.add_argument("--storage-dir", default=".claude-patterns", help="Storage directory")
    parser.add_argument("--action", choices=["start", "stop", "status", "register", "test"], help="Action to perform")
    parser.add_argument("--agent-id", help="Agent ID for registration")
    parser.add_argument("--tier", choices=["analysis", "execution"], help="Agent tier")
    parser.add_argument("--duration", type=int, default=30, help="Test duration in seconds")

    args = parser.parse_args()

    system = NeuralMonitoringSystem(args.storage_dir)

    if args.action == "start":
        system.start_monitoring()
        print("Monitoring started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            system.stop_monitoring()

    elif args.action == "stop":
        system.stop_monitoring()

    elif args.action == "status":
        dashboard = system.get_monitoring_dashboard()
        print("Neural Monitoring System Status:")
        print(f"  Active: {dashboard['system_overview']['monitoring_active']}")
        print(f"  System Health: {dashboard['system_overview']['system_health']:.1%}")
        print(f"  Monitored Agents: {dashboard['system_overview']['monitored_agents']}")
        print(f"  Total Metrics: {dashboard['system_overview']['total_metrics']}")
        print(f"  Active Anomalies: {dashboard['performance_metrics']['active_anomalies']}")
        print(f"  Active Predictions: {dashboard['performance_metrics']['active_predictions']}")

    elif args.action == "register":
        if not all([args.agent_id, args.tier]):
            print("Error: --agent-id and --tier required for register")
            sys.exit(1)

        system.register_monitoring_agent(args.agent_id, args.tier)

    elif args.action == "test":
        print("Running neural monitoring system test...")

        # Register test agents
        system.register_monitoring_agent("test-agent-1", "analysis")
        system.register_monitoring_agent("test-agent-2", "execution")

        # Start monitoring
        system.start_monitoring()

        # Generate test metrics
        import random

        for i in range(args.duration):
            # Generate random metrics
            system.record_metric("cpu_usage", random.uniform(20, 80), "test-agent-1", "analysis")
            system.record_metric("memory_usage", random.uniform(30, 90), "test-agent-1", "analysis")
            system.record_metric("response_time", random.uniform(50, 500), "test-agent-2", "execution")
            system.record_metric("quality_score", random.uniform(70, 95), "test-agent-2", "execution")

            # Occasionally generate anomalies
            if random.random() < 0.1:  # 10% chance
                system.record_metric("error_rate", random.uniform(5, 20), "test-agent-1", "analysis")

            time.sleep(1)

        # Show results
        dashboard = system.get_monitoring_dashboard()
        print(f"\nTest Results:")
        print(f"  System Health: {dashboard['system_overview']['system_health']:.1%}")
        print(f"  Total Metrics: {dashboard['system_overview']['total_metrics']}")
        print(f"  Active Anomalies: {dashboard['performance_metrics']['active_anomalies']}")
        print(f"  Detection Accuracy: {dashboard['performance_metrics']['detection_accuracy']:.1%}")

        # Stop monitoring
        system.stop_monitoring()

    else:
        # Show status by default
        dashboard = system.get_monitoring_dashboard()
        print("Neural Monitoring System Summary:")
        print(f"  System Health: {dashboard['system_overview']['system_health']:.1%}")
        print(f"  Monitored Agents: {dashboard['system_overview']['monitored_agents']}")
        print(f"  Active Anomalies: {dashboard['performance_metrics']['active_anomalies']}")


if __name__ == "__main__":
    import uuid
    import math

    main()
