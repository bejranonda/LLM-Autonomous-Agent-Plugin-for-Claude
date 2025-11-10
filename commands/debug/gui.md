---
name: debug:gui
description: Debug and validate GUI systems (dashboard, CLI, web) with automated diagnostics
delegates-to: autonomous-agent:orchestrator
---

# GUI Debug & Validation Command

**🔍 Ultimate GUI diagnostic tool for comprehensive graphical user interface validation and debugging**

Run comprehensive validation, debugging, and performance analysis of the entire GUI system (web dashboard, CLI interface, visual components, and user interactions) with automated issue detection and resolution capabilities across all user touchpoints.

## 🚀 Features

### **Multi-Interface GUI Validation**
- **Web Dashboard**: Flask application, real-time charts, responsive design, browser compatibility
- **CLI Interface**: Slash command execution, output formatting, Claude Code CLI integration
- **Visual Components**: Chart rendering, color schemes, typography, accessibility compliance
- **Data Presentation**: Real-time updates, caching, export functionality, cross-interface consistency

### **Systematic GUI Testing**
- **Interface Discovery**: Catalog all GUI components and user interaction flows
- **Functionality Testing**: Complete validation of all interface interactions
- **Performance Analysis**: Load times, responsiveness, memory usage across all interfaces
- **Cross-Platform Testing**: Windows, macOS, Linux compatibility validation
- **Accessibility Testing**: WCAG 2.1 AA compliance checking

### **Automated Issue Resolution**
- **Web Dashboard Auto-Fixes**: Missing assets, broken links, JavaScript errors, API issues
- **CLI Interface Auto-Fixes**: Command registration, argument parsing, output formatting
- **Visual Component Auto-Fixes**: Color contrast, chart defaults, responsive layouts
- **Pattern Learning**: Store successful GUI debugging approaches for future resolution

## 📋 Usage

```bash
# Show help message
/debug:gui --help

# Complete GUI system validation (recommended for first time)
/debug:gui

# Quick health check (45 seconds)
/debug:gui --quick-check

# Web dashboard focused validation
/debug:gui --web-dashboard

# CLI interface focused validation
/debug:gui --cli-interface

# Visual components validation
/debug:gui --visual-components

# Cross-platform compatibility testing
/debug:gui --cross-platform

# Accessibility compliance testing
/debug:gui --accessibility

# Full system scan with detailed reporting
/debug:gui --full-scan

# Real-time GUI monitoring mode (continuous)
/debug:gui --monitor

# Debug mode with enhanced logging
/debug:gui --verbose

# Show agent delegation process
/debug:gui --verbose
```

## Help & Documentation

### `--help` Option
```bash
# Display comprehensive help information
/debug:gui --help
```

The `--help` option provides:
- Complete command description and purpose
- Detailed usage examples with syntax
- Explanation of all available options and flags
- Agent delegation information
- Common use cases and recommendations
- Troubleshooting guidance

### Command Syntax
```bash
/debug:gui [OPTIONS]
```

### Agent Delegation
This command delegates to the **orchestrator** agent, which:
- Analyzes the GUI debugging request
- Selects appropriate specialized agents (gui-validator, frontend-analyzer, etc.)
- Manages the validation workflow
- Ensures quality assessment and reporting
- Stores learned patterns for future improvements

### Verbose Mode
```bash
/debug:gui --verbose
```
Shows detailed agent selection and delegation process:
```
🔍 ORCHESTRATOR: Analyzing GUI debugging request...
📋 ORCHESTRATOR: Task type identified: "comprehensive GUI validation"
🎯 ORCHESTRATOR: Selecting agents: gui-validator, frontend-analyzer, performance-analytics
🚀 GUI-VALIDATOR: Beginning systematic GUI analysis...
📊 FRONTEND-ANALYZER: Analyzing frontend components...
📈 PERFORMANCE-ANALYTICS: Monitoring GUI performance metrics...
```
### Getting Started
1. **First Time**: Run `/debug:gui` for complete system validation
2. **Quick Check**: Use `/debug:gui --quick-check` for rapid health assessment
3. **Specific Issues**: Use targeted options (`--web-dashboard`, `--cli-interface`)
4. **Monitor Mode**: Use `/debug:gui --monitor` for continuous oversight
5. **Get Help**: Always available with `/debug:gui --help`

### Common Issues & Solutions

**Dashboard Loading Problems**:
```bash
/debug:gui --web-dashboard --verbose
```

**CLI Command Issues**:
```bash
/debug:gui --cli-interface --verbose
```

**Performance Issues**:
```bash
/debug:gui --visual-components --performance
```

**Cross-Platform Problems**:
```bash
/debug:gui --cross-platform --full-scan
```

