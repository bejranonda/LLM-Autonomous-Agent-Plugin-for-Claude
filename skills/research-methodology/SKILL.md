---
name: research-methodology
description: Structured research techniques for conducting systematic investigations, multi-step searches, source evaluation, and synthesizing findings with proper citations
version: 1.0.0
---

## Overview

This skill provides comprehensive research methodologies for conducting high-quality, systematic investigations across web sources, documentation, and code. It encompasses planning multi-step research, evaluating source credibility, cross-referencing information, and synthesizing findings into actionable insights.

## Core Research Principles

### 1. Systematic Investigation

**Multi-Step Research Process**:
1. **Define Goal**: Clearly articulate what you need to learn
2. **Map Gaps**: Identify what you don't know
3. **Plan Steps**: Break into specific, answerable questions
4. **Execute Searches**: Systematically gather information
5. **Verify Claims**: Cross-reference and validate
6. **Synthesize**: Combine findings into coherent narrative
7. **Document**: Provide citations and enable verification

**Key Insight from Research Best Practices**:
> "Claude operates agentically, conducting multiple searches that build on each other while determining exactly what to investigate next. It explores different angles of your question automatically and works through open questions systematically."

Apply this by:
- Conducting sequential searches that build on each finding
- Adapting search strategy based on initial results
- Exploring multiple perspectives on each question
- Following information threads to deeper understanding

### 2. Search Strategy Design

**Query Construction**:
```
Bad Query:  "I2C"
Good Query: "I2C vs SPI protocol comparison embedded systems"
Better Query: "I2C vs SPI trade-offs Raspberry Pi hardware communication"
```

**Query Patterns**:
- **Overview Queries**: "[Topic] overview | introduction | basics"
- **Comparison Queries**: "[Option A] vs [Option B] pros cons comparison"
- **Specification Queries**: "[Technology] datasheet | specification | documentation"
- **Problem-Solution Queries**: "[Problem] solution | fix | troubleshooting | best practices"
- **Authority Queries**: "[Topic] site:ieee.org OR site:.edu OR datasheet"

**Progressive Depth**:
1. Start broad: "Authentication methods web applications"
2. Narrow down: "OAuth 2.0 vs JWT authentication Node.js"
3. Get specific: "JWT refresh token rotation best practices security"
4. Verify: "JWT security vulnerabilities OWASP recommendations"

### 3. Source Evaluation Framework

**Source Credibility Hierarchy**:

**Tier 1: Authoritative (90-100 credibility)**
- Official datasheets (manufacturer documentation)
- IEEE, ACM, W3C, IETF standards and papers
- Official language/framework documentation (.org sites)
- Government research (.gov, .edu with peer review)
- Example: NXP TEA5767 datasheet, React official docs

**Tier 2: Reliable (70-89 credibility)**
- High-reputation Stack Overflow answers (high votes, accepted)
- Major tech company engineering blogs (Google, Microsoft, etc.)
- Well-maintained GitHub repositories with documentation
- Established technical publications (Embedded.com, EETimes)
- Example: StackOverflow answer with 200+ upvotes

**Tier 3: Supplementary (50-69 credibility)**
- Medium articles from recognized authors
- Smaller technical blogs with expertise demonstrated
- Forum discussions from specialized communities
- Tutorial sites with recent content
- Example: Medium article by experienced developer

**Tier 4: Questionable (0-49 credibility)**
- Content farms with generic information
- Outdated tutorials (> 5 years old for fast-moving tech)
- Yahoo Answers, Quora (variable quality)
- Sites with no author attribution
- Avoid: W3Schools (known for outdated info)

**Evaluation Criteria**:
- **Authority**: Is the author/publisher an expert in this domain?
- **Recency**: Is the information current? (Check publish date)
- **Peer Review**: Has this been reviewed or validated by others?
- **Citations**: Does the source cite its own sources?
- **Bias**: Are there conflicts of interest or commercial bias?
- **Consistency**: Does this align with other authoritative sources?

### 4. Citation Management

