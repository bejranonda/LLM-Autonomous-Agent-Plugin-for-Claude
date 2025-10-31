# Dashboard Development Quick Reference

## 🚨 Important: Dual-Mode Architecture

This dashboard operates in two modes:

- **Development Mode**: Running from `lib/dashboard.py` (where you are now)
- **Distribution Mode**: Running from `.claude-patterns/dashboard.py` (auto-copied for users)

## Quick Start for Developers

### 1. Development Mode Testing
```bash
# Current location (development mode)
python dashboard.py --no-browser --port 5000

# Test API endpoints
curl http://127.0.0.1:5000/api/overview
```

### 2. Distribution Mode Testing
```bash
# Simulate user distribution
cp dashboard.py ../.claude-patterns/dashboard.py

# Test distribution version
python ../.claude-patterns/dashboard.py --no-browser --port 5001

# Verify distribution API
curl http://127.0.0.1:5001/api/overview
```

## Architecture Differences

| Feature | Development Mode | Distribution Mode |
|---------|------------------|------------------|
| **Location** | `lib/dashboard.py` | `.claude-patterns/dashboard.py` |
| **Detection** | `current_dir.name == 'lib'` | `current_dir.name == '.claude-patterns'` |
| **Project Root** | Discovered by searching upward | `current_dir.parent` |
| **Patterns Dir** | Discovered dynamically | `current_dir` |
| **Local Copy** | `False` | `True` |
| **Unified Storage** | `project_root/.claude-unified` | Multiple locations searched |

## Code Patterns

### Detection Logic
```python
# This is how the dashboard detects its mode
if current_dir.name == '.claude-patterns':
    # Distribution mode
    self.is_local_copy = True
    self.project_root = current_dir.parent
    self.patterns_dir = current_dir
elif current_dir.name == 'lib':
    # Development mode
    self.is_local_copy = False
    self.project_root = self._discover_project_root()
    self.patterns_dir = self._discover_patterns_dir()
```

### Unified Storage Access
```python
# ALWAYS use this pattern for data access
def get_data(self):
    unified_data = self._load_unified_data()
    quality_data = unified_data.get("quality", {})
    patterns_data = unified_data.get("patterns", {})
    # ... process data
```

## Common Development Tasks

### Adding New API Endpoints
1. Implement function in `DashboardDataCollector` class
2. Add Flask route at bottom of file
3. Test in both development and distribution modes
4. Update documentation if needed

### Modifying Data Structures
1. Update unified storage schema
2. Modify data access patterns
3. Test in both modes
4. Ensure backward compatibility

### Debugging Path Issues
```bash
# Check current directory detection
python -c "
from pathlib import Path
print(f'Current: {Path.cwd()}')
print(f'Dir name: {Path.cwd().name}')
print(f'Parent: {Path.cwd().parent}')
"

# Check unified storage
python -c "
from pathlib import Path
paths = ['.claude-unified', '../.claude-unified']
for p in paths:
    print(f'{p}: {Path(p).exists()}')
"
```

## Testing Checklist

Before committing changes, verify:

- [ ] Development mode works: `python dashboard.py`
- [ ] Distribution mode works: `cp dashboard.py ../.claude-patterns/ && python ../.claude-patterns/dashboard.py`
- [ ] API endpoints work in both modes
- [ ] Unified storage integration works
- [ ] No regression in existing functionality
- [ ] Documentation updated if needed

## Full Documentation

For complete understanding, please read:
- **[Development & Distribution Architecture](../../docs/DEVELOPMENT_DISTRIBUTION_ARCHITECTURE.md)** - Comprehensive guide
- **[Distribution Validation Report](../../DISTRIBUTION_VALIDATION_REPORT.md)** - Validation results

## Support

If you encounter issues:

1. Check which mode you're running in
2. Verify path detection logic
3. Test both development and distribution modes
4. Check unified storage availability
5. Review architecture documentation

---

**Last Updated**: 2025-10-31
**Mode**: Development (lib/dashboard.py)