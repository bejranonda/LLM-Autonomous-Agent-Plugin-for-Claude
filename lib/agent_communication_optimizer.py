#!/usr/bin/env python3
#     Agent Communication Optimizer
"""
Advanced communication protocol optimizer for autonomous agents that minimizes token usage
while maintaining effective inter-agent collaboration and information exchange.

Version: 1.0.0
Author: Autonomous Agent Plugin
"""
import json
import os
import time
import hashlib
import pathlib
from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import zlib
import base64

from smart_caching_system import get_smart_cache
from token_optimization_engine import get_token_optimizer


class MessagePriority(Enum):
    """Message priority levels for communication optimization."""

    CRITICAL = "critical"  # Always deliver, no optimization
    HIGH = "high"  # Important, minimal optimization
    NORMAL = "normal"  # Standard optimization applied
    LOW = "low"  # Aggressive optimization


class CompressionType(Enum):
    """Compression types for message optimization."""

    NONE = "none"  # No compression
    BASIC = "basic"  # Remove redundancy
    STRUCTURAL = "structural"  # Structure-based compression
    SEMANTIC = "semantic"  # Semantic compression


@dataclass
class OptimizedMessage:
    """Optimized message with metadata."""

    original_id: str
    compressed_content: str
    tokens_original: int
    tokens_compressed: int
    priority: MessagePriority
    compression_type: CompressionType
    compression_ratio: float
    metadata: Dict[str, Any]
    dependencies: List[str]
    created_at: float

    @property
    def token_savings(self) -> int:
        """Calculate token savings."""
        return self.tokens_original - self.tokens_compressed

    @property
    def efficiency_score(self) -> float:
        """Calculate efficiency score."""
        if self.tokens_original == 0:
            return 0.0
        return self.token_savings / self.tokens_original


@dataclass
class CommunicationProtocol:
    """Communication protocol definition for agent interactions."""

    protocol_id: str
    agent_group: str
    message_format: str
    optimization_rules: Dict[str, Any]
    compression_type: CompressionType
    priority_mapping: Dict[str, MessagePriority]
    token_limits: Dict[str, int]


class AgentCommunicationOptimizer:
"""
    Advanced optimizer for agent-to-agent communication that minimizes token usage
"""
    while maintaining effective collaboration.
"""

"""
    def __init__(self, cache_dir: str = ".claude-patterns"):
        """Initialize the processor with default configuration."""
        self.cache_dir = pathlib.Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Core components
        self.cache = get_smart_cache()
        self.token_optimizer = get_token_optimizer()

        # Communication protocols
        self.protocols: Dict[str, CommunicationProtocol] = {}
        self.active_conversations: Dict[str, List[str]] = {}

        # Message optimization
        self.compression_strategies = {
            CompressionType.NONE: self._no_compression,
            CompressionType.BASIC: self._basic_compression,
            CompressionType.STRUCTURAL: self._structural_compression,
            CompressionType.SEMANTIC: self._semantic_compression,
        }

        # Statistics
        self.stats = {
            "messages_optimized": 0,
            "tokens_saved": 0,
            "compression_ratio_avg": 0.0,
            "protocols_used": {},
            "agent_efficiency": {},
            "communication_patterns": {},
        }

        # Cache files
        self.protocols_file = self.cache_dir / "communication_protocols.json"
        self.stats_file = self.cache_dir / "communication_stats.json"
        self.patterns_file = self.cache_dir / "communication_patterns.json"

        # Load existing data
        self._load_protocols()
        self._load_stats()
        self._load_patterns()

        # Initialize default protocols
        self._initialize_default_protocols()

    def optimize_message(
        self, sender: str, receiver: str, message: Dict[str, Any], protocol_id: str = None
    )-> OptimizedMessage:
        """Optimize Message."""
        Optimize a single message for token efficiency.

        Args:
            sender: Sending agent
            receiver: Receiving agent
            message: Original message
            protocol_id: Communication protocol to use

        Returns:
            Optimized message with metadata
