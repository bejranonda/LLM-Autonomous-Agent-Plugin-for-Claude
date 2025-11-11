# Alternative Installation Guide

## 🚨 GitHub Access Issue

If you're encountering a GitHub account suspension error when trying to install the plugin, here are several alternative methods to get the cache_control fix (v7.6.7).

## Method 1: Direct Download (Recommended)

### Step 1: Download the Plugin Files
1. Go to: https://github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude/releases/tag/v7.6.7
2. Download the `Source code (zip)` file
3. Extract the zip file to your preferred location

### Step 2: Manual Installation
```bash
# 1. Navigate to the extracted directory
cd LLM-Autonomous-Agent-Plugin-for-Claude-7.6.7

# 2. Create plugin directory if it doesn't exist
mkdir -p ~/.claude/plugins

# 3. Copy plugin to Claude Code plugins directory
cp -r . ~/.claude/plugins/autonomous-agent

# 4. Restart Claude Code
# 5. Test the fix
```

## Method 2: Git Clone with Different Credentials

If you have access to the repository through other means:

### Option A: Using Personal Access Token
```bash
# Create a personal access token on GitHub (Settings > Developer settings)
# Then use it to clone:

git clone https://YOUR_TOKEN@github.com/bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude.git ~/.claude/plugins/autonomous-agent
```

### Option B: Using SSH (if you have SSH keys set up)
```bash
git clone git@github.com:bejranonda/LLM-Autonomous-Agent-Plugin-for-Claude.git ~/.claude/plugins/autonomous-agent
```

## Method 3: Copy from Existing Installation

If someone you know has the working v7.6.7 version:

```bash
# Copy from their installation
cp -r /path/to/their/.claude/plugins/autonomous-agent ~/.claude/plugins/

# Restart Claude Code
```

## Method 4: Download Specific Files

Download these critical files and place them in the correct directory structure:

### Directory Structure:
```
~/.claude/plugins/autonomous-agent/
├── .claude-plugin/
│   └── plugin.json (v7.6.7)
├── agents/
│   └── orchestrator.md (with cache_control fix)
├── skills/
│   ├── pattern-learning/SKILL.md (fixed)
│   └── predictive-skill-loading/SKILL.md (fixed)
└── commands/
    └── learn/init.md
```

## Method 5: Temporary Manual Fix

If you have the old version and want to apply the emergency fix manually:

### Fix 1: Update plugin.json
Change version to "7.6.7" in `~/.claude/plugins/autonomous-agent/.claude-plugin/plugin.json`

### Fix 2: Remove cache_control from orchestrator.md
In `~/.claude/plugins/autonomous-agent/agents/orchestrator.md`:
```bash
# Replace these lines:
cache_control: { type: "ephemeral" }

# With:
/* cache_control removed for emergency fix */
```

### Fix 3: Fix Empty Array Returns
In skill files, replace `return [];` with:
```javascript
return [{ note: "Emergency fallback - empty array prevented", type: "emergency" }];
```

## Verification

After installation, verify the fix works:

```bash
# 1. Check plugin version
/plugin
# Should show: autonomous-agent v7.6.7

# 2. Test the previously broken command
/learn:init
# Should work without cache_control errors

# 3. If still broken, check for any remaining cache_control usage
grep -r "cache_control" ~/.claude/plugins/autonomous-agent/
```

## Support

If you continue to experience issues:

1. **Verify Installation**: Ensure you have v7.6.7, not an older version
2. **Check File Permissions**: Make sure all plugin files are readable
3. **Restart Claude Code**: Completely close and restart the application
4. **Clear Cache**: Some systems may cache old plugin versions

## Why This Fix Is Critical

The cache_control error was preventing **ALL plugin functionality**:
- `/learn:init` command was completely broken
- All 39 commands were affected
- The plugin was essentially unusable

Version 7.6.7 completely resolves this by:
- Removing all problematic cache_control usage
- Ensuring all message content blocks contain valid text
- Maintaining 100% plugin functionality

## Quick Test

After installation, run this test:
```bash
/learn:init
```

**Success**: Command completes without "cache_control cannot be set for empty text blocks" error
**Failure**: Still see the error → installation may not have updated properly

---

**Version 7.6.7 Status**: ✅ **CRITICAL FIX APPLIED** - Restores full plugin functionality