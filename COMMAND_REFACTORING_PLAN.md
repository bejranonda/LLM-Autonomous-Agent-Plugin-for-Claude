# Command Refactoring Plan

## Executive Summary

This document outlines the comprehensive refactoring of slash commands to improve organization, memorability, and user experience. The refactoring introduces **category-based prefixes** that group related commands into logical families.

**Total Commands**: 23 → 22 (1 merge)
**Categories**: 8 clear categories
**Breaking Changes**: Yes (requires migration guide)

---

## Goals

1. ✅ **Easy to Remember**: Category prefixes make commands intuitive
2. ✅ **Logical Grouping**: Related commands grouped by function
3. ✅ **Consistent Naming**: All commands follow `category:action` pattern
4. ✅ **No Confusion**: Clear separation between old and new names during migration
5. ✅ **Quality Assurance**: All commands validated before and after changes

---

## New Command Structure

### Category 1: `dev:` - Development Workflow (3 commands)

| New Name | Old Name | Description | Change Type |
|----------|----------|-------------|-------------|
| `dev:auto` | `dev-auto` | Autonomous development from requirements to release | Rename |
| `dev:release` | `release-dev` | Streamlined release preparation | Rename |
| `dev:pr-review` | `pr-review` | Comprehensive PR review | Rename + Categorize |

**Rationale**: Core development workflow commands. `dev:` prefix clearly indicates development-focused operations.

---

### Category 2: `analyze:` - Code Analysis (4 commands)

| New Name | Old Name | Description | Change Type |
|----------|----------|-------------|-------------|
| `analyze:project` | `auto-analyze` | Autonomous project analysis | Rename + Clarify |
| `analyze:quality` | `quality-check` | Comprehensive quality control | Rename + Categorize |
| `analyze:static` | `static-analysis` | Static analysis with 40+ linters | Rename + Categorize |
| `analyze:dependencies` | `scan-dependencies` | Dependency vulnerability scanning | Rename + Categorize |

**Rationale**: All commands that analyze code/project. Clearer than mixed naming (auto-analyze, quality-check, static-analysis, scan-dependencies).

**Merging Consideration**: Could merge `analyze:quality` and `analyze:static` in future, but keeping separate for now as they serve different purposes (quality = comprehensive, static = linters only).

---

### Category 3: `validate:` - Validation & Verification (4 commands)

| New Name | Old Name | Description | Change Type |
|----------|----------|-------------|-------------|
| `validate:all` | `validate` | Comprehensive validation checks | Rename + Clarify |
| `validate:fullstack` | `validate-fullstack` | Full-stack validation | Rename (consistency) |
| `validate:plugin` | `validate-claude-plugin` | Claude plugin validation | Rename + Shorten |
| `validate:patterns` | `validate-patterns` | Pattern learning validation | Rename (consistency) |

**Rationale**: All validation commands already have `validate` prefix. Standardizing to `validate:` format. `validate:all` is clearer than generic `validate`.

---

### Category 4: `debug:` - Debugging & Diagnostics (2 commands)

| New Name | Old Name | Description | Change Type |
|----------|----------|-------------|-------------|
| `debug:eval` | `eval-debug` | Evaluation debugging | Rename (prefix first) |
| `debug:gui` | `gui-debug` | GUI debugging and validation | Rename (prefix first) |

**Rationale**: Debugging commands should start with `debug:` for clarity. Current naming has suffix-style (eval-debug, gui-debug).

---

### Category 5: `learn:` - Learning & Analytics (4 commands)

| New Name | Old Name | Description | Change Type |
|----------|----------|-------------|-------------|
| `learn:init` | `learn-patterns` | Initialize pattern learning | Rename + Clarify |
| `learn:analytics` | `learning-analytics` | Learning analytics dashboard | Rename (consistency) |
| `learn:performance` | `performance-report` | Performance analytics | Rename + Categorize |
| `learn:predict` | `predictive-analytics` | Predictive analytics | Rename + Categorize |

**Rationale**: All learning/analytics commands grouped. `learn:init` is clearer than `learn-patterns` for initialization.

