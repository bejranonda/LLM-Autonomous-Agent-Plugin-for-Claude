---
name: dev:commit
description: Intelligent commit management with automatic staging, conventional commits, and learning integration
delegates-to: autonomous-agent:git-repository-manager
---

# Dev-Commit Command

## Command: `/dev:commit`

**Smart commit management** - Analyzes changes, generates intelligent commit messages following conventional commit standards, stages appropriate files, and creates commits with learning integration. Does NOT create releases or tags.

**🔧 Intelligent Commit Features:**
- **Automatic Change Analysis**: Reviews all modified and new files
- **Smart File Staging**: Intelligently stages related files together
- **Conventional Commits**: Generates proper commit messages (feat:, fix:, docs:, etc.)
- **Multi-file Commits**: Groups related changes into logical commits
- **Interactive Mode**: Option to review before committing
- **Learning Integration**: Learns effective commit patterns over time
- **No Release**: Only commits - no tags, no releases, no version bumps

## How It Works

1. **Analyze Changes**: Reviews all uncommitted changes
2. **Categorize Changes**: Groups changes by type (features, fixes, docs, etc.)
3. **Generate Commit Messages**: Creates conventional commit messages
4. **Stage Files**: Intelligently stages files for each commit
5. **Create Commits**: Executes git commit with generated messages
6. **Push (Optional)**: Optionally pushes to remote
7. **Learn**: Stores commit patterns for future improvements

## Usage

### Basic Usage
```bash
# Analyze and commit all changes with smart grouping
/dev:commit

# Commit with custom message
/dev:commit "feat: add new authentication system"

# Commit specific files only
/dev:commit --files "src/auth.py,tests/test_auth.py"
```

### Automatic Commit Message Generation
```bash
# Let the agent analyze and generate appropriate messages
/dev:commit --auto

# Generate message but review before committing
/dev:commit --auto --interactive

# Use conventional commit format
/dev:commit --conventional
```

### Commit Grouping Options
```bash
# Group all changes into single commit
/dev:commit --single

# Create multiple commits grouped by type
/dev:commit --group-by-type

# Create commit per file
/dev:commit --per-file

# Create commit per directory
/dev:commit --per-directory
```

### Push Options
```bash
# Commit and push to remote
/dev:commit --push

# Commit and push to specific branch
/dev:commit --push --branch feature/new-feature

# Commit only (no push) - DEFAULT
/dev:commit --no-push
```

### Advanced Options
```bash
# Include untracked files
/dev:commit --include-untracked

# Exclude specific patterns
/dev:commit --exclude "*.log,*.tmp"

# Verbose output with reasoning
/dev:commit --verbose

# Dry run (show what would be committed)
/dev:commit --dry-run
```

## Output Format

### Terminal Output (Concise)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 COMMIT ANALYSIS COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Analyzed: 12 files
Commit Strategy: Group by type

Proposed Commits:

1. feat: Add 6 new analysis commands
   Files: 6 files in commands/analyze/ and commands/learn/

2. fix: Fix dashboard browser opening issues
   Files: 2 files (lib/dashboard.py, lib/dashboard_launcher.py)

3. docs: Update plugin documentation
   Files: 4 files (README.md, CLAUDE.md, etc.)

Execute commits? [Y/n]: Y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ COMMITS CREATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Commit 1: feat: Add 6 new analysis commands (abc1234)
✓ Commit 2: fix: Fix dashboard browser opening issues (def5678)
✓ Commit 3: docs: Update plugin documentation (ghi9012)

Total: 3 commits created
Pushed: No (use --push to push to remote)

⏱ Completed in 8 seconds
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Commit Message Generation

### Conventional Commit Format

The command automatically detects change types and generates appropriate conventional commit messages:

**Format**: `<type>(<scope>): <description>`

**Types:**
- `feat`: New features or functionality
- `fix`: Bug fixes
- `docs`: Documentation changes only
- `style`: Code style/formatting (no logic changes)
- `refactor`: Code refactoring (no feature/fix)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, configs, etc.)
- `ci`: CI/CD configuration changes
- `build`: Build system changes

**Examples:**
```bash
# Feature additions
feat: add JWT authentication system
feat(auth): implement refresh token mechanism

# Bug fixes
fix: resolve memory leak in data processing
fix(api): correct endpoint parameter validation

# Documentation
docs: update README with new commands
docs(api): add authentication examples

# Refactoring
refactor: simplify authentication logic
refactor(db): optimize query performance

# Tests
test: add integration tests for auth module
test(api): improve endpoint coverage

# Chores
chore: update dependencies to latest versions
chore(deps): bump python-jose to 1.6.1
```

