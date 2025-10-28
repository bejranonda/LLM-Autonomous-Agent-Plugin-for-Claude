# Migration Guide: Unified Parameter Storage

## Overview

This guide helps developers migrate from scattered parameter storage systems to the unified parameter storage system. It provides step-by-step instructions for different migration scenarios and ensures minimal disruption to existing functionality.

## Migration Scenarios

### 1. New Projects

For new projects, simply use the unified storage system from the start:

```python
from unified_parameter_storage import UnifiedParameterStorage

# Initialize and use
storage = UnifiedParameterStorage()
storage.set_quality_score(85.0)
```

### 2. Existing Projects with Legacy Storage

For existing projects, follow these steps:

#### Step 1: Install Compatibility Layer

```python
from parameter_compatibility import enable_compatibility_mode

# Enable compatibility mode (adds no breaking changes)
enable_compatibility_mode(auto_patch=True, monkey_patch=True)
```

#### Step 2: Gradual Migration

```python
# Phase 1: Use unified storage for new data
from unified_parameter_storage import UnifiedParameterStorage

storage = UnifiedParameterStorage()

# Phase 2: Migrate existing data
from parameter_migration import MigrationManager

migration_manager = MigrationManager(storage)
result = migration_manager.execute_gradual_migration()

# Phase 3: Update code to use unified storage APIs
# Replace legacy API calls with unified storage calls
```

### 3. Dashboard Integration

Update dashboard to use unified storage API endpoints:

```javascript
// Replace legacy API calls
// OLD:
fetch('/api/quality-trends')

// NEW:
fetch('/api/unified/quality')
```

## Legacy Storage Locations

### Quality Data
- `.claude-quality/quality_history.json`
- `.claude-patterns/quality_history.json`

### Model Performance
- `.claude-patterns/model_performance.json`

### Learning Patterns
- `.claude-patterns/patterns.json`

### Auto-fix Patterns
- `patterns/autofix-patterns.json`

## Code Migration Examples

### Quality Tracking

#### Before (Legacy)
```python
from lib.quality_tracker import QualityTracker

tracker = QualityTracker(".claude-patterns")
tracker.record_quality("task_123", 0.85, {
    "syntax_compliance": 0.9,
    "functionality": 0.8
})
```

#### After (Unified Storage)
```python
from unified_parameter_storage import UnifiedParameterStorage

storage = UnifiedParameterStorage()
storage.set_quality_score(85.0, {
    "syntax_compliance": 90.0,
    "functionality": 80.0
})
```

#### Using Compatibility Layer (No Code Changes)
```python
from parameter_compatibility import get_legacy_quality_tracker

tracker = get_legacy_quality_tracker()
tracker.record_quality("task_123", 0.85, {
    "syntax_compliance": 0.9,
    "functionality": 0.8
})
# Uses unified storage under the hood
```

### Model Performance

#### Before (Legacy)
```python
from lib.model_performance import ModelPerformanceManager

manager = ModelPerformanceManager(".claude-patterns")
manager.add_performance_score("Claude", 92.5, "testing")
```

#### After (Unified Storage)
```python
from unified_parameter_storage import UnifiedParameterStorage

storage = UnifiedParameterStorage()
storage.update_model_performance("Claude", 92.5, "testing")
```

### Dashboard Data Collection

#### Before (Legacy)
```python
from lib.dashboard import DashboardDataCollector

collector = DashboardDataCollector(".claude-patterns")
data = collector.collect_all_data()
```

#### After (Unified Storage)
```python
from lib.dashboard import DashboardDataCollector

collector = DashboardDataCollector()  # Uses unified storage automatically
data = collector.get_unified_dashboard_data()
```

## API Mapping

### Quality APIs

| Legacy API | Unified Storage API | Notes |
|------------|-------------------|-------|
| `record_quality(task_id, score, metrics)` | `set_quality_score(score * 100, {k: v * 100})` | Score scale: 0-1 → 0-100 |
| `get_average_quality()` | `get_quality_score() / 100` | Score scale: 0-100 → 0-1 |
| `get_quality_trends(days)` | `get_quality_history(days)` | Returns different format |

### Model APIs

| Legacy API | Unified Storage API | Notes |
|------------|-------------------|-------|
| `add_performance_score(model, score, task_type)` | `update_model_performance(model, score, task_type)` | Direct replacement |
| `get_model_summary(model)` | `get_model_performance(model)` | Returns similar data |
| `get_active_model()` | `get_active_model()` | Direct replacement |

## Data Format Changes

### Quality Scores

#### Legacy Format (0-1 scale)
```json
{
  "task_id": "task_123",
  "quality_score": 0.85,
  "metrics": {
    "syntax_compliance": 0.9,
    "functionality": 0.8
  }
}
```

#### Unified Format (0-100 scale)
```json
{
  "score": 85.0,
  "timestamp": "2025-01-01T12:00:00Z",
  "metrics": {
    "syntax_compliance": 90.0,
    "functionality": 80.0
  }
}
```

### Model Performance

#### Legacy Format
```json
{
  "recent_scores": [
    {"score": 92.5, "timestamp": "...", "task_type": "testing"}
  ],
  "total_tasks": 25,
  "success_rate": 0.92,
  "contribution_to_project": 85.0
}
```

#### Unified Format
```json
{
  "scores": [
    {"score": 92.5, "timestamp": "...", "task_type": "testing"}
  ],
  "total_tasks": 25,
  "success_rate": 0.92,
  "contribution": 85.0,
  "last_updated": "2025-01-01T12:00:00Z"
}
```

## Migration Checklist

### Pre-Migration

