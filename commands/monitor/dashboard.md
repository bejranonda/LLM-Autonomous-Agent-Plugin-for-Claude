---
name: monitor:dashboard
description: Launch real-time monitoring dashboard for autonomous agent system metrics and learning analytics
model: inherit
tools: Read,Write,Edit,Bash,Grep,Glob
---

# Monitor Dashboard Command

## Command: `/monitor:dashboard`

**Simple launcher** that starts a monitoring dashboard in the background and opens the web browser.

## How It Works

1. **Silent Launch**: Command executes dashboard.py directly with no console output
2. **Background Process**: Starts Flask server in background without blocking
3. **Auto Browser**: Opens default browser to dashboard URL automatically
4. **Zero Reporting**: No performance metrics or console output
5. **Direct Access**: Dashboard provides all analytics through web interface

**CRITICAL**: This command executes silently with no console reporting. All analytics and metrics are available through the web dashboard interface only.

## Usage

### Basic Usage
```bash
# Launch monitoring dashboard in background (default)
/monitor:dashboard

# Launch with custom port
/monitor:dashboard --port 8080

# Launch with external access (trusted networks only)
/monitor:dashboard --host 0.0.0.0

# Launch with custom data directory
/monitor:dashboard --data-dir /path/to/patterns

# Check if dashboard is running
/monitor:dashboard --status

# Stop running dashboard
/monitor:dashboard --stop
```

### Advanced Options
```bash
# Launch with debug mode (foreground for debugging)
/monitor:dashboard --debug

# Launch with custom refresh rate
/monitor:dashboard --refresh-rate 30

# Generate report without launching server
/monitor:dashboard --report-only

# Force restart if already running
/monitor:dashboard --restart
```

**Expected Performance**: Command completes in 1-2 seconds with dashboard running in background and browser automatically opened. No console output.

## Command Behavior and Implementation

### Direct Execution (No Agent Delegation)

**CRITICAL**: This command executes the dashboard directly without agent delegation to prevent duplicate launches.

1. **Direct Python Call**: `python <plugin_path>/lib/dashboard.py` (no agents involved)
2. **Background Process**: Runs Flask server completely in background
3. **Auto Browser**: Opens browser automatically (once only)
4. **Silent Operation**: No console reporting or status messages
5. **Web Interface**: All metrics available through dashboard only

### Implementation

**Direct Python Execution with Built-in Discovery**:
```bash
# Self-contained Python command that finds plugin AND runs dashboard:
# Windows, Linux, macOS - works from ANY directory

python -c "
import sys, os, subprocess, platform
from pathlib import Path

def find_plugin():
    home = Path.home()
    plugin_name = 'LLM-Autonomous-Agent-Plugin-for-Claude'

    # Marketplace paths (priority)
    search_paths = [
        home / '.claude' / 'plugins' / 'marketplaces' / plugin_name,
        home / '.config' / 'claude' / 'plugins' / 'marketplaces' / plugin_name,
        home / '.claude' / 'plugins' / 'marketplace' / plugin_name,
        home / '.config' / 'claude' / 'plugins' / 'marketplace' / plugin_name,
    ]

    # Platform-specific paths
    if platform.system() == 'Windows':
        appdata = Path(os.environ.get('APPDATA', ''))
        localappdata = Path(os.environ.get('LOCALAPPDATA', ''))
        if appdata:
            search_paths.extend([
                appdata / 'Claude' / 'plugins' / 'marketplaces' / plugin_name,
                appdata / 'Claude' / 'plugins' / 'autonomous-agent',
            ])
        if localappdata:
            search_paths.extend([
                localappdata / 'Claude' / 'plugins' / 'marketplaces' / plugin_name,
                localappdata / 'Claude' / 'plugins' / 'autonomous-agent',
            ])
    else:
        search_paths.extend([
            Path('/usr/local/share/claude/plugins/marketplaces') / plugin_name,
            Path('/opt/claude/plugins/marketplaces') / plugin_name,
        ])

    # Development/local installations (fallback)
    search_paths.extend([
        home / '.claude' / 'plugins' / 'autonomous-agent',
        home / '.config' / 'claude' / 'plugins' / 'autonomous-agent',
    ])

    # Search for plugin
    for path in search_paths:
        if path and (path / '.claude-plugin' / 'plugin.json').exists():
            return path

    # Development mode - check current directory and parents
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / '.claude-plugin' / 'plugin.json').exists():
            return parent

    return None

# Main execution
plugin_path = find_plugin()
if not plugin_path:
    print('ERROR: Plugin installation not found', file=sys.stderr)
    print('Please install the LLM Autonomous Agent Plugin from marketplace', file=sys.stderr)
    sys.exit(1)

dashboard_script = plugin_path / 'lib' / 'dashboard.py'
if not dashboard_script.exists():
    print(f'ERROR: Dashboard script not found at {dashboard_script}', file=sys.stderr)
    sys.exit(1)

# Execute dashboard with current directory for pattern data
args = ['--patterns-dir', '.claude-patterns'] + sys.argv[1:]
cmd = [sys.executable, str(dashboard_script)] + args
result = subprocess.run(cmd, cwd=Path.cwd())
sys.exit(result.returncode)
" --port 5000

# This single command:
# 1. Finds the plugin installation automatically
# 2. Locates dashboard.py within the plugin
# 3. Uses current directory for pattern data
# 4. Works across all platforms and installation methods
```