## Smart File Staging

The command intelligently groups files for commits:

### Group by Type (Default)
```
Commit 1: feat: Add new commands
├─ commands/analyze/explain.md
├─ commands/analyze/repository.md
├─ commands/learn/history.md
└─ commands/learn/clone.md

Commit 2: fix: Fix dashboard issues
├─ lib/dashboard.py
└─ lib/dashboard_launcher.py

Commit 3: docs: Update documentation
├─ README.md
├─ CLAUDE.md
└─ CHANGELOG.md
```

### Group by Directory
```
Commit 1: feat: Update analyze commands
└─ commands/analyze/
    ├─ explain.md
    └─ repository.md

Commit 2: feat: Update learn commands
└─ commands/learn/
    ├─ history.md
    └─ clone.md

Commit 3: fix: Update library
└─ lib/
    ├─ dashboard.py
    └─ dashboard_launcher.py
```

### Single Commit
```
Commit 1: chore: Update plugin with multiple improvements
├─ commands/analyze/explain.md
├─ commands/analyze/repository.md
├─ commands/learn/history.md
├─ commands/learn/clone.md
├─ lib/dashboard.py
├─ lib/dashboard_launcher.py
├─ README.md
└─ CLAUDE.md
```

## Change Detection

The command analyzes changes to determine appropriate commit messages:

### Feature Detection
Triggers `feat:` commit when:
- New files in `commands/`, `agents/`, `skills/`
- New function definitions
- New API endpoints
- New classes or modules

### Fix Detection
Triggers `fix:` commit when:
- Bug fix keywords in changes (fix, bug, issue, error)
- Modified error handling
- Modified validation logic
- Corrected typos or logic errors

### Documentation Detection
Triggers `docs:` commit when:
- Only markdown files modified
- Only docstrings modified
- Only comments modified
- README, CHANGELOG, or documentation files

### Refactor Detection
Triggers `refactor:` commit when:
- Code structure changes without logic changes
- Function/class renaming
- Code organization improvements
- Performance optimizations

## Integration with Learning System

The `/dev:commit` command integrates with pattern learning:

**Learning from Commits**:
- Effective commit message patterns
- Optimal file grouping strategies
- Common change type patterns
- Successful commit sizes
- Push timing patterns

**Pattern Storage**:
```json
{
  "commit_patterns": {
    "grouping_strategy": "by_type",
    "avg_commits_per_session": 2.5,
    "avg_files_per_commit": 4.2,
    "effective_message_patterns": [
      "feat: add {feature}",
      "fix: resolve {issue}",
      "docs: update {document}"
    ],
    "success_metrics": {
      "single_commit_clarity": 0.78,
      "grouped_commit_clarity": 0.92,
      "per_file_commit_clarity": 0.65
    },
    "reuse_count": 45,
    "effectiveness_score": 0.91
  }
}
```

**Continuous Improvement**:
- Learn which grouping strategies work best
- Improve commit message quality over time
- Optimize file staging decisions
- Reduce commit fragmentation
- Enhance clarity and traceability

## Interactive Mode

When using `--interactive`, the command shows a review before committing:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 COMMIT REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commit 1 of 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: feat
Message: Add 6 new analysis and learning commands
Description:
  Implements external repository analysis, task explanation,
  commit history learning, feature cloning, and documentation
  updates. Enhances learning capabilities significantly.

Files to be committed:
├─ commands/analyze/explain.md (new, 26 KB)
├─ commands/analyze/repository.md (new, 35 KB)
├─ commands/learn/history.md (new, 24 KB)
├─ commands/learn/clone.md (new, 21 KB)
├─ commands/workspace/update-readme.md (new, 3.7 KB)
└─ commands/workspace/update-about.md (new, 3.9 KB)

Total: 6 files, 113.6 KB

Options:
[c] Commit as shown
[e] Edit commit message
[s] Skip this commit
[m] Modify file selection
[q] Quit without committing

