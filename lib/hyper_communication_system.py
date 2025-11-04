#!/usr/bin/env python3
"""
Hyper-Communication System
Advanced cross-tier communication optimization with quantum entanglement-inspired
message passing, predictive routing, and intelligent bandwidth allocation.
"""

import json
import sys
import time
import asyncio
import threading
import queue
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable, Union
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import hashlib
import uuid

# Platform-specific imports for file locking
try:
    import msvcrt  # Windows
    PLATFORM = 'windows'
except ImportError:
    import fcntl  # Unix/Linux/Mac
    PLATFORM = 'unix'


class MessagePriority(Enum):
    """Message priority levels."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


class MessageType(Enum):
    """Message types for different communication patterns."""
    ANALYSIS_REQUEST = "analysis_request"
    ANALYSIS_RESPONSE = "analysis_response"
    EXECUTION_REQUEST = "execution_request"
    EXECUTION_RESPONSE = "execution_response"
    FEEDBACK = "feedback"
    LEARNING_UPDATE = "learning_update"
    PERFORMANCE_METRIC = "performance_metric"
    HEARTBEAT = "heartbeat"
    EMERGENCY = "emergency"


@dataclass
class HyperMessage:
    """Hyper-communication message structure."""
    message_id: str
    message_type: MessageType
    priority: MessagePriority
    source_tier: str  # "analysis" or "execution"
    source_agent: str
    target_tier: str
    target_agent: str
    payload: Dict[str, Any]
    timestamp: datetime
    expires_at: Optional[datetime] = None
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    routing_path: List[str] = None
    quantum_signature: Optional[str] = None
    bandwidth_allocation: float = 1.0
    latency_requirement: float = 0.0

    def __post_init__(self):
        if self.routing_path is None:
            self.routing_path = []
        if self.expires_at is None:
            self.expires_at = datetime.now() + timedelta(hours=1)
        if self.quantum_signature is None:
            self.quantum_signature = self._generate_quantum_signature()

    def _generate_quantum_signature(self) -> str:
        """Generate quantum signature for message integrity."""
        content = f"{self.message_id}_{self.message_type}_{self.source_agent}_{self.target_agent}_{self.payload}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class CommunicationMetrics:
    """Communication performance metrics."""
    total_messages: int = 0
    successful_deliveries: int = 0
    failed_deliveries: int = 0
    average_latency: float = 0.0
    peak_bandwidth: float = 0.0
    queue_depth: int = 0
    error_rate: float = 0.0
    throughput: float = 0.0
    efficiency: float = 0.0


class HyperCommunicationSystem:
    """
    Advanced cross-tier communication system with quantum-inspired
    message passing, predictive routing, and intelligent bandwidth allocation.
    """

    def __init__(self, storage_dir: str = ".claude-patterns"):
        """
        Initialize the hyper-communication system.

        Args:
            storage_dir: Directory for storing communication data
        """
        self.storage_dir = Path(storage_dir)
        self.communication_file = self.storage_dir / "hyper_communication.json"
        self.routing_file = self.storage_dir / "communication_routing.json"
        self.metrics_file = self.storage_dir / "communication_metrics.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Communication infrastructure
        self.message_queues = defaultdict(queue.PriorityQueue)  # agent_id -> PriorityQueue
        self.active_connections = defaultdict(set)  # agent_id -> set of connected agents
        self.bandwidth_allocations = defaultdict(float)  # agent_id -> allocated bandwidth
        self.latency_requirements = defaultdict(float)  # agent_id -> latency requirement

        # Routing and optimization
        self.routing_table = {}
        self.predictive_router = {}
        self.quantum_entanglements = defaultdict(dict)  # agent pairs -> entanglement strength
        self.communication_patterns = defaultdict(list)

        # Performance tracking
        self.metrics = defaultdict(CommunicationMetrics)
        self.latency_history = defaultdict(lambda: deque(maxlen=100))
        self.throughput_history = defaultdict(lambda: deque(maxlen=100))
        self.error_history = defaultdict(lambda: deque(maxlen=50))

        # System state
        self.running = False
        self.communication_threads = {}
        self.message_handlers = defaultdict(list)
        self.global_bandwidth = 1000.0  # Mbps
        self.available_bandwidth = self.global_bandwidth

        # Initialize storage
        self._initialize_communication_storage()
        self._load_communication_state()

        # Start background services
        self._start_background_services()

    def _initialize_communication_storage(self):
        """Initialize communication storage files."""
        if not self.communication_file.exists():
            initial_data = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "active_connections": {},
                "bandwidth_allocations": {},
                "communication_patterns": {},
                "quantum_entanglements": {},
                "message_history": []
            }
            self._write_communication_data(initial_data)

        if not self.routing_file.exists():
            routing_data = {
                "version": "1.0.0",
                "routing_table": {},
                "predictive_routes": {},
                "routing_performance": {},
                "last_optimization": datetime.now().isoformat()
            }
            self._write_routing_data(routing_data)

        if not self.metrics_file.exists():
            metrics_data = {
                "version": "1.0.0",
                "agent_metrics": {},
                "global_metrics": asdict(CommunicationMetrics()),
                "performance_history": [],
                "efficiency_trends": {}
            }
            self._write_metrics_data(metrics_data)

    def _load_communication_state(self):
        """Load communication state from storage."""
        try:
            # Load connections and allocations
            comm_data = self._read_communication_data()
            self.active_connections = defaultdict(set, comm_data.get("active_connections", {}))
            self.bandwidth_allocations = defaultdict(float, comm_data.get("bandwidth_allocations", {}))
            self.communication_patterns = defaultdict(list, comm_data.get("communication_patterns", {}))
            self.quantum_entanglements = defaultdict(dict, comm_data.get("quantum_entanglements", {}))

            # Load routing table
            routing_data = self._read_routing_data()
            self.routing_table = routing_data.get("routing_table", {})
            self.predictive_router = routing_data.get("predictive_routes", {})

            # Load metrics
            metrics_data = self._read_metrics_data()
            stored_metrics = metrics_data.get("agent_metrics", {})
            for agent_id, metric_data in stored_metrics.items():
                self.metrics[agent_id] = CommunicationMetrics(**metric_data)

        except Exception as e:
            print(f"Warning: Failed to load communication state: {e}", file=sys.stderr)

    def _start_background_services(self):
        """Start background communication services."""
        self.running = True

        # Start message processor
        processor_thread = threading.Thread(target=self._message_processor_loop, daemon=True)
        processor_thread.start()
        self.communication_threads["processor"] = processor_thread

        # Start bandwidth manager
        bandwidth_thread = threading.Thread(target=self._bandwidth_manager_loop, daemon=True)
        bandwidth_thread.start()
        self.communication_threads["bandwidth"] = bandwidth_thread

        # Start routing optimizer
        routing_thread = threading.Thread(target=self._routing_optimizer_loop, daemon=True)
        routing_thread.start()
        self.communication_threads["routing"] = routing_thread

        # Start metrics collector
        metrics_thread = threading.Thread(target=self._metrics_collector_loop, daemon=True)
        metrics_thread.start()
        self.communication_threads["metrics"] = metrics_thread

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

    def _read_communication_data(self) -> Dict[str, Any]:
        """Read communication data with file locking."""
        try:
            with open(self.communication_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_communication_storage()
            return self._read_communication_data()

    def _write_communication_data(self, data: Dict[str, Any]):
        """Write communication data with file locking."""
        with open(self.communication_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_routing_data(self) -> Dict[str, Any]:
        """Read routing data with file locking."""
        try:
            with open(self.routing_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"routing_table": {}, "predictive_routes": {}}

    def _write_routing_data(self, data: Dict[str, Any]):
        """Write routing data with file locking."""
        with open(self.routing_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def _read_metrics_data(self) -> Dict[str, Any]:
        """Read metrics data with file locking."""
        try:
            with open(self.metrics_file, 'r', encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"agent_metrics": {}, "global_metrics": asdict(CommunicationMetrics())}

    def _write_metrics_data(self, data: Dict[str, Any]):
        """Write metrics data with file locking."""
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            self._lock_file(f)
            try:
                json.dump(data, f, indent=2, ensure_ascii=False)
            finally:
                self._unlock_file(f)

    def establish_connection(
        self,
        agent1: str,
        agent2: str,
        tier1: str,
        tier2: str,
        bandwidth: float = 10.0,
        latency_requirement: float = 100.0
    ) -> bool:
        """
        Establish a high-performance connection between two agents.

        Args:
            agent1: First agent name
            agent2: Second agent name
            tier1: First agent tier
            tier2: Second agent tier
            bandwidth: Required bandwidth in Mbps
            latency_requirement: Maximum acceptable latency in ms

        Returns:
            True if connection established successfully
        """
        try:
            # Check bandwidth availability
            if self.available_bandwidth < bandwidth:
                print(f"Warning: Insufficient bandwidth for {agent1}-{agent2} connection", file=sys.stderr)
                return False

            # Establish connection
            self.active_connections[agent1].add(agent2)
            self.active_connections[agent2].add(agent1)

            # Allocate bandwidth
            self.bandwidth_allocations[agent1] += bandwidth / 2
            self.bandwidth_allocations[agent2] += bandwidth / 2
            self.available_bandwidth -= bandwidth

            # Set latency requirements
            self.latency_requirements[agent1] = min(self.latency_requirements[agent1], latency_requirement)
            self.latency_requirements[agent2] = min(self.latency_requirements[agent2], latency_requirement)

            # Create quantum entanglement between agents
            entanglement_strength = self._calculate_entanglement_strength(tier1, tier2, bandwidth, latency_requirement)
            self.quantum_entanglements[agent1][agent2] = entanglement_strength
            self.quantum_entanglements[agent2][agent1] = entanglement_strength

            # Update routing table
            self._update_routing_table(agent1, agent2, tier1, tier2)

            # Initialize metrics
            if agent1 not in self.metrics:
                self.metrics[agent1] = CommunicationMetrics()
            if agent2 not in self.metrics:
                self.metrics[agent2] = CommunicationMetrics()

            # Save state
            self._save_communication_state()

            print(f"Established hyper-connection: {agent1} ({tier1}) <-> {agent2} ({tier2})")
            return True

        except Exception as e:
            print(f"Error establishing connection: {e}", file=sys.stderr)
            return False

    def _calculate_entanglement_strength(
        self,
        tier1: str,
        tier2: str,
        bandwidth: float,
        latency_requirement: float
    ) -> float:
        """Calculate quantum entanglement strength between agents."""
        base_strength = 0.5

        # Cross-tier connections have higher entanglement
        if tier1 != tier2:
            base_strength += 0.3

        # Bandwidth factor
        bandwidth_factor = min(1.0, bandwidth / 100.0)  # Normalize to 0-1
        base_strength += bandwidth_factor * 0.1

        # Latency factor (lower latency = higher entanglement)
        latency_factor = max(0.0, 1.0 - latency_requirement / 1000.0)  # Normalize to 0-1
        base_strength += latency_factor * 0.1

        return min(1.0, base_strength)

    def _update_routing_table(self, agent1: str, agent2: str, tier1: str, tier2: str):
        """Update routing table with new connection."""
        # Direct routes
        if agent1 not in self.routing_table:
            self.routing_table[agent1] = {}
        if agent2 not in self.routing_table:
            self.routing_table[agent2] = {}

        # Direct connection
        self.routing_table[agent1][agent2] = {
            "path": [agent2],
            "cost": 1.0,
            "bandwidth": self.bandwidth_allocations[agent1] + self.bandwidth_allocations[agent2],
            "latency": self.latency_requirements[agent1] + self.latency_requirements[agent2],
            "tier": tier2
        }

        self.routing_table[agent2][agent1] = {
            "path": [agent1],
            "cost": 1.0,
            "bandwidth": self.bandwidth_allocations[agent1] + self.bandwidth_allocations[agent2],
            "latency": self.latency_requirements[agent1] + self.latency_requirements[agent2],
            "tier": tier1
        }

        # Update indirect routes through this connection
        self._propagate_route_updates(agent1, agent2)

    def _propagate_route_updates(self, new_agent1: str, new_agent2: str):
        """Propagate route updates to all connected agents."""
        # For each agent connected to agent1, update routes to agent2
        for connected_agent in self.active_connections[new_agent1]:
            if connected_agent != new_agent2:
                if connected_agent in self.routing_table and new_agent2 in self.routing_table[connected_agent]:
                    existing_cost = self.routing_table[connected_agent][new_agent2]["cost"]
                    new_cost = self.routing_table[connected_agent][new_agent1]["cost"] + 1.0

                    if new_cost < existing_cost:
                        # Update route
                        self.routing_table[connected_agent][new_agent2] = {
                            "path": self.routing_table[connected_agent][new_agent1]["path"] + [new_agent2],
                            "cost": new_cost,
                            "bandwidth": min(
                                self.routing_table[connected_agent][new_agent1]["bandwidth"],
                                self.routing_table[new_agent1][new_agent2]["bandwidth"]
                            ),
                            "latency": (
                                self.routing_table[connected_agent][new_agent1]["latency"] +
                                self.routing_table[new_agent1][new_agent2]["latency"]
                            )
                        }

    def send_message(
        self,
        source_agent: str,
        target_agent: str,
        source_tier: str,
        target_tier: str,
        message_type: MessageType,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.MEDIUM,
        correlation_id: Optional[str] = None,
        reply_to: Optional[str] = None,
        bandwidth_allocation: float = 1.0,
        latency_requirement: float = 0.0
    ) -> str:
        """
        Send a hyper-communication message.

        Args:
            source_agent: Source agent name
            target_agent: Target agent name
            source_tier: Source agent tier
            target_tier: Target agent tier
            message_type: Type of message
            payload: Message payload
            priority: Message priority
            correlation_id: Optional correlation ID for request/response pairing
            reply_to: Optional message ID to reply to
            bandwidth_allocation: Required bandwidth allocation
            latency_requirement: Maximum acceptable latency

        Returns:
            Message ID
        """
        # Generate message ID
        message_id = str(uuid.uuid4())

        # Create hyper-message
        message = HyperMessage(
            message_id=message_id,
            message_type=message_type,
            priority=priority,
            source_tier=source_tier,
            source_agent=source_agent,
            target_tier=target_tier,
            target_agent=target_agent,
            payload=payload,
            timestamp=datetime.now(),
            correlation_id=correlation_id,
            reply_to=reply_to,
            bandwidth_allocation=bandwidth_allocation,
            latency_requirement=latency_requirement
        )

        # Determine optimal routing
        routing_path = self._determine_optimal_routing(message)
        message.routing_path = routing_path

        # Add to priority queue
        priority_value = (priority.value, time.time())
        self.message_queues[target_agent].put((priority_value, message))

        # Update metrics
        self.metrics[source_agent].total_messages += 1
        self.metrics[source_agent].queue_depth = self.message_queues[target_agent].qsize()

        # Record communication pattern
        self._record_communication_pattern(source_agent, target_agent, message_type, priority)

        # Save state
        self._save_communication_state()

        return message_id

    def _determine_optimal_routing(self, message: HyperMessage) -> List[str]:
        """Determine optimal routing path for message."""
        source = message.source_agent
        target = message.target_agent

        # Check for direct connection
        if target in self.active_connections.get(source, set()):
            return [target]

        # Use quantum entanglement for routing
        if source in self.quantum_entanglements and target in self.quantum_entanglements[source]:
            entanglement_strength = self.quantum_entanglements[source][target]
            if entanglement_strength > 0.8:
                # Direct quantum connection
                return [target]

        # Use routing table
        if source in self.routing_table and target in self.routing_table[source]:
            return self.routing_table[source][target]["path"]

        # Use predictive routing
        predictive_key = f"{source}_{target}"
        if predictive_key in self.predictive_router:
            return self.predictive_router[predictive_key]["path"]

        # Find shortest path
        return self._find_shortest_path(source, target)

    def _find_shortest_path(self, source: str, target: str) -> List[str]:
        """Find shortest path using Dijkstra's algorithm."""
        if source not in self.active_connections:
            return [target]  # Direct fallback

        distances = {source: 0}
        previous = {}
        unvisited = set([source])
        queue = deque([source])

        while queue:
            current = queue.popleft()
            unvisited.discard(current)

            if current == target:
                break

            for neighbor in self.active_connections.get(current, set()):
                # Calculate path cost based on latency and bandwidth
                cost = distances[current] + 1.0  # Simplified cost

                if neighbor not in distances or cost < distances[neighbor]:
                    distances[neighbor] = cost
                    previous[neighbor] = current
                    if neighbor not in unvisited:
                        queue.append(neighbor)
                        unvisited.add(neighbor)

        # Reconstruct path
        if target in previous:
            path = []
            current = target
            while current != source:
                path.append(current)
                current = previous[current]
            path.reverse()
            return path

        return [target]  # Direct fallback

    def _record_communication_pattern(
        self,
        source_agent: str,
        target_agent: str,
        message_type: MessageType,
        priority: MessagePriority
    ):
        """Record communication pattern for learning."""
        pattern_key = f"{source_agent}_{target_agent}"
        pattern = {
            "timestamp": datetime.now().isoformat(),
            "message_type": message_type.value,
            "priority": priority.value
        }

        self.communication_patterns[pattern_key].append(pattern)

        # Keep last 100 patterns per connection
        if len(self.communication_patterns[pattern_key]) > 100:
            self.communication_patterns[pattern_key] = self.communication_patterns[pattern_key][-100:]

    def register_message_handler(
        self,
        agent_id: str,
        message_types: List[MessageType],
        handler: Callable[[HyperMessage], Any]
    ):
        """
        Register message handler for specific message types.

        Args:
            agent_id: Agent ID to register handler for
            message_types: List of message types to handle
            handler: Handler function
        """
        for message_type in message_types:
            self.message_handlers[agent_id].append((message_type, handler))

    def _message_processor_loop(self):
        """Background message processing loop."""
        while self.running:
            try:
                # Process messages for all agents
                for agent_id, message_queue in self.message_queues.items():
                    if not message_queue.empty():
                        try:
                            priority_value, message = message_queue.get_nowait()

                            # Check if message has expired
                            if datetime.now() > message.expires_at:
                                self.metrics[message.source_agent].failed_deliveries += 1
                                continue

                            # Process message
                            self._process_message(agent_id, message)

                            # Update metrics
                            delivery_time = (datetime.now() - message.timestamp).total_seconds()
                            self.latency_history[agent_id].append(delivery_time)
                            self.metrics[message.source_agent].successful_deliveries += 1
                            self.metrics[message.source_agent].average_latency = statistics.mean(
                                list(self.latency_history[agent_id])
                            )

                        except queue.Empty:
                            continue
                        except Exception as e:
                            print(f"Error processing message for {agent_id}: {e}", file=sys.stderr)

                # Small delay to prevent busy waiting
                time.sleep(0.01)

            except Exception as e:
                print(f"Error in message processor loop: {e}", file=sys.stderr)
                time.sleep(0.1)

    def _process_message(self, agent_id: str, message: HyperMessage):
        """Process a single message."""
        # Find appropriate handler
        handlers = self.message_handlers.get(agent_id, [])
        for message_type, handler in handlers:
            if message_type == message.message_type:
                try:
                    # Call handler
                    result = handler(message)

                    # Handle response if needed
                    if message.message_type in [MessageType.ANALYSIS_REQUEST, MessageType.EXECUTION_REQUEST]:
                        response_type = (MessageType.ANALYSIS_RESPONSE
                                       if message.message_type == MessageType.ANALYSIS_REQUEST
                                       else MessageType.EXECUTION_RESPONSE)

                        # Send response
                        self.send_message(
                            source_agent=agent_id,
                            target_agent=message.source_agent,
                            source_tier=message.target_tier,
                            target_tier=message.source_tier,
                            message_type=response_type,
                            payload={"result": result, "original_message_id": message.message_id},
                            correlation_id=message.correlation_id,
                            reply_to=message.message_id
                        )

                except Exception as e:
                    print(f"Error in message handler for {agent_id}: {e}", file=sys.stderr)

                    # Record error
                    self.error_history[agent_id].append({
                        "timestamp": datetime.now().isoformat(),
                        "error": str(e),
                        "message_id": message.message_id
                    })

    def _bandwidth_manager_loop(self):
        """Background bandwidth management loop."""
        while self.running:
            try:
                # Calculate current bandwidth usage
                total_allocated = sum(self.bandwidth_allocations.values())
                usage_ratio = total_allocated / self.global_bandwidth

                # Update metrics
                for agent_id in self.bandwidth_allocations:
                    self.metrics[agent_id].peak_bandwidth = max(
                        self.metrics[agent_id].peak_bandwidth,
                        self.bandwidth_allocations[agent_id]
                    )

                # Optimize bandwidth allocation if needed
                if usage_ratio > 0.9:  # 90% usage threshold
                    self._optimize_bandwidth_allocation()

                # Update throughput metrics
                current_time = time.time()
                for agent_id in self.metrics:
                    recent_messages = sum(1 for _ in self.latency_history[agent_id] if current_time - _.timestamp < 60)
                    self.metrics[agent_id].throughput = recent_messages / 60  # messages per second
                    self.throughput_history[agent_id].append(recent_messages / 60)

                time.sleep(5)  # Check every 5 seconds

            except Exception as e:
                print(f"Error in bandwidth manager loop: {e}", file=sys.stderr)
                time.sleep(1)

    def _optimize_bandwidth_allocation(self):
        """Optimize bandwidth allocation based on current usage."""
        # Sort agents by priority and usage
        agent_priorities = []
        for agent_id, allocation in self.bandwidth_allocations.items():
            priority = self._calculate_agent_priority(agent_id)
            recent_throughput = statistics.mean(list(self.throughput_history[agent_id])) if self.throughput_history[agent_id] else 0
            agent_priorities.append((priority, recent_throughput, agent_id, allocation))

        # Sort by priority (descending) and throughput (descending)
        agent_priorities.sort(key=lambda x: (-x[0], -x[1]))

        # Reallocate bandwidth
        available_bandwidth = self.global_bandwidth * 0.8  # Keep 20% as reserve
        for priority, throughput, agent_id, current_allocation in agent_priorities:
            # Calculate new allocation based on priority and throughput
            new_allocation = min(
                current_allocation * 1.1 if priority > 0.7 else current_allocation * 0.9,
                available_bandwidth * 0.3  # Max 30% per agent
            )

            self.bandwidth_allocations[agent_id] = new_allocation
            available_bandwidth -= new_allocation

    def _calculate_agent_priority(self, agent_id: str) -> float:
        """Calculate priority score for an agent."""
        base_priority = 0.5

        # Factor in message success rate
        if self.metrics[agent_id].total_messages > 0:
            success_rate = (self.metrics[agent_id].successful_deliveries /
                          self.metrics[agent_id].total_messages)
            base_priority += success_rate * 0.3

        # Factor in efficiency (throughput vs bandwidth)
        if self.bandwidth_allocations[agent_id] > 0:
            efficiency = self.metrics[agent_id].throughput / self.bandwidth_allocations[agent_id]
            base_priority += min(0.2, efficiency * 0.1)

        return min(1.0, base_priority)

    def _routing_optimizer_loop(self):
        """Background routing optimization loop."""
        while self.running:
            try:
                # Analyze communication patterns
                self._analyze_communication_patterns()

                # Update predictive routing
                self._update_predictive_routing()

                # Optimize quantum entanglements
                self._optimize_quantum_entanglements()

                # Save routing updates
                self._save_routing_state()

                time.sleep(30)  # Optimize every 30 seconds

            except Exception as e:
                print(f"Error in routing optimizer loop: {e}", file=sys.stderr)
                time.sleep(5)

    def _analyze_communication_patterns(self):
        """Analyze communication patterns for optimization."""
        for pattern_key, patterns in self.communication_patterns.items():
            if len(patterns) < 10:
                continue  # Not enough data

            source_agent, target_agent = pattern_key.split('_', 1)

            # Calculate pattern metrics
            message_frequency = len(patterns) / 3600  # messages per hour (assuming 1 hour window)
            avg_priority = statistics.mean([p["priority"] for p in patterns])

            # Update routing performance
            if source_agent not in self.routing_table:
                self.routing_table[source_agent] = {}

            if target_agent in self.routing_table[source_agent]:
                route_info = self.routing_table[source_agent][target_agent]
                route_info["message_frequency"] = message_frequency
                route_info["avg_priority"] = avg_priority
                route_info["pattern_strength"] = min(1.0, message_frequency / 10)

    def _update_predictive_routing(self):
        """Update predictive routing based on patterns."""
        for source_agent, routes in self.routing_table.items():
            for target_agent, route_info in routes.items():
                # Use pattern strength and entanglement for prediction
                pattern_strength = route_info.get("pattern_strength", 0.5)
                entanglement_strength = self.quantum_entanglements.get(source_agent, {}).get(target_agent, 0.5)

                # Predict optimal routing
                if pattern_strength > 0.7 or entanglement_strength > 0.8:
                    predictive_key = f"{source_agent}_{target_agent}"
                    self.predictive_router[predictive_key] = {
                        "path": route_info["path"],
                        "confidence": (pattern_strength + entanglement_strength) / 2,
                        "last_updated": datetime.now().isoformat()
                    }

    def _optimize_quantum_entanglements(self):
        """Optimize quantum entanglements between agents."""
        # Calculate entanglement effectiveness
        for agent1 in list(self.quantum_entanglements.keys()):
            for agent2 in list(self.quantum_entanglements[agent1].keys()):
                current_strength = self.quantum_entanglements[agent1][agent2]

                # Calculate effectiveness based on communication success
                if agent1 in self.metrics and agent2 in self.metrics:
                    success_rate_1 = (self.metrics[agent1].successful_deliveries /
                                   max(1, self.metrics[agent1].total_messages))
                    success_rate_2 = (self.metrics[agent2].successful_deliveries /
                                   max(1, self.metrics[agent2].total_messages))
                    avg_success_rate = (success_rate_1 + success_rate_2) / 2

                    # Adjust entanglement strength
                    if avg_success_rate > 0.9:
                        new_strength = min(1.0, current_strength * 1.05)  # Increase by 5%
                    elif avg_success_rate < 0.7:
                        new_strength = max(0.1, current_strength * 0.95)  # Decrease by 5%
                    else:
                        new_strength = current_strength

                    self.quantum_entanglements[agent1][agent2] = new_strength
                    self.quantum_entanglements[agent2][agent1] = new_strength

    def _metrics_collector_loop(self):
        """Background metrics collection loop."""
        while self.running:
            try:
                # Calculate global metrics
                total_messages = sum(m.total_messages for m in self.metrics.values())
                total_successful = sum(m.successful_deliveries for m in self.metrics.values())
                total_failed = sum(m.failed_deliveries for m in self.metrics.values())

                global_metrics = CommunicationMetrics(
                    total_messages=total_messages,
                    successful_deliveries=total_successful,
                    failed_deliveries=total_failed,
                    average_latency=statistics.mean([m.average_latency for m in self.metrics.values() if m.average_latency > 0]) if self.metrics else 0,
                    peak_bandwidth=max(m.peak_bandwidth for m in self.metrics.values()) if self.metrics else 0,
                    error_rate=total_failed / max(1, total_messages),
                    throughput=sum(m.throughput for m in self.metrics.values()),
                    efficiency=self._calculate_global_efficiency()
                )

                # Update agent metrics
                for agent_id, metrics in self.metrics.items():
                    # Calculate efficiency
                    if metrics.total_messages > 0:
                        metrics.error_rate = metrics.failed_deliveries / metrics.total_messages
                        metrics.efficiency = self._calculate_agent_efficiency(agent_id)

                # Save metrics
                self._save_metrics_state(global_metrics)

                time.sleep(10)  # Collect every 10 seconds

            except Exception as e:
                print(f"Error in metrics collector loop: {e}", file=sys.stderr)
                time.sleep(2)

    def _calculate_global_efficiency(self) -> float:
        """Calculate global communication efficiency."""
        if not self.metrics:
            return 0.0

        total_efficiency = sum(m.efficiency for m in self.metrics.values())
        return total_efficiency / len(self.metrics)

    def _calculate_agent_efficiency(self, agent_id: str) -> float:
        """Calculate efficiency for a specific agent."""
        metrics = self.metrics[agent_id]

        if metrics.total_messages == 0:
            return 0.0

        # Factors: success rate, latency, throughput, bandwidth utilization
        success_rate = metrics.successful_deliveries / metrics.total_messages
        latency_score = max(0, 1 - metrics.average_latency / 1000)  # Normalize to 0-1
        throughput_score = min(1, metrics.throughput / 10)  # Normalize to 0-1 (10 msg/s = 1.0)
        bandwidth_score = min(1, metrics.peak_bandwidth / 100)  # Normalize to 0-1 (100 Mbps = 1.0)

        efficiency = (
            success_rate * 0.4 +
            latency_score * 0.3 +
            throughput_score * 0.2 +
            bandwidth_score * 0.1
        )

        return efficiency

    def _save_communication_state(self):
        """Save communication state to storage."""
        comm_data = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "active_connections": {k: list(v) for k, v in self.active_connections.items()},
            "bandwidth_allocations": dict(self.bandwidth_allocations),
            "communication_patterns": dict(self.communication_patterns),
            "quantum_entanglements": dict(self.quantum_entanglements)
        }
        self._write_communication_data(comm_data)

    def _save_routing_state(self):
        """Save routing state to storage."""
        routing_data = {
            "version": "1.0.0",
            "routing_table": self.routing_table,
            "predictive_routes": self.predictive_router,
            "routing_performance": {},
            "last_optimization": datetime.now().isoformat()
        }
        self._write_routing_data(routing_data)

    def _save_metrics_state(self, global_metrics: CommunicationMetrics):
        """Save metrics state to storage."""
        metrics_data = {
            "version": "1.0.0",
            "agent_metrics": {k: asdict(v) for k, v in self.metrics.items()},
            "global_metrics": asdict(global_metrics),
            "performance_history": [],  # Would store historical data here
            "efficiency_trends": {}  # Would store trend data here
        }
        self._write_metrics_data(metrics_data)

    def get_communication_status(self) -> Dict[str, Any]:
        """Get comprehensive communication system status."""
        global_metrics = CommunicationMetrics(
            total_messages=sum(m.total_messages for m in self.metrics.values()),
            successful_deliveries=sum(m.successful_deliveries for m in self.metrics.values()),
            failed_deliveries=sum(m.failed_deliveries for m in self.metrics.values()),
            average_latency=statistics.mean([m.average_latency for m in self.metrics.values() if m.average_latency > 0]) if self.metrics else 0,
            peak_bandwidth=sum(m.peak_bandwidth for m in self.metrics.values()) if self.metrics else 0,
            error_rate=sum(m.failed_deliveries for m in self.metrics.values()) / max(1, sum(m.total_messages for m in self.metrics.values())),
            throughput=sum(m.throughput for m in self.metrics.values()),
            efficiency=self._calculate_global_efficiency()
        )

        status = {
            "system_status": {
                "running": self.running,
                "active_connections": sum(len(connections) for connections in self.active_connections.values()) // 2,
                "total_agents": len(self.active_connections),
                "available_bandwidth": self.available_bandwidth,
                "global_bandwidth": self.global_bandwidth
            },
            "global_metrics": asdict(global_metrics),
            "top_performers": self._get_top_performers(),
            "communication_heatmap": self._generate_communication_heatmap(),
            "quantum_entanglements": {
                agent: dict(connections) for agent, connections in self.quantum_entanglements.items()
                if connections
            }
        }

        return status

    def _get_top_performers(self) -> List[Dict[str, Any]]:
        """Get top performing agents."""
        performers = []

        for agent_id, metrics in self.metrics.items():
            if metrics.total_messages > 0:
                performers.append({
                    "agent_id": agent_id,
                    "efficiency": metrics.efficiency,
                    "success_rate": metrics.successful_deliveries / metrics.total_messages,
                    "throughput": metrics.throughput,
                    "average_latency": metrics.average_latency
                })

        # Sort by efficiency
        performers.sort(key=lambda x: x["efficiency"], reverse=True)
        return performers[:5]  # Top 5

    def _generate_communication_heatmap(self) -> Dict[str, Dict[str, float]]:
        """Generate communication heatmap data."""
        heatmap = defaultdict(dict)

        for pattern_key, patterns in self.communication_patterns.items():
            if len(patterns) < 2:
                continue

            source_agent, target_agent = pattern_key.split('_', 1)
            frequency = len(patterns)
            avg_priority = statistics.mean([p["priority"] for p in patterns])

            # Calculate heatmap intensity
            intensity = min(1.0, frequency / 50)  # Normalize to 0-1
            heatmap[source_agent][target_agent] = intensity

        return dict(heatmap)

    def shutdown(self):
        """Shutdown the hyper-communication system."""
        print("Shutting down hyper-communication system...")
        self.running = False

        # Wait for threads to finish
        for thread_name, thread in self.communication_threads.items():
            if thread.is_alive():
                thread.join(timeout=5)
                print(f"  {thread_name} thread stopped")

        # Save final state
        self._save_communication_state()
        self._save_routing_state()

        print("Hyper-communication system shutdown complete")