## 🔧 Validation Options

| Option | Description | Duration | When to Use |
|---------|-------------|----------|-------------|
| `--help` | Show comprehensive help and usage information | Instant | First time use or guidance needed |
| `--quick-check` | Basic health check for all GUI interfaces | 45s | Quick validation before use |
| `--web-dashboard` | Web dashboard focused validation | 60s | Dashboard issues suspected |
| `--cli-interface` | CLI interface focused validation | 30s | Command execution problems |
| `--visual-components` | Charts and visual elements validation | 90s | Visualization issues |
| `--cross-platform` | Multi-platform compatibility testing | 2min | Platform-specific issues |
| `--accessibility` | WCAG compliance and accessibility testing | 60s | Accessibility requirements |
| `--full-scan` | Complete GUI system validation | 3min | Comprehensive analysis |
| `--monitor` | Continuous real-time GUI monitoring | Ongoing | Production monitoring |
| `--verbose` | Enhanced logging and diagnostics | Varied | Debugging complex issues |

## 📊 What Gets Validated

### **Web Dashboard Interface**
- ✅ Flask application health and accessibility
- ✅ Real-time chart rendering and data visualization
- ✅ Interactive UI components (buttons, dropdowns, filters)
- ✅ Responsive design and mobile compatibility
- ✅ Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- ✅ JavaScript functionality and performance
- ✅ API endpoint connectivity and response times
- ✅ Loading states, error states, and user feedback

### **CLI Interface**
- ✅ All slash command execution and validation
- ✅ Command argument parsing and validation
- ✅ Output formatting consistency and readability
- ✅ Error handling and user feedback clarity
- ✅ Integration with Claude Code CLI
- ✅ Help text completeness and accuracy
- ✅ Long-running command progress indicators
- ✅ Terminal compatibility and color formatting

### **Visual Components System**
- ✅ Chart rendering accuracy and performance
- ✅ Color schemes and theme consistency
- ✅ Typography readability across devices
- ✅ Interactive elements and animations
- ✅ Icons, symbols, and visual feedback
- ✅ Data labels, legends, and tooltips
- ✅ Loading states and error visualization
- ✅ Export functionality and report generation

### **Data Presentation Layer**
- ✅ Real-time data synchronization across interfaces
- ✅ Data transformation and formatting accuracy
- ✅ Caching strategies and performance optimization
- ✅ Cross-interface data consistency
- ✅ Multi-language support and localization
- ✅ Export formats (JSON, CSV, images)
- ✅ Historical data handling and trends

## 🐛 Common GUI Issues Auto-Fixed

### **High Priority (Auto-Fixed)**
- **Web Dashboard Loading**: Missing CSS/JS files, broken links, API connectivity
- **CLI Command Execution**: Command registration, argument parsing, output formatting
- **Data Synchronization**: Real-time update failures, cross-interface consistency
- **Visual Component Rendering**: Chart library loading, data format issues

### **Medium Priority (Attempted Auto-Fix)**
- **Browser Compatibility**: JavaScript polyfills, CSS compatibility fixes
- **Mobile Responsiveness**: Layout issues, touch interaction problems
- **Performance Optimization**: Bundle size reduction, caching improvements
- **Color Contrast**: Accessibility improvements for colorblind users

### **Low Priority (Reported with Guidance)**
- **Advanced Accessibility**: Screen reader compatibility, keyboard navigation
- **Internationalization**: RTL language support, character encoding
- **Advanced Visual Design**: Theme customization, advanced animations
- **Edge Case Scenarios**: Unusual device sizes, legacy browser support

## 📈 Comprehensive GUI Performance Metrics

### **Web Dashboard Metrics:**
- **Page Load Time**: Full page and component loading times
- **First Contentful Paint**: Time to first meaningful content
- **Time to Interactive**: Time until interface is fully interactive
- **Chart Rendering Time**: Individual chart rendering performance
- **API Response Times**: Backend data fetching performance
- **Memory Usage**: Browser memory consumption and leak detection
- **Bundle Size**: JavaScript and CSS bundle optimization

### **CLI Interface Metrics:**
- **Command Execution Time**: Time from command invocation to output
- **Output Rendering Time**: Time to format and display results
- **Error Response Time**: Time to handle and display errors
- **Argument Parsing Speed**: Command argument processing performance
- **Integration Response**: Claude Code CLI integration performance

### **User Experience Metrics:**
- **Interface Responsiveness**: Response to user interactions
- **Navigation Efficiency**: Time to complete common tasks
- **Error Recovery**: Time to recover from errors
- **Learning Curve**: Interface intuitiveness and ease of use
- **Accessibility Score**: WCAG compliance and usability

