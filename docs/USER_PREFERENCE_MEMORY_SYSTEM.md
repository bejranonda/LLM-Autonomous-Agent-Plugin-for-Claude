# User Preference Memory System

## Overview

The User Preference Memory System is a comprehensive component of the Autonomous Agent Plugin that captures, stores, and learns from user preferences and system environments to provide personalized development guidance and intelligent suggestions.

## Key Features

### 1. User Preference Storage
- **Persistent Storage**: Stores user preferences in JSON format with cross-platform compatibility
- **Category Organization**: Organized into development, workflow, UI, and privacy categories
- **Version Control**: Tracks preference changes with timestamps and migration support
- **Privacy-First Design**: Optional data sharing with granular privacy controls

### 2. System Environment Detection
- **Comprehensive Profiling**: Hardware, software, and development environment detection
- **Cross-Platform Support**: Windows, Linux, and macOS compatibility
- **Resource Monitoring**: CPU, memory, disk usage tracking
- **Development Tools**: Auto-detection of installed development tools and editors

### 3. Intelligent Suggestion Engine
- **Context-Aware Suggestions**: Based on current task, quality score, and project state
- **Learning System**: Improves suggestions based on user behavior and preferences
- **Multi-Factor Scoring**: Confidence, priority, impact, and relevance scoring
- **Template-Based Generation**: Extensible suggestion templates for customization

### 4. Task Queue Integration
- **Sequential Execution**: Queue tasks for uninterrupted batch operations
- **Priority Management**: Critical, high, medium, low priority levels
- **Dependency Handling**: Task dependencies and prerequisite management
- **Auto-Retry Logic**: Intelligent retry with exponential backoff

## Architecture

### Core Components

#### 1. UserPreferenceMemory Class
```python
class UserPreferenceMemory:
    """Main class for managing user preferences and system profiles."""

    def __init__(self, storage_dir: str = ".claude-preferences")
    def set_preference(self, category: str, key: str, value: Any)
    def get_preference(self, category: str, key: str, default: Any = None) -> Any
    def record_command_usage(self, command: str, context: Dict[str, Any])
    def record_task_completion(self, task_type: str, success: bool, quality_score: float)
    def get_user_profile(self) -> Dict[str, Any]
```

#### 2. SystemProfiler Class
```python
class SystemProfiler:
    """Comprehensive system environment detection and profiling."""

    def get_system_fingerprint(self) -> Dict[str, Any]
    def _get_system_info(self) -> Dict[str, Any]
    def _get_hardware_info(self) -> Dict[str, Any]
    def _get_development_environment(self) -> Dict[str, Any]
    def _assess_system_capabilities(self) -> Dict[str, Any]
```

#### 3. IntelligentSuggestionEngine Class
```python
class IntelligentSuggestionEngine:
    """Generates context-aware suggestions based on patterns and preferences."""

    def generate_suggestions(self, context: SuggestionContext, max_suggestions: int = 5) -> List[Dict[str, Any]]
    def record_suggestion_response(self, suggestion: Dict[str, Any], accepted: bool)
    def create_custom_template(self, template_id: str, category: str, ...) -> bool
    def get_suggestion_analytics(self) -> Dict[str, Any]
```

#### 4. Enhanced TaskQueue Class
```python
class TaskQueue:
    """Enhanced task queue with priority-based execution and slash command support."""

    def add_task(self, name: str, description: str, command: str = None, ...) -> str
    def add_slash_command(self, command: str, description: str = None, ...) -> str
    def start_sequential_execution(self, stop_on_error: bool = False) -> bool
    def get_status(self) -> Dict[str, Any]
    def list_tasks(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]
```

## Storage Structure

### Directory Layout
```
.claude-preferences/
├── user_preferences.json      # Main user preferences file
├── system_environment.json     # System environment profiles
├── suggestions_history.json   # Suggestion response history
├── suggestion_templates.json  # Custom suggestion templates
├── suggestion_analytics.json  # Suggestion effectiveness analytics
└── backups/                   # Automatic backups
    ├── user_preferences_20241228_143022.json
    └── system_environment_20241228_143022.json
```

