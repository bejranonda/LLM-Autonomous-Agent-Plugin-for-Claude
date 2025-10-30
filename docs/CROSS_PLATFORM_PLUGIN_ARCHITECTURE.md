# Cross-Platform Plugin Architecture

## Problem Statement

The plugin needs to execute Python scripts from slash commands, but faces these challenges:

1. **Unknown Installation Path**: Users install from marketplace, paths vary by platform
2. **Multiple Installation Methods**: Development, marketplace, system-wide
3. **Platform Differences**: Windows, Linux, macOS have different path structures
4. **User Directory Variations**: Home directories differ between users

**Example Installation Paths**:
- Windows Marketplace: `C:\Users\{username}\.claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude\`
- Linux Marketplace: `~/.claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude/`
- Development: `~/projects/AutonomousAgent/`

## Solution Architecture

### Three-Layer Solution

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Slash Commands (commands/*.md)                │
│  - Simple execution instructions                         │
│  - Platform-independent                                  │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 2: Script Executor (lib/exec_plugin_script.py)   │
│  - Finds plugin installation automatically              │
│  - Executes target script with arguments                │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Path Resolver (lib/plugin_path_resolver.py)   │
│  - Platform detection (Windows, Linux, macOS)           │
│  - Checks all standard installation locations           │
│  - Returns validated plugin path                        │
└─────────────────────────────────────────────────────────┘
```

## Implementation Details

### Layer 1: Slash Commands

**File**: `commands/monitor/dashboard.md` (example)

```markdown
When executing this command, run the following:

```bash
python lib/exec_plugin_script.py dashboard.py --port 5000
```
```

**Key Points**:
- Simple, one-line execution command
- Relative path `lib/exec_plugin_script.py` (Claude Code resolves plugin root)
- Arguments passed directly to target script
- No hardcoded paths anywhere

### Layer 2: Script Executor

**File**: `lib/exec_plugin_script.py`

**Purpose**: Automatically locate and execute plugin scripts

**Features**:
- Finds plugin installation via `plugin_path_resolver.py`
- Resolves target script in `lib/` directory
- Executes with correct Python interpreter
- Forwards all arguments to target script
- Cross-platform compatible

**Usage**:
```bash
# Execute dashboard.py with arguments
python lib/exec_plugin_script.py dashboard.py --host 0.0.0.0 --port 8080

# Execute any lib script
python lib/exec_plugin_script.py learning_analytics.py show

# Show plugin installation info
python lib/exec_plugin_script.py --info
```

**How It Works**:
1. Receives script name and arguments
2. Calls `get_script_path(script_name)` to locate script
3. If not found, shows helpful error with searched locations
4. Executes script using `subprocess.run()`
5. Returns script's exit code

### Layer 3: Path Resolver

**File**: `lib/plugin_path_resolver.py`

**Purpose**: Discover plugin installation location across all platforms and installation methods

**Discovery Strategy**:

```python
def get_plugin_path() -> Optional[Path]:
    """
    Search order:
    1. Current working directory (development mode)
    2. Parent directories (if inside plugin structure)
    3. CLAUDE_PLUGIN_PATH environment variable
    4. Standard installation locations (platform-specific)
    """
```

**Installation Locations Checked**:

**All Platforms**:
- `~/.claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude/`
- `~/.config/claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude/`
- `~/.claude/plugins/autonomous-agent/`
- `~/.config/claude/plugins/autonomous-agent/`

**Windows Additional**:
- `%APPDATA%\Claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude\`
- `%LOCALAPPDATA%\Claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude\`
- `%PROGRAMFILES%\Claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude\`

**Linux/macOS Additional**:
- `/usr/local/share/claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude/`
- `/opt/claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude/`

**Validation**: Each location checked for `.claude-plugin/plugin.json` existence

## Usage Examples

### From Slash Commands (Primary Use Case)

**Scenario**: User runs `/monitor:dashboard` from any directory

```markdown
# commands/monitor/dashboard.md
When executing this command, run:

```bash
python lib/exec_plugin_script.py dashboard.py
```
```

**What Happens**:
1. Claude Code executes the bash command from plugin root directory
2. `exec_plugin_script.py` discovers plugin installation
3. Finds `lib/dashboard.py` in that installation
4. Executes dashboard with proper Python interpreter
5. Dashboard launches on available port

### From Command Line (Development/Testing)

```bash
# Show plugin info (verify installation)
python lib/exec_plugin_script.py --info

# Execute dashboard
python lib/exec_plugin_script.py dashboard.py

# Execute with arguments
python lib/exec_plugin_script.py dashboard.py --port 8080 --host 0.0.0.0

# Execute other scripts
python lib/exec_plugin_script.py learning_analytics.py show --dir .claude-patterns
```

### Environment Variable Override

```bash
# Set custom plugin path
export CLAUDE_PLUGIN_PATH=/custom/path/to/plugin

# Now all scripts use this path
python lib/exec_plugin_script.py dashboard.py
```

## Error Handling

### Plugin Not Found

```
ERROR: Script 'dashboard.py' not found
Plugin installation not found!

Troubleshooting:
1. Check if plugin is installed correctly
2. Verify .claude-plugin/plugin.json exists
3. Try setting CLAUDE_PLUGIN_PATH environment variable

Searched locations:
  [X] C:\Users\{user}\.claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude
  [X] C:\Users\{user}\.config\claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude
  [OK] D:\Git\Werapol\AutonomousAgent
  ...
```

### Script Not Found (But Plugin Found)

```
ERROR: Script 'nonexistent.py' not found
Plugin found at: D:\Git\Werapol\AutonomousAgent
But script not found in: D:\Git\Werapol\AutonomousAgent/lib/
```

## Benefits

### For Plugin Developers

✅ **No Hardcoded Paths**: All paths discovered dynamically
✅ **Platform Independent**: Works on Windows, Linux, macOS without changes
✅ **Simple Commands**: One-line execution in slash commands
✅ **Easy Testing**: Can test locally and in marketplace installations
✅ **Clear Errors**: Helpful error messages with troubleshooting steps

### For Plugin Users

✅ **Works Everywhere**: Installation location doesn't matter
✅ **No Configuration**: Automatic discovery, no setup needed
✅ **Consistent Behavior**: Same commands work across all platforms
✅ **Clear Feedback**: Knows if plugin is properly installed

### For Claude Code

✅ **Simple Integration**: Just execute `python lib/exec_plugin_script.py {script}`
✅ **No Path Resolution**: Plugin handles all path discovery
✅ **Error Recovery**: Clear errors if installation is broken
✅ **Portable**: Same command works for all users

## Migration Guide

### Before (Problematic)

```markdown
# Old command implementation
Execute: python <plugin_path>/lib/dashboard.py --port 5000

# Issues:
# - <plugin_path> is a placeholder, Claude Code doesn't know the value
# - Hardcoded assumptions about installation location
# - Doesn't work with marketplace installations
```

### After (Correct)

```markdown
# New command implementation
Execute: python lib/exec_plugin_script.py dashboard.py --port 5000

# Benefits:
# - Actual executable command, no placeholders
# - Works everywhere (development, marketplace, system-wide)
# - Cross-platform compatible
# - Clear error messages if something is wrong
```

## Testing

### Development Mode Test

```bash
# From plugin repository root
cd /path/to/AutonomousAgent
python lib/exec_plugin_script.py --info

# Should show:
# [OK] Plugin Found: /path/to/AutonomousAgent
```

### Marketplace Installation Test

```bash
# From any directory
cd ~
python ~/.claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude/lib/exec_plugin_script.py --info

