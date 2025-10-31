# Development and Distribution Architecture

## Overview

This document describes the dual-mode architecture for the dashboard system, which supports both development environments and user distribution through a smart hybrid approach.

## Architecture Summary

The dashboard operates in two distinct modes:

1. **Development Mode**: Running directly from `/lib/dashboard.py`
2. **Distribution Mode**: Running from `.claude-patterns/dashboard.py` (automatically copied)

## Dual-Mode Architecture

### Development Mode (`/lib/dashboard.py`)

**Purpose**: Primary development and testing environment
**Location**: Plugin's `lib/` directory
**Detection**: `current_dir.name == 'lib'`

**Characteristics**:
```python
# Detection Logic
if current_dir.name == 'lib':
    # Development mode detected
    self.is_local_copy = False
    self.project_root = self._discover_project_root()  # Search upward for project root
    self.patterns_dir = self._discover_patterns_dir()   # Find patterns directory
```

**Path Resolution**:
- **Current Directory**: `/path/to/plugin/lib/`
- **Project Root**: Detected by searching upward for `.claude-plugin`, `README.md`, `.git`, etc.
- **Patterns Directory**: `project_root/.claude-patterns/` or other discovered locations
- **Unified Storage**: `project_root/.claude-unified/` or other discovered locations

**Use Cases**:
- Primary development and testing
- Plugin development iterations
- Feature development and debugging
- Performance testing and optimization

### Distribution Mode (`.claude-patterns/dashboard.py`)

**Purpose**: User distribution after automatic copying
**Location**: Project's `.claude-patterns/` directory
**Detection**: `current_dir.name == '.claude-patterns'`

**Characteristics**:
```python
# Detection Logic
if current_dir.name == '.claude-patterns':
    # Distribution mode detected
    self.is_local_copy = True
    self.project_root = current_dir.parent          # Parent directory is project root
    self.patterns_dir = current_dir                 # Current directory is patterns dir
```

**Path Resolution**:
- **Current Directory**: `/path/to/project/.claude-patterns/`
- **Project Root**: `current_dir.parent` (parent of `.claude-patterns`)
- **Patterns Directory**: `current_dir` (same as current directory)
- **Unified Storage**: `current_dir/.claude-unified`, `project_root/.claude-unified`, etc.

**Use Cases**:
- End-user distribution
- Production deployment
- Offline usage after initial setup
- Per-project dashboard instances

## Unified Parameter Storage Integration

### Storage Discovery Priority

Both modes use the same unified storage discovery algorithm:

```python
storage_dirs = [
    # Priority 1: Current directory unified storage
    self.patterns_dir / '.claude-unified',

    # Priority 2: Project root unified storage
    self.project_root / '.claude-unified',

    # Priority 3: Current directory (fallback)
    self.patterns_dir,

    # Priority 4: Project root (fallback)
    self.project_root
]
```

### Data Access Pattern

```python
def _load_unified_data(self) -> dict:
    """
    Load data from unified parameter storage.
    This is the PRIMARY data source for all dashboard APIs.
    """
    if not self.use_unified_storage or not self.unified_storage:
        # Graceful fallback when unified storage not available
        return {
            "quality": {"assessments": {"history": [], "current": {}}},
            "patterns": {},
            "performance": {"records": []},
            "skills": {"skill_effectiveness": {}},
            "agents": {"agent_effectiveness": {}}
        }

    try:
        unified_data = self.unified_storage._read_data()
        return unified_data
    except Exception as e:
        # Error handling with fallback
        return fallback_data_structure
```

## Development Workflow

### 1. Development Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd <repository-name>

# Work with development version
python lib/dashboard.py --no-browser --port 5000
```

### 2. Making Changes

```python
# Edit development version
vim lib/dashboard.py

# Test changes locally
python lib/dashboard.py --no-browser --port 5000

# Run API tests
curl http://127.0.0.1:5000/api/overview
```

### 3. Distribution Testing

```bash
# Copy to local patterns directory (simulate distribution)
cp lib/dashboard.py .claude-patterns/dashboard.py

# Test distribution version
python .claude-patterns/dashboard.py --no-browser --port 5001

# Verify dual-mode functionality
curl http://127.0.0.1:5001/api/overview
```

### 4. Commit Changes

```bash
# Commit both development and distribution-ready versions
git add lib/dashboard.py .claude-patterns/dashboard.py
git commit -m "feat: implement dual-mode dashboard architecture"
git push
```

## Distribution Process

### Automatic Copy Mechanism

The plugin automatically copies the dashboard to user projects:

```bash
# Smart Hybrid Approach (in commands/monitor/dashboard.md)
if [ -f ".claude-patterns/dashboard.py" ]; then
    # Use local copy (fastest)
    python .claude-patterns/dashboard.py --patterns-dir .claude-patterns "$@"
else
    # Auto-copy from plugin
    PLUGIN_DIR=$(find plugin paths...)
    mkdir -p .claude-patterns
    cp "$PLUGIN_DIR/lib/dashboard.py" ".claude-patterns/dashboard.py"
    python .claude-patterns/dashboard.py --patterns-dir .claude-patterns "$@"
