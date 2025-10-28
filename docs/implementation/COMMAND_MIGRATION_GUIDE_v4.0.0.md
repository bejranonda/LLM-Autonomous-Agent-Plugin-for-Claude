# Command Migration Guide: v3.7.1 → v4.0.0

## 🚨 Breaking Changes

Version 4.0.0 introduces a complete reorganization of slash commands into **logical categories**. All commands now use a `category:action` format for better organization and discoverability.

**Summary of Changes:**
- **22 commands** reorganized into **7 clear categories**
- All command names now follow `category:action` pattern
- **No functional changes** - all features work exactly the same
- Old command names no longer supported (major version upgrade)

---

## Quick Reference

### Development Commands (`dev:`)
| Old Command | New Command | Purpose |
|-------------|-------------|---------|
| `/dev-auto` | `/dev:auto` | Autonomous development from requirements to release |
| `/release-dev` | `/dev:release` | Streamlined release preparation and publishing |
| `/pr-review` | `/dev:pr-review` | Comprehensive pull request review |

### Analysis Commands (`analyze:`)
| Old Command | New Command | Purpose |
|-------------|-------------|---------|
| `/auto-analyze` | `/analyze:project` | Autonomous project analysis |
| `/quality-check` | `/analyze:quality` | Comprehensive quality control |
| `/static-analysis` | `/analyze:static` | Static analysis with 40+ linters |
| `/scan-dependencies` | `/analyze:dependencies` | Dependency vulnerability scanning |

### Validation Commands (`validate:`)
| Old Command | New Command | Purpose |
|-------------|-------------|---------|
| `/validate` | `/validate:all` | Comprehensive validation checks |
| `/validate-fullstack` | `/validate:fullstack` | Full-stack validation |
| `/validate-claude-plugin` | `/validate:plugin` | Claude plugin validation |
| `/validate-patterns` | `/validate:patterns` | Pattern learning validation |

### Debug Commands (`debug:`)
| Old Command | New Command | Purpose |
|-------------|-------------|---------|
| `/eval-debug` | `/debug:eval` | Evaluation debugging |
| `/gui-debug` | `/debug:gui` | GUI debugging and validation |

### Learning Commands (`learn:`)
| Old Command | New Command | Purpose |
|-------------|-------------|---------|
| `/learn-patterns` | `/learn:init` | Initialize pattern learning |
| `/learning-analytics` | `/learn:analytics` | Learning analytics dashboard |
| `/performance-report` | `/learn:performance` | Performance analytics |
| `/predictive-analytics` | `/learn:predict` | Predictive analytics |

### Workspace Commands (`workspace:`)
| Old Command | New Command | Purpose |
|-------------|-------------|---------|
| `/organize-workspace` | `/workspace:organize` | Workspace organization |
| `/organize-reports` | `/workspace:reports` | Report organization |
| `/improve-plugin` | `/workspace:improve` | Plugin improvement |

### Monitor Commands (`monitor:`)
| Old Command | New Command | Purpose |
|-------------|-------------|---------|
| `/dashboard` | `/monitor:dashboard` | Real-time monitoring dashboard |
| `/recommend` | `/monitor:recommend` | Smart recommendations |

### Merged/Removed Commands
| Old Command | Status | New Command |
|-------------|--------|-------------|
| `/git-release-workflow` | **Merged** into `/dev:release` | Use `/dev:release` instead |

---

## Benefits of New Structure

### 🎯 Easy Discovery
Type `/dev:` to see all development commands, `/analyze:` for analysis tools, etc.

### 📁 Logical Grouping
Related commands are grouped by function:
- **Development**: `dev:auto`, `dev:release`, `dev:pr-review`
- **Analysis**: `analyze:project`, `analyze:quality`, `analyze:static`, `analyze:dependencies`
- **Validation**: `validate:all`, `validate:fullstack`, `validate:plugin`, `validate:patterns`

### 🔍 Clear Purpose
Category prefixes immediately tell you what the command does:
- `dev:auto` - Development automation
- `analyze:quality` - Analysis of quality
- `validate:fullstack` - Validation of full-stack
- `debug:gui` - Debugging GUI
- `learn:analytics` - Learning analytics
- `workspace:organize` - Workspace organization
- `monitor:dashboard` - Monitoring dashboard

### 🚀 Future Extensibility
Easy to add new commands in existing categories:
- `dev:test` - Run comprehensive tests
- `analyze:security` - Security analysis
- `validate:api` - API contract validation
- `debug:performance` - Performance debugging
- `learn:export` - Export learned patterns
- `workspace:backup` - Backup workspace
- `monitor:alerts` - Set up alerts

---

## Usage Examples: Before vs After

### Development Workflow
**Before:**
```bash
/dev-auto "add new feature"
/quality-check
/release-dev
```

**After:**
```bash
/dev:auto "add new feature"
/analyze:quality
/dev:release
```

### Analysis Workflow
**Before:**
```bash
/auto-analyze
/static-analysis
/scan-dependencies
```

**After:**
```bash
/analyze:project
/analyze:static
/analyze:dependencies
```

### Learning & Analytics
**Before:**
```bash
/learn-patterns
/learning-analytics
/performance-report
```

**After:**
```bash
/learn:init
/learn:analytics
/learn:performance
```

### Validation Workflow
**Before:**
```bash
/validate
/validate-fullstack
/validate-patterns
```

**After:**
```bash
/validate:all
/validate:fullstack
/validate:patterns
```

---

## Updated Workflows