**Proper Citation Format**:
```markdown
**Claim**: "I2C supports multi-master configuration with clock stretching."

**Source**: NXP I2C-bus specification and user manual (UM10204)
**URL**: https://www.nxp.com/docs/en/user-guide/UM10204.pdf
**Section**: Section 3.1.9, Page 10
**Accessed**: 2024-01-15
**Credibility**: Authoritative (manufacturer specification)
```

**Citation Best Practices**:
- Always include URL for web sources
- Note access date (important for changing content)
- Include section/page numbers for long documents
- Provide direct quotes for critical technical claims
- Link claims to specific sources (not generic attribution)
- Verify URLs are accessible before citing

**Red Flags**:
- Claims without any source attribution
- Vague citations like "according to research"
- Broken or inaccessible URLs
- Sources that don't actually support the claim
- Over-reliance on single source

### 5. Cross-Reference Verification

**Triangulation Method**:

For critical technical claims, verify across 3 independent sources:

Example: "I2C maximum speed is 3.4 Mbps (High-Speed mode)"

Source 1: NXP I2C specification (authoritative) ✓
Source 2: Wikipedia I2C article (reliable, cites spec) ✓
Source 3: Embedded.com tutorial (supplementary) ✓

Confidence: **High** (authoritative + 2 reliable sources confirm)

**Handling Contradictions**:

If sources contradict:
1. Identify the most authoritative source
2. Check recency (newer may supersede older)
3. Look for context differences (e.g., different versions)
4. Explicitly note the contradiction in findings
5. Recommend seeking expert clarification if critical

Example:
```
Finding: "I2C pull-up resistor values"
Source A (datasheet): 2.2kΩ - 4.7kΩ recommended
Source B (forum): "Always use 4.7kΩ"

Resolution: Datasheet is authoritative. Resistor value depends on
bus capacitance and speed. 4.7kΩ is common default, but 2.2kΩ may
be needed for high-speed or long traces. Trust datasheet formula.
```

## Research Workflow Patterns

### Pattern 1: Technology Comparison Research

**Use When**: Comparing options (libraries, protocols, architectures)

**Steps**:
1. Define comparison criteria (speed, complexity, compatibility, cost)
2. Research each option independently (avoid comparison articles initially)
3. Build trade-off matrix with sources for each cell
4. Look for authoritative comparisons to validate your matrix
5. Identify use-case recommendations
6. Synthesize with clear "when to use" guidance

**Deliverable**: Trade-off matrix + recommendations with conditions

### Pattern 2: Problem-Solution Research

**Use When**: Debugging, troubleshooting, finding best practices

**Steps**:
1. Precisely define the problem (symptoms, context, constraints)
2. Search for exact error messages or symptoms
3. Find multiple solutions and their trade-offs
4. Verify solutions work in similar contexts
5. Identify root cause if possible
6. Document solution with rationale and caveats

**Deliverable**: Root cause + prioritized solutions with trade-offs

### Pattern 3: Learning Research

**Use When**: Learning a new technology, framework, or concept

**Steps**:
1. Start with official documentation (overview/getting started)
2. Find authoritative tutorials or courses
3. Identify common patterns and best practices
4. Learn anti-patterns and pitfalls to avoid
5. Find real-world examples and case studies
6. Summarize mental model and key principles

**Deliverable**: Mental model + key concepts + resources for deep dive

### Pattern 4: Specification Research

**Use When**: Need exact technical specifications (hardware, protocols, APIs)

**Steps**:
1. Find official datasheet or specification document
2. Extract exact values, constraints, capabilities
3. Cross-reference with manufacturer application notes
4. Look for errata or known issues
5. Find practical implementation examples
6. Document gotchas and edge cases

**Deliverable**: Specification summary + practical considerations

### Pattern 5: Security Research

**Use When**: Evaluating security implications or best practices

**Steps**:
1. Identify security concerns and threat model
2. Consult OWASP guidelines or security frameworks
3. Find CVE reports or known vulnerabilities
4. Research mitigation techniques
5. Cross-reference with current best practices
6. Verify recommendations are current (security evolves fast)

**Deliverable**: Threat assessment + mitigation strategies with sources

## Research Quality Metrics

### Completeness Checklist