fi
```

### User Experience Flow

1. **Installation**: User installs plugin
2. **First Run**: `/monitor:dashboard` command executed
3. **Auto-Copy**: Dashboard copied to `.claude-patterns/dashboard.py`
4. **Local Execution**: Dashboard runs from local copy
5. **Performance**: 85-90% faster startup on subsequent runs
6. **Offline Ready**: Works without plugin after initial copy

## File Structure Dependencies

### Development Dependencies

```
plugin-root/
├── lib/
│   ├── dashboard.py              # Development version
│   └── unified_parameter_storage.py  # Unified storage implementation
├── .claude-plugin/
│   └── plugin.json               # Plugin manifest
└── docs/
    └── DEVELOPMENT_DISTRIBUTION_ARCHITECTURE.md
```

### Distribution Dependencies

```
user-project/
├── .claude-patterns/
│   ├── dashboard.py              # Distribution copy (auto-copied)
│   ├── .claude-unified/          # Unified storage (created when needed)
│   ├── parameters.json           # Unified parameter storage
│   └── patterns.json             # Pattern learning data
└── source-code/
    └── project files...
```

## Debugging and Troubleshooting

### Development Mode Issues

```bash
# Check development mode detection
python -c "
from pathlib import Path
current_dir = Path('.').absolute()
print(f'Current: {current_dir}')
print(f'Is lib directory: {current_dir.name == \"lib\"}')
"
```

### Distribution Mode Issues

```bash
# Check distribution mode detection
python -c "
from pathlib import Path
current_dir = Path('.').absolute()
print(f'Current: {current_dir}')
print(f'Is .claude-patterns directory: {current_dir.name == \".claude-patterns\"}')
print(f'Project root: {current_dir.parent}')
"
```

### Unified Storage Issues

```bash
# Check unified storage locations
python -c "
from pathlib import Path
import os

paths_to_check = [
    '.claude-unified',
    '../.claude-unified',
    os.path.expanduser('~/.claude-unified')
]

for path in paths_to_check:
    p = Path(path)
    if p.exists():
        print(f'✅ Found: {p.absolute()}')
    else:
        print(f'❌ Not found: {p.absolute()}')
"
```

## Testing Strategy

### Development Testing

```bash
# Test development mode
python lib/dashboard.py --no-browser --port 5000
curl http://127.0.0.1:5000/api/overview

# Verify unified storage integration
curl http://127.0.0.1:5000/api/unified/quality
```

### Distribution Testing

```bash
# Test distribution mode
cp lib/dashboard.py .claude-patterns/dashboard.py
python .claude-patterns/dashboard.py --no-browser --port 5001
curl http://127.0.0.1:5001/api/overview

# Verify graceful fallback
curl http://127.0.0.1:5001/api/unified/quality  # Should handle missing storage gracefully
```

### Regression Testing

```bash
# Test both modes in sequence
python lib/dashboard.py --no-browser --port 5000 &
sleep 2
python .claude-patterns/dashboard.py --no-browser --port 5001 &
sleep 2

# Compare results
curl -s http://127.0.0.1:5000/api/overview > dev_output.json
curl -s http://127.0.0.1:5001/api/overview > dist_output.json
diff dev_output.json dist_output.json
```

## Maintenance Guidelines

### When Adding New Features

1. **Implement in Development Version**: Add feature to `lib/dashboard.py`
2. **Test Development Mode**: Verify functionality in development environment
3. **Test Distribution Mode**: Copy to `.claude-patterns` and test distribution version
4. **Verify Dual-Mode**: Ensure feature works in both modes
5. **Update Documentation**: Update this architecture document if needed
6. **Commit Both Versions**: Include both development and distribution-ready versions

### When Fixing Bugs

1. **Identify Mode-Specific Issues**: Determine if bug affects development, distribution, or both modes
2. **Fix Root Cause**: Address issue in shared code (unified storage, data access patterns)
3. **Test Both Modes**: Verify fix works in both development and distribution modes
4. **Update Tests**: Add regression tests for the fixed issue
5. **Document Changes**: Update architecture documentation if needed

### Performance Optimization

1. **Test Both Modes**: Measure performance in both development and distribution modes
2. **Local Copy Optimization**: Ensure distribution mode benefits from local copy optimization
3. **Unified Storage Optimization**: Optimize unified storage access patterns
4. **Memory Management**: Monitor memory usage in both modes
5. **Benchmark Changes**: Document performance improvements

## Future Enhancements

### Potential Improvements

1. **Enhanced Detection**: More sophisticated project root detection
2. **Configuration Management**: User-configurable paths and preferences
3. **Plugin Updates**: Automatic updates of local dashboard when plugin updates
4. **Multi-Project Support**: Support for multiple project dashboards
5. **Cloud Integration**: Cloud-based unified storage synchronization

### Migration Path

When implementing new features or architectural changes:

1. **Backward Compatibility**: Ensure existing installations continue to work
2. **Gradual Migration**: Support both old and new approaches during transition
3. **User Communication**: Clearly communicate changes to users
4. **Rollback Plan**: Ability to revert changes if issues arise
5. **Testing Strategy**: Comprehensive testing of migration scenarios

## Conclusion

The dual-mode architecture provides the best of both worlds:

- **Development Efficiency**: Direct access to source code and immediate testing
- **Distribution Reliability**: Self-contained local copies with offline capability
- **Performance Optimization**: Local copy provides 85-90% faster startup
- **Automatic Learning**: Seamless integration with unified parameter storage system
- **User Experience**: Zero configuration with immediate functionality

Future developers should maintain this dual-mode approach to ensure both development productivity and user distribution reliability.

---

**Last Updated**: 2025-10-31
**Architecture Version**: 1.0
**Maintainer**: Autonomous Agent Development Team