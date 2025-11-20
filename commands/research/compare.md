---
name: research:compare
description: Specialized A vs B comparison research with decision matrix, trade-off analysis, and clear recommendations - optimized for choosing between two options
category: research
---

# Compare Research Command - Hybrid Architecture

Specialized A vs B comparison using hybrid approach: **main thread searches web**, **research-executor analyzes and builds decision matrix**, **results validated and presented**.

## Hybrid Comparison Workflow

```
1. Main → WebSearch/WebFetch: Research Option A and Option B
2. Main → research-executor: Analyze, build decision matrix
3. Main → Format and present comparison results
```

## Comparison Research Workflow

### Step 1: Parse Comparison Request (30 seconds)

Extract the two options being compared:
```typescript
// Parse "React vs Vue for e-commerce project"
const optionA = "React"
const optionB = "Vue"
const context = "e-commerce project"

// Identify comparison criteria
const criteria = [
  "Performance", "Developer Experience", "Ecosystem",
  "Learning Curve", "Community Size", "TypeScript Support",
  "State Management", "Build Tooling"
]
```

### Step 2: Research Both Options (Main Thread, 8-12 minutes)

**Your task**: Execute searches for both options.

```typescript
// Search for Option A
const optionA_queries = [
  `${optionA} features pros cons 2025`,
  `${optionA} ${context} best practices`,
  `${optionA} performance benchmarks`
]

const optionA_content = []
for (const query of optionA_queries) {
  const results = WebSearch({ query })
  for (const result of results.slice(0, 4)) {
    const content = WebFetch({
      url: result.url,
      prompt: `Extract information about ${optionA}:
      - Key features and capabilities
      - Strengths and advantages
      - Weaknesses and limitations
      - Performance characteristics
      - Developer experience
      - Community and ecosystem
      - Use cases and best practices

Provide specific, factual information with numbers where possible.`
    })
    optionA_content.push({ url: result.url, title: result.title, content })
  }
}

// Search for Option B (same pattern)
const optionB_content = [] // ... same as above for Option B

// Search for direct comparisons
const comparison_queries = [`${optionA} vs ${optionB} comparison 2025`]
const comparison_content = []
for (const query of comparison_queries) {
  const results = WebSearch({ query })
  for (const result of results.slice(0, 3)) {
    const content = WebFetch({
      url: result.url,
      prompt: `Extract comparison information between ${optionA} and ${optionB}:
      - Side-by-side feature comparison
      - Performance benchmarks
      - When to use each option
      - Migration considerations

Focus on factual comparisons with data.`
    })
    comparison_content.push({ url: result.url, title: result.title, content })
  }
}
```

### Step 3: Build Decision Matrix (Delegate to research-executor)

**Your task**: Pass all fetched content to research-executor for analysis.

```typescript
const analysis = Task({
  subagent_type: "autonomous-agent:research-executor",
  prompt: `Build a decision matrix comparing ${optionA} vs ${optionB} for ${context}.

Fetched Content for ${optionA}:
${optionA_content.map(c => `URL: ${c.url}\nTitle: ${c.title}\nContent: ${c.content}`).join('\n---\n')}

Fetched Content for ${optionB}:
${optionB_content.map(c => `URL: ${c.url}\nTitle: ${c.title}\nContent: ${c.content}`).join('\n---\n')}

Direct Comparisons:
${comparison_content.map(c => `URL: ${c.url}\nTitle: ${c.title}\nContent: ${c.content}`).join('\n---\n')}

Please provide:
1. **Decision Matrix**: Score each option on key criteria (0-10)
   - Performance, Developer DX, Ecosystem, Learning Curve, etc.
   - Justify each score with evidence from sources
2. **Feature Comparison**: Feature-by-feature comparison table
3. **Strengths & Weaknesses**: For each option
4. **Use Case Recommendations**: When to choose A vs B
5. **Overall Recommendation**: Which option for this context, with reasoning
6. **Trade-offs**: Key trade-offs between options

Return format:
{
  "decision_matrix": {
    "criteria": [
      {
        "name": "Performance",
        "optionA_score": 8,
        "optionB_score": 9,
        "winner": "B",
        "analysis": "...",
        "sources": ["url1", "url2"]
      }
    ],
    "total_scores": { "A": 42, "B": 38 }
  },
  "strengths_weaknesses": {
    "optionA": {
      "strengths": ["...", "..."],
      "weaknesses": ["...", "..."]
    },
    "optionB": {
      "strengths": ["...", "..."],
      "weaknesses": ["...", "..."]
    }
  },
  "recommendation": {
    "choice": "A|B|Conditional",
    "reasoning": "...",
    "conditions": {
      "choose_A_if": ["...", "..."],
      "choose_B_if": ["...", "..."]
    }
  },
  "key_tradeoffs": [
    { "factor": "...", "A": "...", "B": "..." }
  ]
}`
})
```

**Agent returns**: Decision matrix and recommendation

### Step 4: Present Results (Main Thread)

**Your task**: Format results in two-tier format.

