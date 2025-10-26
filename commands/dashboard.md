---
name: monitor:dashboard
description: Launch improved real-time web dashboard with automatic port detection and robust error handling

delegates-to: orchestrator

# Real-Time Monitoring Dashboard

Launch an interactive web-based dashboard with automatic port detection, server validation, and robust error handling to prevent connectivity issues. The dashboard provides comprehensive monitoring of the autonomous agent's learning progress, quality trends, and performance metrics.

## Command Implementation

**For the Orchestrator**: When this command is invoked, execute the robust dashboard launcher with comprehensive error handling and automatic learning integration:

```bash
# Execute robust launcher with auto-restart and monitoring
python lib/dashboard_launcher.py --host 127.0.0.1 --port 5000

# After successful dashboard startup, automatically trigger learning engine
# to record the dashboard startup pattern and performance metrics
```

**Critical Instructions for Orchestrator**:
1. **Execute the robust launcher** (not the basic dashboard.py)
2. **Validate successful startup** before reporting success
3. **Trigger learning-engine automatically** after dashboard is running
4. **Record performance metrics** for the dashboard startup task
5. **Monitor for any issues** and handle them appropriately

**Key Features**:
- ✅ **Automatic Port Detection**: Finds available ports if 5000 is occupied
- ✅ **Health Monitoring**: Continuously checks dashboard responsiveness
- ✅ **Auto-Restart**: Restarts dashboard if it crashes (max 5 attempts)
- ✅ **Startup Validation**: Confirms API is responding before reporting success
- ✅ **Robust Error Handling**: Clear error messages and recovery suggestions
- ✅ **Background Monitoring**: Keeps dashboard running reliably
- ✅ **Cross-Platform**: Works on Windows, Linux, and macOS
- ✅ **Automatic Learning**: Integrates with learning system for continuous improvement

**Execution Flow**:
1. Execute robust dashboard launcher
2. Wait for successful startup and validation
3. Confirm dashboard API endpoints are responding
4. Open browser automatically on success
5. **Automatically trigger learning-engine** to record the pattern
6. Begin background monitoring for continuous reliability
7. **Continue with standard orchestrator learning workflow**

## Usage

```bash
/monitor:dashboard [OPTIONS]
```

**Examples**:
```bash
/monitor:dashboard                          # Launch with automatic port detection
/monitor:dashboard --port 8080              # Launch on preferred port (finds alternative if occupied)
/monitor:dashboard --host 0.0.0.0           # Allow external access
/monitor:dashboard --patterns-dir ./patterns # Custom pattern directory
/monitor:dashboard --no-browser             # Don't open browser automatically
```

## Key Improvements

### 1. Automatic Port Detection
- Detects if port 5000 is in use
- Automatically finds available alternative ports (5001-5010)
- Falls back to random ports in 8000-9000 range if needed
- No more "Address already in use" errors

### 2. Server Startup Validation
- Validates that the server is responding before declaring success
- Checks API endpoint availability within 5 seconds
- Provides clear feedback about server status
- Automatic retry mechanism for startup issues

### 3. Enhanced Error Handling
- Graceful handling of missing dependencies
- Clear error messages with actionable suggestions
- Automatic patterns directory creation
- Proper cleanup on server shutdown

### 4. Browser Integration
- Automatic browser opening after successful startup
- Fallback instructions if auto-open fails
- Option to disable auto-opening with --no-browser

### 5. Windows Compatibility
- Removed emoji characters that cause encoding issues
- Full Windows support with proper path handling
- Cross-platform port detection

## Troubleshooting

### Issue: Dashboard not reachable at localhost:5000

**Previous Problem**:
```
Connection refused at http://localhost:5000/
```

**New Solution**: The dashboard automatically:
1. Detects if port 5000 is occupied
2. Finds an available port (e.g., 5001, 5002, etc.)
3. Validates server startup
4. Opens the correct URL automatically

**Output Example**:
```
Port 5000 is already in use.
Using alternative port: 5001
Starting Autonomous Agent Dashboard...
Dashboard URL: http://127.0.0.1:5001
Dashboard is running at: http://127.0.0.1:5001
Opening browser automatically...
```

