---
name: dev:release
description: Complete automated release workflow with platform detection (GitHub/GitLab/Bitbucket) and release creation
delegates-to: autonomous-agent:version-release-manager
---

# Release-Dev Command

## Command: `/autonomous-agent:dev:release`

**CRITICAL**: This command MUST execute ALL steps from version detection through GitHub release creation. The version-release-manager agent MUST complete the entire workflow without stopping early.

Streamlined release preparation and publishing workflow. This command automates the entire release process from version detection to GitHub/GitLab publishing with intelligent validation and automatic documentation updates.

## MANDATORY EXECUTION STEPS

**The version-release-manager agent MUST execute these steps in order and COMPLETE ALL OF THEM:**

### Step 1: Analyze Changes (REQUIRED)
- Run `git log --oneline` to review commits since last release
- Categorize changes (features, fixes, breaking changes)
- Determine version bump type (major/minor/patch)

### Step 2: Determine Version (REQUIRED)
- Read current version from `.claude-plugin/plugin.json`
- Calculate new version based on changes
- Confirm version follows semantic versioning

### Step 3: Update Version Files (REQUIRED)
- Update `.claude-plugin/plugin.json`
- Update `README.md` (all version references)
- Update `CLAUDE.md` (all version references)
- Update any other files with version numbers

### Step 4: Generate Documentation (REQUIRED)
- Generate `CHANGELOG.md` entry from git commits
- Create `RELEASE_NOTES_v{version}.md` with human-readable summary
- Update feature counts and component lists

### Step 5: Validate Consistency (REQUIRED)
- Verify all version numbers match
- Check documentation consistency
- Validate no old version references remain

### Step 6: Git Operations (REQUIRED)
- Stage all changes: `git add .`
- Create commit with message: `release: v{version} - {summary}`
- Create git tag: `git tag v{version}`
- Push to remote: `git push origin main`
- Push tags: `git push origin v{version}`

### Step 7: Create Repository Release (REQUIRED - DO NOT SKIP)
**This step is MANDATORY and MUST be executed based on detected platform:**

#### Step 7a: Detect Repository Platform (REQUIRED)
```bash
# Detect platform from git remote URL
git remote get-url origin

# Identify platform:
# - Contains "github.com" -> GitHub
# - Contains "gitlab.com" or "gitlab" -> GitLab
# - Contains "bitbucket.org" -> Bitbucket
# - Others -> Generic git repository (skip release creation)
```

#### Step 7b: Create Platform Release (REQUIRED if platform detected)

**For GitHub repositories:**
```bash
# Verify GitHub CLI is authenticated
gh auth status

# Create GitHub release
gh release create v{version} \
  --title "Release v{version}: {title}" \
  --notes-file RELEASE_NOTES_v{version}.md \
  --latest
```

**For GitLab repositories:**
```bash
# Verify GitLab CLI is authenticated
glab auth status

# Create GitLab release
glab release create v{version} \
  --name "Release v{version}: {title}" \
  --notes "$(cat RELEASE_NOTES_v{version}.md)"
```

**For Bitbucket repositories:**
```bash
# Bitbucket uses git tags (already created in Step 6)
# No additional CLI command needed
echo "✅ Release created via git tag (Bitbucket)"
```

**For other git repositories:**
```bash
# Generic git repository without platform-specific features
echo "✅ Release created via git tag"
```

### Step 8: Verify Release (REQUIRED)
**Platform-specific verification:**

**For GitHub:**
```bash
gh release view v{version}
echo "✅ GitHub Release: https://github.com/{owner}/{repo}/releases/tag/v{version}"
```

**For GitLab:**
```bash
glab release view v{version}
echo "✅ GitLab Release: https://gitlab.com/{owner}/{repo}/-/releases/v{version}"
```

**For others:**
```bash
git tag -l v{version}
echo "✅ Git tag created: v{version}"
```

- Store release pattern for learning

