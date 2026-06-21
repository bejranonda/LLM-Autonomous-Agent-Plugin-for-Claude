# Documentation Index

This directory contains organized documentation for the Autonomous Agent Plugin (v8.4.5). For the most current version, always check the [root `CHANGELOG.md`](../CHANGELOG.md) and [`plugin.json`](../.claude-plugin/plugin.json).

## Directory Structure

### `docs/guidelines/` - Operational Guidelines and Best Practices
- [`BRAIN_MCP_INTEGRATION_GUIDELINES.md`](guidelines/BRAIN_MCP_INTEGRATION_GUIDELINES.md) - External Brain MCP server integration protocol, retrieval-path differences, classifier guardrails, recovery procedures (v8.4.5)
- [`SESSION_START_CHECKLIST.md`](guidelines/SESSION_START_CHECKLIST.md) - Pre-flight checks for new sessions: Brain MCP probe, validator sweep, release readiness, plugin reload (v8.4.5)
- [`RESULT_PRESENTATION_GUIDELINES.md`](guidelines/RESULT_PRESENTATION_GUIDELINES.md) - Two-tier result presentation standards for slash commands (terminal summary + file report)
- [`MODEL_COMMUNICATION_GUIDELINE.md`](guidelines/MODEL_COMMUNICATION_GUIDELINE.md) - Cross-model communication standards and capability adaptation
- [`prompt-agent-creating.md`](guidelines/prompt-agent-creating.md) - Guide for creating new agents

### `docs/release-notes/` - Release Notes (v6.0+)
- [`RELEASE_NOTES.md`](release-notes/RELEASE_NOTES.md) - General release notes index
- [`RELEASE_NOTES_v8.4.5.md`](release-notes/RELEASE_NOTES_v8.4.5.md) - Latest release (quality metric correctness, Brain MCP documentation)
- [`RELEASE_NOTES_v8.3.0.md`](release-notes/RELEASE_NOTES_v8.3.0.md) - Dashboard rewrite
- [`RELEASE_NOTES_v7.x.md`](release-notes/) - v7.1.0 through v7.6.3 release notes
- [`RELEASE_NOTES_v6.x.md`](release-notes/) - v6.0.0 and v6.1.1 release notes

### `docs/releases/` - Historical Release Notes (v2.0-v8.0)
- [`RELEASE_NOTES_v8.x.md`](releases/) - v8.0.0 and v8.0.1 release notes
- [`RELEASE_NOTES_v7.x.md`](releases/) - v7.10.0 through v7.19.0 release notes
- [`RELEASE_NOTES_v6.x.md`](releases/) - v6.0.1, v6.1.0, v6.2.0 release notes
- [`RELEASE_NOTES_v5.x.md`](releases/) - v5.3.0 through v5.8.3 release notes
- [`RELEASE_NOTES_v4.x.md`](releases/) - v4.4.0, v4.4.1, v4.11.0 release notes
- [`RELEASE_NOTES_v2.x` and `v3.x`](releases/) - Earlier release notes

### `docs/architecture/` - Architecture Documentation
- [`FOUR_TIER_SUMMARY.md`](architecture/FOUR_TIER_SUMMARY.md) - Four-tier agent architecture summary
- [`V6_2_FOUR_TIER_ARCHITECTURE.md`](architecture/V6_2_FOUR_TIER_ARCHITECTURE.md) - Four-tier architecture design
- [`V6_TWO_TIER_ARCHITECTURE.md`](architecture/V6_TWO_TIER_ARCHITECTURE.md) - Original two-tier architecture
- [`TOKEN_EFFICIENT_ARCHITECTURE.md`](architecture/TOKEN_EFFICIENT_ARCHITECTURE.md) - Token optimization architecture
- [`CROSS_PLATFORM_DASHBOARD_SOLUTION.md`](architecture/CROSS_PLATFORM_DASHBOARD_SOLUTION.md) - Cross-platform dashboard resolution
- Other architecture analysis and fix reports

