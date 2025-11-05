---
name: learn:clone
description: Clone and learn features from external repos to implement in current project
delegates-to: autonomous-agent:dev-orchestrator
---

# Learn-Clone Command

## Command: `/learn:clone`

**Feature cloning through learning** - Analyzes features and capabilities in external GitHub/GitLab repositories, understands their implementation, and helps implement similar or equivalent functionality in the current project while respecting licenses and best practices.

**🔄 Intelligent Feature Cloning:**
- **Feature Analysis**: Deep understanding of how features work
- **Implementation Extraction**: Learn implementation patterns
- **Adaptation**: Adapt features to current project context
- **License Compliance**: Respect and comply with source licenses
- **Best Practice Integration**: Implement using current project standards
- **Testing Strategy**: Learn and adapt testing approaches

## How It Works

1. **Feature Identification**: Analyzes target repository for specific features
2. **Implementation Study**: Studies how features are implemented
3. **Pattern Extraction**: Extracts implementation patterns and approaches
4. **Adaptation Planning**: Plans how to adapt to current project
5. **Implementation**: Implements similar functionality (with attribution)
6. **Testing**: Adapts testing strategies from source
7. **Documentation**: Documents learnings and implementation

## Usage

### Basic Usage
```bash
# Clone specific feature from repository
/learn:clone https://github.com/user/repo --feature "JWT authentication"

# Clone multiple features
/learn:clone https://github.com/user/repo --features "auth,caching,rate-limiting"

# Learn implementation approach
/learn:clone https://github.com/user/repo --feature "real-time notifications" --learn-only
```

### With Implementation
```bash
# Clone and implement immediately
/learn:clone https://github.com/user/repo --feature "JWT auth" --implement

# Clone with adaptation
/learn:clone https://github.com/user/repo --feature "caching" --adapt-to-current

# Clone with testing
/learn:clone https://github.com/user/repo --feature "API validation" --include-tests
```

### Advanced Options
```bash
# Deep learning mode (understands internals)
/learn:clone https://github.com/user/repo --feature "auth" --deep-learning

# Compare implementations
/learn:clone https://github.com/user/repo --feature "caching" --compare-approaches

# Extract patterns only (no implementation)
/learn:clone https://github.com/user/repo --feature "queue" --extract-patterns

# With license attribution
/learn:clone https://github.com/user/repo --feature "parser" --add-attribution
```

## Output Format

### Terminal Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 FEATURE LEARNING COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: JWT Authentication
Source: fastapi/fastapi (MIT License)
Complexity: Medium | Adaptation Required: Yes

Key Components Identified:
• Token generation with configurable expiry
• Dependency injection for auth validation
• Refresh token mechanism

Implementation Strategy:
1. Add python-jose dependency
2. Create auth utility module
3. Implement token generation/validation
4. Add authentication middleware

📄 Full analysis: .claude/reports/learn-clone-jwt-auth-2025-10-29.md
⏱ Analysis completed in 2.8 minutes

Next: Review analysis, then use /dev:auto to implement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Detailed Report

