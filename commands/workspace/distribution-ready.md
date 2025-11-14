---
name: workspace:distribution-ready
description: Clean and optimize repository for marketplace/public distribution
delegates-to: autonomous-agent:workspace-organizer
---

# Command: `/workspace:distribution-ready`

**Prepares the repository for public marketplace distribution** by removing all computer-specific files, local patterns, performance data, and unnecessary files while preserving local functionality.

## Purpose

- Clean repository for public marketplace distribution
- Remove computer-specific files and local data
- Optimize repository structure for plugin marketplace
- Preserve local functionality while cleaning remote repository
- Ensure cross-platform compatibility

## What It Does

### 1. **Repository Analysis** (5-10 seconds)
- Scan repository for computer-specific files
- Identify local patterns and performance data
- Detect unnecessary files for marketplace
- Analyze current .gitignore coverage

### 2. **File Classification** (10-15 seconds)
- **Essential Files**: Plugin core functionality (agents, skills, commands, lib)
- **Computer-Specific**: .claude*, .reports, local patterns, performance data
- **Local Development**: improvements/, patterns/, generated reports
- **Marketplace Ready**: Documentation, plugin manifest, core components

### 3. **Git Repository Cleanup** (30-60 seconds)
- Remove computer-specific files from Git tracking
- Update .gitignore with comprehensive exclusions
- Clean repository while preserving local files
- Optimize for public distribution

### 4. **Structure Verification** (10-15 seconds)
- Verify all 22 agents are present and functional
- Confirm 17 skills are accessible
- Validate 39 commands are properly structured
- Check 140+ Python scripts for cross-platform compatibility

### 5. **Marketplace Readiness Check** (15-20 seconds)
- Validate plugin manifest completeness
- Check essential documentation presence
- Verify repository size optimization
- Confirm privacy and security compliance

## Key Features

### **Smart File Preservation**
```
Computer-Specific Files (Removed from tracking, kept locally):
+- .claude*/                    # Claude AI local directories
+- .reports*/                   # Local reports and data
+- improvements/                # Local improvement analysis
+- patterns/                    # Local auto-fix patterns
+- *performance*.json          # Performance metrics
+- *metrics*.json              # Local metrics
+- quality_history*.json       # Quality tracking
+- Generated release notes      # Local changelogs

Essential Files (Kept in repository):
+- agents/                     # 22 specialized agents
+- skills/                     # 17 knowledge packages
+- commands/                   # 39 slash commands
+- lib/                        # 140+ Python utilities
+- .claude-plugin/             # Plugin manifest
+- docs/                       # Essential documentation
+- README.md                   # Main documentation
+- assets/                     # Plugin assets
```

### **Enhanced Gitignore Protection**
```gitignore
# Claude AI local directories (computer-specific)
.claude/
.claude-patterns/
.claude-unified/
.claude-preferences/
.claude-quality/
.claude-test/
data/reports/
.claudedata/reports/

# User-specific reports and data
.data/reports/
.reportscurrent/
.reportscurrentvalidation/

# Local patterns and performance data (computer-specific)
patterns/
improvements/
local_config.json
user_settings.json
*performance*.json
*metrics*.json
quality_history*.json
debugging_performance*.json
dashboard_*.json
*_backup*

# Temporary and backup files
*.tmp
*.log
*.backup
*~
.DS_Store
Thumbs.db

# OS generated files
lib/__pycache__/
__pycache__/
*.pyc
*.pyo

# Test files (local only)
dashboard_test.html
*.test.*
test_.*

# Local development files
.env.local
.env.local.*
local_settings.json
settings.local.json

# Generated reports (keep structure, clean content)
data/reports/generated/*
!data/reports/generated/.gitkeep

# Python cache and environment
*.egg-info/
.venv/
venv/
env/
ENV/
```

### **Cross-Platform Compatibility**
- ✅ Windows path compatibility
- ✅ Linux/Unix compatibility
- ✅ macOS compatibility
- ✅ Python scripts work across platforms
- ✅ File locking handled properly

### **Automatic Learning Integration**
The command integrates with the pattern learning system:
- **Store distribution patterns**: Record successful repository cleaning patterns
- **Learn optimization**: Improve file classification over time
- **Track effectiveness**: Monitor distribution success rates
- **Share patterns**: Cross-project distribution knowledge

## Usage Examples

