---
name: orchestrator-implementation
description: Detailed implementation strategies for the four-tier orchestrator agent architecture including sub-agent definitions and group coordination protocols.
---

# Orchestrator Implementation Reference

This skill provides detailed implementation guidance for the orchestrator agent.
It covers sub-agent definitions, group coordination, and the complete four-tier
workflow. The orchestrator agent will reference this skill when detailed
implementation context is needed.

## Implementation Strategy

### Phase 1: Four-Tier Architecture Foundation (v6.2.0)
- Implement core four-tier workflow system
- Create new specialized agents for each tier
- Enhance existing learning systems for four-tier support
- Maintain full backward compatibility

### Phase 2: Advanced Features (v6.3.0)
- Cross-tier learning acceleration
- Advanced performance optimization
- Enhanced user personalization across tiers
- Predictive decision-making capabilities

### Phase 3: AI-Driven Optimization (v6.4.0)
- Machine learning integration for tier selection
- Predictive performance optimization
- Advanced cross-tier knowledge synthesis
- Real-time adaptation and improvement

**Integration with Existing Systems**:
- **Pattern Learning**: Both tiers contribute to `.claude-patterns/patterns.json`
- **Agent Performance**: Individual agent metrics in `.claude-patterns/agent_performance.json`
- **Agent Feedback**: Cross-tier communication in `.claude-patterns/agent_feedback.json`
- **User Preferences**: Learned preferences in `.claude-patterns/user_preferences.json`

**Benefits of Two-Tier Architecture**:
- [OK] **Separation of Concerns**: Analysis vs Execution clearly separated
- [OK] **Better Decisions**: Tier 2 evaluates multiple Tier 1 recommendations
- [OK] **Continuous Learning**: Explicit feedback loops between tiers
- [OK] **User Adaptation**: Tier 2 incorporates learned user preferences
- [OK] **Independent Growth**: Each agent improves its specialized skills
- [OK] **Risk Mitigation**: Analysis identifies risks before execution

### 1. Autonomous Task Analysis
When receiving a task:
- Analyze the task context and requirements independently
- Identify the task category (coding, refactoring, documentation, testing, optimization)
- Determine project scope and complexity level
- Make autonomous decisions about approach without asking for confirmation
- **NEW**: Explicitly delegate to Tier 1 (Analysis) agents first, then Tier 2 (Execution) agents

### 2. Intelligent Skill Auto-Selection with Model Adaptation
Automatically select and load relevant skills based on model capabilities and task context:

**Model-Adaptive Skill Loading**:

**Claude Models (Sonnet/4.5)** - Progressive Disclosure:
```javascript
// Load skill metadata first, then full content based on context
const skillLoadingStrategy = {
  claude: {
    approach: "progressive_disclosure",
    context_aware: true,
    weight_based: true,
    merging_enabled: true
  }
}
```

**GLM Models** - Complete Loading:
```javascript
// Load complete skill content upfront with clear structure
const skillLoadingStrategy = {
  glm: {
    approach: "complete_loading",
    explicit_criteria: true,
    priority_sequenced: true,
    structured_handoffs: true
  }
}
```

**Universal Pattern Recognition**:
- Analyze historical patterns from the project
- **CRITICAL**: Check if `.claude-patterns/` directory exists and contains data before loading
- Review `.claude-patterns/` directory for learned patterns ONLY if they exist
- **EMPTY PATTERN HANDLING**: If no patterns exist, use default skill loading without caching
- Match current task against known successful approaches (skip if no patterns available)
- Auto-load skills that have proven effective for similar tasks (skip if no history)

**🚨 CRITICAL: Empty Pattern Prevention - ENFORCED VALIDATION**:
```javascript
// COMPREHENSIVE validation before applying cache_control
function validateContentForCaching(content) {
  // Handle null/undefined
  if (content === null || content === undefined) {
    return false;
  }

  // Convert to string if it's not already
  const contentStr = String(content);

  // Check for empty string
  if (contentStr.length === 0) {
    return false;
  }

  // Check for whitespace-only string
  if (contentStr.trim().length === 0) {
    return false;
  }

  // Check for minimal meaningful content (at least 5 characters)
  if (contentStr.trim().length < 5) {
    return false;
  }

  // Check for common empty indicators
  const emptyIndicators = ['null', 'undefined', '[]', '{}', 'none', 'empty'];
  if (emptyIndicators.includes(contentStr.trim().toLowerCase())) {
    return false;
  }

  return true;
}

// SAFE pattern loading with cache_control
if (validateContentForCaching(existingPatterns)) {
  // ONLY add with caching if content passes validation
  messages.push({
    type: "text",
    text: String(existingPatterns),
    /* cache_control removed for emergency fix */
  });
} else {
  // ALWAYS provide meaningful fallback content
  messages.push({
    type: "text",
    text: "Pattern learning will be initialized after first task execution. Using default skill selection for optimal results.",
    /* cache_control removed for emergency fix */
  });
}
```

**Context Analysis**:
- Scan project structure and technologies
- Identify programming languages, frameworks, and tools in use
- Select skills matching the technology stack
- **EMPTY CONTENT PREVENTION**: Only load skills if framework/language data exists
- Load domain-specific knowledge automatically (with fallback defaults if empty)

**Model-Enhanced Skill Loading Strategy**:
```
IF current model = "claude-sonnet-4.5":
  → Use progressive disclosure with context merging
  → Apply weight-based skill ranking
  → Enable cross-skill synergy detection

IF current model = "claude-haiku-4.5":
  → Use selective disclosure with fast loading
  → Apply efficient skill prioritization
  → Enable focused skill deployment

IF current model = "claude-opus-4.1":
  → Use intelligent progressive disclosure with prediction
  → Apply advanced weight-based skill ranking
  → Enable enhanced cross-skill synergy detection

IF current model = "glm-4.6":
  → Use complete upfront loading
  → Apply priority-based sequencing
  → Use explicit skill selection criteria

IF task involves Python:
  → Auto-load: code-analysis, quality-standards
  → **PATTERN LEARNING**: Only load if patterns exist (check .claude-patterns/patterns.json)
IF task involves testing:
  → Auto-load: testing-strategies
IF task involves documentation:
  → Auto-load: documentation-best-practices
IF refactoring detected:
  → Auto-load: code-analysis
  → **PATTERN LEARNING**: Only load if patterns exist (check .claude-patterns/patterns.json)
IF cross-model compatibility needed:
  → Auto-load: model-detection
IF GUI development detected (dashboard, web app, UI, frontend):
  → Auto-load: gui-design-principles, quality-standards
  → **PATTERN LEARNING**: Only load if patterns exist (check .claude-patterns/patterns.json)

**ENFORCED FIRST RUN HANDLING - EXECUTE SUBPROCESS**:
```python
# MANDATORY: Execute this subprocess call to validate pattern loading
# This ensures pattern learning is only enabled when safe

import subprocess
import sys
from pathlib import Path

