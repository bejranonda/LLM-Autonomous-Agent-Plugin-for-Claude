# Unified Dashboard User Guide

## Overview

The AutonomousAgent plugin now features a **single, comprehensive unified dashboard** that consolidates all dashboard functionality into one powerful interface. This guide covers everything you need to know about the new unified dashboard system.

## 🎯 What's New

### Before vs After

**Before (5 Separate Dashboards):**
- `/monitor:dashboard` → Main metrics
- Token dashboard (separate URL) → Cost optimization
- KPI dashboard (separate file) → Executive metrics
- System health (separate tool) → Health monitoring
- Multiple URLs and interfaces

**After (1 Unified Dashboard):**
- `/monitor:dashboard` → **Complete solution**
- **5 integrated tabs** with all functionality
- **Single URL**: `http://localhost:5000`
- **Unified data** and **consistent interface**

## 🚀 Quick Start

### Launch the Unified Dashboard

```bash
# Same command you already use
/monitor:dashboard
```

The dashboard will open automatically in your browser at `http://localhost:5000`

### Navigate Between Sections

Use the tabbed navigation at the top:

- **🏠 Overview** - System health and key metrics
- **📊 Analytics** - Skills and agents performance
- **💰 Token Optimization** - Cost savings and usage
- **📈 KPI & Reports** - Executive metrics and trends
- **🔧 System Health** - Resource monitoring and validation

## 📊 Dashboard Sections

### Overview Tab
- **Current Model Status**: Active AI model information
- **Quality Trends**: Historical quality scores with filtering
- **Task Distribution**: Task type breakdown
- **System Health**: Quick system status indicators
- **Recent Activity**: Latest dashboard interactions

### Analytics Tab
- **Top Performing Skills**: Success rates and usage statistics
- **Top Performing Agents**: Performance metrics and reliability
- **Task Distribution**: Visual breakdown of task types
- **Performance Insights**: Detailed analytics

### Token Optimization Tab
- **Token Savings**: Daily, weekly, monthly savings
- **Compression Ratios**: Token compression effectiveness
- **Cost Savings**: Monetary value of optimizations
- **Cache Hit Rates**: Performance optimization metrics
- **Usage Trends**: 30-day historical analysis

### KPI & Reports Tab
- **Performance Score**: Overall KPI scoring
- **Business Impact**: Cost reduction and time savings
- **Trend Analysis**: Historical KPI trends
- **Performance Radar**: Multi-dimensional performance view
- **Executive Summary**: High-level metrics overview

### System Health Tab
- **Resource Monitoring**: CPU, memory, disk usage
- **Data Integrity**: Consistency scoring and validation
- **System Alerts**: Real-time notifications
- **Health Checks**: Manual and automatic validation

## 🎨 Features & Capabilities

### Real-Time Updates
- **Auto-refresh**: Data updates every 30 seconds
- **Smart Caching**: Optimized performance with data caching
- **Tab-Specific Updates**: Only active tab data refreshes
- **Visibility Detection**: Pauses updates when tab is hidden

### Export Functionality
Each section provides export options:

**Export Formats:**
- **JSON**: Structured data for integration
- **CSV**: Spreadsheet-compatible format
- **PDF**: Printable reports (KPI section)

**How to Export:**
1. Navigate to desired tab
2. Click export buttons in section header
3. Choose format and download

### Mobile Responsive Design
- **Touch-Friendly**: Optimized for mobile devices
- **Responsive Layout**: Adapts to screen size
- **Mobile Navigation**: Wrapped tabs for small screens
- **High Contrast**: Accessibility support

### Performance Optimizations
- **Data Caching**: 30-second cache TTL
- **Chart Management**: Efficient chart creation and updates
- **Performance Monitoring**: Load time tracking
- **Memory Management**: Optimized resource usage

## 🔧 Advanced Features

### Data Migration
If you're upgrading from previous dashboard versions:

1. **Automatic Migration**: Data is migrated automatically
2. **Backup Creation**: Safety backup of existing data
3. **Compatibility Shims**: Legacy tools continue working
4. **Migration Reports**: Detailed migration logs

### Backward Compatibility
- **Legacy APIs**: Compatibility shims for old integrations
- **Gradual Transition**: No immediate changes required
- **Deprecation Warnings**: Clear migration guidance
- **Fallback Support**: Graceful degradation

### Customization
- **Period Selection**: Filter data by time periods
- **Chart Types**: Multiple visualization options
- **Metric Configuration**: Customizable KPIs
- **Alert Settings**: Notification preferences

## 📈 Performance Metrics

