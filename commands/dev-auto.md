---
name: dev:auto
description: Command for dev auto
delegates-to: orchestrator
---


# Dev-Auto Command

## Command: `/dev:auto`

Fully autonomous development from requirements to release-ready implementation. This command handles the entire development lifecycle including planning, implementation, testing, debugging, validation, and optional release - all automatically with minimal human intervention.

**🤖 Full Autonomous Development:**
- **Zero to Release**: From user requirement to production-ready code
- **Incremental Development**: Commits each working milestone
- **Continuous Validation**: Tests and validates at every step
- **Auto-Debugging**: Automatically fixes failures and bugs
- **Quality Assurance**: Ensures ≥ 85/100 quality score
- **Learning Integration**: Improves from every development cycle

## How It Works

1. **Requirements Analysis**: Breaks down user requirements into implementable tasks
2. **Development Planning**: Creates phased development plan with milestones
3. **Incremental Implementation**: Implements each milestone with automatic commits
4. **Continuous Testing**: Tests after each change, debugs automatically if failed
5. **Parameter Validation**: Validates consistency (common failure point)
6. **Quality Control**: Runs quality checks, auto-fixes issues
7. **Requirements Verification**: Ensures implementation matches requirements
8. **Optional Release**: Can trigger `/release-dev` when complete

## Usage

### Basic Usage
```bash
# Simple feature request
/dev:auto "add MQTT broker with certificate support"

# Complex feature with multiple parts
/dev:auto "implement user authentication with JWT, including login, logout, and token refresh"

# Bug fix with testing
/dev:auto "fix memory leak in data processing module and add comprehensive tests"

# Refactoring task
/dev:auto "refactor authentication module to use dependency injection pattern"
```

### Advanced Options
```bash
# Development with automatic release
/dev:auto "add email notification system" --auto-release

# Specify quality threshold (default: 85)
/dev:auto "add caching layer" --quality-threshold 90

# Maximum debug iterations per milestone (default: 5)
/dev:auto "fix login bug" --max-debug-iterations 3

# Skip tests (not recommended)
/dev:auto "update documentation" --skip-tests

# Verbose logging for debugging
/dev:auto "implement API endpoint" --verbose

# Dry run (planning only, no implementation)
/dev:auto "add OAuth support" --dry-run
```

### Incremental Commit Options
```bash
# Commit frequency
/dev:auto "large feature" --commit-per-milestone  # Default
/dev:auto "large feature" --commit-per-file       # More frequent
/dev:auto "large feature" --commit-per-step       # Very frequent

# Skip commits (single commit at end)
/dev:auto "small feature" --no-incremental-commits
```

### Testing Options
```bash
# Test types to run
/dev:auto "add API" --run-unit-tests --run-integration-tests
/dev:auto "add UI" --run-e2e-tests

# Test coverage requirement (default: 80%)
/dev:auto "add feature" --test-coverage 90

# Generate tests automatically
/dev:auto "add feature" --auto-generate-tests
```

## Development Workflow

### Phase 1: Requirements Analysis (10-30 seconds)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 REQUIREMENTS ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User Request: "add MQTT broker with certificate support"

Requirement Breakdown:
├─ 1. MQTT Broker Setup
│  ├─ Dependencies: paho-mqtt or similar
│  ├─ Configuration: broker URL, port, credentials
│  └─ Complexity: Medium
│
├─ 2. Certificate Management
│  ├─ SSL/TLS certificate loading
│  ├─ Certificate validation
│  ├─ Secure storage of credentials
│  └─ Complexity: Medium
│
├─ 3. Connection Management
│  ├─ Connect/disconnect logic
│  ├─ Reconnection handling
│  ├─ Connection state monitoring
│  └─ Complexity: Medium
│
├─ 4. Message Publishing/Subscribing
│  ├─ Topic management
│  ├─ QoS handling
│  ├─ Error handling
│  └─ Complexity: Medium
│
└─ 5. Testing & Documentation
   ├─ Unit tests
   ├─ Integration tests
   ├─ Documentation
   └─ Complexity: Simple

Technology Stack Detected:
├─ Language: Python (detected from project)
├─ Framework: Flask/FastAPI (if web API)
├─ MQTT Library: paho-mqtt (recommended)
└─ Testing: pytest

