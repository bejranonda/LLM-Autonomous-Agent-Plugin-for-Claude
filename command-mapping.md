# Command File Renaming Mapping

## Hyphen to Colon Conversion

This document shows the mapping from current hyphen-separated filenames to new colon-separated filenames.

## Files to Rename

| Current Filename | New Name in Content | Target Directory | New File Path |
|-----------------|-------------------|------------------|---------------|
| auto-analyze.md | analyze:project | analyze/ | analyze/project.md |
| dev-auto.md | dev:auto | dev/ | dev/auto.md |
| dev-model-switch.md | dev:model-switch | dev/ | dev/model-switch.md |
| eval-debug.md | debug:eval | debug/ | debug/eval.md |
| git-release-workflow.md | git-release-workflow | [keep root] | git-release-workflow.md (special case) |
| gui-debug.md | debug:gui | debug/ | debug/gui.md |
| improve-plugin.md | workspace:improve | workspace/ | workspace/improve.md |
| learning-analytics.md | learn:analytics | learn/ | learn/analytics.md |
| learn-patterns.md | learn:init | learn/ | learn/init.md |
| organize-reports.md | workspace:reports | workspace/ | workspace/reports.md |
| organize-workspace.md | workspace:organize | workspace/ | workspace/organize.md |
| performance-report.md | learn:performance | learn/ | learn/performance.md |
| predictive-analytics.md | learn:predict | learn/ | learn/predict.md |
| pr-review.md | dev:pr-review | dev/ | dev/pr-review.md |
| quality-check.md | analyze:quality | analyze/ | analyze/quality.md |
| recommend.md | monitor:recommend | monitor/ | monitor/recommend.md |
| release-dev.md | dev:release | dev/ | dev/release.md |
| scan-dependencies.md | analyze:dependencies | analyze/ | analyze/dependencies.md |
| static-analysis.md | analyze:static | analyze/ | analyze/static.md |
| validate.md | validate:all | validate/ | validate/all.md |
| validate-claude-plugin.md | validate:plugin | validate/ | validate/plugin.md |
| validate-fullstack.md | validate:fullstack | validate/ | validate/fullstack.md |
| validate-patterns.md | validate:patterns | validate/ | validate/patterns.md |

## Directory Structure After Renaming

```
commands/
├── analyze/
│   ├── project.md        (from auto-analyze.md)
│   ├── quality.md       (from quality-check.md)
│   ├── dependencies.md  (from scan-dependencies.md)
│   └── static.md        (from static-analysis.md)
├── debug/
│   ├── eval.md          (from eval-debug.md)
│   └── gui.md          (from gui-debug.md)
├── dev/
│   ├── auto.md          (from dev-auto.md)
│   ├── model-switch.md  (from dev-model-switch.md)
│   ├── pr-review.md     (from pr-review.md)
│   └── release.md       (from release-dev.md)
├── learn/
│   ├── analytics.md     (from learning-analytics.md)
│   ├── init.md          (from learn-patterns.md)
│   ├── performance.md   (from performance-report.md)
│   └── predict.md       (from predictive-analytics.md)
├── monitor/
│   └── recommend.md     (from recommend.md)
├── validate/
│   ├── all.md           (from validate.md)
│   ├── plugin.md        (from validate-claude-plugin.md)
│   ├── fullstack.md     (from validate-fullstack.md)
│   └── patterns.md      (from validate-patterns.md)
├── workspace/
│   ├── improve.md       (from improve-plugin.md)
│   ├── reports.md       (from organize-reports.md)
│   └── organize.md      (from organize-workspace.md)
└── git-release-workflow.md (unchanged - special case)
```

## Special Cases

1. **git-release-workflow.md**: This command doesn't follow the pattern and has no colon in its name field. It will stay in the root.
2. **File content already correct**: All files already have the correct colon notation in their YAML frontmatter and content.

## Implementation Plan

1. Create/move files to appropriate subdirectories
2. Verify content is already correct (it should be)
3. Update cross-references in documentation
4. Update plugin.json description
5. Test discovery works properly

## Benefits

- Commands become discoverable via colon notation (category:command)
- Better organization by functional categories
- Follows Claude Code's expected command structure
- Fixes user issue with commands not being found