# Git Release Workflow Command

## Command: `/git-release-workflow`

Automated Git release workflow that handles version bumping, changelog generation, release creation, and multi-platform publishing with intelligent semantic versioning and comprehensive validation.

## How It Works

1. **Repository Analysis**: Analyzes current state and changes since last release
2. **Version Detection**: Automatically determines semantic version bump needed
3. **Quality Validation**: Runs comprehensive pre-release validation checks
4. **Release Execution**: Executes complete release workflow with proper Git operations
5. **Multi-Platform Publishing**: Publishes to GitHub, GitLab, package managers, and Docker registries
6. **Documentation Updates**: Updates changelog, version files, and documentation
7. **Post-Release Monitoring**: Sets up monitoring and validation for the new release

## Usage

### Basic Release Workflow
```bash
# Automated release with intelligent version bumping
/git-release-workflow

# Specify version type (overrides automatic detection)
/git-release-workflow --version-type patch
/git-release-workflow --version-type minor
/git-release-workflow --version-type major
/git-release-workflow --version 1.2.3
```

### Advanced Release Options
```bash
# Release with custom options
/git-release-workflow \
  --version-type minor \
  --pre-release-validation \
  --create-github-release \
  --update-documentation \
  --notify-team

# Release with dry run (no actual changes)
/git-release-workflow --dry-run

# Force release (skip validation warnings)
/git-release-workflow --force

# Release with custom release notes
/git-release-workflow --release-notes RELEASE_NOTES.md
```

### Platform-Specific Publishing
```bash
# GitHub-focused release
/git-release-workflow \
  --platform github \
  --create-prerelease \
  --github-discussion

# Multi-platform release
/git-release-workflow \
  --platform github,gitlab \
  --publish-packages \
  --docker-image
```

## Workflow Stages

### Stage 1: Repository Analysis (30-60 seconds)

**Analyzes**:
- Current Git state and branch status
- Changes since last release
- Commit types and impact
- Repository health and quality metrics

**Output**:
```
============================================================
REPOSITORY ANALYSIS
============================================================

📊 Current State:
├─ Current Branch: main ✓
├─ Working Directory: Clean ✓
├─ Last Release: v1.2.0 (2024-01-10)
├─ Commits Since Release: 12
└─ Repository Health: Good (92/100)

📈 Change Analysis:
├─ Features: 3 feat commits detected
├─ Fixes: 4 fix commits detected
├─ Documentation: 2 docs commits detected
├─ Refactoring: 2 refactor commits detected
└─ Breaking Changes: None detected

🎯 Recommended Version Bump: MINOR (v1.2.0 → v1.3.0)
⏱ Analysis completed in 45 seconds
```

### Stage 2: Pre-Release Validation (2-5 minutes)

**Validates**:
- Code quality and standards compliance
- Test execution and coverage
- Security vulnerability scanning
- Documentation completeness
- Dependency health and compatibility

**Output**:
```
============================================================
PRE-RELEASE VALIDATION
============================================================

✅ Code Quality: PASS (95/100)
├─ Linting: No issues found
├─ Style: Standards compliant
└─ Metrics: Within acceptable ranges

✅ Test Suite: PASS (98% coverage)
├─ Unit Tests: 245/248 passing
├─ Integration Tests: 32/32 passing
├─ E2E Tests: 15/15 passing
└─ Coverage Threshold: 70% required, 98% achieved

✅ Security Scan: PASS
├─ Vulnerabilities: 0 high, 0 medium, 2 low
├─ Dependencies: All up to date
└─ Sensitive Data: None detected

✅ Documentation: PASS (88/100)
├─ README: Up to date ✓
├─ API Docs: Complete ✓
├─ CHANGELOG: Generated ✓
└─ Version References: Consistent ✓

🎯 Validation Score: 94/100 (Ready for Release)
⏱ Validation completed in 3.2 minutes
```

### Stage 3: Release Execution (1-2 minutes)

**Executes**:
- Version bump in all relevant files
- Changelog generation and updates
- Git operations (branch, commit, tag)
- Release creation on platforms
- Package publishing and deployment