Estimated Time: 45-90 minutes
Milestones: 5 major milestones
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 2: Development Planning (5-10 seconds)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📐 DEVELOPMENT PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Development Strategy: Incremental with milestones

Milestone 1: Dependencies & Configuration
├─ Install paho-mqtt library
├─ Create configuration module
├─ Add certificate path configuration
├─ Estimated: 10 minutes
└─ Commit: "feat: add MQTT dependencies and configuration"

Milestone 2: Certificate Management
├─ Implement certificate loader
├─ Add certificate validation
├─ Implement secure storage
├─ Estimated: 15 minutes
└─ Commit: "feat: implement certificate management for MQTT"

Milestone 3: MQTT Connection Layer
├─ Implement connection class
├─ Add connect/disconnect methods
├─ Implement reconnection logic
├─ Add connection state monitoring
├─ Estimated: 20 minutes
└─ Commit: "feat: implement MQTT connection with auto-reconnect"

Milestone 4: Publish/Subscribe Interface
├─ Implement publish method
├─ Implement subscribe method
├─ Add topic management
├─ Handle QoS levels
├─ Estimated: 20 minutes
└─ Commit: "feat: add MQTT publish/subscribe interface"

Milestone 5: Testing & Documentation
├─ Write unit tests
├─ Write integration tests
├─ Update documentation
├─ Add usage examples
├─ Estimated: 15 minutes
└─ Commit: "test: add comprehensive MQTT tests and docs"

Success Criteria:
├─ ✅ All tests pass (100%)
├─ ✅ Certificate validation works
├─ ✅ Reconnection logic tested
├─ ✅ Documentation complete
└─ ✅ Quality score ≥ 85/100

Starting development in 3 seconds...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 3: Incremental Development Loop

Each milestone follows this loop:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔨 MILESTONE 1/5: Dependencies & Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[IMPLEMENTATION]
Creating mqtt_config.py...
├─ ✅ Configuration class created
├─ ✅ Environment variable support added
├─ ✅ Certificate path validation added
└─ ✅ Default values configured

Creating requirements.txt entry...
├─ ✅ Added: paho-mqtt==1.6.1
└─ ✅ Updated lock file

[VALIDATION]
Parameter Consistency Check:
├─ ✅ Config parameter names consistent
├─ ✅ Type hints correct
└─ ✅ No undefined variables

[TESTING]
Running unit tests...
├─ test_config_loading: ✅ PASS
├─ test_certificate_path_validation: ✅ PASS
├─ test_env_variable_loading: ✅ PASS
└─ Test Coverage: 95% (target: 80%)

[QUALITY CHECK]
├─ Code Quality: 92/100 ✅
├─ Standards: ✅ PEP 8 compliant
├─ Documentation: ✅ Docstrings present
└─ Security: ✅ No vulnerabilities

[COMMIT]
├─ Staging files: 3 files
├─ Commit message: "feat: add MQTT dependencies and configuration"
├─ Commit hash: abc1234
└─ ✅ Pushed to origin/main

Milestone 1: ✅ COMPLETE (elapsed: 8m 32s)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔨 MILESTONE 2/5: Certificate Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[IMPLEMENTATION]
Creating mqtt_certificates.py...
├─ ✅ CertificateLoader class created
├─ ✅ SSL context configuration
├─ ✅ Certificate validation logic
└─ ✅ Error handling added

[VALIDATION]
Parameter Consistency Check:
├─ ✅ Certificate parameters match config
├─ ✅ SSL context options consistent
└─ ✅ Error messages standardized

[TESTING]
Running unit tests...
├─ test_certificate_loading: ✅ PASS
├─ test_invalid_certificate: ✅ PASS
├─ test_certificate_validation: ❌ FAIL
│  └─ Error: SSL certificate verification failed
└─ Test Coverage: 88%

[DEBUG LOOP - Iteration 1]
Analyzing failure...
├─ Root Cause: Certificate path mismatch
├─ Issue: Using absolute path instead of relative
└─ Fix: Update certificate path resolution

Applying fix...
├─ ✅ Updated path resolution logic
└─ ✅ Added path normalization

Re-running tests...
├─ test_certificate_loading: ✅ PASS
├─ test_invalid_certificate: ✅ PASS
├─ test_certificate_validation: ✅ PASS
└─ Test Coverage: 92%

[QUALITY CHECK]
├─ Code Quality: 90/100 ✅
├─ Security: ✅ No hardcoded credentials
└─ Documentation: ✅ Complete

