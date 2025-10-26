---
name: analyze:dependencies
description: Scan project dependencies for known vulnerabilities across all package managers (Python, npm, Ruby, Go, Rust, Java, PHP, .NET)

delegates-to: orchestrator

# Dependency Vulnerability Scanner

Comprehensive dependency vulnerability scanning across 11 package managers and ecosystems, with CVE database integration and automated fix recommendations.

## Usage

```bash
/analyze:dependencies [PATH] [OPTIONS]
```

**Examples**:
```bash
/analyze:dependencies                  # Scan current project
/analyze:dependencies backend/         # Scan specific directory
/analyze:dependencies --critical-only  # Show only critical vulnerabilities
/analyze:dependencies --with-fixes     # Include upgrade recommendations
```

## Supported Ecosystems

### Python (pip, pipenv, poetry)
**Tools**: pip-audit, safety
**Manifests**: requirements.txt, Pipfile, pyproject.toml, poetry.lock

### JavaScript/Node.js (npm, yarn, pnpm)
**Tools**: npm audit, yarn audit, pnpm audit
**Manifests**: package.json, package-lock.json, yarn.lock, pnpm-lock.yaml

### Ruby (bundler)
**Tools**: bundle-audit
**Manifests**: Gemfile, Gemfile.lock

### PHP (composer)
**Tools**: local-php-security-checker
**Manifests**: composer.json, composer.lock

### Go (go modules)
**Tools**: govulncheck
**Manifests**: go.mod, go.sum

### Rust (cargo)
**Tools**: cargo-audit
**Manifests**: Cargo.toml, Cargo.lock

### Java (maven, gradle)
**Tools**: dependency-check
**Manifests**: pom.xml, build.gradle, build.gradle.kts

### .NET (nuget)
**Tools**: dotnet list package --vulnerable
**Manifests**: packages.config, *.csproj

## How It Works

### 1. Ecosystem Detection

Automatically detects package managers:

```
Detecting Ecosystems...
✅ Python (requirements.txt)
✅ JavaScript (package.json, yarn.lock)
✅ Go (go.mod)
```

### 2. Vulnerability Scanning

Runs appropriate scanners for each ecosystem:

```
Scanning Dependencies...
[████████████] Python    (pip-audit)  - 2.3s
[████████████] npm       (npm audit)  - 4.1s
[████████████] Go        (govulncheck) - 1.8s

Results:
✅ Python:     5 vulnerabilities (2 critical)
✅ npm:        12 vulnerabilities (0 critical)
✅ Go:         0 vulnerabilities
```

### 3. Result Aggregation

Deduplicates and synthesizes results:

```
Aggregating Results...
- Total Vulnerabilities: 15 unique
- Duplicates Removed: 2
- Vulnerable Dependencies: 12/187
```

### 4. Risk Assessment

```
Risk Score (0-100) =
    Critical × 25 +
    High × 15 +
    Medium × 8 +
    Low × 3 +
    Info × 1

Example:
- Critical: 2 → 50 points
- High: 3 → 45 points
- Medium: 7 → 56 points
- Low: 3 → 9 points
---


-----------------------
Total: 160 (capped at 100)
Risk Score: 100/100 (EXTREME)
```

**Risk Levels**:
- 70-100: Extreme/High Risk
- 40-69: Medium Risk
- 0-39: Low Risk

## Output Format

### Terminal Output (Tier 1: Concise Summary)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DEPENDENCY VULNERABILITY SCAN COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Risk Score: 78/100 (HIGH RISK)

📊 Overview
   Total Vulnerabilities: 15
   Vulnerable Dependencies: 12/187 (6.4%)
   Ecosystems: Python, npm, Go

🚨 Vulnerabilities by Severity
   🔴 Critical: 2
   🟠 High: 3
   🟡 Medium: 7
   🔵 Low: 3
   ⚪ Info: 0

📦 By Ecosystem
   Python: 5 vulnerabilities
   npm: 10 vulnerabilities
   Go: 0 vulnerabilities

⚠️  Top 3 Vulnerable Packages
   1. requests (Python) - 2 vulnerabilities
   2. axios (npm) - 3 vulnerabilities
   3. lodash (npm) - 2 vulnerabilities

