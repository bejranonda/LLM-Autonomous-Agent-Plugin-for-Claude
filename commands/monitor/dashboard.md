---
name: monitor:dashboard
description: Launch real-time monitoring dashboard for autonomous agent system metrics and learning analytics
delegates-to: orchestrator
---

# Monitor Dashboard Command

## Command: `/monitor:dashboard`

**Quick launcher** that delegates to the orchestrator to start a real-time monitoring dashboard in the background for autonomous agent system metrics and learning analytics.

## How It Works

1. **Quick Launch**: Command completes in 2-3 seconds with status report
2. **Delegate to Orchestrator**: Orchestrator manages background dashboard process
3. **Background Server**: Flask web server runs independently in background
4. **Data Collection**: Dashboard aggregates data from pattern learning files
5. **Real-time Updates**: Provides API endpoints for live data access
6. **Web Interface**: Browser-based dashboard with interactive charts
7. **System Monitoring**: Tracks agent performance, skill effectiveness, and learning trends

**IMPORTANT**: This command MUST delegate to the orchestrator agent for background process management. The command itself should return immediately after launching the background process.

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

**Expected Performance**: Command completes in 2-3 seconds with dashboard running in background.

## Command Behavior and Delegation

### Orchestrator Integration

**CRITICAL**: This command MUST delegate to the orchestrator agent. The orchestrator will:

1. **Process Management**: Start dashboard.py as background process
2. **Port Detection**: Find available port (5000, 5001, etc.)
3. **Status Tracking**: Monitor dashboard process health
4. **Clean Shutdown**: Handle process termination gracefully
5. **Error Handling**: Manage startup failures and conflicts

### Expected Command Output

The orchestrator MUST present a concise status report immediately:

```
🚀 Autonomous Agent Dashboard
════════════════════════════════════════════════════════

Status: ✅ Running in background
URL:   http://127.0.0.1:5001
Port:  5001 (5000 was in use)
PID:   12345
Data:  .claude-patterns/ (2.3MB)

📊 Dashboard Features:
• Real-time learning analytics
• Agent performance metrics
• Quality trend visualization
• Interactive system monitoring

💡 Browser opening automatically...
⚠️  Press Ctrl+C in terminal to stop dashboard
🔧 Use /monitor:dashboard --status to check status
════════════════════════════════════════════════════════
⏱️  Started in 2.1 seconds
```

### Error Handling

If dashboard fails to start, orchestrator MUST report:

```
❌ Dashboard Launch Failed
════════════════════════════════════════════════════════

Error: Port 5000-5005 all in use
Solution: /monitor:dashboard --port 8080

or

Error: Missing Flask dependencies
Solution: pip install flask flask-cors

════════════════════════════════════════════════════════
🔧 Try: /monitor:dashboard --debug for troubleshooting
```

### Process Management Commands

```bash
# Check dashboard status
/monitor:dashboard --status
→ ✅ Dashboard running on http://127.0.0.1:5001 (PID: 12345)

# Stop dashboard
/monitor:dashboard --stop
→ ⏹ Dashboard stopped (PID: 12345)

# Restart dashboard
/monitor:dashboard --restart
→ 🔄 Dashboard restarted on http://127.0.0.1:5002
```

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

# Verify dashboard script
python lib/dashboard.py --test

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

# Validate installation
python lib/dashboard.py --validate
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

**Version**: 1.0.0
**Integration**: Uses dashboard.py from lib/ directory
**Dependencies**: Flask, Flask-CORS, Python 3.8+
**Platform**: Cross-platform (Windows, Linux, Mac)
**Learning**: Integrates with learning-engine for pattern analysis