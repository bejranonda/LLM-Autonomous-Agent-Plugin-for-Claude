---
name: workspace:organize
description: Automatically organize workspace files, consolidate reports, and validate links

delegates-to: orchestrator

# Command: `/workspace:organize`

Automatically organizes your workspace by moving files to appropriate directories, consolidating scattered reports, and fixing broken links. Improves project hygiene and maintains professional structure.

## Purpose

- Move misplaced files to their proper directories
- Consolidate scattered reports into organized structure
- Validate and fix documentation links
- Maintain clean workspace for better productivity
- Track workspace health over time

## What It Does

### 1. **Report File Organization** (15-30 seconds)
- Move `*.md` reports from root → `docs/reports/generated/`
- Consolidate `.reports*` directories into single location
- Archive reports older than 30 days to `docs/reports/archive/`
- Create/update `docs/reports/README.md` index

### 2. **Python Utility Organization** (10-20 seconds)
- Move standalone Python scripts from root to `lib/`
- Validate scripts still function after move
- Check for import dependencies that need updating
- Create `lib/README.md` if missing

### 3. **Pattern Storage Consolidation** (10-15 seconds)
- Migrate any `patterns/` directories to `.claude-patterns/`
- Validate pattern JSON format consistency
- Remove old pattern locations if empty
- Ensure `.claude-patterns/.gitignore` exists

### 4. **Link Validation & Fixing** (20-40 seconds)
- Scan all `.md` files for internal links
- Identify broken links to moved files
- Update relative paths to new locations
- Generate link validation report

### 5. **Gitignore Management** (5-10 seconds)
- Check for `.gitignore` entries for organized directories
- Add entries for `.claude/`, `.claude-patterns/`, `docs/reports/generated/`
- Prompt if major changes should be gitignored

### 6. **Workspace Health Report** (5-10 seconds)
- Calculate before/after workspace health score
- Show files organized and links fixed
- Provide recommendations for further improvement

## Usage

```bash
# Basic workspace organization
/organize-workspace

# Dry run to see what would be moved
/organize-workspace --dry-run

# Include archive cleanup (remove reports > 90 days)
/organize-workspace --cleanup

# Skip link validation for faster execution
/organize-workspace --no-validate-links
```

## Output

### Terminal Summary (concise)
```
Workspace Organization Complete
├─ Health Score: 78/100 → 92/100 ✅ (+14)
├─ Files Organized: 7 files moved
├─ Links Fixed: 3 links updated
├─ Reports Archived: 2 files
└─ Duration: 1m 23s

📄 Detailed report: .claude/reports/organize-workspace-2025-01-15.md
```

### Detailed Report (file)
- Complete list of files moved with source/destination
- All links that were updated
- Any broken links that need manual attention
- Workspace health scoring breakdown
- Recommendations for maintaining organization

## Directory Structure After Organization

```
project/
├── docs/
│   └── reports/
│       ├── README.md           # Report index
│       ├── generated/          # Auto-generated reports
│       └── archive/            # Old reports (>30 days)
├── lib/                        # Python utilities
│   └── README.md               # Utility documentation
├── .claude-patterns/           # Learning patterns
├── .claude/                    # Claude Code data
└── [other project files]
```

## Integration

The `/organize-workspace` command integrates with:

- **workspace-organizer agent**: Handles the actual file operations
- **validation-standards skill**: Ensures links are properly validated
- **orchestrator**: Suggests organization when workspace health < 70

## Safety Features

- **Dry Run Mode**: Preview changes before executing
- **Backup Creation**: Creates `.claude/backup/` before major moves
- **Selective Execution**: Can skip specific organization steps
- **Rollback Support**: Can undo last organization if needed

## Examples

### Example 1: Basic Organization
```bash
User: /organize-workspace

System: Moved 3 reports to docs/reports/generated/
        Fixed 2 broken links in README.md
        Health score improved: 65/100 → 85/100
```

### Example 2: With Cleanup
```bash
User: /organize-workspace --cleanup

System: Archived 5 old reports (>90 days)
        Consolidated 2 .reports directories
        Created docs/reports/README.md index
```

## When to Use

Run `/organize-workspace` when:
- Root directory has many report files
- Multiple `.reports*` directories exist
- Documentation links are broken
- Workspace health score is below 70
- Before major releases or code reviews

## Automation

The orchestrator can automatically suggest `/organize-workspace` when:
- Workspace health drops below 70/100
- More than 5 report files in root directory
- Broken links detected in documentation

## Notes

- Always creates backup before major file moves
- Preserves file history and timestamps
- Updates all internal documentation links
- Respects existing `.gitignore` entries
- Works with any project structure

## Best Practices

1. **Run before releases**: Clean workspace for professional presentation
2. **Check after analysis**: Analysis commands often generate reports
3. **Regular maintenance**: Run monthly to prevent accumulation
4. **Review changes**: Check the detailed report after organization
5. **Update team**: Inform team members about new file locations

## Related Commands

- `/validate-patterns` - Validate pattern learning consistency
- `/quality-check` - Run after organization to ensure quality
- `/learn-patterns` - Initialize pattern learning system

## See Also

- [Workspace Organization Guide](../docs/guidelines/WORKSPACE_ORGANIZATION.md)
- [Link Validation Standards](../skills/validation-standards/SKILL.md)
- [Workspace-Organizer Agent](../agents/workspace-organizer.md)
---
