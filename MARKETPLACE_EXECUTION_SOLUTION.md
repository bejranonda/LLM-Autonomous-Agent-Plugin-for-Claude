# Marketplace Execution Solution

## Problem Solved

Users install the plugin from marketplace, which stores Python scripts in the plugin directory, but they want to run commands from their project directories where the data lives.

**Challenge**:
- **Script Location**: `C:\Users\{username}\.claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude\lib\dashboard.py`
- **Data Location**: `{project_directory}\.claude-patterns\`
- **User Context**: Running `/monitor:dashboard` from any project directory

## Solution: Marketplace Template System

### Core Innovation

Use a template placeholder that gets filled during marketplace installation:

```bash
# Template in command file:
python -c "exec(open(r'{PLUGIN_PATH}/lib/marketplace_executor.py').read())" dashboard.py

# After marketplace installation (filled in):
python -c "exec(open(r'C:\Users\{username}\.claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude\lib\marketplace_executor.py').read())" dashboard.py
```

### Components

#### 1. Marketplace Executor (`lib/marketplace_executor.py`)
- **Purpose**: Universal script executor for marketplace installations
- **Features**:
  - Handles template execution (when `__file__` is available)
  - Fallback path discovery (when `__file__` is not available)
  - Cross-platform compatibility
  - Preserves current working directory for data access

#### 2. Template System
- **Placeholder**: `{PLUGIN_PATH}` gets replaced during installation
- **Execution**: Uses `exec(open(...).read())` to load and run the executor
- **Flexibility**: Works regardless of where the plugin is installed

#### 3. Updated Command Documentation
- **Primary Method**: Marketplace template approach
- **Fallback Method**: Development mode using `exec_plugin_script.py`
- **Examples**: Clear syntax for different use cases

## How It Works

### Marketplace Installation Flow

1. **Installation**: Claude Code installs plugin to marketplace directory
2. **Template Processing**: `{PLUGIN_PATH}` gets replaced with actual installation path
3. **User Command**: User runs `/monitor:dashboard` from any project directory
4. **Execution**: Template loads executor, which runs script from plugin directory
5. **Data Access**: Script accesses data from current working directory

### Path Resolution

```python
# Step 1: Template execution
python -c "exec(open(r'{ACTUAL_PLUGIN_PATH}/lib/marketplace_executor.py').read())" dashboard.py

# Step 2: Executor runs script from plugin directory
# Script runs from: C:\Users\{user}\.claude\plugins\marketplaces\...\lib\dashboard.py
# But current directory is: {user_project_directory}

# Step 3: Dashboard accesses data from current directory
# Pattern data: ./.claude-patterns/ (in user's project)
```

## Benefits

✅ **Universal Compatibility**: Works on Windows, Linux, macOS
✅ **Installation Agnostic**: Works from any plugin installation location
✅ **Project Independent**: Users can run from any project directory
✅ **Data Access**: Script can access project-specific data
✅ **No Copying**: Doesn't duplicate files between plugin and project
✅ **Template Based**: Clean, maintainable approach
✅ **Fallback Support**: Works in development mode too

## Implementation Details

### Marketplace Executor Features

```python
# 1. Smart path detection
try:
    plugin_path = Path(__file__).parent.parent  # When __file__ available
except NameError:
    # Fallback to automatic discovery
    plugin_path = find_plugin_installation()

# 2. Script execution from plugin directory
script_path = plugin_path / "lib" / script_name
cmd = [sys.executable, str(script_path)] + script_args

# 3. Preserve current working directory for data access
result = subprocess.run(cmd, cwd=os.getcwd())
```

### Template Processing

During marketplace installation:
```bash
# Before installation (template):
{PLUGIN_PATH}

# After installation (filled):
C:\Users\{username}\.claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude
```

## Usage Examples

### Basic Usage
```bash
# From any project directory
/monitor:dashboard

# With custom port
/monitor:dashboard --port 8080

# With external access
/monitor:dashboard --host 0.0.0.0
```

### Template Variations
```bash
# Simple command
python -c "exec(open(r'{PLUGIN_PATH}/lib/marketplace_executor.py').read())" dashboard.py

# With arguments
python -c "exec(open(r'{PLUGIN_PATH}/lib/marketplace_executor.py').read())" dashboard.py --port 8080

# Multiple scripts
python -c "exec(open(r'{PLUGIN_PATH}/lib/marketplace_executor.py').read())" learning_analytics.py show
```

## Testing

### Development Testing
```bash
# Test from plugin directory
python lib/marketplace_executor.py dashboard.py --help

# Test from different directory
cd /tmp && python /path/to/plugin/lib/marketplace_executor.py dashboard.py --help
```

### Template Testing
```bash
# Test template execution
cd /tmp && python -c "exec(open(r'/path/to/plugin/lib/marketplace_executor.py').read())" dashboard.py --help
```

## Cross-Platform Compatibility

### Windows
```bash
# Template after installation:
python -c "exec(open(r'C:\Users\{user}\.claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude\lib\marketplace_executor.py').read())" dashboard.py
```

### Linux/macOS
```bash
# Template after installation:
python -c "exec(open(r'/home/{user}/.claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude/lib/marketplace_executor.py').read())" dashboard.py
```

## Error Handling

### Plugin Not Found
```
ERROR: Cannot determine plugin path. Install plugin from marketplace or run from development directory.
```

### Script Not Found
```
ERROR: Script 'dashboard.py' not found at {plugin_path}/lib/dashboard.py
```

### Execution Failed
```
ERROR: Failed to execute script: {error details}
```

## File Structure

```
lib/
├── marketplace_executor.py          # NEW: Universal executor for marketplace
├── exec_plugin_script.py            # Development mode executor
├── plugin_path_resolver.py          # Path discovery utilities
└── dashboard.py                     # Target script (and others)

commands/monitor/
└── dashboard.md                     # UPDATED: Marketplace template documentation
```

## Migration Guide

### For Other Commands

To apply this pattern to other commands:

1. **Update command file**:
   ```markdown
   **Marketplace Installation**:
   ```bash
   python -c "exec(open(r'{PLUGIN_PATH}/lib/marketplace_executor.py').read())" {script_name}
   ```
   ```

2. **Keep development fallback**:
   ```markdown
   **Development Mode**:
   ```bash
   python lib/exec_plugin_script.py {script_name}
   ```
   ```

3. **Test both methods**:
   ```bash
   # Test marketplace template
   python -c "exec(open(r'{PLUGIN_PATH}/lib/marketplace_executor.py').read())" {script_name} --help

   # Test development mode
   python lib/exec_plugin_script.py {script_name} --help
   ```

## Future Considerations

### Enhancement Opportunities

1. **Automatic Template Processing**: Claude Code could automatically detect and process `{PLUGIN_PATH}` placeholders
2. **Universal Executor**: Single executor that handles all use cases without templates
3. **Configuration Files**: Allow users to customize plugin paths if needed
4. **Performance Optimization**: Cache plugin path discovery for faster execution

### Scalability

This approach scales to:
- **Multiple Scripts**: Any script in `lib/` directory
- **Multiple Commands**: All slash commands can use this pattern
- **Multiple Platforms**: Works across Windows, Linux, macOS
- **Multiple Users**: Each user gets their own path filled in

## Conclusion

The marketplace template system provides a robust, universal solution for executing plugin scripts from any directory while maintaining access to project-specific data. It solves the core challenge of separating script location (plugin) from data location (project) while providing a clean, maintainable approach that works across all platforms and installation methods.

**Key Achievement**: Users can now run `/monitor:dashboard` from any project directory, and it will work regardless of where the plugin is installed on their system.
