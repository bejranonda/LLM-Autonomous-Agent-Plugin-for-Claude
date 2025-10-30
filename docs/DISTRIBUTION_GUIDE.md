# Distribution Guide for Public Release

This guide ensures the plugin works correctly when users install it from the marketplace or directly from GitHub.

## Key Requirements for Distribution

### 1. Path Resolution
All Python scripts must work regardless of installation method:
- **Development**: Scripts in local `lib/` directory
- **Marketplace**: Scripts in user's plugin directory (`~/.config/claude/plugins/autonomous-agent/lib/`)

### 2. User Data Exclusion
User-specific data must not be included in the repository:
- `.claude/` - Claude's local data
- `.claude-patterns/` - User project patterns
- `.claude-unified/` - Unified parameter storage
- Local reports and generated files

### 3. Plugin Installation Detection
Scripts must automatically detect the plugin installation path.

## Implementation Details

### Path Resolution System

The plugin uses `lib/plugin_path_resolver.py` to automatically find the correct paths:

```python
from plugin_path_resolver import get_script_path

# This works in both development and production
script_path = get_script_path("dashboard.py")
# Returns: /home/user/.config/claude/plugins/autonomous-agent/lib/dashboard.py
# Or: /path/to/dev/repo/lib/dashboard.py
```

### Script Execution Wrapper

The `lib/run_script.py` wrapper ensures scripts run from the correct directory:

```bash
# Users can run scripts directly
python <plugin_path>/lib/run_script.py dashboard.py --port 8080

# This works regardless of installation method
```

### Updated Slash Commands

All slash commands now use `<plugin_path>` placeholders in documentation:

```bash
# Before (development only)
python <plugin_path>/lib/dashboard.py

# After (works everywhere)
python <plugin_path>/lib/dashboard.py
```

## Testing Distribution

### 1. Local Testing

Test that the plugin works in both modes:

```bash
# Test in development mode (current repo)
python <plugin_path>/lib/plugin_path_resolver.py

# Should find current repository
```

### 2. Simulate Marketplace Installation

Test by installing to a temporary location:

```bash
# Create temporary plugin directory
mkdir /tmp/test-plugin
cp -r . /tmp/test-plugin/autonomous-agent

# Test path resolution from outside
cd /tmp
python /tmp/test-plugin/autonomous-agent/lib/plugin_path_resolver.py

# Should find the plugin installation
```

### 3. Test Python Scripts

Verify all Python scripts work with the new path system:

```bash
# Test dashboard
python <plugin_path>/lib/dashboard.py --test

# Test learning analytics
python <plugin_path>/lib/learning_analytics.py show --dir /tmp/test-patterns

# Test pattern storage
python <plugin_path>/lib/pattern_storage.py stats
```

## Files Modified for Distribution

### 1. `.gitignore`
Added exclusions for user-specific data:
```
.claude-unified/
.reports/
patterns/
local_config.json
user_settings.json
```

### 2. `lib/plugin_path_resolver.py` (NEW)
Automatically detects plugin installation path:
- Development mode: Current repository
- Marketplace: User's plugin directory
- Cross-platform support (Windows/Linux/Mac)

### 3. `lib/run_script.py` (NEW)
Wrapper script for proper script execution:
- Changes to correct directory
- Handles relative imports
- Provides error messages

### 4. Updated Slash Commands
Changed all `python <plugin_path>/lib/` references to `python <plugin_path>/lib/`:
- `commands/monitor/dashboard.md`
- `commands/learn/analytics.md`
- Any future commands

## User Experience

### Installation from Marketplace

Users install with:
```bash
/plugin install https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude
```

The plugin automatically:
- Detects installation path
- Runs scripts from correct location
- Stores patterns in user's project directory
- Excludes developer-specific data

### Backward Compatibility

The plugin maintains backward compatibility:
- Existing commands work unchanged
- Pattern data remains in user projects
- No migration required for users

## Troubleshooting Distribution Issues

### Script Not Found
If users get "script not found" errors:
1. Check plugin installation: `/plugin list`
2. Verify plugin directory exists
3. Check Python is installed and accessible

### Path Resolution Fails
If path resolver can't find plugin:
1. Check `.claude-plugin/plugin.json` exists
2. Verify plugin directory structure
3. Check file permissions

### Python Scripts Don't Run
If Python scripts fail:
1. Verify Python 3.7+ is installed
2. Check script permissions
3. Use the run_script.py wrapper

## Validation Checklist

Before releasing to public:

- [ ] `.gitignore` excludes all user-specific data
- [ ] `plugin_path_resolver.py` correctly detects installation
- [ ] All Python scripts work with path resolver
- [ ] Slash commands use `<plugin_path>` in documentation
- [ ] No hardcoded local paths remain
- [ ] Plugin works from marketplace installation
- [ ] Plugin works in development mode
- [ ] Cross-platform compatibility verified
- [ ] Error messages are user-friendly

## Release Process

1. **Commit Changes**
   ```bash
   git add .
   git commit -m "Prepare plugin for public distribution"
   ```

2. **Tag Release**
   ```bash
   git tag -a v5.5.0 -m "Release v5.5.0: Distribution-ready plugin"
   ```

3. **Push to GitHub**
   ```bash
   git push origin main
   git push origin v5.5.0
   ```

4. **Test Marketplace Installation**
   ```bash
   /plugin install https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude
   ```

5. **Verify Functionality**
   ```bash
   /monitor:dashboard
   /learn:analytics
   ```

## Support for Users

Provide clear installation and troubleshooting documentation:

1. **Installation Guide**: Update `INSTALLATION.md`
2. **Usage Examples**: Update `USAGE_GUIDE.md`
3. **Troubleshooting**: Add FAQ for common issues
4. **Support Channel**: Provide GitHub Issues link

## Summary

These changes ensure the plugin:
- ✅ Works when installed from marketplace
- ✅ Excludes developer-specific data
- ✅ Automatically detects installation path
- ✅ Maintains backward compatibility
- ✅ Provides clear error messages
- ✅ Works across all platforms

The plugin is now ready for public distribution without any local dependencies or hardcoded paths.