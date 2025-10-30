# Unified Parameter Storage System

## Overview

The Unified Parameter Storage System is a comprehensive solution for centralizing all parameter storage across the Autonomous Agent Plugin. It provides a single, reliable source of truth for quality scores, model performance metrics, learning patterns, dashboard data, and auto-fix patterns.

### Key Features

- **Centralized Storage**: Single location for all parameters and metrics
- **Thread-Safe Operations**: Concurrent access with proper file locking
- **Cross-Platform Compatibility**: Windows, Linux, and macOS support
- **Backward Compatibility**: Seamless migration from legacy storage systems
- **Performance Optimized**: Caching and efficient data structures
- **Data Integrity**: Validation, backup, and recovery mechanisms
- **Real-Time Access**: Dashboard integration for live monitoring

## Architecture

### Storage Structure

```
.claude-unified/
├── unified_parameters.json    # Main storage file
├── backups/                   # Automatic backups
│   ├── unified_parameters_YYYYMMDD_HHMMSS.json
│   └── ...
├── migration_backups/         # Migration backups
│   └── ...
└── migrated_sources/          # Archived legacy files
    └── ...
```

### Data Schema

```json
{
  "version": "1.0.0",
  "metadata": {
    "created_at": "2025-01-01T00:00:00Z",
    "last_updated": "2025-01-01T12:00:00Z",
    "migration_history": []
  },
  "parameters": {
    "quality": {
      "scores": {
        "current": 85.5,
        "history": [...],
        "trends": {},
        "averages": {}
      },
      "metrics": {
        "syntax_compliance": 90.0,
        "functionality": 85.0,
        "maintainability": 88.0,
        "documentation": 82.0,
        "pattern_adherence": 87.0,
        "code_metrics": 84.0
      }
    },
    "models": {
      "active_model": "Claude",
      "performance": {
        "Claude": {
          "scores": [...],
          "success_rate": 0.92,
          "contribution": 85.0,
          "total_tasks": 150,
          "last_updated": "2025-01-01T12:00:00Z"
        }
      },
      "usage_stats": {
        "total_queries": 1000,
        "model_switches": 25,
        "preferred_models": ["Claude", "GLM"]
      }
    },
    "learning": {
      "patterns": {
        "skill_effectiveness": {...},
        "agent_performance": {...},
        "task_patterns": [...],
        "success_rates": {...}
      },
      "analytics": {
        "learning_rate": 0.85,
        "prediction_accuracy": 0.78,
        "optimization_suggestions": [...]
      }
    },
    "dashboard": {
      "metrics": {
        "active_tasks": 5,
        "completed_tasks": 100,
        "failed_tasks": 3,
        "average_response_time": 2.5,
        "system_health": 95.0
      },
      "real_time": {
        "current_model": "Claude",
        "last_activity": "2025-01-01T12:00:00Z",
        "active_agents": ["quality-controller", "test-engineer"],
        "resource_usage": {...}
      }
    },
    "autofix": {
      "patterns": {...},
      "success_rates": {...},
      "usage_statistics": {...}
    }
  }
}
```

## Quick Start

### Basic Usage

```python
from unified_parameter_storage import UnifiedParameterStorage

# Initialize storage
storage = UnifiedParameterStorage()

# Store quality score
storage.set_quality_score(85.5, {
    "syntax_compliance": 90.0,
    "functionality": 85.0,
    "documentation": 80.0
})

# Store model performance
storage.update_model_performance("Claude", 92.0, "feature_implementation")

# Update dashboard metrics
storage.update_dashboard_metrics({
    "active_tasks": 3,
    "completed_tasks": 25,
    "system_health": 97.5
})

# Retrieve data
quality_score = storage.get_quality_score()
model_perf = storage.get_model_performance("Claude")
dashboard_data = storage.get_dashboard_data()
```

### CLI Usage

```bash
# Set quality score
python <plugin_path>/lib/unified_parameter_storage.py set-quality --score 85.5

# Set active model
python <plugin_path>/lib/unified_parameter_storage.py set-model --model Claude

# Migrate from legacy storage
python <plugin_path>/lib/unified_parameter_storage.py migrate

# Get storage statistics
python <plugin_path>/lib/unified_parameter_storage.py stats

# Validate data integrity
python <plugin_path>/lib/unified_parameter_storage.py validate

# Export data
python <plugin_path>/lib/unified_parameter_storage.py export --path backup.json --format json
```

## API Reference

### UnifiedParameterStorage Class

#### Core Methods

##### `set_quality_score(score: float, metrics: Dict[str, float] = None) -> None`
Set current quality score with optional detailed metrics.

**Parameters:**
- `score`: Quality score (0-100)
- `metrics`: Optional dictionary of detailed metrics