## 🎯 Example Outputs

### **✅ Successful GUI Validation**
```
=======================================================
  COMPREHENSIVE GUI VALIDATION COMPLETE
=======================================================

+- Overall GUI Health Score ----------------------------+
| Score: 91/100 ✅ EXCELLENT                           |
| Status: Production Ready                            |
| Validation Time: 2m 15s                             |
+-------------------------------------------------------+

+- Interface Summary ---------------------------------+
| Web Dashboard:    94/100 ✅ (Fully functional)        |
| CLI Interface:    89/100 ✅ (All commands working)    |
| Visual Components: 92/100 ✅ (Charts rendering correctly)|
| Data Presentation: 88/100 ✅ (Real-time sync working)  |
+-------------------------------------------------------+

+- Performance Metrics -------------------------------+
| Web Dashboard Load: 1.8s ✅ (target: <2s)            |
| CLI Command Response: 0.4s ✅ (target: <1s)         |
| Chart Render Time: 0.8s ✅ (target: <1s)            |
| Real-time Update: 0.3s ✅ (target: <1s)             |
| Memory Usage: 124MB ✅ (stable)                     |
| API Response Time: 142ms ✅ (target: <200ms)        |
+-------------------------------------------------------+

+- Cross-Platform Compatibility -----------------------+
| Windows:           ✅ Fully compatible               |
| macOS:             ✅ Fully compatible               |
| Linux:             ✅ Fully compatible               |
| Mobile Responsive: ✅ Responsive design working      |
+-------------------------------------------------------+

+- Browser Compatibility ------------------------------+
| Chrome:  ✅ Full functionality                      |
| Firefox: ✅ Full functionality                      |
| Safari:  ✅ Full functionality                      |
| Edge:    ✅ Full functionality                      |
+-------------------------------------------------------+

+- Issues Resolved -----------------------------------+
| * Fixed 2 web dashboard layout issues                |
| * Optimized 3 CLI command output formats            |
| * Improved 1 chart rendering performance             |
| * Enhanced 1 mobile responsiveness issue             |
| * Resolved 1 color contrast accessibility problem     |
+-------------------------------------------------------+

+- Accessibility Score -------------------------------+
| WCAG 2.1 AA Compliance: 92/100 ✅                   |
| Color Contrast: ✅ Pass                             |
| Keyboard Navigation: ✅ Pass                         |
| Screen Reader Support: ✅ Pass                       |
| Focus Management: ✅ Pass                           |
+-------------------------------------------------------+

🌐 Web Dashboard URL: http://127.0.0.1:5000
💻 CLI Commands: 16/16 working ✅
📊 Real-time monitoring: ENABLED
🧠 Pattern learning: 4 new GUI debugging patterns stored
⏰ Next auto-check: In 30 minutes

**GUI System Status: Production Ready** ✅
```

### **[WARN]️ GUI Issues Found**
```
=======================================================
  GUI VALIDATION - ACTION REQUIRED
=======================================================

+- Overall GUI Health Score ----------------------------+
| Score: 76/100 [WARN]️ NEEDS IMPROVEMENT                   |
| Status: Functional with Issues                      |
| Validation Time: 2m 45s                             |
+-------------------------------------------------------+

+- Critical Issues -----------------------------------+
| 🔴 [HIGH] Web dashboard charts not rendering on Safari |
|   Impact: 15% of users cannot view data visualizations |
|   Auto-fix attempted: Failed - Safari-specific JS issue |
|   Required action: Test and implement Safari polyfills  |
|                                                       |
| 🔴 [HIGH] CLI commands failing on Windows PowerShell  |
|   Impact: Windows users cannot execute plugin commands |
|   Auto-fix attempted: Partial - Fixed argument parsing  |
|   Required action: Complete PowerShell compatibility     |
+-------------------------------------------------------+

+- Performance Issues -------------------------------+
| 🟡 [MED] Slow chart rendering with large datasets      |
|   Impact: Poor user experience with >1000 data points   |
|   Current: 3.2s (target: <1s)                        |
|   Fix needed: Implement data sampling and lazy loading  |
|                                                       |
| 🟡 [MED] Mobile menu not fully responsive             |
|   Impact: Poor mobile navigation experience             |
|   Fix needed: CSS media query adjustments               |
|                                                       |
| 🟡 [MED] CLI output formatting inconsistent            |
|   Impact: Reduced readability across terminals         |
|   Fix needed: Standardize output formatting            |
+-------------------------------------------------------+

+- Usability Issues ----------------------------------+
| 🟢 [LOW] Color contrast insufficient for colorblind   |
|   Impact: Reduced accessibility for 8% of users       |
|   Fix needed: Adjust color contrast ratios              |
|                                                       |
| 🟢 [LOW] Help text missing for advanced options       |
|   Impact: Reduced discoverability of features         |
|   Fix needed: Generate comprehensive help documentation |
+-------------------------------------------------------+

+- Interface Status ----------------------------------+
| Web Dashboard:    [WARN]️ Functional with issues          |
| CLI Interface:    [WARN]️ Partial functionality           |
| Visual Components: [WARN]️ Performance issues              |
| Data Presentation: ✅ Working correctly              |
+-------------------------------------------------------+

+- Immediate Actions Required ------------------------+
| 1. [HIGH] Fix Safari chart rendering compatibility   |
| 2. [HIGH] Complete Windows PowerShell support        |
| 3. [MED] Optimize chart performance for large data   |
| 4. [MED] Improve mobile responsiveness               |
| 5. [MED] Standardize CLI output formatting          |
| 6. [LOW] Enhance color accessibility                |
| 7. [LOW] Complete help documentation                |
+-------------------------------------------------------+

+- Auto-Fix Applied -----------------------------------+
| ✅ Fixed web dashboard layout issues                  |
| ✅ Restored missing JavaScript assets                 |
| ✅ Improved CLI error message formatting              |
| ✅ Updated color contrast for better accessibility    |
+-------------------------------------------------------+

📊 Pattern learning: 5 new GUI debugging patterns stored
🔧 Tools used: code-analysis, quality-standards, pattern-learning
⏰ Follow-up recommended: In 1 hour
```

