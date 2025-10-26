---
name: release-dev
description: Command for release dev
delegates-to: autonomous-agent:orchestrator
---

# Release-Dev Command

## Command: `/release-dev`

Streamlined release preparation and publishing workflow. This command automates the entire release process from version detection to GitHub/GitLab publishing with intelligent validation and automatic documentation updates.

**🚀 Quick Release Features:**
- **One-command release**: Automated end-to-end release workflow
- **Smart version detection**: Automatically determines version bump needed
- **Documentation sync**: Updates all docs, README, changelog automatically
- **Validation first**: Ensures quality before releasing
- **Auto-commit & push**: Handles all Git operations automatically
- **Multi-platform publishing**: GitHub, GitLab, npm, PyPI, Docker support

## How It Works

1. **Analyze Changes**: Reviews all changes since last release
2. **Determine Version**: Auto-detects major/minor/patch based on commits
3. **Update Version Files**: Updates plugin.json, package.json, setup.py, etc.
4. **Sync Documentation**: Updates README, CHANGELOG, RELEASE_NOTES
5. **Validate Consistency**: Cross-checks all files for version consistency
6. **Quality Check**: Runs validation to ensure quality ≥ 85/100
7. **Git Operations**: Commits, tags, and pushes automatically
8. **Create Release**: Publishes to GitHub/GitLab with release notes

## Usage

### Quick Release (Recommended)
```bash
# Fully automated release with smart detection
/release-dev

# This will:
# - Analyze changes and determine version bump
# - Update all version files and documentation
# - Validate consistency across all files
# - Run quality checks (must pass ≥ 85/100)
# - Commit, tag, and push to remote
# - Create GitHub/GitLab release automatically
```

### Specify Version Type
```bash
# Force specific version bump
/release-dev --patch     # Bug fixes only (x.y.Z)
/release-dev --minor     # New features (x.Y.0)
/release-dev --major     # Breaking changes (X.0.0)

# Specify exact version
/release-dev --version 2.5.0
```

### Validation Options
```bash
# Skip quality validation (not recommended)
/release-dev --skip-validation

# Set minimum quality threshold (default: 85)
/release-dev --quality-threshold 90

# Dry run (preview without making changes)
/release-dev --dry-run
```

### Documentation Options
```bash
# Update specific documentation
/release-dev --update-changelog
/release-dev --update-readme
/release-dev --generate-release-notes

# Custom release notes file
/release-dev --release-notes ./CUSTOM_NOTES.md
```

### Platform Options
```bash
# Publish to specific platforms
/release-dev --github      # GitHub only
/release-dev --gitlab      # GitLab only
/release-dev --npm         # Also publish to npm
/release-dev --pypi        # Also publish to PyPI
/release-dev --docker      # Build and push Docker image

# Multi-platform release
/release-dev --github --npm --docker
```

### Pre-release Options
```bash
# Create pre-release versions
/release-dev --pre-release alpha
/release-dev --pre-release beta
/release-dev --pre-release rc

# Example: v1.2.3-beta.1
/release-dev --minor --pre-release beta
```

## Workflow Stages

### Stage 1: Change Analysis (5-15 seconds)
Analyzes all changes since last release to determine version bump:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 CHANGE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Version: v3.3.2
Last Release: 2025-01-15 (9 days ago)
Commits Since Release: 24

Change Breakdown:
├─ 🎉 Features: 3 commits
│  ├─ feat: add /dev-auto command
│  ├─ feat: add interactive suggestions
│  └─ feat: .gitignore management
├─ 🐛 Bug Fixes: 2 commits
│  ├─ fix: validation error handling
│  └─ fix: documentation typos
├─ 📚 Documentation: 5 commits
├─ ♻️  Refactoring: 1 commit
└─ ⚠️  Breaking Changes: None

Recommended Version: v3.4.0 (MINOR)
Reason: New features added, no breaking changes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage 2: Version Update (5-10 seconds)
Updates version across all project files:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 VERSION UPDATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Updating version: v3.3.2 → v3.4.0

Files Updated:
├─ ✅ .claude-plugin/plugin.json
├─ ✅ README.md (4 references)
├─ ✅ CLAUDE.md (2 references)
├─ ✅ package.json
└─ ✅ docs/IMPLEMENTATION_SUMMARY.md

Total: 5 files, 8 version references updated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage 3: Documentation Sync (10-20 seconds)
Automatically updates all documentation:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 DOCUMENTATION SYNC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

README.md:
├─ Updated version badge
├─ Updated feature list
└─ Updated installation instructions