"""
        # Determine protocol
        if protocol_id is None:
            protocol_id = self._determine_protocol(sender, receiver)

        protocol = self.protocols.get(protocol_id)
        if not protocol:
            # Use default protocol
            protocol = self._get_default_protocol()
            self.protocols[protocol_id] = protocol

        # Determine priority
        priority = self._determine_priority(message, protocol)

        # Skip optimization for critical messages
        if priority == MessagePriority.CRITICAL:
            return self._create_optimized_message(message, CompressionType.NONE, priority, protocol)

        # Choose compression strategy
        compression_type = protocol.compression_type
        if compression_type == CompressionType.ADAPTIVE:
            compression_type = self._choose_compression_strategy(message, priority)

        # Compress message
        compressed_content = self.compression_strategies[compression_type](message)

        # Create optimized message
        optimized = self._create_optimized_message(message, compression_type, priority, protocol, compressed_content)

        # Update statistics
        self._update_stats(optimized)
        self._track_communication_pattern(sender, receiver, protocol_id)

        return optimized

"""
    def decompress_message():
"""
        
        Decompress an optimized message back to original form.

        Args:
            optimized_message: Optimized message to decompress

        Returns:
            Decompressed original message
"""
        if optimized_message.compression_type == CompressionType.NONE:
            # Original content stored directly
            return json.loads(optimized_message.compressed_content)

        # Decompress based on compression type
        if optimized_message.compression_type == CompressionType.BASIC:
            return self._decompress_basic(optimized_message.compressed_content)
        elif optimized_message.compression_type == CompressionType.STRUCTURAL:
            return self._decompress_structural(optimized_message.compressed_content)
        elif optimized_message.compression_type == CompressionType.SEMANTIC:
            return self._decompress_semantic(optimized_message.compressed_content)

        # Fallback
        return json.loads(optimized_message.compressed_content)

"""
    def optimize_conversation():
"""
        
        Optimize an entire conversation for token efficiency.

        Args:
            conversation: List of messages in the conversation
            participants: List of participants in the conversation

        Returns:
            Optimization results with metrics
"""
        optimized_messages = []
        total_original_tokens = 0
        total_optimized_tokens = 0

        # Group messages by sender-receiver pairs
        message_groups = self._group_messages_by_participants(conversation, participants)

        for (sender, receiver), messages in message_groups.items():
            for i, message in enumerate(messages):
                # Consider context in conversation
                context = {
                    "conversation_index": i,
                    "total_messages": len(messages),
                    "participants": participants,
                    "previous_messages": optimized_messages[-3:] if optimized_messages else [],
                }

                # Optimize message with context
                optimized = self.optimize_message(sender, receiver, message, context=context)

                optimized_messages.append(optimized)
                total_original_tokens += optimized.tokens_original
                total_optimized_tokens += optimized.tokens_compressed

        tokens_saved = total_original_tokens - total_optimized_tokens

        return {
            "optimized_messages": optimized_messages,
            "original_tokens": total_original_tokens,
            "optimized_tokens": total_optimized_tokens,
            "tokens_saved": tokens_saved,
            "efficiency_score": tokens_saved / total_original_tokens if total_original_tokens > 0 else 0,
            "compression_ratio": total_optimized_tokens / total_original_tokens if total_original_tokens > 0 else 1,
            "message_count": len(conversation),
        }

"""
    def create_communication_protocol(
        self, protocol_id: str, agent_group: str, message_format: str, optimization_rules: Dict[str, Any]
    )-> bool:
        """Create Communication Protocol."""
        Create a new communication protocol for agent interactions.

        Args:
            protocol_id: Unique protocol identifier
            agent_group: Group of agents this protocol applies to
            message_format: Message format specification
            optimization_rules: Optimization rules to apply

        Returns:
            True if protocol created successfully