### Issue: Server fails to start silently

**New Solution**:
- Server validation checks if Flask is responding
- Clear error messages if startup fails
- Suggestions for alternative ports

### Issue: Browser doesn't open

**New Solution**:
- Automatic retry with delay
- Manual URL provided if auto-open fails
- --no-browser option for headless environments

## Features

### 1. Overview Metrics (Real-time)

**Key Performance Indicators**:
- **Total Patterns**: Number of learned patterns
- **Active Skills**: Skills currently in use
- **Active Agents**: Agents available
- **Average Quality Score**: Overall quality (0-100)
- **Learning Velocity**: Accelerating/Stable/Declining

**Auto-refresh**: Every 30 seconds

### 2. Quality Score Trends

**Visualization**: Line chart showing quality scores over time

**Features**:
- Daily average quality scores
- Min/max ranges
- Trend analysis (last 30 days)
- Overall average calculation

**Use Cases**:
- Track improvement over time
- Identify quality degradation
- Validate learning effectiveness

### 3. Task Distribution

**Visualization**: Doughnut chart showing task type distribution

**Metrics**:
- Task type breakdown (refactoring, bug-fix, feature, etc.)
- Count per task type
- Success rate per type

**Insights**:
- Most common task types
- Task type performance
- Workload distribution

### 4. Top Performing Skills

**Table View** with sortable columns:
- **Skill Name**: Identifier
- **Success Rate**: Percentage of successful applications
- **Usage Count**: How many times used
- **Avg Quality Impact**: Quality improvement contribution

**Sorting**: By success rate (descending)

**Use Cases**:
- Identify most effective skills
- Optimize skill selection
- Discover underutilized skills

### 5. Top Performing Agents

**Table View** with performance metrics:
- **Agent Name**: Identifier
- **Success Rate**: Task completion percentage
- **Usage Count**: Invocation frequency
- **Avg Duration**: Execution time in seconds
- **Reliability**: Consistency score (0-100%)

**Sorting**: By reliability (descending)

**Use Cases**:
- Identify reliable agents
- Optimize agent delegation
- Detect performance issues

### 6. Recent Activity

**Real-time Activity Feed** (last 20 tasks):
- **Timestamp**: When task executed
- **Task Type**: Category
- **Quality Score**: Achieved score
- **Status**: Success/Failed badge
- **Skills Used**: Top 3 skills applied

**Auto-refresh**: Every 30 seconds

**Use Cases**:
- Monitor current system activity
- Track recent performance
- Quick issue detection

### 7. System Health

**Health Monitoring** with status indicator:
- **Status**: Excellent/Warning/Degraded (pulsing indicator)
- **Error Rate**: Percentage of failed tasks (last 50)
- **Avg Quality**: Average quality score (last 50)
- **Patterns Stored**: Total pattern count
- **Storage Size**: Pattern database size (KB)

**Health Thresholds**:
- **Excellent**: Error rate < 10%, Quality > 70
- **Warning**: Error rate < 20%, Quality > 60
- **Degraded**: Error rate ≥ 20% or Quality ≤ 60

## How It Works

### 1. Data Collection

Dashboard reads from pattern storage files:

```
.claude-patterns/
├── enhanced_patterns.json     # Task execution patterns
├── skill_metrics.json         # Skill performance data
└── agent_metrics.json         # Agent performance data
```

**Caching**: 60-second cache to reduce file I/O

### 2. Flask Web Server

**Backend**:
- Flask application serving dashboard UI
- RESTful API endpoints for data
- CORS enabled for API access

**Frontend**:
- Single-page application (SPA)
- Chart.js for visualizations
- Auto-refresh every 30 seconds

### 3. API Endpoints

```
GET /                              # Dashboard UI
GET /api/overview                  # Overview metrics
GET /api/quality-trends?days=30    # Quality trends
GET /api/skills?top_k=10           # Top skills
GET /api/agents?top_k=10           # Top agents
GET /api/task-distribution         # Task breakdown
GET /api/recent-activity?limit=20  # Recent tasks
GET /api/system-health             # Health status
```

