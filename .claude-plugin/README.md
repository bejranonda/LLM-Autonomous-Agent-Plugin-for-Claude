# Plugin Manifest Schema

## Current Status

The plugin manifest has been simplified to work with Claude Code's plugin system. The manifest only includes basic metadata:

- `name`: Plugin identifier
- `version`: Current version
- `description`: Brief description
- `author`: Author information
- `repository`: Source code repository
- `license`: License type
- `homepage`: Project homepage
- `keywords`: Searchable keywords

## Removed Fields

The following fields were removed as they are not supported by Claude Code's plugin manifest schema:

- `model_compatibility`: Model-specific configurations
- `adaptive_features`: Feature toggles
- `components`: Agent, skill, and command definitions

## Plugin Structure

While the manifest only contains metadata, the plugin still maintains its full structure in the file system:

```
autonomous-agent/
├── .claude-plugin/
│   └── plugin.json          # Simplified manifest
├── agents/                  # 16 specialized agents
├── skills/                  # 11 skill packages
├── commands/                # 10 slash commands
├── patterns/                # Auto-fix patterns
└── lib/                     # Python utilities
```

## Loading Behavior

Claude Code automatically discovers:
- Agents from `agents/*.md` files
- Skills from `skills/*/SKILL.md` files
- Commands from `commands/*.md` files

The plugin works through Claude Code's conventions-based discovery rather than explicit component registration.