def enforce_pattern_safety():
    """Execute the pattern safety script and return status."""

    # Find and execute safety script
    safety_script = Path("lib/pattern_loading_safety.py")

    if not safety_script.exists():
        # Fallback: check manually if script doesn't exist
        patterns_file = Path(".claude-patterns/patterns.json")
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    data = f.read().strip()
                SKIP_PATTERN_LEARNING = len(data) < 50  # Very basic check
                print(f"[FALLBACK] Pattern learning: {'ENABLED' if not SKIP_PATTERN_LEARNING else 'DISABLED'}")
            except:
                SKIP_PATTERN_LEARNING = True
                print("[FALLBACK] Pattern learning DISABLED: Error reading patterns")
        else:
            SKIP_PATTERN_LEARNING = True
            print("[FALLBACK] Pattern learning DISABLED: No patterns file")
        return SKIP_PATTERN_LEARNING

    try:
        # Execute safety script via subprocess
        result = subprocess.run([
            sys.executable, str(safety_script)
        ], capture_output=True, text=True)

        # Interpret result
        SKIP_PATTERN_LEARNING = result.returncode != 0
        print(f"[SAFETY] Pattern learning: {'ENABLED' if not SKIP_PATTERN_LEARNING else 'DISABLED'}")
        if result.stdout.strip():
            print(f"[SAFETY] {result.stdout.strip()}")
        if result.returncode != 0 and result.stderr.strip():
            print(f"[SAFETY] {result.stderr.strip()}")

    except Exception as e:
        print(f"[SAFETY] Pattern learning DISABLED: Error executing safety check: {e}")
        SKIP_PATTERN_LEARNING = True

    return SKIP_PATTERN_LEARNING

# EXECUTE the safety check
SKIP_PATTERN_LEARNING = enforce_pattern_safety()
```

**CRITICAL FIRST RUN HANDLING**:
IF SKIP_PATTERN_LEARNING == True:
  → Skip ALL pattern-learning skill loading
  → Use default skill selection based on task type only
  → DO NOT attempt to load existing patterns
  → DO NOT apply cache_control to empty pattern content
  → EXECUTE the Python code above to set this flag correctly
IF responsive design needed:
  → Auto-load: gui-design-principles, validation-standards
IF accessibility requirements mentioned:
  → Auto-load: gui-design-principles, validation-standards
IF dashboard or data visualization mentioned:
  → Auto-load: gui-design-principles, quality-standards
  → **PATTERN LEARNING**: Only load if patterns exist (check .claude-patterns/patterns.json)
```

### 3. Enhanced Pattern Learning & Predictive Intelligence (v3.0)

**Advanced Learning System**:
- Monitor all task executions with rich contextual data
- Generate project fingerprints for accurate pattern matching
- Use predictive models for optimal skill selection
- Store enhanced patterns with confidence scoring
- Enable cross-project knowledge transfer

**Enhanced Pattern Storage Architecture**:
```python
# Three-tier storage system for maximum learning efficiency

# 1. Enhanced Patterns (.claude-patterns/enhanced_patterns.json)
{
  "version": "3.0.0",
  "project_fingerprint": "sha256_hash",
  "patterns": [{
    "pattern_id": "enhanced_pattern_...",
    "task_classification": {
      "type": "refactoring|bug-fix|implementation",
      "complexity": "simple|medium|complex|expert",
      "domain": "authentication|data-processing|ui",
      "security_critical": true|false
    },
    "context": {
      "project_fingerprint": "unique_hash",
      "languages": ["python", "javascript"],
      "frameworks": ["flask", "react"],
      "file_patterns": ["backend/", "frontend/"]
    },
    "execution": {
      "skills_loaded": ["code-analysis", "security-patterns"],
      "skill_loading_strategy": "predictive",
      "agents_delegated": ["code-analyzer"],
      "model_detected": "claude-sonnet-4.5"
    },
    "outcome": {
      "success": true,
      "quality_score": 94,
      "performance_impact": "positive"
    },
    "prediction_data": {
      "predicted_quality": 90,
      "prediction_accuracy": 0.96,
      "skill_effectiveness_scores": {...}
    },
    "reuse_analytics": {
      "reuse_count": 5,
      "reuse_success_rate": 1.0,
      "confidence_boost": 0.15
    }
  }]
}

# 2. Skill Metrics (.claude-patterns/skill_metrics.json)
{
  "skill-name": {
    "total_uses": 87,
    "success_rate": 0.943,
    "confidence_score": 0.89,
    "performance_trend": "improving",
    "by_task_type": {...},
    "recommended_for": ["refactoring"],
    "not_recommended_for": ["documentation"]
  }
}

# 3. Predictive Models (.claude-patterns/skill_predictions.json)
{
  "performance_models": {
    "status": "trained",
    "prediction_accuracy": 0.87,
    "models": {...}  # Trained classifiers per skill
  }
}
```

**Predictive Skill Selection Process**:
```javascript
async function select_skills_intelligently(task_context) {
  // 1. Generate project fingerprint
  const fingerprint = generate_project_fingerprint({
    languages: detect_languages(),
    frameworks: detect_frameworks(),
    project_type: classify_project_type(),
    file_structure_patterns: analyze_file_structure()
  })

  // 2. Extract task features
  const features = extract_context_features({
    task_type: task_context.type,
    complexity: estimate_complexity(task_context),
    security_critical: is_security_critical(task_context),
    technology_stack: detect_tech_stack()
  })

  // 3. Query predictive system
  const predictions = await predict_optimal_skills({
    context_features: features,
    project_fingerprint: fingerprint,
    task_type: task_context.type
  })

  // 4. Filter by confidence threshold
  const high_confidence_skills = predictions
    .filter(p => p.confidence > 0.8)
    .sort((a, b) => b.probability - a.probability)

  // 5. Load top skills
  return high_confidence_skills.slice(0, 5)
}
```

**Auto-Creation and Maintenance**:
- Automatically create `.claude-patterns/` directory structure
- Initialize enhanced pattern database on first use
- Train prediction models after 20+ patterns captured
- Update skill effectiveness metrics in real-time
- Contribute anonymized patterns to cross-project learning

### 4. Special Slash Command Handling

**IMPORTANT**: Some slash commands require direct execution rather than full autonomous analysis. These are typically infrastructure, utility, or simple data display commands that benefit from immediate execution.

**Commands that use DIRECT EXECUTION** (bypass full analysis for speed):
- Infrastructure: `/monitor:dashboard` (start dashboard service)
- Data Display: `/learn:analytics`, `/learn:performance` (show reports)
- Utilities: `/workspace:organize`, `/workspace:reports` (file organization)
- Simple Tools: `/monitor:recommend`, `/learn:init`, `/validate:plugin` (basic operations)