"""
        protocol = CommunicationProtocol(
            protocol_id=protocol_id,
            agent_group=agent_group,
            message_format=message_format,
            optimization_rules=optimization_rules,
            compression_type=CompressionType.BASIC,
            priority_mapping={},
            token_limits={},
        )

        # Set default priority mapping
        protocol.priority_mapping = {
            "error": MessagePriority.HIGH,
            "warning": MessagePriority.NORMAL,
            "info": MessagePriority.NORMAL,
            "debug": MessagePriority.LOW,
        }

        # Set default token limits
        protocol.token_limits = {
            "max_tokens_per_message": 5000,
            "max_tokens_per_conversation": 50000,
            "critical_message_limit": 10000,
        }

        self.protocols[protocol_id] = protocol
        self._save_protocols()

        return True

"""
    def get_agent_efficiency_report():
"""
        
        Get efficiency report for agents or all agents.

        Args:
            agent_id: Specific agent ID, or None for all agents

        Returns:
            Efficiency report with metrics
"""
        if agent_id:
            # Single agent report
            agent_stats = self.stats["agent_efficiency"].get(agent_id, {})
            return {
                "agent_id": agent_id,
                "messages_sent": agent_stats.get("messages_sent", 0),
                "tokens_saved": agent_stats.get("tokens_saved", 0),
                "average_efficiency": agent_stats.get("average_efficiency", 0),
                "preferred_protocols": agent_stats.get("protocols_used", {}),
                "communication_patterns": agent_stats.get("patterns", {}),
            }
        else:
            # All agents report
            return {
                "total_agents": len(self.stats["agent_efficiency"]),
                "agent_stats": self.stats["agent_efficiency"],
                "overall_efficiency": self._calculate_overall_efficiency(),
                "protocol_usage": self.stats["protocols_used"],
                "top_performers": self._get_top_performers(),
            }