### User Preferences Schema
```json
{
  "version": "1.0.0",
  "created_at": "2024-12-28T14:30:22.123Z",
  "last_updated": "2024-12-28T14:30:22.123Z",
  "user_id": "abc123def456",
  "preferences": {
    "development": {
      "preferred_languages": ["python", "javascript"],
      "frameworks": ["flask", "react"],
      "tools": ["git", "docker", "vscode"],
      "code_style": {"indent_size": 4, "quote_style": "single"},
      "testing_preference": "comprehensive",
      "documentation_style": "detailed"
    },
    "workflow": {
      "auto_save": true,
      "auto_backup": true,
      "parallel_execution": true,
      "quality_threshold": 70,
      "suggestion_level": "balanced",
      "notification_level": "important"
    },
    "ui": {
      "theme": "auto",
      "verbosity": "medium",
      "show_progress": true,
      "confirm_destructive": true
    },
    "privacy": {
      "share_patterns": false,
      "share_analytics": false,
      "local_storage_only": true,
      "data_retention_days": 90
    }
  },
  "learned_patterns": {
    "command_preferences": {
      "/analyze:quality": {
        "usage_count": 15,
        "last_used": "2024-12-28T10:30:00Z",
        "success_rate": 0.93,
        "contexts": [...]
      }
    },
    "agent_effectiveness": {...},
    "skill_success_rates": {...},
    "common_workflows": [...],
    "error_patterns": {...}
  },
  "history": {
    "commands_used": [...],
    "tasks_completed": [...],
    "suggestions_accepted": [...],
    "suggestions_rejected": [...]
  }
}
```

## Slash Commands

### Queue Management Commands

#### /queue:add
Add tasks to the autonomous task queue for sequential execution.

```bash
/queue:add --name "Task Name" --description "Description" --command "command" --priority high
```

#### /queue:slash
Add slash commands directly to the queue.

```bash
/queue:slash --command "/analyze:quality" --priority high
```

#### /queue:execute
Execute queued tasks sequentially.

```bash
/queue:execute [--stop-on-error] [--background]
```

#### /queue:status
Show comprehensive queue status.

```bash
/queue:status [--verbose]
```

#### /queue:list
List tasks with filtering options.

```bash
/queue:list [--status STATUS] [--priority PRIORITY] [--limit N]
```

#### /queue:retry
Retry failed tasks.

```bash
/queue:retry [--task-id ID] [--status failed] [--priority high]
```

#### /queue:clear
Clean up completed tasks.

```bash
/queue:clear [--older-than HOURS] [--status completed] [--dry-run]
```

### Preference Management Commands

#### /preferences:set
Set user preferences.

```bash
/preferences:set --category development --key preferred_languages --value '["python", "javascript"]'
```

#### /preferences:get
Get user preferences.

```bash
/preferences:get --category workflow --key quality_threshold
```

#### /preferences:show
Show all user preferences.

```bash
/preferences:show
```

#### /preferences:profile
Show comprehensive user profile.

```bash
/preferences:profile
```

#### /preferences:export
Export preferences to file.

```bash
/preferences:export --path preferences.json [--include-sensitive]
```

#### /preferences:import
Import preferences from file.

```bash
/preferences:import --path preferences.json --strategy merge
```

### Suggestion Commands

#### /suggest:generate
Generate intelligent suggestions.

```bash
/suggest:generate [--max 5] [--quality 75] [--project-type web]
```

## Integration Points

### 1. Orchestrator Integration
The orchestrator automatically:
- Detects special slash commands for direct execution
- Routes queue commands to enhanced task queue
- Routes preference commands to user preference memory
- Routes suggestion commands to intelligent suggestion engine

### 2. Learning Engine Integration
- Records user command usage patterns
- Tracks suggestion response rates
- Updates preference effectiveness metrics
- Improves future suggestion quality

### 3. Parameter Storage Integration
- Shares data with unified parameter storage
- Maintains consistency across systems
- Provides backup and recovery capabilities
- Supports data migration and versioning

## Usage Examples

### Setting Up Personalized Workflow

```bash
# Set your preferred languages
/preferences:set --category development --key preferred_languages --value '["python", "typescript"]'

# Set quality threshold
/preferences:set --category workflow --key quality_threshold --value 85

# Queue multiple tasks for batch execution
/queue:slash --command "/analyze:project" --priority high
/queue:slash --command "/analyze:quality" --priority medium
/queue:slash --command "/validate:fullstack" --priority medium

# Execute all tasks sequentially
/queue:execute --background
```

### Intelligent Suggestion Usage

```bash
# Get suggestions based on current context
/suggest:generate --quality 70 --project-type web

# System might suggest:
# 1. [High Priority] Run quality check (score: 70/100)
#    → /analyze:quality
# 2. [Recommended] Update documentation
#    → /dev:auto "update documentation"
# 3. [Optional] Optimize performance
#    → /dev:auto "optimize performance"
```

### Learning from User Behavior

The system automatically learns:
- Commands you use frequently
- Tasks you prefer to batch together
- Quality thresholds you maintain
- Suggestion patterns you accept/reject

## Configuration

### Environment Variables
```bash
export CLAUDE_PREFERENCES_DIR="/path/to/preferences"
export CLAUDE_QUEUE_DIR="/path/to/queue"
export CLAUDE_SUGGESTION_CACHE_TTL="3600"
```

