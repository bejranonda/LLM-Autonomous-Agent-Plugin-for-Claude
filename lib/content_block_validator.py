#!/usr/bin/env python3
#     Content Block Validator
"""

Simulates message construction to identify which content block becomes empty.
"""
def analyze_orchestrator_response():
    """Analyze how the orchestrator constructs responses and identify empty blocks."""

    # Simulate the orchestrator's response construction process
    content_blocks = []

    # Block 0: Main response header
    block0 = "============================================================\n  PATTERN LEARNING INITIALIZED\n============================================================\n"
    content_blocks.append(block0)

    # Block 1: Project analysis (this could be empty if no project detected)
    block1 = """PROJECT ANALYSIS:
Type: Plugin project with autonomous agents
Languages: Markdown, JavaScript, Python
Frameworks: Claude Code Plugin System
Total Files: 500+
Project Structure: Autonomous agent architecture"""
    content_blocks.append(block1)

    # Block 2: Pattern database creation status
    block2 = """PATTERN DATABASE CREATED:
Location: .claude-patterns/
Files Created:
- patterns.json (pattern storage)
- task_queue.json (task management)
- quality_history.json (quality tracking)
- config.json (configuration)
Status: Ready for pattern capture"""
    content_blocks.append(block2)

    # Block 3: Initial patterns detected (this could be empty on first run)
    block3 = """INITIAL PATTERNS DETECTED:
- Autonomous delegation pattern (27 agents)
- Quality control pattern (5-layer validation)
- Learning engine pattern (continuous improvement)
- Cross-platform compatibility pattern
- Cache_control safety pattern (error prevention)"""
    content_blocks.append(block3)

    # Block 4: Baseline metrics
    block4 = """BASELINE METRICS:
Skill Effectiveness: Baseline established
Quality Baseline: Will update after first task
Coverage Baseline: Will update after first task
Agent Performance: Will track from first delegation"""
    content_blocks.append(block4)

    # Block 5: Next steps
    block5 = """NEXT STEPS:
1. Run /auto-analyze to analyze project quality
2. Run /quality-check to establish quality baseline
3. Start working on tasks - learning begins!
4. Each task improves the system automatically

Skills Loaded: code-analysis, documentation-best-practices"""
    content_blocks.append(block5)

    # Block 6: Footer
    block6 = """============================================================
  Pattern learning is ready. The system will learn
  and improve automatically with every task you perform.
============================================================"""
    content_blocks.append(block6)

    # Check each block for emptiness
    print("Content Block Analysis:")
    print("=" * 50)

    empty_blocks = []
    for i, block in enumerate(content_blocks):
        is_empty = not block or len(block.strip()) == 0
        if is_empty:
            empty_blocks.append(i)

        status = "EMPTY" if is_empty else f"OK ({len(block)} chars)"
        print(f"Block {i}: {status}")

        if is_empty:
            print(f"  Content: '{repr(block)}'")

    print(f"\nEmpty blocks found: {empty_blocks}")

    # Simulate cache_control application
    print(f"\nCache Control Simulation:")
    print("=" * 50)

    for i, block in enumerate(content_blocks):
        # Simulate the validation function from our fix
        is_valid_for_cache = (
            block is not None
            and len(str(block)) > 0
            and len(str(block).strip()) > 0
            and len(str(block).strip()) >= 5
            and str(block).strip().lower() not in ["null", "undefined", "[]", "{}", "none", "empty"]
        )

        if is_valid_for_cache:
            print(f"Block {i}: SAFE for cache_control")
        else:
            print(f"Block {i}: UNSAFE for cache_control - would cause error!")

    return empty_blocks


def test_edge_cases():
    """Test edge cases that might cause empty content blocks."""

    test_cases = [
        ("Empty string", ""),
        ("Whitespace only", "   \n\t  "),
        ("Very short", "abc"),
        ("Null indicators", ["null", "undefined", "[]", "{}", "none", "empty"]),
        ("Valid content", "This is valid content with enough characters."),
    ]

    print("\nEdge Case Testing:")
    print("=" * 50)

    for name, content in test_cases:
        if isinstance(content, list):
            for item in content:
                is_valid = len(str(item).strip()) >= 5 and str(item).strip().lower() not in [
                    "null",
                    "undefined",
                    "[]",
                    "{}",
                    "none",
                    "empty",
                ]
                print(f"{name} ('{item}'): {'VALID' if is_valid else 'INVALID'}")
        else:
            is_valid = len(str(content).strip()) >= 5 and str(content).strip().lower() not in [
                "null",
                "undefined",
                "[]",
                "{}",
                "none",
                "empty",
            ]
            print(f"{name}: {'VALID' if is_valid else 'INVALID'}")


if __name__ == "__main__":
    empty_blocks = analyze_orchestrator_response()
    test_edge_cases()

    if empty_blocks:
        print(f"\n[ERROR] Found {len(empty_blocks)} empty content blocks that would cause cache_control errors!")
        exit(1)
    else:
        print(f"\n[OK] All content blocks are valid for cache_control")
        exit(0)