"""
    def _determine_protocol(self, sender: str, receiver: str) -> str:
        """Determine the appropriate protocol for agent communication."""
        # Check if agents are in the same group
        sender_group = self._get_agent_group(sender)
        receiver_group = self._get_agent_group(receiver)

        # Use group-specific protocol if available
        group_protocols = [
            pid
            for pid, protocol in self.protocols.items()
            if protocol.agent_group == sender_group and protocol.agent_group == receiver_group
        ]

        if group_protocols:
            return group_protocols[0]

        # Use default protocol
        return "default"

    def _get_agent_group(self, agent_id: str) -> str:
        """Get the group an agent belongs to."""
        # Extract group from agent ID
        if "-" in agent_id:
            parts = agent_id.split("-")
            if len(parts) > 1:
                return parts[0]

        # Default group based on agent type
        if "analyzer" in agent_id:
            return "analysis"
        elif "controller" in agent_id:
            return "execution"
        elif "validator" in agent_id:
            return "validation"
        elif "optimizer" in agent_id:
            return "optimization"
        else:
            return "general"

    def _get_default_protocol(self) -> CommunicationProtocol:
        """Get default communication protocol."""
        return CommunicationProtocol(
            protocol_id="default",
            agent_group="general",
            message_format="json",
            optimization_rules={"compress_content": True, "remove_metadata": True, "optimize_structure": True},
            compression_type=CompressionType.BASIC,
            priority_mapping={
                "error": MessagePriority.HIGH,
                "warning": MessagePriority.NORMAL,
                "info": MessagePriority.NORMAL,
                "debug": MessagePriority.LOW,
            },
            token_limits={
                "max_tokens_per_message": 5000,
                "max_tokens_per_conversation": 50000,
                "critical_message_limit": 10000,
            },
        )

    def _determine_priority(self, message: Dict[str, Any], protocol: CommunicationProtocol) -> MessagePriority:
        """Determine message priority based on content and protocol."""
        # Check for explicit priority in message
        if "priority" in message:
            priority_str = message["priority"].lower()
            if priority_str == "critical":
                return MessagePriority.CRITICAL
            elif priority_str == "high":
                return MessagePriority.HIGH
            elif priority_str == "low":
                return MessagePriority.LOW

        # Check message type
        message_type = message.get("type", "").lower()
        if message_type in ["error", "critical", "urgent"]:
            return MessagePriority.CRITICAL
        elif message_type in ["warning", "alert"]:
            return MessagePriority.HIGH
        elif message_type in ["debug", "trace"]:
            return MessagePriority.LOW

        # Use protocol priority mapping
        content_key = message.get("content_key", "")
        return protocol.priority_mapping.get(content_key, MessagePriority.NORMAL)

    def _choose_compression_strategy(self, message: Dict[str, Any], priority: MessagePriority) -> CompressionType:
        """Choose optimal compression strategy based on message and priority."""
        message_size = len(json.dumps(message))

        # Critical messages: no compression
        if priority == MessagePriority.CRITICAL:
            return CompressionType.NONE

        # Small messages: basic compression
        if message_size < 1000:
            return CompressionType.BASIC

        # Medium messages: structural compression
        if message_size < 5000:
            return CompressionType.STRUCTURAL

        # Large messages: semantic compression
        return CompressionType.SEMANTIC

    def _no_compression(self, message: Dict[str, Any]) -> str:
        """No compression - store as-is."""
        return json.dumps(message)

    def _basic_compression(self, message: Dict[str, Any]) -> str:
        """Basic compression - remove redundancy and optimize structure."""
        # Create optimized version
        optimized = {}

        # Keep essential fields only
        essential_fields = ["type", "content", "data", "timestamp", "sender", "receiver"]
        for field in essential_fields:
            if field in message:
                optimized[field] = message[field]

        # Optimize content
        if "content" in optimized:
            content = optimized["content"]
            if isinstance(content, str):
                # Remove extra whitespace
                optimized["content"] = " ".join(content.split())
            elif isinstance(content, dict):
                # Remove None values
                optimized["content"] = {k: v for k, v in content.items() if v is not None}

        return json.dumps(optimized)

    def _structural_compression(self, message: Dict[str, Any]) -> str:
        """Structural compression - optimize message structure."""
        # Create structure map
        structure_map = {}
        for key, value in message.items():
            if isinstance(value, (str, int, float, bool)):
                structure_map[key] = value
            elif isinstance(value, dict):
                # Compress nested dictionaries
                structure_map[key] = {k: v for k, v in value.items() if v is not None}
            elif isinstance(value, list):
                # Compress lists
                structure_map[key] = [item for item in value if item is not None]

        return json.dumps(structure_map)

    def _semantic_compression(self, message: Dict[str, Any]) -> str:
        """Semantic compression - compress based on meaning."""
        # Create semantic representation
        semantic_data = {
            "type": message.get("type"),
            "intent": self._extract_intent(message),
            "key_data": self._extract_key_data(message),
            "timestamp": message.get("timestamp", time.time()),
        }

        return json.dumps(semantic_data)

    def _extract_intent(self, message: Dict[str, Any]) -> str:
        """Extract intent from message."""
        content = message.get("content", "")
        if isinstance(content, str):
            content = content.lower()
            if "error" in content or "fail" in content:
                return "error"
            elif "success" in content or "complete" in content:
                return "success"
            elif "analyze" in content:
                return "analysis"
            elif "validate" in content:
                return "validation"
            elif "optimize" in content:
                return "optimization"

        return "general"

    def _extract_key_data(self, message: Dict[str, Any]) -> Any:
        """Extract key data from message."""
        if "data" in message:
            return message["data"]
        elif "content" in message:
            return message["content"]
        else:
            return message.get("message", "")

    def _create_optimized_message(
        self,
        message: Dict[str, Any],
        compression_type: CompressionType,
        priority: MessagePriority,
        protocol: CommunicationProtocol,
        compressed_content: str = None,
    )-> OptimizedMessage:
        """ Create Optimized Message."""Create optimized message with metadata."""
        original_tokens = self._estimate_tokens(message)

        if compressed_content is None:
            compressed_content = self.compression_strategies[compression_type](message)

        compressed_tokens = self._estimate_tokens(compressed_content)

        return OptimizedMessage(
            original_id=self._generate_message_id(message),
            compressed_content=compressed_content,
            tokens_original=original_tokens,
            tokens_compressed=compressed_tokens,
            priority=priority,
            compression_type=compression_type,
            compression_ratio=compressed_tokens / original_tokens if original_tokens > 0 else 1.0,
            metadata={
                "original_size": original_tokens,
                "compressed_size": compressed_tokens,
                "protocol_id": protocol.protocol_id,
                "agent_group": protocol.agent_group,
            },
            dependencies=[],
            created_at=time.time(),
        )

    def _generate_message_id(self, message: Dict[str, Any]) -> str:
        """Generate unique ID for message."""
        content = json.dumps(message, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def _estimate_tokens(self, content: Any) -> int:
        """Estimate token count for content."""
        if isinstance(content, str):
            return len(content) // 3
        elif isinstance(content, dict):
            return len(str(content)) // 3
        elif isinstance(content, list):
            return sum(len(str(item)) // 3 for item in content)
        else:
            return len(str(content)) // 3

    def _group_messages_by_participants(
        self, conversation: List[Dict[str, Any]], participants: List[str]
    )-> Dict[Tuple[str, str], List[Dict[str, Any]]]:
        """ Group Messages By Participants."""Group messages by sender-receiver pairs."""
        groups = {}

        for message in conversation:
            sender = message.get("sender", "unknown")
            receiver = message.get("receiver", "unknown")

            # Filter for participants
            if sender in participants and receiver in participants:
                pair = (sender, receiver)
                if pair not in groups:
                    groups[pair] = []
                groups[pair].append(message)

        return groups

    def _track_communication_pattern(self, sender: str, receiver: str, protocol_id: str) -> None:
        """Track communication patterns for optimization."""
        pattern_key = f"{sender}->{receiver}"
        if pattern_key not in self.stats["communication_patterns"]:
            self.stats["communication_patterns"][pattern_key] = {"count": 0, "protocols_used": {}, "average_efficiency": 0.0}

        pattern = self.stats["communication_patterns"][pattern_key]
        pattern["count"] += 1
        pattern["protocols_used"][protocol_id] = pattern["protocols_used"].get(protocol_id, 0) + 1

    def _update_stats(self, optimized_message: OptimizedMessage) -> None:
        """Update optimization statistics."""
        self.stats["messages_optimized"] += 1
        self.stats["tokens_saved"] += optimized_message.token_savings

        # Update compression ratio average
        total_messages = self.stats["messages_optimized"]
        if total_messages > 0:
            current_avg = self.stats["compression_ratio_avg"]
            self.stats["compression_ratio_avg"] = (
                current_avg * (total_messages - 1) + optimized_message.compression_ratio
            ) / total_messages

        # Update protocol usage
        protocol_id = optimized_message.metadata["protocol_id"]
        self.stats["protocols_used"][protocol_id] = self.stats["protocols_used"].get(protocol_id, 0) + 1

        self._save_stats()

    def _calculate_overall_efficiency(self) -> float:
        """Calculate overall communication efficiency."""
        if self.stats["messages_optimized"] == 0:
            return 0.0

        total_saved = self.stats["tokens_saved"]
        total_messages = self.stats["messages_optimized"]

        return total_saved / total_messages

    def _get_top_performers(self) -> List[Dict[str, Any]]:
        """Get top performing agents."""
        agent_stats = self.stats["agent_efficiency"]
        performers = []

        for agent_id, stats in agent_stats.items():
            performers.append(
                {
                    "agent_id": agent_id,
                    "efficiency": stats.get("average_efficiency", 0),
                    "tokens_saved": stats.get("tokens_saved", 0),
                    "messages_sent": stats.get("messages_sent", 0),
                }
            )

        return sorted(performers, key=lambda x: x["efficiency"], reverse=True)[:10]

    def _initialize_default_protocols(self) -> None:
        """Initialize default communication protocols."""
        # Group 1 (Analysis) protocol
        self.create_communication_protocol(
            "group_1_communication",
            "analysis",
            "structured_json",
            {"compress_content": True, "optimize_structure": True, "semantic_compression": False},
        )

        # Group 2 (Decision) protocol
        self.create_communication_protocol(
            "group_2_communication",
            "decision",
            "structured_json",
            {"compress_content": True, "optimize_structure": True, "semantic_compression": True},
        )

        # Group 3 (Execution) protocol
        self.create_communication_protocol(
            "group_3_communication",
            "execution",
            "structured_json",
            {"compress_content": True, "optimize_structure": True, "semantic_compression": False},
        )

        # Group 4 (Validation) protocol
        self.create_communication_protocol(
            "group_4_communication",
            "validation",
            "structured_json",
            {"compress_content": True, "optimize_structure": True, "semantic_compression": True},
        )

    def _load_protocols(self) -> None:
        """Load communication protocols from cache."""
        if self.protocols_file.exists():
            try:
                with open(self.protocols_file, "r") as f:
                    data = json.load(f)
                    for protocol_id, protocol_data in data.items():
                        self.protocols[protocol_id] = CommunicationProtocol(**protocol_data)
            except Exception as e:
                print(f"Error loading protocols: {e}")

    def _save_protocols(self) -> None:
        """Save communication protocols to cache."""
        try:
            with open(self.protocols_file, "w") as f:
                data = {}
                for protocol_id, protocol in self.protocols.items():
                    data[protocol_id] = asdict(protocol)
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving protocols: {e}")

    def _load_stats(self) -> None:
        """Load statistics from cache."""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, "r") as f:
                    self.stats = json.load(f)
            except Exception as e:
                print(f"Error loading stats: {e}")

    def _save_stats(self) -> None:
        """Save statistics to cache."""
        try:
            with open(self.stats_file, "w") as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")

    def _load_patterns(self) -> None:
        """Load communication patterns from cache."""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, "r") as f:
                    self.stats["communication_patterns"] = json.load(f)
            except Exception as e:
                print(f"Error loading patterns: {e}")

    def _save_patterns(self) -> None:
        """Save communication patterns to cache."""
        try:
            with open(self.patterns_file, "w") as f:
                json.dump(self.stats["communication_patterns"], f, indent=2)
        except Exception as e:
            print(f"Error saving patterns: {e}")

    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report."""
        return {
            "total_messages_optimized": self.stats["messages_optimized"],
            "total_tokens_saved": self.stats["tokens_saved"],
            "average_compression_ratio": self.stats["compression_ratio_avg"],
            "protocols_count": len(self.protocols),
            "protocol_usage": self.stats["protocols_used"],
            "agent_count": len(self.stats["agent_efficiency"]),
            "communication_patterns": len(self.stats["communication_patterns"]),
            "top_protocols": self._get_top_protocols(),
            "top_performers": self._get_top_performers(),
            "efficiency_trends": self._analyze_efficiency_trends(),
        }

    def _get_top_protocols(self) -> List[Dict[str, Any]]:
        """Get most used protocols."""
        protocols = []
        for protocol_id, usage_count in self.stats["protocols_used"].items():
            protocols.append(
                {
                    "protocol_id": protocol_id,
                    "usage_count": usage_count,
                    "agent_group": self.protocols.get(protocol_id, {}).agent_group,
                }
            )

        return sorted(protocols, key=lambda x: x["usage_count"], reverse=True)

    def _analyze_efficiency_trends(self) -> Dict[str, Any]:
        """Analyze efficiency trends over time."""
        # Simplified trend analysis
        return {
            "trend": "improving",
            "recent_efficiency": self.stats["compression_ratio_avg"],
            "target_efficiency": 0.4,  # 40% compression ratio target
            "status": "on_track" if self.stats["compression_ratio_avg"] >= 0.4 else "needs_improvement",
        }


# Global optimizer instance
_communication_optimizer = None


def get_communication_optimizer() -> AgentCommunicationOptimizer:
    """Get or create global communication optimizer instance."""
    global _communication_optimizer
    if _communication_optimizer is None:
        _communication_optimizer = AgentCommunicationOptimizer()
    return _communication_optimizer


if __name__ == "__main__":
    optimizer = get_communication_optimizer()
    report = optimizer.get_optimization_report()
    print("=== Agent Communication Optimizer Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