**Future Optimization**: Consider merging `learn:performance` into `learn:analytics` as a sub-view:
- `learn:analytics` - Full dashboard
- `learn:analytics --focus performance` - Performance-only view

---

### Category 6: `workspace:` - Organization & Management (3 commands)

| New Name | Old Name | Description | Change Type |
|----------|----------|-------------|-------------|
| `workspace:organize` | `organize-workspace` | Workspace organization | Rename (prefix first) |
| `workspace:reports` | `organize-reports` | Report organization | Rename (prefix first) |
| `workspace:improve` | `improve-plugin` | Plugin improvement | Rename + Recategorize |

**Rationale**: Workspace management commands. `improve-plugin` fits here as it improves the workspace/plugin itself.

---

### Category 7: `monitor:` - Monitoring & Visualization (2 commands)

| New Name | Old Name | Description | Change Type |
|----------|----------|-------------|-------------|
| `monitor:dashboard` | `dashboard` | Real-time monitoring dashboard | Rename + Categorize |
| `monitor:recommend` | `recommend` | Smart recommendations | Rename + Categorize |

**Rationale**: Monitoring and observability commands. `dashboard` and `recommend` are too generic without prefix.

---

### Category 8: `release:` - Git & Release Management (MERGED)

| New Name | Old Name | Description | Change Type |
|----------|----------|-------------|-------------|
| ~~`release:auto`~~ | `git-release-workflow` | **MERGED INTO `dev:release`** | Merge + Deprecate |

**Rationale**: `git-release-workflow` and `release-dev` are redundant. Both handle release workflows.

**Migration Strategy**:
1. `dev:release` becomes the primary release command
2. `git-release-workflow` deprecated with alias to `dev:release --workflow auto`
3. Remove `git-release-workflow.md` after migration period

---

## Complete Command Mapping

### Quick Reference Table

| Category | New Command | Old Command | Status |
|----------|-------------|-------------|--------|
| **dev:** | `dev:auto` | `dev-auto` | ✅ Rename |
| **dev:** | `dev:release` | `release-dev` | ✅ Rename |
| **dev:** | `dev:pr-review` | `pr-review` | ✅ Rename |
| **analyze:** | `analyze:project` | `auto-analyze` | ✅ Rename |
| **analyze:** | `analyze:quality` | `quality-check` | ✅ Rename |
| **analyze:** | `analyze:static` | `static-analysis` | ✅ Rename |
| **analyze:** | `analyze:dependencies` | `scan-dependencies` | ✅ Rename |
| **validate:** | `validate:all` | `validate` | ✅ Rename |
| **validate:** | `validate:fullstack` | `validate-fullstack` | ✅ Rename |
| **validate:** | `validate:plugin` | `validate-claude-plugin` | ✅ Rename |
| **validate:** | `validate:patterns` | `validate-patterns` | ✅ Rename |
| **debug:** | `debug:eval` | `eval-debug` | ✅ Rename |
| **debug:** | `debug:gui` | `gui-debug` | ✅ Rename |
| **learn:** | `learn:init` | `learn-patterns` | ✅ Rename |
| **learn:** | `learn:analytics` | `learning-analytics` | ✅ Rename |
| **learn:** | `learn:performance` | `performance-report` | ✅ Rename |
| **learn:** | `learn:predict` | `predictive-analytics` | ✅ Rename |
| **workspace:** | `workspace:organize` | `organize-workspace` | ✅ Rename |
| **workspace:** | `workspace:reports` | `organize-reports` | ✅ Rename |
| **workspace:** | `workspace:improve` | `improve-plugin` | ✅ Rename |
| **monitor:** | `monitor:dashboard` | `dashboard` | ✅ Rename |
| **monitor:** | `monitor:recommend` | `recommend` | ✅ Rename |
| ~~**release:**~~ | ~~`release:auto`~~ | `git-release-workflow` | ❌ **MERGED into `dev:release`** |

**Total**: 22 active commands (23 original - 1 merge)

---

## File System Changes

### Commands to Rename

