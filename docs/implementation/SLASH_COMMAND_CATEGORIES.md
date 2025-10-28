# Slash Command Categories

## Direct Execution Commands (Handled by Orchestrator)

These commands use direct Python script execution for speed and immediate response. They bypass the full autonomous analysis pipeline.

### Infrastructure & Monitoring
- `/monitor:dashboard` - Launch web dashboard service
- `/learn:analytics` - Display learning analytics reports
- `/learn:performance` - Show performance reports

### Utilities & Organization
- `/workspace:organize` - Organize workspace files
- `/workspace:reports` - Manage report files
- `/learn:patterns` - Pattern management operations
- `/monitor:recommend` - Simple recommendations
- `/validate:plugin` - Basic plugin validation

**Why Direct Execution?**
- ✅ Simple, well-defined operations
- ✅ Require immediate response
- ✅ Don't need complex analysis or learning
- ✅ Infrastructure/utility functions
- ✅ Performance critical (dashboard startup)

## Full Autonomous Analysis Commands

These commands go through the complete autonomous analysis pipeline with pattern learning, skill selection, and quality control.

### Development & Release
- `/dev:auto` - Autonomous development workflow
- `/dev:release` - Release preparation and publishing
- `/dev:model-switch` - Model switching operations

### Comprehensive Analysis
- `/analyze:project` - Complete project analysis
- `/analyze:quality` - Quality assessment and control
- `/analyze:dependencies` - Dependency vulnerability scanning
- `/analyze:static` - Static code analysis

### Advanced Validation
- `/validate:fullstack` - Full-stack validation with auto-fix
- `/validate:all` - Comprehensive validation audit
- `/validate:patterns` - Pattern validation and optimization

### Complex Debugging
- `/debug:gui` - GUI debugging and diagnostics
- `/debug:eval` - Evaluation debugging

### Strategic Tasks
- `/pr-review` - Pull request review
- `/improve-plugin` - Plugin improvement analysis

**Why Full Autonomous Analysis?**
- ✅ Complex, multi-step operations
- ✅ Benefit from pattern learning and historical data
- ✅ Require adaptive approach and skill selection
- ✅ Need quality control and validation
- ✅ Showcase autonomous agent capabilities

## Architecture Benefits

This separation provides:

1. **Performance**: Critical infrastructure commands start instantly
2. **Intelligence**: Complex tasks benefit from learning and adaptation
3. **Maintainability**: Clear distinction between utilities and complex operations
4. **User Experience**: Fast response for simple tasks, thorough analysis for complex ones
5. **Scalability**: Easy to add new commands to either category

## Implementation Details

- Direct execution commands are handled first in `detect_special_command()`
- They use specific Python scripts in `lib/` directory
- Full autonomous commands continue through the normal orchestrator workflow
- Both paths integrate with the learning system for pattern storage