## Dashboard UI

### Layout

```
┌─────────────────────────────────────────────────────┐
│      🤖 Autonomous Agent Dashboard                  │
├─────────────────────────────────────────────────────┤
│  [Total Patterns] [Active Skills] [Active Agents]   │
│  [Avg Quality]    [Learning Velocity]               │
├─────────────────────────────────────────────────────┤
│  Quality Score Trends (Last 30 Days)                │
│  [Line Chart with trend line]                       │
├──────────────────────────┬──────────────────────────┤
│  Task Distribution       │  System Health           │
│  [Doughnut Chart]        │  [Health Metrics]        │
├──────────────────────────┴──────────────────────────┤
│  Top Performing Skills                              │
│  [Table with success rates, usage counts]           │
├─────────────────────────────────────────────────────┤
│  Top Performing Agents                              │
│  [Table with reliability, duration metrics]         │
├─────────────────────────────────────────────────────┤
│  Recent Activity                                    │
│  [Activity feed with latest 20 tasks]               │
└─────────────────────────────────────────────────────┘
```

### Color Scheme

**Primary Colors**:
- Purple gradient background: #667eea → #764ba2
- Success green: #28a745
- Warning yellow: #ffc107
- Danger red: #dc3545
- Info blue: #17a2b8

**Interactive Elements**:
- Hover effects on cards (lift animation)
- Pulsing health indicator
- Smooth chart transitions

## Usage Scenarios

### Scenario 1: Daily Monitoring

```bash
# Morning routine: Check system health
/dashboard

# View dashboard in browser
# http://localhost:5000

# Check:
# - Learning velocity (should be accelerating)
# - Error rate (should be < 10%)
# - Recent activity (any failures?)
```

### Scenario 2: Performance Analysis

```bash
# Launch dashboard
/dashboard --port 8080

# Analysis tasks:
# 1. Review quality trends - Are we improving?
# 2. Check top skills - Which are most effective?
# 3. Review task distribution - Any imbalances?
# 4. Identify underperforming agents
```

### Scenario 3: Team Presentation

```bash
# Allow team access
/dashboard --host 0.0.0.0 --port 8080

# Share URL: http://<your-ip>:8080
# Present live metrics to team
# Demonstrate learning progress
```

### Scenario 4: Continuous Monitoring

```bash
# Run dashboard in background
/dashboard &

# Keep browser tab open
# Auto-refresh every 30s
# Monitor system health in real-time
```

## Advanced Configuration

### Custom Port

```bash
# Avoid conflicts with other services
/dashboard --port 3000
/dashboard --port 8888
```

### External Access

```bash
# Allow access from other machines on network
/dashboard --host 0.0.0.0 --port 5000

# Access from other machines:
# http://<your-machine-ip>:5000
```

### Custom Pattern Directory

```bash
# Monitor different project
/dashboard --patterns-dir /path/to/project/.claude-patterns
```

## API Usage (Programmatic Access)

### Python Example

```python
import requests

# Get overview metrics
response = requests.get('http://localhost:5000/api/overview')
metrics = response.json()

print(f"Total Patterns: {metrics['total_patterns']}")
print(f"Avg Quality: {metrics['average_quality_score']}")
print(f"Learning Velocity: {metrics['learning_velocity']}")
```

### JavaScript Example

```javascript
// Fetch quality trends
fetch('http://localhost:5000/api/quality-trends?days=30')
  .then(response => response.json())
  .then(data => {
    console.log('Overall Average:', data.overall_average);
    console.log('Trend Data:', data.trend_data);
  });
```

### cURL Example

```bash
# Get system health
curl http://localhost:5000/api/system-health

# Get top skills
curl http://localhost:5000/api/skills?top_k=5

# Get recent activity
curl http://localhost:5000/api/recent-activity?limit=10
```

## Performance Metrics

### Resource Usage

| Component | CPU | Memory | Disk I/O |
|
---


--------|-----|--------|----------|
| Flask Server | <1% | ~50MB | Minimal |
| Data Collection | <1% | ~20MB | 1-2 reads/30s |
| Web UI | <1% | ~30MB | None (cached) |