**Output**:
```
============================================================
RELEASE EXECUTION
============================================================

📦 Version Update: v1.2.0 → v1.3.0
├─ package.json: Updated ✓
├─ setup.py: Updated ✓
├─ CHANGELOG.md: Generated ✓
├─ README.md: Updated ✓
└─ Version files: 3 files updated

🔧 Git Operations:
├─ Release Branch: release/v1.3.0 created ✓
├─ Version Commit: chore(release): v1.3.0 ✓
├─ Tag Created: v1.3.0 ✓
├─ Main Branch Merge: Completed ✓
└─ Push to Origin: Completed ✓

🚀 Platform Publishing:
├─ GitHub Release: Created ✓
├─ Package Registry: Published ✓
├─ Docker Image: Pushed ✓
└─ Documentation: Updated ✓

🎯 Release Status: SUCCESS
📄 Release Notes: https://github.com/user/repo/releases/tag/v1.3.0
⏱ Release completed in 1.8 minutes
```

### Stage 4: Post-Release Monitoring (Ongoing)

**Monitors**:
- Download statistics and installation metrics
- Issue reports and user feedback
- Performance metrics and error rates
- Documentation engagement and usage

**Output**:
```
============================================================
POST-RELEASE MONITORING
============================================================

📊 Release Metrics (First 24 Hours):
├─ Downloads: 1,247 (+15% from v1.2.0)
├─ Installs: 892
├─ GitHub Stars: +12
├─ Issues Reported: 0
└─ Performance Score: 96/100

🔔 Monitoring Setup:
├─ Download Analytics: Active ✓
├─ Error Tracking: Active ✓
├─ Performance Monitoring: Active ✓
└─ User Feedback Collection: Active ✓

📈 Next Release Forecast:
├─ Estimated Date: 2024-01-24 (2 weeks)
├─ Planned Features: 3 in progress
├─ Known Issues: 0 critical, 1 minor
└─ Dependency Updates: 2 available

🎯 Release v1.3.0: HEALTHY
```

## Command Line Options

### Version Options
```bash
--version-type <type>     # Override automatic version detection
                           # Values: major, minor, patch, auto (default)

--version <version>       # Specify exact version (e.g., 1.2.3)

--pre-release             # Mark as pre-release (alpha, beta, rc)

--build-metadata <meta>   # Add build metadata (e.g., +build.123)
```

### Validation Options
```bash
--skip-validation         # Skip pre-release validation (not recommended)

--validation-level <level> # Set validation thoroughness
                           # Values: quick, standard (default), thorough

--quality-threshold <score> # Minimum quality score to proceed
                            # Default: 70

--require-tests           # Require passing tests before release
```

### Platform Options
```bash
--platform <platforms>    # Target platforms for publishing
                           # Values: github, gitlab, npm, pypi, docker
                           # Default: github

--create-github-release   # Create GitHub release with notes

--github-discussion       # Create GitHub discussion for release

--publish-packages        # Publish to package managers

--docker-image            # Build and push Docker image
```

### Documentation Options
```bash
--update-documentation    # Update all documentation files

--generate-changelog      # Generate comprehensive changelog

--release-notes <file>    # Use custom release notes file

--update-api-docs         # Update API documentation

--create-migration-guide  # Create migration guide for breaking changes
```

### Control Options
```bash
--dry-run                # Simulate release without making changes

--force                  # Force release despite warnings

--interactive            # Interactive mode with confirmation prompts

--verbose                # Detailed output logging

--quiet                  # Minimal output (summary only)

--no-push               # Skip pushing to remote repository
```

## Advanced Features

### Intelligent Version Detection

**Automatic Version Bump Logic**:
```bash
# Breaking changes detected → MAJOR
if [[ $(git log --oneline $range | grep -c "BREAKING\|breaking") -gt 0 ]]; then
    version_bump="major"

# New features detected → MINOR
elif [[ $(git log --oneline $range | grep -c "feat:") -gt 0 ]]; then
    version_bump="minor"

# Bug fixes and improvements only → PATCH
else
    version_bump="patch"
fi
```

**Version File Detection**:
- package.json (Node.js/npm)
- setup.py or pyproject.toml (Python)
- Cargo.toml (Rust)
- composer.json (PHP)
- pom.xml (Maven/Java)
- __init__.py or version.py (Python)

