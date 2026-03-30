---
name: plugin-validation
description: "Validates plugin manifest (plugin.json), directory structure, YAML frontmatter, file encoding, and cross-platform compatibility before release. Use when preparing a plugin for distribution, debugging installation failures, or checking version compatibility after structural changes."
---

# Plugin Validation

Validates plugin packages against official development guidelines to prevent installation failures. Checks manifest fields, directory layout, YAML frontmatter syntax, UTF-8 encoding, and cross-platform path compatibility.

## Claude Code Plugin Guidelines Validation

### 1. Plugin Manifest (plugin.json) Validation

**Critical Requirements**:
- **Required Fields**: `name`, `version`, `description`, `author`
- **Valid JSON Syntax**: Must pass JSON parsing without errors
- **Semantic Versioning**: Use `x.y.z` format (no pre-release identifiers)
- **Version Consistency**: Must match version references in documentation
- **Character Encoding**: UTF-8 encoding required
- **File Size**: Under 1MB recommended for performance

**Validation Checks**:
```json
{
  "required_fields": ["name", "version", "description", "author"],
  "optional_fields": ["repository", "license", "homepage", "keywords"],
  "version_pattern": "^\\d+\\.\\d+\\.\\d+$",
  "max_file_size": 1048576,
  "encoding": "utf-8"
}
```

**Common Issues that Cause Installation Failures**:
- Missing required fields
- Invalid JSON syntax (trailing commas, unescaped characters)
- Incorrect version format
- Special characters in description without proper escaping
- File encoding issues

### 2. Directory Structure Validation

**Required Structure**:
```
plugin-root/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (REQUIRED)
├── agents/                  # Agent definitions (optional)
├── skills/                  # Skill definitions (optional)
├── commands/                # Command definitions (optional)
└── lib/                    # Python utilities (optional)
```

**Validation Rules**:
- `.claude-plugin/plugin.json` must exist and be valid JSON
- Directory names must match plugin system conventions
- Files must use `.md` extension for agents/skills/commands
- No circular directory references
- Proper case sensitivity handling

### 3. File Format Compliance

**Agent Files (agents/*.md)**:
```yaml
---
name: agent-name
description: When to invoke this agent (action-oriented)
tools: Read,Write,Edit,Bash,Grep,Glob  # optional
model: inherit  # optional
---

# Agent Title

Core responsibilities...

## Skills Integration
Reference skills by name...

## Approach
Detailed instructions...

## Handoff Protocol
How to return results...
```

**Skill Files (skills/*/SKILL.md)**:
```yaml
---
name: Skill Name
description: What this skill provides (200 char max)
version: 1.0.0
---

## Overview
What, when, and why...

## Domain-Specific Sections
2-5 sections with guidelines, examples, standards...

## When to Apply
Trigger conditions...
```

