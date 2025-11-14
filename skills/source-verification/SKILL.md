---
name: source-verification
description: Citation validation, source credibility assessment, and claim verification techniques for ensuring research quality and accuracy
version: 1.0.0
---

## Overview

This skill provides systematic techniques for verifying research sources, validating citations, assessing credibility, and ensuring claims are properly supported. It ensures research findings are reliable, accurate, and properly attributed.

## Citation Verification Techniques

### 1. URL Accessibility Checking

**Always verify URLs are accessible before citing**:

```python
# Pseudo-code for URL verification
def verify_url_accessible(url: str) -> dict:
    try:
        response = fetch(url, timeout=10)

        if response.status_code == 200:
            return {
                "status": "accessible",
                "severity": "none",
                "title": extract_title(response.content)
            }
        elif response.status_code == 404:
            return {
                "status": "broken-link",
                "severity": "high",
                "recommendation": "Find alternative source"
            }
        elif response.status_code in [301, 302]:
            return {
                "status": "redirected",
                "severity": "low",
                "new_url": response.headers['Location'],
                "recommendation": "Update citation with new URL"
            }
    except TimeoutError:
        return {
            "status": "timeout",
            "severity": "medium",
            "recommendation": "Check URL or try alternative source"
        }
```

**Red Flags**:
- 404 errors → Broken link, find replacement
- Paywall without institutional access → Note access limitations
- Redirect to different domain → Verify legitimacy
- SSL certificate errors → Security concern
- Connection timeouts → Unstable source

### 2. Claim-Source Matching

**Verify that sources actually support the claims made**:

**Verification Process**:
1. Extract specific claim from finding
2. Fetch source content
3. Search for claim in source text
4. Assess support level: FULLY_SUPPORTS | PARTIALLY_SUPPORTS | DOES_NOT_SUPPORT | CONTRADICTS
5. Extract relevant quote as evidence

**Support Levels**:

**FULLY_SUPPORTS**:
- Source explicitly states the claim
- No ambiguity or interpretation needed
- Example: Claim: "TEA5767 operates on I2C bus"
  Source quote: "The TEA5767 uses the I2C bus for communication"

**PARTIALLY_SUPPORTS**:
- Source implies the claim but doesn't state it directly
- Requires minor inference
- Example: Claim: "I2C is slower than SPI"
  Source mentions: "I2C typical speeds 100-400 kHz, SPI can reach 10+ MHz"

**DOES_NOT_SUPPORT**:
- Source doesn't mention the claim
- Different topic entirely
- Citation error (wrong source cited)

**CONTRADICTS**:
- Source explicitly contradicts the claim
- Critical error requiring correction
- Example: Claim: "I2C maximum speed is 1 Mbps"
  Source states: "I2C High-Speed mode reaches 3.4 Mbps"

**Action Matrix**:
| Support Level | Claim Confidence | Action Required |
|---------------|------------------|-----------------|
| FULLY_SUPPORTS | High | ✓ Approve |
| FULLY_SUPPORTS | Medium/Low | Upgrade confidence |
| PARTIALLY_SUPPORTS | High | Downgrade to Medium |
| PARTIALLY_SUPPORTS | Medium | ✓ Approve with note |
| PARTIALLY_SUPPORTS | Low | Find stronger source |
| DOES_NOT_SUPPORT | Any | Remove citation or find correct source |
| CONTRADICTS | Any | **Critical error** - Correct claim immediately |

### 3. Quote Accuracy Verification

**When using direct quotes**:

Checklist:
- [ ] Quote is exact word-for-word match
- [ ] Quote is properly attributed with quotation marks
- [ ] Context is preserved (not misleadingly truncated)
- [ ] Page/section number provided for long documents
- [ ] Ellipsis (...) used correctly for omissions
- [ ] Square brackets [...] used for clarifying insertions

**Bad Example**:
> According to the datasheet, "maximum speed... 3.4 Mbps"
> (Misleading omission: full quote is "maximum speed in High-Speed mode is 3.4 Mbps")

**Good Example**:
> According to the NXP I2C specification (Section 3.1.9), "the maximum speed in High-Speed mode is 3.4 Mbps" [1]

## Source Credibility Assessment

### Domain Reputation Analysis

**Authoritative Domains (Credibility: 90-100)**:

Academic & Standards:
- `.edu` (universities with peer-reviewed content)
- `ieee.org`, `acm.org` (professional organizations)
- `w3.org`, `ietf.org`, `rfc-editor.org` (web/internet standards)
- `iso.org`, `nist.gov` (standards bodies)