[COMMIT]
├─ Commit message: "feat: implement certificate management for MQTT"
├─ Commit hash: def5678
└─ ✅ Pushed to origin/main

Milestone 2: ✅ COMPLETE (elapsed: 12m 45s)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

... (Milestones 3-5 continue similarly) ...
```

### Phase 4: Requirements Verification (20-40 seconds)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ REQUIREMENTS VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Original Request: "add MQTT broker with certificate support"

Implementation Checklist:
├─ ✅ MQTT broker connection implemented
│  ├─ ✅ Connect method working
│  ├─ ✅ Disconnect method working
│  └─ ✅ Auto-reconnection implemented
│
├─ ✅ Certificate support implemented
│  ├─ ✅ SSL/TLS certificates loaded
│  ├─ ✅ Certificate validation working
│  └─ ✅ Secure credential storage
│
├─ ✅ Message handling implemented
│  ├─ ✅ Publish method working
│  ├─ ✅ Subscribe method working
│  └─ ✅ QoS levels supported
│
├─ ✅ Error handling complete
│  ├─ ✅ Connection errors handled
│  ├─ ✅ Certificate errors handled
│  └─ ✅ Message errors handled
│
└─ ✅ Testing complete
   ├─ ✅ Unit tests: 24/24 passing
   ├─ ✅ Integration tests: 6/6 passing
   └─ ✅ Test coverage: 94%

Quality Metrics:
├─ Code Quality: 92/100 ✅ (threshold: 85)
├─ Test Coverage: 94% ✅ (threshold: 80%)
├─ Documentation: 90/100 ✅
├─ Security: 95/100 ✅
└─ Overall: 92/100 ✅

Completeness: 100% ✅
All requirements satisfied!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 5: Final Report (10 seconds)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ AUTONOMOUS DEVELOPMENT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Requirement: add MQTT broker with certificate support
⏱️  Total Time: 48m 32s
🔄 Iterations: 1 (1 debug loop in Milestone 2)
📊 Final Quality: 92/100

✨ Implemented:
├─ MQTT broker connection with auto-reconnect
├─ SSL/TLS certificate management and validation
├─ Publish/Subscribe interface with QoS support
├─ Comprehensive error handling
└─ Complete documentation and usage examples

📦 Files Created/Modified:
├─ mqtt_config.py (new)
├─ mqtt_certificates.py (new)
├─ mqtt_client.py (new)
├─ tests/test_mqtt.py (new)
├─ requirements.txt (modified)
└─ README.md (modified)

✅ Tests: 30/30 passing (100%)
├─ Unit tests: 24/24
└─ Integration tests: 6/6

📚 Documentation: 90/100
├─ API documentation complete
├─ Usage examples added
└─ Configuration guide included

🔒 Security: 95/100
├─ No hardcoded credentials
├─ Secure certificate storage
└─ Proper SSL/TLS configuration

🐛 Issues Fixed: 1
└─ Certificate path resolution (Milestone 2)

📊 Code Metrics:
├─ Lines Added: 486
├─ Lines Modified: 23
├─ Test Coverage: 94%
└─ Cyclomatic Complexity: Low

🔄 Commits: 5 incremental commits
├─ abc1234: feat: add MQTT dependencies and configuration
├─ def5678: feat: implement certificate management for MQTT
├─ ghi9012: feat: implement MQTT connection with auto-reconnect
├─ jkl3456: feat: add MQTT publish/subscribe interface
└─ mno7890: test: add comprehensive MQTT tests and docs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 SUGGESTED NEXT ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [High Priority] Test MQTT integration end-to-end
   → /dev:auto "add integration tests for MQTT with real broker"

2. [Recommended] Release this feature
   → /dev:release --minor

3. [Optional] Add monitoring for MQTT connection
   → /dev:auto "add prometheus metrics for MQTT"

4. [Learning] View development analytics
   → /learn:performance

Choose option (1-4) or type custom command:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Optional: Auto-Release (if --auto-release flag used)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 AUTO-RELEASE TRIGGERED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Triggering /dev:release...

[Release workflow output here - see /dev:release docs]

Release: v3.5.1 ✅
Links:
├─ GitHub: https://github.com/user/repo/releases/tag/v3.5.1
└─ Changelog: https://github.com/user/repo/blob/main/CHANGELOG.md

Total Time (dev + release): 51m 15s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Debug Loop Details

When tests fail, the debug loop automatically:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 DEBUG LOOP - Iteration 1/5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test Failure Detected:
├─ Test: test_mqtt_publish
├─ Error: ConnectionRefusedError: [Errno 111] Connection refused
└─ Stack Trace: [truncated for brevity]

[ANALYSIS]
Root Cause Analysis:
├─ Category: Integration Error
├─ Specific Issue: MQTT broker not running
├─ Affected Component: mqtt_client.py:45
└─ Similar Patterns: Found 3 similar issues in patterns

Recommended Fix:
├─ Option 1: Add connection retry logic (recommended)
├─ Option 2: Mock MQTT broker for tests
└─ Option 3: Skip integration tests in CI

Selected Fix: Option 1 (best success rate: 95%)

[IMPLEMENTATION]
Applying fix...
├─ ✅ Added exponential backoff retry
├─ ✅ Maximum 3 retry attempts
├─ ✅ Configurable retry delay
└─ ✅ Logging for retry attempts

[VALIDATION]
Parameter Consistency:
├─ ✅ Retry parameters consistent
├─ ✅ Timeout values aligned
└─ ✅ Error messages standardized

[RE-TEST]
Running tests again...
├─ test_mqtt_publish: ✅ PASS
├─ test_mqtt_subscribe: ✅ PASS
└─ All tests: 30/30 passing

Debug Loop: ✅ SUCCESS (resolved in 1 iteration)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If debug loop fails after max iterations:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  DEBUG LOOP - MAX ITERATIONS REACHED (5/5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Unable to resolve issue automatically.

Issue Summary:
├─ Test: test_complex_reconnection_logic
├─ Error: Intermittent connection timeout
├─ Attempts: 5 different fixes tried
└─ Success Rate: 0/5

Attempted Fixes:
1. Increased timeout values - Failed
2. Added connection pooling - Failed
3. Implemented circuit breaker - Failed
4. Adjusted retry backoff - Failed
5. Modified SSL handshake - Failed

Manual Intervention Required:
This appears to be a complex integration issue that requires
human analysis. The following information has been collected:

Detailed Error Report: .claude/reports/debug-failure-2025-01-24.md
Code Changes Applied: 5 incremental commits
Test Logs: .claude/logs/test-failures.log

Recommendations for Manual Fix:
1. Review MQTT broker configuration
2. Check network connectivity and firewall rules
3. Verify SSL certificate chain is complete
4. Test with different MQTT broker versions

Would you like to:
1. Continue with partial implementation (current milestone only)
2. Rollback all changes and report issue
3. Commit current state for manual fix later

Choose option (1-3):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Parameter Validation

Critical validation performed automatically:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 PARAMETER VALIDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checking parameter consistency across codebase...

Function Call Analysis:
├─ mqtt_connect(broker_url, port, username, password)
├─ Used in 8 locations
└─ ✅ All parameters match function signature

Configuration Validation:
├─ Config file: mqtt_config.py
├─ Environment variables: .env
├─ Function parameters: mqtt_client.py
└─ ✅ All parameter names consistent

Type Safety Check:
├─ Type hints present: ✅ 100%
├─ Type consistency: ✅ All correct
└─ ✅ No type mismatches found

Null Safety Check:
├─ Null checks present: ✅ All critical paths
├─ Default values defined: ✅ All optional params
└─ ✅ No null pointer risks

Common Failure Patterns:
├─ ✅ No undefined variables
├─ ✅ No parameter name typos
├─ ✅ No missing required parameters
└─ ✅ No type conversion errors

Parameter Validation: ✅ PASS (100%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Integration with Learning System

The `/dev-auto` command deeply integrates with pattern learning:

**Learning from Success**:
- Successful implementation approaches
- Effective milestone breakdown strategies
- Optimal test coverage strategies
- Best debugging techniques
- Common parameter patterns

**Learning from Failure**:
- Failed debug attempts
- Ineffective implementation patterns
- Common error causes
- Integration pitfalls
- Time-consuming approaches to avoid

**Pattern Storage**:
```json
{
  "dev_auto_patterns": {
    "task_type": "mqtt_integration",
    "successful_approach": {
      "milestones": 5,
      "avg_milestone_time": "9.7 minutes",
      "total_time": "48.5 minutes",
      "debug_iterations": 1,
      "quality_score": 92
    },
    "common_issues": [
      {
        "issue": "certificate_path_mismatch",
        "frequency": 0.65,
        "fix_success_rate": 0.95,
        "recommended_fix": "use_relative_paths"
      }
    ],
    "skill_effectiveness": {
      "code-analysis": 0.94,
      "testing-strategies": 0.91,
      "security-patterns": 0.88
    },
    "reuse_count": 12,
    "average_improvement": "+18% quality, -23% time"
  }
}
```

## Integration with Other Commands

### Complete Development Workflow
```bash
# Plan feature
/dev:auto "add feature" --dry-run