**Total**: <3% CPU, ~100MB RAM

### Response Times

| Endpoint | Avg Response | Max Response |
|----------|-------------|--------------|
| /api/overview | 10-20ms | 50ms |
| /api/quality-trends | 20-50ms | 100ms |
| /api/skills | 15-30ms | 75ms |
| /api/agents | 15-30ms | 75ms |
| /api/recent-activity | 10-20ms | 50ms |

**Note**: First request may be slower (cache miss)

## Troubleshooting

### Issue: Port Already in Use

```
Error: Address already in use
```

**Solution**:
```bash
# Use different port
/dashboard --port 8080

# Or kill existing process
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows (find PID)
taskkill /PID <pid> /F         # Windows (kill process)
```

### Issue: No Data Displayed

```
Dashboard shows zeros or "No data"
```

**Solution**:
```bash
# Check pattern directory exists
ls -la .claude-patterns/

# Initialize pattern learning if needed
/learn-patterns

# Run some tasks to generate data
/auto-analyze
```

### Issue: Slow Performance

```
Dashboard is slow to load or refresh
```

**Solution**:
```bash
# Reduce cache TTL (edit lib/dashboard.py)
# Change: self.cache_ttl = 60
# To:     self.cache_ttl = 120

# Or reduce auto-refresh interval (edit dashboard HTML)
# Change: setInterval(fetchDashboardData, 30000)
# To:     setInterval(fetchDashboardData, 60000)
```

### Issue: Can't Access from Other Machines

```
Connection refused from remote machine
```

**Solution**:
```bash
# Bind to all interfaces
/dashboard --host 0.0.0.0 --port 5000

# Check firewall allows port 5000
# macOS: System Preferences → Security → Firewall
# Linux: sudo ufw allow 5000
# Windows: Windows Firewall → Advanced Settings → Inbound Rules
```

## Security Considerations

### Local Use Only (Default)

```bash
# Binds to localhost only
/dashboard

# Only accessible from same machine
# URL: http://127.0.0.1:5000
```

**Recommendation**: Use default for security

### Network Access (Use with Caution)

```bash
# Binds to all interfaces
/dashboard --host 0.0.0.0

# Accessible from any machine on network
# URL: http://<your-ip>:5000
```

**Security Measures**:
1. Use only on trusted networks
2. Consider adding authentication (edit `lib/dashboard.py`)
3. Use firewall rules to restrict access
4. Use HTTPS in production (add SSL certificate)

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Dashboard Report
on:
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  dashboard-snapshot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Get Dashboard Metrics
        run: |
          curl http://localhost:5000/api/overview > metrics.json
          curl http://localhost:5000/api/system-health > health.json
      - name: Upload Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dashboard-metrics
          path: |
            metrics.json
            health.json
```

### Monitoring Alerts

```python
# alert_monitor.py
import requests
import time

while True:
    health = requests.get('http://localhost:5000/api/system-health').json()

    if health['status'] == 'degraded':
        # Send alert (email, Slack, etc.)
        print(f"ALERT: System health degraded!")
        print(f"Error rate: {health['error_rate']}%")
        print(f"Avg quality: {health['avg_quality']}")

    time.sleep(300)  # Check every 5 minutes
```

## Best Practices

1. **Regular Monitoring**: Check dashboard daily during development
2. **Track Trends**: Monitor quality trends weekly
3. **Identify Issues Early**: Set up alerts for degraded health
4. **Share with Team**: Use external access for team visibility
5. **Optimize Performance**: Review top skills/agents monthly
6. **Clean Data**: Archive old patterns if storage grows too large

## Future Enhancements

**Planned Features** (v1.1+):
- WebSocket support for instant updates (no polling)
- User authentication and multi-user support
- Custom date ranges for trend analysis
- Export reports to PDF/Excel
- Alerting system (email, Slack integration)
- Dark mode toggle
- Mobile-responsive design improvements
- Comparison view (compare projects or time periods)

---

This dashboard provides comprehensive real-time monitoring of your autonomous agent's learning and performance, helping you track improvements and identify issues quickly.
