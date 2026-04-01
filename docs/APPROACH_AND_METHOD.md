# Operational Approach and Methods

This document defines the underlying execution paradigm of the Autonomous Agent Plugin (v8.0.0+).

## The Four-Tier Coordination Method
We avoid monolithic decision making structures by compartmentalizing tasks into specialized execution groups:

1. **Group 1: Strategic Analysis** - Operates at a high-level abstraction. Uses the `Project Analysis` skills to map the user's workspace before making decisions.
2. **Group 2: The Orchestrator** - Takes the structural analysis and determines the required sequence of tool executions and subsequent routing protocols. 
3. **Group 3: Execution Engine** - Contains deterministic rules and highly localized shell commands. They carry out isolated steps without worrying about overall system alignment.
4. **Group 4: Quality & Validation** - Performs aggressive checking. They cross-verify the execution states against the initially proposed approach plan from Group 1.

## Stabilization & De-Risking Methods
With version 8.0.0, we prioritize stability over sheer feature output.
1. **Defunct Code Pruning:** Redundant fix scripts have been comprehensively pruned to strictly minimize API confusion.
2. **Standardized Communication:** `orchestrator.md` handles cross-agent sub-prompt delegation (extracted to Reference Skills), so no single generation sequence surpasses 128KB in context length arbitrarily.
3. **Immutable Source Pathing:** All internal Python libraries reference via strict environment variables `$CLAUDE_PLUGIN_ROOT`. Code explicitly never injects arbitrary strings into terminal evaluations without rigorous formatting.