**Example:**
```python
storage.set_quality_score(88.0, {
    "syntax_compliance": 92.0,
    "functionality": 87.0,
    "documentation": 85.0
})
```

##### `get_quality_score() -> float`
Get current quality score.

**Returns:** Current quality score (0-100)

##### `get_quality_history(days: int = 30) -> List[Dict[str, Any]]`
Get quality score history.

**Parameters:**
- `days`: Number of days to include in history

**Returns:** List of historical quality records

##### `set_active_model(model: str) -> None`
Set currently active AI model.

**Parameters:**
- `model`: Model name (e.g., "Claude", "OpenAI", "GLM")

##### `update_model_performance(model: str, score: float, task_type: str = "unknown") -> None`
Update performance metrics for a model.

**Parameters:**
- `model`: Model name
- `score`: Performance score (0-100)
- `task_type`: Type of task performed

##### `get_model_performance(model: str) -> Dict[str, Any]`
Get performance data for a specific model.

**Parameters:**
- `model`: Model name

**Returns:** Dictionary with model performance data

##### `update_dashboard_metrics(metrics: Dict[str, Any]) -> None`
Update dashboard metrics.

**Parameters:**
- `metrics`: Dictionary of dashboard metrics to update

##### `get_dashboard_data() -> Dict[str, Any]`
Get complete dashboard data.

**Returns:** Dictionary with all dashboard data

#### Migration Methods

##### `migrate_from_legacy_storage(force: bool = False) -> Dict[str, Any]`
Migrate data from legacy storage systems.

**Parameters:**
- `force`: Force migration even if already completed

**Returns:** Migration result dictionary

#### Utility Methods

##### `get_storage_stats() -> Dict[str, Any]`
Get storage statistics and metadata.

**Returns:** Dictionary with storage statistics

##### `validate_data_integrity() -> Dict[str, Any]`
Validate data integrity and structure.

**Returns:** Validation result dictionary

##### `export_data(export_path: str, format: str = "json") -> bool`
Export data to external file.

**Parameters:**
- `export_path`: Path to export file
- `format`: Export format ("json" or "csv")

**Returns:** True if export was successful

##### `import_data(import_path: str, merge_strategy: str = "overwrite") -> bool`
Import data from external file.

**Parameters:**
- `import_path`: Path to import file
- `merge_strategy`: How to merge with existing data ("overwrite", "merge", "skip")

**Returns:** True if import was successful

## Migration Guide

### From Legacy Storage

The unified storage system includes automatic migration from legacy storage locations:

#### Legacy Storage Locations
- `.claude-quality/quality_history.json`
- `.claude-patterns/quality_history.json`
- `.claude-patterns/model_performance.json`
- `.claude-patterns/patterns.json`
- `patterns/autofix-patterns.json`

#### Migration Process

1. **Automatic Migration**: When first initialized, the system detects and migrates legacy data
2. **Manual Migration**: Use the CLI or API to trigger migration
3. **Validation**: Built-in validation ensures data integrity
4. **Rollback**: Backup files allow rollback if needed

#### Example Migration

```python
from unified_parameter_storage import UnifiedParameterStorage
from parameter_migration import MigrationManager

# Initialize storage
storage = UnifiedParameterStorage()

# Create migration manager
migration_manager = MigrationManager(storage)

# Analyze migration complexity
analysis = migration_manager.analyze_migration_complexity()
print(f"Found {analysis['total_sources']} legacy sources")

# Execute migration
result = migration_manager.execute_gradual_migration()
print(f"Migrated {result['items_migrated']} items")

# Validate migration
validation = migration_manager.validate_migration()
print(f"Migration status: {validation['overall_status']}")
```

### Compatibility Layer

For existing code that uses legacy storage APIs, use the compatibility layer:

```python
from parameter_compatibility import (
    get_legacy_quality_tracker,
    get_legacy_model_performance_manager
)

# Use legacy API with unified storage backend
tracker = get_legacy_quality_tracker()
tracker.record_quality("task_id", 0.85, {"syntax": 0.9})

manager = get_legacy_model_performance_manager()
manager.add_performance_score("Claude", 92.0, "testing")
```

## Dashboard Integration

### API Endpoints

The unified storage system integrates with the dashboard via REST API:

#### GET `/api/unified/quality`
Get quality data from unified storage.

**Response:**
```json
{
  "current_score": 85.5,
  "history": [...],
  "metrics": {...},
  "source": "unified_storage"
}
```

#### GET `/api/unified/models`
Get model performance data.

**Response:**
```json
{
  "active_model": "Claude",
  "model_performance": {...},
  "source": "unified_storage"
}
```

#### GET `/api/unified/dashboard`
Get complete dashboard data.

#### POST `/api/unified/quality`
Update quality score.

**Request:**
```json
{
  "score": 85.5,
  "metrics": {"syntax_compliance": 90.0},
  "task_id": "optional_task_id"
}
```

