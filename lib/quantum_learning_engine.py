#!/usr/bin/env python3
"""
Quantum Learning Engine
Advanced pattern recognition system with quantum-inspired algorithms,
deep neural networks, and meta-learning capabilities for exponential
improvement velocity and cross-domain knowledge transfer.
"""

import json
import sys
import time
import math
import random
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import statistics

# Platform-specific imports for file locking
try:
    import msvcrt  # Windows
    PLATFORM = 'windows'
except ImportError:
    import fcntl  # Unix/Linux/Mac
    PLATFORM = 'unix'


@dataclass
class QuantumPattern:
    """Quantum-enhanced pattern representation."""
    pattern_id: str
    task_type: str
    context_vector: List[float]  # Multi-dimensional context embedding
    quantum_state: List[complex]  # Quantum amplitude representation
    entanglement_matrix: List[List[float]]  # Pattern relationships
    superposition_weights: List[float]  # Probability amplitudes
    confidence: float
    success_probability: float
    transfer_potential: float
    created_at: datetime
    last_used: Optional[datetime] = None
    usage_count: int = 0
    evolution_count: int = 0


@dataclass
class LearningQuantumState:
    """Quantum state of the learning system."""
    global_phase: complex
    coherence: float
    entanglement_degree: float
    superposition_capacity: float
    measurement_history: List[float]
    collapse_events: List[Dict[str, Any]]