1. `commands/dev-auto.md` → `commands/dev-auto.md` (keep for backward compatibility, update content)
2. `commands/release-dev.md` → `commands/release-dev.md` (keep for backward compatibility, update content)
3. Create new files with new names, keep old files with deprecation notices

### Files to Create

All new command files with new naming:

```
commands/
├── dev/
│   ├── auto.md
│   ├── release.md
│   └── pr-review.md
├── analyze/
│   ├── project.md
│   ├── quality.md
│   ├── static.md
│   └── dependencies.md
├── validate/
│   ├── all.md
│   ├── fullstack.md
│   ├── plugin.md
│   └── patterns.md
├── debug/
│   ├── eval.md
│   └── gui.md
├── learn/
│   ├── init.md
│   ├── analytics.md
│   ├── performance.md
│   └── predict.md
├── workspace/
│   ├── organize.md
│   ├── reports.md
│   └── improve.md
└── monitor/
    ├── dashboard.md
    └── recommend.md
```

### Files to Deprecate (Migration Period)

Keep old files with deprecation notice for 1 version:

```
commands/
├── dev-auto.md (deprecated, redirects to dev:auto)
├── release-dev.md (deprecated, redirects to dev:release)
├── pr-review.md (deprecated, redirects to dev:pr-review)
... (all old files)
```

**After migration period (v4.0.0)**: Remove old files entirely.

---

## Documentation Updates Required

### Files to Update

1. **CLAUDE.md** - Update all command references
2. **README.md** - Update command list and examples
3. **USAGE_GUIDE.md** - Update all command examples
4. **STRUCTURE.md** - Update commands section
5. **CHANGELOG.md** - Add breaking changes note
6. **.claude-plugin/plugin.json** - Update description
7. **All agent files** - Update command references in agents/*.md
8. **All skill files** - Update command references in skills/*/SKILL.md

### Search & Replace Pattern

```bash
# Examples of references to update:
/dev-auto → /dev:auto
/release-dev → /dev:release
/auto-analyze → /analyze:project
/quality-check → /analyze:quality
... (all 23 commands)
```

---

## Migration Strategy

### Phase 1: Preparation (Current Version - v3.7.1)

1. ✅ Create this refactoring plan
2. ⏳ Review and validate plan
3. ⏳ Get user approval

### Phase 2: Implementation (v3.8.0 - Migration Release)

1. **Create new command files** with new names in subdirectories
2. **Keep old command files** with deprecation notices and auto-redirect
3. **Update all documentation** to show new names (with old names in parentheses)
4. **Update plugin.json** description
5. **Add migration guide** (COMMAND_MIGRATION_GUIDE.md)
6. **Update CHANGELOG** with breaking changes warning
7. **Test all commands** to ensure they work with both old and new names

**Example Deprecation Notice in Old Files**:

```markdown
---
name: dev-auto
description: [DEPRECATED] Use /dev:auto instead. This command will be removed in v4.0.0.
redirect-to: dev:auto
---

# ⚠️ DEPRECATED: This command has been renamed

**Old Name**: `/dev-auto`
**New Name**: `/dev:auto`

This command has been renamed for better organization. Please use `/dev:auto` instead.

**Why the change?**
We've reorganized all commands into clear categories (dev:, analyze:, validate:, etc.)
to make them easier to remember and discover.

**Migration Path**:
- v3.8.0 (current): Both names work, deprecation warning shown
- v4.0.0 (future): Old name removed, only new name works

For the full command documentation, see: [dev:auto](dev/auto.md)

[Original documentation follows below for reference...]
```

### Phase 3: Migration Period (v3.8.x - v3.9.x)

1. Monitor usage of old vs new commands
2. Send deprecation warnings when old commands used
3. Update tutorials and examples
4. User feedback and adjustments

### Phase 4: Cleanup (v4.0.0 - Breaking Release)

1. **Remove all old command files**
2. **Remove all old command references**
3. **Update plugin.json version** to 4.0.0
4. **Update CHANGELOG** with removed commands
5. **Final validation**

---

## Benefits of New Structure

### 1. **Easy Discovery**

Users can type `/dev:` and see all development commands, `/analyze:` for all analysis commands, etc.

