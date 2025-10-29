#!/usr/bin/env python3
"""
Multi-Agent Communication Protocol for Autonomous Claude Agent Plugin

Standardized communication and coordination system for multi-agent workflows
with 95% success rate target through reliable message passing and state management.
"""

import json
import argparse
import sys
import platform
import uuid
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union
from enum import Enum
from dataclasses import dataclass, asdict
from collections import defaultdict, deque

# Cross-platform file locking
if platform.system() == 'Windows':
    import msvcrt
    def lock_file(f, exclusive=False):
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)
    def unlock_file(f):
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl
    def lock_file(f, exclusive=False):
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
    def unlock_file(f):
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class MessageType(Enum):
    """Message types for agent communication."""
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    STATUS_UPDATE = "status_update"
    COORDINATION_REQUEST = "coordination_request"
    COORDINATION_RESPONSE = "coordination_response"
    ERROR_NOTIFICATION = "error_notification"
    RESOURCE_REQUEST = "resource_request"
    RESOURCE_RESPONSE = "resource_response"
    HEARTBEAT = "heartbeat"
    COMPLETION_NOTIFICATION = "completion_notification"


class AgentStatus(Enum):
    """Agent status enumeration."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"
    COORDINATING = "coordinating"


class Priority(Enum):
    """Message priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Message:
    """Standardized message format for agent communication."""
    id: str
    sender: str
    recipient: str
    message_type: MessageType
    payload: Dict[str, Any]
    timestamp: datetime
    priority: Priority = Priority.NORMAL
    correlation_id: Optional[str] = None
    requires_response: bool = False
    expires_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['message_type'] = self.message_type.value
        data['priority'] = self.priority.value
        if self.expires_at:
            data['expires_at'] = self.expires_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary."""
        data['message_type'] = MessageType(data['message_type'])
        data['priority'] = Priority(data['priority'])
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        if data.get('expires_at'):
            data['expires_at'] = datetime.fromisoformat(data['expires_at'])
        return cls(**data)


@dataclass
class AgentState:
    """Agent state information."""
    id: str
    name: str
    status: AgentStatus
    current_task: Optional[str] = None
    capabilities: List[str] = None
    last_heartbeat: datetime = None
    load_factor: float = 0.0  # 0.0 to 1.0
    error_count: int = 0
    success_count: int = 0
    last_error: Optional[str] = None

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.last_heartbeat is None:
            self.last_heartbeat = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert agent state to dictionary."""
        data = asdict(self)
        data['status'] = self.status.value
        data['last_heartbeat'] = self.last_heartbeat.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentState':
        """Create agent state from dictionary."""
        data['status'] = AgentStatus(data['status'])
        data['last_heartbeat'] = datetime.fromisoformat(data['last_heartbeat'])
        return cls(**data)