# Should show:
# [OK] Plugin Found: /home/user/.claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude
```

### Cross-Platform Test

**Windows (PowerShell)**:
```powershell
python $env:USERPROFILE\.claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude\lib\exec_plugin_script.py --info
```

**Linux/macOS (Bash)**:
```bash
python ~/.claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude/lib/exec_plugin_script.py --info
```

## Best Practices

### For Slash Command Authors

1. **Use Executor**: Always use `python lib/exec_plugin_script.py {script}` pattern
2. **No Absolute Paths**: Never hardcode absolute paths
3. **Relative to Plugin**: Assume commands run from plugin root
4. **Test Everywhere**: Test in development and marketplace installations
5. **Document Arguments**: Clearly document script arguments in command files

### For Script Authors

1. **Use Resolver**: Import and use `plugin_path_resolver.py` for finding plugin files
2. **Portable Code**: Don't assume specific installation paths
3. **Handle Errors**: Gracefully handle missing files or directories
4. **Platform Aware**: Use `sys.platform` for platform-specific code
5. **Test Cross-Platform**: Test on Windows, Linux, and macOS if possible

## Troubleshooting

### Command: Plugin Not Found

**Symptom**: `ERROR: Plugin installation not found`

**Solutions**:
1. Check if plugin is installed: Look for `.claude-plugin/plugin.json`
2. Set environment variable: `export CLAUDE_PLUGIN_PATH=/path/to/plugin`
3. Verify Claude Code version supports marketplace plugins
4. Check file permissions (especially on Linux/macOS)

### Command: Script Not Found

**Symptom**: `ERROR: Script 'dashboard.py' not found`

**Solutions**:
1. Verify script exists in `lib/` directory
2. Check file name spelling (case-sensitive on Linux/macOS)
3. Ensure script file has correct permissions
4. Look at exec_plugin_script output for searched locations

### Command: Permission Denied

**Symptom**: `ERROR: Permission denied executing script`

**Solutions**:
```bash
# Linux/macOS: Make scripts executable
chmod +x lib/*.py

# Or ensure Python can read the files
chmod 644 lib/*.py
```

## Advanced: Custom Plugin Locations

### Development with Custom Path

```bash
# Set custom plugin location
export CLAUDE_PLUGIN_PATH=/custom/dev/path

# All commands now use this path
python lib/exec_plugin_script.py dashboard.py
```

### Multiple Plugin Versions

```bash
# Switch between versions
export CLAUDE_PLUGIN_PATH=~/plugins/autonomous-agent-v1
python lib/exec_plugin_script.py --info

export CLAUDE_PLUGIN_PATH=~/plugins/autonomous-agent-v2
python lib/exec_plugin_script.py --info
```

## Architecture Diagram

```
User runs: /monitor:dashboard
         │
         ▼
┌─────────────────────────────────────────┐
│ Claude Code                              │
│ - Finds commands/monitor/dashboard.md   │
│ - Reads execution instructions           │
│ - Executes via Bash tool                 │
└──────────┬──────────────────────────────┘
           │
           │ python lib/exec_plugin_script.py dashboard.py
           ▼
┌─────────────────────────────────────────┐
│ exec_plugin_script.py                    │
│ - Imports plugin_path_resolver           │
│ - Calls get_script_path('dashboard.py') │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│ plugin_path_resolver.py                  │
│ - Checks CWD and parents                 │
│ - Checks CLAUDE_PLUGIN_PATH env var      │
│ - Checks standard locations              │
│ - Returns validated plugin path          │
└──────────┬──────────────────────────────┘
           │
           │ Returns: ~/.claude/plugins/marketplaces/.../lib/dashboard.py
           ▼
┌─────────────────────────────────────────┐
│ exec_plugin_script.py                    │
│ - Executes: python {resolved_path}      │
│ - Forwards arguments: --port 5000       │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│ dashboard.py                             │
│ - Starts Flask server                    │
│ - Opens browser                          │
│ - Serves dashboard UI                    │
└─────────────────────────────────────────┘
```

## Conclusion

This three-layer architecture solves the cross-platform plugin path problem by:

1. **Slash commands** remain simple with no hardcoded paths
2. **Script executor** provides a stable API for running scripts
3. **Path resolver** handles all platform and installation variations

The solution is:
- ✅ Platform-independent (Windows, Linux, macOS)
- ✅ Installation-method agnostic (development, marketplace, system-wide)
- ✅ User-independent (no hardcoded user directories)
- ✅ Maintainable (single place to update path logic)
- ✅ Testable (easy to verify on different platforms)
- ✅ User-friendly (clear error messages)

**Key Innovation**: No placeholders, no hardcoded paths, all discovery is dynamic and runtime-based.
