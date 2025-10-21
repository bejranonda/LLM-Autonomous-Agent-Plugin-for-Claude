# Installation Guide

## Quick Install via Marketplace

The easiest way to install the Autonomous Agent Plugin is through Claude Code's plugin marketplace:

```bash
# Add the plugin marketplace
/plugin marketplace add https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude

# Install the plugin
/plugin install autonomous-agent
```

## Manual Installation

### Option 1: Install from GitHub

```bash
# Install directly from GitHub repository
/plugin install https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude
```

### Option 2: Clone and Install Locally

```bash
# Clone the repository
git clone https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude.git

# Navigate to your Claude Code plugins directory
# Linux/Mac:
cd ~/.config/claude/plugins/

# Windows:
cd %APPDATA%\Claude\plugins\

# Copy the plugin
cp -r /path/to/LLM-Autonomous-Agent-Plugin-for-Claude ./autonomous-agent

# Restart Claude Code or reload plugins
/plugin reload
```

## Verify Installation

After installation, verify the plugin is loaded:

```bash
# List installed plugins
/plugin list

# You should see "autonomous-agent" in the list

# Check available commands
/help

# You should see:
# - /auto-analyze
# - /quality-check
# - /learn-patterns
```

## Post-Installation Setup

### 1. Initialize Pattern Learning (Optional)

Create the pattern learning directory in your project:

```bash
# Run in your project directory
/learn-patterns
```

This creates `.claude-patterns/` directory for storing learned patterns.

### 2. Test Python Utilities (Optional)

If you want to use the enhanced Python-based pattern storage:

```bash
# Check Python version (requires 3.7+)
python3 --version

# Test pattern storage
python3 ~/.config/claude/plugins/autonomous-agent/lib/pattern_storage.py stats

# Test task queue
python3 ~/.config/claude/plugins/autonomous-agent/lib/task_queue.py status

# Test quality tracker
python3 ~/.config/claude/plugins/autonomous-agent/lib/quality_tracker.py average
```

**Note**: Python utilities are optional. The plugin works perfectly fine without them using pure Markdown mode.

## System Requirements

### Minimum Requirements
- Claude Code CLI (version 1.0.0 or higher)
- No additional dependencies required

### Optional Requirements
- Python 3.7+ (for enhanced pattern storage utilities)
- Git (for version control integration)

### Platform Support
- ✅ Linux (all distributions)
- ✅ macOS (10.15+)
- ✅ Windows 10/11

## Configuration

The plugin works out-of-the-box with no configuration required. However, you can customize behavior:

### Pattern Learning Configuration

Edit `.claude-patterns/config.json` in your project (created automatically):

```json
{
  "pattern_storage": {
    "min_quality_threshold": 0.7,
    "max_patterns": 1000,
    "auto_cleanup": true,
    "cleanup_days": 90
  },
  "quality_control": {
    "enabled": true,
    "auto_fix": true,
    "max_fix_iterations": 3,
    "quality_threshold": 70
  },
  "background_tasks": {
    "enabled": true,
    "max_parallel": 3
  }
}
```

## Troubleshooting

### Plugin Not Found After Installation

```bash
# Reload plugins
/plugin reload

# If still not found, check plugin directory
ls ~/.config/claude/plugins/autonomous-agent/

# Verify plugin.json exists
cat ~/.config/claude/plugins/autonomous-agent/.claude-plugin/plugin.json
```

### Commands Not Available

```bash
# Check if plugin is enabled
/plugin list

# Enable the plugin if disabled
/plugin enable autonomous-agent

# Reload Claude Code
/reload
```

### Python Scripts Not Working

This is normal and expected! The plugin automatically falls back to pure Markdown mode:

```bash
# Check Python installation
python3 --version

# If Python is not installed or version < 3.7, the plugin will use MD-only mode
# All features remain available in MD-only mode
```

### Permission Errors

**Linux/Mac**:
```bash
# Fix plugin directory permissions
chmod -R 755 ~/.config/claude/plugins/autonomous-agent/

# Fix Python script permissions
chmod +x ~/.config/claude/plugins/autonomous-agent/lib/*.py
```

**Windows**:
```powershell
# Run as Administrator if needed
# Check file permissions in File Explorer
```

### Pattern Directory Not Created

```bash
# Manually create pattern directory
mkdir -p .claude-patterns

# Initialize with empty files
echo '[]' > .claude-patterns/patterns.json
echo '[]' > .claude-patterns/task_queue.json
echo '[]' > .claude-patterns/quality_history.json
```

## Updating

### Update via Marketplace

```bash
# Update to latest version
/plugin update autonomous-agent
```

### Update Manually

```bash
# Navigate to plugin directory
cd ~/.config/claude/plugins/autonomous-agent/

# Pull latest changes
git pull origin main

# Reload plugins
/plugin reload
```

## Uninstallation

### Remove Plugin

```bash
# Uninstall via Claude Code
/plugin uninstall autonomous-agent
```

### Clean Up Pattern Data

```bash
# Remove pattern learning data from your projects
# (Optional - only if you want to delete learned patterns)
rm -rf .claude-patterns/
```

## Next Steps

After installation:

1. **Read the Quick Start**: See [README.md](README.md) for usage examples
2. **Try Commands**: Run `/auto-analyze` in a project to see autonomous analysis
3. **Learn Patterns**: Use `/learn-patterns` to initialize pattern learning
4. **Check Quality**: Run `/quality-check` to assess code quality with auto-fix

## Support

- **Issues**: https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude/issues
- **Discussions**: https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude/discussions
- **Documentation**: See [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed usage

## Advanced Installation

### Custom Plugin Directory

```bash
# Set custom plugin directory
export CLAUDE_PLUGINS_DIR=/custom/path/to/plugins

# Install to custom directory
/plugin install autonomous-agent --dir $CLAUDE_PLUGINS_DIR
```

### Development Installation

For plugin development:

```bash
# Clone the repository
git clone https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude.git

# Create symbolic link
ln -s /path/to/LLM-Autonomous-Agent-Plugin-for-Claude ~/.config/claude/plugins/autonomous-agent

# Make changes and test
/plugin reload
```

## Verification Checklist

After installation, verify everything works:

- [ ] Plugin appears in `/plugin list`
- [ ] Commands available: `/auto-analyze`, `/quality-check`, `/learn-patterns`
- [ ] Can run `/auto-analyze` in a test project
- [ ] Pattern directory created at `.claude-patterns/`
- [ ] Python scripts work (optional, check with `python3 lib/pattern_storage.py stats`)

## FAQ

**Q: Do I need Python installed?**
A: No, Python is optional. The plugin works perfectly in pure Markdown mode without Python.

**Q: Will this work on Windows?**
A: Yes, full Windows support with both PowerShell and CMD examples in documentation.

**Q: Can I use this in multiple projects?**
A: Yes, each project gets its own `.claude-patterns/` directory for isolated learning.

**Q: How much disk space does it use?**
A: Minimal - typically < 10MB for the plugin, and < 1MB per project for pattern data.

**Q: Is internet required?**
A: Only for initial installation. After that, works completely offline.

**Q: Can I customize the agents?**
A: Yes, you can modify agent files in `~/.config/claude/plugins/autonomous-agent/agents/` after installation.