🔴 Critical Vulnerabilities (2)
   1. CVE-2023-12345 - requests 2.25.1
      SQL injection vulnerability
      Fix: Upgrade to 2.31.0+

   2. CVE-2023-67890 - axios 0.21.1
      Server-side request forgery
      Fix: Upgrade to 1.6.0+

📄 Detailed Report: .reports/dependency-scan-2025-01-15.md

⏱️  Scan completed in 8.2s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### File Report (Tier 2: Comprehensive)

Saved to `.reports/dependency-scan-{DATE}.md`:

```markdown
# Dependency Vulnerability Scan Report
**Generated**: 2025-01-15 16:45:23
**Project**: /project
**Risk Score**: 78/100 (HIGH RISK)

---

## Executive Summary

**Total Vulnerabilities**: 15 unique
**Vulnerable Dependencies**: 12 out of 187 total (6.4%)
**Ecosystems Scanned**: Python, npm, Go
**Scan Duration**: 8.2s

**Risk Assessment**: HIGH RISK
- Immediate action required for 2 critical vulnerabilities
- 3 high-severity issues should be addressed soon
- 7 medium-severity issues for next sprint
- 3 low-severity issues can be deferred

---

## Vulnerabilities by Severity

| Severity | Count | Percentage |
|----------|-------|-----------|
| 🔴 Critical | 2 | 13.3% |
| 🟠 High | 3 | 20.0% |
| 🟡 Medium | 7 | 46.7% |
| 🔵 Low | 3 | 20.0% |
| ⚪ Info | 0 | 0.0% |

---

## Vulnerabilities by Ecosystem

### Python (5 vulnerabilities)
- **Critical**: 1
- **High**: 1
- **Medium**: 2
- **Low**: 1

### npm (10 vulnerabilities)
- **Critical**: 1
- **High**: 2
- **Medium**: 5
- **Low**: 2

### Go (0 vulnerabilities)
- No vulnerabilities detected

---

## Top 10 Vulnerable Packages

| Package | Ecosystem | Vulnerabilities | Severity |
|---------|-----------|----------------|----------|
| axios | npm | 3 | 1 Critical, 2 Medium |
| requests | Python | 2 | 1 Critical, 1 High |
| lodash | npm | 2 | 2 Medium |
| urllib3 | Python | 2 | 1 High, 1 Low |
| ws | npm | 1 | 1 High |
| express | npm | 1 | 1 Medium |
| jinja2 | Python | 1 | 1 Medium |
| moment | npm | 1 | 1 Low |
| pyyaml | Python | 1 | 1 Low |
| react-dom | npm | 1 | 1 Medium |

---

## Critical Vulnerabilities (IMMEDIATE ACTION REQUIRED)

### CVE-2023-12345: SQL Injection in requests
**Package**: requests (Python)
**Installed Version**: 2.25.1
**Severity**: 🔴 CRITICAL
**CVSS Score**: 9.8

**Description**:
SQL injection vulnerability in the `requests` library allows remote attackers to execute arbitrary SQL commands via crafted HTTP requests.

**Impact**:
- Database compromise
- Data exfiltration
- Unauthorized access

**CWE**: CWE-89 (SQL Injection)

**Fixed Versions**: 2.31.0, 2.32.0+

**Remediation**:
```bash
# Python (pip)
pip install --upgrade requests>=2.31.0

# Python (poetry)
poetry update requests
```

**References**:
- https://nvd.nist.gov/vuln/detail/CVE-2023-12345
- https://github.com/psf/requests/security/advisories/GHSA-xxxx

---

### CVE-2023-67890: SSRF in axios
**Package**: axios (npm)
**Installed Version**: 0.21.1
**Severity**: 🔴 CRITICAL
**CVSS Score**: 9.1

**Description**:
Server-side request forgery (SSRF) vulnerability allows attackers to make the server perform requests to arbitrary destinations.

**Impact**:
- Internal network scanning
- Access to internal services
- Data exfiltration from internal endpoints

**CWE**: CWE-918 (SSRF)

**Fixed Versions**: 1.6.0+

**Remediation**:
```bash
# npm
npm install axios@latest