Official Documentation:
- `python.org`, `nodejs.org`, `reactjs.org` (official language/framework docs)
- `developer.mozilla.org`, `docs.microsoft.com` (major vendor docs)
- `raspberrypi.org`, `arduino.cc` (hardware platform official docs)

Manufacturer Datasheets:
- `nxp.com`, `ti.com`, `microchip.com`, `analog.com` (semiconductor manufacturers)
- `broadcom.com`, `intel.com` (hardware manufacturers)

**Reliable Domains (Credibility: 70-89)**:

Technical Communities:
- `stackoverflow.com`, `*.stackexchange.com` (if high votes + accepted answer)
- `github.com`, `gitlab.com` (well-maintained repos with docs)

Technical Publications:
- `embedded.com`, `eetimes.com`, `electronicdesign.com`
- `arstechnica.com`, `anandtech.com` (for hardware reviews)

Company Engineering Blogs:
- `engineering.fb.com`, `developers.googleblog.com`, `aws.amazon.com/blogs`
- `netflixtechblog.com`, `eng.uber.com`

**Supplementary Domains (Credibility: 50-69)**:

Developer Platforms:
- `medium.com`, `dev.to`, `hashnode.com` (if author has credentials)
- `youtube.com` (from recognized channels)

Community Forums:
- `reddit.com/r/embedded`, `/r/reactjs` (if high upvotes)
- Specialized forums (check reputation)

**Questionable Domains (Credibility: 0-49)**:

Avoid or verify extensively:
- `answers.yahoo.com`, `quora.com` (variable quality, often outdated)
- `w3schools.com` (known for outdated/incorrect information)
- Content farms: `ehow.com`, `suite101.com`
- Sites with no author attribution
- Sites with excessive ads/popups
- Auto-generated content sites

### Author Expertise Evaluation

**Indicators of Expertise**:
- Academic credentials (PhD, Professor) in relevant field
- Professional experience (10+ years in domain)
- Publications in peer-reviewed journals
- Contributions to open-source projects
- Conference speaker/presenter
- Industry recognition or awards

**Red Flags**:
- No author attribution
- Anonymous or pseudonymous author (unless high community reputation)
- Self-proclaimed "expert" without credentials
- Clickbait titles
- Over-generalized claims
- No citations to sources

### Recency Assessment

**Technology Recency Guidelines**:

| Technology Type | Acceptable Age | Preferred Age |
|----------------|----------------|---------------|
| Framework/Library best practices | < 2 years | < 1 year |
| Security recommendations | < 1 year | < 6 months |
| Hardware protocols (stable) | < 5 years | < 3 years |
| Algorithm fundamentals | Any | Recent explanation |
| Language syntax | Matches version | Current version |
| Build tools/config | < 2 years | < 1 year |

**Recency Penalties**:
- Content > 5 years old for fast-moving tech: **-20 credibility**
- Content > 10 years old: **-40 credibility**
- Security advice > 2 years old: **-30 credibility**

**Exceptions** (timeless content):
- Fundamental algorithms (e.g., sorting, graph theory)
- Mathematical proofs
- Historical context or evolution
- Stable hardware protocols (I2C, SPI specifications from original docs)

### Peer Review & Citations

**Peer-Reviewed Content (Credibility +20)**:
- Academic papers in journals
- Conference proceedings (IEEE, ACM)
- Technical reports with external review

**Well-Cited Content (Credibility +10)**:
- Source cites authoritative references
- Provides evidence for claims
- Links to original sources
- Shows awareness of counterarguments

**No Citations (Credibility -10)**:
- Unsupported opinions
- "Trust me" assertions
- No backing evidence
- Isolated claims

## Contradiction Resolution

### Identifying Contradictions

**Types of Contradictions**:

1. **Factual Contradictions**:
   - Source A: "I2C max speed is 400 kHz"
   - Source B: "I2C max speed is 3.4 Mbps"
   - Resolution: Both correct - different modes (Fast vs High-Speed)

2. **Recommendation Contradictions**:
   - Source A: "Always use 4.7kΩ pull-ups for I2C"
   - Source B: "Use 2.2kΩ for high-speed I2C"
   - Resolution: Context-dependent - resistor value depends on bus speed and capacitance

3. **Opinion Contradictions**:
   - Source A: "React Query is better than Redux"
   - Source B: "Redux is better than React Query"
   - Resolution: Different use cases - clarify when each is appropriate

