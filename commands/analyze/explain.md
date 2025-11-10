---
name: analyze:explain
description: Explain and analyze task, event, or code without making modifications - read-only review
delegates-to: autonomous-agent:orchestrator
---

# Analyze-Explain Command

## Command: `/analyze:explain`

**Read-only analysis and explanation** - Reviews and explains tasks, events, code, or issues without making any modifications. Perfect for understanding what needs to be done before committing to changes.

**🔍 Pure Analysis Mode:**
- **Zero Modifications**: Absolutely no code changes, no fixes, no commits
- **Comprehensive Explanation**: Detailed breakdown of what, why, and how
- **Impact Analysis**: What would change if task were implemented
- **Risk Assessment**: Potential issues and concerns
- **Recommendation Generation**: Suggested approaches without implementation
- **Learning Integration**: Learns from analysis patterns

## How It Works

1. **Task Understanding**: Analyzes the request or code in detail
2. **Context Gathering**: Examines relevant code, files, and dependencies
3. **Impact Assessment**: Identifies what would be affected by changes
4. **Risk Analysis**: Evaluates potential problems and edge cases
5. **Approach Recommendation**: Suggests optimal implementation strategies
6. **Pattern Learning**: Stores analysis patterns for future reference

## Usage

### Basic Usage
```bash
# Explain a feature request
/analyze:explain "add user authentication with JWT"

# Explain existing code or issue
/analyze:explain "why is the login endpoint failing"

# Explain error or bug
/analyze:explain "investigate memory leak in data processing"

# Explain architectural decision
/analyze:explain "should we use microservices or monolith for this project"
```

### With Context
```bash
# Explain with specific file context
/analyze:explain "how does authentication work in auth/login.py"

# Explain with repository URL
/analyze:explain "analyze authentication approach in https://github.com/user/repo"

# Explain test failures
/analyze:explain "why are these 5 tests failing in test_auth.py"

# Explain performance issue
/analyze:explain "what's causing slow response times in API endpoints"
```

### Advanced Options
```bash
# Detailed technical explanation
/analyze:explain "explain JWT implementation" --detail-level technical

# High-level overview
/analyze:explain "explain authentication system" --detail-level overview

# Include code examples in explanation
/analyze:explain "how to implement caching" --include-examples

# Compare multiple approaches
/analyze:explain "Redis vs Memcached for caching" --compare-approaches
```

## Output Format

### Terminal Output (Concise Summary)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 ANALYSIS COMPLETE - READ-ONLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: "add user authentication with JWT"
Complexity: Medium | Estimated Time: 3-4 hours | Risk Level: Medium

Key Findings:
* No existing authentication system detected
* 8 endpoints would need protection
* JWT library not in dependencies

Critical Considerations:
1. Token storage strategy (localStorage vs httpOnly cookies)
2. Refresh token implementation required
3. Password hashing strategy needed

Recommended Approach:
1. Install python-jose and passlib
2. Implement token generation/validation
3. Add authentication middleware

📄 Full analysis: .claude/reports/explain-auth-jwt-2025-10-29.md
⏱ Analysis completed in 45 seconds
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
* Review full analysis report
* Use /dev:auto "add JWT auth" to implement
* Use /analyze:quality to validate after implementation
```

### Detailed Report (.claude/reports/)

```markdown
=======================================================
  TASK ANALYSIS REPORT - READ-ONLY
=======================================================
Generated: 2025-10-29 16:30:00
Task: "add user authentication with JWT"
Status: ANALYSIS ONLY - NO MODIFICATIONS MADE

+- Task Understanding ---------------------------------+
| Request: Implement JWT-based authentication system   |
|                                                       |
| Requirements Breakdown:                               |
| 1. User registration endpoint                         |
| 2. Login endpoint with JWT token generation          |
| 3. Token validation middleware                        |
| 4. Token refresh mechanism                            |
| 5. Logout functionality (token invalidation)         |
| 6. Protected route implementation                     |
|                                                       |
| Technical Components:                                 |
| * JWT token generation and validation                 |
| * Password hashing (bcrypt/argon2)                   |
| * Token storage strategy                              |
| * Middleware for route protection                     |
| * Refresh token rotation                              |
+-------------------------------------------------------+

