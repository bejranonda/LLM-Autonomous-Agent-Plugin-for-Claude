# Command Update Guide: Cross-Platform Script Execution

## Quick Reference

### Old Pattern (❌ Don't Use)

```markdown
Execute: python <plugin_path>/lib/dashboard.py --port 5000
```

**Problems**:
- `<plugin_path>` is a placeholder that doesn't resolve
- Doesn't work with marketplace installations
- Not cross-platform compatible

### New Pattern (✅ Use This)

```markdown
Execute: python lib/exec_plugin_script.py dashboard.py --port 5000
```

**Benefits**:
- Actual executable command
- Works everywhere (dev, marketplace, all platforms)
- Automatic plugin path resolution

## Update Checklist

For each command file in `commands/`:

- [ ] Search for `<plugin_path>` placeholders
- [ ] Replace with `python lib/exec_plugin_script.py {script_name}`
- [ ] Keep all script arguments unchanged
- [ ] Test the command works
- [ ] Update documentation if needed

## Examples

### Example 1: Simple Dashboard Command

**Before**:
```markdown
```bash
python <plugin_path>/lib/dashboard.py --host 127.0.0.1 --port 5000
```
```

**After**:
```markdown
```bash
python lib/exec_plugin_script.py dashboard.py --host 127.0.0.1 --port 5000
```
```

### Example 2: Learning Analytics Command

**Before**:
```markdown
```bash
python <plugin_path>/lib/learning_analytics.py show --dir .claude-patterns
```
```

**After**:
```markdown
```bash
python lib/exec_plugin_script.py learning_analytics.py show --dir .claude-patterns
```
```

### Example 3: Multiple Python Scripts

**Before**:
```markdown
```bash
# First script
python <plugin_path>/lib/script1.py --option value

# Second script
python <plugin_path>/lib/script2.py --other-option
```
```

**After**:
```markdown
```bash
# First script
python lib/exec_plugin_script.py script1.py --option value

# Second script
python lib/exec_plugin_script.py script2.py --other-option
```
```

## Commands That Need Updating

### Priority 1: Commands with `<plugin_path>`

Search for files containing `<plugin_path>`:
```bash
grep -r "<plugin_path>" commands/
```

**Found in**:
- `commands/monitor/dashboard.md` ✅ (Already updated)
- `commands/learn/analytics.md` (Needs update)
- (Other files as found)

### Priority 2: Commands with Hardcoded Paths

Search for hardcoded Python script paths:
```bash
grep -r "python.*lib/.*\.py" commands/
```

Update any that don't use the executor pattern.

## Implementation Instructions for Claude Code

When you (Claude Code) encounter a slash command with Python script execution:

### Step 1: Identify the Pattern

Look for:
- `python <plugin_path>/lib/{script}.py`
- `python {absolute_path}/lib/{script}.py`
- Direct Python script calls

### Step 2: Transform to New Pattern

```python
# Old: python <plugin_path>/lib/dashboard.py --port 5000
# New: python lib/exec_plugin_script.py dashboard.py --port 5000

# Pattern:
# python lib/exec_plugin_script.py {script_name} {all_original_arguments}
```

### Step 3: Execute via Bash Tool

```python
# In your code
bash_command = "python lib/exec_plugin_script.py dashboard.py --port 5000"
result = execute_bash(bash_command)
```

## Testing Each Command

After updating a command, test it:

```bash
# 1. Show plugin info (verify setup)
python lib/exec_plugin_script.py --info

# 2. Test the command
python lib/exec_plugin_script.py {script_name} --help

# 3. Test with actual arguments
python lib/exec_plugin_script.py {script_name} {actual_args}
```

## Common Issues and Solutions

### Issue: "Plugin installation not found"

**Cause**: Running from wrong directory or plugin not installed

**Solution**:
```bash
# Check if plugin.json exists
ls .claude-plugin/plugin.json

# Or set explicit path
export CLAUDE_PLUGIN_PATH=/path/to/plugin
```

### Issue: "Script not found"

**Cause**: Script name misspelled or doesn't exist

**Solution**:
```bash
# List available scripts
ls lib/*.py

# Check exact filename (case-sensitive on Linux/macOS)
```

### Issue: "Permission denied"

**Cause**: Script file not executable or readable

**Solution**:
```bash
# Linux/macOS
chmod 644 lib/*.py  # Make readable
chmod +x lib/*.py   # Make executable (if needed)
```

## Bulk Update Script

For updating multiple commands at once:

```bash
# Create backup
cp -r commands commands.backup

# Find all files with <plugin_path>
grep -l "<plugin_path>" commands/**/*.md

# Replace pattern (GNU sed)
find commands -name "*.md" -type f -exec sed -i 's|python <plugin_path>/lib/\([^[:space:]]*\)|python lib/exec_plugin_script.py \1|g' {} \;

# Replace pattern (macOS sed)
find commands -name "*.md" -type f -exec sed -i '' 's|python <plugin_path>/lib/\([^[:space:]]*\)|python lib/exec_plugin_script.py \1|g' {} \;
```

## Verification

After updates, verify all commands:

```bash
# Check no <plugin_path> placeholders remain
grep -r "<plugin_path>" commands/

# Should return empty or only documentation references
```

## Documentation Updates

After updating commands, also update:

1. **README.md**: Update any command examples
2. **USAGE_GUIDE.md**: Update usage examples if they show commands
3. **STRUCTURE.md**: Update if command structure changed
4. **CLAUDE.md**: Verify architecture documentation is current

## Roll-out Strategy

### Phase 1: Core Commands (High Priority)
- `/monitor:dashboard` ✅
- `/learn:analytics`
- `/analyze:quality`
- `/analyze:project`

### Phase 2: Frequently Used Commands
- `/dev:auto`
- `/dev:release`
- `/validate:fullstack`
- `/workspace:organize`

### Phase 3: Specialized Commands
- All other commands in `commands/` directory

### Phase 4: Documentation
- Update all documentation files
- Update examples in README
- Update CLAUDE.md

## Success Criteria

- ✅ All commands use `python lib/exec_plugin_script.py` pattern
- ✅ No `<plugin_path>` placeholders in command files
- ✅ All commands tested on Windows (minimum)
- ✅ Documentation updated
- ✅ No hardcoded absolute paths

## Notes for Future Development

When creating new slash commands:

1. **Always use executor**: `python lib/exec_plugin_script.py {script}`
2. **Never hardcode paths**: Let the resolver find the plugin
3. **Test cross-platform**: Verify on Windows at minimum
4. **Document clearly**: Show exact command syntax
5. **Handle errors**: Mention common issues in command docs

---

**Status**: Guide created
**Next Steps**: Begin Phase 1 updates
**Tracking**: Use this checklist to track progress