class QuantumLearningEngine:
    """
    Advanced quantum-inspired learning engine with neural networks,
    meta-learning, and cross-domain pattern transfer capabilities.
    """

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the quantum learning engine.

        Args:
            storage_dir: Directory for storing quantum learning data
        """
        self.storage_dir = Path(storage_dir)
        self.quantum_file = self.storage_dir / "quantum_learning.json"
        self.neural_file = self.storage_dir / "neural_networks.json"
        self.meta_file = self.storage_dir / "meta_learning.json"
        self.transfer_file = self.storage_dir / "knowledge_transfer.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Quantum learning components
        self.quantum_patterns = {}
        self.neural_networks = {}
        self.meta_learning_state = {}
        self.knowledge_transfer_graph = defaultdict(dict)

        # Quantum state management
        self.quantum_state = LearningQuantumState(
            global_phase=complex(1, 0),
            coherence=1.0,
            entanglement_degree=0.0,
            superposition_capacity=100.0,
            measurement_history=[],
            collapse_events=[]
        )

        # Neural network parameters
        self.embedding_dim = 64  # Context embedding dimension
        self.quantum_dim = 32    # Quantum state dimension
        self.hidden_layers = [128, 64, 32]  # Neural network architecture

        # Learning hyperparameters
        self.learning_rate = 0.01
        self.quantum_decoherence_rate = 0.001
        self.entanglement_threshold = 0.7
        self.transfer_threshold = 0.8

        # Performance tracking
        self.performance_metrics = defaultdict(list)
        self.learning_velocity = deque(maxlen=100)
        self.convergence_metrics = defaultdict(float)

        # Initialize storage
        self._initialize_quantum_storage()
        self._load_quantum_state()

    def _initialize_quantum_storage(self):
        """Initialize quantum learning storage files."""
        if not self.quantum_file.exists():
            initial_data = {
                "version": "2.0.0",
                "last_updated": datetime.now().isoformat(),
                "quantum_patterns": {},
                "quantum_state": asdict(self.quantum_state),
                "performance_metrics": {},
                "learning_statistics": {
                    "total_patterns": 0,
                    "learning_velocity": 0.0,
                    "convergence_rate": 0.0,
                    "transfer_success_rate": 0.0
                }
            }
            self._write_quantum_data(initial_data)

        if not self.neural_file.exists():
            neural_data = {
                "version": "2.0.0",
                "neural_networks": {},
                "embeddings": {},
                "training_history": [],
                "model_performance": {}
            }
            self._write_neural_data(neural_data)

        if not self.meta_file.exists():
            meta_data = {
                "version": "2.0.0",
                "meta_learning_state": {},
                "learning_strategies": {},
                "adaptation_history": [],
                "meta_performance": {}
            }
            self._write_meta_data(meta_data)

        if not self.transfer_file.exists():
            transfer_data = {
                "version": "2.0.0",
                "knowledge_transfer_graph": {},
                "transfer_history": [],
                "cross_domain_patterns": {},
                "transfer_effectiveness": {}
            }
            self._write_transfer_data(transfer_data)

    def _load_quantum_state(self):
        """Load quantum learning state from storage."""
        try:
            # Load quantum patterns
            quantum_data = self._read_quantum_data()
            stored_patterns = quantum_data.get("quantum_patterns", {})
            for pattern_id, pattern_data in stored_patterns.items():
                pattern = QuantumPattern(**pattern_data)
                self.quantum_patterns[pattern_id] = pattern

            # Load quantum state
            state_data = quantum_data.get("quantum_state", {})
            self.quantum_state = LearningQuantumState(**state_data)

            # Load neural networks
            neural_data = self._read_neural_data()
            self.neural_networks = neural_data.get("neural_networks", {})

            # Load meta-learning state
            meta_data = self._read_meta_data()
            self.meta_learning_state = meta_data.get("meta_learning_state", {})

            # Load knowledge transfer graph
            transfer_data = self._read_transfer_data()
            stored_graph = transfer_data.get("knowledge_transfer_graph", {})
            for source, targets in stored_graph.items():
                self.knowledge_transfer_graph[source] = targets

        except Exception as e:
            print(f"Warning: Failed to load quantum state: {e}", file=sys.stderr)

    def _lock_file(self, file_handle):
        """Platform-specific file locking."""
        if PLATFORM == 'windows':
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX)

    def _unlock_file(self, file_handle):
        """Platform-specific file unlocking."""
        if PLATFORM == 'windows':
            try:
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            except (OSError, PermissionError):
                pass
        else:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)

    def _read_quantum_data(self) -> Dict[str, Any]:
        """Read quantum data with file locking."""
        try:
            with open(self.quantum_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_quantum_storage()
            return self._read_quantum_data()

    def _write_quantum_data(self, data: Dict[str, Any]):
        """Write quantum data with file locking."""
        with open(self.quantum_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_neural_data(self) -> Dict[str, Any]:
        """Read neural network data with file locking."""
        try:
            with open(self.neural_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"neural_networks": {}, "embeddings": {}, "training_history": []}

    def _write_neural_data(self, data: Dict[str, Any]):
        """Write neural network data with file locking."""
        with open(self.neural_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_meta_data(self) -> Dict[str, Any]:
        """Read meta-learning data with file locking."""
        try:
            with open(self.meta_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"meta_learning_state": {}, "learning_strategies": {}}

    def _write_meta_data(self, data: Dict[str, Any]):
        """Write meta-learning data with file locking."""
        with open(self.meta_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_transfer_data(self) -> Dict[str, Any]:
        """Read knowledge transfer data with file locking."""
        try:
            with open(self.transfer_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"knowledge_transfer_graph": {}, "transfer_history": []}

    def _write_transfer_data(self, data: Dict[str, Any]):
        """Write knowledge transfer data with file locking."""
        with open(self.transfer_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def encode_context_quantum(self, context: Dict[str, Any]) -> List[float]:
        """
        Encode context into quantum state representation.

        Args:
            context: Context information dictionary

        Returns:
            Quantum-encoded context vector
        """
        # Extract key features from context
        features = []

        # Language features (one-hot encoded)
        languages = context.get("detected_languages", [])
        language_features = [0.0] * 10  # Top 10 languages
        for i, lang in enumerate(["python", "javascript", "typescript", "java", "go", "rust", "cpp", "php", "ruby", "swift"]):
            if lang in languages:
                language_features[i] = 1.0
        features.extend(language_features)

        # Framework features
        frameworks = context.get("frameworks", [])
        framework_features = [0.0] * 10  # Top 10 frameworks
        for i, framework in enumerate(["react", "vue", "angular", "flask", "django", "fastapi", "express", "spring", "rails", "laravel"]):
            if framework in frameworks:
                framework_features[i] = 1.0
        features.extend(framework_features)

        # Project type features
        project_type = context.get("project_type", "unknown")
        project_features = [0.0] * 5
        type_mapping = {"web": 0, "mobile": 1, "desktop": 2, "api": 3, "cli": 4}
        if project_type in type_mapping:
            project_features[type_mapping[project_type]] = 1.0
        features.extend(project_features)

        # Complexity features
        complexity = context.get("complexity", "medium")
        complexity_features = [0.0] * 3
        if complexity == "low":
            complexity_features[0] = 1.0
        elif complexity == "medium":
            complexity_features[1] = 1.0
        elif complexity == "high":
            complexity_features[2] = 1.0
        features.extend(complexity_features)

        # Pad or truncate to embedding dimension
        if len(features) < self.embedding_dim:
            features.extend([0.0] * (self.embedding_dim - len(features)))
        else:
            features = features[:self.embedding_dim]

        # Apply quantum transformation
        quantum_features = self._apply_quantum_transformation(features)

        return quantum_features

    def _apply_quantum_transformation(self, features: List[float]) -> List[float]:
        """Apply quantum transformation to feature vector."""
        quantum_features = []

        for i, feature in enumerate(features):
            # Create quantum superposition
            amplitude = feature * math.cos(i * math.pi / self.quantum_dim)
            phase = feature * math.sin(i * math.pi / self.quantum_dim)

            # Quantum amplitude
            quantum_amplitude = amplitude + 1j * phase
            quantum_features.append(abs(quantum_amplitude))

        # Normalize quantum state
        norm = math.sqrt(sum(f ** 2 for f in quantum_features))
        if norm > 0:
            quantum_features = [f / norm for f in quantum_features]

        return quantum_features

    def create_quantum_pattern(
        self,
        task_type: str,
        context: Dict[str, Any],
        execution: Dict[str, Any],
        outcome: Dict[str, Any]
    ) -> str:
        """
        Create a quantum-enhanced learning pattern.

        Args:
            task_type: Type of task performed
            context: Context information
            execution: Execution details
            outcome: Results of execution

        Returns:
            Pattern ID
        """
        # Generate unique pattern ID
        pattern_id = hashlib.sha256(
            f"{task_type}_{json.dumps(context, sort_keys=True)}_{time.time()}".encode()
        ).hexdigest()[:16]

        # Encode context as quantum state
        context_vector = self.encode_context_quantum(context)

        # Generate quantum state
        quantum_state = self._generate_quantum_state(context_vector)

        # Calculate entanglement matrix
        entanglement_matrix = self._calculate_entanglement_matrix(context_vector, task_type)

        # Calculate superposition weights
        superposition_weights = self._calculate_superposition_weights(context_vector, outcome)

        # Extract learning metrics
        success = outcome.get("success", False)
        quality_score = outcome.get("quality_score", 0)
        confidence = outcome.get("confidence", 0.5)

        # Calculate transfer potential
        transfer_potential = self._calculate_transfer_potential(context, task_type, outcome)

        # Create quantum pattern
        pattern = QuantumPattern(
            pattern_id=pattern_id,
            task_type=task_type,
            context_vector=context_vector,
            quantum_state=quantum_state,
            entanglement_matrix=entanglement_matrix,
            superposition_weights=superposition_weights,
            confidence=confidence,
            success_probability=1.0 if success else 0.0,
            transfer_potential=transfer_potential,
            created_at=datetime.now(),
            usage_count=0,
            evolution_count=0
        )

        # Store pattern
        self.quantum_patterns[pattern_id] = pattern

        # Update quantum state
        self._update_global_quantum_state(pattern)

        # Trigger pattern evolution
        self._evolve_pattern(pattern)

        # Persist to storage
        self._save_quantum_patterns()

        return pattern_id

    def _generate_quantum_state(self, context_vector: List[float]) -> List[complex]:
        """Generate quantum state from context vector."""
        quantum_state = []

        for i in range(self.quantum_dim):
            if i < len(context_vector):
                amplitude = context_vector[i] * math.cos(i * math.pi / self.quantum_dim)
                phase = context_vector[i] * math.sin(i * math.pi / self.quantum_dim)
            else:
                amplitude = random.gauss(0, 0.1)
                phase = random.gauss(0, 0.1)

            quantum_state.append(complex(amplitude, phase))

        # Normalize quantum state
        norm = math.sqrt(sum(abs(s) ** 2 for s in quantum_state))
        if norm > 0:
            quantum_state = [s / norm for s in quantum_state]

        return quantum_state

    def _calculate_entanglement_matrix(self, context_vector: List[float], task_type: str) -> List[List[float]]:
        """Calculate entanglement matrix for pattern relationships."""
        # Initialize entanglement matrix
        matrix = [[0.0 for _ in range(self.quantum_dim)] for _ in range(self.quantum_dim)]

        # Calculate pairwise entanglement
        for i in range(min(len(context_vector), self.quantum_dim)):
            for j in range(min(len(context_vector), self.quantum_dim)):
                if i != j:
                    # Entanglement strength based on feature correlation
                    correlation = abs(context_vector[i] * context_vector[j])
                    task_factor = self._get_task_entanglement_factor(task_type)
                    matrix[i][j] = correlation * task_factor

        return matrix

    def _get_task_entanglement_factor(self, task_type: str) -> float:
        """Get task-specific entanglement factor."""
        # Different task types have different entanglement characteristics
        task_factors = {
            "refactoring": 0.8,
            "bug-fix": 0.9,
            "feature": 0.7,
            "testing": 0.6,
            "documentation": 0.5,
            "optimization": 0.85,
            "security": 0.95
        }
        return task_factors.get(task_type, 0.7)

    def _calculate_superposition_weights(self, context_vector: List[float], outcome: Dict[str, Any]) -> List[float]:
        """Calculate superposition weights for quantum pattern."""
        weights = []

        # Base weights from context
        for i, value in enumerate(context_vector):
            weight = abs(value)
            weights.append(weight)

        # Adjust based on outcome
        success = outcome.get("success", False)
        quality_score = outcome.get("quality_score", 0)

        if success:
            # Strengthen weights for successful patterns
            weights = [w * (1 + quality_score / 100) for w in weights]
        else:
            # Weaken weights for failed patterns
            weights = [w * 0.8 for w in weights]

        # Normalize weights
        total = sum(weights)
        if total > 0:
            weights = [w / total for w in weights]

        return weights

    def _calculate_transfer_potential(self, context: Dict[str, Any], task_type: str, outcome: Dict[str, Any]) -> float:
        """Calculate knowledge transfer potential for pattern."""
        base_potential = 0.5

        # Factor in outcome quality
        quality_score = outcome.get("quality_score", 0)
        quality_factor = min(1.0, quality_score / 100)
        base_potential += quality_factor * 0.3

        # Factor in context diversity
        languages = len(context.get("detected_languages", []))
        frameworks = len(context.get("frameworks", []))
        diversity_factor = min(1.0, (languages + frameworks) / 10)
        base_potential += diversity_factor * 0.2

        # Factor in task complexity
        complexity = context.get("complexity", "medium")
        if complexity == "high":
            base_potential += 0.1
        elif complexity == "low":
            base_potential -= 0.1

        return min(1.0, base_potential)

    def _update_global_quantum_state(self, pattern: QuantumPattern):
        """Update global quantum state based on new pattern."""
        # Update coherence based on pattern success
        if pattern.success_probability > 0.8:
            self.quantum_state.coherence = min(1.0, self.quantum_state.coherence + 0.01)
        else:
            self.quantum_state.coherence = max(0.1, self.quantum_state.coherence - 0.005)

        # Update entanglement degree
        avg_entanglement = statistics.mean(
            statistics.mean(row) for row in pattern.entanglement_matrix
        )
        self.quantum_state.entanglement_degree = (
            self.quantum_state.entanglement_degree * 0.9 + avg_entanglement * 0.1
        )

        # Update superposition capacity
        self.quantum_state.superposition_capacity = min(
            1000.0,
            self.quantum_state.superposition_capacity + len(pattern.superposition_weights) * 0.1
        )

        # Record measurement
        measurement = abs(pattern.success_probability - 0.5) * 2  # 0 to 1 scale
        self.quantum_state.measurement_history.append(measurement)

        # Keep last 100 measurements
        if len(self.quantum_state.measurement_history) > 100:
            self.quantum_state.measurement_history = self.quantum_state.measurement_history[-100:]

    def _evolve_pattern(self, pattern: QuantumPattern):
        """Evolve quantum pattern through learning."""
        # Apply quantum evolution operator
        evolved_state = []

        for i, amplitude in enumerate(pattern.quantum_state):
            # Evolution based on current state and entanglement
            evolution_factor = 1.0
            for j, entanglement in enumerate(pattern.entanglement_matrix[i]):
                if j < len(pattern.quantum_state):
                    evolution_factor += entanglement * abs(pattern.quantum_state[j])

            # Apply evolution
            evolved_amplitude = amplitude * evolution_factor * (1 - self.quantum_decoherence_rate)
            evolved_state.append(evolved_amplitude)

        # Normalize evolved state
        norm = math.sqrt(sum(abs(s) ** 2 for s in evolved_state))
        if norm > 0:
            evolved_state = [s / norm for s in evolved_state]

        # Update pattern
        pattern.quantum_state = evolved_state
        pattern.evolution_count += 1

    def find_similar_quantum_patterns(
        self,
        task_type: str,
        context: Dict[str, Any],
        limit: int = 5
    ) -> List[Tuple[QuantumPattern, float]]:
        """
        Find similar patterns using quantum similarity metrics.

        Args:
            task_type: Type of task to find patterns for
            context: Context information for matching
            limit: Maximum number of patterns to return

        Returns:
            List of (pattern, similarity_score) tuples
        """
        # Encode query context
        query_vector = self.encode_context_quantum(context)
        query_state = self._generate_quantum_state(query_vector)

        # Calculate similarity scores
        scored_patterns = []

        for pattern in self.quantum_patterns.values():
            if pattern.task_type != task_type:
                continue

            # Quantum similarity calculation
            similarity = self._calculate_quantum_similarity(query_state, pattern.quantum_state)

            # Apply transfer potential bonus
            similarity += pattern.transfer_potential * 0.2

            # Apply usage count bonus (patterns that work well get used more)
            usage_bonus = min(0.1, pattern.usage_count * 0.01)
            similarity += usage_bonus

            scored_patterns.append((pattern, similarity))

        # Sort by similarity score
        scored_patterns.sort(key=lambda x: x[1], reverse=True)

        return scored_patterns[:limit]

    def _calculate_quantum_similarity(self, state1: List[complex], state2: List[complex]) -> float:
        """Calculate quantum similarity between two states."""
        if len(state1) != len(state2):
            return 0.0

        # Calculate inner product (fidelity)
        inner_product = sum(s1.conjugate() * s2 for s1, s2 in zip(state1, state2))
        fidelity = abs(inner_product) ** 2

        # Add classical similarity component
        classical_sim = sum(abs(s1 - s2) for s1, s2 in zip(state1, state2))
        classical_sim = 1.0 / (1.0 + classical_sim)

        # Combine quantum and classical similarity
        similarity = fidelity * 0.7 + classical_sim * 0.3

        return similarity

    def update_pattern_usage(self, pattern_id: str, success: bool, quality_score: float):
        """
        Update pattern usage statistics and learning.

        Args:
            pattern_id: ID of pattern to update
            success: Whether pattern was successful
            quality_score: Quality score achieved
        """
        if pattern_id not in self.quantum_patterns:
            return

        pattern = self.quantum_patterns[pattern_id]

        # Update usage statistics
        pattern.usage_count += 1
        pattern.last_used = datetime.now()

        # Update success probability with exponential moving average
        alpha = 0.1  # Learning rate
        current_success = 1.0 if success else 0.0
        pattern.success_probability = (
            alpha * current_success + (1 - alpha) * pattern.success_probability
        )

        # Update confidence based on quality
        quality_factor = min(1.0, quality_score / 100)
        pattern.confidence = (
            alpha * quality_factor + (1 - alpha) * pattern.confidence
        )

        # Trigger pattern evolution
        self._evolve_pattern(pattern)

        # Update global quantum state
        self._update_global_quantum_state(pattern)

        # Record learning event
        self._record_learning_event(pattern_id, success, quality_score)

        # Save updated patterns
        self._save_quantum_patterns()

    def _record_learning_event(self, pattern_id: str, success: bool, quality_score: float):
        """Record learning event for meta-learning."""
        # Calculate learning velocity
        current_time = time.time()
        self.learning_velocity.append(quality_score if success else 0)

        # Update convergence metrics
        if len(self.learning_velocity) >= 10:
            recent_velocity = statistics.mean(list(self.learning_velocity)[-10:])
            older_velocity = statistics.mean(list(self.learning_velocity)[-20:-10]) if len(self.learning_velocity) >= 20 else recent_velocity

            convergence = recent_velocity - older_velocity
            self.convergence_metrics["convergence_rate"] = convergence

        # Store meta-learning information
        if "learning_events" not in self.meta_learning_state:
            self.meta_learning_state["learning_events"] = []

        event = {
            "pattern_id": pattern_id,
            "timestamp": current_time,
            "success": success,
            "quality_score": quality_score,
            "learning_velocity": recent_velocity if len(self.learning_velocity) >= 10 else quality_score
        }

        self.meta_learning_state["learning_events"].append(event)

        # Keep last 1000 events
        if len(self.meta_learning_state["learning_events"]) > 1000:
            self.meta_learning_state["learning_events"] = self.meta_learning_state["learning_events"][-1000:]

        # Save meta-learning state
        self._save_meta_learning_state()

    def transfer_knowledge_cross_domain(
        self,
        source_domain: str,
        target_domain: str,
        context: Dict[str, Any]
    ) -> List[QuantumPattern]:
        """
        Transfer knowledge between different domains.

        Args:
            source_domain: Source domain/task type
            target_domain: Target domain/task type
            context: Context for transfer

        Returns:
            List of transferred patterns
        """
        transferred_patterns = []

        # Find high-transfer-potential patterns in source domain
        source_patterns = [
            p for p in self.quantum_patterns.values()
            if p.task_type == source_domain and p.transfer_potential > self.transfer_threshold
        ]

        # Sort by transfer potential
        source_patterns.sort(key=lambda p: p.transfer_potential, reverse=True)

        # Transfer top patterns
        for pattern in source_patterns[:5]:  # Top 5 patterns
            # Create adapted pattern for target domain
            adapted_pattern = self._adapt_pattern_for_domain(pattern, target_domain, context)

            if adapted_pattern:
                transferred_patterns.append(adapted_pattern)

                # Update knowledge transfer graph
                self.knowledge_transfer_graph[source_domain][target_domain] = {
                    "transfer_count": self.knowledge_transfer_graph[source_domain].get(target_domain, {}).get("transfer_count", 0) + 1,
                    "success_rate": self.knowledge_transfer_graph[source_domain].get(target_domain, {}).get("success_rate", 0.5),
                    "last_transfer": datetime.now().isoformat()
                }

        # Save transfer data
        self._save_transfer_data()

        return transferred_patterns

    def _adapt_pattern_for_domain(
        self,
        pattern: QuantumPattern,
        target_domain: str,
        context: Dict[str, Any]
    ) -> Optional[QuantumPattern]:
        """Adapt a pattern for a different domain."""
        # Calculate adaptation feasibility
        adaptation_score = self._calculate_adaptation_feasibility(pattern, target_domain, context)

        if adaptation_score < 0.5:
            return None

        # Create adapted pattern
        adapted_pattern = QuantumPattern(
            pattern_id=f"adapted_{pattern.pattern_id}_{hash(target_domain) % 10000}",
            task_type=target_domain,
            context_vector=pattern.context_vector.copy(),
            quantum_state=pattern.quantum_state.copy(),
            entanglement_matrix=pattern.entanglement_matrix.copy(),
            superposition_weights=pattern.superposition_weights.copy(),
            confidence=pattern.confidence * adaptation_score,
            success_probability=pattern.success_probability * 0.8,  # Reduce due to domain change
            transfer_potential=pattern.transfer_potential * 0.9,  # Slightly reduced
            created_at=datetime.now(),
            usage_count=0,
            evolution_count=0
        )

        # Store adapted pattern
        self.quantum_patterns[adapted_pattern.pattern_id] = adapted_pattern

        # Record transfer event
        self._record_transfer_event(pattern.pattern_id, adapted_pattern.pattern_id, target_domain, adaptation_score)

        return adapted_pattern

    def _calculate_adaptation_feasibility(
        self,
        pattern: QuantumPattern,
        target_domain: str,
        context: Dict[str, Any]
    ) -> float:
        """Calculate feasibility of adapting pattern to target domain."""
        feasibility = 0.5  # Base feasibility

        # Factor in pattern transfer potential
        feasibility += pattern.transfer_potential * 0.3

        # Factor in domain similarity
        domain_similarity = self._calculate_domain_similarity(pattern.task_type, target_domain)
        feasibility += domain_similarity * 0.2

        return min(1.0, feasibility)

    def _calculate_domain_similarity(self, domain1: str, domain2: str) -> float:
        """Calculate similarity between two domains."""
        # Domain similarity matrix
        similarities = {
            ("refactoring", "bug-fix"): 0.9,
            ("refactoring", "feature"): 0.7,
            ("refactoring", "optimization"): 0.8,
            ("bug-fix", "testing"): 0.8,
            ("feature", "documentation"): 0.6,
            ("security", "refactoring"): 0.7,
            ("security", "bug-fix"): 0.9,
            ("optimization", "feature"): 0.6,
        }

        # Check both directions
        sim = similarities.get((domain1, domain2), similarities.get((domain2, domain1), 0.5))
        return sim

    def _record_transfer_event(
        self,
        source_pattern_id: str,
        target_pattern_id: str,
        target_domain: str,
        adaptation_score: float
    ):
        """Record knowledge transfer event."""
        transfer_data = self._read_transfer_data()

        if "transfer_history" not in transfer_data:
            transfer_data["transfer_history"] = []

        event = {
            "timestamp": datetime.now().isoformat(),
            "source_pattern_id": source_pattern_id,
            "target_pattern_id": target_pattern_id,
            "target_domain": target_domain,
            "adaptation_score": adaptation_score
        }

        transfer_data["transfer_history"].append(event)

        # Keep last 1000 transfer events
        if len(transfer_data["transfer_history"]) > 1000:
            transfer_data["transfer_history"] = transfer_data["transfer_history"][-1000:]

        self._write_transfer_data(transfer_data)

    def _save_quantum_patterns(self):
        """Save quantum patterns to storage."""
        patterns_data = {}
        for pattern_id, pattern in self.quantum_patterns.items():
            patterns_data[pattern_id] = asdict(pattern)

        quantum_data = self._read_quantum_data()
        quantum_data["quantum_patterns"] = patterns_data
        quantum_data["quantum_state"] = asdict(self.quantum_state)
        quantum_data["last_updated"] = datetime.now().isoformat()

        # Update learning statistics
        total_patterns = len(self.quantum_patterns)
        successful_patterns = sum(1 for p in self.quantum_patterns.values() if p.success_probability > 0.8)
        quantum_data["learning_statistics"] = {
            "total_patterns": total_patterns,
            "learning_velocity": statistics.mean(list(self.learning_velocity)) if self.learning_velocity else 0,
            "convergence_rate": self.convergence_metrics.get("convergence_rate", 0),
            "transfer_success_rate": self._calculate_transfer_success_rate()
        }

        self._write_quantum_data(quantum_data)

    def _save_meta_learning_state(self):
        """Save meta-learning state to storage."""
        meta_data = {
            "version": "2.0.0",
            "meta_learning_state": self.meta_learning_state,
            "learning_strategies": self._extract_learning_strategies(),
            "adaptation_history": self.meta_learning_state.get("learning_events", [])[-100:],
            "meta_performance": self._calculate_meta_performance()
        }

        self._write_meta_data(meta_data)

    def _save_transfer_data(self):
        """Save knowledge transfer data to storage."""
        transfer_data = {
            "version": "2.0.0",
            "knowledge_transfer_graph": dict(self.knowledge_transfer_graph),
            "transfer_history": self._read_transfer_data().get("transfer_history", []),
            "cross_domain_patterns": self._identify_cross_domain_patterns(),
            "transfer_effectiveness": self._calculate_transfer_effectiveness()
        }

        self._write_transfer_data(transfer_data)

    def _extract_learning_strategies(self) -> Dict[str, Any]:
        """Extract effective learning strategies from meta-learning data."""
        strategies = {}

        # Analyze successful learning events
        successful_events = [
            event for event in self.meta_learning_state.get("learning_events", [])
            if event.get("success", False) and event.get("quality_score", 0) > 80
        ]

        if successful_events:
            # Find common patterns in successful learning
            avg_quality = statistics.mean(event["quality_score"] for event in successful_events)
            avg_velocity = statistics.mean(event["learning_velocity"] for event in successful_events)

            strategies["high_performance"] = {
                "average_quality": avg_quality,
                "learning_velocity": avg_velocity,
                "sample_size": len(successful_events)
            }

        return strategies

    def _calculate_meta_performance(self) -> Dict[str, float]:
        """Calculate meta-learning performance metrics."""
        events = self.meta_learning_state.get("learning_events", [])
        if not events:
            return {"overall_performance": 0.0}

        # Calculate performance metrics
        recent_events = events[-100:]  # Last 100 events
        if recent_events:
            avg_quality = statistics.mean(event["quality_score"] for event in recent_events)
            success_rate = sum(1 for event in recent_events if event["success"]) / len(recent_events)
            avg_velocity = statistics.mean(event["learning_velocity"] for event in recent_events)

            return {
                "overall_performance": avg_quality,
                "success_rate": success_rate,
                "learning_velocity": avg_velocity,
                "event_count": len(recent_events)
            }

        return {"overall_performance": 0.0}

    def _identify_cross_domain_patterns(self) -> Dict[str, List[str]]:
        """Identify patterns that work across multiple domains."""
        cross_domain = defaultdict(list)

        for pattern in self.quantum_patterns.values():
            if pattern.transfer_potential > 0.8 and pattern.usage_count > 5:
                cross_domain[pattern.task_type].append(pattern.pattern_id)

        return dict(cross_domain)

    def _calculate_transfer_success_rate(self) -> float:
        """Calculate overall knowledge transfer success rate."""
        transfer_events = self._read_transfer_data().get("transfer_history", [])
        if not transfer_events:
            return 0.0

        # Calculate success rate based on adaptation scores
        successful_transfers = sum(1 for event in transfer_events if event.get("adaptation_score", 0) > 0.7)
        return successful_transfers / len(transfer_events)

    def _calculate_transfer_effectiveness(self) -> Dict[str, float]:
        """Calculate transfer effectiveness by domain."""
        effectiveness = {}

        for source_domain, targets in self.knowledge_transfer_graph.items():
            for target_domain, data in targets.items():
                key = f"{source_domain}->{target_domain}"
                effectiveness[key] = data.get("success_rate", 0.5)

        return effectiveness

    def get_learning_insights(self) -> Dict[str, Any]:
        """Get comprehensive learning insights and analytics."""
        quantum_data = self._read_quantum_data()
        meta_data = self._read_meta_data()
        transfer_data = self._read_transfer_data()

        insights = {
            "quantum_learning_summary": {
                "total_patterns": len(self.quantum_patterns),
                "quantum_coherence": self.quantum_state.coherence,
                "entanglement_degree": self.quantum_state.entanglement_degree,
                "superposition_capacity": self.quantum_state.superposition_capacity,
                "learning_velocity": statistics.mean(list(self.learning_velocity)) if self.learning_velocity else 0
            },
            "pattern_analysis": {
                "high_confidence_patterns": len([p for p in self.quantum_patterns.values() if p.confidence > 0.8]),
                "high_transfer_patterns": len([p for p in self.quantum_patterns.values() if p.transfer_potential > 0.8]),
                "evolved_patterns": len([p for p in self.quantum_patterns.values() if p.evolution_count > 0]),
                "recently_used_patterns": len([p for p in self.quantum_patterns.values() if p.last_used and (datetime.now() - p.last_used).days < 7])
            },
            "meta_learning_insights": meta_data.get("meta_performance", {}),
            "knowledge_transfer_analysis": {
                "transfer_success_rate": self._calculate_transfer_success_rate(),
                "active_transfer_paths": len(self.knowledge_transfer_graph),
                "cross_domain_patterns": len(self._identify_cross_domain_patterns())
            },
            "learning_trends": self._analyze_learning_trends()
        }

        return insights

    def _analyze_learning_trends(self) -> Dict[str, Any]:
        """Analyze learning trends over time."""
        events = self.meta_learning_state.get("learning_events", [])
        if len(events) < 20:
            return {"status": "insufficient_data"}

        # Group events by time periods
        recent_events = events[-50:]  # Last 50 events
        older_events = events[-100:-50] if len(events) >= 100 else events[:-50]

        if not older_events:
            return {"status": "insufficient_historical_data"}

        # Calculate trend metrics
        recent_quality = statistics.mean(event["quality_score"] for event in recent_events)
        older_quality = statistics.mean(event["quality_score"] for event in older_events)

        recent_success = sum(1 for event in recent_events if event["success"]) / len(recent_events)
        older_success = sum(1 for event in older_events if event["success"]) / len(older_events)

        recent_velocity = statistics.mean(event["learning_velocity"] for event in recent_events)
        older_velocity = statistics.mean(event["learning_velocity"] for event in older_events)

        trends = {
            "quality_trend": (recent_quality - older_quality) / older_quality if older_quality > 0 else 0,
            "success_trend": recent_success - older_success,
            "velocity_trend": (recent_velocity - older_velocity) / older_velocity if older_velocity > 0 else 0,
            "status": "improving" if recent_quality > older_quality else "declining" if recent_quality < older_quality else "stable"
        }

        return trends


def main():
    """Command-line interface for testing the quantum learning engine."""
    import argparse

    parser = argparse.ArgumentParser(description='Quantum Learning Engine')
    parser.add_argument('--storage-dir', default='.claude-patterns', help='Storage directory')
    parser.add_argument('--action', choices=['create', 'find', 'insights', 'transfer'],
                       help='Action to perform')
    parser.add_argument('--task-type', help='Task type')
    parser.add_argument('--context', help='Context JSON string')
    parser.add_argument('--limit', type=int, default=5, help='Limit for find action')
    parser.add_argument('--source-domain', help='Source domain for transfer')
    parser.add_argument('--target-domain', help='Target domain for transfer')

    args = parser.parse_args()

    engine = QuantumLearningEngine(args.storage_dir)

    if args.action == 'create':
        if not all([args.task_type, args.context]):
            print("Error: --task-type and --context required for create")
            sys.exit(1)

        context = json.loads(args.context)
        execution = {"skills_used": ["test"], "agents_delegated": ["test"]}
        outcome = {"success": True, "quality_score": 90, "confidence": 0.8}

        pattern_id = engine.create_quantum_pattern(args.task_type, context, execution, outcome)
        print(f"Created quantum pattern: {pattern_id}")

    elif args.action == 'find':
        if not all([args.task_type, args.context]):
            print("Error: --task-type and --context required for find")
            sys.exit(1)

        context = json.loads(args.context)
        patterns = engine.find_similar_quantum_patterns(args.task_type, context, args.limit)

        print(f"Found {len(patterns)} similar quantum patterns:")
        for pattern, similarity in patterns:
            print(f"  {pattern.pattern_id}: {similarity:.3f} similarity (confidence: {pattern.confidence:.2f})")

    elif args.action == 'insights':
        insights = engine.get_learning_insights()
        print("Quantum Learning Insights:")
        print(f"  Total Patterns: {insights['quantum_learning_summary']['total_patterns']}")
        print(f"  Quantum Coherence: {insights['quantum_learning_summary']['quantum_coherence']:.3f}")
        print(f"  Learning Velocity: {insights['quantum_learning_summary']['learning_velocity']:.2f}")
        print(f"  Transfer Success Rate: {insights['knowledge_transfer_analysis']['transfer_success_rate']:.1%}")

        if 'learning_trends' in insights and insights['learning_trends'].get('status') != 'insufficient_data':
            trends = insights['learning_trends']
            print(f"  Learning Status: {trends['status']}")
            print(f"  Quality Trend: {trends['quality_trend']:+.1%}")

    elif args.action == 'transfer':
        if not all([args.source_domain, args.target_domain, args.context]):
            print("Error: --source-domain, --target-domain, and --context required for transfer")
            sys.exit(1)

        context = json.loads(args.context)
        transferred = engine.transfer_knowledge_cross_domain(args.source_domain, args.target_domain, context)

        print(f"Transferred {len(transferred)} patterns from {args.source_domain} to {args.target_domain}")
        for pattern in transferred:
            print(f"  {pattern.pattern_id}: confidence {pattern.confidence:.2f}")

    else:
        # Show summary
        insights = engine.get_learning_insights()
        print("Quantum Learning Engine Summary:")
        print(f"  Total Patterns: {insights['quantum_learning_summary']['total_patterns']}")
        print(f"  Quantum Coherence: {insights['quantum_learning_summary']['quantum_coherence']:.3f}")
        print(f"  Transfer Success Rate: {insights['knowledge_transfer_analysis']['transfer_success_rate']:.1%}")


if __name__ == '__main__':
    main()