- [ ] All research questions answered
- [ ] High-confidence answers for critical questions
- [ ] Alternatives explored (not just first option found)
- [ ] Trade-offs identified and documented
- [ ] Edge cases and limitations noted
- [ ] Recommendations are actionable
- [ ] Sources are authoritative and cited
- [ ] Contradictions resolved or flagged
- [ ] Next steps or gaps clearly identified

### Quality Indicators

**High-Quality Research (80-100)**:
- 3+ authoritative sources for critical claims
- All technical specifications verified
- Trade-offs clearly articulated
- Recommendations have clear conditions
- Citations are precise and accessible
- No unresolved contradictions

**Moderate-Quality Research (60-79)**:
- Mix of authoritative and reliable sources
- Most claims verified
- Basic trade-offs identified
- General recommendations provided
- Citations present but may lack detail
- Minor contradictions noted

**Low-Quality Research (0-59)**:
- Reliance on questionable sources
- Claims not verified
- Missing trade-offs
- Vague or generic recommendations
- Poor citation practices
- Unresolved contradictions

## Common Research Pitfalls

### Pitfall 1: Confirmation Bias
**Problem**: Only searching for information that confirms initial assumptions
**Solution**: Explicitly search for counter-arguments and alternative perspectives

### Pitfall 2: Recency Bias
**Problem**: Assuming newest information is always best
**Solution**: Check if core principles have changed or just implementation details

### Pitfall 3: Authority Bias
**Problem**: Trusting everything from a high-reputation source
**Solution**: Even authoritative sources can have errors; cross-reference critical claims

### Pitfall 4: Depth-Breadth Imbalance
**Problem**: Either too shallow (surface-level) or too deep (rabbit hole)
**Solution**: Define success criteria upfront; know when you have "enough" information

### Pitfall 5: Outdated Information
**Problem**: Using information from 5+ years ago for fast-evolving tech
**Solution**: Always check publication date; prefer last 1-2 years for best practices

### Pitfall 6: Generic Tutorials
**Problem**: Following tutorials that don't match your specific context
**Solution**: Verify tutorial assumptions match your environment (versions, platform, etc.)

### Pitfall 7: Missing Context
**Problem**: Applying advice without understanding when it applies
**Solution**: Always extract the "when to use" and "when NOT to use" conditions

## Research Report Structure

### Executive Summary
- 2-3 sentences: What was researched, key findings, main recommendation

### Research Questions
- List of specific questions addressed

### Key Findings
For each finding:
- **Question**: [Original question]
- **Answer**: [Synthesized answer]
- **Confidence**: High/Medium/Low
- **Sources**: [Cited sources with URLs]
- **Notes**: [Caveats, context, additional details]

### Trade-Off Matrix (if applicable)
| Criterion | Option A | Option B | Winner |
|-----------|----------|----------|--------|
| [criterion] | [details] [[source]] | [details] [[source]] | [Option X] |

### Recommendations
For each recommendation:
- **Recommendation**: [What to do]
- **Rationale**: [Why this is recommended]
- **Conditions**: [When this applies]
- **Alternatives**: [What to do if conditions don't match]
- **Sources**: [Supporting citations]

### Remaining Gaps
- List of unanswered questions or low-confidence findings
- Suggested next steps for additional research

### Sources Consulted
Organized by credibility tier:
- Authoritative sources: [list with URLs]
- Reliable sources: [list with URLs]
- Supplementary sources: [list with URLs]

## Integration with Pattern Learning

After completing research:
1. Store research pattern with topic, sources, and outcomes
2. Track which sources were most valuable
3. Record time spent vs. value gained
4. Note effective search queries for similar future research
5. Learn which research workflow pattern worked best

This enables:
- Faster research on similar topics in future
- Better source selection based on past success
- Improved search query formulation
- Recognition of similar research needs

## When to Apply

Use this skill when:
- Planning comprehensive research investigations
- Need to systematically explore a technical topic
- Evaluating multiple options or approaches
- Verifying technical claims and specifications
- Learning new technologies or frameworks
- Troubleshooting complex problems
- Need to synthesize information from multiple sources
- Required to provide well-cited, credible findings

This methodology ensures high-quality, systematic research that produces reliable, actionable insights with proper attribution and verification.