CHANGELOG.md:
├─ Generated from commit history
├─ Categorized changes:
│  ├─ Added (3 features)
│  ├─ Fixed (2 bugs)
│  ├─ Changed (1 refactor)
│  └─ Documentation (5 docs)
└─ Release date: 2025-01-24

RELEASE_NOTES.md:
├─ Human-readable summary
├─ Feature highlights
├─ Bug fix details
└─ Upgrade instructions

Documentation Status: ✅ All files synchronized
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage 4: Consistency Validation (10-15 seconds)
Cross-checks all files for consistency:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ CONSISTENCY VALIDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Version Consistency:
├─ ✅ All version references match: v3.4.0
├─ ✅ No old version numbers found
└─ ✅ Version format consistent

Documentation Consistency:
├─ ✅ Feature counts match across files
├─ ✅ Component counts accurate
├─ ✅ All links valid
└─ ✅ Examples up-to-date

Structure Consistency:
├─ ✅ All agents registered (20)
├─ ✅ All skills registered (14)
├─ ✅ All commands registered (18)
└─ ✅ Plugin.json valid

Validation Score: 100/100 ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage 5: Quality Check (30-60 seconds)
Runs comprehensive quality validation:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 QUALITY CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Code Quality:
├─ ✅ Plugin structure valid
├─ ✅ All YAML frontmatter valid
├─ ✅ All JSON files valid
└─ ✅ No syntax errors

Documentation Quality:
├─ ✅ README complete (95/100)
├─ ✅ All commands documented
├─ ✅ All agents documented
└─ ✅ Examples working

Standards Compliance:
├─ ✅ Follows plugin guidelines
├─ ✅ Naming conventions correct
└─ ✅ File structure correct

Quality Score: 92/100 ✅ (Threshold: 85)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage 6: Git Operations (10-20 seconds)
Commits, tags, and pushes automatically:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 GIT OPERATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Staging Changes:
├─ ✅ 5 files staged
└─ ✅ No unexpected changes

Creating Commit:
├─ Message: "release: v3.4.0 - Add /dev-auto and suggestions"
├─ Files: 5 modified
└─ ✅ Commit created: abc1234

Creating Tag:
├─ Tag: v3.4.0
├─ Message: "Release v3.4.0"
└─ ✅ Tag created

Pushing to Remote:
├─ ✅ Pushed to origin/main
└─ ✅ Pushed tags

Git Status: ✅ All operations successful
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage 7: Platform Publishing (15-30 seconds)
Creates releases on configured platforms:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 PLATFORM PUBLISHING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GitHub Release:
├─ Creating release v3.4.0...
├─ Title: "Release v3.4.0"
├─ Release notes from RELEASE_NOTES.md
├─ ✅ Published: https://github.com/user/repo/releases/tag/v3.4.0
└─ Downloads: https://github.com/user/repo/archive/refs/tags/v3.4.0.zip

npm Publishing:
├─ Building package...
├─ Running npm publish...
└─ ✅ Published: https://npmjs.com/package/autonomous-agent@3.4.0

Docker Publishing:
├─ Building image: user/autonomous-agent:3.4.0
├─ Pushing to Docker Hub...
└─ ✅ Published: docker pull user/autonomous-agent:3.4.0

Release Status: ✅ All platforms published successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage 8: Learning Integration (5 seconds)
Stores release pattern for future optimization:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 LEARNING INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pattern Stored:
├─ Task Type: release
├─ Version Bump: minor (3.3.2 → 3.4.0)
├─ Files Updated: 5
├─ Quality Score: 92/100
├─ Time Taken: 2m 15s
└─ ✅ Stored to .claude-patterns/

Future Improvements:
├─ Faster documentation sync (learned shortcuts)
├─ Better changelog categorization
└─ Optimized validation checks

Learning Status: ✅ Pattern captured
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ RELEASE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Release: v3.4.0
Previous: v3.3.2
Type: MINOR (new features)

Summary:
├─ 📦 Version updated across 5 files
├─ 📚 Documentation synchronized
├─ ✅ Validation passed (92/100)
├─ 🔧 Git operations successful
├─ 🚀 Published to 3 platforms
└─ 🧠 Pattern learned for future

Total Time: 2m 15s

Links:
├─ GitHub: https://github.com/user/repo/releases/tag/v3.4.0
├─ npm: https://npmjs.com/package/autonomous-agent@3.4.0
└─ Docker: docker pull user/autonomous-agent:3.4.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 SUGGESTED NEXT ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Monitor release metrics
   → /performance-report