**Platform Support**:
- **Windows**: ✅ Native support (cmd.exe, PowerShell, Git Bash)
- **Linux**: ✅ Native support (bash, sh)
- **macOS**: ✅ Native support (bash, zsh)
- **All Installation Methods**: ✅ Marketplace, development, system-wide

**How It Works**:
1. **Built-in Discovery**: The Python script automatically searches for plugin installation across all standard locations
2. **Marketplace Priority**: Prioritizes marketplace installations over development/local installations
3. **Platform-Aware**: Uses OS-specific environment variables and paths (Windows: APPDATA/LOCALAPPDATA, Linux/macOS: standard directories)
4. **Fallback Support**: Falls back to development mode if marketplace installation not found
5. **Current Directory Access**: Preserves current working directory for pattern data access (.claude-patterns/)

**Discovery Order**:
1. **Marketplace Installations** (Primary):
   - Windows: `%USERPROFILE%\.claude\plugins\marketplaces\LLM-Autonomous-Agent-Plugin-for-Claude\`
   - macOS/Linux: `~/.claude/plugins/marketplaces/LLM-Autonomous-Agent-Plugin-for-Claude/`
   - Alternative paths in `.config/claude/plugins/`

2. **Platform-Specific Paths**:
   - Windows: `APPDATA\Claude\plugins\marketplaces\`, `LOCALAPPDATA\Claude\plugins\marketplaces\`
   - Linux/macOS: `/usr/local/share/claude/plugins/marketplaces/`, `/opt/claude/plugins/marketplaces/`

3. **Development/Local Installations** (Fallback):
   - `~/.claude/plugins/autonomous-agent/`
   - Current directory and parent directories (development mode)

**Data Access**: Pattern data always comes from current project directory (`./.claude-patterns/`), while the dashboard script runs from the plugin installation directory.

**Benefits**:
- ✅ Self-contained - no external launcher files needed
- ✅ Works from any user project directory
- ✅ Cross-platform compatible (Windows, Linux, macOS)
- ✅ Automatic plugin discovery - no hardcoded paths
- ✅ Marketplace installation priority
- ✅ Clear error messages with installation guidance

**Key Fix**: Eliminates path resolution issues by embedding discovery logic directly in the command rather than relying on external launcher files that don't exist in user project directories.

### Smart Browser Opening (Enhanced v1.0.2)

**Prevents Double Browser Opening**:
- **Existing Dashboard Detection**: Checks if dashboard is already running on ports 5000-5010
- **Browser Lock Mechanism**: Uses lock files to track browser opening per port
- **Single Browser Launch**: Opens browser only once per dashboard instance
- **Multiple Instance Support**: Handles multiple dashboard instances gracefully

**Browser Opening Logic**:
1. **Check existing dashboard**: Scans for running dashboard on specified port range
2. **Browser state tracking**: Uses temporary lock files to track browser opening state
3. **Smart opening**: Opens browser only if not already opened for that specific instance
4. **Automatic cleanup**: Removes lock files on dashboard shutdown

**Edge Cases Handled**:
- **Multiple dashboards**: Each port gets separate browser lock tracking
- **Dashboard restarts**: Lock files are properly cleaned up and recreated
- **Manual browser opening**: Respects existing browser states
- **Cross-platform**: Works on Windows, Linux, and macOS

### Expected Command Output

**Smart console output**. The command provides intelligent feedback based on dashboard state:

```
# New dashboard instance:
Starting Autonomous Agent Dashboard...
Dashboard URL: http://127.0.0.1:5000
Opening browser automatically...
Browser opened to http://127.0.0.1:5000

# Existing dashboard found:
Dashboard is already running at: http://127.0.0.1:5000
Browser already opened for this dashboard instance.

# Browser opened for existing instance:
Dashboard is already running at: http://127.0.0.1:5000
Browser opened to existing dashboard: http://127.0.0.1:5000
```

### Error Handling

If dashboard fails to start, the command fails silently. Check for common issues:

- **Port conflicts**: Use different port with `--port 8080`
- **Missing dependencies**: Install with `pip install flask flask-cors`
- **Directory issues**: Ensure `.claude-patterns` directory exists

All error handling and status information is available through the web dashboard interface.

### Process Management Commands

```bash
# Check dashboard status
/monitor:dashboard --status