Choice:
```

## Best Practices

### When to Use `/dev:commit`

✅ **Good use cases:**
- During active development (commit frequently)
- After completing a logical unit of work
- Before switching tasks or branches
- After fixing bugs or issues
- When you want smart commit organization

❌ **Don't use for:**
- Creating releases (use `/dev:release` instead)
- Version tagging (use `/dev:release` instead)
- Publishing to package managers (use `/dev:release`)

### Commit Frequency

**Recommended patterns:**
- **Small features**: 1-2 commits
- **Medium features**: 3-5 commits grouped logically
- **Large features**: Multiple commits per logical component
- **Bug fixes**: 1 commit per bug
- **Documentation**: 1 commit per documentation update session

**Avoid:**
- Too many tiny commits (creates noise)
- Giant commits with unrelated changes (hard to review)
- Commits without clear purpose or message

### Commit Message Quality

**Good commit messages:**
```bash
feat: add JWT authentication with refresh tokens
fix: resolve memory leak in background task manager
docs: add comprehensive API documentation with examples
refactor: simplify validation logic using schemas
test: add integration tests for auth workflow
```

**Poor commit messages:**
```bash
update files
fix stuff
changes
wip
asdf
```

## Integration with Other Commands

### Development Workflow
```bash
# Work on feature
/dev:auto "add new feature"

# Commit progress regularly
/dev:commit --auto

# Continue working...
/dev:commit --auto

# When ready to release
/dev:release
```

### Pre-Release Workflow
```bash
# Commit all pending changes
/dev:commit --auto --group-by-type

# Validate quality
/analyze:quality

# Create release
/dev:release
```

### Feature Branch Workflow
```bash
# Create feature branch
git checkout -b feature/new-auth

# Work and commit
/dev:commit --auto

# Push to remote branch
/dev:commit --push --branch feature/new-auth

# Create PR when ready
/dev:pr-review
```

## Troubleshooting

### No Changes to Commit
```bash
# Check git status
git status

# Show what would be committed
/dev:commit --dry-run

# Include untracked files
/dev:commit --include-untracked
```

### Commit Failed
```bash
# Check for conflicts
git status

# Resolve conflicts manually
git add <resolved-files>

# Retry commit
/dev:commit --retry
```

### Wrong Files Staged
```bash
# Unstage all
git reset

# Specify files explicitly
/dev:commit --files "file1.py,file2.py"
```

### Push Failed
```bash
# Check remote status
git remote -v

# Pull first if needed
git pull origin main

# Retry push
/dev:commit --push --retry
```

## Performance Metrics

Expected performance:

| Task | Time | Success Rate |
|------|------|--------------|
| Analyze changes | 2-5s | 100% |
| Generate commit messages | 3-8s | 95% |
| Create single commit | 1-2s | 99% |
| Create multiple commits | 5-15s | 97% |
| Push to remote | 3-10s | 95% |

**Learning improvement:**
- After 10 commits: 20% faster message generation
- After 25 commits: 85% message quality (up from 70%)
- After 50 commits: 92% optimal grouping decisions

## Examples

### Example 1: Auto-commit with smart grouping
```bash
$ /dev:commit --auto

Analyzing changes...
Found: 8 modified files, 4 new files

Proposed commits:
1. feat: Add new authentication commands (6 files)
2. fix: Resolve dashboard rendering issue (2 files)
3. docs: Update README and CHANGELOG (4 files)

Creating commits...
✓ 3 commits created successfully

Total changes committed: 12 files
```

### Example 2: Custom commit with specific files
```bash
$ /dev:commit "feat: implement JWT token validation" --files "src/auth/jwt.py,tests/test_jwt.py"

Staging files...
├─ src/auth/jwt.py
└─ tests/test_jwt.py

Creating commit...
✓ Commit created: feat: implement JWT token validation (abc1234)
```

### Example 3: Interactive review mode
```bash
$ /dev:commit --auto --interactive

[Shows review interface for each proposed commit]

Commit 1: Accept (c)
Commit 2: Edit message (e)
Commit 3: Skip (s)

Result:
✓ 2 commits created
⊘ 1 commit skipped
```

### Example 4: Commit and push
```bash
$ /dev:commit --auto --push

Creating commits...
✓ 3 commits created

Pushing to origin/main...
✓ Pushed successfully

Branch: main
Remote: origin
Commits: 3 new commits
```

---

**Version**: 1.0.0
**Integration**: Uses git-repository-manager agent
**Skills**: git-automation, pattern-learning, code-analysis
**Platform**: Cross-platform (Windows, Linux, Mac)
**Learning**: Full integration with pattern learning system
**Scope**: Commit management only - no releases, tags, or version bumps
