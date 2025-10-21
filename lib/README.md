# Lib Directory - Python Utility Scripts

This directory contains optional Python utility scripts that enhance the Autonomous Claude Agent Plugin with programmatic pattern learning, task management, and quality tracking capabilities.

## Overview

These scripts provide production-ready implementations for:
- **pattern_storage.py**: JSON-based pattern learning and retrieval
- **task_queue.py**: Priority-based task queue management
- **quality_tracker.py**: Quality metrics tracking and trend analysis

## Important: Fallback Mechanism

**The plugin works perfectly fine without these Python scripts!**

If Python is not available or these scripts fail to execute, the plugin will automatically fall back to the pure Markdown-based skill system. The agents and skills are designed to work in both modes:

1. **With Python Scripts** (Enhanced Mode):
   - Programmatic pattern storage and retrieval
   - Structured task queue management
   - Statistical quality analysis
   - Command-line interface for direct manipulation

2. **Without Python Scripts** (Pure MD Mode):
   - Pattern learning using JSON files managed by Claude Code tools
   - Task tracking via agent delegation and markdown notes
   - Quality assessment through agent-based evaluation
   - All core functionality remains intact

## System Requirements

- Python 3.7 or higher
- No external dependencies (uses only standard library)

## Installation Check

To verify if Python scripts are available:

```bash
# Check Python version
python3 --version

# Test pattern storage
python3 lib/pattern_storage.py stats --dir .claude-patterns

# Test task queue
python3 lib/task_queue.py status --dir .claude-patterns

# Test quality tracker
python3 lib/quality_tracker.py average --dir .claude-patterns
```

If any of these commands fail, the plugin will automatically use the pure Markdown mode.

## Usage Examples

### Pattern Storage

```bash
# Store a new pattern
python3 lib/pattern_storage.py store --pattern '{
  "task_type": "refactoring",
  "context": "authentication module security improvements",
  "skills_used": ["code-analysis", "quality-standards"],
  "approach": "Applied OWASP guidelines and refactored auth flow",
  "quality_score": 0.92
}'

# Retrieve similar patterns
python3 lib/pattern_storage.py retrieve \
  --context "authentication security" \
  --min-quality 0.8 \
  --limit 5

# Update pattern usage
python3 lib/pattern_storage.py update \
  --pattern-id pattern_20251021_143022 \
  --success

# View statistics
python3 lib/pattern_storage.py stats
```

### Task Queue

```bash
# Add a new task
python3 lib/task_queue.py add \
  --name "code_optimization" \
  --description "Analyze and optimize database queries" \
  --priority high \
  --skills "code-analysis,pattern-learning"

# Get next task to execute
python3 lib/task_queue.py execute-next

# Update task status
python3 lib/task_queue.py update \
  --task-id task_20251021_143022 \
  --status running

python3 lib/task_queue.py update \
  --task-id task_20251021_143022 \
  --status completed \
  --result "Optimized 5 queries, reduced load time by 40%"

# View queue status
python3 lib/task_queue.py status

# List all tasks
python3 lib/task_queue.py list

# Clear completed tasks
python3 lib/task_queue.py clear
```

### Quality Tracker

```bash
# Record quality assessment
python3 lib/quality_tracker.py record \
  --task-id task_20251021_143022 \
  --score 0.88 \
  --metrics '{
    "code_quality": 0.90,
    "test_coverage": 0.85,
    "documentation": 0.87,
    "security": 0.92
  }'

# View quality trends
python3 lib/quality_tracker.py trends --days 30

# View specific metric trends
python3 lib/quality_tracker.py trends \
  --days 30 \
  --metric code_quality

# Get average quality score
python3 lib/quality_tracker.py average --days 30

# View metric statistics
python3 lib/quality_tracker.py stats --days 30

# Show recent quality records
python3 lib/quality_tracker.py recent --limit 10

# Find low quality tasks
python3 lib/quality_tracker.py low-quality \
  --threshold 0.7 \
  --days 30
```

## Integration with Agents

The agents automatically detect and use these scripts when available:

### Orchestrator Agent
```markdown
# Check if Python utilities are available
if python3 lib/pattern_storage.py stats succeeds:
    use programmatic pattern retrieval
else:
    use JSON file reading with Read tool
```

### Learning Engine Agent
```markdown
# Store patterns using best available method
try python3 lib/pattern_storage.py store
fallback to Write tool with JSON manipulation
```