# Stop dashboard
/monitor:dashboard --stop

# Restart dashboard
/monitor:dashboard --restart
```

*Process management commands are handled through the dashboard web interface.*

## Dashboard Features

### 📊 Real-time Metrics
- **Learning Progress**: Pattern effectiveness and skill improvement over time
- **Quality Trends**: Code quality metrics and validation scores
- **Agent Performance**: Success rates and execution times for specialized agents
- **System Health**: Resource usage and operational status
- **Task Analytics**: Task completion rates and learning patterns

### 📈 Interactive Charts
- **Time Series Analysis**: Performance metrics over customizable time ranges
- **Comparative Analysis**: Side-by-side agent and skill performance
- **Trend Visualization**: Learning curves and improvement trajectories
- **Distribution Charts**: Success rates and outcome distributions
- **Resource Monitoring**: CPU, memory, and storage usage patterns

### 🎯 Performance Insights
- **Skill Effectiveness**: Which skills perform best for specific task types
- **Agent Specialization**: Performance comparison across different agents
- **Learning Patterns**: How the system improves over time
- **Quality Metrics**: Code quality trends and validation scores
- **Optimization Opportunities**: Areas for performance improvement

### 🔍 Advanced Analytics
- **Pattern Recognition**: Automatic identification of successful patterns
- **Predictive Insights**: Performance predictions based on historical data
- **Anomaly Detection**: Unusual performance patterns and potential issues
- **Correlation Analysis**: Relationships between different metrics
- **Recommendation Engine**: Actionable insights for system optimization

## System Requirements

### Dependencies
- **Python 3.8+**: Required for dashboard server
- **Flask**: Web framework for dashboard interface
- **Flask-CORS**: Cross-origin resource sharing
- **Standard libraries**: `json`, `statistics`, `threading`, `pathlib`

### Resource Requirements
- **Minimum**: 2GB RAM, 1 CPU core
- **Recommended**: 4GB+ RAM, 2+ CPU cores
- **Storage**: 100MB+ for pattern data
- **Network**: Optional, for external access and team sharing

## Dashboard Interface

### Main Navigation
```
🏠 Overview    → System health and key metrics
📊 Analytics  → Detailed performance analytics
🎯 Skills      → Skill effectiveness analysis
🤖 Agents      → Agent performance comparison
📚 Learning    → Learning progress and patterns
🔧 System      → Resource usage and health
⚙️  Settings   → Configuration and preferences
```

### Key Dashboard Sections

#### Overview Panel
- **System Status**: Overall health and operational status
- **Active Metrics**: Current performance indicators
- **Quick Stats**: Success rates, quality scores, task counts
- **Recent Activity**: Latest task executions and outcomes
- **Alerts & Issues**: System notifications and warnings

#### Analytics Panel
- **Performance Trends**: Time-based performance analysis
- **Quality Metrics**: Code quality over time
- **Success Rates**: Task completion and success patterns
- **Learning Curves**: System improvement trajectories
- **Comparative Analysis**: Side-by-side performance comparisons

#### Skills Analysis
- **Skill Rankings**: Performance ranking of all skills
- **Usage Patterns**: How often and when skills are used
- **Effectiveness Metrics**: Success rates by skill type
- **Optimization Suggestions**: Areas for skill improvement
- **Skill Dependencies**: Relationships between skills

#### Agent Performance
- **Agent Comparison**: Performance across different agents
- **Specialization Analysis**: Which agents excel at specific tasks
- **Efficiency Metrics**: Time and resource usage by agent
- **Quality Scores**: Output quality by agent type
- **Delegation Success**: Rate of successful task delegation

#### Learning Progress
- **Pattern Recognition**: Discovered learning patterns
- **Knowledge Base**: Growing pattern database
- **Improvement Metrics**: Quantified learning progress
- **Adaptation Rate**: How quickly the system adapts
- **Cross-Project Learning**: Knowledge transfer between projects

## API Endpoints

The dashboard provides REST API endpoints for data access:

```bash
# Get overview data
GET /api/overview

# Get learning analytics
GET /api/analytics

# Get skill performance
GET /api/skills

# Get agent performance
GET /api/agents

# Get system health
GET /api/health

# Get historical data
GET /api/history?period=7d

# Get performance insights
GET /api/insights
```

## Configuration

### Environment Variables
```bash
# Dashboard configuration
DASHBOARD_HOST=127.0.0.1          # Default bind address
DASHBOARD_PORT=5000               # Default port
DASHBOARD_DEBUG=false             # Debug mode
DASHBOARD_CACHE_TTL=60            # Cache TTL in seconds
DASHBOARD_REFRESH_RATE=30         # Auto-refresh rate