**Command Files (commands/*.md)**:
- Should not start with dot (.)
- Must contain usage examples
- Should include `## Usage` section
- Must be valid Markdown

### 4. YAML Frontmatter Validation

**Required YAML Structure**:
```yaml
---
name: string           # Required for agents/skills
description: string    # Required for agents/skills
version: string       # Required for skills
tools: array          # Optional for agents
model: string         # Optional for agents
---
```

**YAML Validation Rules**:
- Valid YAML syntax (no tabs for indentation)
- Proper string escaping
- No duplicate keys
- Valid data types (string, array, etc.)
- UTF-8 encoding

### 5. Cross-Platform Compatibility

**File Path Handling**:
- Use forward slashes in documentation
- Handle Windows path separators (\\) in scripts
- Case sensitivity considerations
- Maximum path length (260 chars Windows, 4096 Linux/Mac)

**Character Encoding**:
- All files must be UTF-8 encoded
- No BOM (Byte Order Mark)
- Proper Unicode handling in JSON
- Escape special characters correctly

**Line Ending Compatibility**:
- Git configuration: `git config --global core.autocrlf false`
- Use LF line endings in source files
- Batch scripts: CRLF endings required
- Shell scripts: LF endings required

### 6. Plugin Dependency Validation

**External Dependencies**:
- List all Python dependencies in requirements
- Validate package availability and versions
- Check for conflicting dependencies
- Ensure cross-platform package availability

**Claude Code Compatibility**:
- Check for deprecated Claude Code features
- Validate agent tool usage
- Ensure skill loading compatibility
- Verify command naming conventions

### 7. Installation Failure Prevention

**Pre-Installation Validation**:
```bash
# Validate plugin before distribution
python -c "
import json
import os

# Check plugin manifest
try:
    with open('.claude-plugin/plugin.json', 'r') as f:
        manifest = json.load(f)
    required = ['name', 'version', 'description', 'author']
    missing = [field for field in required if field not in manifest]
    if missing:
        print(f'Missing required fields: {missing}')
        exit(1)
    print('✅ Plugin manifest valid')
except Exception as e:
    print(f'❌ Plugin manifest error: {e}')
    exit(1)

# Check file encoding
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(('.json', '.md', '.py')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    f.read()
            except UnicodeDecodeError:
                print(f'❌ Invalid encoding: {filepath}')
                exit(1)
print('✅ File encoding valid')
"
```

**Common Installation Failure Causes**:
1. **JSON Syntax Errors**: Trailing commas, unescaped quotes
2. **Missing Required Fields**: name, version, description, author
3. **Invalid Version Format**: Using semantic versioning incorrectly
4. **File Encoding Issues**: Non-UTF-8 encoded files
5. **Path Length Issues**: Exceeding system path limits
6. **Permission Problems**: Incorrect file permissions
7. **Case Sensitivity**: Mismatched file/directory names

### 8. Version Compatibility Matrix

**Claude Code Version Compatibility**:
| Plugin Version | Claude Code Support | Notes |
|---------------|-------------------|-------|
| 2.1.0+ | Latest | ✅ Full compatibility |
| 2.0.x | 2024-11+ | ✅ Compatible with auto-fix |
| 1.x.x | Pre-2024-11 | ⚠️ Limited features |

**Plugin Breaking Changes**:
- Manifest schema changes
- Agent tool requirement changes
- Skill loading modifications
- Command naming updates

### 9. Quality Assurance Checklist

**Pre-Release Validation**:
- [ ] Plugin manifest validates with JSON schema
- [ ] All required fields present and valid
- [ ] YAML frontmatter validates in all .md files
- [ ] File encoding is UTF-8 throughout
- [ ] Directory structure follows conventions
- [ ] Version numbers are consistent
- [ ] No broken file references
- [ ] Cross-platform path handling
- [ ] Installation test on clean environment
- [ ] Documentation accuracy verification

**Automated Validation Script**:
```python
# Full plugin validation
def validate_plugin(plugin_dir="."):
    issues = []

    # 1. Manifest validation
    manifest_path = os.path.join(plugin_dir, ".claude-plugin", "plugin.json")
    if not validate_manifest(manifest_path):
        issues.append("Invalid plugin manifest")

    # 2. Directory structure
    if not validate_structure(plugin_dir):
        issues.append("Invalid directory structure")

    # 3. File format validation
    if not validate_file_formats(plugin_dir):
        issues.append("File format issues found")

    # 4. Encoding validation
    if not validate_encoding(plugin_dir):
        issues.append("File encoding issues found")

    return issues

# Usage
issues = validate_plugin()
if issues:
    print("Validation failed:")
    for issue in issues:
        print(f"  ❌ {issue}")
    exit(1)
else:
    print("✅ Plugin validation passed")
```

### 10. Troubleshooting Installation Failures

**Debug Steps**:
1. **Check Plugin Manifest**:
   ```bash
   python -m json.tool .claude-plugin/plugin.json
   ```

2. **Validate File Encoding**:
   ```bash
   find . -type f -name "*.md" -exec file {} \;
   ```

3. **Check Directory Structure**:
   ```bash
   tree .claude-plugin/ agents/ skills/ commands/
   ```

4. **Test Installation**:
   ```bash
   # Test in clean directory
   mkdir test-plugin && cp -r . test-plugin/
   cd test-plugin
   # Try installation here
   ```

**Common Error Solutions**:
- **"Plugin failed to load"**: Check JSON syntax and required fields
- **"Agent not found"**: Verify agent file naming and structure
- **"Skill loading failed"**: Check YAML frontmatter syntax
- **"Command not available"**: Verify command file format

## Validation Workflow

1. **Manifest** → `python -m json.tool .claude-plugin/plugin.json` — verify JSON syntax and required fields
2. **Structure** → verify `.claude-plugin/`, `agents/`, `skills/`, `commands/` directories exist with correct naming
3. **Content** → parse YAML frontmatter in all `.md` files, validate required fields
4. **Encoding** → confirm all `.json`, `.md`, `.py` files are valid UTF-8
5. **Compatibility** → check for deprecated features and cross-platform path issues

**Error severity**: Critical (blocks install) → Warning (non-blocking) → Info (optimization suggestions).

Complements `lib/plugin_validator.py` with plugin-system-specific rules, installation failure prevention, and version compatibility checking.