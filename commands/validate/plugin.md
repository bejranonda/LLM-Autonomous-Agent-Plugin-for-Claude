---
name: validate:plugin
description: Validate Claude Code plugin against official guidelines
delegates-to: autonomous-agent:orchestrator
---

# Validate Claude Plugin

Comprehensive validation for Claude Code plugins against official development guidelines to prevent installation failures and ensure marketplace compatibility.

## Command: `/validate:plugin`

Validates the current plugin against Claude Code official guidelines, checking for common installation failures, compatibility issues, and marketplace requirements.

## How It Works

1. **Plugin Manifest Validation**: Validates .claude-plugin/plugin.json against Claude Code schema requirements
2. **Directory Structure Check**: Ensures proper plugin directory layout and required files
3. **File Format Compliance**: Validates Markdown files with YAML frontmatter
4. **Command Execution Validation**: Checks agent delegation and command-to-agent mappings
5. **Installation Readiness**: Checks for common installation blockers
6. **Cross-Platform Compatibility**: Validates plugin works on Windows, Linux, and Mac

### Command Execution Validation Details

The validator now checks for command execution issues that cause runtime failures:

**Agent Delegation Validation**:
- Verifies all command frontmatter includes proper `delegates-to` field
- Validates referenced agents exist in the `agents/` directory
- Checks agent identifiers use correct prefix format (`autonomous-agent:name`)
- Ensures command documentation matches delegation targets

**Common Command Execution Failures Detected**:
- Missing `delegates-to` field in command YAML frontmatter
- Agent names without `autonomous-agent:` prefix
- References to non-existent agent files
- Mismatched delegation between documentation and frontmatter

## Validation Criteria

### Critical Issues (Installation Blockers)
- Missing or invalid plugin.json manifest
- Invalid JSON syntax in manifest
- Missing required fields (name, version, description, author)
- Invalid version format (must be x.y.z semantic versioning)
- Non-UTF-8 file encoding
- Missing .claude-plugin directory

### Command Execution Issues (Runtime Failures)
- Invalid agent delegation references in commands
- Missing or incorrect agent identifiers
- Commands that reference non-existent agents
- Broken command-to-agent mappings
- Missing `delegates-to` field in command frontmatter

### Warnings (Non-Critical)
- Long file paths (Windows limit 260 characters)
- Missing optional YAML frontmatter fields
- Inconsistent line endings
- Very long or short descriptions
- Agent names without proper prefixes in documentation

### Quality Score
- **100**: Perfect - No issues found
- **90-99**: Ready - Minor warnings only
- **70-89**: Usable - Some fixes recommended
- **< 70**: Needs fixes before release

## Usage

### Quick Validation
```bash
/validate:plugin
```

### Strict Validation (treat warnings as errors)
```bash
/validate:plugin --strict
```

### Validate Specific Plugin Directory
```bash
/validate:plugin --dir /path/to/plugin
```

## Expected Output

### Successful Validation (Perfect)
```
============================================================
VALIDATE CLAUDE PLUGIN RESULTS
============================================================

[+] Plugin Validation PASSED - Ready for Release!

Validation Summary:
+- Plugin Manifest: [OK] Valid JSON schema
+- Directory Structure: [OK] Compliant layout
+- File Formats: [OK] Valid Markdown/YAML
+- Installation Readiness: [OK] No blockers
+- Cross-Platform Compatibility: [OK] Ready for all platforms

Quality Score: 100/100 (Perfect)
Detailed report: .claude/reports/validate-claude-plugin-2025-10-23.md
Completed in 1.2 minutes

[+] Assessment stored in pattern database for dashboard monitoring
[+] Plugin is fully compliant with Claude Code guidelines
    Ready for immediate distribution and installation
```