**CRITICAL: /learn:init PATTERN LOADING RULES**:
- **DO NOT LOAD existing patterns** - this command creates them
- **DO NOT USE pattern-learning skill** - use default skills only
- **DO NOT APPLY cache_control** to pattern content (doesn't exist yet)
- **USE DEFAULT SKILLS**: code-analysis, documentation-best-practices only

**Commands that use FULL AUTONOMOUS ANALYSIS** (require intelligence):
- Complex Development: `/dev:auto`, `/dev:release`, `/dev:model-switch`
- Comprehensive Analysis: `/analyze:project`, `/analyze:quality`
- Advanced Validation: `/validate:fullstack`, `/validate:all`, `/validate:patterns`
- Complex Debugging: `/debug:gui`, `/debug:eval`
- Strategic Tasks: `/pr-review`, `/analyze:dependencies`, `/analyze:static`

```python
# Command Detection Logic (run FIRST before any analysis)
def detect_special_command(user_input):
    """Check if input is a special command that needs direct execution."""

    cmd = user_input.strip()

    # Dashboard and monitoring commands - direct Python execution
    if cmd.startswith('/monitor:dashboard'):
        return {
            'type': 'direct_execution',
            'command': 'dashboard',
            'script': 'lib/dashboard.py',
            'args': parse_dashboard_args(user_input)
        }

    # Learning and analytics commands - direct Python execution (data display only)
    if cmd.startswith('/learn:analytics'):
        return {
            'type': 'direct_execution',
            'command': 'learning_analytics',
            'script': 'lib/learning_analytics.py',
            'args': parse_learning_analytics_args(user_input)
        }

    if cmd.startswith('/learn:performance'):
        return {
            'type': 'direct_execution',
            'command': 'performance_report',
            'script': 'lib/performance_report.py',
            'args': parse_performance_report_args(user_input)
        }

    # Workspace organization commands - direct Python execution (utility functions)
    if cmd.startswith('/workspace:organize'):
        return {
            'type': 'direct_execution',
            'command': 'organize_workspace',
            'script': 'lib/workspace_organizer.py',
            'args': parse_organize_workspace_args(user_input)
        }

    if cmd.startswith('/workspace:reports'):
        return {
            'type': 'direct_execution',
            'command': 'organize_reports',
            'script': 'lib/report_organizer.py',
            'args': parse_organize_reports_args(user_input)
        }

    # Pattern management commands - direct Python execution (simple operations)
    if cmd.startswith('/learn:patterns'):
        return {
            'type': 'direct_execution',
            'command': 'pattern_management',
            'script': 'lib/pattern_management.py',
            'args': parse_pattern_management_args(user_input)
        }

    # User preference commands - direct Python execution (preference management)
    if cmd.startswith('/preferences:') or cmd.startswith('/prefs:'):
        pref_action = cmd.split(':')[1].split()[0]
        return {
            'type': 'direct_execution',
            'command': f'preference_{pref_action}',
            'script': 'lib/user_preference_memory.py',
            'args': parse_preference_args(user_input)
        }

    # Intelligent suggestion commands - direct Python execution (suggestion system)
    if cmd.startswith('/suggest:') or cmd.startswith('/recommend:'):
        return {
            'type': 'direct_execution',
            'command': 'generate_suggestions',
            'script': 'lib/intelligent_suggestion_engine.py',
            'args': parse_suggestion_args(user_input)
        }

    # Recommendation system - direct Python execution (simple recommendations)
    if cmd.startswith('/monitor:recommend'):
        return {
            'type': 'direct_execution',
            'command': 'smart_recommendations',
            'script': 'lib/smart_recommender.py',
            'args': parse_smart_recommendations_args(user_input)
        }

    # Plugin validation - direct Python execution (utility validation)
    if cmd.startswith('/validate:plugin'):
        return {
            'type': 'direct_execution',
            'command': 'plugin_validation',
            'script': 'lib/plugin_validator.py',
            'args': parse_plugin_validation_args(user_input)
        }

    # Learning initialization - direct Python execution (simple tool)
    if cmd.startswith('/learn:init'):
        return {
            'type': 'direct_execution',
            'command': 'learn_init',
            'args': parse_learn_init_args(user_input),
            'critical_instruction': 'DO_NOT_LOAD_PATTERNS',  # Prevents cache_control error
            'skip_pattern_learning': True,                   # Skip pattern-learning skill
            'allowed_skills': ['code-analysis', 'documentation-best-practices']  # Default skills only
        }

    # Note: Complex analytical commands like /debug:eval, /debug:gui, and /validate:commands
    # should go through full autonomous analysis for pattern learning, skill selection, and quality control

    if cmd.startswith('/validate:web'):
        return {
            'type': 'direct_execution',
            'command': 'validate_web',
            'script': 'lib/web_validator.py',
            'args': parse_web_validation_args(user_input)
        }

    # Workspace commands - direct Python execution (workspace utilities)
    if cmd.startswith('/workspace:distribution-ready'):
        return {
            'type': 'direct_execution',
            'command': 'workspace_distribution_ready',
            'script': 'lib/distribution_preparer.py',
            'args': parse_workspace_distribution_ready_args(user_input)
        }

    # Note: /workspace:improve is a complex analytical command that should go through
    # full autonomous analysis for pattern learning and improvement generation

    if cmd.startswith('/workspace:update-about'):
        return {
            'type': 'direct_execution',
            'command': 'workspace_update_about',
            'script': 'lib/about_updater.py',
            'args': parse_about_update_args(user_input)
        }

    if cmd.startswith('/workspace:update-readme'):
        return {
            'type': 'direct_execution',
            'command': 'workspace_update_readme',
            'script': 'lib/readme_updater.py',
            'args': parse_readme_update_args(user_input)
        }

    # All other commands should go through full autonomous analysis
    # Complex commands like /dev:auto, /analyze:project, /validate:fullstack, etc.
    # benefit from pattern learning, skill selection, and quality control

    return None

def parse_dashboard_args(user_input):
    """Parse dashboard command arguments - SAFE VERSION prevents empty text blocks."""
    if EMERGENCY_FIXES_AVAILABLE:
        return safe_parse_dashboard_args(user_input or "")
    else:
        # Fallback implementation if emergency fixes not available
        args = {
            'host': '127.0.0.1',
            'port': 5000,
            'patterns_dir': '.claude-patterns',
            'auto_open_browser': True
        }

        if not user_input:
            return args

        cmd = str(user_input).strip()
        if not cmd:
            return args

        # Safe extraction with fallbacks
        if '--host' in cmd:
            host_value = safe_extract_after(cmd, '--host')
            host_parts = safe_split(host_value, ' ', 1)
            args['host'] = host_parts[0] if host_parts else 'localhost'

        if '--port' in cmd:
            port_value = safe_extract_after(cmd, '--port')
            port_parts = safe_split(port_value, ' ', 1)
            port_str = port_parts[0] if port_parts else '5000'
            try:
                args['port'] = int(port_str) if port_str.isdigit() else 5000
            except (ValueError, TypeError):
                args['port'] = 5000

        if '--patterns-dir' in cmd:
            patterns_value = safe_extract_after(cmd, '--patterns-dir')
            patterns_parts = safe_split(patterns_value, ' ', 1)
            args['patterns_dir'] = patterns_parts[0] if patterns_parts else '.claude-patterns'

        if '--no-browser' in cmd:
            args['auto_open_browser'] = False

        return args

def parse_learning_analytics_args(user_input):
    """Parse learning analytics command arguments."""
    args = {
        'action': 'show',
        'dir': '.claude-patterns',
        'output': None,
        'format': None
    }

    # Default action is 'show'
    cmd = user_input.strip()

    # Parse subcommand
    if 'export-json' in cmd:
        args['action'] = 'export-json'
    elif 'export-md' in cmd:
        args['action'] = 'export-md'

    # Parse output file
    if '--output' in cmd:
        parts = cmd.split('--output')[1].strip().split()
        if parts:
            args['output'] = parts[0]

    # Parse directory
    if '--dir' in cmd:
        parts = cmd.split('--dir')[1].strip().split()
        if parts:
            args['dir'] = parts[0]

    return args

def parse_performance_report_args(user_input):
    """Parse performance report command arguments."""
    args = {
        'action': 'show',
        'dir': '.claude-patterns',
        'output': None,
        'format': None,
        'days': 30
    }

    cmd = user_input.strip()

    if 'export' in cmd:
        args['action'] = 'export'

    if '--output' in cmd:
        parts = cmd.split('--output')[1].strip().split()
        if parts:
            args['output'] = parts[0]

    if '--dir' in cmd:
        parts = cmd.split('--dir')[1].strip().split()
        if parts:
            args['dir'] = parts[0]

    if '--days' in cmd:
        parts = cmd.split('--days')[1].strip().split()
        if parts and parts[0].isdigit():
            args['days'] = int(parts[0])

    return args

def parse_organize_workspace_args(user_input):
    """Parse workspace organization command arguments."""
    args = {
        'action': 'organize',
        'target': '.',
        'dry_run': False,
        'backup': True
    }

    cmd = user_input.strip()

    if '--dry-run' in cmd:
        args['dry_run'] = True

    if '--no-backup' in cmd:
        args['backup'] = False

    if '--target' in cmd:
        parts = cmd.split('--target')[1].strip().split()
        if parts:
            args['target'] = parts[0]

    return args

def parse_organize_reports_args(user_input):
    """Parse report organization command arguments."""
    args = {
        'action': 'organize',
        'source': '.claude/reports',
        'archive_old': True,
        'days_threshold': 90
    }

    cmd = user_input.strip()

    if '--source' in cmd:
        parts = cmd.split('--source')[1].strip().split()
        if parts:
            args['source'] = parts[0]

    if '--no-archive' in cmd:
        args['archive_old'] = False

    if '--days' in cmd:
        parts = cmd.split('--days')[1].strip().split()
        if parts and parts[0].isdigit():
            args['days_threshold'] = int(parts[0])

    return args

def parse_pattern_management_args(user_input):
    """Parse pattern management command arguments."""
    args = {
        'action': 'show',
        'dir': '.claude-patterns',
        'pattern_type': None,
        'export': None
    }

    cmd = user_input.strip()

    if 'export' in cmd:
        args['action'] = 'export'
    elif 'validate' in cmd:
        args['action'] = 'validate'
    elif 'clean' in cmd:
        args['action'] = 'clean'

    if '--dir' in cmd:
        parts = cmd.split('--dir')[1].strip().split()
        if parts:
            args['dir'] = parts[0]

    if '--type' in cmd:
        parts = cmd.split('--type')[1].strip().split()
        if parts:
            args['pattern_type'] = parts[0]

    if '--export' in cmd:
        parts = cmd.split('--export')[1].strip().split()
        if parts:
            args['export'] = parts[0]

    return args

def parse_smart_recommendations_args(user_input):
    """Parse smart recommendations command arguments."""
    args = {
        'task_description': None,
        'context': 'current',
        'count': 3,
        'show_confidence': True
    }

    cmd = user_input.strip()

    # Extract task description after command
    if '--task' in cmd:
        parts = cmd.split('--task')[1].strip()
        args['task_description'] = parts

    if '--context' in cmd:
        parts = cmd.split('--context')[1].strip().split()
        if parts:
            args['context'] = parts[0]

    if '--count' in cmd:
        parts = cmd.split('--count')[1].strip().split()
        if parts and parts[0].isdigit():
            args['count'] = int(parts[0])

    if '--no-confidence' in cmd:
        args['show_confidence'] = False

    return args

def parse_plugin_validation_args(user_input):
    """Parse plugin validation command arguments."""
    args = {
        'plugin_path': '.',
        'strict_mode': False,
        'output_format': 'table'
    }

    cmd = user_input.strip()

    if '--strict' in cmd:
        args['strict_mode'] = True

    if '--format' in cmd:
        parts = cmd.split('--format')[1].strip().split()
        if parts:
            args['output_format'] = parts[0]

    if '--path' in cmd:
        parts = cmd.split('--path')[1].strip().split()
        if parts:
            args['plugin_path'] = parts[0]

    return args

def parse_queue_args(user_input):
    """Parse queue command arguments."""
    args = {
        'action': None,
        'task_id': None,
        'name': None,
        'description': None,
        'command': None,
        'priority': 'medium',
        'status': None,
        'limit': 20,
        'older_than': 24,
        'stop_on_error': False,
        'background': False,
        'dry_run': False,
        'dir': '.claude-patterns'
    }

    cmd = user_input.strip()
    parts = cmd.split()

    if len(parts) < 2:
        return args

    # Extract action from command
    action_part = parts[1] if ':' in parts[0] else parts[0]
    args['action'] = action_part

    # Parse specific arguments based on action
    if '--task-id' in cmd:
        idx = cmd.index('--task-id')
        if idx + 1 < len(cmd.split()):
            args['task_id'] = cmd.split()[idx + 1]

    if '--name' in cmd:
        idx = cmd.index('--name')
        if EMERGENCY_FIXES_AVAILABLE:
            remaining = safe_extract_remaining_args(cmd, idx + 1)
            args['name'] = safe_extract_between(remaining, '', '--description') or safe_extract_after(remaining, '') or 'Untitled Task'
        else:
            remaining = ' '.join(cmd.split()[idx + 1:]) if idx + 1 < len(cmd.split()) else ''
            if '--description' in remaining:
                args['name'] = remaining.split('--description')[0].strip()
            else:
                args['name'] = remaining or 'Untitled Task'

    if '--description' in cmd:
        idx = cmd.index('--description')
        if EMERGENCY_FIXES_AVAILABLE:
            remaining = safe_extract_remaining_args(cmd, idx + 1)
            args['description'] = safe_extract_between(remaining, '', '--command') or safe_extract_after(remaining, '') or 'No description provided'
        else:
            remaining = ' '.join(cmd.split()[idx + 1:]) if idx + 1 < len(cmd.split()) else ''
            if '--command' in remaining:
                args['description'] = remaining.split('--command')[0].strip()
            else:
                args['description'] = remaining or 'No description provided'

    if '--command' in cmd:
        idx = cmd.index('--command')
        if EMERGENCY_FIXES_AVAILABLE:
            remaining = safe_extract_remaining_args(cmd, idx + 1)
            args['command'] = safe_extract_between(remaining, '', '--priority') or safe_extract_after(remaining, '') or 'No command specified'
        else:
            remaining = ' '.join(cmd.split()[idx + 1:]) if idx + 1 < len(cmd.split()) else ''
            if '--priority' in remaining:
                args['command'] = remaining.split('--priority')[0].strip()
            else:
                args['command'] = remaining or 'No command specified'

    if '--priority' in cmd:
        idx = cmd.index('--priority')
        if idx + 1 < len(cmd.split()):
            priority = cmd.split()[idx + 1]
            args['priority'] = priority

    if '--status' in cmd:
        idx = cmd.index('--status')
        if idx + 1 < len(cmd.split()):
            args['status'] = cmd.split()[idx + 1]

    if '--limit' in cmd:
        idx = cmd.index('--limit')
        if idx + 1 < len(cmd.split()):
            try:
                args['limit'] = int(cmd.split()[idx + 1])
            except ValueError:
                pass

    if '--older-than' in cmd:
        idx = cmd.index('--older-than')
        if idx + 1 < len(cmd.split()):
            try:
                args['older_than'] = int(cmd.split()[idx + 1])
            except ValueError:
                pass

    if '--stop-on-error' in cmd:
        args['stop_on_error'] = True

    if '--background' in cmd:
        args['background'] = True

    if '--dry-run' in cmd:
        args['dry_run'] = True

    if '--dir' in cmd:
        idx = cmd.index('--dir')
        if idx + 1 < len(cmd.split()):
            args['dir'] = cmd.split()[idx + 1]

    return args

def parse_web_validation_args(user_input):
    """Parse web validation command arguments."""
    args = {
        'url': None,
        'comprehensive': False,
        'debug': False,
        'auto_fix': False
    }

    cmd = user_input.strip()

    # Extract URL from command
    if len(cmd.split()) > 1:
        potential_url = cmd.split()[1]
        if potential_url.startswith(('http://', 'https://')):
            args['url'] = potential_url

    # Parse flags
    if '--comprehensive' in cmd:
        args['comprehensive'] = True
    if '--debug' in cmd:
        args['debug'] = True
    if '--auto-fix' in cmd:
        args['auto_fix'] = True

    return args

def parse_about_update_args(user_input):
    """Parse about update command arguments."""
    args = {
        'repo': None,
        'description': None,
        'topics': None
    }

    cmd = user_input.strip()

    if '--repo' in cmd:
        parts = cmd.split('--repo')[1].strip().split()
        if parts:
            args['repo'] = parts[0]

    if '--description' in cmd:
        parts = cmd.split('--description')[1].strip().split()
        if parts:
            args['description'] = ' '.join(parts)

    if '--topics' in cmd:
        parts = cmd.split('--topics')[1].strip().split()
        if parts:
            args['topics'] = parts[0]

    return args

def parse_readme_update_args(user_input):
    """Parse README update command arguments."""
    args = {
        'style': 'smart',
        'sections': None
    }

    cmd = user_input.strip()

    if '--style' in cmd:
        parts = cmd.split('--style')[1].strip().split()
        if parts:
            args['style'] = parts[0]

    if '--sections' in cmd:
        parts = cmd.split('--sections')[1].strip().split()
        if parts:
            args['sections'] = parts[0]

    return args

def parse_learn_init_args(user_input):
    """Parse learn init command arguments."""
    args = {
        'dir': '.claude-patterns',
        'force': False,
        'verbose': False
    }

    cmd = user_input.strip()

    # Parse directory argument
    if '--dir' in cmd:
        parts = cmd.split('--dir')[1].strip().split()
        if parts:
            args['dir'] = parts[0]

    # Parse flags
    if '--force' in cmd:
        args['force'] = True
    if '--verbose' in cmd:
        args['verbose'] = True

    return args

# Parser functions for complex analytical commands removed - they now go through autonomous analysis
# These commands benefit from pattern learning, skill selection, and quality control

def parse_workspace_distribution_ready_args(user_input):
    """Parse workspace distribution ready command arguments."""
    args = {
        'target': '.',
        'clean': False,
        'validate': True,
        'output': None
    }

    cmd = user_input.strip()

    # Parse target directory
    if len(cmd.split()) > 1:
        args['target'] = cmd.split()[1]

    # Parse flags
    if '--clean' in cmd:
        args['clean'] = True
    if '--no-validate' in cmd:
        args['validate'] = False
    if '--output' in cmd:
        parts = cmd.split('--output')[1].strip().split()
        if parts:
            args['output'] = parts[0]

    return args

def parse_preference_args(user_input):
    """Parse preference command arguments."""
    args = {
        'action': None,
        'category': None,
        'key': None,
        'value': None,
        'export_path': None,
        'import_path': None,
        'strategy': 'merge',
        'include_sensitive': False,
        'dir': '.claude-preferences'
    }

    cmd = user_input.strip()
    parts = cmd.split()

    if len(parts) < 2:
        return args

    # Extract action from command
    if ':' in parts[0]:
        action_part = parts[0].split(':')[1]
    else:
        action_part = parts[1]
    args['action'] = action_part

    if '--category' in cmd:
        idx = cmd.index('--category')
        if idx + 1 < len(cmd.split()):
            args['category'] = cmd.split()[idx + 1]

    if '--key' in cmd:
        idx = cmd.index('--key')
        if idx + 1 < len(cmd.split()):
            args['key'] = cmd.split()[idx + 1]

    if '--value' in cmd:
        idx = cmd.index('--value')
        if EMERGENCY_FIXES_AVAILABLE:
            remaining = safe_extract_remaining_args(cmd, idx + 1)
            args['value'] = remaining or 'default_value'
        else:
            remaining = ' '.join(cmd.split()[idx + 1:]) if idx + 1 < len(cmd.split()) else ''
            args['value'] = remaining or 'default_value'

    if '--export' in cmd:
        idx = cmd.index('--export')
        if idx + 1 < len(cmd.split()):
            args['export_path'] = cmd.split()[idx + 1]

    if '--import' in cmd:
        idx = cmd.index('--import')
        if idx + 1 < len(cmd.split()):
            args['import_path'] = cmd.split()[idx + 1]

    if '--strategy' in cmd:
        idx = cmd.index('--strategy')
        if idx + 1 < len(cmd.split()):
            args['strategy'] = cmd.split()[idx + 1]

    if '--include-sensitive' in cmd:
        args['include_sensitive'] = True

    if '--dir' in cmd:
        idx = cmd.index('--dir')
        if idx + 1 < len(cmd.split()):
            args['dir'] = cmd.split()[idx + 1]

    return args

def parse_suggestion_args(user_input):
    """Parse suggestion command arguments."""
    args = {
        'action': 'generate',
        'max_suggestions': 5,
        'quality_score': None,
        'project_type': None,
        'include_learning': True,
        'dir': '.claude-preferences'
    }

    cmd = user_input.strip()

    if '--max' in cmd:
        idx = cmd.index('--max')
        if idx + 1 < len(cmd.split()):
            try:
                args['max_suggestions'] = int(cmd.split()[idx + 1])
            except ValueError:
                pass

    if '--quality' in cmd:
        idx = cmd.index('--quality')
        if idx + 1 < len(cmd.split()):
            try:
                args['quality_score'] = float(cmd.split()[idx + 1])
            except ValueError:
                pass

    if '--project-type' in cmd:
        idx = cmd.index('--project-type')
        if idx + 1 < len(cmd.split()):
            args['project_type'] = cmd.split()[idx + 1]

    if '--no-learning' in cmd:
        args['include_learning'] = False

    if '--dir' in cmd:
        idx = cmd.index('--dir')
        if idx + 1 < len(cmd.split()):
            args['dir'] = cmd.split()[idx + 1]

    return args

# EXECUTION PRIORITY CHECK
def handle_special_command(command_info):
    """Execute special commands directly."""
    if command_info['type'] == 'direct_execution':
        if command_info['command'] == 'dashboard':
            # Build Python command
            cmd = ['python', command_info['script']]

            args = command_info['args']
            if args['host'] != '127.0.0.1':
                cmd.extend(['--host', args['host']])
            if args['port'] != 5000:
                cmd.extend(['--port', str(args['port'])])
            if args['patterns_dir'] != '.claude-patterns':
                cmd.extend(['--patterns-dir', args['patterns_dir']])
            if args['auto_open_browser'] == False:
                cmd.append('--no-browser')

            # Execute dashboard
            import subprocess
            import sys

            try:
                # Consolidate dashboard startup output to prevent empty content blocks
                dashboard_output = [
                    f"[OK] Starting Autonomous Agent Dashboard...",
                    f"   Dashboard URL: http://{args['host']}:{args['port']}",
                    f"   Pattern directory: {args['patterns_dir']}"
                ]
                print("\n".join(dashboard_output))

                # Run in background to not block
                process = subprocess.Popen(cmd,
                                         stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL)

                # Brief wait to ensure startup
                import time
                time.sleep(1)

                if process.poll() is None:
                    success_output = [
                        f"[OK] Dashboard started successfully!",
                        f"   Access at: http://{args['host']}:{args['port']}"
                    ]

                    # Auto-open browser if enabled
                    if args['auto_open_browser']:
                        try:
                            import webbrowser
                            import time
                            time.sleep(1)  # Give server time to start
                            webbrowser.open(f"http://{args['host']}:{args['port']}")
                            success_output.append(f"   [WEB] Browser opened automatically")
                        except Exception:
                            success_output.append(f"   [FOLDER] Manual browser access required")

                    success_output.append(f"   Press Ctrl+C in the terminal to stop the server")
                    print("\n".join(success_output))
                    return True
                else:
                    print(f"[ERROR] Dashboard failed to start")
                    return False

            except Exception as e:
                print(f"[ERROR] Error starting dashboard: {e}")
                return False

    elif command_info['command'] == 'learning_analytics':
        # Build Python command for learning analytics
        cmd = ['python', command_info['script']]

        args = command_info['args']
        cmd.append(args['action'])

        if args['dir'] != '.claude-patterns':
            cmd.extend(['--dir', args['dir']])

        if args['output']:
            cmd.extend(['--output', args['output']])

        # Execute learning analytics
        import subprocess
        import sys

        try:
                # Consolidate learning analytics output to prevent empty content blocks
                analytics_output = [
                    f"[REPORT] Generating Learning Analytics Report...",
                    f"   Command: {' '.join(cmd)}"
                ]
                print("\n".join(analytics_output))

                # Run and capture output
                result = subprocess.run(cmd,
                                       capture_output=True,
                                       text=True,
                                       check=True)

                # Display the output
                print(result.stdout)

                return True

            except subprocess.CalledProcessError as e:
                error_output = [
                    f"[ERROR] Error generating learning analytics: {e}"
                ]
                if e.stderr:
                    error_output.append(f"   Error details: {e.stderr}")
                error_output.append(f"   Try running manually: python ${CLAUDE_PLUGIN_ROOT}/lib/learning_analytics.py show")
                print("\n".join(error_output))
                return False
            except Exception as e:
                print(f"[ERROR] Error: {e}")
                return False

    elif command_info['command'] == 'learn_init':
        # TOKEN-EFFICIENT: AI reasoning + Python script for file operations
        import os
        import subprocess
        import json
        import sys
        from pathlib import Path
        from datetime import datetime

        args = command_info['args']
        patterns_dir = args['dir']

        print("[OK] Initializing Learning System...")

        # AI REASONING: Analyze project and prepare context
        print("   [OK] Analyzing project structure...")

        current_dir = Path.cwd()
        project_context = {
            "location": str(current_dir),
            "name": current_dir.name,
            "type": "unknown",
            "frameworks": [],
            "languages": [],
            "total_files": 0,
            "detected_at": datetime.now().isoformat()
        }

        # Efficient project analysis (lightweight scanning)
        try:
            python_files = list(current_dir.rglob("*.py"))
            js_files = list(current_dir.rglob("*.js"))
            ts_files = list(current_dir.rglob("*.ts"))

            project_context["languages"] = []
            if python_files: project_context["languages"].append("python")
            if js_files: project_context["languages"].append("javascript")
            if ts_files: project_context["languages"].append("typescript")

            project_context["total_files"] = len(python_files) + len(js_files) + len(ts_files)

            # Quick framework detection
            all_files = python_files + js_files + ts_files
            for file_path in all_files[:20]:  # Check first 20 files for efficiency
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if 'fastapi' in content: project_context["frameworks"].append("fastapi")
                        elif 'flask' in content: project_context["frameworks"].append("flask")
                        elif 'django' in content: project_context["frameworks"].append("django")
                        elif 'react' in content: project_context["frameworks"].append("react")
                        elif 'vue' in content: project_context["frameworks"].append("vue")
                except:
                    continue

            # Determine project type
            if project_context["frameworks"]:
                project_context["type"] = f"{project_context['frameworks'][0]}-application"
            elif "python" in project_context["languages"]:
                project_context["type"] = "python-project"
            elif "javascript" in project_context["languages"] or "typescript" in project_context["languages"]:
                project_context["type"] = "web-application"

        except Exception as e:
            print(f"   [WARN]  Project analysis limited: {e}")

        # DELEGATE TO PYTHON SCRIPT: Efficient file operations
        print("   [STORAGE]  Creating learning databases...")

        try:
            # Find plugin installation and execute learning_engine.py
            home = Path.home()
            plugin_name = "LLM-Autonomous-Agent-Plugin-for-Claude"

            # Search for plugin
            search_paths = [
                home / ".claude" / "plugins" / "marketplaces" / plugin_name,
                home / ".config" / "claude" / "plugins" / "marketplaces" / plugin_name,
                home / ".claude" / "plugins" / "autonomous-agent",
            ]

            plugin_path = None
            for path in search_paths:
                if path and (path / ".claude-plugin" / "plugin.json").exists():
                    plugin_path = path
                    break

            if not plugin_path:
                # Fallback to current directory
                plugin_path = Path.cwd()

            learning_script = plugin_path / "lib" / "learning_engine.py"

            if learning_script.exists():
                # Execute efficient Python script for file operations
                cmd = [
                    sys.executable, str(learning_script),
                    "init",
                    "--data-dir", patterns_dir,
                    "--project-context", json.dumps(project_context)
                ]

                # Add optional flags
                if args['force']:
                    cmd.append("--force")
                if args['verbose']:
                    cmd.append("--verbose")

                result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

                if result.returncode == 0:
                    # Parse JSON result from script
                    init_result = json.loads(result.stdout)

                    if init_result.get("status") == "initialized":
                        print("   [OK] Learning databases created successfully")

                        # Present results as required by command specification
                        # Consolidate all output into a single block to prevent empty content blocks
                        output_lines = [
                            "",
                            "=======================================================",
                            "  PATTERN LEARNING INITIALIZED",
                            "=======================================================",
                            "",
                            "== Project Analysis ====================================",
                            f"= Location: {project_context['location']}            =",
                            f"= Type: {project_context['type']}                      =",
                            f"= Languages: {', '.join(project_context['languages']) or 'None detected'} =",
                            f"= Frameworks: {', '.join(project_context['frameworks']) or 'None detected'} =",
                            f"= Total Files: {project_context['total_files']}          =",
                            "= Project Structure: Scanned successfully              =",
                            "=========================================================",
                            "",
                            "== Pattern Database Created ============================",
                            "= Location: .claude-patterns/                         =",
                            "=                                                       =",
                            "= Files Created:                                        ="
                        ]

                        # Add files created dynamically
                        for file_name in init_result.get("files_created", []):
                            file_type = 'storage' if 'config' in file_name else 'tracking' if 'quality' in file_name else 'data'
                            output_lines.append(f"= [OK] {file_name:<20} {file_type:<8}            =")

                        # Continue with the rest of the output
                        output_lines.extend([
                            "=                                                       =",
                            "= Status: Ready for pattern capture                     =",
                            "=========================================================",
                            "",
                            "== Initial Patterns Detected ===========================",
                            "= • Project structure patterns                          =",
                            "= • File organization patterns                         ="
                        ])

                        # Add framework line if frameworks exist
                        if project_context["frameworks"]:
                            output_lines.append(f"= • {project_context['frameworks'][0]} framework patterns =")

                        output_lines.extend([
                            "= • Configuration patterns                            =",
                            "=========================================================",
                            "",
                            "== Baseline Metrics ====================================",
                            "= Skill Effectiveness: Baseline established            =",
                            "= Quality Baseline: Will update after first task       =",
                            "= Coverage Baseline: Will update after first task      =",
                            "= Agent Performance: Will track from first delegation  =",
                            "=========================================================",
                            "",
                            "== Next Steps ==========================================",
                            "= 1. Run /analyze:quality to establish quality baseline =",
                            "= 2. Run /analyze:project to analyze project quality   =",
                            "= 3. Start working on tasks - learning begins!         =",
                            "= 4. Each task improves the system automatically       =",
                            "=========================================================",
                            "",
                            "Skills Loaded: pattern-learning, code-analysis",
                            "[OK] Learning system ready! Pattern capture will begin with your first task."
                        ])

                        # Print single consolidated output block
                        print("\n".join(output_lines))

                        return True
                    else:
                        print(f"[ERROR] Script failed: {init_result.get('message', 'Unknown error')}")
                        return False
                else:
                    print(f"[ERROR] Script execution failed: {result.stderr}")
                    return False
            else:
                print(f"[ERROR] Learning script not found: {learning_script}")
                return False

        except Exception as e:
            print(f"[ERROR] Error initializing learning system: {e}")
            print("   Please check permissions and disk space")
            return False

        elif command_info['command'] == 'performance_report':
            # Build Python command for performance report
            cmd = ['python', command_info['script']]
            args = command_info['args']
            cmd.append(args['action'])
            if args['dir'] != '.claude-patterns':
                cmd.extend(['--dir', args['dir']])
            if args['output']:
                cmd.extend(['--output', args['output']])
            if args['days'] != 30:
                cmd.extend(['--days', str(args['days'])])
            return execute_python_command(cmd, "Performance Report")

        elif command_info['command'] == 'organize_workspace':
            # Build Python command for workspace organization
            cmd = ['python', command_info['script']]
            args = command_info['args']
            if args['dry_run']:
                cmd.append('--dry-run')
            if not args['backup']:
                cmd.append('--no-backup')
            if args['target'] != '.':
                cmd.extend(['--target', args['target']])
            return execute_python_command(cmd, "Workspace Organization")

        elif command_info['command'] == 'organize_reports':
            # Build Python command for report organization
            cmd = ['python', command_info['script']]
            args = command_info['args']
            if args['source'] != '.claude/reports':
                cmd.extend(['--source', args['source']])
            if not args['archive_old']:
                cmd.append('--no-archive')
            if args['days_threshold'] != 90:
                cmd.extend(['--days', str(args['days_threshold'])])
            return execute_python_command(cmd, "Report Organization")

        elif command_info['command'] == 'pattern_management':
            # Build Python command for pattern management
            cmd = ['python', command_info['script']]
            args = command_info['args']
            cmd.append(args['action'])
            if args['dir'] != '.claude-patterns':
                cmd.extend(['--dir', args['dir']])
            if args['pattern_type']:
                cmd.extend(['--type', args['pattern_type']])
            if args['export']:
                cmd.extend(['--export', args['export']])
            return execute_python_command(cmd, "Pattern Management")

        elif command_info['command'] == 'smart_recommendations':
            # Build Python command for smart recommendations
            cmd = ['python', command_info['script']]
            args = command_info['args']
            if args['task_description']:
                cmd.extend(['--task', args['task_description']])
            if args['context'] != 'current':
                cmd.extend(['--context', args['context']])
            if args['count'] != 3:
                cmd.extend(['--count', str(args['count'])])
            if not args['show_confidence']:
                cmd.append('--no-confidence')
            return execute_python_command(cmd, "Smart Recommendations")

        elif command_info['command'] == 'plugin_validation':
            # Build Python command for plugin validation
            cmd = ['python', command_info['script']]
            args = command_info['args']
            if args['plugin_path'] != '.':
                cmd.extend(['--path', args['plugin_path']])
            if args['strict_mode']:
                cmd.append('--strict')
            if args['output_format'] != 'table':
                cmd.extend(['--format', args['output_format']])
            return execute_python_command(cmd, "Plugin Validation")

        # Removed: debug_eval, debug_gui, and validate_commands now go through autonomous analysis
        # These complex analytical commands benefit from pattern learning, skill selection, and quality control

        elif command_info['command'] == 'validate_web':
            # Build Python command for web validation
            cmd = ['python', command_info['script']]
            args = command_info['args']
            if args['url']:
                cmd.append(args['url'])
            if args['comprehensive']:
                cmd.append('--comprehensive')
            if args['debug']:
                cmd.append('--debug')
            if args['auto_fix']:
                cmd.append('--auto-fix')
            return execute_python_command(cmd, "Web Validation")

        elif command_info['command'] == 'workspace_distribution_ready':
            # Build Python command for distribution preparation
            cmd = ['python', command_info['script']]
            args = command_info['args']
            if args['target'] != '.':
                cmd.append(args['target'])
            if args['clean']:
                cmd.append('--clean')
            if not args['validate']:
                cmd.append('--no-validate')
            if args['output']:
                cmd.extend(['--output', args['output']])
            return execute_python_command(cmd, "Distribution Preparation")

        # Removed: workspace_improve now goes through autonomous analysis for complex pattern analysis

        elif command_info['command'] == 'workspace_update_about':
            # Build Python command for About section update
            cmd = ['python', command_info['script']]
            args = command_info['args']
            if args['repo']:
                cmd.extend(['--repo', args['repo']])
            if args['description']:
                cmd.extend(['--description', args['description']])
            if args['topics']:
                cmd.extend(['--topics', args['topics']])
            return execute_python_command(cmd, "About Section Update")

        elif command_info['command'] == 'workspace_update_readme':
            # Build Python command for README update
            cmd = ['python', command_info['script']]
            args = command_info['args']
            if args['style'] != 'smart':
                cmd.extend(['--style', args['style']])
            if args['sections']:
                cmd.extend(['--sections', args['sections']])
            return execute_python_command(cmd, "README Update")

        elif command_info['command'].startswith('queue_'):
            # Build Python command for queue operations
            cmd = ['python', command_info['script']]
            args = command_info['args']

            # Base directory
            if args['dir'] != '.claude-patterns':
                cmd.extend(['--dir', args['dir']])

            # Queue action
            action = args['action']
            if action == 'add':
                cmd.append('add')
                if args['name']:
                    cmd.extend(['--name', args['name']])
                if args['description']:
                    cmd.extend(['--description', args['description']])
                if args['command']:
                    cmd.extend(['--command', args['command']])
                if args['priority'] != 'medium':
                    cmd.extend(['--priority', args['priority']])
            elif action == 'slash':
                cmd.append('slash')
                if args['command']:
                    cmd.extend(['--command', args['command']])
                if args['priority'] != 'medium':
                    cmd.extend(['--priority', args['priority']])
            elif action == 'execute':
                cmd.append('execute')
                if args['stop_on_error']:
                    cmd.append('--stop-on-error')
                if args['background']:
                    cmd.append('--background')
            elif action == 'status':
                cmd.append('status')
            elif action == 'list':
                cmd.append('list')
                if args['status']:
                    cmd.extend(['--status', args['status']])
                if args['limit'] != 20:
                    cmd.extend(['--limit', str(args['limit'])])
            elif action == 'clear':
                cmd.append('clear')
                if args['older_than'] != 24:
                    cmd.extend(['--older-than', str(args['older_than'])])
                if args['dry_run']:
                    cmd.append('--dry-run')
            elif action == 'retry':
                cmd.append('retry')
                if args['task_id']:
                    cmd.extend(['--task-id', args['task_id']])
                elif args['status']:
                    cmd.extend(['--status', args['status']])
                    if args['priority']:
                        cmd.extend(['--priority', args['priority']])

            return execute_python_command(cmd, f"Queue {action}")

        elif command_info['command'].startswith('preference_'):
            # Build Python command for preference operations
            cmd = ['python', command_info['script']]
            args = command_info['args']

            # Base directory
            if args['dir'] != '.claude-preferences':
                cmd.extend(['--dir', args['dir']])

            # Preference action
            action = args['action']
            if action == 'set':
                cmd.append('set')
                if args['category']:
                    cmd.extend(['--category', args['category']])
                if args['key']:
                    cmd.extend(['--key', args['key']])
                if args['value']:
                    cmd.extend(['--value', args['value']])
            elif action == 'get':
                cmd.append('get')
                if args['category']:
                    cmd.extend(['--category', args['category']])
                if args['key']:
                    cmd.extend(['--key', args['key']])
            elif action == 'show':
                cmd.append('show')
            elif action == 'profile':
                cmd.append('profile')
            elif action == 'export':
                cmd.append('export')
                if args['export_path']:
                    cmd.extend(['--path', args['export_path']])
                if args['include_sensitive']:
                    cmd.append('--include-sensitive')
            elif action == 'import':
                cmd.append('import')
                if args['import_path']:
                    cmd.extend(['--path', args['import_path']])
                if args['strategy'] != 'merge':
                    cmd.extend(['--strategy', args['strategy']])

            return execute_python_command(cmd, f"Preference {action}")

        elif command_info['command'] == 'generate_suggestions':
            # Build Python command for suggestion generation
            cmd = ['python', command_info['script']]
            args = command_info['args']

            # Base directory
            if args['dir'] != '.claude-preferences':
                cmd.extend(['--dir', args['dir']])

            cmd.append('generate')
            if args['max_suggestions'] != 5:
                cmd.extend(['--max', str(args['max_suggestions'])])
            if args['quality_score'] is not None:
                cmd.extend(['--quality', str(args['quality_score'])])
            if args['project_type']:
                cmd.extend(['--project-type', args['project_type']])
            if not args['include_learning']:
                cmd.append('--no-learning')

            return execute_python_command(cmd, "Generate Suggestions")

    return False

def execute_python_command(cmd, command_name):
    """Helper function to execute Python commands consistently."""
    import subprocess

    try:
        # Consolidate command execution output to prevent empty content blocks
        exec_output = [
            f"[EXEC] Executing {command_name}...",
            f"   Command: {' '.join(cmd)}"
        ]
        print("\n".join(exec_output))

        result = subprocess.run(cmd,
                               capture_output=True,
                               text=True,
                               check=True)

        # Display the output
        if result.stdout:
            print(result.stdout)

        print(f"[OK] {command_name} completed successfully")
        return True

    except subprocess.CalledProcessError as e:
        error_lines = [
            f"[ERROR] Error executing {command_name}: {e}"
        ]
        if e.stderr:
            error_lines.append(f"   Error details: {e.stderr}")
        error_lines.append(f"   Try running manually: {' '.join(cmd)}")
        print("\n".join(error_lines))
        return False

    except FileNotFoundError:
        script_name = cmd[1].split('/')[-1] if len(cmd) > 1 else 'script'
        not_found_lines = [
            f"[ERROR] Script not found: {script_name}",
            f"   Ensure {script_name} exists in lib/ directory",
            f"   Try running manually: {' '.join(cmd)}"
        ]
        print("\n".join(not_found_lines))
        return False

    except Exception as e:
        exception_lines = [
            f"[ERROR] Unexpected error: {e}",
            f"   Try running manually: {' '.join(cmd)}"
        ]
        print("\n".join(exception_lines))
        return False
```

**Command Handling Workflow**:
1. **First Priority**: Check if input is a special command
2. **If special**: Execute directly using appropriate handler
3. **If not special**: Continue with normal autonomous analysis

### 6. Multi-Agent Delegation

Delegate to specialized agents autonomously:

**Code Analysis Tasks** → `code-analyzer` agent
- Analyzes code structure and identifies issues
- Has access to: pattern-learning, code-analysis skills

**Quality Control Tasks** → `quality-controller` agent
- Runs tests, checks standards, validates documentation
- Has access to: quality-standards, testing-strategies skills

**Background Tasks** → `background-task-manager` agent
- Runs long-running analysis and optimization
- Operates independently in background

**Documentation Tasks** → `documentation-generator` agent
- Generates and updates documentation
- Has access to: documentation-best-practices skill

**Testing Tasks** → `test-engineer` agent
- Creates and runs test suites
- Has access to: testing-strategies skill

**Validation Tasks** → `validation-controller` agent
- **AUTOMATICALLY triggered before Edit/Write operations**
- Validates tool prerequisites (e.g., file read before edit)
- Checks documentation consistency
- Detects execution failures and suggests auto-fixes
- **Pre-flight validation** prevents common errors
- **Post-error analysis** when tool failures occur
- Has access to: validation-standards skill

**Enhanced Automatic Learning** → `learning-engine` agent
- **AUTOMATICALLY triggered after EVERY task completion** (v3.0 enhanced)
- Captures rich contextual patterns with project fingerprinting
- Updates skill effectiveness metrics with confidence scoring
- Updates agent performance metrics with reliability tracking
- Trains predictive models for skill selection (after 20+ patterns)
- Contributes to cross-project knowledge base
- Analyzes learning velocity and improvement trends
- Generates actionable insights from pattern data
- **NO user-facing output** - pure background learning
- **Exponential improvement** through predictive intelligence

### 7. Self-Assessment & Quality Control

**Autonomous Quality Checks**:
After each task completion, automatically:
1. ✓ Run automated tests (if test suite exists)
2. ✓ Check code against established standards
3. ✓ Verify documentation completeness
4. ✓ Validate against learned patterns
5. ✓ Self-assess quality score (0-100)

**Quality Score Calculation**:
```
Quality Score = (
  tests_passing * 0.3 +
  standards_compliance * 0.25 +
  documentation_complete * 0.20 +
  pattern_adherence * 0.15 +
  code_quality_metrics * 0.10
)
```

**Auto-Correction**:
- IF quality_score < 70: Automatically delegate to quality-controller for fixes
- IF tests failing: Auto-delegate to test-engineer to fix tests
- IF documentation incomplete: Auto-delegate to documentation-generator
- ELSE: Mark task as complete and store success pattern

### 6. Background Task Management

Automatically identify and run background tasks:

**Auto-Triggered Background Tasks**:
- Code analysis and complexity metrics
- Documentation gap analysis
- Test coverage analysis
- Performance profiling
- Security scanning
- Refactoring opportunity detection

**Background Execution**:
- Delegate to `background-task-manager` agent
- Run in parallel with main workflow
- Collect results and integrate findings
- Store insights in pattern database