### Resolution Strategy

**Step 1: Check Context**
- Are sources talking about the same thing?
- Different versions, modes, or configurations?
- Different use cases or constraints?

**Step 2: Evaluate Authority**
- Which source is more authoritative?
- Official documentation > Blog post
- Manufacturer spec > Tutorial
- Peer-reviewed paper > Forum answer

**Step 3: Check Recency**
- Has the recommendation changed over time?
- Is one source outdated?
- Has technology evolved?

**Step 4: Look for Synthesis**
- Can both be true in different contexts?
- Is there a "when to use A vs B" answer?
- What are the conditions that determine the correct approach?

**Step 5: Document Resolution**
```markdown
**Contradiction Detected**:
- Source A (NXP Datasheet): "I2C Fast mode maximum 400 kHz"
- Source B (Wikipedia): "I2C High-Speed mode reaches 3.4 Mbps"

**Resolution**:
Both are correct. I2C has multiple speed modes:
- Standard mode: up to 100 kHz
- Fast mode: up to 400 kHz
- Fast mode Plus: up to 1 MHz
- High-Speed mode: up to 3.4 Mbps

Most common implementation (including Raspberry Pi) supports Fast mode (400 kHz).
High-Speed mode requires additional hardware support.

**Recommendation**: Use "up to 400 kHz (Fast mode)" for typical I2C claims,
note High-Speed capability separately if relevant.
```

## Verification Checklist

### Before Approving Research

Citation Quality:
- [ ] All URLs are accessible (200 OK status)
- [ ] Each claim has at least one supporting source
- [ ] Critical claims have 2+ independent sources
- [ ] Direct quotes are accurate and properly attributed
- [ ] Page/section numbers provided for long documents
- [ ] Access dates noted for all web sources

Source Credibility:
- [ ] Majority of sources are Tier 1 (Authoritative) or Tier 2 (Reliable)
- [ ] No reliance on Tier 4 (Questionable) sources for critical claims
- [ ] Author expertise verified where possible
- [ ] Content recency appropriate for topic
- [ ] Peer-reviewed sources used for scientific claims

Claim Verification:
- [ ] All technical specifications verified against datasheets
- [ ] No contradictions unresolved
- [ ] Numerical values cross-referenced
- [ ] Version/compatibility information confirmed
- [ ] Edge cases and limitations noted

Completeness:
- [ ] All research questions have cited answers
- [ ] Trade-offs are properly sourced
- [ ] Recommendations have supporting evidence
- [ ] Alternative approaches are documented
- [ ] Gaps are clearly identified

## Verification Scoring Matrix

| Category | Weight | Score Calculation |
|----------|--------|-------------------|
| Citation Accessibility | 25% | (accessible_urls / total_urls) * 25 |
| Claim-Source Match | 30% | (supported_claims / total_claims) * 30 |
| Source Credibility | 25% | (avg_source_credibility / 100) * 25 |
| Cross-Reference | 10% | (cross_referenced / critical_claims) * 10 |
| Recency | 10% | (recent_sources / total_sources) * 10 |

**Verification Score** = Sum of all categories (0-100)

**Approval Thresholds**:
- **90-100**: Excellent - High confidence approval
- **80-89**: Good - Approve with minor recommendations
- **70-79**: Acceptable - Approve with improvement suggestions
- **60-69**: Marginal - Conditional approval, address issues
- **Below 60**: Insufficient - Require improvements before approval

## Integration with Research Workflow

**When to Apply Source Verification**:
1. **During Research Execution** (proactive):
   - Verify source credibility before extracting information
   - Check URL accessibility before citing
   - Cross-reference critical claims in real-time

2. **After Research Completion** (validation):
   - Comprehensive citation audit
   - Systematic credibility assessment
   - Contradiction resolution
   - Quality scoring

**Handoff to Validation**:
- Provide verification score
- List critical issues requiring correction
- Identify low-credibility sources needing replacement
- Document resolved contradictions
- Recommend confidence adjustments

## When to Apply

Use this skill when:
- Validating research findings and citations
- Assessing source credibility for critical decisions
- Resolving contradictory information
- Ensuring research quality before publication
- Cross-referencing technical specifications
- Verifying claims against authoritative sources
- Building high-confidence knowledge bases
- Preparing research for peer review or audit

This systematic verification ensures research is reliable, properly attributed, and suitable for informed decision-making.