def main():
    """Command-line interface for testing the hyper-communication system."""
    import argparse

    parser = argparse.ArgumentParser(description='Hyper-Communication System')
    parser.add_argument('--storage-dir', default='.claude-patterns', help='Storage directory')
    parser.add_argument('--action', choices=['connect', 'send', 'status', 'test'],
                       help='Action to perform')
    parser.add_argument('--agent1', help='First agent name')
    parser.add_argument('--agent2', help='Second agent name')
    parser.add_argument('--tier1', choices=['analysis', 'execution'], help='First agent tier')
    parser.add_argument('--tier2', choices=['analysis', 'execution'], help='Second agent tier')
    parser.add_argument('--bandwidth', type=float, default=10.0, help='Bandwidth in Mbps')
    parser.add_argument('--message', help='Test message content')
    parser.add_argument('--duration', type=int, default=10, help='Test duration in seconds')

    args = parser.parse_args()

    system = HyperCommunicationSystem(args.storage_dir)

    if args.action == 'connect':
        if not all([args.agent1, args.agent2, args.tier1, args.tier2]):
            print("Error: --agent1, --agent2, --tier1, and --tier2 required for connect")
            sys.exit(1)

        success = system.establish_connection(
            args.agent1, args.agent2, args.tier1, args.tier2, args.bandwidth
        )
        print(f"Connection {'established' if success else 'failed'}")

    elif args.action == 'send':
        if not all([args.agent1, args.agent2, args.tier1, args.tier2]):
            print("Error: --agent1, --agent2, --tier1, and --tier2 required for send")
            sys.exit(1)

        message_content = args.message or "Test message"
        message_id = system.send_message(
            args.agent1, args.agent2, args.tier1, args.tier2,
            MessageType.ANALYSIS_REQUEST,
            {"content": message_content}
        )
        print(f"Message sent: {message_id}")

    elif args.action == 'status':
        status = system.get_communication_status()
        print("Hyper-Communication System Status:")
        print(f"  Running: {status['system_status']['running']}")
        print(f"  Active Connections: {status['system_status']['active_connections']}")
        print(f"  Total Agents: {status['system_status']['total_agents']}")
        print(f"  Available Bandwidth: {status['system_status']['available_bandwidth']:.1f} Mbps")
        print(f"  Global Efficiency: {status['global_metrics']['efficiency']:.1%}")
        print(f"  Error Rate: {status['global_metrics']['error_rate']:.1%}")

    elif args.action == 'test':
        print("Running hyper-communication test...")

        # Establish test connections
        system.establish_connection("agent1", "agent2", "analysis", "execution", 20.0)
        system.establish_connection("agent2", "agent3", "execution", "analysis", 15.0)

        # Send test messages
        for i in range(10):
            system.send_message(
                "agent1", "agent2", "analysis", "execution",
                MessageType.ANALYSIS_REQUEST,
                {"test_message": f"Test {i+1}", "timestamp": time.time()}
            )
            time.sleep(0.1)

        # Wait for processing
        time.sleep(2)

        # Show final status
        status = system.get_communication_status()
        print(f"Test completed. Efficiency: {status['global_metrics']['efficiency']:.1%}")

        # Cleanup
        system.shutdown()

    else:
        # Show status by default
        status = system.get_communication_status()
        print("Hyper-Communication System Summary:")
        print(f"  Active Connections: {status['system_status']['active_connections']}")
        print(f"  Global Efficiency: {status['global_metrics']['efficiency']:.1%}")
        print(f"  Throughput: {status['global_metrics']['throughput']:.1f} msg/s")


if __name__ == '__main__':
    main()