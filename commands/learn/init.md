---
name: learn:init
description: Initialize or update pattern learning database for current version

# Smart Pattern Learning Initialization
# This command checks existing patterns and intelligently manages them:
# 1. If patterns exist -> Review and update for current version
# 2. If patterns are partial -> Complete missing components
# 3. If patterns don't exist -> Create new initial database
# 4. Focus on current version only (no legacy migration)

---

# Pattern Learning Initialization

Initialize or update the pattern learning database for the autonomous agent system.

## 🎯 Smart Initialization Logic

This command intelligently handles different scenarios:

### Scenario 1: Patterns Already Exist ✅
```bash
# If .claude-patterns/ exists and has complete data:
-> Review current patterns
-> Update for current plugin version (7.6.7)
-> Verify database integrity
-> Report: "Pattern learning already initialized. Database healthy."
```

### Scenario 2: Partial Patterns 🔧
```bash
# If .claude-patterns/ exists but incomplete:
-> Detect missing components
-> Complete partial databases
-> Validate all required files
-> Report: "Completed missing pattern components"
```

### Scenario 3: No Patterns (First Run) 🆕
```bash
# If .claude-patterns/ doesn't exist:
-> Create new pattern directory
-> Initialize empty pattern database
-> Create baseline configuration
-> Report: "Pattern learning initialized from scratch"
```

## 📋 Execution Steps

### Step 1: Check Existing Patterns
```bash
python lib/exec_plugin_script.py pattern_storage.py --check
```

### Step 2: Initialize or Update Based on Status
```bash
# If needed, create/update patterns
python lib/exec_plugin_script.py pattern_storage.py --init --version 7.6.7
```

### Step 3: Verify Database Health
```bash
python lib/exec_plugin_script.py pattern_storage.py --validate
```

## 🔍 What Gets Checked

1. **Directory Existence**: Does `.claude-patterns/` exist?
2. **File Completeness**: Are all required files present?
   - patterns.json
   - task_queue.json
   - quality_history.json
   - config.json
3. **Version Compatibility**: Is the database for current version (7.6.7)?
4. **Data Integrity**: Is the JSON valid and contains required fields?

## 📊 Expected Output

### First Run (No Existing Patterns)
```
============================================================
PATTERN LEARNING INITIALIZATION
============================================================

Status: NEW INSTALLATION
Action: Creating fresh pattern database for v7.6.7

Created:
- .claude-patterns/ directory
- patterns.json (empty, ready for learning)
- task_queue.json (empty task queue)
- quality_history.json (empty history)
- config.json (version 7.6.7)

Next Steps:
1. Start using other commands - patterns will be captured automatically
2. Run /analyze:project to begin pattern collection
3. Each task you perform builds the learning database

Pattern Learning: READY FOR USE
============================================================
```

### Existing Patterns (Already Initialized)
```
============================================================
PATTERN LEARNING STATUS
============================================================

Status: ALREADY INITIALIZED
Version: 7.6.7
Pattern Count: 15 patterns
Task History: 42 tasks recorded
Quality Metrics: 38 data points

Database Health: EXCELLENT
- All required files present
- JSON structure valid
- Version compatible with current plugin
- Data integrity confirmed

Recommendations:
- Continue using the system - learning is active
- Review analytics with /learn:analytics
- Check performance with /learn:performance

Pattern Learning: ACTIVE AND HEALTHY
============================================================
```

### Partial Patterns (Needs Completion)
```
============================================================
PATTERN LEARNING COMPLETION
============================================================

Status: PARTIAL DATABASE DETECTED
Action: Completing missing components

Found:
✓ patterns.json (valid)
✓ config.json (valid)
✗ task_queue.json (missing) -> CREATED
✗ quality_history.json (missing) -> CREATED

Updated:
- Version updated to 7.6.7
- Missing files created with proper structure
- Database integrity restored

Pattern Learning: COMPLETED AND READY
============================================================
```

## 🛠️ Technical Implementation

### Pattern Storage Script (`lib/pattern_storage.py`)
The command uses the existing Python utility to manage patterns:

**Check Mode**:
```python
python lib/pattern_storage.py --check
# Returns: exists, complete, version, integrity status
```

**Init Mode**:
```python
python lib/pattern_storage.py --init --version 7.6.7
# Creates or updates pattern database for current version
```

**Validate Mode**:
```python
python lib/pattern_storage.py --validate
# Verifies all files and structure
```

## 🎯 Key Features

1. **No Orchestrator Delegation**: Direct execution without agent overhead
2. **No Skill Loading**: Avoids empty content block issues
3. **Smart Detection**: Automatically determines what action is needed
4. **Version Aware**: Focuses on current version (7.6.7) only
5. **Idempotent**: Safe to run multiple times
6. **Fast Execution**: Completes in < 1 second

## 🔐 Safety Features

- **No Empty Content Blocks**: Pure Python execution, no message arrays
- **No cache_control Usage**: Completely eliminates the API error
- **Minimal Dependencies**: Uses only standard Python libraries
- **Error Handling**: Graceful degradation if files are missing
- **Validation**: Ensures database integrity before reporting success

## 📝 Usage

```bash
# Initialize pattern learning (first time or update)
/learn:init

# That's it! The command handles everything automatically.
```

## 🔄 Integration with Other Commands

After initialization, other commands automatically use the pattern database:

- `/analyze:project` - Records project analysis patterns
- `/analyze:quality` - Stores quality check outcomes
- `/dev:auto` - Learns from autonomous development
- All other commands contribute to pattern learning

## 🚀 Next Steps After Initialization

1. **Start Working**: Just use the plugin normally - patterns capture automatically
2. **Review Learning**: `/learn:analytics` to see what's been learned
3. **Check Performance**: `/learn:performance` to see improvement metrics
4. **Predict Patterns**: `/learn:predict` to get AI-driven recommendations

---

**Version**: 7.6.7
**Execution**: Direct Python (no orchestrator)
**Safety**: Zero cache_control errors
**Performance**: < 1 second execution time