### Multi-Platform Publishing

**GitHub Release Creation**:
```bash
gh release create "v$version" \
  --title "Release v$version" \
  --notes "$(cat RELEASE_NOTES.md)" \
  --latest
```

**Package Publishing**:
```bash
# npm
npm publish

# PyPI
twine upload dist/*

# Docker
docker build -t username/project:$version .
docker push username/project:$version
```

### Automated Changelog Generation

**Smart Chelog Logic**:
```markdown
## [$version] - $date

### Added
- Feature implemented from #123
- Additional functionality #124

### Changed
- Improved performance #125
- Updated dependencies #126

### Deprecated
- Old feature will be removed in v2.0 #127

### Removed
- Removed deprecated feature #128

### Fixed
- Critical bug fix #129
- Minor bug fix #130

### Security
- Security vulnerability patch #131
```

### Release Validation Checks

**Comprehensive Validation**:
- **Code Quality**: Linting, formatting, static analysis
- **Test Coverage**: Unit, integration, E2E tests
- **Security**: Vulnerability scanning, dependency checks
- **Documentation**: Completeness, accuracy, consistency
- **Performance**: Load testing, benchmarking
- **Compatibility**: Cross-platform, version compatibility

## Integration with Other Commands

### With `/validate-fullstack`
```bash
# Run full-stack validation before release
/validate-fullstack
/git-release-workflow --validation-level thorough
```

### With `/quality-check`
```bash
# Ensure quality before release
/quality-check
/git-release-workflow --quality-threshold 90
```

### With `/auto-analyze`
```bash
# Analyze project before deciding on release
/auto-analyze
/git-release-workflow --interactive
```

## Best Practices

### Pre-Release Checklist
- [ ] All tests passing with adequate coverage
- [ ] No critical security vulnerabilities
- [ ] Documentation up to date
- [ ] CHANGELOG generated and reviewed
- [ ] Release notes prepared
- [ ] Dependencies updated and secure
- [ ] Performance benchmarks met
- [ ] Cross-platform compatibility verified

### Release Frequency Guidelines
- **Major Releases**: Every 3-6 months for significant features
- **Minor Releases**: Every 2-4 weeks for new features
- **Patch Releases**: As needed for bug fixes and security updates
- **Pre-Releases**: 1-2 weeks before major releases for testing

### Team Communication
- **Release Announcement**: Notify team before release
- **Release Notes**: Share highlights and changes
- **Post-Mortem**: Review release process and outcomes
- **Feedback Collection**: Gather user feedback after release

## Troubleshooting

### Common Issues

**Validation Failures**:
```bash
# Check specific validation results
/git-release-workflow --validation-level thorough --verbose

# Bypass validation (not recommended)
/git-release-workflow --skip-validation --force
```

**Git Conflicts**:
```bash
# Resolve conflicts before release
git status
git merge --abort  # if needed
/git-release-workflow --interactive
```

**Platform Publishing Issues**:
```bash
# Check platform authentication
gh auth status
npm whoami
docker info

# Retry specific platforms
/git-release-workflow --platform github --retry
```

### Recovery Procedures

**Failed Release Rollback**:
```bash
# Tag deletion
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3

# Branch reset
git reset --hard HEAD~1
git push --force-with-lease origin main

# Package unpublish (if needed)
npm unpublish username@package@1.2.3
```

**Hotfix Release**:
```bash
/git-release-workflow \
  --version-type patch \
  --branch hotfix/critical-issue \
  --skip-validation \
  --create-github-release
```

## Integration with Learning System

The Git Release Workflow command learns from each release to improve future workflows:

**Pattern Learning**:
- Optimal release timing based on team availability
- Common validation issues and prevention strategies
- Successful release communication patterns
- Platform-specific optimization opportunities

**Continuous Improvement**:
- Streamline validation based on project characteristics
- Optimize release timing for maximum impact
- Improve changelog generation quality
- Enhance error detection and prevention

---

**Version**: 1.0.0
**Platform**: Cross-platform (Windows, Linux, Mac)
**Dependencies**: Git, GitHub CLI (gh), npm/pip as needed
**Integration**: Works with all validation and quality commands