**Terminal Output** (15-20 lines):
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPARISON: ${optionA} vs ${optionB}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Context: ${context}

Decision Matrix (scored 0-10):

Criterion        | ${optionA} | ${optionB} | Winner
-----------------|------------|------------|--------
${matrix_rows}
-----------------|------------|------------|--------
Total Score      | ${scoreA}  | ${scoreB}  | ${winner}

Recommendation: ${recommendation.choice}
Reason: ${recommendation.reasoning}

Key Trade-offs:
• ${optionA}: ${tradeoff1_A}
• ${optionB}: ${tradeoff1_B}

When to choose ${optionA}: ${condition_A}
When to choose ${optionB}: ${condition_B}

Full Report: .claude/reports/compare-${optionA}-vs-${optionB}-${timestamp}.md
Sources: ${total_sources}
Time: ${elapsed}
```

**File Report** (save to `.claude/reports/compare-[A]-vs-[B]-[timestamp].md`):

```markdown
# Comparison Research: ${optionA} vs ${optionB}

**Context**: ${context}
**Date**: ${date}
**Time Spent**: ${elapsed}
**Sources**: ${total_sources}

---

## Executive Summary

${executiveSummary}

**Recommendation**: ${recommendation.choice}

**Reasoning**: ${recommendation.reasoning}

---

## Decision Matrix

| Criterion | ${optionA} | ${optionB} | Winner | Analysis |
|-----------|------------|------------|--------|----------|
${matrix.criteria.map(c => `| ${c.name} | ${c.optionA_score} | ${c.optionB_score} | ${c.winner} | ${c.analysis} [[sources]] |`).join('\n')}
| **Total** | **${scoreA}** | **${scoreB}** | **${winner}** | |

**Sources**:
${all_sources.map((s, i) => `[${i+1}]: ${s.url}`).join('\n')}

---

## Strengths & Weaknesses

### ${optionA}

**Strengths** ✅:
${strengths_A.map(s => `- ${s}`).join('\n')}

**Weaknesses** ❌:
${weaknesses_A.map(w => `- ${w}`).join('\n')}

### ${optionB}

**Strengths** ✅:
${strengths_B.map(s => `- ${s}`).join('\n')}

**Weaknesses** ❌:
${weaknesses_B.map(w => `- ${w}`).join('\n')}

---

## Use Case Recommendations

### Choose ${optionA} when:
${chooseA_conditions.map(c => `- ${c}`).join('\n')}

### Choose ${optionB} when:
${chooseB_conditions.map(c => `- ${c}`).join('\n')}

---

## Key Trade-offs

${tradeoffs.map(t => `
### ${t.factor}
- **${optionA}**: ${t.A}
- **${optionB}**: ${t.B}
`).join('\n')}

---

## Sources Consulted

${sources.map((s, i) => `${i+1}. [${s.title}](${s.url}) (Accessed: ${s.accessed})`).join('\n')}

---

*Comparison conducted using hybrid architecture: main thread web search + research-executor analysis.*
```

### Step 5: Pattern Learning (Main Thread)

```bash
python lib/exec_plugin_script.py pattern_storage.py --action store \
  --pattern-type research_compare \
  --data '{
    "task_type": "research_compare",
    "options": ["${optionA}", "${optionB}"],
    "category": "${category}",
    "recommendation": "${recommendation.choice}",
    "score_difference": ${scoreDiff},
    "sources_count": ${total_sources},
    "time_taken": "${elapsed}"
  }'
```

## Usage Examples

### Technology Comparisons
```bash
/research:compare "React vs Vue for e-commerce project"
/research:compare "PostgreSQL vs MongoDB for analytics"
/research:compare "TypeScript vs JavaScript for new codebase"
```

### Framework Comparisons
```bash
/research:compare "Next.js vs Remix for SSR"
/research:compare "Express vs Fastify for Node.js API"
/research:compare "Tailwind CSS vs styled-components"
```

### Tool Comparisons
```bash
/research:compare "Webpack vs Vite for React build"
/research:compare "Jest vs Vitest for testing"
/research:compare "Docker vs Podman for containers"
```

### Protocol Comparisons
```bash
/research:compare "I2C vs SPI for Raspberry Pi sensors"
/research:compare "REST vs GraphQL for mobile API"
/research:compare "WebSocket vs Server-Sent Events"
```

## Success Criteria

- Decision matrix with 6-10 criteria
- All scores justified with sources
- Clear recommendation with reasoning
- Conditional guidance (when to choose each)
- File report with comprehensive analysis

## Key Benefits of Hybrid Approach

1. **WebSearch works** - Main thread fetches comparison data
2. **Expert analysis** - research-executor builds decision matrix
3. **Structured output** - Consistent comparison format
4. **Source-backed** - All scores justified with citations

---

**Version**: 2.0.0 (Hybrid architecture with decision matrix analysis)
**Platform**: Cross-platform (Windows, Linux, Mac)
**Architecture**: Main thread (WebSearch) + research-executor (Analysis)
**Dependencies**: WebSearch, WebFetch, Task tool, research-executor agent