```markdown
═══════════════════════════════════════════════════════
  FEATURE LEARNING REPORT
═══════════════════════════════════════════════════════
Feature: JWT Authentication
Source: https://github.com/fastapi/fastapi
License: MIT (attribution required)
Analysis Date: 2025-10-29

┌─ Feature Overview ───────────────────────────────────┐
│ Feature Name: JWT Authentication System              │
│ Location: fastapi/security/oauth2.py                 │
│ Complexity: Medium                                    │
│ Dependencies: python-jose, passlib                   │
│                                                       │
│ Core Capabilities:                                    │
│ • Access token generation with expiry                │
│ • Refresh token support                              │
│ • Dependency injection for validation                │
│ • Multiple authentication schemes                     │
│ • Token revocation support                           │
└───────────────────────────────────────────────────────┘

┌─ Implementation Analysis ────────────────────────────┐
│ Key Files Analyzed:                                   │
│ • fastapi/security/oauth2.py (core logic)            │
│ • fastapi/security/utils.py (helpers)                │
│ • tests/test_security_oauth2.py (tests)              │
│                                                       │
│ Architecture:                                         │
│ ├─ Token Generation Layer                           │
│ │  • Uses python-jose for JWT encoding              │
│ │  • Configurable algorithms (HS256, RS256)         │
│ │  • Expiry and claims management                   │
│ │                                                     │
│ ├─ Validation Layer                                  │
│ │  • Dependency injection pattern                    │
│ │  • Automatic token extraction from headers        │
│ │  • Validation with error handling                 │
│ │                                                     │
│ └─ Integration Layer                                 │
│    • Middleware for route protection                 │
│    • Flexible authentication schemes                 │
│    • OAuth2 PasswordBearer support                   │
└───────────────────────────────────────────────────────┘

┌─ Code Patterns Extracted ────────────────────────────┐
│ Pattern 1: Token Generation                          │
│ ```python                                            │
│ from jose import jwt                                  │
│ from datetime import datetime, timedelta             │
│                                                       │
│ def create_token(data: dict, expires_delta: timedelta):│
│     to_encode = data.copy()                          │
│     expire = datetime.utcnow() + expires_delta       │
│     to_encode.update({"exp": expire})                │
│     return jwt.encode(to_encode, SECRET_KEY, ALGO)   │
│ ```                                                  │
│                                                       │
│ Pattern 2: Dependency Injection for Auth             │
│ ```python                                            │
│ from fastapi import Depends, HTTPException           │
│ from fastapi.security import OAuth2PasswordBearer    │
│                                                       │
│ oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")│
│                                                       │
│ async def get_current_user(token: str = Depends(oauth2_scheme)):│
│     credentials_exception = HTTPException(...)        │
│     try:                                             │
│         payload = jwt.decode(token, SECRET, ALGO)    │
│         username = payload.get("sub")                │
│         if username is None:                         │
│             raise credentials_exception              │
│         return username                              │
│     except JWTError:                                 │
│         raise credentials_exception                  │
│ ```                                                  │
│                                                       │
│ Pattern 3: Route Protection                           │
│ ```python                                            │
│ @app.get("/users/me")                                │
│ async def read_users_me(current_user: User = Depends(get_current_user)):│
│     return current_user                              │
│ ```                                                  │
└───────────────────────────────────────────────────────┘

┌─ Adaptation Strategy for Current Project ────────────┐
│ Current Project Context:                              │
│ • Type: Claude Code Plugin                           │
│ • Language: Python + Markdown config                 │
│ • Architecture: Agent-based with skills              │
│                                                       │
│ Adaptation Required:                                  │
│ 1. Simplify for plugin context                       │
│    • May not need OAuth2PasswordBearer               │
│    • Focus on token generation/validation            │
│    • Adapt for agent communication                    │
│                                                       │
│ 2. Integration points                                 │
│    • Add to orchestrator for secure agent calls      │
│    • Protect sensitive agent operations              │
│    • Add authentication skill                         │
│                                                       │
│ 3. Dependencies                                       │
│    • Add: python-jose[cryptography]                  │
│    • Add: passlib[bcrypt]                            │
│    • Keep: Lightweight, minimal deps                 │
└───────────────────────────────────────────────────────┘

┌─ Implementation Roadmap ──────────────────────────────┐
│ Phase 1: Core Implementation (2-3 hours)             │
│ Step 1: Add Dependencies                             │
│ ├─ Add python-jose to requirements                   │
│ ├─ Add passlib for password hashing                  │
│ └─ Update lock file                                  │
│                                                       │
│ Step 2: Create Auth Skill                            │
│ ├─ Create skills/authentication/SKILL.md             │
│ ├─ Add JWT token generation patterns                 │
│ ├─ Add validation best practices                     │
│ └─ Add security considerations                       │
│                                                       │
│ Step 3: Implement Token Utilities                    │
│ ├─ Create lib/auth_utils.py                         │
│ ├─ Implement create_token()                         │
│ ├─ Implement validate_token()                       │
│ └─ Add error handling                                │
│                                                       │
│ Phase 2: Integration (1-2 hours)                     │
│ Step 4: Agent Authentication                         │
│ ├─ Add auth to sensitive agent operations            │
│ ├─ Implement token validation middleware             │
│ └─ Add authentication examples                       │
│                                                       │
│ Step 3: Testing (1 hour)                            │
│ ├─ Write unit tests for token utils                 │
│ ├─ Write integration tests                          │
│ └─ Add security tests                                │
│                                                       │
│ Phase 3: Documentation (30 min)                      │
│ ├─ Document auth skill usage                        │
│ ├─ Add examples to README                           │
│ ├─ Add security best practices                      │
│ └─ Include attribution to FastAPI                   │
└───────────────────────────────────────────────────────┘

┌─ Testing Strategy Learned ───────────────────────────┐
│ From Source Repository Tests:                        │
│                                                       │
│ Test Categories:                                      │
│ 1. Token Generation Tests                            │
│    • Valid token creation                            │
│    • Token expiry handling                           │
│    • Custom claims inclusion                         │
│                                                       │
│ 2. Token Validation Tests                            │
│    • Valid token validation                          │
│    • Expired token rejection                         │
│    • Invalid signature detection                     │
│    • Malformed token handling                        │
│                                                       │
│ 3. Integration Tests                                  │
│    • Protected route access with valid token         │
│    • Protected route rejection without token         │
│    • Token refresh flow                              │
│                                                       │
│ Test Implementation Example:                          │
│ ```python                                            │
│ def test_create_access_token():                      │
│     data = {"sub": "user@example.com"}               │
│     token = create_access_token(data)                │
│     assert token is not None                         │
│     payload = jwt.decode(token, SECRET, ALGO)        │
│     assert payload["sub"] == "user@example.com"      │
│     assert "exp" in payload                          │
│ ```                                                  │
└───────────────────────────────────────────────────────┘

┌─ License Compliance ──────────────────────────────────┐
│ Source License: MIT License                           │
│                                                       │
│ Requirements:                                         │
│ ✅ Include original license notice                   │
│ ✅ Include attribution in documentation              │
│ ✅ Do not claim original authorship                  │
│                                                       │
│ Attribution Text (add to README and code files):     │
│                                                       │
│ """                                                  │
│ JWT Authentication implementation learned from:       │
│ FastAPI (https://github.com/tiangolo/fastapi)        │
│ Copyright (c) 2018 Sebastián Ramírez                 │
│ MIT License                                          │
│                                                       │
│ Adapted for Claude Code Plugin with modifications.   │
│ """                                                  │
└───────────────────────────────────────────────────────┘

┌─ Learned Patterns to Store ──────────────────────────┐
│ Pattern: Dependency Injection for Security           │
│ • Effectiveness: 95/100                              │
│ • Reusability: High                                  │
│ • Complexity: Medium                                 │
│ • Store in: .claude-patterns/security-patterns.json │
│                                                       │
│ Pattern: Token-Based Authentication                   │
│ • Effectiveness: 92/100                              │
│ • Reusability: High                                  │
│ • Complexity: Medium                                 │
│ • Store in: .claude-patterns/auth-patterns.json     │
└───────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════
  NEXT STEPS
═══════════════════════════════════════════════════════

Ready to Implement?
• Review implementation roadmap above
• Check license compliance requirements
• Use: /dev:auto "implement JWT authentication based on learned patterns"

Need More Analysis?
• Analyze alternative implementations
• Compare with other auth approaches
• Deep-dive into security considerations

═══════════════════════════════════════════════════════

Analysis Time: 2.8 minutes
Feature Complexity: Medium
Implementation Estimate: 4-6 hours
License: MIT (attribution required)

Learned patterns stored in database for future reference.
```