class MultiAgentProtocol:
    """Multi-agent communication protocol manager."""

    def __init__(self, protocol_dir: str = ".claude-patterns"):
        """Initialize multi-agent protocol."""
        self.protocol_dir = Path(protocol_dir)
        self.agents_file = self.protocol_dir / "agent_registry.json"
        self.messages_file = self.protocol_dir / "message_queue.json"
        self.coordination_file = self.protocol_dir / "coordination_state.json"
        self.stats_file = self.protocol_dir / "protocol_stats.json"

        self.agents: Dict[str, AgentState] = {}
        self.message_queue: deque = deque()
        self.coordination_state: Dict[str, Any] = {}
        self.message_handlers: Dict[MessageType, List[Callable]] = defaultdict(list)
        self.running = False
        self.protocol_thread = None
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "successful_coordinations": 0,
            "failed_coordinations": 0,
            "agent_errors": 0,
            "average_response_time": 0.0,
            "success_rate": 0.0
        }

        self._ensure_files()
        self._load_state()

    def _ensure_files(self):
        """Create necessary files with default structure."""
        self.protocol_dir.mkdir(parents=True, exist_ok=True)

        if not self.agents_file.exists():
            self._write_json(self.agents_file, {})

        if not self.messages_file.exists():
            self._write_json(self.messages_file, {"queue": [], "processed": []})

        if not self.coordination_file.exists():
            self._write_json(self.coordination_file, {
                "active_coordinations": {},
                "coordination_history": [],
                "resource_allocation": {}
            })

        if not self.stats_file.exists():
            self._write_json(self.stats_file, {
                "version": "1.0.0",
                "created": datetime.now().isoformat(),
                "stats": self.stats,
                "success_history": []
            })

    def _read_json(self, file_path: Path) -> Dict[str, Any]:
        """Read JSON file with error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _write_json(self, file_path: Path, data: Dict[str, Any]):
        """Write JSON file with atomic update."""
        temp_file = file_path.with_suffix('.tmp')
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            temp_file.replace(file_path)
        except Exception as e:
            print(f"Error writing {file_path}: {e}", file=sys.stderr)

    def _load_state(self):
        """Load protocol state from files."""
        agents_data = self._read_json(self.agents_file)
        for agent_id, agent_data in agents_data.items():
            self.agents[agent_id] = AgentState.from_dict(agent_data)

        messages_data = self._read_json(self.messages_file)
        for msg_data in messages_data.get("queue", []):
            self.message_queue.append(Message.from_dict(msg_data))

        self.coordination_state = self._read_json(self.coordination_file)

        stats_data = self._read_json(self.stats_file)
        self.stats = stats_data.get("stats", self.stats)

    def _save_state(self):
        """Save protocol state to files."""
        agents_data = {agent_id: agent.to_dict() for agent_id, agent in self.agents.items()}
        self._write_json(self.agents_file, agents_data)

        messages_data = {
            "queue": [msg.to_dict() for msg in self.message_queue],
            "processed": []
        }
        self._write_json(self.messages_file, messages_data)

        self._write_json(self.coordination_file, self.coordination_state)

        stats_data = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "stats": self.stats,
            "success_history": self.stats.get("success_history", [])
        }
        self._write_json(self.stats_file, stats_data)

    def register_agent(self, agent_id: str, name: str, capabilities: List[str]) -> bool:
        """Register a new agent with the protocol."""
        if agent_id in self.agents:
            print(f"Agent {agent_id} already registered")
            return False

        agent = AgentState(
            id=agent_id,
            name=name,
            status=AgentStatus.IDLE,
            capabilities=capabilities,
            last_heartbeat=datetime.now()
        )

        self.agents[agent_id] = agent
        self._save_state()
        print(f"Registered agent: {name} ({agent_id})")
        return True

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the protocol."""
        if agent_id not in self.agents:
            print(f"Agent {agent_id} not found")
            return False

        del self.agents[agent_id]
        self._save_state()
        print(f"Unregistered agent: {agent_id}")
        return True

    def send_message(self, sender: str, recipient: str, message_type: MessageType,
                    payload: Dict[str, Any], priority: Priority = Priority.NORMAL,
                    correlation_id: Optional[str] = None,
                    requires_response: bool = False,
                    expires_in: Optional[int] = None) -> str:
        """Send a message to another agent."""
        message_id = str(uuid.uuid4())

        expires_at = None
        if expires_in:
            expires_at = datetime.now() + timezone(timedelta(seconds=expires_in))

        message = Message(
            id=message_id,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            payload=payload,
            timestamp=datetime.now(),
            priority=priority,
            correlation_id=correlation_id,
            requires_response=requires_response,
            expires_at=expires_at
        )

        self.message_queue.append(message)
        self.stats["messages_sent"] += 1
        self._save_state()

        return message_id

    def send_task_request(self, requester: str, target_agent: str, task_data: Dict[str, Any],
                         priority: Priority = Priority.NORMAL) -> str:
        """Send a task request to a specific agent."""
        return self.send_message(
            sender=requester,
            recipient=target_agent,
            message_type=MessageType.TASK_REQUEST,
            payload=task_data,
            priority=priority,
            requires_response=True
        )

    def coordinate_multi_agent_task(self, coordinator: str, task_data: Dict[str, Any],
                                  required_agents: List[str]) -> str:
        """Coordinate a multi-agent task."""
        coordination_id = str(uuid.uuid4())

        # Create coordination state
        self.coordination_state["active_coordinations"][coordination_id] = {
            "coordinator": coordinator,
            "task_data": task_data,
            "required_agents": required_agents,
            "status": "pending",
            "responses": {},
            "created_at": datetime.now().isoformat(),
            "timeout": 300  # 5 minutes
        }

        # Send coordination requests to all required agents
        for agent_id in required_agents:
            if agent_id in self.agents:
                self.send_message(
                    sender=coordinator,
                    recipient=agent_id,
                    message_type=MessageType.COORDINATION_REQUEST,
                    payload={
                        "coordination_id": coordination_id,
                        "task_data": task_data,
                        "required_agents": required_agents
                    },
                    priority=Priority.HIGH,
                    correlation_id=coordination_id,
                    requires_response=True
                )

        self._save_state()
        return coordination_id

    def update_agent_status(self, agent_id: str, status: AgentStatus,
                           current_task: Optional[str] = None,
                           error_message: Optional[str] = None):
        """Update an agent's status."""
        if agent_id not in self.agents:
            return False

        agent = self.agents[agent_id]
        agent.status = status
        agent.last_heartbeat = datetime.now()

        if current_task:
            agent.current_task = current_task

        if status == AgentStatus.ERROR:
            agent.error_count += 1
            agent.last_error = error_message
            self.stats["agent_errors"] += 1
        elif status == AgentStatus.IDLE:
            agent.current_task = None
            agent.success_count += 1

        self._save_state()
        return True

    def get_agent_status(self, agent_id: str) -> Optional[AgentState]:
        """Get the status of a specific agent."""
        return self.agents.get(agent_id)

    def get_available_agents(self, capability: Optional[str] = None) -> List[AgentState]:
        """Get list of available agents, optionally filtered by capability."""
        available = []
        for agent in self.agents.values():
            if agent.status == AgentStatus.IDLE:
                if capability is None or capability in agent.capabilities:
                    available.append(agent)
        return available

    def process_message(self, message: Message) -> bool:
        """Process a single message."""
        try:
            # Check if message has expired
            if message.expires_at and datetime.now() > message.expires_at:
                return False

            # Check if recipient exists
            if message.recipient not in self.agents:
                print(f"Message recipient {message.recipient} not found")
                return False

            # Update recipient status based on message
            agent = self.agents[message.recipient]

            if message.message_type == MessageType.TASK_REQUEST:
                agent.status = AgentStatus.BUSY
                agent.current_task = message.payload.get("task_id", "unknown")
            elif message.message_type == MessageType.COMPLETION_NOTIFICATION:
                agent.status = AgentStatus.IDLE
                agent.current_task = None
                agent.success_count += 1

            agent.last_heartbeat = datetime.now()
            self.stats["messages_received"] += 1

            # Call registered handlers
            for handler in self.message_handlers[message.message_type]:
                try:
                    handler(message)
                except Exception as e:
                    print(f"Error in message handler: {e}")

            return True

        except Exception as e:
            print(f"Error processing message {message.id}: {e}")
            return False

    def process_message_queue(self):
        """Process all pending messages in the queue."""
        processed_count = 0
        while self.message_queue:
            message = self.message_queue.popleft()
            if self.process_message(message):
                processed_count += 1
        return processed_count

    def start_protocol_daemon(self):
        """Start the protocol daemon for message processing."""
        if self.running:
            return

        self.running = True
        self.protocol_thread = threading.Thread(target=self._protocol_daemon, daemon=True)
        self.protocol_thread.start()
        print("Multi-agent protocol daemon started")

    def stop_protocol_daemon(self):
        """Stop the protocol daemon."""
        self.running = False
        if self.protocol_thread:
            self.protocol_thread.join(timeout=5)
        print("Multi-agent protocol daemon stopped")

    def _protocol_daemon(self):
        """Background daemon for processing messages and heartbeats."""
        while self.running:
            try:
                # Process message queue
                self.process_message_queue()

                # Check for agent timeouts
                current_time = datetime.now()
                for agent_id, agent in self.agents.items():
                    time_since_heartbeat = (current_time - agent.last_heartbeat).total_seconds()
                    if time_since_heartbeat > 60:  # 1 minute timeout
                        if agent.status != AgentStatus.OFFLINE:
                            agent.status = AgentStatus.OFFLINE
                            print(f"Agent {agent_id} timed out")

                # Check coordination timeouts
                self._check_coordination_timeouts()

                # Calculate success rate
                total_tasks = sum(agent.success_count + agent.error_count for agent in self.agents.values())
                if total_tasks > 0:
                    successful_tasks = sum(agent.success_count for agent in self.agents.values())
                    self.stats["success_rate"] = successful_tasks / total_tasks

                # Save state periodically
                if int(time.time()) % 10 == 0:  # Every 10 seconds
                    self._save_state()

                time.sleep(1)  # Process every second

            except Exception as e:
                print(f"Error in protocol daemon: {e}")
                time.sleep(5)

    def _check_coordination_timeouts(self):
        """Check for coordination timeouts."""
        current_time = datetime.now()
        expired_coordinations = []

        for coord_id, coord_data in self.coordination_state["active_coordinations"].items():
            created_at = datetime.fromisoformat(coord_data["created_at"])
            if (current_time - created_at).total_seconds() > coord_data["timeout"]:
                expired_coordinations.append(coord_id)

        for coord_id in expired_coordinations:
            coord_data = self.coordination_state["active_coordinations"].pop(coord_id)
            coord_data["status"] = "timeout"
            self.coordination_state["coordination_history"].append(coord_data)
            self.stats["failed_coordinations"] += 1
            print(f"Coordination {coord_id} timed out")

    def get_protocol_stats(self) -> Dict[str, Any]:
        """Get current protocol statistics."""
        active_agents = sum(1 for agent in self.agents.values() if agent.status != AgentStatus.OFFLINE)
        busy_agents = sum(1 for agent in self.agents.values() if agent.status == AgentStatus.BUSY)

        return {
            "total_agents": len(self.agents),
            "active_agents": active_agents,
            "busy_agents": busy_agents,
            "idle_agents": active_agents - busy_agents,
            "messages_in_queue": len(self.message_queue),
            "active_coordinations": len(self.coordination_state["active_coordinations"]),
            "stats": self.stats.copy()
        }

    def simulate_workflow(self, workflow_steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate a multi-agent workflow for testing."""
        results = {
            "steps_completed": 0,
            "steps_failed": 0,
            "total_time": 0,
            "success_rate": 0.0
        }

        start_time = time.time()

        for step in workflow_steps:
            step_type = step.get("type")
            agent_id = step.get("agent")
            task_data = step.get("task_data", {})

            try:
                if step_type == "single_agent":
                    message_id = self.send_task_request(
                        requester="simulator",
                        target_agent=agent_id,
                        task_data=task_data
                    )
                    results["steps_completed"] += 1

                elif step_type == "multi_agent":
                    required_agents = step.get("required_agents", [])
                    coordination_id = self.coordinate_multi_agent_task(
                        coordinator="simulator",
                        task_data=task_data,
                        required_agents=required_agents
                    )
                    results["steps_completed"] += 1

                # Simulate processing time
                time.sleep(0.1)

            except Exception as e:
                print(f"Step failed: {e}")
                results["steps_failed"] += 1

        results["total_time"] = time.time() - start_time
        total_steps = results["steps_completed"] + results["steps_failed"]
        if total_steps > 0:
            results["success_rate"] = results["steps_completed"] / total_steps

        return results


def main():
    """Command line interface for multi-agent protocol."""
    parser = argparse.ArgumentParser(description='Multi-Agent Communication Protocol')
    parser.add_argument('--dir', default='.claude-patterns', help='Protocol directory')
    parser.add_argument('--action', choices=['register', 'unregister', 'stats', 'simulate', 'start', 'stop'],
                       default='stats', help='Action to perform')
    parser.add_argument('--agent-id', help='Agent ID')
    parser.add_argument('--agent-name', help='Agent name')
    parser.add_argument('--capabilities', nargs='+', help='Agent capabilities')

    args = parser.parse_args()

    protocol = MultiAgentProtocol(args.dir)

    if args.action == 'register':
        if not args.agent_id or not args.agent_name or not args.capabilities:
            print("Error: --agent-id, --agent-name, and --capabilities required for registration")
            return

        success = protocol.register_agent(args.agent_id, args.agent_name, args.capabilities)
        if success:
            print(f"Agent {args.agent_name} registered successfully")

    elif args.action == 'unregister':
        if not args.agent_id:
            print("Error: --agent-id required for unregistration")
            return

        success = protocol.unregister_agent(args.agent_id)
        if success:
            print(f"Agent {args.agent_id} unregistered successfully")

    elif args.action == 'stats':
        stats = protocol.get_protocol_stats()
        print("Multi-Agent Protocol Statistics")
        print("=" * 40)
        print(f"Total Agents: {stats['total_agents']}")
        print(f"Active Agents: {stats['active_agents']}")
        print(f"Busy Agents: {stats['busy_agents']}")
        print(f"Idle Agents: {stats['idle_agents']}")
        print(f"Messages in Queue: {stats['messages_in_queue']}")
        print(f"Active Coordinations: {stats['active_coordinations']}")
        print()
        print("Protocol Performance:")
        print(f"Messages Sent: {stats['stats']['messages_sent']}")
        print(f"Messages Received: {stats['stats']['messages_received']}")
        print(f"Successful Coordinations: {stats['stats']['successful_coordinations']}")
        print(f"Failed Coordinations: {stats['stats']['failed_coordinations']}")
        print(f"Agent Errors: {stats['stats']['agent_errors']}")
        print(f"Success Rate: {stats['stats']['success_rate']:.1%}")

    elif args.action == 'simulate':
        # Test workflow simulation
        workflow = [
            {
                "type": "single_agent",
                "agent": "code-analyzer",
                "task_data": {"task": "analyze_code", "file": "example.py"}
            },
            {
                "type": "multi_agent",
                "required_agents": ["code-analyzer", "quality-controller"],
                "task_data": {"task": "refactor_module", "module": "auth"}
            },
            {
                "type": "single_agent",
                "agent": "test-engineer",
                "task_data": {"task": "run_tests", "coverage": True}
            }
        ]

        print("Simulating multi-agent workflow...")
        results = protocol.simulate_workflow(workflow)
        print("Simulation Results:")
        print(f"Steps Completed: {results['steps_completed']}")
        print(f"Steps Failed: {results['steps_failed']}")
        print(f"Success Rate: {results['success_rate']:.1%}")
        print(f"Total Time: {results['total_time']:.2f}s")

    elif args.action == 'start':
        protocol.start_protocol_daemon()

    elif args.action == 'stop':
        protocol.stop_protocol_daemon()


if __name__ == "__main__":
    main()