### **Basic Usage**
```bash
# Prepare repository for marketplace distribution
/workspace:distribution-ready

# Include verbose output
/workspace:distribution-ready --verbose

# Dry run to see what would be removed
/workspace:distribution-ready --dry-run
```

### **Advanced Options**
```bash
# Prepare with specific file preservation
/workspace:distribution-ready --keep "custom-data/"

# Force cleanup of additional patterns
/workspace:distribution-ready --aggressive

# Create backup before cleanup
/workspace:distribution-ready --backup

# Skip confirmation prompts
/workspace:distribution-ready --force
```

### **Analysis Mode**
```bash
# Analyze only, don't make changes
/workspace:distribution-ready --analyze-only

# Show detailed file classification
/workspace:distribution-ready --classification

# Generate cleanup report
/workspace:distribution-ready --report
```

## Output Format

### **Terminal Output (Concise)**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 MARKETPLACE DISTRIBUTION PREPARATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Repository Analysis Complete
Files Scanned: 340
Essential Files: 304
Computer-Specific: 36

Cleanup Strategy: Optimize for marketplace

Files to Remove from Tracking:
+- .claude-patterns/ (23 files)
+- improvements/ (3 files)
+- patterns/ (1 file)
+- Generated reports (9 files)
+- Performance data (12 files)

Local Files Preserved: ✅ All 36 files
Git Protection: ✅ Enhanced .gitignore
Cross-Platform: ✅ Verified

Execute cleanup? [Y/n]: Y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ DISTRIBUTION READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[PASS] Repository cleaned for marketplace distribution
[PASS] 36 computer-specific files removed from tracking
[PASS] 304 essential files preserved
[PASS] Enhanced gitignore protection implemented
[PASS] Cross-platform compatibility verified

Final Repository: 304 files (11MB reduction)
Ready for: Marketplace distribution and GitHub release

⏱ Completed in 2 minutes 15 seconds
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### **Detailed Report File**

```
📄 Detailed report: .claude/data/reports/distribution-ready-2025-10-30.md
```

## File Classification Details

### **Essential Files (Preserved)**
- **Plugin Core**: agents/, skills/, commands/, lib/
- **Documentation**: README.md, docs/, assets/
- **Configuration**: .claude-plugin/, .github/workflows/
- **Templates**: Essential templates and examples
- **Utilities**: Core Python scripts and tools

### **Computer-Specific Files (Removed from Tracking)**
- **Local Patterns**: .claude-patterns/ (all JSON files)
- **Performance Data**: quality history, metrics, debugging data
- **Local Reports**: .data/reports/, validation reports
- **Development Files**: improvements/, patterns/, test files
- **Generated Content**: Release notes, changelogs, generated docs

### **Protected but Local**
- All removed files remain available locally
- Accessible for continued development and testing
- Automatically excluded from future commits
- Preserved across system reboots and updates

## Integration with Existing Commands

### **Development Workflow**
```bash
# Complete development work
/dev:commit --auto

# Prepare for marketplace release
/workspace:distribution-ready

# Create release
/dev:release

# Validate plugin readiness
/validate:plugin
```

### **Quality Assurance**
```bash
# Check code quality
/analyze:quality

# Prepare repository
/workspace:distribution-ready

# Validate full structure
/validate:all

# Test plugin functionality
/debug:eval plugin-installation-test
```

### **Continuous Integration**
```bash
# Automated cleanup in CI/CD
/workspace:distribution-ready --force

# Validate structure
/validate:fullstack

# Run tests
/test:comprehensive
```

## Learning System Integration

### **Pattern Storage**
```json
{
  "distribution_patterns": {
    "computer_specific_files": [
      ".claude-patterns/*.json",
      "improvements/*.json",
      "patterns/*.json",
      "*performance*.json"
    ],
    "essential_directories": [
      "agents/",
      "skills/",
      "commands/",
      "lib/",
      "docs/"
    ],
    "gitignore_patterns": [
      ".claude*",
      ".reports*",
      "*performance*",
      "*metrics*"
    ],
    "success_rate": 0.98,
    "avg_cleanup_time": 135,
    "file_preservation_accuracy": 1.0
  }
}
```

### **Continuous Improvement**
- **File Classification Learning**: Improve file type recognition
- **Cleanup Strategy Optimization**: Learn optimal cleanup approaches
- **Cross-Project Patterns**: Share successful distribution patterns
- **Effectiveness Tracking**: Monitor distribution success rates