### Issues Found
```
============================================================
VALIDATE CLAUDE PLUGIN RESULTS
============================================================

[WARN]️  Plugin Validation Issues Found

📊 Validation Summary:
+- Plugin Manifest: ❌ 2 critical issues
+- Directory Structure: ✅ Compliant layout
+- File Formats: [WARN]️ 3 warnings
+- Installation Readiness: ❌ 2 blockers
+- Cross-Platform Compatibility: ✅ Ready for all platforms

🚨 Critical Issues (Installation Blockers):
* Missing required field: version
* Invalid JSON syntax: trailing comma in plugin.json
* File encoding error: agents/orchestrator.md (not UTF-8)

[WARN]️ Command Execution Issues (Runtime Failures):
* Invalid agent delegation: commands/quality-check.md references 'orchestrator' (should be 'autonomous-agent:orchestrator')
* Missing delegates-to field: commands/auto-analyze.md lacks agent delegation specification
* Non-existent agent: commands/example.md references 'missing-agent' (file not found)

[WARN]️  Warnings:
* YAML frontmatter missing in 2 agent files
* Long file paths (Windows limit): 3 files
* Description too short (< 10 chars)

🔧 Auto-Fix Available:
* JSON syntax errors: Can be automatically corrected
* Missing required fields: Can be added with defaults
* File encoding: Can be converted to UTF-8
* Agent delegation errors: Can auto-correct prefixes and add missing fields

🛠️ Command Execution Fixes Applied:
* Fixed commands/quality-check.md: Added `delegates-to: autonomous-agent:orchestrator`
* Auto-corrected agent identifier: `orchestrator` -> `autonomous-agent:orchestrator`
* Updated command documentation: Explicit agent references with proper prefixes

🎯 Quality Score: 65/100 (Needs Fixes)

💡 Recommendations:
1. [HIGH] Fix JSON syntax in plugin.json
2. [HIGH] Add missing version field (use semantic versioning)
3. [HIGH] Convert files to UTF-8 encoding
4. [MED] Add missing YAML frontmatter to agents
5. [LOW] Reduce file path lengths

📄 Detailed report: .claude/reports/validate-claude-plugin-2025-10-23.md
⏱ Completed in 1.5 minutes

❌ Plugin needs fixes before release
   Run recommended fixes and re-validate
```

## Files Created

The validation command creates detailed reports in:

1. **Console Output**: Concise summary with key findings
2. **Detailed Report**: `.claude/reports/validate-claude-plugin-YYYY-MM-DD.md`
3. **JSON Report**: Machine-readable validation results

## Integration with Development Workflow

### Pre-Release Checklist
```bash
# Required validation before any release
/validate:plugin --strict

# Only proceed if validation passes
if [ $? -eq 0 ]; then
    echo "✅ Ready for release"
else
    echo "❌ Fix issues before release"
    exit 1
fi
```

### Continuous Integration
```yaml
# GitHub Actions example
- name: Validate Claude Plugin
  run: |
    /validate:plugin --strict
    if [ $? -ne 0 ]; then
      echo "Plugin validation failed - blocking release"
      exit 1
    fi
```

### Local Development
```bash
# During development
make validate-plugin  # Custom command that runs validation

# Before committing changes
git add .
git commit -m "Update plugin (validated: ✅)"
```

## Common Installation Failure Prevention

The validator specifically targets the most common causes of plugin installation failures:

### 1. JSON Syntax Errors
```json
// ❌ INVALID (trailing comma)
{
  "name": "my-plugin",
  "version": "1.0.0",
}

// ✅ VALID
{
  "name": "my-plugin",
  "version": "1.0.0"
}
```

### 2. Missing Required Fields
```json
// ❌ MISSING VERSION
{
  "name": "my-plugin",
  "description": "A great plugin"
}

// ✅ COMPLETE
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A great plugin",
  "author": "Developer Name"
}
```

### 3. File Encoding Issues
```bash
# Check file encoding
file .claude-plugin/plugin.json

# Convert to UTF-8 if needed
iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt
```

