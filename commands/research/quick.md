---
name: research:quick
description: Fast research for quick answers without full planning and validation - ideal for straightforward lookups and simple comparisons
category: research
---

# Quick Research Command - Hybrid Architecture

Fast research for quick answers using simplified hybrid approach: **main thread searches web**, **result is immediately presented** (no iterative loop for speed).

## Simplified Hybrid for Speed

```
1. Main → WebSearch/WebFetch: Execute 2-4 targeted searches
2. Main → Synthesize and present results immediately
3. (No planning, no validation, no iteration - just fast lookup)
```

## Quick Research Workflow

### Step 1: Identify Key Question (30 seconds)

Parse user query into 1-3 specific search queries:
- What's the core question?
- What specific information is needed?
- What format (version, comparison, how-to)?

### Step 2: Execute Targeted Searches (2-5 minutes)

**Your task**: Execute 2-4 focused WebSearch queries and fetch top results.

**Search Strategy**:
```typescript
// Version check example
const queries = [
  "Next.js latest version 2025",
  "Next.js 15 new features"
]

const allResults = []

for (const query of queries) {
  const searchResults = WebSearch({ query })

  // Fetch top 3 results per query
  for (const result of searchResults.slice(0, 3)) {
    const content = WebFetch({
      url: result.url,
      prompt: `Extract key information about: ${user_query}

Focus on:
- Direct answer to question
- Specific facts and numbers
- Key points (3-4 max)
- Source credibility

Be concise - extract only essentials.`
    })

    allResults.push({
      url: result.url,
      title: result.title,
      content: content
    })
  }
}
```

**Source Priority** (for speed):
1. **Official docs** → Most reliable, check first
2. **Stack Overflow** → For how-to and comparisons
3. **GitHub releases** → For version information
4. **Tech blogs** → For comparisons and best practices

### Step 3: Synthesize Answer (1 minute)

**Your task**: Combine results into concise answer.

Extract from fetched content:
- **Direct answer**: 2-3 sentences answering the question
- **Key points**: 3-4 specific facts/details
- **Sources**: URLs used (2-5 max)

### Step 4: Present Results (Terminal Only)

**Format** (10 lines max):
```
[OK] Quick Research: ${topic}

Answer:
${concise 2-3 sentence answer}

Key Points:
1. ${specific point 1}
2. ${specific point 2}
3. ${specific point 3}

Sources: ${url1}, ${url2}, ${url3}
Time: ${elapsed}
```

**No file report** - terminal only for speed.

## Usage Examples

### Version Checks
```bash
/research:quick "Latest React version"
/research:quick "Node.js LTS version 2025"
/research:quick "Python 3.12 new features"
```

### Quick Comparisons
```bash
/research:quick "TypeScript vs JavaScript for new project"
/research:quick "PostgreSQL vs MySQL performance"
/research:quick "REST vs GraphQL quick comparison"
```

### Documentation Lookups
```bash
/research:quick "How to use React useEffect hook"
/research:quick "Docker compose networking setup"
/research:quick "Git rebase vs merge when to use"
```

## Example Outputs

### Example 1: Version Check
```
[OK] Quick Research: Latest Next.js version

Answer:
Next.js 15.1.0 (released January 2025) is the latest stable version.
Introduces Turbopack stable, improved Server Components, and partial
prerendering for hybrid static/dynamic pages.

Key Points:
1. Turbopack production-ready (5x faster than Webpack)
2. Enhanced Server Actions with better error handling
3. Partial Prerendering for mixed content types
4. ~20% reduction in client JavaScript bundle size

Sources: nextjs.org/blog, vercel.com/blog, github.com/vercel/next.js
Time: 38 seconds
```

### Example 2: Quick Comparison
```
[OK] Quick Research: Vite vs Webpack

Answer:
Vite provides 10x faster dev server with instant HMR and simpler
configuration, while Webpack offers more mature ecosystem and
finer control over production optimization.

Key Points:
1. Vite: Instant dev server, ESM-native, simple config
2. Webpack: Mature plugins, complex config, battle-tested
3. Recommendation: Vite for new projects, Webpack for legacy
4. Migration effort: Moderate (config rewrite needed)

Sources: vitejs.dev, webpack.js.org, blog.logrocket.com
Time: 45 seconds
```

## Comparison with Other Commands

| Feature | /research:quick | /research:structured | /research:compare |
|---------|-----------------|---------------------|-------------------|
| Speed | ✅ 1-5 min | ⏱️ 20-40 min | ⏱️ 10-20 min |
| Depth | Basic | Comprehensive | Focused |
| File Report | ❌ No | ✅ Yes | ✅ Yes |
| Quality Score | ❌ No | ✅ Yes | ❌ No |
| Iteration Loop | ❌ No | ✅ Yes (2-4x) | Partial |
| Best For | Quick answers | Deep research | A vs B choices |

## Best Practices

**Good Use Cases**:
- ✅ "What is X?"
- ✅ "Latest version of X"
- ✅ "X vs Y quick comparison"
- ✅ "How to do X"
- ✅ "Best practices for X"

**Use /research:structured instead for**:
- ❌ Complex decisions requiring deep analysis
- ❌ Research needing formal citations
- ❌ Multi-faceted investigations
- ❌ Quality-validated research

---

**Version**: 2.0.0 (Hybrid architecture - main thread only, no iteration)
**Platform**: Cross-platform (Windows, Linux, Mac)
**Architecture**: Main thread (WebSearch + immediate synthesis)
**Dependencies**: WebSearch, WebFetch tools