**🚀 Quick Release Features:**
- **One-command release**: Automated end-to-end release workflow
- **Smart version detection**: Automatically determines version bump needed
- **Platform detection**: Automatically detects GitHub, GitLab, Bitbucket, or generic git
- **Platform-specific releases**: Creates releases using appropriate CLI (gh, glab, etc.)
- **Documentation sync**: Updates all docs, README, changelog automatically
- **Validation first**: Ensures quality before releasing
- **Auto-commit & push**: Handles all Git operations automatically
- **Multi-platform support**: GitHub, GitLab, Bitbucket, and generic git repositories

## How It Works

The workflow executes 8 MANDATORY steps in sequence:

1. **Analyze Changes**: Reviews all changes since last release
2. **Determine Version**: Auto-detects major/minor/patch based on commits
3. **Update Version Files**: Updates plugin.json, package.json, setup.py, etc.
4. **Sync Documentation**: Updates README, CHANGELOG, RELEASE_NOTES
5. **Validate Consistency**: Cross-checks all files for version consistency
6. **Git Operations**: Commits, tags, and pushes automatically
7. **Create Platform Release**: Detects platform (GitHub/GitLab/Bitbucket) and creates appropriate release
8. **Verify Release**: Confirms release was created successfully on detected platform

## Usage

### Quick Release (Recommended)
```bash
# Fully automated release with smart detection
/autonomous-agent:dev:release

# This will:
# - Analyze changes and determine version bump
# - Update all version files and documentation
# - Validate consistency across all files
# - Run quality checks (must pass ≥ 85/100)
# - Commit, tag, and push to remote
# - Create GitHub release with comprehensive notes (DEFAULT)
# - Optional: Publish to npm, PyPI, Docker (if specified)
```

### Specify Version Type
```bash
# Force specific version bump
/autonomous-agent:dev:release --patch     # Bug fixes only (x.y.Z)
/autonomous-agent:dev:release --minor     # New features (x.Y.0)
/autonomous-agent:dev:release --major     # Breaking changes (X.0.0)

# Specify exact version
/autonomous-agent:dev:release --version 2.5.0
```

### Validation Options
```bash
# Skip quality validation (not recommended)
/autonomous-agent:dev:release --skip-validation

# Set minimum quality threshold (default: 85)
/autonomous-agent:dev:release --quality-threshold 90

# Dry run (preview without making changes)
/autonomous-agent:dev:release --dry-run
```

### Documentation Options
```bash
# Update specific documentation
/autonomous-agent:dev:release --update-changelog
/autonomous-agent:dev:release --update-readme
/autonomous-agent:dev:release --generate-release-notes

# Custom release notes file
/autonomous-agent:dev:release --release-notes ./CUSTOM_NOTES.md
```

### Platform Options
```bash
# GitHub release is now created by DEFAULT
/autonomous-agent:dev:release               # Creates GitHub release automatically

# Additional platforms (optional)
/autonomous-agent:dev:release --npm         # Also publish to npm
/autonomous-agent:dev:release --pypi        # Also publish to PyPI
/autonomous-agent:dev:release --docker      # Build and push Docker image
/autonomous-agent:dev:release --gitlab      # GitLab instead of GitHub

# Multi-platform release
/autonomous-agent:dev:release --npm --docker  # GitHub + npm + Docker
```