### 4. Directory Structure
```
my-plugin/
+-- .claude-plugin/
|   +-- plugin.json        # REQUIRED
+-- agents/               # OPTIONAL
+-- skills/               # OPTIONAL
+-- commands/             # OPTIONAL
+-- lib/                  # OPTIONAL
```

## Marketplace Compatibility

The validation ensures compatibility with Claude Code plugin marketplaces:

### Installation Methods Supported
- ✅ GitHub repository URLs
- ✅ Git repository URLs
- ✅ Local directory paths
- ✅ Team distribution sources
- ✅ Marketplace listing files

### Requirements Met
- ✅ JSON manifest schema compliance
- ✅ Semantic versioning format
- ✅ UTF-8 encoding throughout
- ✅ Cross-platform file paths
- ✅ Proper directory structure
- ✅ Valid file formats

## Error Recovery

### Auto-Fix Capabilities
The validator can automatically correct many common issues:

1. **JSON Syntax**: Remove trailing commas, fix quotes
2. **Missing Fields**: Add defaults (version: "1.0.0", author: "Unknown")
3. **File Encoding**: Convert to UTF-8 automatically
4. **Line Endings**: Normalize line endings for platform
5. **Agent Delegation**: Auto-correct agent identifier prefixes (`orchestrator` -> `autonomous-agent:orchestrator`)
6. **Command Frontmatter**: Add missing `delegates-to` fields based on command content analysis
7. **Agent Mapping**: Verify and fix command-to-agent mappings by cross-referencing agents directory

### Manual Fixes Required
1. **Structural Issues**: Directory reorganization
2. **Content Issues**: Improve documentation quality
3. **Naming Conflicts**: Resolve duplicate names
4. **Version Conflicts**: Semantic versioning corrections

## Troubleshooting

### Common Validation Failures

**Error**: "Missing plugin manifest"
- **Cause**: No `.claude-plugin/plugin.json` file
- **Fix**: Create manifest with required fields

**Error**: "Invalid JSON syntax"
- **Cause**: Syntax errors in plugin.json
- **Fix**: Use JSON linter, check for trailing commas

**Error**: "Missing required fields"
- **Cause**: Required JSON fields absent
- **Fix**: Add name, version, description, author fields

**Error**: "File encoding error"
- **Cause**: Non-UTF-8 encoded files
- **Fix**: Convert all files to UTF-8 encoding

**Error**: "Agent type not found" (Runtime Command Failure)
- **Cause**: Command references incorrect agent identifier
- **Example**: `/quality-check` tries to delegate to `orchestrator` instead of `autonomous-agent:orchestrator`
- **Fix**: Update command frontmatter with correct `delegates-to: autonomous-agent:agent-name`

**Error**: "Missing delegates-to field"
- **Cause**: Command YAML frontmatter lacks delegation specification
- **Fix**: Add `delegates-to: autonomous-agent:agent-name` to command frontmatter

**Error**: "Command execution failed"
- **Cause**: Referenced agent file doesn't exist in `agents/` directory
- **Fix**: Create missing agent file or update delegation to existing agent

### Getting Help

```bash
# Detailed validation with debugging
/validate:plugin --debug

# Check specific file
/validate:plugin --file .claude-plugin/plugin.json

# Show validation rules
/validate:plugin --show-rules
```

## Best Practices

### Development Workflow
1. **Create Plugin Structure**: Follow standard layout
2. **Write Manifest**: Complete all required fields
3. **Add Content**: Agents, skills, commands
4. **Validate**: Run `/validate:plugin`
5. **Fix Issues**: Address any problems found
6. **Re-validate**: Ensure all issues resolved
7. **Release**: Publish with confidence

### Quality Assurance
- Run validation before every commit
- Use `--strict` mode for pre-release checks
- Monitor validation scores over time
- Keep documentation up to date
- Test on multiple platforms

---

This validation command ensures your Claude Code plugin meets official guidelines and will install successfully across all supported platforms and marketplace types.