# Data directory
PATTERNS_DIR=.claude-patterns    # Pattern data directory
```

### Configuration File
```json
{
  "dashboard": {
    "host": "127.0.0.1",
    "port": 5000,
    "debug": false,
    "cache_ttl": 60,
    "refresh_rate": 30
  },
  "data": {
    "patterns_dir": ".claude-patterns",
    "retention_days": 30,
    "auto_cleanup": true
  },
  "features": {
    "real_time_updates": true,
    "export_reports": true,
    "email_alerts": false,
    "team_sharing": true
  }
}
```

## Security Considerations

### Local Access Only (Default)
- Binds to localhost (127.0.0.1) for security
- Accessible only from the machine where it's running
- Recommended for most use cases

### Network Access (Use with Caution)
```bash
# Enable external access (trusted networks only)
/monitor:dashboard --host 0.0.0.0

# Add firewall rules for security
sudo ufw allow 5000  # Linux
# Configure firewall rules appropriately
```

### Data Privacy
- All data processing happens locally
- No external data transmission
- Pattern data stored locally
- User controls data retention

## Integration with Other Commands

### Pre-Dashboard Analysis
```bash
# Generate comprehensive data before dashboard
/analyze:project
/learn:analytics
/analyze:quality

# Then launch dashboard
/monitor:dashboard
```

### Post-Dashboard Actions
```bash
# Generate reports based on dashboard insights
/workspace:reports
/learn:performance

# Implement optimizations
/workspace:improve
```

### Continuous Monitoring
```bash
# Background monitoring
/monitor:dashboard --background

# Generate periodic reports
/workspace:organize
```

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Use different port
/monitor:dashboard --port 8080

# Kill existing process
lsof -ti:5000 | xargs kill -9
```

**No Data Available**
```bash
# Initialize pattern learning
/learn:init

# Generate some activity
/analyze:project

# Check data directory
ls -la .claude-patterns/
```

**Dashboard Won't Load**
```bash
# Check Python dependencies
pip install flask flask-cors

# Verify dashboard script (auto-detects plugin path)
python <plugin_path>/lib/dashboard.py --test

# Check system resources
free -h  # Memory
df -h    # Disk space
```

**Performance Issues**
```bash
# Increase cache TTL
/monitor:dashboard --cache-ttl 120

# Reduce refresh rate
/monitor:dashboard --refresh-rate 60

# Clear old data
/monitor:dashboard --cleanup-days 7
```

### Debug Mode
```bash
# Launch with debug output
/monitor:dashboard --debug

# Check log files
tail -f .claude/logs/dashboard.log

# Validate installation (auto-detects plugin path)
python <plugin_path>/lib/dashboard.py --validate
```

## Best Practices

### Production Use
- Use external access only on trusted networks
- Set up appropriate firewall rules
- Monitor resource usage
- Regular data backups
- Implement access controls for team sharing

### Performance Optimization
- Regular data cleanup and archiving
- Optimize cache settings based on usage
- Monitor system resources
- Use appropriate refresh intervals
- Consider resource limits for long-term operation

### Data Management
- Regular backup of pattern data
- Archive old data to maintain performance
- Monitor storage usage
- Implement data retention policies
- Export important insights regularly

## Performance Metrics

### Expected Resource Usage
- **CPU**: 2-5% during normal operation
- **Memory**: 50-200MB depending on data size
- **Storage**: Grows with pattern data (manageable)
- **Network**: Minimal (local access)

### Scalability
- **Data Points**: Handles 10,000+ pattern entries efficiently
- **Concurrent Users**: Supports 5-10 simultaneous users
- **Historical Data**: Optimal performance with 30-day retention
- **Response Times**: <100ms for most API endpoints

## Examples

### Basic Monitoring
```bash
# Launch dashboard for local development
/monitor:dashboard

# Monitor specific project
cd /path/to/project
/monitor:dashboard --data-dir .claude-patterns
```

### Team Monitoring
```bash
# Share dashboard with team
/monitor:dashboard --host 0.0.0.0 --port 8080

# Team members access at:
# http://your-ip:8080
```

### Production Monitoring
```bash
# Background monitoring with alerts
/monitor:dashboard --background --email-alerts

# Generate daily reports
/monitor:dashboard --report-only --email-reports
```

---

**Version**: 1.0.2
**Integration**: Uses dashboard.py directly from lib/ directory (no delegation)
**Dependencies**: Flask, Flask-CORS, Python 3.8+
**Platform**: Cross-platform (Windows, Linux, Mac)
**Learning**: Integrates with learning-engine for pattern analysis
**Fix**: Enhanced smart browser opening with lock mechanism and existing dashboard detection (v1.0.2)
**Previous**: Removed agent delegation to prevent duplicate browser launches (v1.0.1)