### System Performance
- **Initialization**: < 2 seconds
- **Data Retrieval**: < 0.1 seconds average
- **Chart Rendering**: Optimized for performance
- **Memory Usage**: Efficient resource management

### Data Processing
- **Cache Hit Rate**: High-performance caching
- **Update Frequency**: 30-second intervals
- **API Response**: Sub-100ms response times
- **Error Rate**: < 1% error handling success

## 🛠️ Troubleshooting

### Common Issues

**Dashboard doesn't load:**
```bash
# Check if port is available
python lib/dashboard.py --status

# Try different port
/monitor:dashboard --port 5001
```

**Data not updating:**
- Check network connection
- Refresh browser cache
- Verify data files in `.claude-patterns/`

**Charts not displaying:**
- Enable JavaScript in browser
- Check browser console for errors
- Verify Chart.js library loading

**Mobile display issues:**
- Refresh browser cache
- Check responsive design
- Test in different browsers

### Getting Help

**For Issues:**
1. Check the migration backup directory
2. Review deprecation warnings
3. Test with different browsers
4. Verify data file permissions

**For Questions:**
- Refer to this documentation
- Check migration reports
- Review test results
- Contact support if needed

## 📚 API Reference

### Unified API Endpoints

```bash
# Token optimization data
GET /api/tokens/overview

# KPI metrics data
GET /api/kpi/overview

# System health data
GET /api/unified/system/health

# Generic section data
GET /api/sections/<section_name>
```

### Data Structure

**Unified Data Format:**
```json
{
  "migration_info": {
    "timestamp": "2025-11-05T...",
    "version": "1.0",
    "source_dashboards": ["token_dashboard", "kpi_dashboard"]
  },
  "sections": {
    "tokens": { "token_usage": {...}, "cost_savings": {...} },
    "kpi": { "performance_kpis": {...}, "business_kpis": {...} },
    "system": { "system_metrics": {...}, "alerts": [...] }
  }
}
```

## 🔄 Migration Guide

### From Legacy Dashboards

**Step 1: Backup Existing Data**
- Automatic backup created during first run
- Located in `.dashboard-migration-backup/`
- Includes all dashboard data files

**Step 2: Verify Migration**
- Check unified dashboard sections
- Verify data completeness
- Test functionality

**Step 3: Update Integrations**
- Update scripts to use unified APIs
- Replace multiple dashboard calls
- Test integrations

**Step 4: Clean Up**
- Remove old dashboard files after confirmation
- Delete backup after 30 days
- Update documentation

### Integration Examples

**Old Approach:**
```bash
# Multiple dashboard calls
python lib/token_dashboard.py
python lib/kpi_dashboard.py
python lib/system_health.py
```

**New Approach:**
```bash
# Single unified dashboard
/monitor:dashboard

# Or API calls
curl http://localhost:5000/api/sections/tokens
curl http://localhost:5000/api/sections/kpi
curl http://localhost:5000/api/sections/system
```

## 📋 Best Practices

### Usage Recommendations
- **Regular Usage**: Keep dashboard open for monitoring
- **Data Export**: Export reports regularly for record-keeping
- **Mobile Access**: Use mobile version for on-the-go monitoring
- **Performance**: Monitor system resources during heavy usage

### Data Management
- **Regular Backups**: Export important data periodically
- **File Organization**: Keep `.claude-patterns/` directory clean
- **Version Control**: Track configuration changes
- **Documentation**: Record customizations

### Performance Tips
- **Browser Caching**: Allow browser caching for faster loads
- **Tab Management**: Close unused tabs to save resources
- **Update Frequency**: Adjust auto-refresh intervals as needed
- **Resource Monitoring**: Watch system memory usage

## 🎉 Conclusion

The unified dashboard provides a **complete, integrated solution** for monitoring your Autonomous Agent system. With real-time updates, comprehensive analytics, and mobile-responsive design, it offers everything you need in one convenient interface.

**Key Benefits:**
- ✅ **Single Interface**: All functionality in one place
- ✅ **Real-Time Updates**: Live data monitoring
- ✅ **Mobile Access**: Works on all devices
- ✅ **Export Capabilities**: Multiple format support
- ✅ **Performance Optimized**: Fast and efficient
- ✅ **Backward Compatible**: Smooth migration path

**Getting Started:**
1. Run `/monitor:dashboard`
2. Explore all 5 integrated sections
3. Customize views to your preferences
4. Export reports as needed
5. Enjoy your unified monitoring experience!

---

**Last Updated**: November 5, 2025
**Version**: 1.0
**Dashboard Version**: v7.5.0+