### Complete Development Cycle
```bash
# Start development
/dev:auto "implement new API endpoint"

# Analysis phase
/analyze:project
/analyze:quality
/analyze:dependencies

# Validation phase
/validate:all
/validate:fullstack

# Learning phase
/learn:analytics
/learn:performance

# Release phase
/dev:release
```

### Quality Assurance Workflow
```bash
# Comprehensive analysis
/analyze:project
/analyze:static
/analyze:dependencies

# Validation checks
/validate:all
/validate:plugin
/validate:patterns

# Monitor results
/monitor:dashboard
/learn:performance
```

### Plugin Management Workflow
```bash
# Workspace organization
/workspace:organize
/workspace:reports

# Plugin improvement
/workspace:improve
/validate:plugin

# Monitor performance
/monitor:dashboard
/monitor:recommend
```

### Debugging Workflow
```bash
# Debug evaluation
/debug:eval

# Debug GUI issues
/debug:gui

# Analyze performance
/learn:performance
/monitor:dashboard
```

---

## Integration Updates

### CI/CD Pipelines
Update your CI/CD files:

**GitHub Actions Example:**
```yaml
# Before
- name: Run Quality Check
  run: /quality-check

# After
- name: Run Quality Analysis
  run: /analyze:quality
```

### Documentation
Update any documentation, tutorials, or guides:

**Before:**
```markdown
Use `/dev-auto` to automatically implement features.
```

**After:**
```markdown
Use `/dev:auto` to automatically implement features.
```

### Scripts and Automation
Update any scripts or automation tools:

**Before:**
```bash
#!/bin/bash
/auto-analyze
/quality-check
```

**After:**
```bash
#!/bin/bash
/analyze:project
/analyze:quality
```

---

## Category Overview

### 🛠️ Development (`dev:`)
Commands for development workflow and lifecycle management.
- `dev:auto` - Autonomous development from requirements to release
- `dev:release` - Streamlined release preparation and publishing
- `dev:pr-review` - Comprehensive pull request review

### 🔍 Analysis (`analyze:`)
Commands for analyzing code, quality, and dependencies.
- `analyze:project` - Autonomous project analysis
- `analyze:quality` - Comprehensive quality control
- `analyze:static` - Static analysis with 40+ linters
- `analyze:dependencies` - Dependency vulnerability scanning

### ✅ Validation (`validate:`)
Commands for validation and verification.
- `validate:all` - Comprehensive validation checks
- `validate:fullstack` - Full-stack validation
- `validate:plugin` - Claude plugin validation
- `validate:patterns` - Pattern learning validation

### 🐛 Debug (`debug:`)
Commands for debugging and diagnostics.
- `debug:eval` - Evaluation debugging
- `debug:gui` - GUI debugging and validation

### 📚 Learning (`learn:`)
Commands for pattern learning and analytics.
- `learn:init` - Initialize pattern learning
- `learn:analytics` - Learning analytics dashboard
- `learn:performance` - Performance analytics
- `learn:predict` - Predictive analytics

### 🗂️ Workspace (`workspace:`)
Commands for workspace organization and management.
- `workspace:organize` - Workspace organization
- `workspace:reports` - Report organization
- `workspace:improve` - Plugin improvement

### 📊 Monitor (`monitor:`)
Commands for monitoring and visualization.
- `monitor:dashboard` - Real-time monitoring dashboard
- `monitor:recommend` - Smart recommendations

---

## Troubleshooting

### Common Issues

**Q: My old commands don't work anymore**
A: This is a breaking change in v4.0.0. Use the new command names from the reference table above.

**Q: I can't remember the new command names**
A: Type the category prefix (e.g., `/dev:`) and you'll see all available commands in that category.

**Q: Where did `/git-release-workflow` go?**
A: It's been merged into `/dev:release` for consistency. All functionality is preserved.

**Q: How do I find a specific command?**
A: Think about the category:
- Development tasks → `dev:`
- Analysis tasks → `analyze:`
- Validation tasks → `validate:`
- Debugging tasks → `debug:`
- Learning/analytics → `learn:`
- Workspace management → `workspace:`
- Monitoring tasks → `monitor:`

### Migration Checklist

- [ ] Update scripts and automation
- [ ] Update CI/CD pipelines
- [ ] Update documentation and tutorials
- [ ] Update team training materials
- [ ] Test your common workflows
- [ ] Share this guide with your team

---

## Support

If you encounter issues with the migration:

1. **Check this guide** - Most questions are answered here
2. **Try the category prefix** - Type `/dev:`, `/analyze:`, etc. to discover commands
3. **Refer to the complete command list** - See README.md for full documentation
4. **Check the CHANGELOG** - For detailed technical changes

---

## Looking Forward

This reorganization provides a solid foundation for future enhancements:

### Coming Soon
- New `dev:test` command for comprehensive testing
- Enhanced `analyze:security` command
- Advanced `validate:api` command
- Intelligent `debug:performance` command
- Powerful `learn:export` command
- Automated `workspace:backup` command
- Real-time `monitor:alerts` command

### Benefits for New Users
- **Easier learning curve** - Commands grouped logically
- **Better discoverability** - Category prefixes guide exploration
- **Consistent naming** - All commands follow same pattern
- **Clear purpose** - Category immediately tells you the function

---

**Version**: 4.0.0
**Breaking Changes**: Yes
**Migration Required**: Yes
**Backward Compatibility**: No (major version)
**Functional Changes**: None - all features preserved

Welcome to the new organized command structure! 🎉