+- Current State Analysis -----------------------------+
| Project Type: FastAPI/Flask application              |
| Current Auth: None detected                           |
|                                                       |
| Affected Files (would be modified):                   |
| * main.py - Add auth middleware                       |
| * models.py - Add User model                         |
| * routes/auth.py - New file for auth endpoints       |
| * utils/security.py - New file for JWT/hashing       |
| * requirements.txt - Add dependencies                 |
|                                                       |
| Protected Endpoints (would need auth):                |
| * POST /api/users/profile                            |
| * GET /api/users/me                                   |
| * PUT /api/users/update                              |
| * DELETE /api/users/delete                           |
| * GET /api/admin/*                                    |
| * [3 more endpoints]                                  |
+-------------------------------------------------------+

+- Implementation Impact ------------------------------+
| Estimated Changes:                                    |
| * Files Created: 4 new files                         |
| * Files Modified: 6 existing files                    |
| * Lines Added: ~450-600 lines                        |
| * Dependencies: 3 new packages                        |
|                                                       |
| Breaking Changes:                                     |
| * All protected endpoints require auth header         |
| * Clients must implement token storage               |
| * Login flow changes for existing users              |
|                                                       |
| Database Changes:                                     |
| * New 'users' table required                         |
| * New 'refresh_tokens' table required                |
| * Migration scripts needed                            |
+-------------------------------------------------------+

+- Risk Assessment ------------------------------------+
| Security Risks:                                       |
| * [HIGH] Token storage vulnerabilities               |
| * [HIGH] Password hashing strength                    |
| * [MED]  Token expiration strategy                   |
| * [MED]  Refresh token rotation                      |
| * [LOW]  CORS configuration for auth                 |
|                                                       |
| Technical Risks:                                      |
| * [MED]  Breaking existing API clients               |
| * [MED]  Token validation performance impact         |
| * [LOW]  Database migration complexity               |
|                                                       |
| Operational Risks:                                    |
| * [MED]  User migration to new auth system           |
| * [LOW]  Monitoring and logging requirements         |
+-------------------------------------------------------+

+- Recommended Approaches -----------------------------+
| Approach 1: Standard JWT (Recommended)               |
| +- Pros:                                             |
| |  * Industry standard                               |
| |  * Well-tested libraries available                 |
| |  * Good documentation                              |
| |  * Stateless authentication                        |
| +- Cons:                                             |
| |  * Token revocation complexity                     |
| |  * Larger token size                               |
| +- Libraries:                                        |
| |  * python-jose[cryptography]                       |
| |  * passlib[bcrypt]                                 |
| |  * python-multipart                                |
| +- Estimated Time: 3-4 hours                         |
| +- Complexity: Medium                                |
|                                                       |
| Approach 2: JWT + Redis for Token Blacklist          |
| +- Pros:                                             |
| |  * Token revocation support                        |
| |  * Better security                                 |
| |  * Session management                              |
| +- Cons:                                             |
| |  * Additional infrastructure (Redis)               |
| |  * More complex setup                              |
| |  * Stateful authentication                         |
| +- Estimated Time: 5-6 hours                         |
| +- Complexity: Medium-High                           |
|                                                       |
| Approach 3: OAuth2 with JWT                          |
| +- Pros:                                             |
| |  * OAuth2 standard compliance                      |
| |  * Third-party provider support                    |
| |  * Flexible scope management                       |
| +- Cons:                                             |
| |  * More complex implementation                     |
| |  * Requires additional setup                       |
| +- Estimated Time: 6-8 hours                         |
| +- Complexity: High                                  |
+-------------------------------------------------------+

+- Implementation Steps (if you proceed) --------------+
| Phase 1: Setup & Dependencies (30 min)               |
| 1. Install required packages                         |
| 2. Configure environment variables                    |
| 3. Set up database models                            |
|                                                       |
| Phase 2: Core Auth Logic (90 min)                    |
| 4. Implement password hashing utilities              |
| 5. Create JWT token generation                       |
| 6. Implement token validation                        |
| 7. Add refresh token mechanism                       |
|                                                       |
| Phase 3: Endpoints (60 min)                          |
| 8. Create registration endpoint                      |
| 9. Create login endpoint                             |
| 10. Create token refresh endpoint                    |
| 11. Create logout endpoint                           |
|                                                       |
| Phase 4: Middleware & Protection (45 min)            |
| 12. Implement authentication middleware              |
| 13. Protect existing endpoints                       |
| 14. Add role-based access control (optional)         |
|                                                       |
| Phase 5: Testing & Documentation (45 min)            |
| 15. Write unit tests                                 |
| 16. Write integration tests                          |
| 17. Update API documentation                         |
| 18. Add usage examples                               |
+-------------------------------------------------------+

+- Code Examples (Reference Only) ---------------------+
| Token Generation Example:                            |
|                                                       |
| ```python                                            |
| from jose import jwt                                  |
| from datetime import datetime, timedelta             |
|                                                       |
| def create_access_token(data: dict):                 |
|     to_encode = data.copy()                          |
|     expire = datetime.utcnow() + timedelta(minutes=15)|
|     to_encode.update({"exp": expire})                |
|     return jwt.encode(to_encode, SECRET_KEY, ALGO)   |
| ```                                                  |
|                                                       |
| Middleware Example:                                   |
|                                                       |
| ```python                                            |
| from fastapi import Depends, HTTPException           |
|                                                       |
| async def get_current_user(token: str = Depends(...)):|
|     try:                                             |
|         payload = jwt.decode(token, SECRET_KEY, ALGO)|
|         return payload.get("sub")                    |
|     except JWTError:                                 |
|         raise HTTPException(401, "Invalid token")    |
| ```                                                  |
+-------------------------------------------------------+

+- Configuration Requirements -------------------------+
| Environment Variables Needed:                         |
| * SECRET_KEY - JWT signing key (strong random)       |
| * ALGORITHM - "HS256" (default) or "RS256"           |
| * ACCESS_TOKEN_EXPIRE_MINUTES - 15-30 recommended    |
| * REFRESH_TOKEN_EXPIRE_DAYS - 7-30 recommended       |
|                                                       |
| Database Schema:                                      |
| * users table: id, username, email, password_hash    |
| * refresh_tokens table: token, user_id, expires_at   |
+-------------------------------------------------------+

+- Testing Strategy -----------------------------------+
| Unit Tests Required:                                  |
| * Token generation with valid data                    |
| * Token validation with valid/invalid tokens         |
| * Password hashing and verification                   |
| * Token expiration handling                          |
|                                                       |
| Integration Tests Required:                           |
| * User registration flow                             |
| * Login and token retrieval                          |
| * Protected endpoint access with valid token         |
| * Protected endpoint rejection without token         |
| * Token refresh flow                                 |
| * Logout and token invalidation                      |
+-------------------------------------------------------+

+- Pattern Learning Insights --------------------------+
| Similar Tasks Found: 3 previous auth implementations |
|                                                       |
| Common Success Patterns:                              |
| * Using python-jose over PyJWT (92% success rate)    |
| * Implementing refresh tokens from start (87%)       |
| * Using httpOnly cookies for tokens (84%)            |
|                                                       |
| Common Pitfalls to Avoid:                            |
| * Weak SECRET_KEY generation (found in 23% of cases) |
| * Missing token expiration (found in 18% of cases)   |
| * No refresh token rotation (found in 31% of cases)  |
|                                                       |
| Learned Optimizations:                                |
| * Cache token validation results (15% faster)        |
| * Use background tasks for token cleanup             |
| * Implement rate limiting on auth endpoints          |
+-------------------------------------------------------+

+- Recommendations Summary ----------------------------+
| 1. [RECOMMENDED] Use Approach 1 (Standard JWT)       |
|    - Best balance of simplicity and security         |
|    - Well-documented and tested                      |
|    - 3-4 hour implementation time                    |
|                                                       |
| 2. Add refresh token mechanism from start            |
|    - Prevents need for later refactoring             |
|    - Better user experience                          |
|                                                       |
| 3. Use httpOnly cookies instead of localStorage      |
|    - More secure against XSS attacks                 |
|    - Industry best practice                          |
|                                                       |
| 4. Implement rate limiting on auth endpoints         |
|    - Prevents brute force attacks                    |
|    - Add from the start                              |
|                                                       |
| 5. Write comprehensive tests                         |
|    - Auth is security-critical                       |
|    - 90%+ coverage recommended                       |
+-------------------------------------------------------+

=======================================================
  NEXT STEPS
=======================================================

Ready to Implement?
* Use: /dev:auto "add JWT authentication with refresh tokens"
* Review: Read this report carefully first
* Prepare: Backup database before migration

Need More Analysis?
* Security review: /validate:security
* Architecture review: /analyze:project
* Compare with existing repos: /analyze:repository <url>

Questions or Concerns?
* Review pattern learning insights above
* Check similar implementations in patterns database
* Consult team for security-critical decisions

=======================================================

Analysis Time: 45 seconds
Pattern Matches: 3 similar tasks
Confidence Level: High (92%)
Recommendation Strength: Strong

NO MODIFICATIONS WERE MADE TO ANY FILES
This is a read-only analysis report.
```

## Integration with Learning System

The `/analyze:explain` command integrates with pattern learning:

**Learning from Analysis**:
- Common task patterns and requirements
- Effective explanation structures
- Risk assessment accuracy
- Recommendation quality
- User follow-through rates

**Pattern Storage**:
```json
{
  "explain_patterns": {
    "task_type": "authentication_jwt",
    "analysis_approach": {
      "breakdown_depth": "detailed",
      "risk_assessment": "comprehensive",
      "approaches_compared": 3,
      "code_examples_included": true
    },
    "outcome": {
      "user_implemented": true,
      "implementation_success": true,
      "analysis_accuracy": 0.95,
      "time_estimate_accuracy": 0.88
    },
    "reuse_count": 8,
    "effectiveness_score": 0.92
  }
}
```

## Agent Delegation

`/analyze:explain` delegates to:
- **orchestrator**: Main analysis coordinator
- **code-analyzer**: Code structure and impact analysis
- **security-auditor**: Security risk assessment
- **pattern-learning**: Similar task pattern matching

## Skills Integration

Auto-loads relevant skills:
- **code-analysis**: For code understanding
- **pattern-learning**: For similar task identification
- **security-patterns**: For security considerations
- **documentation-best-practices**: For clear explanations

## Use Cases

### Before Implementation
```bash
# Understand requirements before coding
/analyze:explain "implement real-time notifications"
# Review the analysis
# Then implement: /dev:auto "implement real-time notifications"
```

### Understanding Existing Code
```bash
# Understand how something works
/analyze:explain "how does the caching system work in cache.py"
```

### Troubleshooting
```bash
# Understand what's wrong before fixing
/analyze:explain "why is the API returning 500 errors"
# Review the analysis
# Then fix: /dev:auto "fix API 500 errors"
```

### Decision Making
```bash
# Compare approaches
/analyze:explain "should we use GraphQL or REST for the new API"
```

### Learning
```bash
# Learn from external repositories
/analyze:explain "how does authentication work in https://github.com/fastapi/fastapi"
```

## Best Practices

### Good Explain Requests
```bash
# Specific and focused
/analyze:explain "explain JWT token refresh mechanism in auth/token.py"

# Clear context provided
/analyze:explain "why are tests failing after adding authentication"

# Decision-oriented
/analyze:explain "compare WebSocket vs Server-Sent Events for real-time updates"
```

### Poor Explain Requests
```bash
# Too vague
/analyze:explain "explain the code"

# Too broad
/analyze:explain "explain everything about the project"

# Not analysis-focused
/analyze:explain "fix all bugs"  # Use /dev:auto instead
```

## Output Options

### Detail Levels

- **overview**: High-level summary (default)
- **technical**: Detailed technical analysis
- **comparison**: Compare multiple approaches
- **security**: Focus on security considerations

### Include Examples

```bash
# With code examples
/analyze:explain "JWT implementation" --include-examples

# Without code examples (faster)
/analyze:explain "JWT implementation" --no-examples
```

## Performance Metrics

- **Analysis Time**: 30-90 seconds typically
- **Accuracy**: 90-95% for requirement understanding
- **Time Estimates**: ±20% accuracy
- **Risk Identification**: 85-90% of critical risks identified

---

**Version**: 1.0.0
**Integration**: Uses orchestrator, code-analyzer, security-auditor agents
**Skills**: code-analysis, pattern-learning, security-patterns
**Platform**: Cross-platform (Windows, Linux, Mac)
**Learning**: Full integration with pattern learning system
**Mode**: READ-ONLY - No modifications ever made