#### POST `/api/unified/migrate`
Trigger migration from legacy storage.

#### GET `/api/unified/validate`
Validate data integrity.

### JavaScript Integration

```javascript
// Fetch quality data
async function getQualityData() {
    const response = await fetch('/api/unified/quality');
    return await response.json();
}

// Update quality score
async function updateQualityScore(score, metrics) {
    const response = await fetch('/api/unified/quality', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ score, metrics })
    });
    return await response.json();
}
```

## Performance Considerations

### Caching

- **Read Caching**: 30-second TTL cache for read operations
- **Write-Through**: Writes update cache immediately
- **Cache Invalidation**: Automatic on write operations

### Concurrency

- **File Locking**: Platform-specific file locking (fcntl/Unix, msvcrt/Windows)
- **Thread Safety**: All operations are thread-safe
- **Atomic Operations**: Critical sections protected by locks

### Memory Usage

- **Lazy Loading**: Data loaded on-demand
- **Streaming**: Large datasets processed in chunks
- **Garbage Collection**: Regular cleanup of old data

### Optimization Tips

1. **Batch Operations**: Group multiple updates together
2. **Use Cache**: Enable caching for frequently accessed data
3. **Periodic Cleanup**: Archive old data to reduce file size
4. **Background Migration**: Run migrations during low-usage periods

## Backup and Recovery

### Automatic Backups

- **Frequency**: Created before each write operation
- **Retention**: Last 10 backups maintained
- **Location**: `.claude-unified/backups/`

### Manual Backup

```python
# Create manual backup
storage._create_backup()

# Restore from backup
success = storage._restore_from_backup()
```

### Export/Import

```python
# Export data
storage.export_data("backup.json", "json")

# Import data
storage.import_data("backup.json", "merge")
```

## Troubleshooting

### Common Issues

#### File Access Errors
```
Error: Permission denied accessing storage file
```
**Solution**: Check file permissions and ensure no other processes have exclusive access.

#### Migration Failures
```
Error: Failed to migrate legacy data
```
**Solution**: Check legacy file formats and ensure they're valid JSON.

#### Data Corruption
```
Error: Malformed JSON in storage file
```
**Solution**: Use automatic backup restore or validation tools.

### Validation Tools

```python
# Validate data integrity
validation = storage.validate_data_integrity()
if not validation['valid']:
    print("Issues found:", validation['errors'])

# Get storage statistics
stats = storage.get_storage_stats()
print(f"Storage size: {stats['storage_size']} bytes")
```

### Debug Logging

Enable debug logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Operations will now show detailed debug information
storage = UnifiedParameterStorage()
```

## Best Practices

### Data Management

1. **Regular Backups**: Schedule regular exports of important data
2. **Validation**: Periodically validate data integrity
3. **Cleanup**: Archive old data to maintain performance
4. **Monitoring**: Monitor storage size and performance metrics

### Code Integration

1. **Error Handling**: Always handle storage operation errors
2. **Retry Logic**: Implement retry logic for transient failures
3. **Fallbacks**: Provide fallback mechanisms when storage unavailable
4. **Testing**: Test with both available and unavailable storage

### Performance

1. **Batch Operations**: Group multiple updates together
2. **Async Operations**: Use async operations for UI applications
3. **Caching**: Leverage built-in caching for read-heavy workloads
4. **Monitoring**: Monitor operation timing and performance

## Security Considerations

### File Permissions

- **Restrict Access**: Limit file access to authorized users
- **Secure Storage**: Store sensitive data in secure locations
- **Backup Security**: Secure backup files with appropriate permissions

### Data Validation

- **Input Validation**: Validate all input data
- **Sanitization**: Sanitize data before storage
- **Type Checking**: Ensure data types are correct
- **Range Validation**: Validate numeric ranges

### Access Control

- **API Security**: Secure API endpoints with authentication
- **Rate Limiting**: Implement rate limiting for API access
- **Audit Logging**: Log all access and modifications

## Version History

### v1.0.0 (Current)
- Initial release
- Core parameter storage functionality
- Migration system from legacy storage
- Dashboard integration
- Thread safety and cross-platform support

### Future Versions
- Scheduled for v1.1.0:
  - Compression support for large datasets
  - Advanced caching strategies
  - Performance monitoring and analytics
  - Enhanced backup and recovery options

## Support and Contributing

### Getting Help

- **Documentation**: Check this documentation first
- **Issues**: Report issues on the project repository
- **Community**: Join discussions for questions and suggestions

### Contributing

- **Code**: Follow contribution guidelines
- **Tests**: Add tests for new functionality
- **Documentation**: Update documentation for changes
- **Reviews**: Participate in code reviews

---

**Last Updated**: January 27, 2025
**Version**: 1.0.0
**Author**: Autonomous Agent Development Team