2. Announce release to team
   → Draft announcement with highlights

3. Create next milestone
   → Plan features for v3.5.2

4. Update project board
   → Close completed issues

Choose option (1-4) or type custom command:
```

## Version Detection Logic

### Major Version (X.0.0)
Triggered by:
- `BREAKING CHANGE:` in commit messages
- `breaking:` commit type
- Major API changes detected
- Interface modifications
- Schema changes

### Minor Version (x.Y.0)
Triggered by:
- `feat:` commits (new features)
- `feature:` commits
- New functionality added
- Non-breaking additions

### Patch Version (x.y.Z)
Triggered by:
- `fix:` commits (bug fixes)
- `perf:` commits (performance improvements)
- `refactor:` commits (code refactoring)
- `docs:` commits (documentation only)
- `style:` commits (formatting)
- `chore:` commits (maintenance)

## Version File Detection

Automatically detects and updates:
- **.claude-plugin/plugin.json** (Claude plugins)
- **package.json** (Node.js/npm)
- **setup.py** (Python)
- **pyproject.toml** (Python Poetry)
- **Cargo.toml** (Rust)
- **composer.json** (PHP)
- **pom.xml** (Maven/Java)
- **\_\_init\_\_.py** (Python packages)
- **version.py** (Python version files)
- **Dockerfile** (Docker version ARG)

## Documentation Sync

Automatically updates:
- **README.md**: Version badges, feature lists, installation instructions
- **CHANGELOG.md**: Categorized change history with links
- **RELEASE_NOTES.md**: Human-readable release summary
- **docs/\*\*/\*.md**: Any documentation with version references

## Validation Checks

### Version Consistency
- All version references match
- No old version numbers remain
- Version format follows semver

### Documentation Consistency
- Feature counts accurate
- Component counts match
- Links valid and working
- Examples up-to-date

### Quality Standards
- Plugin structure valid
- YAML frontmatter correct
- JSON files parseable
- No syntax errors

### Git Readiness
- Working directory clean
- No merge conflicts
- Remote accessible
- Branch up-to-date

## Integration with Learning System

The `/release-dev` command integrates with the autonomous learning system:

**Pattern Storage**:
- Version bump decisions and reasoning
- Documentation update strategies
- Common consistency issues found
- Optimal release timing
- Platform-specific success rates

**Continuous Improvement**:
- Learn best changelog formats
- Optimize documentation sync speed
- Improve version detection accuracy
- Reduce validation time
- Enhance error prevention

## Integration with Other Commands

### Pre-Release Validation
```bash
# Validate before releasing
/validate-fullstack
/quality-check
/release-dev
```

### Post-Release Monitoring
```bash
# Monitor after release
/release-dev
/performance-report
/learning-analytics
```

### Integrated Workflow
```bash
# Complete development cycle
/dev-auto "add new feature"
# ... development happens ...
/quality-check
/release-dev
```

## Troubleshooting

### Quality Check Failed
```bash
# View detailed quality report
/quality-check --verbose

# Fix issues and retry
/release-dev --retry

# Skip validation (not recommended)
/release-dev --skip-validation --force
```

### Version Conflict
```bash
# Reset version detection
/release-dev --version 3.4.0 --force

# Manual version update
edit .claude-plugin/plugin.json
/release-dev --skip-version-update
```

### Git Operation Failed
```bash
# Check Git status
git status
git log --oneline -5

# Retry with verbose logging
/release-dev --verbose --retry
```

### Platform Publishing Failed
```bash
# Check authentication
gh auth status    # GitHub
glab auth status  # GitLab
npm whoami        # npm
docker info       # Docker

# Retry specific platform
/release-dev --github --retry
```

## Best Practices

### Pre-Release Checklist
- [ ] All changes committed and pushed
- [ ] Tests passing locally
- [ ] Documentation reflects changes
- [ ] No TODOs or FIXMEs in critical code
- [ ] Version bump type is appropriate
- [ ] Release notes are meaningful

### Release Frequency
- **Major**: Every 6-12 months (breaking changes)
- **Minor**: Every 2-4 weeks (new features)
- **Patch**: As needed (bug fixes)

### Communication
- Notify team before major/minor releases
- Share release notes with stakeholders
- Announce on relevant channels
- Update documentation sites

---

**Version**: 1.0.0
**Integration**: Works with version-release-manager agent and git-automation skill
**Platform**: Cross-platform (Windows, Linux, Mac)
**Dependencies**: Git, GitHub CLI (gh) or GitLab CLI (glab) optional
