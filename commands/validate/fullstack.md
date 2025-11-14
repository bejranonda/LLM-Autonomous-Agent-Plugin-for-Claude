---
name: validate:fullstack
description: Validate full-stack app (backend, frontend, database, API contracts) with auto-fix
delegates-to: autonomous-agent:orchestrator
---

# Validate Full-Stack Command

**Slash command**: `/validate:fullstack`

**Description**: Comprehensive validation workflow for full-stack applications. Automatically detects project structure, runs parallel validation for all components, validates API contracts, and auto-fixes common issues.

## What This Command Does

This command orchestrates a complete validation workflow for multi-component applications:

1. **Project Detection** (5-10 seconds)
   - Identifies all technology components (backend, frontend, database, infrastructure)
   - Detects frameworks and build tools
   - Maps project structure

2. **Parallel Component Validation** (30-120 seconds)
   - Backend: Dependencies, type hints, tests, API schema, database migrations
   - Frontend: TypeScript, build, dependencies, bundle size
   - Database: Schema, test isolation, query efficiency
   - Infrastructure: Docker services, environment variables

3. **Cross-Component Validation** (15-30 seconds)
   - API contract synchronization (frontend ↔ backend)
   - Environment variable consistency
   - Authentication flow validation

4. **Auto-Fix Application** (10-30 seconds)
   - TypeScript unused imports removal
   - SQLAlchemy text() wrapper addition
   - React Query syntax updates
   - Build configuration fixes
   - Environment variable generation

5. **Quality Assessment** (5-10 seconds)
   - Calculate quality score (0-100)
   - Generate prioritized recommendations
   - Create comprehensive report

## When to Use This Command

**Ideal scenarios**:
- Before deploying full-stack applications
- After significant code changes
- Setting up CI/CD pipelines
- Onboarding new team members
- Periodic quality checks

**Project types**:
- Monorepos with backend + frontend
- Separate repos with Docker Compose
- Microservices architectures
- Full-stack web applications

## Execution Flow

```
User runs: /validate:fullstack

v

Orchestrator Agent:
  1. Load skills: fullstack-validation, code-analysis, quality-standards
  2. Detect project structure
  3. Create validation plan

v

Parallel Execution (background-task-manager):
  +- [Frontend-Analyzer] TypeScript + Build validation
  +- [Test-Engineer] Backend tests + coverage
  +- [Quality-Controller] Code quality checks
  +- [Build-Validator] Build config validation

v

Sequential Execution:
  1. [API-Contract-Validator] Frontend ↔ Backend synchronization
  2. [Quality-Controller] Cross-component quality assessment

v

Auto-Fix Loop (if quality score < 70):
  1. Apply automatic fixes
  2. Re-run validation
  3. Repeat until quality ≥ 70 or max 3 attempts

v

Results:
  - Terminal: Concise summary (15-20 lines)
  - File: Detailed report saved to .claude/data/reports/
  - Pattern Storage: Store results for future learning
```

## Expected Output

### Terminal Output (Concise)

```
✅ Full-Stack Validation Complete (2m 34s)

📊 Component Status:
+- Backend (FastAPI): ✅ 96/100 (42% coverage -> target 70%)
+- Frontend (React): ✅ 87/100 (0 errors, 882KB bundle)
+- API Contract: ✅ 23/23 endpoints matched

🔧 Auto-Fixed (11 issues):
[PASS] Removed 5 unused TypeScript imports
[PASS] Added text() wrapper to 3 SQL queries
[PASS] Fixed 2 React Query v5 syntax
[PASS] Generated vite-env.d.ts

[WARN]️  Recommended (2 actions):
1. Increase test coverage to 70% (currently 42%)
2. Add indexes to users.email, projects.created_at

🎯 Overall Score: 87/100 (Production Ready)

📄 Detailed report: .claude/data/reports/validate-fullstack-2025-10-22.md
```

### Detailed Report (File)

Saved to `.claude/data/reports/validate-fullstack-YYYY-MM-DD.md`:

- Complete project structure analysis
- All validation results with metrics
- Every issue found (auto-fixed and remaining)
- Complete recommendations with implementation examples
- Performance metrics and timing breakdown
- Pattern learning insights
- Historical comparison (if available)

## Auto-Fix Capabilities

### Automatically Fixed (No Confirmation)

| Issue | Detection | Fix | Success Rate |
|-------|-----------|-----|--------------|
| Unused TypeScript imports | ESLint | Remove import | 100% |
| Raw SQL strings | Regex | Add text() wrapper | 100% |
| ESM in .js file | File check | Rename to .mjs | 95% |
| Missing vite-env.d.ts | File check | Generate file | 100% |
| Database CASCADE | Error message | Add CASCADE | 100% |
| Missing .env.example | Env var scan | Generate file | 100% |