### Pre-release Options
```bash
# Create pre-release versions
/autonomous-agent:dev:release --pre-release alpha
/autonomous-agent:dev:release --pre-release beta
/autonomous-agent:dev:release --pre-release rc

# Example: v1.2.3-beta.1
/autonomous-agent:dev:release --minor --pre-release beta
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
+- 🎉 Features: 3 commits
|  +- feat: add /dev-auto command
|  +- feat: add interactive suggestions
|  +- feat: .gitignore management
+- 🐛 Bug Fixes: 2 commits
|  +- fix: validation error handling
|  +- fix: documentation typos
+- 📚 Documentation: 5 commits
+- ♻️  Refactoring: 1 commit
+- [WARN]️  Breaking Changes: None

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

Updating version: v3.3.2 -> v3.4.0

Files Updated:
+- ✅ .claude-plugin/plugin.json
+- ✅ README.md (4 references)
+- ✅ CLAUDE.md (2 references)
+- ✅ package.json
+- ✅ docs/IMPLEMENTATION_SUMMARY.md

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
+- Updated version badge
+- Updated feature list
+- Updated installation instructions

CHANGELOG.md:
+- Generated from commit history
+- Categorized changes:
|  +- Added (3 features)
|  +- Fixed (2 bugs)
|  +- Changed (1 refactor)
|  +- Documentation (5 docs)
+- Release date: 2025-01-24

RELEASE_NOTES.md:
+- Human-readable summary
+- Feature highlights
+- Bug fix details
+- Upgrade instructions

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
+- ✅ All version references match: v3.4.0
+- ✅ No old version numbers found
+- ✅ Version format consistent

Documentation Consistency:
+- ✅ Feature counts match across files
+- ✅ Component counts accurate
+- ✅ All links valid
+- ✅ Examples up-to-date

Structure Consistency:
+- ✅ All agents registered (20)
+- ✅ All skills registered (14)
+- ✅ All commands registered (18)
+- ✅ Plugin.json valid

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
+- ✅ Plugin structure valid
+- ✅ All YAML frontmatter valid
+- ✅ All JSON files valid
+- ✅ No syntax errors

Documentation Quality:
+- ✅ README complete (95/100)
+- ✅ All commands documented
+- ✅ All agents documented
+- ✅ Examples working

Standards Compliance:
+- ✅ Follows plugin guidelines
+- ✅ Naming conventions correct
+- ✅ File structure correct

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
+- ✅ 5 files staged
+- ✅ No unexpected changes

Creating Commit:
+- Message: "release: v3.4.0 - Add /dev-auto and suggestions"
+- Files: 5 modified
+- ✅ Commit created: abc1234

Creating Tag:
+- Tag: v3.4.0
+- Message: "Release v3.4.0"
+- ✅ Tag created

Pushing to Remote:
+- ✅ Pushed to origin/main
+- ✅ Pushed tags

Git Status: ✅ All operations successful
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage 7: GitHub Repository Release (10-20 seconds)
Creates GitHub release with comprehensive release notes:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 GITHUB REPOSITORY RELEASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GitHub Authentication Check:
+- ✅ GitHub CLI authenticated
+- ✅ Repository access verified
+- ✅ Release permissions confirmed

Creating GitHub Release:
+- Version: v3.4.0
+- Title: "Release v3.4.0: [Release Summary]"
+- Release Notes: Generated from changelog
+- Assets: Source code archive
+- ✅ Published: https://github.com/user/repo/releases/tag/v3.4.0

Release Details:
+- Release Type: [MAJOR/MINOR/PATCH]
+- Changes: [Number] commits included
+- Features: [Number] new features
+- Bug Fixes: [Number] bug fixes
+- Quality Score: [Score]/100

GitHub Release Status: ✅ Successfully created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage 8: Optional Platform Publishing (15-30 seconds)
Publishes to additional configured platforms (if specified):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 OPTIONAL PLATFORM PUBLISHING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

npm Publishing:
+- Building package...
+- Running npm publish...
+- ✅ Published: https://npmjs.com/package/autonomous-agent@3.4.0

Docker Publishing:
+- Building image: user/autonomous-agent:3.4.0
+- Pushing to Docker Hub...
+- ✅ Published: docker pull user/autonomous-agent:3.4.0

Optional Release Status: ✅ Selected platforms published
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage 9: Learning Integration (5 seconds)
Stores release pattern for future optimization:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 LEARNING INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pattern Stored:
+- Task Type: release
+- Version Bump: minor (3.3.2 -> 3.4.0)
+- Files Updated: 5
+- Quality Score: 92/100
+- Time Taken: 2m 15s
+- ✅ Stored to .claude-patterns/

Future Improvements:
+- Faster documentation sync (learned shortcuts)
+- Better changelog categorization
+- Optimized validation checks

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
+- 📦 Version updated across 5 files
+- 📚 Documentation synchronized
+- ✅ Validation passed (92/100)
+- 🔧 Git operations successful
+- 🚀 GitHub release created
+- 📦 Optional platforms published (if configured)
+- 🧠 Pattern learned for future

Total Time: 2m 30s

Links:
+- GitHub Release: https://github.com/user/repo/releases/tag/v3.4.0
+- Source Archive: https://github.com/user/repo/archive/refs/tags/v3.4.0.zip
+- npm: https://npmjs.com/package/autonomous-agent@3.4.0 (if published)
+- Docker: docker pull user/autonomous-agent:3.4.0 (if published)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 SUGGESTED NEXT ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Monitor release metrics
   -> /autonomous-agent:learn:performance

2. Announce release to team
   -> Draft announcement with highlights

3. Create next milestone
   -> Plan features for v3.5.2

4. Update project board
   -> Close completed issues

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
/autonomous-agent:validate:fullstack
/autonomous-agent:analyze:quality
/autonomous-agent:dev:release
```