## Integration with Learning System

Stores learned feature patterns:

```json
{
  "feature_clone_patterns": {
    "feature_name": "jwt_authentication",
    "source_repo": "fastapi/fastapi",
    "source_license": "MIT",
    "patterns_extracted": 3,
    "adaptation_required": true,
    "implemented": false,
    "implementation_approach": "adapted_for_plugin",
    "attribution_added": true
  }
}
```

## Agent Delegation

- **dev-orchestrator**: Coordinates learning and implementation
- **code-analyzer**: Analyzes source implementation
- **pattern-learning**: Extracts and stores patterns
- **security-auditor**: Ensures secure implementation

## Skills Integration

- **code-analysis**: For understanding source code
- **pattern-learning**: For pattern extraction
- **security-patterns**: For secure implementation
- **documentation-best-practices**: For proper attribution

## Use Cases

### Learning Authentication
```bash
/learn:clone https://github.com/fastapi/fastapi --feature "JWT auth"
```

### Learning Caching Strategies
```bash
/learn:clone https://github.com/django/django --feature "caching"
```

### Learning Testing Approaches
```bash
/learn:clone https://github.com/pytest-dev/pytest --feature "test fixtures"
```

## Best Practices

### License Compliance
- Always check and respect source licenses
- Add proper attribution in code and documentation
- Do not copy code verbatim - learn and adapt
- Understand license restrictions before cloning

### Feature Selection
- Choose features that fit project needs
- Consider maintenance burden
- Evaluate complexity vs value
- Check for dependencies

### Implementation
- Adapt to project conventions
- Don't blindly copy - understand first
- Write tests for cloned features
- Document learnings and adaptations

---

**Version**: 1.0.0
**Integration**: Uses dev-orchestrator, code-analyzer agents
**Skills**: code-analysis, pattern-learning, security-patterns
**Platform**: Cross-platform
**Scope**: Learn and adapt features from external repositories
**License**: Enforces proper attribution and compliance