### Quality Controller Agent
```markdown
# Track quality metrics
try python3 lib/quality_tracker.py record
fallback to append to JSON file using Edit tool
```

## File Locking

All scripts implement file locking (`fcntl.flock`) to support concurrent access. This prevents corruption when multiple agents access the same files simultaneously.

## Error Handling

Scripts provide helpful error messages for:
- Malformed JSON input
- Invalid parameter values
- Missing required fields
- File access issues

All errors are reported via stderr with detailed descriptions.

## JSON Data Structures

### Pattern Storage (.claude-patterns/patterns.json)
```json
[
  {
    "pattern_id": "pattern_20251021_143022",
    "task_type": "feature_implementation",
    "context": "user authentication system",
    "skills_used": ["code-analysis", "security"],
    "approach": "JWT-based authentication with refresh tokens",
    "quality_score": 0.92,
    "completion_time_minutes": 45,
    "artifacts_created": ["auth.py", "test_auth.py"],
    "timestamp": "2025-10-21T14:30:22",
    "usage_count": 5,
    "success_rate": 0.90,
    "last_used": "2025-10-21T15:45:00"
  }
]
```

### Task Queue (.claude-patterns/task_queue.json)
```json
[
  {
    "task_id": "task_20251021_143022",
    "name": "code_optimization",
    "description": "Optimize database queries in user module",
    "priority": 3,
    "status": "completed",
    "skills": ["code-analysis", "pattern-learning"],
    "created_at": "2025-10-21T14:30:22",
    "started_at": "2025-10-21T14:31:00",
    "completed_at": "2025-10-21T15:15:00",
    "result": "Reduced query time by 40%",
    "error": null
  }
]
```

### Quality History (.claude-patterns/quality_history.json)
```json
[
  {
    "task_id": "task_20251021_143022",
    "quality_score": 0.88,
    "timestamp": "2025-10-21T15:15:22",
    "metrics": {
      "code_quality": 0.90,
      "test_coverage": 0.85,
      "documentation": 0.87,
      "security": 0.92
    }
  }
]
```

## Platform Compatibility

### Linux/Mac
All scripts work out of the box with Python 3.7+.

### Windows
Windows users should note:
- File locking uses `fcntl` which requires `pywin32` or works differently
- Scripts will detect Windows and use appropriate locking mechanism
- If locking fails, scripts fall back to unlocked mode (safe for single-agent use)

### Cross-Platform Testing
```bash
# Test on current platform
python3 lib/pattern_storage.py stats
python3 lib/task_queue.py status
python3 lib/quality_tracker.py average
```

## Troubleshooting

### Scripts Not Found
If agents report that Python scripts are not available:
1. Check Python installation: `python3 --version`
2. Verify script permissions: `chmod +x lib/*.py`
3. Try running directly: `python3 lib/pattern_storage.py --help`
4. If all fails, plugin will use pure MD mode automatically

### JSON Corruption
If JSON files become corrupted:
```bash
# Backup current files
cp .claude-patterns/patterns.json .claude-patterns/patterns.json.backup

# Reset files (scripts will recreate)
rm .claude-patterns/*.json

# Scripts will auto-recreate empty JSON files
python3 lib/pattern_storage.py stats
```

### Permission Issues
```bash
# Fix directory permissions
chmod 755 .claude-patterns
chmod 644 .claude-patterns/*.json

# Fix script permissions
chmod 755 lib/*.py
```

## Performance Considerations

- **Pattern Retrieval**: O(n) search with keyword matching (sufficient for <10k patterns)
- **Task Queue**: O(n log n) sorting on add/update (fast for <1k tasks)
- **Quality Tracking**: O(n) for trend analysis (efficient for <5k records)

For very large datasets (>10k records), consider implementing database backends.

## Future Enhancements

Potential improvements if needed:
- SQLite backend for large-scale pattern storage
- Full-text search for pattern retrieval
- Real-time quality visualization
- Pattern similarity using embeddings
- Automated pattern archival

## Contributing

When modifying these scripts:
1. Maintain zero external dependencies
2. Preserve command-line interface compatibility
3. Add comprehensive error handling
4. Update this README with new features
5. Test on Linux, Mac, and Windows

## License

Same license as the parent plugin (check root LICENSE file).