# yarn
yarn upgrade axios@latest
```

**References**:
- https://nvd.nist.gov/vuln/detail/CVE-2023-67890
- https://github.com/axios/axios/security/advisories/GHSA-yyyy

---

## High Severity Vulnerabilities

### CVE-2023-11111: XSS in urllib3
**Package**: urllib3 (Python)
**Installed Version**: 1.26.5
**Severity**: 🟠 HIGH
**CVSS Score**: 7.5

**Description**:
Cross-site scripting vulnerability in URL parsing logic.

**Fixed Versions**: 1.26.18+, 2.0.7+

**Remediation**:
```bash
pip install --upgrade urllib3>=1.26.18
```

---

### CVE-2023-22222: DoS in ws
**Package**: ws (npm)
**Installed Version**: 7.4.5
**Severity**: 🟠 HIGH
**CVSS Score**: 7.5

**Description**:
Denial of service vulnerability via regular expression DoS in WebSocket implementation.

**Fixed Versions**: 7.5.10+, 8.17.1+

**Remediation**:
```bash
npm install ws@latest
```

---

### CVE-2023-33333: Path Traversal in express
**Package**: express (npm)
**Installed Version**: 4.17.1
**Severity**: 🟠 HIGH
**CVSS Score**: 7.3

**Description**:
Path traversal vulnerability allows access to files outside webroot.

**Fixed Versions**: 4.19.2+

**Remediation**:
```bash
npm install express@latest
```

---

## Medium Severity Vulnerabilities

[... 7 medium-severity vulnerabilities with similar detail ...]

---

## Low Severity Vulnerabilities

[... 3 low-severity vulnerabilities with similar detail ...]

---

## Upgrade Recommendations

### Python
```bash
# Upgrade all vulnerable packages
pip install --upgrade \
  requests>=2.31.0 \
  urllib3>=1.26.18 \
  jinja2>=3.1.3 \
  pyyaml>=6.0.1

# Or use requirements file
pip install -r requirements-secure.txt
```

**requirements-secure.txt** (generated):
```
requests>=2.31.0
urllib3>=1.26.18
jinja2>=3.1.3
pyyaml>=6.0.1
```

---

### npm
```bash
# Upgrade all vulnerable packages
npm install \
  axios@latest \
  lodash@latest \
  ws@latest \
  express@latest \
  moment@latest \
  react-dom@latest

# Or auto-fix with npm audit
npm audit fix --force
```

---

## Automated Fix Options

### Safe Auto-Upgrades (Recommended)
These upgrades are backward-compatible (semver minor/patch):

```bash
# Python
pip install --upgrade requests urllib3 pyyaml

# npm
npm audit fix
```

### Manual Review Required
These upgrades may have breaking changes (semver major):

- **axios**: 0.21.1 → 1.6.0 (major version bump)
  - Review: Breaking changes in request config
  - Test: All HTTP client code

- **express**: 4.17.1 → 4.19.2 (minor bump, but middleware changes)
  - Review: Middleware compatibility
  - Test: All routes and error handlers

---

## Dependency Health Summary

### Total Dependencies: 187

**By Ecosystem**:
- Python: 45 packages
- npm: 142 packages
- Go: 0 packages

**Security Status**:
- ✅ Secure: 175 packages (93.6%)
- ⚠️  Vulnerable: 12 packages (6.4%)

**Freshness**:
- Up-to-date: 120 packages (64.2%)
- Minor updates available: 45 packages (24.1%)
- Major updates available: 22 packages (11.8%)

---

## License Compliance

**Detected Licenses**:
- MIT: 95 packages
- Apache-2.0: 32 packages
- BSD-3-Clause: 18 packages
- ISC: 25 packages
- GPL-3.0: 2 packages ⚠️ (Review required)
- Unknown: 15 packages ⚠️ (Investigate)

---

## Risk Score Breakdown

```
Component Scores:
- Critical Vulnerabilities (2 × 25): 50 points
- High Vulnerabilities (3 × 15): 45 points
- Medium Vulnerabilities (7 × 8): 56 points
- Low Vulnerabilities (3 × 3): 9 points
--------------------------------------------
Total: 160 points (capped at 100)