## Best Practices

### **When to Use**
✅ **Before marketplace submission**
✅ **Before GitHub releases**
✅ **Before plugin distribution**
✅ **After major development cycles**
✅ **When repository size becomes an issue**

### **What Gets Preserved**
✅ **All plugin functionality** - Commands work identically
✅ **Learning capabilities** - Pattern learning preserved locally
✅ **Cross-platform compatibility** - All scripts work
✅ **Development workflow** - Local development unaffected
✅ **Performance tracking** - Local metrics preserved

### **What Gets Removed**
❌ **Computer-specific patterns** (preserved locally, not tracked)
❌ **Performance metrics** (preserved locally, not tracked)
❌ **Local reports** (preserved locally, not tracked)
❌ **Generated content** (preserved locally, not tracked)
❌ **Development artifacts** (preserved locally, not tracked)

## Troubleshooting

### **Common Issues**

**Repository not clean enough**
```bash
# Run with aggressive mode
/workspace:distribution-ready --aggressive

# Manually review remaining files
/workspace:distribution-ready --classification
```

**Essential files accidentally removed**
```bash
# Restore from Git history
git checkout HEAD~1 -- path/to/essential/file

# Check what was removed
git log --name-status -5
```

**Local files missing after cleanup**
```bash
# Verify local files still exist
ls -la .claude-patterns/ improvements/ patterns/

# Check gitignore protection
git status --ignored
```

### **Recovery Options**
```bash
# Undo all changes (if needed)
git reset --hard HEAD~1

# Restore specific directories
git checkout HEAD~1 -- improvements/ patterns/

# Generate new patterns
/workspace:organize --regenerate-patterns
```

## Performance Metrics

Expected performance:

| Task | Time | Success Rate |
|------|------|--------------|
| Repository analysis | 5-10s | 100% |
| File classification | 10-15s | 98% |
| Git cleanup | 30-60s | 95% |
| Structure verification | 10-15s | 99% |
| Marketplace validation | 15-20s | 97% |

**Repository Size Reduction**: 10-15MB average
**File Count Optimization**: 30-50 files removed
**Learning Improvement**: 25% faster classification after 5 uses

## Examples

### **Example 1: Standard Distribution Prep**
```bash
$ /workspace:distribution-ready

Scanning repository...
Found: 340 files total, 36 computer-specific

Classification:
[PASS] Essential: 304 files (agents, skills, commands, lib)
[PASS] Computer-specific: 36 files (patterns, metrics, reports)

Cleanup complete:
- Removed 36 files from tracking
- Enhanced .gitignore protection
- Preserved all local functionality
- Ready for marketplace distribution

Result: ✅ Distribution ready (304 files, 12MB reduction)
```

### **Example 2: Analysis Mode**
```bash
$ /workspace:distribution-ready --analyze-only

Repository Analysis Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Essential Components ([PASS] Keep):
+- agents/ (22 files) - Core plugin functionality
+- skills/ (17 files) - Knowledge packages
+- commands/ (39 files) - Slash commands
+- lib/ (140 files) - Python utilities
+- docs/ (15 files) - Essential documentation

Computer-Specific Files (🗑 Remove from tracking):
+- .claude-patterns/ (23 files) - Local patterns
+- improvements/ (3 files) - Local improvements
+- patterns/ (1 file) - Auto-fix patterns
+- Generated content (9 files) - Reports/changelogs

Recommendation: Ready for marketplace distribution cleanup
```

### **Example 3: Aggressive Cleanup**
```bash
$ /workspace:distribution-ready --aggressive --force

Aggressive cleanup mode enabled...
Additional patterns detected:
+- *.log files (5)
+- *.backup files (8)
+- Cache directories (3)
+- Temporary artifacts (12)

Executing comprehensive cleanup...
[PASS] Standard cleanup: 36 files removed
[PASS] Aggressive cleanup: 28 additional files removed
[PASS] Total optimization: 64 files removed
[PASS] Repository size reduction: 18MB

Marketplace ready: ✅ Optimized for distribution
```

---

**Version**: 1.0.0
**Integration**: Uses workspace-organizer, git-repository-manager agents
**Skills**: git-automation, pattern-learning, code-analysis, validation-standards
**Platform**: Cross-platform (Windows, Linux, Mac)
**Learning**: Full integration with pattern learning system
**Scope**: Repository optimization for marketplace distribution only