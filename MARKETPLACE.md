# Plugin Marketplace Installation

This repository now supports installation via Claude Code's marketplace system.

## Quick Installation

1. **Add Marketplace**:
   ```bash
   /plugin marketplace add https://gitlab.com/bwerapol/llm-autonomous-agent-plugin/-/raw/main/marketplace.json
   ```

2. **Install Plugin**:
   ```bash
   /plugin install autonomous-agent
   ```

## Alternative Installation Methods

### Method 1: Direct Git Clone
```bash
git clone https://gitlab.com/bwerapol/llm-autonomous-agent-plugin.git ~/.config/claude/plugins/autonomous-agent
```

### Method 2: Download ZIP
```bash
# Download and extract to ~/.config/claude/plugins/autonomous-agent
wget https://gitlab.com/bwerapol/llm-autonomous-agent-plugin/-/archive/main/llm-autonomous-agent-plugin-main.zip
```

## Plugin Features

- **Four-Tier Architecture**: 27 specialized agents across 4 collaborative groups
- **Pattern Learning**: Automatic learning and optimization over time
- **Token Optimization**: 60-70% cost reduction with smart caching
- **Full-Stack Validation**: 80-90% automatic issue resolution
- **Quality Control**: Comprehensive code quality assessment
- **Autonomous Operation**: Zero human intervention required

## Available Commands

After installation, use these commands:

- `/learn:init` - Initialize pattern learning system
- `/learn:show` - Display learned patterns and insights
- `/analyze:project` - Comprehensive project analysis
- `/analyze:quality` - Code quality assessment
- `/validate:project` - Full-stack validation
- `/validate:fix` - Auto-fix detected issues
- `/optimize:tokens` - Token usage optimization
- `/dashboard:launch` - Launch unified monitoring dashboard

## Marketplace Configuration

The `marketplace.json` file contains all necessary metadata for automatic plugin installation and dependency management.

### Schema Compliance

- ✅ Valid JSON schema for Claude Code marketplace
- ✅ Plugin metadata and dependencies
- ✅ Installation instructions and compatibility
- ✅ Command definitions and categorization
- ✅ Platform compatibility matrix

## Support

For issues and support:
- Repository: https://gitlab.com/bwerapol/llm-autonomous-agent-plugin
- Documentation: Check `README.md` and `docs/` directory
- Issues: Use GitLab's issue tracker