# Implement feature
/dev:auto "add feature"

# Validate quality
/analyze:quality

# Release
/dev:release
```

### With Validation Commands
```bash
# Development with validation
/dev:auto "implement API"
/validate:fullstack
/analyze:static
```

### With Learning Commands
```bash
# Check development patterns
/learn:analytics

# Development with pattern awareness
/dev:auto "similar feature to previous"

# Review performance
/learn:performance
```

## Agent Delegation

`/dev-auto` delegates to specialized agents:

- **code-analyzer**: For code structure analysis
- **test-engineer**: For test generation and debugging
- **quality-controller**: For quality validation and auto-fix
- **documentation-generator**: For documentation updates
- **security-auditor**: For security validation
- **frontend-analyzer**: For frontend-specific tasks
- **api-contract-validator**: For API contract validation
- **build-validator**: For build configuration

## Skills Integration

Auto-loads relevant skills based on task:

- **code-analysis**: For implementation guidance
- **testing-strategies**: For comprehensive testing
- **quality-standards**: For quality compliance
- **security-patterns**: For security best practices
- **documentation-best-practices**: For documentation
- **pattern-learning**: For continuous improvement
- **autonomous-development**: For development strategies

## Best Practices

### Writing Good Requirements
```bash
# Good: Specific and actionable
/dev:auto "add REST API endpoint for user registration with email validation"

