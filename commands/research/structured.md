---
name: research:structured
description: Conduct systematic multi-step research with planning, execution, synthesis, and validation phases - supports technical research, design exploration, idea generation, competitive analysis, and general knowledge gathering
category: research
---

# Structured Research Command - Hybrid Architecture

Execute comprehensive, systematic research investigations using a hybrid approach: **main thread performs web searches**, **specialized agents analyze content and guide the research**.

## Hybrid Architecture

This command uses a feedback loop between main thread (web search) and sub-agents (analysis):

```
1. Main → research-strategist: Create search plan
2. Main → WebSearch/WebFetch: Execute searches
3. Main → research-executor: Analyze content, request refinements
4. LOOP: Main executes refined searches based on agent feedback
5. Main → research-validator: Validate quality
6. Main → Present results
```

## Research Workflow

### Phase 1: Planning (Delegate to research-strategist)

**Your task**: Delegate to research-strategist agent to create the search plan.

```typescript
Task({
  subagent_type: "autonomous-agent:research-strategist",
  prompt: `Create a research plan for: "${user_query}"

Context:
- Research goal: ${user_query}
- Expected output: Comprehensive report with citations
- Time budget: 20-40 minutes

Please provide:
1. Research goal breakdown
2. Key questions to answer (5-10 questions)
3. Search queries for each question (2-3 queries per question)
4. Expected source types (official docs, forums, etc.)
5. Success criteria

Return format:
{
  "research_goal": "...",
  "questions": [
    {
      "question": "...",
      "search_queries": ["...", "..."],
      "expected_sources": ["...", "..."]
    }
  ],
  "success_criteria": ["...", "..."]
}`
})
```

**Agent returns**: Research plan with search queries

### Phase 2: Execute Initial Searches (Main Thread)

**Your task**: Execute WebSearch and WebFetch for each query in the plan.

For each search query from the plan:

```typescript
// Execute web search
const searchResults = WebSearch({
  query: searchQuery,
  blocked_domains: ["content-farms.com"]  // Optional
})

// Fetch top 3-5 results
const fetchedContent = []
for (const result of searchResults.slice(0, 5)) {
  const content = WebFetch({
    url: result.url,
    prompt: `Extract information about: "${question}"

Focus on:
- Key facts and data
- Technical specifications
- Pros/cons and trade-offs
- Best practices
- Citations and references

Provide structured information with sources.`
  })

  fetchedContent.push({
    url: result.url,
    title: result.title,
    content: content
  })
}
```

**Collect all fetched content** before moving to next phase.

### Phase 3: Analysis Loop (Delegate to research-executor)

**Your task**: Pass fetched content to research-executor for analysis and get feedback on what to search next.

```typescript
const analysisResult = Task({
  subagent_type: "autonomous-agent:research-executor",
  prompt: `Analyze the following research content and provide findings + next search requests.

Research Goal: ${research_goal}

Questions to Answer:
${questions.map(q => q.question).join('\n')}

Fetched Content:
${fetchedContent.map(fc => `
URL: ${fc.url}
Title: ${fc.title}
Content: ${fc.content}
`).join('\n---\n')}

Please provide:
1. **Current Findings**: What we've learned so far
   - For each question: current answer, confidence level, sources
2. **Knowledge Gaps**: What's still unclear or missing
3. **Next Search Queries**: Specific searches needed to fill gaps (0-5 queries)
   - If research is complete, return empty array
4. **Overall Status**: "incomplete" or "complete"

Return format:
{
  "findings": [
    {
      "question": "...",
      "answer": "...",
      "confidence": "high|medium|low",
      "sources": ["url1", "url2"]
    }
  ],
  "knowledge_gaps": [
    {
      "gap": "...",
      "importance": "critical|high|medium|low"
    }
  ],
  "next_searches": [
    {
      "query": "...",
      "reason": "why we need this"
    }
  ],
  "status": "incomplete|complete",
  "completion_percentage": 75
}`
})
```

**Agent returns**: Findings + next search queries OR "complete"

### Phase 4: Refinement Loop (Main Thread)

**Your task**: If agent requested more searches, execute them and go back to Phase 3.

```typescript
if (analysisResult.status === "incomplete" && analysisResult.next_searches.length > 0) {
  // Execute refined searches
  for (const nextSearch of analysisResult.next_searches) {
    const refinedResults = WebSearch({ query: nextSearch.query })
    const refinedContent = []

    for (const result of refinedResults.slice(0, 3)) {
      const content = WebFetch({
        url: result.url,
        prompt: `Extract information about: "${nextSearch.reason}"`
      })
      refinedContent.push({ url: result.url, title: result.title, content })
    }
  }

  // Go back to Phase 3 with accumulated content
  // Repeat until agent returns status: "complete"
}
```

**Loop 2-4 times** until research is complete or sufficient.

### Phase 5: Validation (Delegate to research-validator)

**Your task**: Pass all findings to research-validator for quality assessment.

```typescript
const validation = Task({
  subagent_type: "autonomous-agent:research-validator",
  prompt: `Validate this research and calculate quality score.

Research Report:
${JSON.stringify(finalFindings, null, 2)}

Sources Consulted:
${allSources.map(s => `- ${s.url} (${s.title})`).join('\n')}

Please validate:
1. **Citation Coverage**: Are all claims cited?
2. **Source Credibility**: Are sources authoritative/reliable?
3. **Technical Accuracy**: Are technical details specific?
4. **Completeness**: Are all questions answered?
5. **Recommendation Quality**: Are recommendations actionable?