## 🛠️ Advanced GUI Debugging

### **Interface-Specific Debugging**
```bash
# Web dashboard deep dive
/gui-debug --web-dashboard --verbose --performance

# CLI interface analysis
/gui-debug --cli-interface --cross-platform

# Visual components focus
/gui-debug --visual-components --accessibility

# Data presentation validation
/gui-debug --data-integrity --real-time-sync
```

### **Cross-Platform Testing**
```bash
# Complete cross-platform validation
/gui-debug --cross-platform --full-report

# Browser compatibility testing
/gui-debug --browser-compatibility --all-browsers

# Mobile device testing
/gui-debug --mobile-responsive --device-testing
```

### **Continuous Monitoring**
```bash
# Start continuous GUI monitoring with alerts
/gui-debug --monitor --alert-threshold 80

# Monitor specific GUI components
/gui-debug --monitor --components web-dashboard,cli-interface

# Set custom alert thresholds for GUI health
/gui-debug --monitor --response-time-threshold 500 --accessibility-threshold 90
```

### **Deep Diagnostics**
```bash
# GUI memory profiling and leak detection
/gui-debug --profile-gui-memory

# Cross-browser performance analysis
/gui-debug --browser-performance

# CLI command performance analysis
/gui-debug --cli-performance

# Accessibility compliance audit
/gui-debug --accessibility-audit --wcag-2.1-aa
```

## 🔍 Integration with Other Commands

### **Before Development**
```bash
# Ensure GUI system is healthy before making changes
/gui-debug --quick-check
```

### **After Changes**
```bash
# Validate entire GUI system after updates
/gui-debug --web-dashboard --cli-interface
```

### **Production Deployment**
```bash
# Full GUI validation before deployment
/gui-debug --full-scan --cross-platform --accessibility
```

### **Troubleshooting**
```bash
# Debug specific GUI interface issues
/gui-debug --verbose --web-dashboard --performance

# Comprehensive GUI debugging
/gui-debug --full-scan --monitor --detailed-report
```

## 📚 Related Commands

- `/dashboard` - Launch the web monitoring dashboard
- `/quality-check` - Run quality control on plugin components
- `/auto-analyze` - Autonomous project analysis
- `/performance-report` - Generate performance analytics
- `/validate` - General validation of tools and processes

## 🎯 Success Criteria

- **GUI Validation Accuracy**: 95%+ issue detection across all interfaces
- **Auto-Fix Success**: 85%+ success rate for common GUI issues
- **Performance Improvement**: 40%+ average GUI performance gain
- **User Experience**: <2s dashboard load, <1s CLI response, <1s chart render
- **Cross-Platform Compatibility**: 98%+ success rate across all platforms
- **Accessibility Compliance**: WCAG 2.1 AA standard or better
- **Interface Reliability**: 99.5%+ uptime with monitoring across all GUI components

This comprehensive GUI debugging command provides complete validation, automated issue resolution, and continuous monitoring capabilities for the entire graphical user interface system, ensuring all user touchpoints (web dashboard, CLI interface, and visual components) work reliably, perform optimally, and provide an excellent user experience across all platforms and devices.