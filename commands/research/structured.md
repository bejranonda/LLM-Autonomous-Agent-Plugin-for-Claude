---
description: Conduct systematic multi-step research with planning, execution, synthesis, and validation phases - supports technical research, design exploration, idea generation, competitive analysis, and general knowledge gathering
category: research
---

# Structured Research Command

Execute comprehensive, systematic research investigations across all domains—technical, creative, strategic, and general—with automatic planning, source verification, and synthesis.

## Research Types Supported

- **Technical Research**: Specifications, protocols, implementations, comparisons
- **Design & UX Research**: Visual trends, interface patterns, user experience best practices
- **Idea Generation**: Innovative features, emerging technologies, market opportunities
- **Competitive Analysis**: Market landscape, positioning, feature comparison
- **General Knowledge**: Concepts, best practices, learning resources, project improvement

## Workflow

1. **Planning Phase** (research-strategist):
   - Analyze research goal and context
   - Identify knowledge gaps
   - Break into specific research steps
   - Design search strategy

2. **Execution Phase** (research-executor):
   - Execute systematic web searches
   - Gather information from authoritative sources
   - Cross-reference findings
   - Build comprehensive research report with citations

3. **Validation Phase** (research-validator):
   - Verify all citations are accessible
   - Assess source credibility
   - Cross-check technical claims
   - Calculate quality score (0-100)

4. **Synthesis** (research-executor):
   - Create trade-off matrix if applicable
   - Generate actionable recommendations
   - Identify remaining gaps
   - Provide next steps

## Output

**Terminal (Concise)**:
```
[OK] Research completed: [Topic]
Quality Score: [X]/100 (Grade: [A-F])

Key Findings:
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

Top Recommendation: [Main recommendation]

Full Report: .claude/reports/research-[topic]-[timestamp].md
Time: [X] minutes
```

**File (Comprehensive)**:
- Executive summary
- All findings with citations
- Trade-off matrices
- Detailed recommendations
- Source credibility analysis
- Remaining gaps and next steps

## Usage Examples

**Technical Research**:
```
/autonomous-agent:research:structured "Compare I2C vs SPI protocols for Raspberry Pi"
/autonomous-agent:research:structured "Authentication best practices for Node.js applications"
/autonomous-agent:research:structured "React Query v4 to v5 migration patterns"
```

**Design & UX Research**:
```
/autonomous-agent:research:structured "Modern dashboard design trends and patterns"
/autonomous-agent:research:structured "Command-line interface UX best practices"
/autonomous-agent:research:structured "Accessibility best practices for developer tools"
```

**Idea Generation**:
```
/autonomous-agent:research:structured "Innovative features in AI coding assistants"
/autonomous-agent:research:structured "Emerging patterns in autonomous agent systems"
/autonomous-agent:research:structured "Novel approaches to code quality automation"
```

**Competitive Analysis**:
```
/autonomous-agent:research:structured "Comparison of code quality and analysis tools"
/autonomous-agent:research:structured "AI agent plugin marketplace landscape"
/autonomous-agent:research:structured "Developer productivity tools feature comparison"
```

**General Knowledge**:
```
/autonomous-agent:research:structured "Best practices for plugin architecture design"
/autonomous-agent:research:structured "Pattern learning systems in software development"
/autonomous-agent:research:structured "User onboarding strategies for technical products"
```

## Success Criteria

- Quality score >= 70/100
- All claims properly cited with accessible sources
- Majority of sources are authoritative or reliable
- Actionable recommendations provided
- Research pattern stored for future learning
