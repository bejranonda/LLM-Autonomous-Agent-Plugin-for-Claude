---
name: git-release-workflow
description: "[DEPRECATED] Redirects to dev:release - Use /dev:release instead"
delegates-to: autonomous-agent:orchestrator
deprecated: true
redirects-to: dev:release
---

# Git Release Workflow Command [DEPRECATED]

**This command has been deprecated and merged into `/dev:release`.**

## Migration Notice

The `/git-release-workflow` command has been consolidated into the `/dev:release` command to provide a unified release workflow experience.

### What Changed

- **Old Command**: `/git-release-workflow`
- **New Command**: `/dev:release`
- **Status**: This command now redirects to `/dev:release`

### Why the Change

As part of the command restructuring to use category-based naming (dev:, analyze:, validate:, etc.), we've consolidated related release workflows into a single, more comprehensive command.

### Migration Guide

Simply replace any usage of `/git-release-workflow` with `/dev:release`:

```bash
# Old (deprecated)
/git-release-workflow

# New (recommended)
/dev:release
```

All features from `/git-release-workflow` are available in `/dev:release`, including:

- Automated version detection and bumping
- Release notes generation
- Multi-platform publishing (GitHub, GitLab, npm, PyPI, Docker)
- Quality validation before release
- Automated documentation updates
- Git tagging and pushing

### Full Documentation

See the complete documentation at: `commands/release-dev.md`

Or run:
```bash
/dev:release --help
```

---

**Note**: This redirect file will be maintained for backward compatibility but will be removed in a future major version. Please update your workflows to use `/dev:release`.
