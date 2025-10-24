# Model Performance Dashboard

## Overview

The enhanced Autonomous Agent Dashboard now includes comprehensive model performance tracking with interactive charts showing quality scores across different AI models and temporal performance trends.

## New Features

### 1. Model Quality Scores Bar Chart

**Location**: Top row of dashboard, second chart

**Features**:
- **Multi-model comparison**: Displays quality scores for Claude, OpenAI, GLM, and Gemini
- **Dual metrics**: Shows both quality scores and success rates
- **Color-coded models**: Each model has a distinct color for easy identification
- **Interactive tooltips**: Hover to see contribution percentages and detailed metrics
- **Real-time updates**: Charts refresh every 30 seconds

**Chart Details**:
- **Type**: Bar chart with grouped bars
- **X-axis**: Model names (Claude, OpenAI, GLM, Gemini)
- **Y-axis**: Score (0-100 scale)
- **Datasets**: Quality Score (solid) and Success Rate (transparent overlay)

### 2. Temporal Performance Line Chart

**Location**: Top row of dashboard, third chart

**Features**:
- **Dual-axis visualization**: Performance score and contribution to project
- **Time-based tracking**: Shows performance trends over selected period
- **Interactive period selector**: Choose between 7, 30, or 90 days
- **Dynamic calculation**: Contribution scores calculated based on performance
- **Model-specific**: Currently tracks Claude (configurable to other models)

**Chart Details**:
- **Type**: Dual-axis line chart
- **Left Y-axis**: Performance Score (0-100)
- **Right Y-axis**: Contribution Score (0-30)
- **X-axis**: Time timeline
- **Datasets**: Performance Score (blue) and Contribution (green)

### 3. Model Performance Data Storage

**File**: `.claude-patterns/model_performance.json`

**Data Structure**:
```json
{
  "Claude": {
    "recent_scores": [
      {
        "score": 92.5,
        "timestamp": "2025-10-24T14:56:14.137611",
        "task_type": "dashboard_enhancement",
        "contribution": 28.3
      }
    ],
    "total_tasks": 113,
    "success_rate": 0.96,
    "contribution_to_project": 25.2,
    "first_seen": "2025-10-24T14:55:09.490234",
    "last_updated": "2025-10-24T14:56:14.137611"
  }
}
```

## Usage

### Starting the Dashboard

```bash
# Basic usage (default port 5000)
python lib/dashboard.py

# Custom port and pattern directory
python lib/dashboard.py --port 8080 --patterns-dir .claude-patterns

# Allow external access
python lib/dashboard.py --host 0.0.0.0 --port 8080
```

### Accessing the Dashboard

Open your web browser and navigate to:
- **Local**: http://localhost:8080 (or your specified port)
- **Network**: http://your-ip:8080 (if using --host 0.0.0.0)

### Managing Model Performance Data

#### Adding Performance Scores

```bash
# Add a new performance score
python lib/model_performance.py --dir .claude-patterns add \
  --model Claude \
  --score 92.5 \
  --task-type dashboard_enhancement \
  --contribution 28.3
```

**Parameters**:
- `--model`: Model name (Claude, OpenAI, GLM, Gemini)
- `--score`: Performance score (0-100)
- `--task-type`: Type of task performed
- `--contribution`: Contribution to project (0-100)

#### Generating Sample Data

```bash
# Generate 30 days of sample historical data
python lib/model_performance.py --dir .claude-patterns generate-sample --days 30
```

#### Viewing Performance Summaries

```bash
# View all models summary
python lib/model_performance.py --dir .claude-patterns summary

# View specific model summary
python lib/model_performance.py --dir .claude-patterns model-summary --model Claude
```

#### Clearing Data

```bash
# Clear all model performance data
python lib/model_performance.py --dir .claude-patterns clear
```

## API Endpoints

### Model Quality Scores

**Endpoint**: `GET /api/model-quality-scores`

**Response**:
```json
{
  "models": ["Claude", "OpenAI", "GLM", "Gemini"],
  "quality_scores": [85.7, 83.2, 77.4, 82.1],
  "success_rates": [96.4, 91.2, 70.1, 88.3],
  "contributions": [25.2, 24.0, 23.1, 24.6]
}
```

### Temporal Performance

**Endpoint**: `GET /api/temporal-performance?days=30`

**Response**:
```json
{
  "active_model": "Claude",
  "average_performance": 88.4,
  "total_contribution": 265.2,
  "trend": "improving",
  "temporal_data": [
    {
      "timestamp": "2025-10-24T14:56:14.137611",
      "display_time": "10/24",
      "score": 92.5,
      "contribution": 28.3,
      "model": "Claude"
    }
  ],
  "days": 30
}
```

## Performance Metrics

### Quality Score Calculation

Quality scores are measured on a 0-100 scale:
- **90-100**: Excellent performance
- **80-89**: Good performance
- **70-79**: Acceptable performance
- **Below 70**: Needs improvement

### Success Rate

Percentage of tasks with quality scores ≥ 70:
- **Above 90%**: Excellent reliability
- **80-90%**: Good reliability
- **70-80%**: Acceptable reliability
- **Below 70%**: Reliability concerns

### Contribution to Project

Calculated as a weighted average of:
- Direct task performance (30% weight)
- Task complexity and impact (40% weight)
- Consistency over time (30% weight)

## Interactive Features

### Chart Interactions

1. **Hover Effects**:
   - Bar charts show detailed metrics on hover
   - Line charts show exact values at specific points
   - Tooltips display additional context

2. **Period Selection**:
   - Quality trends: 24h, 7d, 30d, 90d, 1y, all time
   - Temporal performance: 7d, 30d, 90d

3. **Auto-refresh**:
   - Dashboard data refreshes every 30 seconds
   - Charts update smoothly without flickering

### Color Scheme

- **Claude**: Purple (#667eea)
- **OpenAI**: Green (#10b981)
- **GLM**: Orange (#f59e0b)
- **Gemini**: Red (#ef4444)

## Integration with Existing Features

The model performance charts integrate seamlessly with existing dashboard features:

1. **Overview Metrics**: Includes model performance averages
2. **Quality Trends**: Shows historical quality patterns
3. **System Health**: Monitors overall system performance
4. **Real-time Updates**: All charts update simultaneously

## Troubleshooting

### Common Issues

1. **No Model Data Displayed**:
   ```bash
   # Generate sample data
   python lib/model_performance.py --dir .claude-patterns generate-sample --days 30
   ```

2. **Chart Loading Errors**:
   - Check browser console for JavaScript errors
   - Verify Chart.js library is loading correctly
   - Ensure API endpoints are accessible

3. **Data Not Updating**:
   - Check file permissions on `.claude-patterns/` directory
   - Verify model_performance.json is writable
   - Check server logs for errors

### Performance Optimization

1. **Data Retention**: Only last 100 scores per model are stored
2. **Caching**: 60-second cache for API responses
3. **Lazy Loading**: Charts render only when visible

## Future Enhancements

**Planned Features** (v2.1+):
- Multi-model temporal comparison
- Custom model addition support
- Performance prediction algorithms
- Export functionality (CSV, PDF)
- Alert system for performance degradation
- Integration with external monitoring tools

## Security Considerations

1. **Local Use Only**: Default configuration binds to localhost
2. **Data Privacy**: All performance data stored locally
3. **Access Control**: Use firewall rules for network access
4. **Data Integrity**: File locking prevents concurrent access issues

---

This enhanced dashboard provides comprehensive insights into model performance, helping you track improvement over time and make data-driven decisions about model selection and optimization.