Final Risk Score: 100/100 → Normalized: 78/100
```

**Risk Level**: 🔴 HIGH RISK

**Mitigation**:
1. Fix 2 critical vulnerabilities immediately
2. Fix 3 high vulnerabilities within 48 hours
3. Schedule medium vulnerabilities for next sprint
4. Low vulnerabilities can be deferred

**Estimated Time to Secure**:
- Critical fixes: 2-4 hours
- High fixes: 4-6 hours
- Testing: 8-12 hours
- **Total**: 1-2 days

---

## Action Plan

### Phase 1: Emergency Fixes (Today)
1. Upgrade `requests` to 2.31.0+ (30 min)
2. Upgrade `axios` to 1.6.0+ (45 min + testing)
3. Run test suite (30 min)
4. Deploy hotfix (30 min)

**Total**: 2-3 hours

### Phase 2: High Priority (This Week)
1. Upgrade `urllib3`, `ws`, `express` (2 hours)
2. Run comprehensive tests (4 hours)
3. QA validation (2 hours)
4. Deploy to production (1 hour)

**Total**: 9 hours

### Phase 3: Medium Priority (Next Sprint)
1. Upgrade remaining 7 packages (3 hours)
2. Testing (4 hours)
3. Documentation updates (1 hour)

**Total**: 8 hours

---

## Continuous Monitoring

**Recommendations**:
1. **CI/CD Integration**: Add dependency scanning to pipeline
2. **Weekly Scans**: Schedule automated vulnerability scans
3. **Dependency Updates**: Review updates monthly
4. **Security Alerts**: Subscribe to security advisories

**GitHub Actions Example**:
```yaml
name: Dependency Scan
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  pull_request:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Scan Dependencies
        run: /analyze:dependencies --format=sarif --output=results.sarif
      - name: Upload Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
```

---

## Next Steps

1. ✅ **Review this report** with development team
2. ⚠️  **Create tickets** for each critical/high vulnerability
3. ⚠️  **Schedule fixes** according to action plan
4. ⚠️  **Set up CI/CD** scanning for future PRs
5. ⚠️  **Subscribe** to security advisories for critical packages

---

**End of Report**
```

## Advanced Features

### Critical-Only Mode

```bash
/analyze:dependencies --critical-only
```

Shows only critical vulnerabilities for rapid triage.

### With Fix Recommendations

```bash
/analyze:dependencies --with-fixes
```

Includes detailed upgrade commands and compatibility notes.

### JSON Output for CI/CD

```bash
/analyze:dependencies --format=json --output=scan-results.json
```

Machine-readable format for automation.

### SARIF Output

```bash
/analyze:dependencies --format=sarif
```

Standard format for security tools integration.

## Integration with Learning System

The dependency scanner integrates with pattern learning:

```python
# After each scan
learning_engine.store_pattern({
    "task_type": "dependency_scan",
    "context": {
        "ecosystems": ["python", "npm"],
        "total_dependencies": 187,
        "vulnerable_count": 12
    },
    "outcome": {
        "risk_score": 78,
        "critical_count": 2,
        "high_count": 3
    },
    "trends": {
        "risk_score_delta": -5,  # Improved from last scan
        "new_vulnerabilities": 3,
        "fixed_vulnerabilities": 8
    }
})
```

## Performance Expectations

| Ecosystem | Dependencies | Scan Time |
|-----------|-------------|-----------|
| Python | <50 | 5-15s |
| Python | 50-200 | 15-45s |
| npm | <100 | 10-30s |
| npm | 100-500 | 30-90s |
| Go | <50 | 5-10s |
| Rust | <50 | 10-20s |
| Multi | Mixed | 30-120s |

## Best Practices

1. **Scan Before Deploy**: Always scan before production deployment
2. **Fix Critical First**: Prioritize by severity and exploitability
3. **Test After Upgrade**: Run full test suite after security updates
4. **Monitor Trends**: Track risk score over time
5. **Automate Scanning**: Integrate into CI/CD pipeline
6. **Stay Updated**: Review security advisories weekly
7. **Document Decisions**: Record why certain vulnerabilities are accepted

---

This command provides comprehensive dependency vulnerability scanning with minimal setup and maximum actionable insight.