### 2. **Logical Grouping**

Related commands are clearly grouped:
- Development: `dev:auto`, `dev:release`, `dev:pr-review`
- Analysis: `analyze:project`, `analyze:quality`, `analyze:static`, `analyze:dependencies`
- Validation: `validate:all`, `validate:fullstack`, `validate:plugin`, `validate:patterns`

### 3. **Consistent Naming**

All commands follow the same `category:action` pattern. No more mixing:
- ❌ Old: `auto-analyze`, `quality-check`, `static-analysis`, `scan-dependencies`
- ✅ New: `analyze:project`, `analyze:quality`, `analyze:static`, `analyze:dependencies`

### 4. **Clearer Purpose**

The category prefix immediately tells users what the command does:
- `dev:auto` - Development automation
- `analyze:quality` - Analysis of quality
- `validate:fullstack` - Validation of full-stack
- `debug:gui` - Debugging GUI
- `learn:analytics` - Learning analytics
- `workspace:organize` - Workspace organization
- `monitor:dashboard` - Monitoring dashboard

### 5. **Future Extensibility**

Easy to add new commands in existing categories:
- `dev:test` - Run comprehensive tests
- `analyze:security` - Security analysis
- `validate:api` - API contract validation
- `debug:performance` - Performance debugging
- `learn:export` - Export learned patterns
- `workspace:backup` - Backup workspace
- `monitor:alerts` - Set up alerts

---

## Risk Assessment

### High Risk
- ❌ **Breaking change** - Users' workflows will break
- ✅ **Mitigation**: Migration period with both old and new names working

### Medium Risk
- ⚠️ **Documentation drift** - Some docs might not get updated
- ✅ **Mitigation**: Comprehensive search & replace, validation scripts

### Low Risk
- ⚠️ **User confusion** during migration
- ✅ **Mitigation**: Clear deprecation notices, migration guide

---

## Validation Checklist

### Before Implementation
- [ ] Review this plan with stakeholders
- [ ] Confirm all command mappings are correct
- [ ] Verify no commands are missed
- [ ] Check for naming conflicts

### During Implementation
- [ ] All new command files created
- [ ] All old command files updated with deprecation notices
- [ ] All documentation updated
- [ ] plugin.json updated
- [ ] Migration guide created
- [ ] CHANGELOG updated

### After Implementation
- [ ] Test all new command names work
- [ ] Test all old command names still work (with warnings)
- [ ] Verify deprecation notices appear
- [ ] Validate all documentation links work
- [ ] Run `/validate:all` to ensure consistency
- [ ] User acceptance testing

---

## Timeline

| Phase | Version | Duration | Status |
|-------|---------|----------|--------|
| Planning | v3.7.1 | 1 day | ✅ Complete |
| Implementation | v3.8.0 | 2-3 days | ⏳ Pending |
| Migration | v3.8.x - v3.9.x | 2-4 weeks | ⏳ Pending |
| Cleanup | v4.0.0 | 1 day | ⏳ Pending |

---

## Next Steps

1. **Review this plan** - Get feedback and approval
2. **Update todos** - Break down into specific tasks
3. **Start implementation** - Begin with new command files
4. **Create migration guide** - User-facing documentation
5. **Update all documentation** - Comprehensive updates
6. **Test thoroughly** - Ensure quality
7. **Release v3.8.0** - Migration release

---

## Questions to Address

1. ❓ Should we merge `learn:performance` into `learn:analytics`?
2. ❓ Should we create subdirectories or keep flat structure with colons in filenames?
3. ❓ How long should the migration period be? (Recommendation: 2-4 weeks)
4. ❓ Should we create aliases for power users? (e.g., `/da` for `/dev:auto`)

---

## Conclusion

This refactoring significantly improves command organization, discoverability, and user experience. The category-based naming scheme is intuitive, consistent, and extensible. With proper migration planning, we can execute this breaking change smoothly while maintaining backward compatibility during the transition period.

**Recommendation**: Proceed with implementation in v3.8.0 with a 2-4 week migration period before final cleanup in v4.0.0.
