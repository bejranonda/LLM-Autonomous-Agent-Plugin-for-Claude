# Plugin Validation System

## Overview

The `plugin_validator.py` script provides comprehensive validation and quality assurance for the Autonomous Agent Plugin. It checks plugin structure, documentation consistency, JSON manifests, agent/skill compliance, and generates detailed reports with recommendations.

## Features

### Comprehensive Validation Checks

1. **Plugin Manifest Validation**
   - Required fields validation (name, version, description, author, repository)
   - Version format checking (semantic versioning x.y.z)
   - JSON syntax validation

2. **Directory Structure Verification**
   - Required directories: agents/, skills/, commands/, lib/
   - Optional directories: patterns/
   - File vs directory path validation

3. **Agent File Validation**
   - YAML frontmatter validation
   - Required frontmatter fields (name, description)
   - Content quality assessment
   - Agent count verification

4. **Skill File Validation**
   - Skill directory structure (skills/*/SKILL.md)
   - YAML frontmatter validation
   - Required fields (name, description, version)
   - Content quality checks

5. **Command File Validation**
   - Command documentation structure
   - Usage section validation
   - Example code presence

6. **Documentation Quality Assessment**
   - README.md completeness (Installation, Usage, Features)
   - CLAUDE.md project instructions
   - LICENSE file presence
   - Documentation quality scoring

7. **Version Consistency Checking**
   - Cross-reference version numbers across files
   - Detect version mismatches
   - Validate semantic versioning

8. **YAML Frontmatter Validation**
   - Syntax validation for all markdown files
   - Required field checking
   - Frontmatter completeness

9. **Cross-Reference Validation**
   - Broken link detection
   - File reference validation
   - Component count consistency

10. **Quality Assurance**
    - Large file detection (performance impact)
    - Sensitive information scanning
    - Common issue detection

## Usage

### Command Line Interface

```bash
# Basic validation (current directory)
python lib/plugin_validator.py

# Specific plugin directory
python lib/plugin_validator.py --dir /path/to/plugin

# Save report with custom name
python lib/plugin_validator.py --output my-validation-report.json

# Quiet mode (summary only)
python lib/plugin_validator.py --quiet

# JSON output format
python lib/plugin_validator.py --format json
```

### Windows PowerShell Example

```powershell
# Validate and save report
python lib/plugin_validator.py --dir "." --output "validation-$(Get-Date -Format 'yyyy-MM-dd').json"

# Quick check with exit code
python lib/plugin_validator.py --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "Plugin validation PASSED" -ForegroundColor Green
} else {
    Write-Host "Plugin validation FAILED" -ForegroundColor Red
}
```

### Windows CMD Example

```cmd
REM Validate with timestamp
python lib/plugin_validator.py --output "validation-%date:~-4,4%%date:~-7,2%%date:~-10,2%.json"

REM Check validation result
python lib/plugin_validator.py --quiet
if %errorlevel% equ 0 (
    echo Plugin validation PASSED
) else (
    echo Plugin validation FAILED
)
```

## Output Format

### Console Output (Text Format)

```
============================================================
PLUGIN VALIDATION RESULTS
============================================================
Plugin is in excellent condition!
Quality Score: 100/100 (0 issues, 4 warnings)

Warnings (4):
  • Missing license file: LICENSE
  • Command missing usage section: validate-fullstack.md
  • autofix-patterns.json has unexpected structure
  • Documentation quality could be improved: 70%

Validations Passed (8):
  • Plugin manifest is valid and complete
  • Validated 13 agent files
  • Validated 9 skill files
  • Validated 7 command files
  • Documentation files validated
  • Version consistency verified: 2.1.1
  • YAML frontmatter valid in 30 files
  • Found 13 agents, 9 skills, 7 commands
============================================================

Detailed report saved to: plugin-validation-report-2025-10-23_11-48-30.json
```

### JSON Output Format

```json
{
  "timestamp": "2025-10-23T11:48:30.123456",
  "plugin_dir": ".",
  "overall_score": 100,
  "quality_level": "Excellent",
  "issues_count": 0,
  "warnings_count": 4,
  "fixes_count": 8,
  "issues": [],
  "warnings": [
    "Missing license file: LICENSE",
    "Command missing usage section: validate-fullstack.md"
  ],
  "fixes": [
    ["manifest_valid", "Plugin manifest is valid and complete"],
    ["agents_valid", "Validated 13 agent files"]
  ],
  "summary": "Plugin is in excellent condition!..."
}
```

## Quality Scoring System

The validator calculates a quality score from 0-100 based on:

- **Critical Issues**: -5 to -30 points each
- **Warnings**: No score impact, but documented
- **Passed Validations**: Positive indicators

### Score Levels

- **90-100**: Excellent - Production ready
- **80-89**: Good - Minor issues
- **70-79**: Acceptable - Needs some improvements
- **60-69**: Needs Improvement - Significant issues
- **0-59**: Poor - Critical issues must be addressed

## Exit Codes

- **0**: Success (Score ≥ 70)
- **1**: Issues found (Score < 70)
- **2**: Validation failed (Exception occurred)

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Plugin Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: pip install PyYAML

    - name: Validate plugin
      run: python lib/plugin_validator.py

    - name: Upload validation report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: validation-report
        path: plugin-validation-report-*.json
```

### Windows Task Scheduler Example

```powershell
# Create a scheduled task to run validation weekly
$action = New-ScheduledTaskAction -Execute "python" -Argument "lib\plugin_validator.py --quiet"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 2am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Plugin Validation" -Description "Validate Autonomous Agent Plugin weekly"
```

## Common Issues and Fixes

### Missing Dependencies

If you encounter `ModuleNotFoundError: No module named 'yaml'`:

```bash
pip install PyYAML
```

### Unicode Encoding Issues (Windows)

The validator automatically handles Unicode encoding for Windows environments. All emoji characters have been replaced with plain text equivalents.

### Permission Issues

Ensure the script has read permissions for all plugin files and write permissions for the output directory.

## Development

### Adding New Validation Rules

1. Add a new validation method to the `PluginValidator` class
2. Call the method from `validate_all()`
3. Use consistent error/warning/fix categorization
4. Update documentation

### Testing

```bash
# Test with quiet mode
python lib/plugin_validator.py --quiet

# Test JSON output
python lib/plugin_validator.py --format json

# Test specific plugin directory
python lib/plugin_validator.py --dir ./test-plugin
```

## Troubleshooting

### Common Error Messages

- **"No such file or directory"**: Check that the plugin directory exists
- **"ModuleNotFoundError"**: Install PyYAML dependency
- **"Permission denied"**: Check file read/write permissions
- **"JSON decode error"**: Fix syntax errors in JSON files

### Debug Mode

For detailed debugging, modify the script to enable verbose output by adding print statements in validation methods.

## Contributing

When contributing to the validation system:

1. Follow the existing code style and patterns
2. Add comprehensive documentation for new features
3. Test across different platforms (Windows, Linux, Mac)
4. Update this README with new validation rules
5. Maintain backward compatibility

## License

This validation script is part of the Autonomous Agent Plugin and follows the same MIT license terms.