Return format:
{
  "quality_score": 85,
  "grade": "B",
  "issues": [
    {
      "type": "missing_citation|low_credibility|vague_detail",
      "description": "...",
      "severity": "critical|high|medium|low"
    }
  ],
  "source_breakdown": {
    "authoritative": 5,
    "reliable": 8,
    "supplementary": 2
  },
  "recommendations": ["..."]
}`
})
```

**Agent returns**: Quality score and issues

### Phase 6: Report Generation (Main Thread)

**Your task**: Format and present results in two-tier format.

**Terminal Output** (15-20 lines max):
```
[OK] Research completed: ${topic}
Quality Score: ${score}/100 (Grade: ${grade})

Key Findings:
1. ${finding1.answer} [${finding1.confidence}]
2. ${finding2.answer} [${finding2.confidence}]
3. ${finding3.answer} [${finding3.confidence}]

Top Recommendations:
1. ${recommendation1}
2. ${recommendation2}

Full Report: .claude/reports/research-${sanitized_topic}-${timestamp}.md
Sources: ${total} (${authoritative} authoritative, ${reliable} reliable)
Time: ${elapsed} minutes
```

**File Report** (save to `.claude/reports/research-[topic]-[timestamp].md`):

```markdown
# Research Report: ${topic}

**Date**: ${date}
**Quality Score**: ${score}/100 (Grade: ${grade})
**Time Spent**: ${elapsed} minutes
**Sources**: ${total} (${authoritative} authoritative, ${reliable} reliable, ${supplementary} supplementary)

---

## Executive Summary

${executiveSummary}

---

## Key Findings

${findings.map(f => `
### ${f.question}

**Finding**: ${f.answer}

**Confidence**: ${f.confidence}

**Sources**:
${f.sources.map(s => `- [${s.title}](${s.url})`).join('\n')}

**Details**: ${f.details}
`).join('\n---\n')}

---

## Trade-Off Matrix

${tradeOffMatrix}

---

## Recommendations

${recommendations.map(r => `
### ${r.title}

**What**: ${r.action}

**Why**: ${r.rationale}

**When**: ${r.conditions}

**Confidence**: ${r.confidence}

**Sources**: ${r.sources.join(', ')}

**Alternative**: ${r.alternative}
`).join('\n')}

---

## Remaining Knowledge Gaps

${gaps.map(g => `
1. **${g.gap}** (Importance: ${g.importance})
   - Status: ${g.status}
   - Suggested actions: ${g.next_steps}
`).join('\n')}

---

## Sources Consulted

### Authoritative Sources
${authSources.map(s => `1. [${s.title}](${s.url}) (Accessed: ${s.accessed})`).join('\n')}

### Reliable Sources
${reliableSources.map(s => `1. [${s.title}](${s.url}) (Accessed: ${s.accessed})`).join('\n')}

### Supplementary Sources
${suppSources.map(s => `1. [${s.title}](${s.url}) (Accessed: ${s.accessed})`).join('\n')}

---

*Research conducted using hybrid architecture: main thread web search + specialized agent analysis.*
```

### Phase 7: Pattern Learning (Main Thread)

**Your task**: Store research pattern for future optimization.

```bash
python lib/exec_plugin_script.py pattern_storage.py --action store \
  --pattern-type research \
  --data '{
    "task_type": "research_structured",
    "topic": "${topic}",
    "research_type": "${type}",
    "sources_consulted": ${count},
    "quality_score": ${score},
    "search_iterations": ${iterations},
    "time_spent": "${elapsed}",
    "timestamp": "${timestamp}"
  }'
```

## Usage Examples

**Technical Research**:
```
/research:structured "Compare I2C vs SPI protocols for Raspberry Pi"
/research:structured "Authentication best practices for Node.js applications"
/research:structured "React Query v4 to v5 migration patterns"
```

**Design & UX Research**:
```
/research:structured "Modern dashboard design trends and patterns"
/research:structured "Command-line interface UX best practices"
/research:structured "Accessibility best practices for developer tools"
```

**Idea Generation**:
```
/research:structured "Innovative features in AI coding assistants"
/research:structured "Emerging patterns in autonomous agent systems"
```

**Competitive Analysis**:
```
/research:structured "Comparison of code quality and analysis tools"
/research:structured "AI agent plugin marketplace landscape"
```

**General Knowledge**:
```
/research:structured "Best practices for plugin architecture design"
/research:structured "User onboarding strategies for technical products"
```

## Success Criteria

- Quality score >= 70/100
- All claims cited with accessible sources
- Majority of sources authoritative or reliable
- Actionable recommendations provided
- Research pattern stored for learning
- 2-4 search iterations completed
- Agent feedback incorporated

## Key Benefits of Hybrid Approach

1. **WebSearch works** - Main thread has access to WebSearch/WebFetch
2. **Agent expertise** - Specialized agents analyze and guide research
3. **Iterative refinement** - Agents request specific searches to fill gaps
4. **Quality validation** - Dedicated validation agent ensures standards
5. **Pattern learning** - System improves over time

---

**Version**: 2.0.0 (Hybrid architecture with iterative feedback loop)
**Platform**: Cross-platform (Windows, Linux, Mac)
**Architecture**: Main thread (WebSearch) + Sub-agents (Analysis, Validation)
**Dependencies**: WebSearch, WebFetch, Task tool, research agents