### Suggested Fixes (Confirmation Needed)

| Issue | Detection | Fix | Success Rate |
|-------|-----------|-----|--------------|
| React Query v4 syntax | Pattern match | Update to v5 | 92% |
| Missing type hints | mypy | Add annotations | 70% |
| Missing error handling | Pattern match | Add try-catch | 88% |
| Large bundle size | Size analysis | Code splitting | 85% |
| API contract mismatch | Schema compare | Generate types | 95% |

## Quality Score Calculation

```
Total Score (0-100):
+- Component Scores (60 points):
|  +- Backend: 20 points max
|  +- Frontend: 20 points max
|  +- Integration: 20 points max
+- Test Coverage (15 points):
|  +- 70%+ = 15, 50-69% = 10, <50% = 5
+- Auto-Fix Success (15 points):
|  +- All fixed = 15, Some fixed = 10, None = 0
+- Best Practices (10 points):
   +- Documentation, types, standards

Threshold:
✅ 70-100: Production Ready
[WARN]️  50-69: Needs Improvement
❌ 0-49: Critical Issues
```

## Configuration Options

Create `.claude/config/fullstack-validation.json` to customize:

```json
{
  "coverage_target": 70,
  "quality_threshold": 70,
  "auto_fix": {
    "typescript_imports": true,
    "sqlalchemy_text": true,
    "react_query_syntax": false,
    "build_configs": true
  },
  "parallel_validation": true,
  "max_auto_fix_attempts": 3,
  "skip_components": [],
  "custom_validators": []
}
```

## Integration with Other Commands

**Before `/validate:fullstack`**:
- `/learn:init` - Initialize pattern learning

**After `/validate:fullstack`**:
- `/analyze:quality` - Deep dive into specific issues
- `/learn:performance` - Analyze performance trends

**Complementary**:
- `/monitor:recommend` - Get workflow suggestions based on validation results

## Success Criteria

Validation is considered successful when:
- ✅ All components validated
- ✅ Quality score ≥ 70/100
- ✅ No critical issues remaining
- ✅ API contracts synchronized
- ✅ Auto-fix success rate > 80%
- ✅ Execution time < 3 minutes

## Troubleshooting

**Validation takes too long (>5 min)**:
- Check for slow tests (timeout after 2 min)
- Disable parallel validation if causing issues
- Skip non-critical components

**Auto-fix failures**:
- Review `.claude/data/reports/` for detailed error messages
- Check autofix-patterns.json for pattern success rates
- Manual fixes may be required for complex issues

**Quality score unexpectedly low**:
- Review individual component scores
- Check test coverage (often the bottleneck)
- Review recommendations for quick wins

## Pattern Learning

This command automatically stores patterns for:
- Project structure (for faster detection next time)
- Common issues (for better detection)
- Auto-fix success rates (for reliability improvement)
- Validation performance (for optimization)

After 5-10 runs on similar projects, validation becomes significantly faster and more accurate.

## Example Use Cases

**Use Case 1: Pre-Deployment Check**
```bash
/validate:fullstack
# Wait for validation
# Review score and recommendations
# If score ≥ 70: Deploy
# If score < 70: Address critical issues and re-validate
```

**Use Case 2: CI/CD Integration**
```bash
# In CI pipeline
claude-code /validate:fullstack --ci-mode
# Exit code 0 if score ≥ 70
# Exit code 1 if score < 70
```

**Use Case 3: Code Review Preparation**
```bash
/validate:fullstack
# Auto-fixes applied automatically
# Review recommendations
# Commit fixes
# Create PR with validation report
```

## Performance Benchmarks

Typical execution times for different project sizes:

| Project Size | Components | Validation Time |
|--------------|------------|-----------------|
| Small | Backend + Frontend | 45-60 seconds |
| Medium | Backend + Frontend + DB | 90-120 seconds |
| Large | Microservices + Frontend | 120-180 seconds |
| Extra Large | Complex monorepo | 180-240 seconds |

Auto-fix adds 10-30 seconds depending on issue count.

## Version History

- **v2.0.0**: Full-stack validation with auto-fix capabilities
- **v2.2.0** (planned): Docker container validation
- **v2.2.0** (planned): Security vulnerability scanning
- **v2.3.0** (planned): Performance profiling integration

---

**Note**: This command requires the following agents to be available:
- `autonomous-agent:orchestrator`
- `autonomous-agent:frontend-analyzer`
- `autonomous-agent:api-contract-validator`
- `autonomous-agent:build-validator`
- `autonomous-agent:test-engineer`
- `autonomous-agent:quality-controller`
- `autonomous-agent:background-task-manager`

All agents are included in the autonomous-agent plugin v2.0+.
