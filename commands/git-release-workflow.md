---
name: git-release-workflow
description: "[DEPRECATED] Redirects to dev:release - Use /autonomous-agent:dev:release instead"
delegates-to: autonomous-agent:orchestrator
deprecated: true
redirects-to: dev:release
---

# Git Release Workflow Command [DEPRECATED]

**This command has been deprecated and merged into `/autonomous-agent:dev:release`.**

## Migration Notice

The `/git-release-workflow` command has been consolidated into the `/autonomous-agent:dev:release` command to provide a unified release workflow experience.

### What Changed

- **Old Command**: `/git-release-workflow`
- **New Command**: `/autonomous-agent:dev:release`
- **Status**: This command now redirects to `/autonomous-agent:dev:release`

### Why the Change

As part of the command restructuring to use category-based naming (dev:, analyze:, validate:, etc.), we've consolidated related release workflows into a single, more comprehensive command.

### Migration Guide

Simply replace any usage of `/git-release-workflow` with `/autonomous-agent:dev:release`:

```bash
# Old (deprecated)
/git-release-workflow

# New (recommended)
/autonomous-agent:dev:release
```

All features from `/git-release-workflow` are available in `/autonomous-agent:dev:release`, including:

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
/autonomous-agent:dev:release --help
```

---

**Note**: This redirect file will be maintained for backward compatibility but will be removed in a future major version. Please update your workflows to use `/autonomous-agent:dev:release`.