# Bad: Too vague
/dev:auto "make the app better"

# Good: Clear scope
/dev:auto "refactor database layer to use repository pattern"

# Bad: Too broad
/dev:auto "fix everything"

# Good: Includes acceptance criteria
/dev:auto "add caching with Redis, must support TTL and invalidation"
```

### When to Use --auto-release
- Small, isolated features
- Bug fixes
- Documentation updates
- Non-breaking changes

### When NOT to Use --auto-release
- Major features requiring review
- Breaking changes
- Security-critical changes
- Changes requiring team discussion

### Quality Thresholds
- **85 (default)**: Production-ready standard
- **90**: High-quality applications
- **95**: Mission-critical systems
- **80**: Development/testing environments

## Troubleshooting

### Development Stuck in Loop
```bash
# Check current status
/dev:auto status

# Force exit debug loop
/dev:auto abort

# View detailed logs
cat .claude/logs/dev-auto-current.log
```

### Tests Keep Failing
```bash
# Increase max debug iterations
/dev:auto "feature" --max-debug-iterations 10

# Skip specific test types
/dev:auto "feature" --skip-integration-tests

# Manual fix mode
/dev:auto "feature" --manual-fix-on-failure
```

### Quality Check Fails
```bash
# Lower threshold temporarily
/dev:auto "feature" --quality-threshold 75

# Skip quality check (not recommended)
/dev:auto "feature" --skip-quality-check

# Run quality check separately
/analyze:quality
```

## Performance Metrics

Expected performance:

| Task Type | Avg Time | Success Rate | Iterations |
|-----------|----------|--------------|------------|
| Small Feature | 15-30 min | 95% | 0-1 |
| Medium Feature | 30-60 min | 88% | 1-2 |
| Large Feature | 1-3 hours | 78% | 2-4 |
| Bug Fix | 10-20 min | 92% | 0-1 |
| Refactoring | 20-45 min | 85% | 1-2 |

Success rate improves with learning:
- First 5 similar tasks: 75-80%
- After 10 similar tasks: 85-90%
- After 25 similar tasks: 90-95%

---

**Version**: 1.0.0
**Integration**: Uses orchestrator, test-engineer, quality-controller, code-analyzer agents
**Skills**: code-analysis, testing-strategies, quality-standards, autonomous-development
**Platform**: Cross-platform (Windows, Linux, Mac)
**Learning**: Full integration with pattern learning system