### Default Preferences
```json
{
  "development": {
    "preferred_languages": [],
    "frameworks": [],
    "tools": [],
    "testing_preference": "balanced",
    "documentation_style": "comprehensive"
  },
  "workflow": {
    "auto_save": true,
    "auto_backup": true,
    "parallel_execution": true,
    "quality_threshold": 70,
    "suggestion_level": "balanced"
  },
  "ui": {
    "theme": "auto",
    "verbosity": "medium",
    "show_progress": true
  },
  "privacy": {
    "local_storage_only": true,
    "data_retention_days": 90
  }
}
```

## Performance Considerations

### Storage Optimization
- **Caching**: 30-second cache for preference reads
- **Compression**: Optional JSON compression for large datasets
- **Cleanup**: Automatic cleanup of old history entries
- **Backup Rotation**: Keep only last 5 automatic backups

### Memory Usage
- **Lazy Loading**: Load components only when needed
- **Efficient Data Structures**: Use dictionaries for O(1) lookups
- **Background Processing**: Non-blocking suggestion generation
- **Resource Monitoring**: Track and optimize memory usage

## Privacy and Security

### Data Protection
- **Local Storage**: All data stored locally by default
- **Encryption**: Optional encryption for sensitive data
- **Access Control**: File system permissions for preference files
- **Data Minimization**: Collect only necessary preference data

### Privacy Controls
```json
{
  "privacy": {
    "share_patterns": false,
    "share_analytics": false,
    "local_storage_only": true,
    "data_retention_days": 90,
    "anonymize_data": true,
    "encryption_enabled": false
  }
}
```

## Troubleshooting

### Common Issues

#### Preference File Not Found
```bash
# Initialize preferences
/preferences:profile

# Check file permissions
ls -la .claude-preferences/
```

#### Queue Execution Fails
```bash
# Check queue status
/queue:status --verbose

# Retry failed tasks
/queue:retry --status failed
```

#### Suggestions Not Generated
```bash
# Check system profile
/preferences:profile

# Generate suggestions manually
/suggest:generate --max 10
```

### Debug Mode
```bash
# Enable debug logging
export CLAUDE_DEBUG=true

# Check system compatibility
python lib/user_preference_memory.py --profile
```

## API Reference

### UserPreferenceMemory API
```python
# Initialize
memory = UserPreferenceMemory("/path/to/preferences")

# Set preferences
memory.set_preference("development", "preferred_languages", ["python", "js"])

# Get preferences
languages = memory.get_preference("development", "preferred_languages", ["python"])

# Record usage
memory.record_command_usage("/analyze:quality", {"project_type": "web"})

# Get profile
profile = memory.get_user_profile()
```

### TaskQueue API
```python
# Initialize
queue = TaskQueue("/path/to/queue")

# Add task
task_id = queue.add_task("Quality Check", "Run quality analysis", "/analyze:quality", "high")

# Add slash command
cmd_id = queue.add_slash_command("/analyze:dependencies", "Security scan", "high")

# Execute
queue.start_sequential_execution(stop_on_error=True)

# Get status
status = queue.get_status()
```

### SuggestionEngine API
```python
# Initialize
engine = IntelligentSuggestionEngine("/path/to/preferences")

# Create context
context = SuggestionContext()
context.quality_score = 75
context.project_type = "web"

# Generate suggestions
suggestions = engine.generate_suggestions(context, max_suggestions=5)

# Record response
engine.record_suggestion_response(suggestions[0], accepted=True)
```

## Migration Guide

### From v5.1.x to v5.2.0
1. **Backup Existing Data**: Export preferences before upgrade
2. **Update Directory Structure**: New `.claude-preferences/` directory
3. **Migrate Settings**: Automatic migration of existing preferences
4. **Verify Integration**: Test new slash commands

### Data Migration
```bash
# Export old preferences
python lib/user_preference_memory.py --export old_prefs.json

# Import to new system
python lib/user_preference_memory.py --import old_prefs.json --strategy merge
```

## Future Enhancements

### Planned Features
- **Multi-Project Profiles**: Separate preferences per project
- **Team Collaboration**: Shared preference templates
- **AI-Powered Suggestions**: ML-based recommendation engine
- **Cloud Sync**: Optional cloud synchronization
- **Mobile App**: Mobile preference management

### Extension Points
- **Custom Preference Categories**: Add domain-specific preferences
- **Plugin Integration**: Third-party plugin preference support
- **Custom Suggestion Templates**: Create specialized suggestion logic
- **Workflow Automation**: Complex workflow definitions

## Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/test_user_preference_memory.py
```

### Adding New Features
1. Follow existing code patterns and conventions
2. Add comprehensive tests
3. Update documentation
4. Ensure cross-platform compatibility
5. Test with various system configurations

## Support

### Documentation
- **User Guide**: This document
- **API Reference**: Inline code documentation
- **Examples**: `examples/` directory
- **FAQ**: `docs/FAQ.md`

### Community
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Contributing**: `CONTRIBUTING.md` for guidelines
- **Code of Conduct**: `CODE_OF_CONDUCT.md`

---

*This documentation is part of the Autonomous Agent Plugin v5.3.4*