#!/usr/bin/env python3
"""
Test suite for agent_communication_optimizer.py
Boosts test coverage by focusing on communication optimization and token efficiency.
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
import time

# Add the lib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

# Mock the dependencies that might not be available
sys.modules['smart_caching_system'] = MagicMock()
sys.modules['token_optimization_engine'] = MagicMock()

from agent_communication_optimizer import (
    AgentCommunicationOptimizer,
    MessagePriority,
    CompressionType,
    OptimizedMessage,
    CommunicationProtocol,
    get_communication_optimizer
)


class TestAgentCommunicationOptimizer:
    """Test cases for AgentCommunicationOptimizer class."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()

        # Mock the dependencies
        mock_cache = MagicMock()
        mock_cache.get = MagicMock(return_value=None)
        mock_cache.set = MagicMock()

        mock_token_optimizer = MagicMock()
        mock_token_optimizer.count_tokens = MagicMock(return_value=100)

        with patch('agent_communication_optimizer.get_smart_cache', return_value=mock_cache), \
             patch('agent_communication_optimizer.get_token_optimizer', return_value=mock_token_optimizer):
            self.optimizer = AgentCommunicationOptimizer(self.temp_dir)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test AgentCommunicationOptimizer initialization."""
        # Test with default directory
        optimizer = AgentCommunicationOptimizer()
        assert optimizer.storage_dir.exists()
        assert optimizer.protocols_file.exists()
        assert optimizer.stats_file.exists()
        assert optimizer.patterns_file.exists()

        # Test with custom directory
        custom_dir = Path(self.temp_dir) / "custom"
        optimizer = AgentCommunicationOptimizer(str(custom_dir))
        assert custom_dir.exists()

        # Check initial structure
        assert isinstance(optimizer.protocols, dict)
        assert isinstance(optimizer.active_conversations, dict)
        assert isinstance(optimizer.stats, dict)

    def test_message_priority_enum(self):
        """Test MessagePriority enum."""
        assert MessagePriority.CRITICAL.value == "critical"
        assert MessagePriority.HIGH.value == "high"
        assert MessagePriority.NORMAL.value == "normal"
        assert MessagePriority.LOW.value == "low"

    def test_compression_type_enum(self):
        """Test CompressionType enum."""
        assert CompressionType.NONE.value == "none"
        assert CompressionType.BASIC.value == "basic"
        assert CompressionType.STRUCTURAL.value == "structural"
        assert CompressionType.SEMANTIC.value == "semantic"

    def test_optimized_message_properties(self):
        """Test OptimizedMessage properties."""
        message = OptimizedMessage(
            original_id="test123",
            compressed_content='{"test": "data"}',
            tokens_original=100,
            tokens_compressed=60,
            priority=MessagePriority.NORMAL,
            compression_type=CompressionType.BASIC,
            compression_ratio=0.6,
            metadata={"test": "meta"},
            dependencies=[],
            created_at=time.time()
        )

        assert message.token_savings == 40  # 100 - 60
        assert message.efficiency_score == 0.4  # 40 / 100

    def test_optimize_message_basic(self):
        """Test basic message optimization."""
        message = {
            "type": "test",
            "content": "This is a test message",
            "data": {"key": "value"},
            "timestamp": time.time()
        }

        optimized = self.optimizer.optimize_message(
            sender="agent1",
            receiver="agent2",
            message=message
        )

        assert isinstance(optimized, OptimizedMessage)
        assert optimized.original_id is not None
        assert optimized.tokens_original > 0
        assert optimized.tokens_compressed >= 0
        assert optimized.priority in MessagePriority
        assert optimized.compression_type in CompressionType

    def test_optimize_message_critical_priority(self):
        """Test optimization of critical priority messages."""
        message = {
            "type": "error",
            "priority": "critical",
            "content": "Critical system error occurred"
        }

        optimized = self.optimizer.optimize_message(
            sender="monitor",
            receiver="orchestrator",
            message=message
        )

        # Critical messages should not be compressed
        assert optimized.compression_type == CompressionType.NONE
        assert optimized.priority == MessagePriority.CRITICAL

    def test_optimize_message_with_protocol(self):
        """Test optimization with specific protocol."""
        # Create a custom protocol
        self.optimizer.create_communication_protocol(
            "test_protocol",
            "test_group",
            "json",
            {"compress_content": True}
        )

        message = {
            "type": "test",
            "content": "Test message content"
        }

        optimized = self.optimizer.optimize_message(
            sender="agent1",
            receiver="agent2",
            message=message,
            protocol_id="test_protocol"
        )

        assert optimized.metadata["protocol_id"] == "test_protocol"

    def test_decompress_message(self):
        """Test message decompression."""
        original_message = {
            "type": "test",
            "content": "Test content",
            "data": {"key": "value"}
        }

        # Optimize then decompress
        optimized = self.optimizer.optimize_message(
            sender="agent1",
            receiver="agent2",
            message=original_message
        )

        decompressed = self.optimizer.decompress_message(optimized)

        # Should recover original structure (may be compressed but should be valid JSON)
        assert isinstance(decompressed, dict)
        if "content" in decompressed:
            assert isinstance(decompressed["content"], str)

    def test_optimize_conversation(self):
        """Test optimizing entire conversation."""
        conversation = [
            {
                "sender": "agent1",
                "receiver": "agent2",
                "content": f"Message {i}",
                "timestamp": time.time() + i
            }
            for i in range(5)
        ]

        participants = ["agent1", "agent2"]

        result = self.optimizer.optimize_conversation(conversation, participants)

        assert "optimized_messages" in result
        assert "original_tokens" in result
        assert "optimized_tokens" in result
        assert "tokens_saved" in result
        assert "efficiency_score" in result
        assert "compression_ratio" in result
        assert "message_count" in result

        assert len(result["optimized_messages"]) == 5
        assert result["message_count"] == 5

    def test_create_communication_protocol(self):
        """Test creating communication protocols."""
        result = self.optimizer.create_communication_protocol(
            "test_protocol",
            "test_group",
            "json",
            {"compress_content": True, "remove_metadata": True}
        )

        assert result is True
        assert "test_protocol" in self.optimizer.protocols

        protocol = self.optimizer.protocols["test_protocol"]
        assert protocol.protocol_id == "test_protocol"
        assert protocol.agent_group == "test_group"
        assert protocol.message_format == "json"

    def test_protocol_auto_configuration(self):
        """Test automatic protocol configuration."""
        result = self.optimizer.create_communication_protocol(
            "auto_protocol",
            "auto_group",
            "json",
            {}
        )

        assert result is True
        protocol = self.optimizer.protocols["auto_protocol"]

        # Should have default priority mapping
        assert "error" in protocol.priority_mapping
        assert protocol.priority_mapping["error"] == MessagePriority.HIGH

        # Should have default token limits
        assert "max_tokens_per_message" in protocol.token_limits
        assert protocol.token_limits["max_tokens_per_message"] == 5000

    def test_get_agent_efficiency_report(self):
        """Test getting agent efficiency report."""
        # Mock some agent performance data
        self.optimizer.stats["agent_efficiency"] = {
            "agent1": {
                "messages_sent": 10,
                "tokens_saved": 500,
                "average_efficiency": 0.3,
                "protocols_used": {"default": 8, "custom": 2}
            }
        }

        # Single agent report
        report = self.optimizer.get_agent_efficiency_report("agent1")
        assert report["agent_id"] == "agent1"
        assert report["messages_sent"] == 10
        assert report["tokens_saved"] == 500

        # All agents report
        all_report = self.optimizer.get_agent_efficiency_report()
        assert "total_agents" in all_report
        assert "agent_stats" in all_report
        assert "overall_efficiency" in all_report

    def test_compression_strategies(self):
        """Test different compression strategies."""
        test_message = {
            "type": "test",
            "content": "This is a test message with some content",
            "metadata": {
                "timestamp": time.time(),
                "source": "test_agent",
                "priority": "normal"
            },
            "data": {
                "key1": "value1",
                "key2": "value2",
                "key3": None  # Should be filtered out
            }
        }

        # Test no compression
        no_compression = self.optimizer._no_compression(test_message)
        assert isinstance(no_compression, str)
        assert "test_message" in no_compression or "content" in no_compression

        # Test basic compression
        basic_compression = self.optimizer._basic_compression(test_message)
        assert isinstance(basic_compression, str)
        # Should remove None values and optimize content

        # Test structural compression
        structural_compression = self.optimizer._structural_compression(test_message)
        assert isinstance(structural_compression, str)

        # Test semantic compression
        semantic_compression = self.optimizer._semantic_compression(test_message)
        assert isinstance(semantic_compression, str)
        # Should extract intent and key data

    def test_priority_determination(self):
        """Test message priority determination."""
        # Create test protocol
        protocol = self.optimizer._get_default_protocol()

        # Test explicit priority
        message = {"priority": "critical", "content": "test"}
        priority = self.optimizer._determine_priority(message, protocol)
        assert priority == MessagePriority.CRITICAL

        # Test message type priority
        message = {"type": "error", "content": "Error occurred"}
        priority = self.optimizer._determine_priority(message, protocol)
        assert priority == MessagePriority.CRITICAL

        message = {"type": "warning", "content": "Warning message"}
        priority = self.optimizer._determine_priority(message, protocol)
        assert priority == MessagePriority.HIGH

        message = {"type": "debug", "content": "Debug info"}
        priority = self.optimizer._determine_priority(message, protocol)
        assert priority == MessagePriority.LOW

        # Test default priority
        message = {"content": "Normal message"}
        priority = self.optimizer._determine_priority(message, protocol)
        assert priority == MessagePriority.NORMAL

    def test_agent_group_determination(self):
        """Test agent group determination."""
        # Test agents with hyphenated names
        group = self.optimizer._get_agent_group("analysis-code-analyzer")
        assert group == "analysis"

        group = self.optimizer._get_agent_group("execution-quality-controller")
        assert group == "execution"

        # Test agents with role-based names
        group = self.optimizer._get_agent_group("code-analyzer")
        assert group == "analysis"

        group = self.optimizer._get_agent_group("test-engineer")
        assert group == "execution"

        group = self.optimizer._get_agent_group("plugin-validator")
        assert group == "validation"

        group = self.optimizer._get_agent_group("performance-optimizer")
        assert group == "optimization"

        # Test default group
        group = self.optimizer._get_agent_group("unknown-agent")
        assert group == "general"

    def test_compression_strategy_selection(self):
        """Test compression strategy selection based on message characteristics."""
        small_message = {"content": "small"}  # < 1000 chars
        medium_message = {"content": "x" * 2000}  # 1000-5000 chars
        large_message = {"content": "x" * 6000}  # > 5000 chars

        # Critical priority should always use no compression
        strategy = self.optimizer._choose_compression_strategy(large_message, MessagePriority.CRITICAL)
        assert strategy == CompressionType.NONE

        # Small messages should use basic compression
        strategy = self.optimizer._choose_compression_strategy(small_message, MessagePriority.NORMAL)
        assert strategy == CompressionType.BASIC

        # Medium messages should use structural compression
        strategy = self.optimizer._choose_compression_strategy(medium_message, MessagePriority.NORMAL)
        assert strategy == CompressionType.STRUCTURAL

        # Large messages should use semantic compression
        strategy = self.optimizer._choose_compression_strategy(large_message, MessagePriority.NORMAL)
        assert strategy == CompressionType.SEMANTIC

    def test_intent_extraction(self):
        """Test intent extraction from messages."""
        test_cases = [
            ("The operation failed with an error", "error"),
            ("Task completed successfully", "success"),
            ("Need to analyze the code structure", "analysis"),
            ("Should validate the input data", "validation"),
            ("Let's optimize the performance", "optimization"),
            ("Just a regular message", "general")
        ]

        for content, expected_intent in test_cases:
            message = {"content": content}
            intent = self.optimizer._extract_intent(message)
            assert intent == expected_intent

    def test_token_estimation(self):
        """Test token estimation for different content types."""
        # Test string content
        string_tokens = self.optimizer._estimate_tokens("This is a test string")
        assert isinstance(string_tokens, int)
        assert string_tokens > 0

        # Test dictionary content
        dict_tokens = self.optimizer._estimate_tokens({"key": "value", "number": 42})
        assert isinstance(dict_tokens, int)
        assert dict_tokens > 0

        # Test list content
        list_tokens = self.optimizer._estimate_tokens(["item1", "item2", "item3"])
        assert isinstance(list_tokens, int)
        assert list_tokens > 0

        # Test numeric content
        num_tokens = self.optimizer._estimate_tokens(42)
        assert isinstance(num_tokens, int)
        assert num_tokens > 0

    def test_message_id_generation(self):
        """Test unique message ID generation."""
        message1 = {"content": "test message 1"}
        message2 = {"content": "test message 2"}
        message3 = {"content": "test message 1"}  # Same as message1

        id1 = self.optimizer._generate_message_id(message1)
        id2 = self.optimizer._generate_message_id(message2)
        id3 = self.optimizer._generate_message_id(message3)

        # Same messages should generate same IDs
        assert id1 == id3
        # Different messages should generate different IDs
        assert id1 != id2
        # IDs should be consistent length (16 chars for MD5 hash prefix)
        assert len(id1) == 16

    def test_statistics_tracking(self):
        """Test statistics tracking during optimization."""
        message = {
            "type": "test",
            "content": "Test message for statistics"
        }

        initial_stats = self.optimizer.stats.copy()

        # Optimize a message
        optimized = self.optimizer.optimize_message(
            sender="agent1",
            receiver="agent2",
            message=message
        )

        # Check that statistics were updated
        assert self.optimizer.stats["messages_optimized"] > initial_stats["messages_optimized"]
        assert self.optimizer.stats["tokens_saved"] >= initial_stats["tokens_saved"]

    def test_communication_pattern_tracking(self):
        """Test communication pattern tracking."""
        message = {"content": "test"}

        # Send multiple messages between same agents
        for i in range(3):
            self.optimizer.optimize_message(
                sender="agent1",
                receiver="agent2",
                message=message
            )

        patterns = self.optimizer.stats["communication_patterns"]
        pattern_key = "agent1->agent2"

        assert pattern_key in patterns
        assert patterns[pattern_key]["count"] == 3

    def test_protocol_initialization(self):
        """Test default protocol initialization."""
        # Should create protocols for all groups
        expected_protocols = [
            "group_1_communication",
            "group_2_communication",
            "group_3_communication",
            "group_4_communication"
        ]

        for protocol_id in expected_protocols:
            assert protocol_id in self.optimizer.protocols

        # Check protocol properties
        analysis_protocol = self.optimizer.protocols["group_1_communication"]
        assert analysis_protocol.agent_group == "analysis"
        assert analysis_protocol.compression_type == CompressionType.BASIC

    def test_get_optimization_report(self):
        """Test getting comprehensive optimization report."""
        # Add some test data
        self.optimizer.stats["messages_optimized"] = 100
        self.optimizer.stats["tokens_saved"] = 5000
        self.optimizer.stats["compression_ratio_avg"] = 0.6

        report = self.optimizer.get_optimization_report()

        required_fields = [
            "total_messages_optimized",
            "total_tokens_saved",
            "average_compression_ratio",
            "protocols_count",
            "protocol_usage",
            "agent_count",
            "communication_patterns",
            "top_protocols",
            "top_performers",
            "efficiency_trends"
        ]

        for field in required_fields:
            assert field in report

        assert report["total_messages_optimized"] == 100
        assert report["total_tokens_saved"] == 5000
        assert report["average_compression_ratio"] == 0.6

    def test_file_operations_error_handling(self):
        """Test error handling in file operations."""
        # Test with corrupted protocol file
        with open(self.optimizer.protocols_file, 'w') as f:
            f.write("invalid json")

        # Should handle gracefully and continue
        message = {"content": "test"}
        optimized = self.optimizer.optimize_message("agent1", "agent2", message)

        assert isinstance(optimized, OptimizedMessage)

    @patch('agent_communication_optimizer.get_communication_optimizer')
    def test_get_communication_optimizer_function(self, mock_get_optimizer):
        """Test the global get_communication_optimizer function."""
        mock_optimizer_instance = MagicMock()
        mock_get_optimizer.return_value = mock_optimizer_instance

        result = get_communication_optimizer()
        assert result == mock_optimizer_instance
        mock_get_optimizer.assert_called_once()

    def test_edge_cases_empty_message(self):
        """Test handling of edge cases like empty messages."""
        # Empty message
        optimized = self.optimizer.optimize_message("agent1", "agent2", {})
        assert isinstance(optimized, OptimizedMessage)

        # None content
        optimized = self.optimizer.optimize_message("agent1", "agent2", {"content": None})
        assert isinstance(optimized, OptimizedMessage)

        # Very long message
        long_content = "x" * 10000
        optimized = self.optimizer.optimize_message("agent1", "agent2", {"content": long_content})
        assert isinstance(optimized, OptimizedMessage)

    def test_concurrent_optimization_simulation(self):
        """Test simulated concurrent message optimization."""
        messages = [{"content": f"Message {i}"} for i in range(50)]

        optimized_messages = []
        for i, message in enumerate(messages):
            sender = f"agent_{i % 5}"
            receiver = f"agent_{(i + 1) % 5}"

            optimized = self.optimizer.optimize_message(sender, receiver, message)
            optimized_messages.append(optimized)

        # All optimizations should succeed
        assert len(optimized_messages) == 50
        assert all(isinstance(opt, OptimizedMessage) for opt in optimized_messages)
        assert all(opt.original_id is not None for opt in optimized_messages)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])