### Post-Release Monitoring
```bash
# Monitor after release
/autonomous-agent:dev:release
/autonomous-agent:learn:performance
/autonomous-agent:learn:analytics
```

### Integrated Workflow
```bash
# Complete development cycle
/autonomous-agent:dev:auto "add new feature"
# ... development happens ...
/autonomous-agent:analyze:quality
/autonomous-agent:dev:release
```

## Platform Requirements

The command automatically detects your repository platform and uses the appropriate CLI tool:

### GitHub Repositories
**Required:**
- **GitHub CLI** (`gh` command) - Install: https://cli.github.com/
- **Authentication**: Run `gh auth login` once
- **Permissions**: Push access and release creation permissions

**Setup:**
```bash
gh auth login
gh auth status
```

### GitLab Repositories
**Required:**
- **GitLab CLI** (`glab` command) - Install: https://gitlab.com/gitlab-org/cli
- **Authentication**: Run `glab auth login` once
- **Permissions**: Push access and release creation permissions

**Setup:**
```bash
glab auth login
glab auth status
```

### Bitbucket Repositories
**No additional CLI required** - Uses git tags only

### Generic Git Repositories
**No additional CLI required** - Uses git tags only

## Troubleshooting

### Platform Release Failed
```bash
# For GitHub
gh auth status
gh repo view
/autonomous-agent:dev:release --retry

# For GitLab
glab auth status
glab repo view
/autonomous-agent:dev:release --retry

# For any platform
git remote -v  # Check remote URL
git tag -l     # List existing tags
```

### Quality Check Failed
```bash
# View detailed quality report
/autonomous-agent:analyze:quality --verbose

# Fix issues and retry
/autonomous-agent:dev:release --retry

# Skip validation (not recommended)
/autonomous-agent:dev:release --skip-validation --force
```

### Version Conflict
```bash
# Reset version detection
/autonomous-agent:dev:release --version 3.4.0 --force

# Manual version update
edit .claude-plugin/plugin.json
/autonomous-agent:dev:release --skip-version-update
```

### Git Operation Failed
```bash
# Check Git status
git status
git log --oneline -5

# Retry with verbose logging
/autonomous-agent:dev:release --verbose --retry
```

### Platform Publishing Failed
```bash
# Check authentication
gh auth status    # GitHub
glab auth status  # GitLab
npm whoami        # npm
docker info       # Docker

# Retry specific platform
/autonomous-agent:dev:release --github --retry
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

**Version**: 1.1.0
**Integration**: Works with version-release-manager agent and git-automation skill
**Platform**: Cross-platform (Windows, Linux, Mac)
**Dependencies**: Git, GitHub CLI (gh) REQUIRED for release creation, GitLab CLI (glab) optional