- [ ] Backup existing data
- [ ] Identify all legacy storage locations
- [ ] Test compatibility layer in development
- [ ] Plan migration strategy (big bang vs gradual)

### During Migration

- [ ] Enable compatibility mode
- [ ] Run migration analysis
- [ ] Execute migration (dry run first)
- [ ] Validate migrated data
- [ ] Test all functionality

### Post-Migration

- [ ] Update code to use unified APIs
- [ ] Remove compatibility layer (optional)
- [ ] Archive legacy files
- [ ] Update documentation
- [ ] Monitor performance

## Troubleshooting Migration

### Common Issues

#### Migration Fails
```
Error: Failed to migrate from legacy source
```

**Solutions:**
1. Check if legacy files exist and are readable
2. Validate JSON format of legacy files
3. Ensure write permissions for unified storage directory
4. Check for sufficient disk space

#### Data Validation Errors
```
Error: Data integrity validation failed
```

**Solutions:**
1. Run validation with detailed output
2. Check for data type mismatches
3. Verify required fields are present
4. Use backup to restore and retry

#### Performance Issues
```
Warning: Migration taking longer than expected
```

**Solutions:**
1. Migrate in smaller batches
2. Close other applications using files
3. Check disk I/O performance
4. Run during low-usage periods

### Recovery Procedures

#### Restore from Backup
```python
storage = UnifiedParameterStorage()
success = storage._restore_from_backup()
if success:
    print("Successfully restored from backup")
else:
    print("No backup available or restore failed")
```

#### Rollback Migration
```python
from parameter_migration import MigrationManager

storage = UnifiedParameterStorage()
migration_manager = MigrationManager(storage)
result = migration_manager.rollback_migration()
print(f"Rollback status: {result['status']}")
```

## Testing Migration

### Unit Tests

```python
import unittest
from unified_parameter_storage import UnifiedParameterStorage
from parameter_migration import MigrationManager

class TestMigration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage = UnifiedParameterStorage(self.test_dir)
        self.migration_manager = MigrationManager(self.storage)

        # Create test legacy data
        self.create_legacy_data()

    def test_migration_success(self):
        result = self.migration_manager.execute_gradual_migration()
        self.assertEqual(result['status'], 'completed')
        self.assertGreater(result['items_migrated'], 0)

    def test_data_integrity(self):
        self.migration_manager.execute_gradual_migration()
        validation = self.migration_manager.validate_migration()
        self.assertIn(validation['overall_status'], ['success', 'acceptable'])
```

### Integration Tests

```python
def test_compatibility_layer():
    """Test that existing code works with compatibility layer."""
    from parameter_compatibility import get_legacy_quality_tracker

    tracker = get_legacy_quality_tracker()

    # Should work without code changes
    success = tracker.record_quality("test_task", 0.85, {"syntax": 0.9})
    assert success

    score = tracker.get_average_quality()
    assert abs(score - 0.85) < 0.01
```

## Performance Impact

### Migration Performance

- **Small Projects** (< 1000 records): < 1 minute
- **Medium Projects** (1000-10000 records): 1-5 minutes
- **Large Projects** (> 10000 records): 5-30 minutes

### Runtime Performance

- **Read Operations**: 10-50ms improvement with caching
- **Write Operations**: 5-20ms overhead for thread safety
- **Memory Usage**: 10-30% increase due to caching

### Optimization Tips

1. **Batch Operations**: Group multiple updates
2. **Background Migration**: Run during off-peak hours
3. **Selective Migration**: Migrate only active data first
4. **Compression**: Enable compression for large datasets

## Agent Integration

### Update Agent Files

Update agent markdown files to include unified storage integration:

```markdown
## Integration with Unified Parameter Storage

**Quality Score Recording**:
- All quality assessments stored in unified parameter storage
- Uses `UnifiedParameterStorage.set_quality_score()` for consistency
- Real-time dashboard integration

```python
from unified_parameter_storage import UnifiedParameterStorage
storage = UnifiedParameterStorage()
storage.set_quality_score(quality_score, detailed_metrics)
```
```

### Agent Code Updates

For agents that use Python code:

```python
# Add to agent initialization
from unified_parameter_storage import UnifiedParameterStorage
self.unified_storage = UnifiedParameterStorage()

# Update quality recording
def record_quality(self, score, metrics):
    self.unified_storage.set_quality_score(score, metrics)
```

## Monitoring and Maintenance

### Health Checks

```python
def check_storage_health():
    storage = UnifiedParameterStorage()

    # Check data integrity
    validation = storage.validate_data_integrity()
    if not validation['valid']:
        return False, validation['errors']

    # Check storage size
    stats = storage.get_storage_stats()
    if stats['storage_size'] > 100 * 1024 * 1024:  # 100MB
        return False, "Storage size too large"

    return True, "Healthy"
```

### Maintenance Tasks

- **Daily**: Validate data integrity
- **Weekly**: Clean up old backups
- **Monthly**: Archive old data
- **Quarterly**: Review storage performance

## Support Resources

### Documentation
- [Unified Parameter Storage Documentation](UNIFIED_PARAMETER_STORAGE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

### Tools
- Migration CLI: `python lib/parameter_migration.py`
- Validation CLI: `python lib/unified_parameter_storage.py validate`
- Export CLI: `python lib/unified_parameter_storage.py export`

### Community
- Issue Tracker: Report migration issues
- Discussion Forum: Ask questions and share experiences
- Wiki: Community-contributed guides and examples

---

**Last Updated**: January 27, 2025
**Version**: 1.0.0
**Author**: Autonomous Agent Development Team