### `docs/implementation/` - Implementation Documentation
- [`IMPLEMENTATION_SUMMARY.md`](implementation/IMPLEMENTATION_SUMMARY.md) - Complete implementation overview
- [`PHASE1_OPTIMIZATION_COMPLETE.md`](implementation/PHASE1_OPTIMIZATION_COMPLETE.md) - Phase 1 architecture documentation
- [`COMMAND_MIGRATION_GUIDE_v4.0.0.md`](implementation/COMMAND_MIGRATION_GUIDE_v4.0.0.md) - Command migration guide
- [`SLASH_COMMAND_CATEGORIES.md`](implementation/SLASH_COMMAND_CATEGORIES.md) - Slash command category reference
- Other implementation phase summaries and improvement plans

### `docs/analysis/` - Analysis Reports
- [`COMMAND_COVERAGE_ANALYSIS.md`](analysis/COMMAND_COVERAGE_ANALYSIS.md) - Command coverage analysis
- [`ARGUMENT_PARSER_IMPROVEMENTS.md`](analysis/ARGUMENT_PARSER_IMPROVEMENTS.md) - Argument parser improvement analysis

### `docs/emergency-fixes/` - Emergency Fix Documentation
- Historical emergency bug reports and deployment guides

## Key Documents (Root of `docs/`)

| Document | Purpose |
|----------|---------|
| [`APPROACH_AND_METHOD.md`](APPROACH_AND_METHOD.md) | Methodology and design principles (11 bullets, v8.4.5) |
| [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) | Current known issues and workarounds |
| [`KNOWLEDGE_MANAGEMENT.md`](KNOWLEDGE_MANAGEMENT.md) | Knowledge management paradigm and storage layers |
| [`FOUR_TIER_ARCHITECTURE.md`](FOUR_TIER_ARCHITECTURE.md) | Complete four-tier architecture documentation (36 agents, 4 groups) |
| [`FULL_STACK_VALIDATION.md`](FULL_STACK_VALIDATION.md) | Full-stack validation system with auto-fix patterns |
| [`LEARNING_SYSTEMS.md`](LEARNING_SYSTEMS.md) | Four-tier learning infrastructure |
| [`CHANGELOG.md`](CHANGELOG.md) | Detailed changelog (v1.0.0-v8.3.0; v8.4.0+ in root `../CHANGELOG.md`) |
| [`CROSS_PLATFORM_PLUGIN_ARCHITECTURE.md`](CROSS_PLATFORM_PLUGIN_ARCHITECTURE.md) | Three-layer cross-platform plugin path resolution |
| [`INSTALLATION.md`](INSTALLATION.md) | Installation guide |
| [`WEB_VALIDATION_SYSTEM.md`](WEB_VALIDATION_SYSTEM.md) | Web validation system documentation |

## Quick Navigation

### For Users
- **Getting Started**: [README.md](../README.md) in the root directory
- **Latest Release**: [`RELEASE_NOTES_v8.4.5.md`](release-notes/RELEASE_NOTES_v8.4.5.md)
- **Known Issues**: [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md)
- **Brain MCP Integration**: [`guidelines/BRAIN_MCP_INTEGRATION_GUIDELINES.md`](guidelines/BRAIN_MCP_INTEGRATION_GUIDELINES.md)

### For Developers
- **Architecture**: [`FOUR_TIER_ARCHITECTURE.md`](FOUR_TIER_ARCHITECTURE.md)
- **Methodology**: [`APPROACH_AND_METHOD.md`](APPROACH_AND_METHOD.md)
- **Session Startup**: [`guidelines/SESSION_START_CHECKLIST.md`](guidelines/SESSION_START_CHECKLIST.md)
- **Result Presentation**: [`guidelines/RESULT_PRESENTATION_GUIDELINES.md`](guidelines/RESULT_PRESENTATION_GUIDELINES.md)
- **Testing**: [`../TESTING.md`](../TESTING.md)

### For Troubleshooting
- **Known Issues**: [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md)
- **Emergency Fixes**: [`emergency-fixes/`](emergency-fixes/)
- **Session Recovery**: [`guidelines/SESSION_START_CHECKLIST.md`](guidelines/SESSION_START_CHECKLIST.md)

---

**Last Updated**: 2026-06-21
**Plugin Version**: 8.4.5
**Canonical Changelog**: [`../CHANGELOG.md`](../CHANGELOG.md) (root, Keep a Changelog format)
